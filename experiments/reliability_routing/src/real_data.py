from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch

from .data import GraphData, standardize


REAL_DATASETS = ("Cora", "Citeseer", "Pubmed", "Chameleon", "Squirrel", "Actor")
EDGE_PROTOCOLS = ("undirected", "source_to_target", "target_to_source")


@dataclass(frozen=True)
class DatasetExpectation:
    num_nodes: int
    num_edges: int
    num_features: int
    num_classes: int
    num_splits: int
    source: str
    source_url: str


EXPECTED_DATASETS = {
    "Cora": DatasetExpectation(2708, 10556, 1433, 7, 1, "PyG Planetoid", "https://github.com/kimiyoung/planetoid"),
    "Citeseer": DatasetExpectation(3327, 9104, 3703, 6, 1, "PyG Planetoid", "https://github.com/kimiyoung/planetoid"),
    "Pubmed": DatasetExpectation(19717, 88648, 500, 3, 1, "PyG Planetoid", "https://github.com/kimiyoung/planetoid"),
    "Chameleon": DatasetExpectation(2277, 36101, 2325, 5, 10, "PyG WikipediaNetwork Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    "Squirrel": DatasetExpectation(5201, 217073, 2089, 5, 10, "PyG WikipediaNetwork Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
    "Actor": DatasetExpectation(7600, 30019, 932, 5, 10, "PyG Actor/Geom-GCN", "https://github.com/graphdml-uiuc-jlu/geom-gcn"),
}


def require_pyg() -> None:
    try:
        import torch_geometric  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "PyTorch Geometric is required for real datasets. "
            "Install it in the server environment before running this script."
        ) from exc


def load_and_validate_dataset(
    name: str,
    root: Path,
    allow_download: bool = True,
) -> tuple[object, dict[str, object]]:
    require_pyg()
    if name not in REAL_DATASETS:
        raise ValueError(f"Unknown real dataset: {name}")

    dataset = load_pyg_dataset(name, root, allow_download)
    data = dataset[0]
    report = validate_pyg_data(name, dataset, data)
    return data, report


def load_pyg_dataset(name: str, root: Path, allow_download: bool) -> object:
    from torch_geometric.datasets import Actor, Planetoid, WikipediaNetwork

    if not allow_download and not dataset_has_local_files(name, root):
        raise FileNotFoundError(
            f"{name} is not present under {root}. Re-run without --no-download."
        )

    if name in {"Cora", "Citeseer", "Pubmed"}:
        pyg_name = existing_planetoid_name(name, root)
        return Planetoid(root=str(root), name=pyg_name, split="public")
    if name in {"Chameleon", "Squirrel"}:
        return WikipediaNetwork(
            root=str(root),
            name=name.lower(),
            geom_gcn_preprocess=True,
        )
    return Actor(root=str(root / "Actor"))


def existing_planetoid_name(name: str, root: Path) -> str:
    aliases = {
        "Cora": ("Cora",),
        "Citeseer": ("Citeseer", "CiteSeer"),
        "Pubmed": ("Pubmed", "PubMed"),
    }
    for candidate in aliases[name]:
        if (root / candidate).exists():
            return candidate
    return name


def dataset_has_local_files(name: str, root: Path) -> bool:
    aliases = {
        "Cora": ("Cora",),
        "Citeseer": ("Citeseer", "CiteSeer"),
        "Pubmed": ("Pubmed", "PubMed"),
        "Chameleon": ("chameleon", "Chameleon"),
        "Squirrel": ("squirrel", "Squirrel"),
        "Actor": ("Actor",),
    }
    return any((root / candidate).exists() for candidate in aliases[name])


def validate_pyg_data(name: str, dataset: object, data: object) -> dict[str, object]:
    expected = EXPECTED_DATASETS[name]
    errors: list[str] = []

    actual = {
        "num_nodes": int(data.num_nodes),
        "num_edges": int(data.edge_index.size(1)),
        "num_features": int(data.x.size(1)),
        "num_classes": int(torch.unique(data.y).numel()),
        "num_splits": mask_split_count(data.train_mask),
    }
    for field in ("num_nodes", "num_edges", "num_features", "num_classes", "num_splits"):
        expected_value = getattr(expected, field)
        if actual[field] != expected_value:
            errors.append(f"{field}: expected {expected_value}, got {actual[field]}")

    if data.x.size(0) != data.num_nodes or data.y.numel() != data.num_nodes:
        errors.append("Node feature/label count does not match num_nodes")
    if data.edge_index.dim() != 2 or data.edge_index.size(0) != 2:
        errors.append("edge_index must have shape [2, num_edges]")
    if data.edge_index.numel() and (
        int(data.edge_index.min()) < 0 or int(data.edge_index.max()) >= data.num_nodes
    ):
        errors.append("edge_index contains out-of-range node indices")
    if not torch.isfinite(data.x).all():
        errors.append("Node features contain NaN or Inf")
    if data.y.min().item() < 0:
        errors.append("Labels contain negative values")

    labels = torch.unique(data.y).cpu()
    if not torch.equal(labels, torch.arange(expected.num_classes)):
        errors.append(f"Labels are not contiguous 0..{expected.num_classes - 1}")

    split_report = validate_masks(data, expected.num_splits)
    errors.extend(split_report.pop("errors"))

    raw_files = raw_file_manifest(dataset)
    if not raw_files:
        errors.append("No non-empty raw dataset files were found")

    report = {
        "dataset": name,
        "status": "valid" if not errors else "invalid",
        "source": expected.source,
        "source_url": expected.source_url,
        "expected": asdict(expected),
        "actual": actual,
        "splits": split_report,
        "raw_files": raw_files,
        "errors": errors,
    }
    if errors:
        raise RuntimeError(
            f"{name} failed dataset validation:\n- " + "\n- ".join(errors)
        )
    return report


