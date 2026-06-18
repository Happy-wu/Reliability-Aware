from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
import torch.nn.functional as F


RELIABILITY_COMPONENTS = ("degree", "local_similarity", "neighbor_variance", "rwse")


@dataclass
class GraphData:
    x: torch.Tensor
    y: torch.Tensor
    edge_index: torch.Tensor
    reliability: torch.Tensor
    reliability_gate: torch.Tensor
    reliability_qk: torch.Tensor
    reliability_gate_raw: torch.Tensor
    reliability_qk_raw: torch.Tensor
    train_mask: torch.Tensor
    val_mask: torch.Tensor
    test_mask: torch.Tensor
    local_similarity: torch.Tensor


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def make_synthetic_graph(
    num_nodes: int = 900,
    num_classes: int = 3,
    feature_dim: int = 32,
    graph_type: str = "heterophily",
    p_in: float | None = None,
    p_out: float | None = None,
    feature_noise: float = 0.7,
    edge_noise: float = 0.0,
    seed: int = 0,
    rw_steps: int = 4,
) -> GraphData:
    """Create a small stochastic-block graph for quick node-classification tests.

    graph_type controls the class-to-class edge pattern:
    - homophily: intra-class edges dominate
    - heterophily: inter-class edges dominate
    - mixed: moderately noisy local structure
    - noisy: homophilic graph plus random feature and edge corruption
    """
    if graph_type not in {"homophily", "heterophily", "mixed", "noisy"}:
        raise ValueError(f"Unknown graph_type: {graph_type}")

    set_seed(seed)
    rng = np.random.default_rng(seed)

    y_np = np.arange(num_nodes) % num_classes
    rng.shuffle(y_np)

    centers = rng.normal(0.0, 1.0, size=(num_classes, feature_dim))
    centers = centers / (np.linalg.norm(centers, axis=1, keepdims=True) + 1e-12)
    x_np = centers[y_np] + feature_noise * rng.normal(size=(num_nodes, feature_dim))

    if graph_type == "homophily":
        p_in = 0.035 if p_in is None else p_in
        p_out = 0.004 if p_out is None else p_out
    elif graph_type == "heterophily":
        p_in = 0.004 if p_in is None else p_in
        p_out = 0.024 if p_out is None else p_out
    elif graph_type == "mixed":
        p_in = 0.020 if p_in is None else p_in
        p_out = 0.014 if p_out is None else p_out
    else:
        p_in = 0.030 if p_in is None else p_in
        p_out = 0.006 if p_out is None else p_out

    src: list[int] = []
    dst: list[int] = []
    for i in range(num_nodes):
        labels_equal = y_np[i + 1 :] == y_np[i]
        probs = np.where(labels_equal, p_in, p_out)
        hits = rng.random(num_nodes - i - 1) < probs
        js = np.nonzero(hits)[0] + i + 1
        src.extend([i] * len(js))
        dst.extend(js.tolist())

    if edge_noise > 0 or graph_type == "noisy":
        random_edges = int((edge_noise if edge_noise > 0 else 0.01) * num_nodes * num_nodes)
        noise_src = rng.integers(0, num_nodes, size=random_edges)
        noise_dst = rng.integers(0, num_nodes, size=random_edges)
        keep = noise_src != noise_dst
        src.extend(noise_src[keep].tolist())
        dst.extend(noise_dst[keep].tolist())

    if graph_type == "noisy":
        corrupt = rng.random(num_nodes) < 0.20
        x_np[corrupt] = rng.normal(size=(corrupt.sum(), feature_dim))

    if not src:
        raise RuntimeError("Generated graph has no edges. Increase p_in or p_out.")

    edge_index_np = unique_directed_edges(np.array([src + dst, dst + src], dtype=np.int64))
    edge_index = torch.from_numpy(edge_index_np)
    x = torch.tensor(x_np, dtype=torch.float32)
    y = torch.tensor(y_np, dtype=torch.long)

    train_mask, val_mask, test_mask = stratified_masks(y, seed=seed)
    reliability_gate, reliability_qk, local_similarity = compute_reliability_features(
        x=x,
        edge_index=edge_index,
        num_nodes=num_nodes,
        rw_steps=rw_steps,
    )

    return GraphData(
        x=x,
        y=y,
        edge_index=edge_index,
        reliability=reliability_gate,
        reliability_gate=reliability_gate,
        reliability_qk=reliability_qk,
        reliability_gate_raw=reliability_gate.clone(),
        reliability_qk_raw=reliability_qk.clone(),
        train_mask=train_mask,
        val_mask=val_mask,
        test_mask=test_mask,
        local_similarity=local_similarity,
    )


def select_reliability_components(
    data: GraphData,
    components: list[str] | tuple[str, ...],
) -> GraphData:
    selected = set(components)
    unknown = selected.difference(RELIABILITY_COMPONENTS)
    if unknown:
        raise ValueError(f"Unknown reliability components: {sorted(unknown)}")
    if not selected:
        raise ValueError("At least one reliability component must be selected")

    gate_mask = data.reliability_gate.new_zeros(data.reliability_gate.size(1))
    qk_mask = data.reliability_qk.new_zeros(data.reliability_qk.size(1))

    if "degree" in selected:
        gate_mask[0] = 1.0
        qk_mask[0] = 1.0
    if "local_similarity" in selected:
        gate_mask[1] = 1.0
    if "neighbor_variance" in selected:
        gate_mask[2] = 1.0
    if "rwse" in selected:
        gate_mask[3:] = 1.0
        qk_mask[1:] = 1.0

    data.reliability_gate = data.reliability_gate * gate_mask.unsqueeze(0)
    data.reliability_qk = data.reliability_qk * qk_mask.unsqueeze(0)
    data.reliability = data.reliability_gate
    return data


