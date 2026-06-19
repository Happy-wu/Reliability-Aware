from __future__ import annotations

import math

import torch
from torch import nn
import torch.nn.functional as F

from .models import LinearAttention, ReliabilityEncoder


CONTROL_MODES = (
    "fixed",
    "feature_only",
    "reliability_only",
    "combined",
    "shuffled_reliability",
    "constant_reliability",
)


class ConservativeAlphaController(nn.Module):
    """Node-wise adjustment constrained to remain near a fixed alpha."""

    def __init__(
        self,
        feature_dim: int,
        reliability_dim: int,
        hidden_dim: int,
        dropout: float,
        mode: str,
        base_alpha: float,
        max_adjustment: float,
        lambda_init: float,
    ):
        super().__init__()
        if mode not in CONTROL_MODES or mode == "fixed":
            raise ValueError(f"Unsupported controller mode: {mode}")
        if not 0.0 <= base_alpha <= 1.0:
            raise ValueError("base_alpha must be between 0 and 1")
        if not 0.0 < max_adjustment <= 1.0:
            raise ValueError("max_adjustment must be in (0, 1]")
        if not 0.0 < lambda_init < max_adjustment:
            raise ValueError("lambda_init must be in (0, max_adjustment)")

        self.mode = mode
        self.base_alpha = float(base_alpha)
        self.max_adjustment = float(max_adjustment)
        self.feature_encoder = nn.Sequential(
            nn.Linear(feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.LayerNorm(hidden_dim),
        )
        self.reliability_encoder = ReliabilityEncoder(
            reliability_dim,
            hidden_dim,
            dropout=dropout,
        )
        self.trunk = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.proposal_head = nn.Linear(hidden_dim, 1)
        self.lambda_head = nn.Linear(hidden_dim, 1)
        nn.init.zeros_(self.proposal_head.weight)
        nn.init.zeros_(self.proposal_head.bias)
        nn.init.zeros_(self.lambda_head.weight)
        lambda_ratio = lambda_init / max_adjustment
        nn.init.constant_(
            self.lambda_head.bias,
            math.log(lambda_ratio / (1.0 - lambda_ratio)),
        )

    def forward(
        self,
        features: torch.Tensor,
        reliability: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        feature_h = self.feature_encoder(features)
        reliability_h = self.reliability_encoder(reliability)
        if self.mode in {
            "reliability_only",
            "shuffled_reliability",
            "constant_reliability",
        }:
            feature_h = torch.zeros_like(feature_h)
        if self.mode == "feature_only":
            reliability_h = torch.zeros_like(reliability_h)

        hidden = self.trunk(torch.cat([feature_h, reliability_h], dim=-1))
        proposal = torch.sigmoid(self.proposal_head(hidden))
        adjustment = self.max_adjustment * torch.sigmoid(
            self.lambda_head(hidden)
        )
        alpha = (1.0 - adjustment) * self.base_alpha + adjustment * proposal
        return alpha, proposal, adjustment


class ResidualAlphaFusion(nn.Module):
    def __init__(
        self,
        feature_dim: int,
        reliability_dim: int,
        hidden_dim: int,
        dropout: float,
        mode: str,
        base_alpha: float,
        max_adjustment: float,
        lambda_init: float,
    ):
        super().__init__()
        self.mode = mode
        self.base_alpha = float(base_alpha)
        self.controller = (
            None
            if mode == "fixed"
            else ConservativeAlphaController(
                feature_dim=feature_dim,
                reliability_dim=reliability_dim,
                hidden_dim=hidden_dim,
                dropout=dropout,
                mode=mode,
                base_alpha=base_alpha,
                max_adjustment=max_adjustment,
                lambda_init=lambda_init,
            )
        )
        self.latest_alpha: torch.Tensor | None = None
        self.latest_proposal: torch.Tensor | None = None
        self.latest_adjustment: torch.Tensor | None = None

    def forward(
        self,
        features: torch.Tensor,
        reliability: torch.Tensor,
        local_logits: torch.Tensor,
        global_logits: torch.Tensor,
    ) -> torch.Tensor:
        if self.controller is None:
            alpha = features.new_full((features.size(0), 1), self.base_alpha)
            proposal = alpha
            adjustment = features.new_zeros((features.size(0), 1))
        else:
            alpha, proposal, adjustment = self.controller(features, reliability)
        self.latest_alpha = alpha.detach()
        self.latest_proposal = proposal.detach()
        self.latest_adjustment = adjustment.detach()
        return alpha * local_logits + (1.0 - alpha) * global_logits

    def diagnostic_stats(self) -> dict[str, float]:
        return alpha_diagnostics(
            self.latest_alpha,
            self.latest_proposal,
            self.latest_adjustment,
        )


class HiddenControlLayer(nn.Module):
    def __init__(
        self,
        hidden_dim: int,
        reliability_dim: int,
        num_heads: int,
        dropout: float,
        mode: str,
        base_alpha: float,
        max_adjustment: float,
        lambda_init: float,
    ):
        super().__init__()
        try:
            from torch_geometric.nn import GCNConv
        except ImportError as exc:
            raise RuntimeError("HiddenControlLayer requires torch-geometric") from exc

        self.mode = mode
        self.base_alpha = float(base_alpha)
        self.local = GCNConv(
            hidden_dim,
            hidden_dim,
            cached=True,
            normalize=True,
        )
        self.global_attn = LinearAttention(hidden_dim, num_heads, dropout)
        self.controller = (
            None
            if mode == "fixed"
            else ConservativeAlphaController(
                feature_dim=hidden_dim,
                reliability_dim=reliability_dim,
                hidden_dim=hidden_dim,
                dropout=dropout,
                mode=mode,
                base_alpha=base_alpha,
                max_adjustment=max_adjustment,
                lambda_init=lambda_init,
            )
        )
        self.dropout = nn.Dropout(dropout)
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, hidden_dim),
        )
        self.latest_alpha: torch.Tensor | None = None
        self.latest_proposal: torch.Tensor | None = None
        self.latest_adjustment: torch.Tensor | None = None

    def forward(
        self,
        hidden: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor,
    ) -> torch.Tensor:
        local_h = F.relu(self.local(hidden, edge_index))
        global_h = self.global_attn(hidden)
        if self.controller is None:
            alpha = hidden.new_full((hidden.size(0), 1), self.base_alpha)
            proposal = alpha
            adjustment = hidden.new_zeros((hidden.size(0), 1))
        else:
            alpha, proposal, adjustment = self.controller(hidden, reliability)
        mixed = alpha * local_h + (1.0 - alpha) * global_h
        self.latest_alpha = alpha.detach()
        self.latest_proposal = proposal.detach()
        self.latest_adjustment = adjustment.detach()
        hidden = self.norm1(hidden + self.dropout(mixed))
        return self.norm2(hidden + self.dropout(self.ffn(hidden)))