def mask_split_count(mask: torch.Tensor) -> int:
    return 1 if mask.dim() == 1 else int(mask.size(1))


def validate_masks(data: object, expected_splits: int) -> dict[str, object]:
    errors = []
    split_sizes = []
    for split in range(expected_splits):
        train = select_mask(data.train_mask, split)
        val = select_mask(data.val_mask, split)
        test = select_mask(data.test_mask, split)
        if train.dtype != torch.bool or val.dtype != torch.bool or test.dtype != torch.bool:
            errors.append(f"split {split}: masks must be boolean")
        if train.numel() != data.num_nodes or val.numel() != data.num_nodes or test.numel() != data.num_nodes:
            errors.append(f"split {split}: mask length does not match num_nodes")
        if (train & val).any() or (train & test).any() or (val & test).any():
            errors.append(f"split {split}: train/val/test masks overlap")
        if not train.any() or not val.any() or not test.any():
            errors.append(f"split {split}: one or more masks are empty")
        split_sizes.append(
            {
                "split": split,
                "train": int(train.sum()),
                "val": int(val.sum()),
                "test": int(test.sum()),
            }
        )
    return {"count": expected_splits, "sizes": split_sizes, "errors": errors}


def select_mask(mask: torch.Tensor, split: int) -> torch.Tensor:
    return mask if mask.dim() == 1 else mask[:, split]


def raw_file_manifest(dataset: object) -> list[dict[str, object]]:
    entries = []
    for raw_path in getattr(dataset, "raw_paths", []):
        path = Path(raw_path)
        if not path.is_file() or path.stat().st_size == 0:
            continue
        entries.append(
            {
                "path": str(path.resolve()),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return entries


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_graph_data(
    pyg_data: object,
    split: int,
    rw_steps: int,
    rw_samples: int,
    rw_seed: int,
    normalize_features: bool = True,
    edge_protocol: str = "source_to_target",
    cache_path: Path | None = None,
    cache_key: str | None = None,
) -> GraphData:
    x = pyg_data.x.float()
    if normalize_features:
        x = row_normalize_features(x)
    y = pyg_data.y.long()
    edge_index = apply_edge_protocol(
        pyg_data.edge_index.long(),
        num_nodes=int(pyg_data.num_nodes),
        protocol=edge_protocol,
    )
    cached = load_reliability_cache(cache_path, cache_key)
    if cached is None:
        # Reliability describes the neighbors whose messages are received by
        # each node. PyG edges are source -> target, so group by target.
        reliability_edge_index = edge_index.flip(0)
        reliability_gate, reliability_qk, local_similarity = compute_real_reliability(
            x,
            reliability_edge_index,
            rw_steps=rw_steps,
            rw_samples=rw_samples,
            rw_seed=rw_seed,
        )
        save_reliability_cache(
            cache_path,
            cache_key,
            reliability_gate,
            reliability_qk,
            local_similarity,
        )
    else:
        reliability_gate, reliability_qk, local_similarity = cached
    return GraphData(
        x=x,
        y=y,
        edge_index=edge_index,
        reliability=reliability_gate,
        reliability_gate=reliability_gate,
        reliability_qk=reliability_qk,
        reliability_gate_raw=reliability_gate.clone(),
        reliability_qk_raw=reliability_qk.clone(),
        train_mask=select_mask(pyg_data.train_mask, split).clone(),
        val_mask=select_mask(pyg_data.val_mask, split).clone(),
        test_mask=select_mask(pyg_data.test_mask, split).clone(),
        local_similarity=local_similarity,
    )


def apply_edge_protocol(
    edge_index: torch.Tensor,
    num_nodes: int,
    protocol: str,
) -> torch.Tensor:
    if protocol not in EDGE_PROTOCOLS:
        raise ValueError(f"Unknown edge protocol: {protocol}")
    try:
        from torch_geometric.utils import coalesce, to_undirected
    except ImportError as exc:
        raise RuntimeError("Edge protocols require torch-geometric") from exc

    edge_index = edge_index.long()
    if protocol == "undirected":
        return to_undirected(edge_index, num_nodes=num_nodes, reduce="add")
    if protocol == "target_to_source":
        edge_index = edge_index.flip(0)
    return coalesce(edge_index, num_nodes=num_nodes)


def validation_fingerprint(report: dict[str, object]) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps(report["actual"], sort_keys=True).encode("utf-8"))
    for item in report["raw_files"]:
        digest.update(str(item["sha256"]).encode("ascii"))
    return digest.hexdigest()


def load_reliability_cache(
    cache_path: Path | None,
    cache_key: str | None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor] | None:
    if cache_path is None or cache_key is None or not cache_path.exists():
        return None
    payload = torch.load(cache_path, map_location="cpu", weights_only=False)
    if payload.get("cache_key") != cache_key:
        return None
    return (
        payload["reliability_gate"],
        payload["reliability_qk"],
        payload["local_similarity"],
    )


def save_reliability_cache(
    cache_path: Path | None,
    cache_key: str | None,
    reliability_gate: torch.Tensor,
    reliability_qk: torch.Tensor,
    local_similarity: torch.Tensor,
) -> None:
    if cache_path is None or cache_key is None:
        return
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "cache_key": cache_key,
            "reliability_gate": reliability_gate,
            "reliability_qk": reliability_qk,
            "local_similarity": local_similarity,
        },
        cache_path,
    )


