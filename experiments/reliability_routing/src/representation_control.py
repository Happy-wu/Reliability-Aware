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
    "zero_reliability",
    "combined_shuffled",
    "combined_constant",
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
            "zero_reliability",
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


class IterativeRelationController(nn.Module):
    """Refine channel-wise local/global mixing with shared recurrent weights."""

    def __init__(
        self,
        feature_dim: int,
        reliability_dim: int,
        hidden_dim: int,
        dropout: float,
        mode: str,
        base_alpha: float,
        max_adjustment: float,
        num_steps: int,
    ):
        super().__init__()
        if mode not in CONTROL_MODES or mode == "fixed":
            raise ValueError(f"Unsupported controller mode: {mode}")
        if not 0.0 <= base_alpha <= 1.0:
            raise ValueError("base_alpha must be between 0 and 1")
        if not 0.0 < max_adjustment <= 1.0:
            raise ValueError("max_adjustment must be in (0, 1]")
        if num_steps < 1:
            raise ValueError("num_steps must be positive")

        self.mode = mode
        self.base_alpha = float(base_alpha)
        self.max_adjustment = float(max_adjustment)
        self.num_steps = int(num_steps)
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
        context_dim = hidden_dim * 5
        self.state_init = nn.Sequential(
            nn.Linear(context_dim, hidden_dim),
            nn.Tanh(),
        )
        self.update_gate = nn.Sequential(
            nn.Linear(hidden_dim + context_dim, hidden_dim),
            nn.Sigmoid(),
        )
        self.state_candidate = nn.Sequential(
            nn.Linear(hidden_dim + context_dim, hidden_dim),
            nn.Tanh(),
        )
        self.alpha_update = nn.Linear(hidden_dim, hidden_dim)
        nn.init.zeros_(self.alpha_update.weight)
        nn.init.zeros_(self.alpha_update.bias)

    def forward(
        self,
        features: torch.Tensor,
        reliability: torch.Tensor,
        local_h: torch.Tensor,
        global_h: torch.Tensor,
    ) -> tuple[
        torch.Tensor,
        torch.Tensor,
        torch.Tensor,
        torch.Tensor,
    ]:
        feature_h = self.feature_encoder(features)
        reliability_h = self.reliability_encoder(reliability)
        if self.mode in {
            "reliability_only",
            "shuffled_reliability",
            "constant_reliability",
            "zero_reliability",
        }:
            feature_h = torch.zeros_like(feature_h)
        if self.mode == "feature_only":
            reliability_h = torch.zeros_like(reliability_h)

        difference = local_h - global_h
        abs_difference = difference.abs()
        interaction = local_h * global_h
        context = torch.cat(
            [
                feature_h,
                reliability_h,
                difference,
                abs_difference,
                interaction,
            ],
            dim=-1,
        )
        state = self.state_init(context)
        raw_adjustment = torch.zeros_like(local_h)
        gates = []
        for _ in range(self.num_steps):
            update_input = torch.cat([state, context], dim=-1)
            gate = self.update_gate(update_input)
            candidate = self.state_candidate(update_input)
            state = (1.0 - gate) * state + gate * candidate
            raw_adjustment = raw_adjustment + self.alpha_update(state)
            gates.append(gate)

        signed_adjustment = self.max_adjustment * torch.tanh(
            raw_adjustment / self.num_steps
        )
        alpha = torch.clamp(
            self.base_alpha + signed_adjustment,
            min=0.0,
            max=1.0,
        )
        relation_h = (alpha - self.base_alpha) * difference
        mean_gate = torch.stack(gates, dim=0).mean(dim=0)
        return alpha, relation_h, state, mean_gate


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