class HiddenMixingNetwork(nn.Module):
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
        base_alpha: float,
        max_adjustment: float,
        lambda_init: float,
    ):
        super().__init__()
        if mode not in CONTROL_MODES:
            raise ValueError(f"Unknown control mode: {mode}")
        self.mode = mode
        self.base_alpha = float(base_alpha)
        self.input_proj = nn.Linear(in_dim, hidden_dim)
        self.layers = nn.ModuleList(
            [
                HiddenControlLayer(
                    hidden_dim=hidden_dim,
                    reliability_dim=reliability_dim,
                    num_heads=num_heads,
                    dropout=dropout,
                    mode=mode,
                    base_alpha=base_alpha,
                    max_adjustment=max_adjustment,
                    lambda_init=lambda_init,
                )
                for _ in range(num_layers)
            ]
        )
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(hidden_dim, out_dim)

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor,
    ) -> torch.Tensor:
        hidden = self.dropout(F.relu(self.input_proj(x)))
        for layer in self.layers:
            hidden = layer(hidden, edge_index, reliability)
        return self.out(hidden)

    def diagnostic_stats(self) -> dict[str, float]:
        alphas = [
            layer.latest_alpha
            for layer in self.layers
            if layer.latest_alpha is not None
        ]
        proposals = [
            layer.latest_proposal
            for layer in self.layers
            if layer.latest_proposal is not None
        ]
        adjustments = [
            layer.latest_adjustment
            for layer in self.layers
            if layer.latest_adjustment is not None
        ]
        return alpha_diagnostics(
            torch.cat(alphas, dim=0) if alphas else None,
            torch.cat(proposals, dim=0) if proposals else None,
            torch.cat(adjustments, dim=0) if adjustments else None,
        )


def alpha_diagnostics(
    alpha: torch.Tensor | None,
    proposal: torch.Tensor | None,
    adjustment: torch.Tensor | None,
) -> dict[str, float]:
    output = {
        "alpha_mean": math.nan,
        "alpha_std": math.nan,
        "alpha_min": math.nan,
        "alpha_max": math.nan,
        "proposal_mean": math.nan,
        "adjustment_mean": math.nan,
        "adjustment_max": math.nan,
    }
    if alpha is not None:
        output.update(
            {
                "alpha_mean": float(alpha.mean().cpu()),
                "alpha_std": float(alpha.std(unbiased=False).cpu()),
                "alpha_min": float(alpha.min().cpu()),
                "alpha_max": float(alpha.max().cpu()),
            }
        )
    if proposal is not None:
        output["proposal_mean"] = float(proposal.mean().cpu())
    if adjustment is not None:
        output["adjustment_mean"] = float(adjustment.mean().cpu())
        output["adjustment_max"] = float(adjustment.max().cpu())
    return output
