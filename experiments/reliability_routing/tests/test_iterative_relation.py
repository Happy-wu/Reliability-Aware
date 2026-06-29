from __future__ import annotations

import sys
import types

import pytest
import torch
from torch import nn

from src.representation_control import (
    ComponentAlignedReliabilityEncoder,
    ComponentConcatReliabilityEncoder,
    GPSLikeNetwork,
    HiddenMixingNetwork,
    IterativeRelationController,
    IterativeRelationNetwork,
)


def make_controller(steps: int = 2) -> IterativeRelationController:
    return IterativeRelationController(
        feature_dim=8,
        reliability_dim=4,
        hidden_dim=8,
        dropout=0.0,
        mode="combined",
        base_alpha=0.4,
        max_adjustment=0.1,
        num_steps=steps,
    )


def test_zero_initialized_controller_recovers_fixed_mixing() -> None:
    torch.manual_seed(0)
    controller = make_controller()
    features = torch.randn(6, 8)
    reliability = torch.randn(6, 4)
    local_h = torch.randn(6, 8)
    global_h = torch.randn(6, 8)

    alpha, relation_h, _, _ = controller(
        features,
        reliability,
        local_h,
        global_h,
    )

    assert torch.equal(alpha, torch.full_like(alpha, 0.4))
    assert torch.equal(relation_h, torch.zeros_like(relation_h))


def test_relation_is_bounded_and_matches_channel_mixing_identity() -> None:
    torch.manual_seed(1)
    controller = make_controller(steps=3)
    with torch.no_grad():
        controller.alpha_update.weight.fill_(0.05)
        controller.alpha_update.bias.fill_(0.02)
    features = torch.randn(5, 8)
    reliability = torch.randn(5, 4)
    local_h = torch.randn(5, 8)
    global_h = torch.randn(5, 8)

    alpha, relation_h, _, _ = controller(
        features,
        reliability,
        local_h,
        global_h,
    )
    base = 0.4 * local_h + 0.6 * global_h
    corrected = base + relation_h
    direct = alpha * local_h + (1.0 - alpha) * global_h

    assert torch.all(alpha >= 0.3)
    assert torch.all(alpha <= 0.5)
    assert torch.allclose(corrected, direct, atol=1e-6, rtol=1e-6)


def test_node_alpha_type_broadcasts_single_adjustment_per_node() -> None:
    controller = IterativeRelationController(
        feature_dim=8,
        reliability_dim=4,
        hidden_dim=8,
        dropout=0.0,
        mode="combined",
        base_alpha=0.4,
        max_adjustment=0.1,
        num_steps=2,
        alpha_type="node",
    )
    with torch.no_grad():
        controller.alpha_update.weight.fill_(0.05)
        controller.alpha_update.bias.fill_(0.02)
    features = torch.randn(5, 8)
    reliability = torch.randn(5, 4)
    local_h = torch.randn(5, 8)
    global_h = torch.randn(5, 8)

    alpha, relation_h, _, _ = controller(
        features,
        reliability,
        local_h,
        global_h,
    )

    assert controller.alpha_update.out_features == 1
    assert alpha.shape == local_h.shape
    assert torch.allclose(alpha, alpha[:, :1].expand_as(alpha))
    assert relation_h.shape == local_h.shape


def test_group_alpha_type_repeats_group_adjustments() -> None:
    controller = IterativeRelationController(
        feature_dim=8,
        reliability_dim=4,
        hidden_dim=8,
        dropout=0.0,
        mode="combined",
        base_alpha=0.4,
        max_adjustment=0.1,
        num_steps=2,
        alpha_type="group",
        alpha_groups=4,
    )
    with torch.no_grad():
        controller.alpha_update.weight.fill_(0.05)
        controller.alpha_update.bias.copy_(
            torch.tensor([-0.03, -0.01, 0.01, 0.03])
        )
    features = torch.randn(5, 8)
    reliability = torch.randn(5, 4)
    local_h = torch.randn(5, 8)
    global_h = torch.randn(5, 8)

    alpha, relation_h, _, _ = controller(
        features,
        reliability,
        local_h,
        global_h,
    )

    assert controller.alpha_update.out_features == 4
    assert alpha.shape == local_h.shape
    assert torch.allclose(alpha[:, 0], alpha[:, 1])
    assert torch.allclose(alpha[:, 2], alpha[:, 3])
    assert torch.allclose(alpha[:, 4], alpha[:, 5])
    assert torch.allclose(alpha[:, 6], alpha[:, 7])
    assert relation_h.shape == local_h.shape
    assert controller.latest_alpha_raw is not None
    assert controller.latest_alpha_raw.shape == (5, 4)


