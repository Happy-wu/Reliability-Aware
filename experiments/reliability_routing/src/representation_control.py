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
ALPHA_TYPES = ("node", "group", "channel")
RELIABILITY_ENCODER_MODES = (
    "raw_concat",
    "component_mean",
    "component_aligned",
    "component_concat",
)
COMPONENT_MISSING_MODES = ("zero_slot", "omit")
RELIABILITY_COMPONENTS = (
    "degree",
    "local_similarity",
    "neighbor_variance",
    "rwse",
)


class ComponentAlignedReliabilityEncoder(nn.Module):
    """Encode each reliability component block before fusing them.

    The reliability layout is fixed by src.data:
    [degree, local_similarity, neighbor_variance, rwse_1, ...].
    Selected-out components are omitted instead of feeding zero values through a
    biased encoder, so component ablations remain clean.
    """

    def __init__(
        self,
        reliability_dim: int,
        hidden_dim: int,
        dropout: float = 0.3,
        components: list[str] | tuple[str, ...] | None = None,
    ):
        super().__init__()
        if reliability_dim < 3:
            raise ValueError("component_aligned reliability requires at least 3 dims")
        selected = tuple(
            RELIABILITY_COMPONENTS if components is None else components
        )
        unknown = set(selected).difference(RELIABILITY_COMPONENTS)
        if unknown:
            raise ValueError(f"Unknown reliability components: {sorted(unknown)}")
        if not selected:
            raise ValueError("At least one reliability component must be selected")

        rwse_dim = reliability_dim - 3
        dims = {
            "degree": 1,
            "local_similarity": 1,
            "neighbor_variance": 1,
            "rwse": rwse_dim,
        }
        if "rwse" in selected and rwse_dim <= 0:
            raise ValueError("rwse component was selected but no RWSE dims exist")

        self.reliability_dim = int(reliability_dim)
        self.output_dim = int(hidden_dim)
        self.components = tuple(
            component for component in RELIABILITY_COMPONENTS if component in selected
        )
        self.rwse_dim = rwse_dim
        self.encoders = nn.ModuleDict(
            {
                component: self._make_encoder(dims[component], hidden_dim, dropout)
                for component in self.components
            }
        )
        self.fusion = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
        )

    @staticmethod
    def _make_encoder(
        in_dim: int,
        hidden_dim: int,
        dropout: float,
    ) -> nn.Sequential:
        return nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
        )

    def _component_input(
        self,
        reliability: torch.Tensor,
        component: str,
    ) -> torch.Tensor:
        if component == "degree":
            return reliability[:, 0:1]
        if component == "local_similarity":
            return reliability[:, 1:2]
        if component == "neighbor_variance":
            return reliability[:, 2:3]
        if component == "rwse":
            return reliability[:, 3:]
        raise ValueError(f"Unknown reliability component: {component}")

    def forward(self, reliability: torch.Tensor) -> torch.Tensor:
        if reliability.size(1) != self.reliability_dim:
            raise ValueError(
                f"Expected reliability dim {self.reliability_dim}, "
                f"got {reliability.size(1)}"
            )
        pieces = [
            self.encoders[component](self._component_input(reliability, component))
            for component in self.components
        ]
        return self.fusion(torch.stack(pieces, dim=0).mean(dim=0))