class GPSLikeControlLayer(nn.Module):
    """GraphGPS-style local/global residual updates with reliability mixing."""

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
            raise RuntimeError("GPSLikeControlLayer requires torch-geometric") from exc

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
        self.local_norm = nn.LayerNorm(hidden_dim)
        self.global_norm = nn.LayerNorm(hidden_dim)
        self.mix_norm = nn.LayerNorm(hidden_dim)
        self.ffn_norm = nn.LayerNorm(hidden_dim)
        self.ffn = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim * 2, hidden_dim),
        )
        self.latest_alpha: torch.Tensor | None = None
        self.latest_proposal: torch.Tensor | None = None
        self.latest_adjustment: torch.Tensor | None = None
        self.latest_local_delta: torch.Tensor | None = None
        self.latest_global_delta: torch.Tensor | None = None

    def forward(
        self,
        hidden: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor,
    ) -> torch.Tensor:
        local_branch = self.local_norm(
            hidden + self.dropout(F.relu(self.local(hidden, edge_index)))
        )
        global_branch = self.global_norm(
            hidden + self.dropout(self.global_attn(hidden))
        )
        local_delta = local_branch - hidden
        global_delta = global_branch - hidden
        if self.controller is None:
            alpha = hidden.new_full((hidden.size(0), 1), self.base_alpha)
            proposal = alpha
            adjustment = hidden.new_zeros((hidden.size(0), 1))
        else:
            alpha, proposal, adjustment = self.controller(hidden, reliability)
        mixed_delta = alpha * local_delta + (1.0 - alpha) * global_delta
        self.latest_alpha = alpha.detach()
        self.latest_proposal = proposal.detach()
        self.latest_adjustment = adjustment.detach()
        self.latest_local_delta = local_delta.detach()
        self.latest_global_delta = global_delta.detach()
        hidden = self.mix_norm(hidden + self.dropout(mixed_delta))
        return self.ffn_norm(hidden + self.dropout(self.ffn(hidden)))


