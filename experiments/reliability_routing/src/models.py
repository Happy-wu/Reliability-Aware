from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F

from .data import normalized_adjacency


class MLP(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float = 0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor | None = None,
        reliability: torch.Tensor | None = None,
        reliability_qk: torch.Tensor | None = None,
    ) -> torch.Tensor:
        return self.net(x)


class GCNLayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, dropout: float = 0.3):
        super().__init__()
        self.lin = nn.Linear(in_dim, out_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        x = self.dropout(x)
        return torch.sparse.mm(adj, self.lin(x))


class GCN(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float = 0.3):
        super().__init__()
        self.conv1 = GCNLayer(in_dim, hidden_dim, dropout)
        self.conv2 = GCNLayer(hidden_dim, out_dim, dropout)

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor | None = None,
        reliability_qk: torch.Tensor | None = None,
    ) -> torch.Tensor:
        adj = normalized_adjacency(edge_index, x.size(0))
        h = F.relu(self.conv1(x, adj))
        return self.conv2(h, adj)


class PyGGCN(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float = 0.5):
        super().__init__()
        try:
            from torch_geometric.nn import GCNConv
        except ImportError as exc:
            raise RuntimeError(
                "gcn_pyg requires torch-geometric. Install the real-data dependencies first."
            ) from exc
        self.conv1 = GCNConv(in_dim, hidden_dim, cached=True, normalize=True)
        self.conv2 = GCNConv(hidden_dim, out_dim, cached=True, normalize=True)
        self.dropout = dropout

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor | None = None,
        reliability_qk: torch.Tensor | None = None,
    ) -> torch.Tensor:
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)