class ComponentConcatReliabilityEncoder(nn.Module):
    """Encode component slots separately and concatenate them.

    With zero_slot mode every canonical component keeps a fixed slot; unselected
    components become exact zeros without passing through biased encoders. This
    keeps controller context width stable across component ablations.
    """

    def __init__(
        self,
        reliability_dim: int,
        component_dim: int,
        dropout: float = 0.3,
        components: list[str] | tuple[str, ...] | None = None,
        missing_mode: str = "zero_slot",
    ):
        super().__init__()
        if reliability_dim < 3:
            raise ValueError("component_concat reliability requires at least 3 dims")
        if component_dim < 1:
            raise ValueError("reliability component dim must be positive")
        if missing_mode not in COMPONENT_MISSING_MODES:
            raise ValueError(f"Unknown component missing mode: {missing_mode}")
        selected = tuple(
            RELIABILITY_COMPONENTS if components is None else components
        )
        unknown = set(selected).difference(RELIABILITY_COMPONENTS)
        if unknown:
            raise ValueError(f"Unknown reliability components: {sorted(unknown)}")
        if not selected:
            raise ValueError("At least one reliability component must be selected")

        rwse_dim = reliability_dim - 3
        dims = {
            "degree": 1,
            "local_similarity": 1,
            "neighbor_variance": 1,
            "rwse": rwse_dim,
        }
        if "rwse" in selected and rwse_dim <= 0:
            raise ValueError("rwse component was selected but no RWSE dims exist")

        self.reliability_dim = int(reliability_dim)
        self.component_dim = int(component_dim)
        self.missing_mode = missing_mode
        self.selected_components = tuple(
            component for component in RELIABILITY_COMPONENTS if component in selected
        )
        self.slot_components = (
            RELIABILITY_COMPONENTS
            if missing_mode == "zero_slot"
            else self.selected_components
        )
        self.output_dim = len(self.slot_components) * self.component_dim
        encoder_components = (
            RELIABILITY_COMPONENTS
            if missing_mode == "zero_slot"
            else self.selected_components
        )
        self.encoders = nn.ModuleDict(
            {
                component: ComponentAlignedReliabilityEncoder._make_encoder(
                    dims[component],
                    self.component_dim,
                    dropout,
                )
                for component in encoder_components
            }
        )

    def _component_input(
        self,
        reliability: torch.Tensor,
        component: str,
    ) -> torch.Tensor:
        if component == "degree":
            return reliability[:, 0:1]
        if component == "local_similarity":
            return reliability[:, 1:2]
        if component == "neighbor_variance":
            return reliability[:, 2:3]
        if component == "rwse":
            return reliability[:, 3:]
        raise ValueError(f"Unknown reliability component: {component}")

    def forward(self, reliability: torch.Tensor) -> torch.Tensor:
        if reliability.size(1) != self.reliability_dim:
            raise ValueError(
                f"Expected reliability dim {self.reliability_dim}, "
                f"got {reliability.size(1)}"
            )
        pieces = []
        for component in self.slot_components:
            if component in self.selected_components:
                pieces.append(
                    self.encoders[component](
                        self._component_input(reliability, component)
                    )
                )
            else:
                pieces.append(
                    reliability.new_zeros(
                        reliability.size(0),
                        self.component_dim,
                    )
                )
        return torch.cat(pieces, dim=-1)