def test_group_alpha_requires_divisible_hidden_dim() -> None:
    with pytest.raises(ValueError, match="hidden_dim must be divisible"):
        IterativeRelationController(
            feature_dim=8,
            reliability_dim=4,
            hidden_dim=10,
            dropout=0.0,
            mode="combined",
            base_alpha=0.4,
            max_adjustment=0.1,
            num_steps=2,
            alpha_type="group",
            alpha_groups=4,
        )


def test_refinement_steps_share_parameters() -> None:
    controller = make_controller(steps=3)

    assert controller.num_steps == 3
    assert not hasattr(controller, "step_modules")


def test_component_aligned_reliability_encoder_uses_selected_blocks() -> None:
    encoder = ComponentAlignedReliabilityEncoder(
        reliability_dim=7,
        hidden_dim=8,
        dropout=0.0,
        components=["degree", "rwse"],
    )
    reliability = torch.randn(5, 7)

    output = encoder(reliability)

    assert output.shape == (5, 8)
    assert encoder.components == ("degree", "rwse")
    assert set(encoder.encoders.keys()) == {"degree", "rwse"}


def test_component_aligned_reliability_encoder_rejects_empty_components() -> None:
    with pytest.raises(ValueError, match="At least one reliability component"):
        ComponentAlignedReliabilityEncoder(
            reliability_dim=7,
            hidden_dim=8,
            dropout=0.0,
            components=[],
        )


def test_component_aligned_reliability_encoder_checks_input_dim() -> None:
    encoder = ComponentAlignedReliabilityEncoder(
        reliability_dim=7,
        hidden_dim=8,
        dropout=0.0,
    )

    with pytest.raises(ValueError, match="Expected reliability dim 7"):
        encoder(torch.randn(5, 6))


def test_component_concat_encoder_uses_fixed_zero_slots() -> None:
    encoder = ComponentConcatReliabilityEncoder(
        reliability_dim=7,
        component_dim=3,
        dropout=0.0,
        components=["degree", "rwse"],
        missing_mode="zero_slot",
    )
    reliability = torch.randn(5, 7)

    output = encoder(reliability)

    assert output.shape == (5, 12)
    assert encoder.output_dim == 12
    assert torch.equal(output[:, 3:6], torch.zeros_like(output[:, 3:6]))
    assert torch.equal(output[:, 6:9], torch.zeros_like(output[:, 6:9]))


def test_component_concat_encoder_can_omit_unselected_slots() -> None:
    encoder = ComponentConcatReliabilityEncoder(
        reliability_dim=7,
        component_dim=3,
        dropout=0.0,
        components=["degree", "rwse"],
        missing_mode="omit",
    )
    reliability = torch.randn(5, 7)

    output = encoder(reliability)

    assert output.shape == (5, 6)
    assert encoder.output_dim == 6


def test_iterative_controller_accepts_component_aligned_reliability() -> None:
    controller = IterativeRelationController(
        feature_dim=8,
        reliability_dim=7,
        hidden_dim=8,
        dropout=0.0,
        mode="combined",
        base_alpha=0.4,
        max_adjustment=0.1,
        num_steps=2,
        reliability_encoder_mode="component_aligned",
        reliability_components=["degree", "local_similarity", "rwse"],
    )
    features = torch.randn(6, 8)
    reliability = torch.randn(6, 7)
    local_h = torch.randn(6, 8)
    global_h = torch.randn(6, 8)

    alpha, relation_h, state, gate = controller(
        features,
        reliability,
        local_h,
        global_h,
    )

    assert alpha.shape == local_h.shape
    assert relation_h.shape == local_h.shape
    assert state.shape == local_h.shape
    assert gate.shape == local_h.shape


def test_iterative_controller_accepts_component_concat_reliability() -> None:
    controller = IterativeRelationController(
        feature_dim=8,
        reliability_dim=7,
        hidden_dim=8,
        dropout=0.0,
        mode="combined",
        base_alpha=0.4,
        max_adjustment=0.1,
        num_steps=2,
        reliability_encoder_mode="component_concat",
        reliability_components=["degree", "local_similarity", "rwse"],
        reliability_component_dim=2,
    )
    features = torch.randn(6, 8)
    reliability = torch.randn(6, 7)
    local_h = torch.randn(6, 8)
    global_h = torch.randn(6, 8)

    alpha, relation_h, state, gate = controller(
        features,
        reliability,
        local_h,
        global_h,
    )

    assert controller.reliability_encoder.output_dim == 8
    assert alpha.shape == local_h.shape
    assert relation_h.shape == local_h.shape
    assert state.shape == local_h.shape
    assert gate.shape == local_h.shape


