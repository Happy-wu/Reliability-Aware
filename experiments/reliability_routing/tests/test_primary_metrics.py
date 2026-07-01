from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch

from run_expert_fusion import evaluate_result
from src.real_data import dataset_has_local_files, primary_metric_for_dataset


def metric_data(primary_metric: str) -> SimpleNamespace:
    return SimpleNamespace(
        y=torch.tensor([0, 0, 1, 1]),
        train_mask=torch.tensor([True, True, True, True]),
        val_mask=torch.tensor([True, True, True, True]),
        test_mask=torch.tensor([True, True, True, True]),
        primary_metric=primary_metric,
    )


def test_dataset_primary_metrics() -> None:
    assert primary_metric_for_dataset("Roman-empire") == "accuracy"
    assert primary_metric_for_dataset("Minesweeper") == "roc_auc"
    assert primary_metric_for_dataset("Tolokers") == "roc_auc"
    assert primary_metric_for_dataset("Questions") == "roc_auc"


def test_roc_auc_is_used_as_primary_score() -> None:
    logits = torch.tensor(
        [
            [0.0, 0.4],
            [0.0, 0.3],
            [0.0, 0.6],
            [0.0, 0.5],
        ]
    )
    result = evaluate_result(logits, metric_data("roc_auc"), epoch=2)

    assert result["val_acc"] == pytest.approx(0.5)
    assert result["val_roc_auc"] == pytest.approx(1.0)
    assert result["train_score"] == pytest.approx(1.0)
    assert result["val_score"] == pytest.approx(1.0)
    assert result["primary_metric"] == "roc_auc"


def test_accuracy_remains_primary_for_multiclass_protocol() -> None:
    logits = torch.tensor(
        [
            [0.0, 0.4],
            [0.0, 0.3],
            [0.0, 0.6],
            [0.0, 0.5],
        ]
    )
    result = evaluate_result(logits, metric_data("accuracy"), epoch=2)

    assert result["val_score"] == pytest.approx(result["val_acc"])
    assert result["train_score"] == pytest.approx(result["train_acc"])
    assert result["primary_metric"] == "accuracy"


def test_dataset_presence_requires_nonempty_files(tmp_path) -> None:
    raw_dir = tmp_path / "tolokers" / "raw"
    raw_dir.mkdir(parents=True)
    assert not dataset_has_local_files("Tolokers", tmp_path)

    (raw_dir / "tolokers.npz").write_bytes(b"data")
    assert dataset_has_local_files("Tolokers", tmp_path)