def build_reliability_encoder(
    reliability_dim: int,
    hidden_dim: int,
    dropout: float,
    mode: str,
    components: list[str] | tuple[str, ...] | None,
    component_dim: int,
    component_missing_mode: str,
) -> nn.Module:
    if mode == "raw_concat":
        encoder = ReliabilityEncoder(reliability_dim, hidden_dim, dropout=dropout)
        encoder.output_dim = hidden_dim
        return encoder
    if mode in {"component_mean", "component_aligned"}:
        return ComponentAlignedReliabilityEncoder(
            reliability_dim,
            hidden_dim,
            dropout=dropout,
            components=components,
        )
    if mode == "component_concat":
        return ComponentConcatReliabilityEncoder(
            reliability_dim,
            component_dim=component_dim,
            dropout=dropout,
            components=components,
            missing_mode=component_missing_mode,
        )
    raise ValueError(f"Unknown reliability encoder mode: {mode}")


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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
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
        self.reliability_encoder = build_reliability_encoder(
            reliability_dim,
            hidden_dim,
            dropout,
            reliability_encoder_mode,
            reliability_components,
            reliability_component_dim,
            component_missing_mode,
        )
        self.trunk = nn.Sequential(
            nn.Linear(hidden_dim + self.reliability_encoder.output_dim, hidden_dim),
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
    """Refine local/global mixing with shared recurrent weights."""

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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
        alpha_type: str = "channel",
        alpha_groups: int = 4,
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
        if alpha_type not in ALPHA_TYPES:
            raise ValueError(f"Unknown alpha_type: {alpha_type}")
        if alpha_groups < 1:
            raise ValueError("alpha_groups must be positive")
        if alpha_type == "group" and hidden_dim % alpha_groups != 0:
            raise ValueError("hidden_dim must be divisible by alpha_groups")

        self.mode = mode
        self.base_alpha = float(base_alpha)
        self.max_adjustment = float(max_adjustment)
        self.num_steps = int(num_steps)
        self.alpha_type = alpha_type
        self.alpha_groups = int(alpha_groups)
        self.alpha_dim = self._alpha_dim(hidden_dim)
        self.feature_encoder = nn.Sequential(
            nn.Linear(feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.LayerNorm(hidden_dim),
        )
        self.reliability_encoder = build_reliability_encoder(
            reliability_dim,
            hidden_dim,
            dropout,
            reliability_encoder_mode,
            reliability_components,
            reliability_component_dim,
            component_missing_mode,
        )
        context_dim = hidden_dim * 4 + self.reliability_encoder.output_dim
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
        self.alpha_update = nn.Linear(hidden_dim, self.alpha_dim)
        nn.init.zeros_(self.alpha_update.weight)
        nn.init.zeros_(self.alpha_update.bias)
        self.latest_alpha_raw: torch.Tensor | None = None

    def _alpha_dim(self, hidden_dim: int) -> int:
        if self.alpha_type == "node":
            return 1
        if self.alpha_type == "group":
            return self.alpha_groups
        return hidden_dim

    def expand_alpha(self, alpha: torch.Tensor, hidden_dim: int) -> torch.Tensor:
        if self.alpha_type == "node":
            return alpha.expand(-1, hidden_dim)
        if self.alpha_type == "group":
            return alpha.repeat_interleave(hidden_dim // self.alpha_groups, dim=-1)
        return alpha

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
        raw_adjustment = local_h.new_zeros(local_h.size(0), self.alpha_dim)
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
        expanded_alpha = self.expand_alpha(alpha, difference.size(-1))
        self.latest_alpha_raw = alpha.detach()
        relation_h = (expanded_alpha - self.base_alpha) * difference
        mean_gate = torch.stack(gates, dim=0).mean(dim=0)
        return expanded_alpha, relation_h, state, mean_gate


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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
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
                reliability_encoder_mode=reliability_encoder_mode,
                reliability_components=reliability_components,
                reliability_component_dim=reliability_component_dim,
                component_missing_mode=component_missing_mode,
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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
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
                reliability_encoder_mode=reliability_encoder_mode,
                reliability_components=reliability_components,
                reliability_component_dim=reliability_component_dim,
                component_missing_mode=component_missing_mode,
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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
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
                    reliability_encoder_mode=reliability_encoder_mode,
                    reliability_components=reliability_components,
                    reliability_component_dim=reliability_component_dim,
                    component_missing_mode=component_missing_mode,
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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
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
                reliability_encoder_mode=reliability_encoder_mode,
                reliability_components=reliability_components,
                reliability_component_dim=reliability_component_dim,
                component_missing_mode=component_missing_mode,
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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
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
                    reliability_encoder_mode=reliability_encoder_mode,
                    reliability_components=reliability_components,
                    reliability_component_dim=reliability_component_dim,
                    component_missing_mode=component_missing_mode,
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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
        alpha_type: str = "channel",
        alpha_groups: int = 4,
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
                reliability_encoder_mode=reliability_encoder_mode,
                reliability_components=reliability_components,
                reliability_component_dim=reliability_component_dim,
                component_missing_mode=component_missing_mode,
                alpha_type=alpha_type,
                alpha_groups=alpha_groups,
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
        self.latest_alpha_raw: torch.Tensor | None = None
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
            alpha_raw = hidden.new_full((hidden.size(0), 1), self.base_alpha)
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
            alpha_raw = self.controller.latest_alpha_raw
        relation_h = self.relation_scale * relation_h
        mixed = base_mixed + relation_h
        self.latest_alpha = alpha.detach()
        self.latest_alpha_raw = (
            alpha_raw.detach() if alpha_raw is not None else None
        )
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
        reliability_encoder_mode: str = "raw_concat",
        reliability_components: list[str] | tuple[str, ...] | None = None,
        reliability_component_dim: int = 16,
        component_missing_mode: str = "zero_slot",
        alpha_type: str = "channel",
        alpha_groups: int = 4,
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
                    reliability_encoder_mode=reliability_encoder_mode,
                    reliability_components=reliability_components,
                    reliability_component_dim=reliability_component_dim,
                    component_missing_mode=component_missing_mode,
                    alpha_type=alpha_type,
                    alpha_groups=alpha_groups,
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