def test_component_aligned_initial_network_matches_fixed_backbone(monkeypatch) -> None:
    install_fake_pyg(monkeypatch)
    torch.manual_seed(5)
    baseline = IterativeRelationNetwork(
        **network_kwargs(),
        mode="fixed",
        relation_steps=2,
        reliability_encoder_mode="component_aligned",
    )
    dynamic = IterativeRelationNetwork(
        **network_kwargs(),
        mode="combined",
        relation_steps=2,
        reliability_encoder_mode="component_aligned",
    )
    missing, unexpected = dynamic.load_state_dict(
        baseline.state_dict(),
        strict=False,
    )
    assert missing
    assert all(".controller." in key for key in missing)
    assert not unexpected

    baseline.eval()
    dynamic.eval()
    x = torch.randn(7, 6)
    reliability = torch.randn(7, 4)
    edge_index = torch.empty(2, 0, dtype=torch.long)
    with torch.no_grad():
        baseline_logits = baseline(x, edge_index, reliability)
        dynamic_logits = dynamic(x, edge_index, reliability)

    assert torch.equal(dynamic_logits, baseline_logits)


def test_component_concat_initial_network_matches_fixed_backbone(monkeypatch) -> None:
    install_fake_pyg(monkeypatch)
    torch.manual_seed(6)
    baseline = IterativeRelationNetwork(
        **network_kwargs(),
        mode="fixed",
        relation_steps=2,
        reliability_encoder_mode="component_concat",
        reliability_component_dim=2,
    )
    dynamic = IterativeRelationNetwork(
        **network_kwargs(),
        mode="combined",
        relation_steps=2,
        reliability_encoder_mode="component_concat",
        reliability_component_dim=2,
    )
    missing, unexpected = dynamic.load_state_dict(
        baseline.state_dict(),
        strict=False,
    )
    assert missing
    assert all(".controller." in key for key in missing)
    assert not unexpected

    baseline.eval()
    dynamic.eval()
    x = torch.randn(7, 6)
    reliability = torch.randn(7, 4)
    edge_index = torch.empty(2, 0, dtype=torch.long)
    with torch.no_grad():
        baseline_logits = baseline(x, edge_index, reliability)
        dynamic_logits = dynamic(x, edge_index, reliability)

    assert torch.equal(dynamic_logits, baseline_logits)


def test_iterative_network_saves_raw_group_alpha(monkeypatch) -> None:
    install_fake_pyg(monkeypatch)
    model = IterativeRelationNetwork(
        **network_kwargs(),
        mode="combined",
        relation_steps=2,
        alpha_type="group",
        alpha_groups=4,
    )
    model.eval()
    x = torch.randn(7, 6)
    reliability = torch.randn(7, 4)
    edge_index = torch.empty(2, 0, dtype=torch.long)

    with torch.no_grad():
        model(x, edge_index, reliability)

    assert model.layers[0].latest_alpha.shape == (7, 8)
    assert model.layers[0].latest_alpha_raw is not None
    assert model.layers[0].latest_alpha_raw.shape == (7, 4)


def install_fake_pyg(monkeypatch) -> None:
    class FakeGCNConv(nn.Module):
        def __init__(self, in_dim: int, out_dim: int, **_) -> None:
            super().__init__()
            self.lin = nn.Linear(in_dim, out_dim)

        def forward(
            self,
            x: torch.Tensor,
            edge_index: torch.Tensor,
        ) -> torch.Tensor:
            del edge_index
            return self.lin(x)

    pyg = types.ModuleType("torch_geometric")
    pyg_nn = types.ModuleType("torch_geometric.nn")
    pyg_nn.GCNConv = FakeGCNConv
    pyg.nn = pyg_nn
    monkeypatch.setitem(sys.modules, "torch_geometric", pyg)
    monkeypatch.setitem(sys.modules, "torch_geometric.nn", pyg_nn)


def network_kwargs() -> dict[str, object]:
    return {
        "in_dim": 6,
        "reliability_dim": 4,
        "hidden_dim": 8,
        "out_dim": 3,
        "num_layers": 2,
        "num_heads": 2,
        "dropout": 0.0,
        "base_alpha": 0.4,
        "max_adjustment": 0.1,
    }


