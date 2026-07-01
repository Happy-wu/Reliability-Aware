from __future__ import annotations

import json
import csv
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

from run_representation_control import (
    find_compatible_hidden_cache,
    hidden_cache_metadata,
    hidden_cache_path,
    validate_args,
)


def base_args(**updates):
    values = {
        "runs": 1,
        "fixed_alphas": [0.0, 0.5, 1.0],
        "max_adjustment": 0.1,
        "lambda_init": 0.001,
        "relation_steps": 1,
        "family": "iterative_relation_frozen",
        "control_mode": "reliability_only",
        "causal_interventions": True,
        "reliability_component_dim": 16,
        "component_missing_mode": "zero_slot",
        "reuse_compatible_backbone_cache": False,
        "compatible_backbone_cache_config": None,
        "save_external_expert_logits": False,
        "save_node_diagnostics": False,
    }
    values.update(updates)
    return SimpleNamespace(**values)


def cache_args(tmp_path: Path, **updates):
    values = {
        "backbone_cache_dir": tmp_path / "_backbone_cache",
        "compatible_backbone_cache_config": tmp_path / "suite_config.json",
        "data_fingerprint": "data-fingerprint",
        "preprocess_code_hash": "preprocess-hash",
        "dataset": "Roman-empire",
        "family": "iterative_relation_frozen",
        "edge_protocol": "undirected",
        "normalize_features": True,
        "fixed_alphas": [0.0, 0.5, 1.0],
        "hidden_dim": 64,
        "num_layers": 2,
        "num_heads": 4,
        "dropout": 0.3,
        "lr": 0.003,
        "weight_decay": 0.0001,
        "expert_epochs": 300,
        "patience": 60,
        "reliability_component_dim": 16,
        "component_missing_mode": "zero_slot",
    }
    values.update(updates)
    return SimpleNamespace(**values)


def test_causal_intervention_rejects_semantically_invalid_control() -> None:
    args = base_args(control_mode="zero_reliability")

    with pytest.raises(ValueError, match="supports only fixed"):
        validate_args(args)


def test_external_logits_require_node_diagnostics() -> None:
    args = base_args(
        causal_interventions=False,
        save_external_expert_logits=True,
    )

    with pytest.raises(ValueError, match="requires --save-node-diagnostics"):
        validate_args(args)


def test_legacy_cache_reuse_rejects_mismatched_suite_config(
    tmp_path: Path,
) -> None:
    args = cache_args(tmp_path)
    config = {
        "edge_protocol": "undirected",
        "normalize_features": True,
        "hidden_dim": 32,
        "num_layers": 2,
        "num_heads": 4,
        "dropout": 0.3,
        "lr": 0.003,
        "weight_decay": 0.0001,
        "expert_epochs": 300,
        "patience": 60,
        "fixed_alphas": [0.0, 0.5, 1.0],
        "families": ["iterative_relation_frozen"],
        "data_fingerprints": {
            "Roman-empire": "data-fingerprint",
        },
    }
    args.compatible_backbone_cache_config.write_text(
        json.dumps(config),
        encoding="utf-8",
    )
    expected_path = hidden_cache_path(args, split=0, seed=0)
    expected_path.parent.mkdir(parents=True)
    legacy_path = expected_path.parent / "hidden_split0_seed0_legacy.pt"
    torch.save(
        {
            "alpha": 0.5,
            "result": {"val_score": 0.8},
            "state_dict": {},
        },
        legacy_path,
    )

    with pytest.raises(RuntimeError, match="Incompatible legacy"):
        find_compatible_hidden_cache(args, expected_path, split=0, seed=0)