class LinearAttention(nn.Module):
    def __init__(self, hidden_dim: int, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        if hidden_dim % num_heads != 0:
            raise ValueError("hidden_dim must be divisible by num_heads")
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        self.q_proj = nn.Linear(hidden_dim, hidden_dim)
        self.k_proj = nn.Linear(hidden_dim, hidden_dim)
        self.v_proj = nn.Linear(hidden_dim, hidden_dim)
        self.out_proj = nn.Linear(hidden_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)

    def project_qkv(
        self,
        x: torch.Tensor,
        gamma_q: torch.Tensor | None = None,
        gamma_k: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)
        if gamma_q is not None:
            q = gamma_q * q
        if gamma_k is not None:
            k = gamma_k * k
        return q, k, v

    def forward(
        self,
        x: torch.Tensor,
        gamma_q: torch.Tensor | None = None,
        gamma_k: torch.Tensor | None = None,
    ) -> torch.Tensor:
        q, k, v = self.project_qkv(x, gamma_q, gamma_k)
        n = x.size(0)
        q = q.view(n, self.num_heads, self.head_dim)
        k = k.view(n, self.num_heads, self.head_dim)
        v = v.view(n, self.num_heads, self.head_dim)

        q = F.elu(q) + 1.0
        k = F.elu(k) + 1.0
        q = self.dropout(q)
        k = self.dropout(k)
        v = self.dropout(v)

        kv = torch.einsum("nhd,nhe->hde", k, v)
        k_sum = k.sum(dim=0)
        denom = torch.einsum("nhd,hd->nh", q, k_sum).clamp_min(1e-6)
        out = torch.einsum("nhd,hde->nhe", q, kv) / denom.unsqueeze(-1)
        out = out.reshape(n, self.hidden_dim)
        return self.out_proj(out)


class ReliabilityEncoder(nn.Module):
    def __init__(self, reliability_dim: int, hidden_dim: int, dropout: float = 0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(reliability_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
        )

    def forward(self, reliability: torch.Tensor) -> torch.Tensor:
        return self.net(reliability)


class LinearGTLayer(nn.Module):
    def __init__(
        self,
        hidden_dim: int,
        reliability_dim: int,
        qk_reliability_dim: int | None = None,
        num_heads: int = 4,
        dropout: float = 0.3,
        use_reliability: bool = False,
        use_gate: bool = False,
        qk_mode: str = "both",
        fixed_local_weight: float = 0.5,
        qk_strength_init: float = -5.0,
        fixed_qk_strength: float | None = None,
        reliability_encoder_mode: str = "separate",
    ):
        super().__init__()
        if reliability_encoder_mode not in {"separate", "branch_specific"}:
            raise ValueError(
                "reliability_encoder_mode must be 'separate' or 'branch_specific'"
            )
        self.use_reliability = use_reliability
        self.use_gate = use_gate
        self.qk_mode = qk_mode
        self.fixed_local_weight = fixed_local_weight
        self.fixed_qk_strength = fixed_qk_strength
        self.reliability_encoder_mode = reliability_encoder_mode
        self.latest_qk_stats: dict[str, float] | None = None
        self.latest_branch_stats: dict[str, float] | None = None

        self.local = GCNLayer(hidden_dim, hidden_dim, dropout)
        self.global_attn = LinearAttention(hidden_dim, num_heads=num_heads, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, hidden_dim),
        )

        uses_encoded_reliability = reliability_encoder_mode == "branch_specific"
        self.qk_reliability_encoder = (
            ReliabilityEncoder(qk_reliability_dim or reliability_dim, hidden_dim, dropout)
            if uses_encoded_reliability and use_reliability
            else None
        )
        self.gate_reliability_encoder = (
            ReliabilityEncoder(reliability_dim, hidden_dim, dropout)
            if uses_encoded_reliability and use_gate
            else None
        )

        if use_reliability:
            if self.qk_reliability_encoder is not None:
                self.rel_proj = nn.Linear(hidden_dim, hidden_dim * 2)
            else:
                self.rel_proj = nn.Sequential(
                    nn.Linear(qk_reliability_dim or reliability_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Linear(hidden_dim, hidden_dim * 2),
                )
            nn.init.zeros_(self.rel_proj[-1].weight if isinstance(self.rel_proj, nn.Sequential) else self.rel_proj.weight)
            nn.init.zeros_(self.rel_proj[-1].bias if isinstance(self.rel_proj, nn.Sequential) else self.rel_proj.bias)
            if fixed_qk_strength is None:
                self.qk_mod_strength = nn.Parameter(torch.tensor(float(qk_strength_init)))
            else:
                if not 0.0 <= fixed_qk_strength <= 1.0:
                    raise ValueError("fixed_qk_strength must be between 0 and 1")
                self.qk_mod_strength = None
        else:
            self.rel_proj = None
            self.qk_mod_strength = None

        if use_gate:
            self.rel_gate_proj = (
                None
                if self.gate_reliability_encoder is not None
                else nn.Sequential(
                    nn.Linear(reliability_dim, hidden_dim),
                    nn.ReLU(),
                )
            )
            self.gate = nn.Sequential(
                nn.Linear(hidden_dim * 4, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, 1),
                nn.Sigmoid(),
            )
        else:
            self.gate = None

    def forward(
        self,
        x: torch.Tensor,
        adj: torch.Tensor,
        reliability_gate: torch.Tensor,
        reliability_qk: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        local_h = self.local(x, adj)

        gamma_q = gamma_k = None
        self.latest_qk_stats = None
        if self.use_reliability:
            qk_input = reliability_qk if reliability_qk is not None else reliability_gate
            if self.qk_reliability_encoder is not None:
                rel_params = self.rel_proj(self.qk_reliability_encoder(qk_input))
            else:
                rel_params = self.rel_proj(qk_input)
            delta_q, delta_k = rel_params.chunk(2, dim=-1)
            if self.fixed_qk_strength is None:
                strength = torch.sigmoid(self.qk_mod_strength)
            else:
                strength = x.new_tensor(float(self.fixed_qk_strength))
            if self.qk_mode in {"both", "q_only"}:
                gamma_q = 1.0 + strength * 0.5 * torch.tanh(delta_q)
            if self.qk_mode in {"both", "k_only"}:
                gamma_k = 1.0 + strength * 0.5 * torch.tanh(delta_k)
            self.latest_qk_stats = collect_gamma_stats(gamma_q, gamma_k)

        global_h = self.global_attn(x, gamma_q, gamma_k)

        gate_value = None
        if self.use_gate:
            rel_h = (
                self.gate_reliability_encoder(reliability_gate)
                if self.gate_reliability_encoder is not None
                else self.rel_gate_proj(reliability_gate)
            )
            gate_value = self.gate(torch.cat([x, rel_h, local_h, global_h], dim=-1))
            mixed = gate_value * local_h + (1.0 - gate_value) * global_h
        else:
            mixed = self.fixed_local_weight * local_h + (1.0 - self.fixed_local_weight) * global_h

        self.latest_branch_stats = collect_branch_stats(
            local_h,
            global_h,
            mixed,
            gate_value,
        )
        x = self.norm1(x + self.dropout(mixed))
        x = self.norm2(x + self.dropout(self.ffn(x)))
        return x, gate_value

class LinearGT(nn.Module):
    def __init__(
        self,
        in_dim: int,
        reliability_dim: int,
        qk_reliability_dim: int | None,
        hidden_dim: int,
        out_dim: int,
        num_layers: int = 2,
        num_heads: int = 4,
        dropout: float = 0.3,
        use_reliability: bool = False,
        use_gate: bool = False,
        qk_mode: str = "both",
        qk_strength_init: float = -5.0,
        fixed_qk_strength: float | None = None,
        reliability_encoder_mode: str = "separate",
        fixed_local_weight: float = 0.5,
    ):
        super().__init__()
        self.input_proj = nn.Linear(in_dim, hidden_dim)
        self.layers = nn.ModuleList(
            [
                LinearGTLayer(
                    hidden_dim=hidden_dim,
                    reliability_dim=reliability_dim,
                    qk_reliability_dim=qk_reliability_dim,
                    num_heads=num_heads,
                    dropout=dropout,
                    use_reliability=use_reliability,
                    use_gate=use_gate,
                    qk_mode=qk_mode,
                    qk_strength_init=qk_strength_init,
                    fixed_qk_strength=fixed_qk_strength,
                    reliability_encoder_mode=reliability_encoder_mode,
                    fixed_local_weight=fixed_local_weight,
                )
                for _ in range(num_layers)
            ]
        )
        self.out = nn.Linear(hidden_dim, out_dim)
        self.dropout = nn.Dropout(dropout)
        self.latest_gate: torch.Tensor | None = None
        self.latest_gates_by_layer: list[torch.Tensor] = []
        self.latest_qk_stats_by_layer: list[dict[str, float]] = []
        self.latest_branch_stats_by_layer: list[dict[str, float]] = []

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor,
        reliability_qk: torch.Tensor | None = None,
    ) -> torch.Tensor:
        adj = normalized_adjacency(edge_index, x.size(0))
        h = self.dropout(F.relu(self.input_proj(x)))
        gates = []
        self.latest_gates_by_layer = []
        self.latest_qk_stats_by_layer = []
        self.latest_branch_stats_by_layer = []
        for layer in self.layers:
            h, gate = layer(h, adj, reliability, reliability_qk)
            if layer.latest_qk_stats is not None:
                self.latest_qk_stats_by_layer.append(layer.latest_qk_stats)
            if gate is not None:
                detached_gate = gate.detach()
                gates.append(detached_gate)
                self.latest_gates_by_layer.append(detached_gate)
            if layer.latest_branch_stats is not None:
                self.latest_branch_stats_by_layer.append(layer.latest_branch_stats)
        self.latest_gate = torch.stack(gates).mean(dim=0) if gates else None
        return self.out(h)

    def qk_strengths(self) -> list[float]:
        values = []
        for layer in self.layers:
            if layer.qk_mod_strength is not None:
                values.append(float(torch.sigmoid(layer.qk_mod_strength.detach()).cpu()))
            elif layer.use_reliability and layer.fixed_qk_strength is not None:
                values.append(float(layer.fixed_qk_strength))
        return values

    def qk_gamma_stats(self) -> dict[str, float]:
        if not self.latest_qk_stats_by_layer:
            return {}
        keys = self.latest_qk_stats_by_layer[0].keys()
        return {
            key: float(torch.tensor([stats[key] for stats in self.latest_qk_stats_by_layer]).mean())
            for key in keys
        }

    def branch_stats(self) -> dict[str, float]:
        if not self.latest_branch_stats_by_layer:
            return {}
        output = {}
        keys = self.latest_branch_stats_by_layer[0].keys()
        for key in keys:
            values = [
                stats[key]
                for stats in self.latest_branch_stats_by_layer
                if not torch.isnan(torch.tensor(stats[key]))
            ]
            output[key] = float(torch.tensor(values).mean()) if values else float("nan")
        for index, stats in enumerate(self.latest_branch_stats_by_layer, start=1):
            for key, value in stats.items():
                output[f"{key}_layer{index}"] = value
        return output


def collect_gamma_stats(
    gamma_q: torch.Tensor | None,
    gamma_k: torch.Tensor | None,
) -> dict[str, float]:
    return {
        "qk_gamma_q_abs_dev_mean": gamma_abs_dev_mean(gamma_q),
        "qk_gamma_k_abs_dev_mean": gamma_abs_dev_mean(gamma_k),
        "qk_gamma_q_std": gamma_std(gamma_q),
        "qk_gamma_k_std": gamma_std(gamma_k),
        "qk_gamma_q_abs_dev_max": gamma_abs_dev_max(gamma_q),
        "qk_gamma_k_abs_dev_max": gamma_abs_dev_max(gamma_k),
    }


def collect_branch_stats(
    local_h: torch.Tensor,
    global_h: torch.Tensor,
    mixed_h: torch.Tensor,
    gate: torch.Tensor | None,
) -> dict[str, float]:
    local = local_h.detach()
    global_ = global_h.detach()
    mixed = mixed_h.detach()
    stats = {
        "local_branch_norm_mean": float(local.norm(dim=-1).mean().cpu()),
        "global_branch_norm_mean": float(global_.norm(dim=-1).mean().cpu()),
        "mixed_branch_norm_mean": float(mixed.norm(dim=-1).mean().cpu()),
        "local_global_cosine_mean": float(
            F.cosine_similarity(local, global_, dim=-1).mean().cpu()
        ),
        "gate_mean": float("nan"),
        "gate_std": float("nan"),
        "gate_min": float("nan"),
        "gate_max": float("nan"),
    }
    if gate is not None:
        detached_gate = gate.detach()
        stats.update(
            {
                "gate_mean": float(detached_gate.mean().cpu()),
                "gate_std": float(detached_gate.std(unbiased=False).cpu()),
                "gate_min": float(detached_gate.min().cpu()),
                "gate_max": float(detached_gate.max().cpu()),
            }
        )
    return stats


def gamma_abs_dev_mean(gamma: torch.Tensor | None) -> float:
    if gamma is None:
        return float("nan")
    return float((gamma.detach() - 1.0).abs().mean().cpu())


def gamma_std(gamma: torch.Tensor | None) -> float:
    if gamma is None:
        return float("nan")
    return float(gamma.detach().std(unbiased=False).cpu())


def gamma_abs_dev_max(gamma: torch.Tensor | None) -> float:
    if gamma is None:
        return float("nan")
    return float((gamma.detach() - 1.0).abs().max().cpu())


def build_model(
    name: str,
    in_dim: int,
    reliability_dim: int,
    qk_reliability_dim: int | None,
    hidden_dim: int,
    out_dim: int,
    num_layers: int,
    num_heads: int,
    dropout: float,
    qk_strength_init: float = -5.0,
    fixed_qk_strength: float | None = None,
) -> nn.Module:
    if name == "mlp":
        return MLP(in_dim, hidden_dim, out_dim, dropout)
    if name == "gcn":
        return GCN(in_dim, hidden_dim, out_dim, dropout)
    if name == "gcn_pyg":
        return PyGGCN(in_dim, hidden_dim, out_dim, dropout)
    if name == "local_only_gt":
        return LinearGT(
            in_dim,
            reliability_dim,
            qk_reliability_dim,
            hidden_dim,
            out_dim,
            num_layers,
            num_heads,
            dropout,
            use_reliability=False,
            use_gate=False,
            fixed_local_weight=1.0,
        )
    if name == "linear_gt":
        return LinearGT(
            in_dim,
            reliability_dim,
            qk_reliability_dim,
            hidden_dim,
            out_dim,
            num_layers,
            num_heads,
            dropout,
            use_reliability=False,
            use_gate=False,
            qk_strength_init=qk_strength_init,
            fixed_qk_strength=fixed_qk_strength,
        )
    if name in {"qk_gt", "q_only_gt", "k_only_gt", "qk_gt_encoded"}:
        qk_mode = {
            "qk_gt": "both",
            "q_only_gt": "q_only",
            "k_only_gt": "k_only",
            "qk_gt_encoded": "both",
        }[name]
        return LinearGT(
            in_dim,
            reliability_dim,
            qk_reliability_dim,
            hidden_dim,
            out_dim,
            num_layers,
            num_heads,
            dropout,
            use_reliability=True,
            use_gate=False,
            qk_mode=qk_mode,
            qk_strength_init=qk_strength_init,
            fixed_qk_strength=fixed_qk_strength,
            reliability_encoder_mode=(
                "branch_specific" if name == "qk_gt_encoded" else "separate"
            ),
        )
    if name in {"gate_gt", "gate_gt_encoded"}:
        return LinearGT(
            in_dim,
            reliability_dim,
            qk_reliability_dim,
            hidden_dim,
            out_dim,
            num_layers,
            num_heads,
            dropout,
            use_reliability=False,
            use_gate=True,
            qk_strength_init=qk_strength_init,
            fixed_qk_strength=fixed_qk_strength,
            reliability_encoder_mode=(
                "branch_specific" if name == "gate_gt_encoded" else "separate"
            ),
        )
    if name in {"reliability_gt", "reliability_gt_encoded"}:
        return LinearGT(
            in_dim,
            reliability_dim,
            qk_reliability_dim,
            hidden_dim,
            out_dim,
            num_layers,
            num_heads,
            dropout,
            use_reliability=True,
            use_gate=True,
            qk_strength_init=qk_strength_init,
            fixed_qk_strength=fixed_qk_strength,
            reliability_encoder_mode=(
                "branch_specific" if name == "reliability_gt_encoded" else "separate"
            ),
        )
    raise ValueError(f"Unknown model: {name}")