def row_normalize_features(x: torch.Tensor) -> torch.Tensor:
    x = x - x.min(dim=-1, keepdim=True).values
    return x / x.sum(dim=-1, keepdim=True).clamp_min(1e-12)


def compute_real_reliability(
    x: torch.Tensor,
    edge_index: torch.Tensor,
    rw_steps: int = 4,
    rw_samples: int = 128,
    rw_seed: int = 0,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    src, dst = edge_index.cpu()
    num_nodes = x.size(0)
    deg = torch.bincount(src, minlength=num_nodes).float()
    deg_feat = standardize(torch.log1p(deg)).unsqueeze(1)

    x_cpu = x.cpu()
    x_norm = torch.nn.functional.normalize(x_cpu, p=2, dim=-1)
    edge_cos = (x_norm[src] * x_norm[dst]).sum(dim=-1)
    sim_sum = torch.zeros(num_nodes).scatter_add_(0, src, edge_cos)
    local_sim = sim_sum / deg.clamp_min(1.0)
    local_sim_feat = standardize(local_sim).unsqueeze(1)

    neigh_sum = torch.zeros_like(x_cpu).scatter_add_(
        0,
        src.unsqueeze(-1).expand(-1, x_cpu.size(1)),
        x_cpu[dst],
    )
    neigh_mean = neigh_sum / deg.clamp_min(1.0).unsqueeze(1)
    centered_sq = (x_cpu[dst] - neigh_mean[src]).pow(2)
    var_sum = torch.zeros_like(x_cpu).scatter_add_(
        0,
        src.unsqueeze(-1).expand(-1, x_cpu.size(1)),
        centered_sq,
    )
    neighbor_variance = (
        var_sum / deg.clamp_min(1.0).unsqueeze(1)
    ).mean(dim=-1)
    neighbor_variance_feat = standardize(neighbor_variance).unsqueeze(1)

    rwse = monte_carlo_rwse(
        edge_index,
        num_nodes=num_nodes,
        rw_steps=rw_steps,
        samples=rw_samples,
        seed=rw_seed,
    )
    reliability_gate = torch.cat(
        [deg_feat, local_sim_feat, neighbor_variance_feat, rwse],
        dim=1,
    )
    reliability_qk = torch.cat([deg_feat, rwse], dim=1)
    return (
        torch.nan_to_num(reliability_gate),
        torch.nan_to_num(reliability_qk),
        local_sim,
    )


def monte_carlo_rwse(
    edge_index: torch.Tensor,
    num_nodes: int,
    rw_steps: int,
    samples: int,
    seed: int,
) -> torch.Tensor:
    if samples < 1:
        raise ValueError("rw_samples must be at least 1")

    src = edge_index[0].cpu().numpy().astype(np.int64, copy=False)
    dst = edge_index[1].cpu().numpy().astype(np.int64, copy=False)
    order = np.argsort(src, kind="stable")
    src = src[order]
    dst = dst[order]
    counts = np.bincount(src, minlength=num_nodes)
    indptr = np.concatenate(([0], np.cumsum(counts)))

    rng = np.random.default_rng(seed)
    starts = np.repeat(np.arange(num_nodes, dtype=np.int64), samples)
    current = starts.copy()
    outputs = []
    for _ in range(rw_steps):
        degree = counts[current]
        next_nodes = current.copy()
        active = degree > 0
        offsets = (rng.random(active.sum()) * degree[active]).astype(np.int64)
        next_nodes[active] = dst[indptr[current[active]] + offsets]
        current = next_nodes
        returns = (current == starts).reshape(num_nodes, samples).mean(axis=1)
        outputs.append(torch.from_numpy(returns).float().unsqueeze(1))
    return standardize(torch.cat(outputs, dim=1))


def write_validation_report(reports: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8")
