from __future__ import annotations

import math

import torch
from torch import nn
import torch.nn.functional as F

from .models import LinearAttention, ReliabilityEncoder


EXPERT_MODELS = (
    "gcn_pyg",
    "global_only",
    "fixed_alpha",
    "ordinary_gate",
    "reliability_gate",
)


class LocalExpert(nn.Module):
    """Two-layer PyG GCN used by both the baseline and every fusion model."""

    def __init__(
        self,
        in_dim: int,
        hidden_dim: int,
        out_dim: int,
        dropout: float,
    ):
        super().__init__()
        try:
            from torch_geometric.nn import GCNConv
        except ImportError as exc:
            raise RuntimeError("LocalExpert requires torch-geometric") from exc
        self.conv1 = GCNConv(in_dim, hidden_dim, cached=True, normalize=True)
        self.conv2 = GCNConv(hidden_dim, out_dim, cached=True, normalize=True)
        self.dropout = dropout

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)


class GlobalExpertLayer(nn.Module):
    def __init__(self, hidden_dim: int, num_heads: int, dropout: float):
        super().__init__()
        self.attn = LinearAttention(hidden_dim, num_heads, dropout)
        self.dropout = nn.Dropout(dropout)
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, hidden_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.norm1(x + self.dropout(self.attn(x)))
        return self.norm2(x + self.dropout(self.ffn(x)))


class GlobalExpert(nn.Module):
    def __init__(
        self,
        in_dim: int,
        hidden_dim: int,
        out_dim: int,
        num_layers: int,
        num_heads: int,
        dropout: float,
    ):
        super().__init__()
        self.input_proj = nn.Linear(in_dim, hidden_dim)
        self.layers = nn.ModuleList(
            [
                GlobalExpertLayer(hidden_dim, num_heads, dropout)
                for _ in range(num_layers)
            ]
        )
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(hidden_dim, out_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.dropout(F.relu(self.input_proj(x)))
        for layer in self.layers:
            x = layer(x)
        return self.out(x)


class NodeGate(nn.Module):
    """Same parameterization for ordinary and reliability-aware gates."""

    def __init__(
        self,
        in_dim: int,
        reliability_dim: int,
        hidden_dim: int,
        out_dim: int,
        dropout: float,
        use_reliability: bool,
    ):
        super().__init__()
        self.use_reliability = use_reliability
        self.feature_encoder = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.LayerNorm(hidden_dim),
        )
        self.reliability_encoder = ReliabilityEncoder(
            reliability_dim,
            hidden_dim,
            dropout,
        )
        self.logit_encoder = nn.Sequential(
            nn.Linear(out_dim * 2, hidden_dim),
            nn.ReLU(),
        )
        self.gate = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid(),
        )

    def forward(
        self,
        x: torch.Tensor,
        reliability: torch.Tensor,
        local_logits: torch.Tensor,
        global_logits: torch.Tensor,
    ) -> torch.Tensor:
        if not self.use_reliability:
            reliability = torch.zeros_like(reliability)
        feature_h = self.feature_encoder(x)
        reliability_h = self.reliability_encoder(reliability)
        logit_h = self.logit_encoder(
            torch.cat([local_logits, global_logits], dim=-1)
        )
        return self.gate(torch.cat([feature_h, reliability_h, logit_h], dim=-1))


