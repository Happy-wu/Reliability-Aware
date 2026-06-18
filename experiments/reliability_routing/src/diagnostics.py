from __future__ import annotations

import math

import numpy as np
import torch


def empty_diagnostics() -> dict[str, float]:
    return {
        "qk_strength_mean": math.nan,
        "qk_strength_layer1": math.nan,
        "qk_strength_layer2": math.nan,
        "qk_gamma_q_abs_dev_mean": math.nan,
        "qk_gamma_k_abs_dev_mean": math.nan,
        "qk_gamma_q_std": math.nan,
        "qk_gamma_k_std": math.nan,
        "qk_gamma_q_abs_dev_max": math.nan,
        "qk_gamma_k_abs_dev_max": math.nan,
        "gate_corr_degree": math.nan,
        "gate_corr_local_similarity": math.nan,
        "gate_corr_neighbor_variance": math.nan,
        "gate_corr_rwse_mean": math.nan,
        "gate_corr_layer1_local_similarity": math.nan,
        "gate_corr_layer2_local_similarity": math.nan,
        "gate_mean": math.nan,
        "gate_std": math.nan,
        "gate_min": math.nan,
        "gate_max": math.nan,
        "local_branch_norm_mean": math.nan,
        "global_branch_norm_mean": math.nan,
        "mixed_branch_norm_mean": math.nan,
        "local_global_cosine_mean": math.nan,
    }


def collect_diagnostics(model: torch.nn.Module, data) -> dict[str, float]:
    diagnostics = empty_diagnostics()
    strengths = getattr(model, "qk_strengths", lambda: [])()
    if strengths:
        diagnostics["qk_strength_mean"] = float(np.mean(strengths))
        diagnostics["qk_strength_layer1"] = strengths[0]
        diagnostics["qk_strength_layer2"] = (
            strengths[1] if len(strengths) >= 2 else math.nan
        )
    diagnostics.update(getattr(model, "qk_gamma_stats", lambda: {})())
    diagnostics.update(getattr(model, "branch_stats", lambda: {})())

    gate = getattr(model, "latest_gate", None)
    if gate is not None:
        gate_np = gate.detach().cpu().view(-1).numpy()
        reliability = data.reliability_gate_raw.detach().cpu()
        diagnostics["gate_corr_degree"] = safe_corr(
            gate_np, reliability[:, 0].numpy()
        )
        diagnostics["gate_corr_local_similarity"] = safe_corr(
            gate_np, data.local_similarity.detach().cpu().view(-1).numpy()
        )
        diagnostics["gate_corr_neighbor_variance"] = safe_corr(
            gate_np, reliability[:, 2].numpy()
        )
        diagnostics["gate_corr_rwse_mean"] = safe_corr(
            gate_np, reliability[:, 3:].mean(dim=1).numpy()
        )

    gates = getattr(model, "latest_gates_by_layer", [])
    if len(gates) >= 1:
        diagnostics["gate_corr_layer1_local_similarity"] = safe_corr(
            gates[0].detach().cpu().view(-1).numpy(),
            data.local_similarity.detach().cpu().view(-1).numpy(),
        )
    if len(gates) >= 2:
        diagnostics["gate_corr_layer2_local_similarity"] = safe_corr(
            gates[1].detach().cpu().view(-1).numpy(),
            data.local_similarity.detach().cpu().view(-1).numpy(),
        )
    return diagnostics


def safe_corr(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) < 1e-8 or np.std(b) < 1e-8:
        return math.nan
    return float(np.corrcoef(a, b)[0, 1])


def move_data(data, device: torch.device):
    for field in (
        "x",
        "y",
        "edge_index",
        "reliability",
        "reliability_gate",
        "reliability_qk",
        "reliability_gate_raw",
        "reliability_qk_raw",
        "train_mask",
        "val_mask",
        "test_mask",
        "local_similarity",
    ):
        setattr(data, field, getattr(data, field).to(device))
    return data