class GPSLikeNetwork(nn.Module):
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
                GPSLikeControlLayer(
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
        alphas = collect_layer_values(self.layers, "latest_alpha")
        proposals = collect_layer_values(self.layers, "latest_proposal")
        adjustments = collect_layer_values(self.layers, "latest_adjustment")
        local_deltas = collect_layer_values(self.layers, "latest_local_delta")
        global_deltas = collect_layer_values(self.layers, "latest_global_delta")
        disagreement = None
        if local_deltas is not None and global_deltas is not None:
            disagreement = local_deltas - global_deltas
        output = alpha_diagnostics(alphas, proposals, adjustments)
        output.update(
            {
                "local_delta_norm_mean": row_norm_mean(local_deltas),
                "global_delta_norm_mean": row_norm_mean(global_deltas),
                "branch_disagreement_norm_mean": row_norm_mean(disagreement),
            }
        )
        return output


class IterativeRelationLayer(nn.Module):
    def __init__(
        self,
        hidden_dim: int,
        reliability_dim: int,
        num_heads: int,
        dropout: float,
        mode: str,
        base_alpha: float,
        max_adjustment: float,
        relation_steps: int,
    ):
        super().__init__()
        try:
            from torch_geometric.nn import GCNConv
        except ImportError as exc:
            raise RuntimeError(
                "IterativeRelationLayer requires torch-geometric"
            ) from exc

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
            else IterativeRelationController(
                feature_dim=hidden_dim,
                reliability_dim=reliability_dim,
                hidden_dim=hidden_dim,
                dropout=dropout,
                mode=mode,
                base_alpha=base_alpha,
                max_adjustment=max_adjustment,
                num_steps=relation_steps,
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
        self.latest_relation: torch.Tensor | None = None
        self.latest_state: torch.Tensor | None = None
        self.latest_update_gate: torch.Tensor | None = None
        self.latest_base_mixed: torch.Tensor | None = None
        self.latest_local_h: torch.Tensor | None = None
        self.latest_global_h: torch.Tensor | None = None
        self.latest_mixed: torch.Tensor | None = None
        self.relation_scale = 1.0

    def forward(
        self,
        hidden: torch.Tensor,
        edge_index: torch.Tensor,
        reliability: torch.Tensor,
    ) -> torch.Tensor:
        local_h = F.relu(self.local(hidden, edge_index))
        global_h = self.global_attn(hidden)
        base_mixed = (
            self.base_alpha * local_h
            + (1.0 - self.base_alpha) * global_h
        )
        if self.controller is None:
            alpha = hidden.new_full(local_h.shape, self.base_alpha)
            relation_h = torch.zeros_like(local_h)
            state = torch.zeros_like(local_h)
            update_gate = torch.zeros_like(local_h)
        else:
            alpha, relation_h, state, update_gate = self.controller(
                hidden,
                reliability,
                local_h,
                global_h,
            )
        relation_h = self.relation_scale * relation_h
        mixed = base_mixed + relation_h
        self.latest_alpha = alpha.detach()
        self.latest_relation = relation_h.detach()
        self.latest_state = state.detach()
        self.latest_update_gate = update_gate.detach()
        self.latest_base_mixed = base_mixed.detach()
        self.latest_local_h = local_h.detach()
        self.latest_global_h = global_h.detach()
        self.latest_mixed = mixed.detach()
        hidden = self.norm1(hidden + self.dropout(mixed))
        return self.norm2(hidden + self.dropout(self.ffn(hidden)))


class IterativeRelationNetwork(nn.Module):
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
        relation_steps: int,
    ):
        super().__init__()
        if mode not in CONTROL_MODES:
            raise ValueError(f"Unknown control mode: {mode}")
        if relation_steps < 1:
            raise ValueError("relation_steps must be positive")
        self.mode = mode
        self.base_alpha = float(base_alpha)
        self.relation_steps = int(relation_steps)
        self.input_proj = nn.Linear(in_dim, hidden_dim)
        self.layers = nn.ModuleList(
            [
                IterativeRelationLayer(
                    hidden_dim=hidden_dim,
                    reliability_dim=reliability_dim,
                    num_heads=num_heads,
                    dropout=dropout,
                    mode=mode,
                    base_alpha=base_alpha,
                    max_adjustment=max_adjustment,
                    relation_steps=relation_steps,
                )
                for _ in range(num_layers)
            ]
        )
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(hidden_dim, out_dim)

    def set_relation_scales(self, scales: list[float] | tuple[float, ...]) -> None:
        if len(scales) != len(self.layers):
            raise ValueError(
                f"Expected {len(self.layers)} relation scales, got {len(scales)}"
            )
        for layer, scale in zip(self.layers, scales):
            layer.relation_scale = float(scale)

    def reset_relation_scales(self) -> None:
        self.set_relation_scales([1.0] * len(self.layers))

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
        alphas = collect_layer_values(self.layers, "latest_alpha")
        relations = collect_layer_values(self.layers, "latest_relation")
        states = collect_layer_values(self.layers, "latest_state")
        gates = collect_layer_values(self.layers, "latest_update_gate")
        bases = collect_layer_values(self.layers, "latest_base_mixed")
        local_values = collect_layer_values(self.layers, "latest_local_h")
        global_values = collect_layer_values(self.layers, "latest_global_h")
        disagreement = (
            local_values - global_values
            if local_values is not None and global_values is not None
            else None
        )
        adjustments = (
            (alphas - self.base_alpha).abs()
            if alphas is not None
            else None
        )
        output = alpha_diagnostics(alphas, None, adjustments)
        output.update(
            {
                "relation_abs_mean": tensor_stat(relations, "abs_mean"),
                "relation_norm_mean": row_norm_mean(relations),
                "relation_to_base_norm": norm_ratio(relations, bases),
                "relation_relative_strength": norm_mean_ratio(
                    relations,
                    local_values,
                    global_values,
                ),
                "relation_to_branch_disagreement": norm_mean_ratio(
                    relations,
                    disagreement,
                ),
                "relation_state_norm_mean": row_norm_mean(states),
                "relation_update_gate_mean": tensor_stat(gates, "mean"),
                "relation_update_gate_std": tensor_stat(gates, "std"),
            }
        )
        return output


def collect_layer_values(
    layers: nn.ModuleList,
    attribute: str,
) -> torch.Tensor | None:
    values = [
        getattr(layer, attribute)
        for layer in layers
        if getattr(layer, attribute) is not None
    ]
    return torch.cat(values, dim=0) if values else None


def tensor_stat(value: torch.Tensor | None, kind: str) -> float:
    if value is None:
        return math.nan
    if kind == "mean":
        result = value.mean()
    elif kind == "std":
        result = value.std(unbiased=False)
    elif kind == "abs_mean":
        result = value.abs().mean()
    else:
        raise ValueError(f"Unknown tensor statistic: {kind}")
    return float(result.cpu())


def row_norm_mean(value: torch.Tensor | None) -> float:
    if value is None:
        return math.nan
    return float(value.norm(dim=-1).mean().cpu())


def norm_ratio(
    numerator: torch.Tensor | None,
    denominator: torch.Tensor | None,
) -> float:
    if numerator is None or denominator is None:
        return math.nan
    denominator_norm = denominator.norm(dim=-1).clamp_min(1e-12)
    return float(
        (numerator.norm(dim=-1) / denominator_norm).mean().cpu()
    )


def norm_mean_ratio(
    numerator: torch.Tensor | None,
    *denominators: torch.Tensor | None,
) -> float:
    if numerator is None or any(value is None for value in denominators):
        return math.nan
    denominator_norm = sum(
        value.norm(dim=-1).mean()
        for value in denominators
        if value is not None
    )
    if not torch.isfinite(denominator_norm) or denominator_norm <= 1e-12:
        return math.nan
    return float(
        (numerator.norm(dim=-1).mean() / denominator_norm).cpu()
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