class ExpertFusionModel(nn.Module):
    def __init__(
        self,
        in_dim: int,
        reliability_dim: int,
        hidden_dim: int,
        out_dim: int,
        num_layers: int,
        num_heads: int,
        dropout: float,
        mode: str,
        fixed_alpha: float = 0.5,
    ):
        super().__init__()
        if mode not in EXPERT_MODELS:
            raise ValueError(f"Unknown expert model: {mode}")
        if not 0.0 <= fixed_alpha <= 1.0:
            raise ValueError("fixed_alpha must be between 0 and 1")
        self.mode = mode
        self.fixed_alpha = fixed_alpha
        # LocalExpert is deliberately constructed first. With the same seed,
        # gcn_pyg and all fusion variants start from identical local weights.
        self.local_expert = LocalExpert(in_dim, hidden_dim, out_dim, dropout)
        self.global_expert = (
            None
            if mode == "gcn_pyg"
            else GlobalExpert(
                in_dim,
                hidden_dim,
                out_dim,
                num_layers,
                num_heads,
                dropout,
            )
        )
        self.node_gate = (
            NodeGate(
                in_dim,
                reliability_dim,
                hidden_dim,
                out_dim,
                dropout,
                use_reliability=mode == "reliability_gate",
            )
            if mode in {"ordinary_gate", "reliability_gate"}
            else None
        )
        self.latest_alpha: torch.Tensor | None = None
        self.latest_local_logits: torch.Tensor | None = None
        self.latest_global_logits: torch.Tensor | None = None

    def forward_local(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        return self.local_expert(x, edge_index)

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor,
    ) -> torch.Tensor:
        if self.mode == "global_only":
            global_logits = self.global_expert(x)
            self.latest_local_logits = None
            self.latest_global_logits = global_logits.detach()
            self.latest_alpha = None
            return global_logits

        local_logits = self.forward_local(x, edge_index)
        self.latest_local_logits = local_logits.detach()
        self.latest_alpha = None
        self.latest_global_logits = None
        if self.mode == "gcn_pyg":
            return local_logits

        global_logits = self.global_expert(x)
        self.latest_global_logits = global_logits.detach()
        if self.mode == "fixed_alpha":
            alpha = x.new_full((x.size(0), 1), self.fixed_alpha)
        else:
            alpha = self.node_gate(
                x,
                reliability,
                local_logits,
                global_logits,
            )
        self.latest_alpha = alpha.detach()
        return alpha * local_logits + (1.0 - alpha) * global_logits

    def diagnostic_stats(self) -> dict[str, float]:
        stats = {
            "alpha_mean": math.nan,
            "alpha_std": math.nan,
            "alpha_min": math.nan,
            "alpha_max": math.nan,
            "local_logit_norm_mean": math.nan,
            "global_logit_norm_mean": math.nan,
            "local_entropy_mean": math.nan,
            "global_entropy_mean": math.nan,
            "local_global_logit_cosine_mean": math.nan,
        }
        if self.latest_local_logits is not None:
            stats["local_logit_norm_mean"] = float(
                self.latest_local_logits.norm(dim=-1).mean().cpu()
            )
            stats["local_entropy_mean"] = mean_entropy(self.latest_local_logits)
        if self.latest_global_logits is not None:
            stats["global_logit_norm_mean"] = float(
                self.latest_global_logits.norm(dim=-1).mean().cpu()
            )
            stats["global_entropy_mean"] = mean_entropy(self.latest_global_logits)
        if (
            self.latest_local_logits is not None
            and self.latest_global_logits is not None
        ):
            stats["local_global_logit_cosine_mean"] = float(
                F.cosine_similarity(
                    self.latest_local_logits,
                    self.latest_global_logits,
                    dim=-1,
                )
                .mean()
                .cpu()
            )
        if self.latest_alpha is not None:
            stats.update(
                {
                    "alpha_mean": float(self.latest_alpha.mean().cpu()),
                    "alpha_std": float(
                        self.latest_alpha.std(unbiased=False).cpu()
                    ),
                    "alpha_min": float(self.latest_alpha.min().cpu()),
                    "alpha_max": float(self.latest_alpha.max().cpu()),
                }
            )
        return stats


def mean_entropy(logits: torch.Tensor) -> float:
    probabilities = logits.softmax(dim=-1)
    entropy = -(probabilities * probabilities.clamp_min(1e-12).log()).sum(dim=-1)
    return float(entropy.mean().cpu())


def build_expert_model(
    name: str,
    in_dim: int,
    reliability_dim: int,
    hidden_dim: int,
    out_dim: int,
    num_layers: int,
    num_heads: int,
    dropout: float,
    fixed_alpha: float,
) -> ExpertFusionModel:
    return ExpertFusionModel(
        in_dim=in_dim,
        reliability_dim=reliability_dim,
        hidden_dim=hidden_dim,
        out_dim=out_dim,
        num_layers=num_layers,
        num_heads=num_heads,
        dropout=dropout,
        mode=name,
        fixed_alpha=fixed_alpha,
    )