def test_cache_search_skips_metadata_mismatch_and_uses_match(
    tmp_path: Path,
) -> None:
    args = cache_args(tmp_path)
    expected_path = hidden_cache_path(args, split=0, seed=0)
    expected_path.parent.mkdir(parents=True)
    metadata = hidden_cache_metadata(args, split=0, seed=0)

    mismatched = dict(metadata)
    mismatched["hidden_dim"] = 32
    torch.save(
        {
            "alpha": 0.5,
            "result": {"val_score": 0.95},
            "metadata": mismatched,
            "state_dict": {},
        },
        expected_path.parent / "hidden_split0_seed0_mismatch.pt",
    )
    compatible_path = (
        expected_path.parent / "hidden_split0_seed0_compatible.pt"
    )
    torch.save(
        {
            "alpha": 0.5,
            "result": {"val_score": 0.80},
            "metadata": metadata,
            "state_dict": {},
        },
        compatible_path,
    )

    selected = find_compatible_hidden_cache(
        args,
        expected_path,
        split=0,
        seed=0,
    )

    assert selected == compatible_path


def test_cache_search_reports_when_all_metadata_mismatch(
    tmp_path: Path,
) -> None:
    args = cache_args(tmp_path)
    expected_path = hidden_cache_path(args, split=0, seed=0)
    expected_path.parent.mkdir(parents=True)
    metadata = hidden_cache_metadata(args, split=0, seed=0)
    metadata["hidden_dim"] = 32
    torch.save(
        {
            "alpha": 0.5,
            "result": {"val_score": 0.95},
            "metadata": metadata,
            "state_dict": {},
        },
        expected_path.parent / "hidden_split0_seed0_mismatch.pt",
    )

    with pytest.raises(RuntimeError, match="No compatible backbone cache"):
        find_compatible_hidden_cache(
            args,
            expected_path,
            split=0,
            seed=0,
        )


def test_legacy_cache_search_matches_fixed_csv_per_file(
    tmp_path: Path,
) -> None:
    args = cache_args(tmp_path)
    config = {
        "edge_protocol": "undirected",
        "normalize_features": True,
        "hidden_dim": 64,
        "num_layers": 2,
        "num_heads": 4,
        "dropout": 0.3,
        "lr": 0.003,
        "weight_decay": 0.0001,
        "expert_epochs": 300,
        "patience": 60,
        "fixed_alphas": [0.0, 0.5, 1.0],
        "families": ["iterative_relation_frozen"],
        "data_fingerprints": {
            "Roman-empire": "data-fingerprint",
        },
    }
    args.compatible_backbone_cache_config.write_text(
        json.dumps(config),
        encoding="utf-8",
    )
    result_path = (
        tmp_path / "Roman-empire_iterative_relation_frozen_fixed.csv"
    )
    row = {
        "family": "iterative_relation_frozen",
        "split": "0",
        "seed": "0",
        "data_fingerprint": "data-fingerprint",
        "preprocess_code_hash": "preprocess-hash",
        "edge_protocol": "undirected",
        "normalize_features": "True",
        "hidden_dim": "64",
        "num_layers": "2",
        "num_heads": "4",
        "dropout": "0.3",
        "lr": "0.003",
        "weight_decay": "0.0001",
        "expert_epochs": "300",
        "patience": "60",
        "fixed_alphas": "0.0,0.5,1.0",
        "base_alpha": "0.5",
        "best_val_primary": "0.8",
        "test_primary_at_best_val": "0.7",
    }
    with result_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)

    expected_path = hidden_cache_path(args, split=0, seed=0)
    expected_path.parent.mkdir(parents=True)
    wrong_path = expected_path.parent / "hidden_split0_seed0_wrong.pt"
    correct_path = expected_path.parent / "hidden_split0_seed0_correct.pt"
    torch.save(
        {
            "alpha": 0.75,
            "result": {"val_score": 0.9, "test_score": 0.8},
            "state_dict": {"weight": torch.tensor([1.0])},
        },
        wrong_path,
    )
    torch.save(
        {
            "alpha": 0.5,
            "result": {"val_score": 0.8, "test_score": 0.7},
            "state_dict": {"weight": torch.tensor([2.0])},
        },
        correct_path,
    )

    selected = find_compatible_hidden_cache(
        args,
        expected_path,
        split=0,
        seed=0,
    )

    assert selected == correct_path
