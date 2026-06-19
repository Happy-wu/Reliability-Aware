from __future__ import annotations

import math

import numpy as np
import torch
from torch import nn


ROUTERS = ("reliability_only", "node_feature_only", "combined")


class PreferenceRouter(nn.Module):
    def __init__(
        self,
        feature_dim: int,
        reliability_dim: int,
        hidden_dim: int,
        dropout: float,
        mode: str,
    ):
        super().__init__()
        if mode not in ROUTERS:
            raise ValueError(f"Unknown preference router: {mode}")
        self.mode = mode
        input_dim = {
            "reliability_only": reliability_dim,
            "node_feature_only": feature_dim,
            "combined": feature_dim + reliability_dim,
        }[mode]
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
        )

    def forward(
        self,
        x: torch.Tensor,
        reliability: torch.Tensor,
    ) -> torch.Tensor:
        if self.mode == "reliability_only":
            inputs = reliability
        elif self.mode == "node_feature_only":
            inputs = x
        else:
            inputs = torch.cat([x, reliability], dim=-1)
        return self.net(inputs).view(-1)


def preference_targets(
    local_logits: torch.Tensor,
    global_logits: torch.Tensor,
    y: torch.Tensor,
    candidate_mask: torch.Tensor,
) -> torch.Tensor:
    """Return -1 for ignored nodes, 0 for global, and 1 for local."""
    local_correct = local_logits.argmax(dim=-1) == y
    global_correct = global_logits.argmax(dim=-1) == y
    targets = torch.full_like(y, -1)
    targets[candidate_mask & local_correct & ~global_correct] = 1
    targets[candidate_mask & ~local_correct & global_correct] = 0
    return targets


def preference_metrics(
    router_logits: torch.Tensor,
    targets: torch.Tensor,
    mask: torch.Tensor,
    threshold: float = 0.5,
) -> dict[str, float | int]:
    selected = mask & (targets >= 0)
    count = int(selected.sum())
    if count == 0:
        return empty_preference_metrics()

    target = targets[selected].detach().cpu().numpy()
    score = router_logits[selected].sigmoid().detach().cpu().numpy()
    prediction = (score >= threshold).astype(np.int64)
    local_count = int((target == 1).sum())
    global_count = int((target == 0).sum())
    accuracy = float((prediction == target).mean())

    if local_count and global_count:
        from sklearn.metrics import balanced_accuracy_score, roc_auc_score

        auc = float(roc_auc_score(target, score))
        balanced_accuracy = float(balanced_accuracy_score(target, prediction))
    else:
        auc = math.nan
        balanced_accuracy = math.nan
    return {
        **preference_label_counts(targets, mask),
        "preference_auc": auc,
        "balanced_accuracy": balanced_accuracy,
        "routing_accuracy": accuracy,
    }


def select_preference_threshold(
    router_logits: torch.Tensor,
    targets: torch.Tensor,
    mask: torch.Tensor,
) -> float:
    selected = mask & (targets >= 0)
    target = targets[selected].detach().cpu().numpy()
    if target.size == 0 or np.unique(target).size < 2:
        return math.nan
    score = router_logits[selected].sigmoid().detach().cpu().numpy()

    from sklearn.metrics import roc_curve

    false_positive_rate, true_positive_rate, thresholds = roc_curve(
        target,
        score,
    )
    balanced_accuracy = (
        true_positive_rate + (1.0 - false_positive_rate)
    ) / 2.0
    finite = np.isfinite(thresholds)
    best_value = balanced_accuracy[finite].max()
    candidates = thresholds[
        finite & np.isclose(balanced_accuracy, best_value)
    ]
    return float(candidates[np.argmin(np.abs(candidates - 0.5))])


def majority_preference_choice(
    targets: torch.Tensor,
    mask: torch.Tensor,
) -> int | None:
    counts = preference_label_counts(targets, mask)
    if counts["preference_count"] == 0:
        return None
    return int(
        counts["local_preference_count"]
        >= counts["global_preference_count"]
    )


def constant_preference_metrics(
    choice: int | None,
    targets: torch.Tensor,
    mask: torch.Tensor,
) -> dict[str, float | int]:
    counts = preference_label_counts(targets, mask)
    if choice is None or counts["preference_count"] == 0:
        return empty_preference_metrics()
    selected = mask & (targets >= 0)
    target = targets[selected].detach().cpu().numpy()
    prediction = np.full(target.shape, choice, dtype=np.int64)
    if np.unique(target).size >= 2:
        from sklearn.metrics import balanced_accuracy_score

        balanced_accuracy = float(
            balanced_accuracy_score(target, prediction)
        )
    else:
        balanced_accuracy = math.nan
    return {
        **counts,
        "preference_auc": 0.5,
        "balanced_accuracy": balanced_accuracy,
        "routing_accuracy": float((prediction == target).mean()),
    }


def preference_label_counts(
    targets: torch.Tensor,
    mask: torch.Tensor,
) -> dict[str, int]:
    selected = mask & (targets >= 0)
    selected_targets = targets[selected]
    return {
        "preference_count": int(selected.sum()),
        "local_preference_count": int((selected_targets == 1).sum()),
        "global_preference_count": int((selected_targets == 0).sum()),
    }


def routed_node_accuracy(
    router_logits: torch.Tensor,
    local_logits: torch.Tensor,
    global_logits: torch.Tensor,
    y: torch.Tensor,
    mask: torch.Tensor,
    threshold: float = 0.5,
) -> float:
    choose_local = router_logits.sigmoid().unsqueeze(-1) >= threshold
    routed_logits = torch.where(choose_local, local_logits, global_logits)
    return float((routed_logits[mask].argmax(dim=-1) == y[mask]).float().mean())


def constant_routed_node_accuracy(
    choice: int | None,
    local_logits: torch.Tensor,
    global_logits: torch.Tensor,
    y: torch.Tensor,
    mask: torch.Tensor,
) -> float:
    if choice is None:
        return math.nan
    logits = local_logits if choice == 1 else global_logits
    return float((logits[mask].argmax(dim=-1) == y[mask]).float().mean())


def empty_preference_metrics() -> dict[str, float | int]:
    return {
        "preference_count": 0,
        "local_preference_count": 0,
        "global_preference_count": 0,
        "preference_auc": math.nan,
        "balanced_accuracy": math.nan,
        "routing_accuracy": math.nan,
    }