def stratified_masks(
    y: torch.Tensor,
    train_per_class: int = 30,
    val_per_class: int = 60,
    seed: int = 0,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    rng = np.random.default_rng(seed)
    num_nodes = y.numel()
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)

    for cls in torch.unique(y).tolist():
        idx = torch.nonzero(y == cls, as_tuple=False).view(-1).cpu().numpy()
        rng.shuffle(idx)
        cls_count = len(idx)
        cls_train = min(train_per_class, max(1, int(0.2 * cls_count)))
        cls_val = min(val_per_class, max(1, int(0.2 * cls_count)))
        if cls_train + cls_val >= cls_count:
            cls_train = max(1, int(0.4 * cls_count))
            cls_val = max(1, int(0.2 * cls_count))
        train_idx = idx[:cls_train]
        val_idx = idx[cls_train : cls_train + cls_val]
        test_idx = idx[cls_train + cls_val :]
        train_mask[torch.from_numpy(train_idx)] = True
        val_mask[torch.from_numpy(val_idx)] = True
        test_mask[torch.from_numpy(test_idx)] = True

    return train_mask, val_mask, test_mask


def compute_reliability_features(
    x: torch.Tensor,
    edge_index: torch.Tensor,
    num_nodes: int,
    rw_steps: int = 4,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    src, dst = edge_index
    device = x.device

    deg = torch.bincount(src, minlength=num_nodes).float().to(device)
    deg_log = torch.log1p(deg)
    deg_feat = standardize(deg_log).unsqueeze(1)

    x_norm = F.normalize(x, p=2, dim=-1)
    edge_cos = (x_norm[src] * x_norm[dst]).sum(dim=-1)
    sim_sum = torch.zeros(num_nodes, device=device).scatter_add_(0, src, edge_cos)
    local_sim = sim_sum / deg.clamp_min(1.0)
    local_sim_feat = standardize(local_sim).unsqueeze(1)

    neigh_sum = torch.zeros_like(x).scatter_add_(
        0, src.unsqueeze(-1).expand(-1, x.size(1)), x[dst]
    )
    neigh_mean = neigh_sum / deg.clamp_min(1.0).unsqueeze(1)
    centered_sq = (x[dst] - neigh_mean[src]).pow(2)
    var_sum = torch.zeros_like(x).scatter_add_(
        0, src.unsqueeze(-1).expand(-1, x.size(1)), centered_sq
    )
    neigh_var = (var_sum / deg.clamp_min(1.0).unsqueeze(1)).mean(dim=-1)
    neigh_var_feat = standardize(neigh_var).unsqueeze(1)

    rwse = random_walk_return_features(edge_index, num_nodes, rw_steps=rw_steps, device=device)
    reliability_gate = torch.cat([deg_feat, local_sim_feat, neigh_var_feat, rwse], dim=1)
    reliability_qk = torch.cat([deg_feat, rwse], dim=1)
    reliability_gate = torch.nan_to_num(reliability_gate, nan=0.0, posinf=0.0, neginf=0.0)
    reliability_qk = torch.nan_to_num(reliability_qk, nan=0.0, posinf=0.0, neginf=0.0)
    return reliability_gate, reliability_qk, local_sim


def unique_directed_edges(edge_index_np: np.ndarray) -> np.ndarray:
    if edge_index_np.shape[1] == 0:
        return edge_index_np
    edge_index_np = np.unique(edge_index_np, axis=1)
    order = np.lexsort((edge_index_np[1], edge_index_np[0]))
    return edge_index_np[:, order]


def random_walk_return_features(
    edge_index: torch.Tensor,
    num_nodes: int,
    rw_steps: int,
    device: torch.device,
) -> torch.Tensor:
    src, dst = edge_index.to(device)
    deg = torch.bincount(src, minlength=num_nodes).float().clamp_min(1.0).to(device)
    values = 1.0 / deg[src]
    adj = torch.sparse_coo_tensor(
        torch.stack([src, dst]),
        values,
        size=(num_nodes, num_nodes),
        device=device,
    ).coalesce()

    dense = adj.to_dense()
    power = dense
    outs = []
    for _ in range(rw_steps):
        outs.append(torch.diagonal(power).unsqueeze(1))
        power = power @ dense
    return standardize(torch.cat(outs, dim=1))


def standardize(x: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    return (x - x.mean(dim=0, keepdim=True)) / (
        x.std(dim=0, keepdim=True, unbiased=False) + eps
    )


def add_self_loops(edge_index: torch.Tensor, num_nodes: int) -> torch.Tensor:
    loops = torch.arange(num_nodes, device=edge_index.device)
    loops = torch.stack([loops, loops], dim=0)
    return torch.cat([edge_index, loops], dim=1)


def normalized_adjacency(edge_index: torch.Tensor, num_nodes: int) -> torch.Tensor:
    edge_index = add_self_loops(edge_index, num_nodes)
    row, col = edge_index
    deg = torch.bincount(row, minlength=num_nodes).float().to(edge_index.device)
    deg_inv_sqrt = deg.clamp_min(1.0).pow(-0.5)
    values = deg_inv_sqrt[row] * deg_inv_sqrt[col]
    return torch.sparse_coo_tensor(
        edge_index,
        values,
        size=(num_nodes, num_nodes),
        device=edge_index.device,
    ).coalesce()
