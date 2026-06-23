from __future__ import annotations

import sys
import types

import torch
from torch import nn

from src.representation_control import (
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


def test_refinement_steps_share_parameters() -> None:
    controller = make_controller(steps=3)

    assert controller.num_steps == 3
    assert not hasattr(controller, "step_modules")


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