def test_fixed_network_has_zero_relation(monkeypatch) -> None:
    install_fake_pyg(monkeypatch)
    model = IterativeRelationNetwork(
        **network_kwargs(),
        mode="fixed",
        relation_steps=2,
    )
    model.eval()
    x = torch.randn(7, 6)
    reliability = torch.randn(7, 4)
    edge_index = torch.empty(2, 0, dtype=torch.long)

    with torch.no_grad():
        model(x, edge_index, reliability)

    assert all(
        torch.equal(
            layer.latest_relation,
            torch.zeros_like(layer.latest_relation),
        )
        for layer in model.layers
    )
    assert model.diagnostic_stats()["relation_norm_mean"] == 0.0


def test_nonfixed_initial_network_matches_fixed_backbone(monkeypatch) -> None:
    install_fake_pyg(monkeypatch)
    torch.manual_seed(2)
    baseline = HiddenMixingNetwork(
        **network_kwargs(),
        mode="fixed",
        lambda_init=0.001,
    )
    fixed = IterativeRelationNetwork(
        **network_kwargs(),
        mode="fixed",
        relation_steps=2,
    )
    fixed.load_state_dict(baseline.state_dict())
    dynamic = IterativeRelationNetwork(
        **network_kwargs(),
        mode="combined",
        relation_steps=2,
    )
    missing, unexpected = dynamic.load_state_dict(
        baseline.state_dict(),
        strict=False,
    )
    assert missing
    assert all(".controller." in key for key in missing)
    assert not unexpected

    baseline.eval()
    fixed.eval()
    dynamic.eval()
    x = torch.randn(7, 6)
    reliability = torch.randn(7, 4)
    edge_index = torch.empty(2, 0, dtype=torch.long)
    with torch.no_grad():
        baseline_logits = baseline(x, edge_index, reliability)
        fixed_logits = fixed(x, edge_index, reliability)
        dynamic_logits = dynamic(x, edge_index, reliability)

    assert torch.equal(fixed_logits, baseline_logits)
    assert torch.allclose(dynamic_logits, baseline_logits, atol=5e-4, rtol=0.0)


def test_relation_scales_support_reversible_causal_ablation(monkeypatch) -> None:
    install_fake_pyg(monkeypatch)
    torch.manual_seed(4)
    model = IterativeRelationNetwork(
        **network_kwargs(),
        mode="combined",
        relation_steps=2,
    )
    with torch.no_grad():
        for layer in model.layers:
            layer.controller.alpha_update.weight.fill_(0.03)
            layer.controller.alpha_update.bias.fill_(0.01)
    model.eval()
    x = torch.randn(7, 6)
    reliability = torch.randn(7, 4)
    edge_index = torch.empty(2, 0, dtype=torch.long)

    with torch.no_grad():
        normal_logits = model(x, edge_index, reliability)
        model.set_relation_scales([0.0, 0.0])
        zero_logits = model(x, edge_index, reliability)

    assert all(
        torch.equal(
            layer.latest_relation,
            torch.zeros_like(layer.latest_relation),
        )
        for layer in model.layers
    )
    assert not torch.equal(normal_logits, zero_logits)

    model.reset_relation_scales()
    with torch.no_grad():
        restored_logits = model(x, edge_index, reliability)

    assert torch.equal(restored_logits, normal_logits)


def test_gps_like_nonfixed_initial_network_matches_fixed_backbone(monkeypatch) -> None:
    install_fake_pyg(monkeypatch)
    torch.manual_seed(3)
    baseline = GPSLikeNetwork(
        **network_kwargs(),
        mode="fixed",
        lambda_init=0.001,
    )
    dynamic = GPSLikeNetwork(
        **network_kwargs(),
        mode="combined",
        lambda_init=0.001,
    )
    missing, unexpected = dynamic.load_state_dict(
        baseline.state_dict(),
        strict=False,
    )
    assert missing
    assert all(".controller." in key for key in missing)
    assert not unexpected

    baseline.eval()
    dynamic.eval()
    x = torch.randn(7, 6)
    reliability = torch.randn(7, 4)
    edge_index = torch.empty(2, 0, dtype=torch.long)
    with torch.no_grad():
        baseline_logits = baseline(x, edge_index, reliability)
        dynamic_logits = dynamic(x, edge_index, reliability)

    assert torch.allclose(dynamic_logits, baseline_logits, atol=5e-4, rtol=0.0)
