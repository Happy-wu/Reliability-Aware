from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import torch

from run_expert_fusion import (
    accuracy,
    code_hash,
    expert_cache_path,
    evaluate_result,
    freeze,
    macro_f1,
    move_data,
    safe_corr,
    train_module,
    train_or_load_expert,
)
from src.data import RELIABILITY_COMPONENTS, select_reliability_components, set_seed
from src.expert_models import GlobalExpert, LocalExpert
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    prepare_graph_data,
    primary_metric_for_dataset,
    select_mask,
    validation_fingerprint,
    write_validation_report,
)
from src.representation_control import (
    ALPHA_TYPES,
    COMPONENT_MISSING_MODES,
    CONTROL_MODES,
    GPSLikeNetwork,
    HiddenMixingNetwork,
    IterativeRelationNetwork,
    RELIABILITY_ENCODER_MODES,
    ResidualAlphaFusion,
)


FAMILIES = (
    "residual_alpha",
    "hidden_mixing_frozen",
    "hidden_mixing_finetune",
    "iterative_relation_frozen",
    "iterative_relation_finetune",
    "gps_like_frozen",
    "gps_like_finetune",
)
CAUSAL_CONTROL_MODES = {
    "fixed",
    "reliability_only",
    "combined",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=REAL_DATASETS, required=True)
    parser.add_argument("--family", choices=FAMILIES, required=True)
    parser.add_argument("--control-mode", choices=CONTROL_MODES, required=True)
    parser.add_argument("--result-name")
    parser.add_argument("--edge-protocol", choices=EDGE_PROTOCOLS, default="undirected")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/representation_control"),
    )
    parser.add_argument("--expert-cache-dir", type=Path)
    parser.add_argument("--backbone-cache-dir", type=Path)
    parser.add_argument(
        "--reuse-compatible-backbone-cache",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--compatible-backbone-cache-config", type=Path)
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument(
        "--normalize-features",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument("--rw-steps", type=int, default=4)
    parser.add_argument("--rw-samples", type=int, default=128)
    parser.add_argument("--rw-seed", type=int, default=0)
    parser.add_argument(
        "--reliability-components",
        nargs="+",
        choices=RELIABILITY_COMPONENTS,
        default=list(RELIABILITY_COMPONENTS),
    )
    parser.add_argument(
        "--reliability-encoder-mode",
        choices=RELIABILITY_ENCODER_MODES,
        default="raw_concat",
    )
    parser.add_argument("--reliability-component-dim", type=int, default=16)
    parser.add_argument(
        "--component-missing-mode",
        choices=COMPONENT_MISSING_MODES,
        default="zero_slot",
    )
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--expert-epochs", type=int, default=300)
    parser.add_argument("--control-epochs", type=int, default=200)
    parser.add_argument("--patience", type=int, default=60)
    parser.add_argument(
        "--fixed-alphas",
        nargs="+",
        type=float,
        default=[0.0, 0.25, 0.5, 0.75, 1.0],
    )
    parser.add_argument("--max-adjustment", type=float, default=0.1)
    parser.add_argument("--lambda-init", type=float, default=0.001)
    parser.add_argument("--relation-steps", type=int, default=1)
    parser.add_argument("--alpha-type", choices=ALPHA_TYPES, default="channel")
    parser.add_argument("--alpha-groups", type=int, default=4)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument(
        "--save-node-diagnostics",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--save-external-expert-logits",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--node-diagnostics-dir", type=Path)
    parser.add_argument(
        "--causal-interventions",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_args(args)
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    args.expert_cache_dir = (
        resolve(root, args.expert_cache_dir)
        if args.expert_cache_dir is not None
        else out_dir / "_expert_cache"
    )
    args.backbone_cache_dir = (
        resolve(root, args.backbone_cache_dir)
        if args.backbone_cache_dir is not None
        else out_dir / "_backbone_cache"
    )
    args.compatible_backbone_cache_config = (
        resolve(root, args.compatible_backbone_cache_config)
        if args.compatible_backbone_cache_config is not None
        else None
    )
    args.node_diagnostics_dir = (
        resolve(root, args.node_diagnostics_dir)
        if args.node_diagnostics_dir is not None
        else out_dir / "_node_diagnostics"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.save_node_diagnostics:
        args.node_diagnostics_dir.mkdir(parents=True, exist_ok=True)
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    device = torch.device(args.device)

    pyg_data, validation = load_and_validate_dataset(
        args.dataset,
        data_root,
        allow_download=not args.no_download,
    )
    write_validation_report(
        [validation],
        out_dir / f"{args.dataset}_validation.json",
    )
    args.data_fingerprint = validation_fingerprint(validation)
    args.preprocess_code_hash = code_hash(
        [root / "src" / "real_data.py", root / "src" / "data.py"]
    )
    cache_key = (
        f"{args.data_fingerprint}:relcode={args.preprocess_code_hash}:"
        f"protocol={args.edge_protocol}:norm={int(args.normalize_features)}:"
        f"steps={args.rw_steps}:samples={args.rw_samples}:seed={args.rw_seed}"
    )
    cache_path = (
        data_root
        / "_reliability_cache"
        / (
            f"{args.dataset}_{args.edge_protocol}_norm{int(args.normalize_features)}_"
            f"rw{args.rw_steps}_samples{args.rw_samples}_seed{args.rw_seed}.pt"
        )
    )
    data = prepare_graph_data(
        pyg_data,
        split=0,
        rw_steps=args.rw_steps,
        rw_samples=args.rw_samples,
        rw_seed=args.rw_seed,
        normalize_features=args.normalize_features,
        edge_protocol=args.edge_protocol,
        cache_path=cache_path,
        cache_key=cache_key,
        primary_metric=primary_metric_for_dataset(args.dataset),
    )
    data = select_reliability_components(data, args.reliability_components)
    num_splits = int(validation["actual"]["num_splits"])

    rows = []
    for run in range(args.runs):
        split, seed = run_assignment(run, num_splits)
        data.train_mask = select_mask(pyg_data.train_mask, split).clone()
        data.val_mask = select_mask(pyg_data.val_mask, split).clone()
        data.test_mask = select_mask(pyg_data.test_mask, split).clone()
        print(
            f"[{run + 1}/{args.runs}] dataset={args.dataset} "
            f"family={args.family} control={args.control_mode} "
            f"split={split} seed={seed}",
            flush=True,
        )
        rows.append(train_one(args, data, device, split, seed))

    result_name = args.result_name or f"{args.family}_{args.control_mode}"
    output_path = out_dir / f"{args.dataset}_{result_name}.csv"
    write_csv(output_path, rows)
    values = np.asarray([float(row["test_acc_at_best_val"]) for row in rows])
    primary_values = np.asarray(
        [float(row["test_primary_at_best_val"]) for row in rows]
    )
    print(
        f"{rows[0]['primary_metric']} mean={primary_values.mean():.4f} "
        f"std={primary_values.std():.4f}; "
        f"test_acc mean={values.mean():.4f}"
    )
    print(f"saved: {output_path}")


def validate_args(args) -> None:
    if args.runs < 1:
        raise ValueError("--runs must be positive")
    if any(not 0.0 <= alpha <= 1.0 for alpha in args.fixed_alphas):
        raise ValueError("--fixed-alphas values must be between 0 and 1")
    if len(set(args.fixed_alphas)) != len(args.fixed_alphas):
        raise ValueError("--fixed-alphas must not contain duplicates")
    if not 0.0 < args.max_adjustment <= 1.0:
        raise ValueError("--max-adjustment must be in (0, 1]")
    if not 0.0 < args.lambda_init < args.max_adjustment:
        raise ValueError("--lambda-init must be in (0, max-adjustment)")
    if args.relation_steps < 0:
        raise ValueError("--relation-steps must not be negative")
    if (
        args.family.startswith("iterative_relation_")
        and args.relation_steps < 1
    ):
        raise ValueError("--relation-steps must be positive")
    if getattr(args, "reliability_component_dim", 16) < 1:
        raise ValueError("--reliability-component-dim must be positive")
    alpha_type = getattr(args, "alpha_type", "channel")
    alpha_groups = getattr(args, "alpha_groups", 4)
    if alpha_groups < 1:
        raise ValueError("--alpha-groups must be positive")
    if alpha_type == "group" and args.hidden_dim % alpha_groups != 0:
        raise ValueError("--hidden-dim must be divisible by --alpha-groups")
    if (
        args.causal_interventions
        and not args.family.startswith("iterative_relation_")
    ):
        raise ValueError(
            "--causal-interventions requires an iterative_relation family"
        )
    if (
        args.causal_interventions
        and args.control_mode not in CAUSAL_CONTROL_MODES
    ):
        raise ValueError(
            "--causal-interventions supports only fixed, reliability_only, "
            "or combined controls"
        )
    if (
        args.reuse_compatible_backbone_cache
        and args.compatible_backbone_cache_config is None
    ):
        raise ValueError(
            "--reuse-compatible-backbone-cache requires "
            "--compatible-backbone-cache-config"
        )
    if args.save_external_expert_logits and not args.save_node_diagnostics:
        raise ValueError(
            "--save-external-expert-logits requires --save-node-diagnostics"
        )


def train_one(args, base_data, device, split: int, seed: int) -> dict[str, object]:
    data = move_data(copy.copy(base_data), device)
    reliability_input = control_reliability(
        data.reliability_gate,
        data.train_mask,
        args.control_mode,
        seed,
    )
    start = time.time()
    if args.family == "residual_alpha":
        result, baseline, model = train_residual_alpha(
            args,
            data,
            reliability_input,
            split,
            seed,
        )
    else:
        result, baseline, model = train_hidden_mixing(
            args,
            data,
            reliability_input,
            split,
            seed,
        )

    model.eval()
    with torch.no_grad():
        if args.family == "residual_alpha":
            logits = model(
                data.x,
                reliability_input,
                baseline["local_logits"],
                baseline["global_logits"],
            )
        else:
            logits = model(data.x, data.edge_index, reliability_input)
    diagnostics = model.diagnostic_stats()
    diagnostics.update(alpha_correlations(model, data, reliability_input))
    causal_metrics: dict[str, float] = {}
    causal_outputs: dict[str, object] = {}
    if args.causal_interventions:
        causal_metrics, causal_outputs = evaluate_causal_interventions(
            args=args,
            model=model,
            data=data,
            normal_logits=logits,
            reliability_input=reliability_input,
            seed=seed,
        )
    if args.save_external_expert_logits and (
        not isinstance(baseline.get("local_logits"), torch.Tensor)
        or not isinstance(baseline.get("global_logits"), torch.Tensor)
    ):
        local_logits, global_logits = load_or_train_external_expert_logits(
            args,
            data,
            split,
            seed,
        )
        baseline["local_logits"] = local_logits
        baseline["global_logits"] = global_logits
    result_name = args.result_name or f"{args.family}_{args.control_mode}"
    if args.save_node_diagnostics:
        save_node_diagnostics(
            args=args,
            data=data,
            model=model,
            logits=logits,
            reliability_input=reliability_input,
            baseline=baseline,
            result=result,
            diagnostics=diagnostics,
            result_name=result_name,
            split=split,
            seed=seed,
            causal_outputs=causal_outputs,
        )
    return {
        "dataset": args.dataset,
        "model": result_name,
        "family": args.family,
        "control_mode": args.control_mode,
        "edge_protocol": args.edge_protocol,
        "run": f"{split}:{seed}",
        "split": split,
        "seed": seed,
        "best_epoch": result["epoch"],
        "primary_metric": result["primary_metric"],
        "best_val_primary": result["val_score"],
        "test_primary_at_best_val": result["test_score"],
        "best_train_primary": result["train_score"],
        "best_train_acc": result["train_acc"],
        "best_val_acc": result["val_acc"],
        "test_acc_at_best_val": result["test_acc"],
        "best_train_roc_auc": result["train_roc_auc"],
        "best_val_roc_auc": result["val_roc_auc"],
        "test_roc_auc_at_best_val": result["test_roc_auc"],
        "test_macro_f1_at_best_val": result["test_macro_f1"],
        "backbone_training_mode": training_mode(args.family, args.control_mode),
        "base_alpha": baseline["alpha"],
        "baseline_val_acc": baseline["val_acc"],
        "baseline_test_acc": baseline["test_acc"],
        "baseline_train_acc": baseline["train_acc"],
        "baseline_val_primary": baseline["val_score"],
        "baseline_test_primary": baseline["test_score"],
        "baseline_train_primary": baseline["train_score"],
        "baseline_val_roc_auc": baseline["val_roc_auc"],
        "baseline_test_roc_auc": baseline["test_roc_auc"],
        "baseline_train_roc_auc": baseline["train_roc_auc"],
        "baseline_macro_f1": baseline["test_macro_f1"],
        "initial_max_abs_logit_delta": baseline["initial_max_abs_logit_delta"],
        "declared_trainable_parameters": sum(
            parameter.numel()
            for parameter in model.parameters()
            if parameter.requires_grad
        ),
        "active_controller_parameters": active_controller_parameters(
            model,
            args.control_mode,
        ),
        "backbone_trainable_parameters": backbone_trainable_parameters(model),
        "max_adjustment": args.max_adjustment,
        "lambda_init": args.lambda_init,
        "relation_steps": effective_relation_steps(
            args.family,
            args.relation_steps,
        ),
        "causal_interventions": bool(args.causal_interventions),
        "save_external_expert_logits": bool(
            args.save_external_expert_logits
        ),
        "reuse_compatible_backbone_cache": bool(
            args.reuse_compatible_backbone_cache
        ),
        "compatible_backbone_cache_config": (
            str(args.compatible_backbone_cache_config)
            if args.compatible_backbone_cache_config is not None
            else ""
        ),
        "reliability_components": ",".join(args.reliability_components),
        "reliability_encoder_mode": args.reliability_encoder_mode,
        "reliability_component_dim": args.reliability_component_dim,
        "component_missing_mode": args.component_missing_mode,
        "alpha_type": args.alpha_type,
        "alpha_groups": args.alpha_groups,
        "normalize_features": args.normalize_features,
        "rw_steps": args.rw_steps,
        "rw_samples": args.rw_samples,
        "rw_seed": args.rw_seed,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "expert_epochs": args.expert_epochs,
        "control_epochs": args.control_epochs,
        "patience": args.patience,
        "fixed_alphas": ",".join(str(value) for value in args.fixed_alphas),
        "data_fingerprint": args.data_fingerprint,
        "preprocess_code_hash": args.preprocess_code_hash,
        "elapsed_sec": time.time() - start,
        **diagnostics,
        **causal_metrics,
    }


def train_residual_alpha(args, data, reliability_input, split, seed):
    set_seed(seed)
    local = LocalExpert(
        data.x.size(1),
        args.hidden_dim,
        int(data.y.max().item()) + 1,
        args.num_layers,
        args.dropout,
    ).to(data.x.device)
    set_seed(seed + 100_000)
    global_expert = GlobalExpert(
        data.x.size(1),
        args.hidden_dim,
        int(data.y.max().item()) + 1,
        args.num_layers,
        args.num_heads,
        args.dropout,
    ).to(data.x.device)

    set_seed(seed)
    train_or_load_expert(
        expert_cache_path(args, split, seed, "local"),
        local,
        lambda: local(data.x, data.edge_index),
        data,
        args,
    )
    set_seed(seed + 100_000)
    train_or_load_expert(
        expert_cache_path(args, split, seed, "global"),
        global_expert,
        lambda: global_expert(data.x),
        data,
        args,
    )
    freeze(local)
    freeze(global_expert)
    with torch.no_grad():
        local_logits = local(data.x, data.edge_index)
        global_logits = global_expert(data.x)
    baseline = select_logit_alpha(
        args.fixed_alphas,
        local_logits,
        global_logits,
        data,
    )
    baseline["local_logits"] = local_logits
    baseline["global_logits"] = global_logits

    set_seed(seed + 200_000)
    model = ResidualAlphaFusion(
        feature_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        hidden_dim=args.hidden_dim,
        dropout=args.dropout,
        mode=args.control_mode,
        base_alpha=baseline["alpha"],
        max_adjustment=args.max_adjustment,
        lambda_init=args.lambda_init,
        reliability_encoder_mode=args.reliability_encoder_mode,
        reliability_components=args.reliability_components,
        reliability_component_dim=args.reliability_component_dim,
        component_missing_mode=args.component_missing_mode,
    ).to(data.x.device)
    with torch.no_grad():
        baseline_logits = (
            baseline["alpha"] * local_logits
            + (1.0 - baseline["alpha"]) * global_logits
        )
        initial_logits = model(
            data.x,
            reliability_input,
            local_logits,
            global_logits,
        )
        baseline["initial_max_abs_logit_delta"] = float(
            (initial_logits - baseline_logits).abs().max().cpu()
        )
    if args.control_mode == "fixed":
        result = dict(baseline)
        result["epoch"] = -1
    else:
        result = train_module(
            model,
            lambda: model(
                data.x,
                reliability_input,
                local_logits,
                global_logits,
            ),
            data,
            args.control_epochs,
            args.patience,
            args.lr,
            args.weight_decay,
        )
    return result, baseline, model


def load_or_train_external_expert_logits(args, data, split, seed):
    set_seed(seed)
    local = LocalExpert(
        data.x.size(1),
        args.hidden_dim,
        int(data.y.max().item()) + 1,
        args.num_layers,
        args.dropout,
    ).to(data.x.device)
    set_seed(seed + 100_000)
    global_expert = GlobalExpert(
        data.x.size(1),
        args.hidden_dim,
        int(data.y.max().item()) + 1,
        args.num_layers,
        args.num_heads,
        args.dropout,
    ).to(data.x.device)
    set_seed(seed)
    train_or_load_expert(
        expert_cache_path(args, split, seed, "local"),
        local,
        lambda: local(data.x, data.edge_index),
        data,
        args,
    )
    set_seed(seed + 100_000)
    train_or_load_expert(
        expert_cache_path(args, split, seed, "global"),
        global_expert,
        lambda: global_expert(data.x),
        data,
        args,
    )
    local.eval()
    global_expert.eval()
    with torch.no_grad():
        return (
            local(data.x, data.edge_index).detach(),
            global_expert(data.x).detach(),
        )


def train_hidden_mixing(args, data, reliability_input, split, seed):
    payload = load_or_train_hidden_baseline(args, data, split, seed)
    baseline = dict(payload["result"])
    baseline["alpha"] = float(payload["alpha"])

    set_seed(seed + 200_000)
    model = build_hidden_model(
        args,
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        out_dim=int(data.y.max().item()) + 1,
        mode=args.control_mode,
        base_alpha=baseline["alpha"],
    ).to(data.x.device)
    missing, unexpected = model.load_state_dict(payload["state_dict"], strict=False)
    expected_missing = {
        key
        for key in missing
        if ".controller." in key
    }
    if set(missing) != expected_missing or unexpected:
        raise RuntimeError(
            f"Unexpected baseline state mismatch: missing={missing}, "
            f"unexpected={unexpected}"
        )
    if is_frozen_family(args.family):
        freeze_hidden_backbone(model)
    reference = build_baseline_hidden_model(
        args,
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        out_dim=int(data.y.max().item()) + 1,
        mode="fixed",
        base_alpha=baseline["alpha"],
    ).to(data.x.device)
    reference.load_state_dict(payload["state_dict"])
    reference.eval()
    model.eval()
    with torch.no_grad():
        baseline_logits = reference(
            data.x,
            data.edge_index,
            data.reliability_gate,
        )
        initial_logits = model(data.x, data.edge_index, reliability_input)
        baseline["initial_max_abs_logit_delta"] = float(
            (initial_logits - baseline_logits).abs().max().cpu()
        )
    del reference
    if args.control_mode == "fixed" and is_frozen_family(args.family):
        result = dict(baseline)
        result["epoch"] = -1
    elif is_frozen_family(args.family):
        result = train_frozen_controller(
            model,
            lambda: model(data.x, data.edge_index, reliability_input),
            data,
            args.control_epochs,
            args.patience,
            args.lr,
            args.weight_decay,
        )
    else:
        result = train_module(
            model,
            lambda: model(data.x, data.edge_index, reliability_input),
            data,
            args.control_epochs,
            args.patience,
            args.lr,
            args.weight_decay,
        )
    return result, baseline, model


def build_hidden_model(args, in_dim, reliability_dim, out_dim, mode, base_alpha):
    if args.family.startswith("gps_like_"):
        return GPSLikeNetwork(
            in_dim=in_dim,
            reliability_dim=reliability_dim,
            hidden_dim=args.hidden_dim,
            out_dim=out_dim,
            num_layers=args.num_layers,
            num_heads=args.num_heads,
            dropout=args.dropout,
            mode=mode,
            base_alpha=base_alpha,
            max_adjustment=args.max_adjustment,
            lambda_init=args.lambda_init,
            reliability_encoder_mode=args.reliability_encoder_mode,
            reliability_components=args.reliability_components,
            reliability_component_dim=args.reliability_component_dim,
            component_missing_mode=args.component_missing_mode,
        )
    common = {
        "in_dim": in_dim,
        "reliability_dim": reliability_dim,
        "hidden_dim": args.hidden_dim,
        "out_dim": out_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "mode": mode,
        "base_alpha": base_alpha,
        "max_adjustment": args.max_adjustment,
        "reliability_encoder_mode": args.reliability_encoder_mode,
        "reliability_components": args.reliability_components,
        "reliability_component_dim": args.reliability_component_dim,
        "component_missing_mode": args.component_missing_mode,
    }
    if args.family.startswith("iterative_relation_"):
        return IterativeRelationNetwork(
            **common,
            relation_steps=args.relation_steps,
            alpha_type=args.alpha_type,
            alpha_groups=args.alpha_groups,
        )
    return HiddenMixingNetwork(
        **common,
        lambda_init=args.lambda_init,
    )


def build_baseline_hidden_model(
    args,
    in_dim,
    reliability_dim,
    out_dim,
    mode,
    base_alpha,
):
    if args.family.startswith("gps_like_"):
        return GPSLikeNetwork(
            in_dim=in_dim,
            reliability_dim=reliability_dim,
            hidden_dim=args.hidden_dim,
            out_dim=out_dim,
            num_layers=args.num_layers,
            num_heads=args.num_heads,
            dropout=args.dropout,
            mode=mode,
            base_alpha=base_alpha,
            max_adjustment=args.max_adjustment,
            lambda_init=args.lambda_init,
            reliability_encoder_mode=args.reliability_encoder_mode,
            reliability_components=args.reliability_components,
            reliability_component_dim=args.reliability_component_dim,
            component_missing_mode=args.component_missing_mode,
        )
    if args.family.startswith("iterative_relation_"):
        return IterativeRelationNetwork(
            in_dim=in_dim,
            reliability_dim=reliability_dim,
            hidden_dim=args.hidden_dim,
            out_dim=out_dim,
            num_layers=args.num_layers,
            num_heads=args.num_heads,
            dropout=args.dropout,
            mode=mode,
            base_alpha=base_alpha,
            max_adjustment=args.max_adjustment,
            relation_steps=args.relation_steps,
            reliability_encoder_mode=args.reliability_encoder_mode,
            reliability_components=args.reliability_components,
            reliability_component_dim=args.reliability_component_dim,
            component_missing_mode=args.component_missing_mode,
            alpha_type=args.alpha_type,
            alpha_groups=args.alpha_groups,
        )
    return HiddenMixingNetwork(
        in_dim=in_dim,
        reliability_dim=reliability_dim,
        hidden_dim=args.hidden_dim,
        out_dim=out_dim,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        dropout=args.dropout,
        mode=mode,
        base_alpha=base_alpha,
        max_adjustment=args.max_adjustment,
        lambda_init=args.lambda_init,
        reliability_encoder_mode=args.reliability_encoder_mode,
        reliability_components=args.reliability_components,
        reliability_component_dim=args.reliability_component_dim,
        component_missing_mode=args.component_missing_mode,
    )


def is_frozen_family(family: str) -> bool:
    return family.endswith("_frozen")


def effective_relation_steps(family: str, relation_steps: int) -> int:
    return relation_steps if family.startswith("iterative_relation_") else 0


def load_or_train_hidden_baseline(args, data, split, seed):
    path = hidden_cache_path(args, split, seed)
    if path is not None and path.exists():
        return torch.load(path, map_location=data.x.device, weights_only=False)
    if path is not None and args.reuse_compatible_backbone_cache:
        compatible = find_compatible_hidden_cache(args, path, split, seed)
        if compatible is not None:
            print(f"reuse compatible backbone cache: {compatible}", flush=True)
            return torch.load(
                compatible,
                map_location=data.x.device,
                weights_only=False,
            )

    candidates = []
    for alpha in args.fixed_alphas:
        set_seed(seed)
        model = build_baseline_hidden_model(
            args,
            in_dim=data.x.size(1),
            reliability_dim=data.reliability_gate.size(1),
            out_dim=int(data.y.max().item()) + 1,
            mode="fixed",
            base_alpha=alpha,
        ).to(data.x.device)
        result = train_module(
            model,
            lambda: model(data.x, data.edge_index, data.reliability_gate),
            data,
            args.expert_epochs,
            args.patience,
            args.lr,
            args.weight_decay,
        )
        candidates.append((alpha, result, copy.deepcopy(model.state_dict())))
    alpha, result, state_dict = max(
        candidates,
        key=lambda item: (
            item[1]["val_score"],
            -abs(item[0] - 0.5),
            -item[0],
        ),
    )
    payload = {
        "alpha": alpha,
        "result": result,
        "metadata": hidden_cache_metadata(args, split, seed),
        "state_dict": {
            key: value.detach().cpu()
            for key, value in state_dict.items()
        },
    }
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(payload, path)
    return payload


def find_compatible_hidden_cache(
    args,
    expected_path: Path,
    split: int,
    seed: int,
) -> Path | None:
    if not expected_path.parent.exists():
        return None
    matches = sorted(
        expected_path.parent.glob(f"hidden_split{split}_seed{seed}_*.pt")
    )
    if not matches:
        return None
    expected_metadata = hidden_cache_metadata(args, split, seed)
    legacy_payloads = []
    candidates = []
    rejected = []
    for path in matches:
        payload = torch.load(path, map_location="cpu", weights_only=False)
        try:
            alpha = float(payload["alpha"])
            val_score = float(payload["result"]["val_score"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(
                f"Invalid compatible backbone cache: {path}"
            ) from exc
        metadata = payload.get("metadata")
        if metadata is not None:
            try:
                validate_hidden_cache_metadata(
                    metadata,
                    expected_metadata,
                    path,
                )
            except RuntimeError as exc:
                rejected.append(f"{path.name}: {exc}")
                del payload
                continue
        else:
            legacy_payloads.append((path, payload, alpha, val_score))
            continue
        candidates.append(
            (val_score, -abs(alpha - 0.5), -alpha, str(path), path)
        )
        del payload
    if legacy_payloads:
        try:
            fixed_rows = compatible_legacy_fixed_rows(args, expected_metadata)
        except RuntimeError as exc:
            rejected.append(str(exc))
            fixed_rows = []
        accepted_legacy = []
        for path, payload, alpha, val_score in legacy_payloads:
            if legacy_payload_matches_fixed_row(
                payload,
                alpha,
                val_score,
                fixed_rows,
            ):
                accepted_legacy.append((path, payload, alpha, val_score))
            else:
                rejected.append(
                    f"{path.name}: alpha/result metrics do not match the "
                    "validated fixed-result CSV"
                )
                del payload
        if len(accepted_legacy) > 1 and not equivalent_legacy_payloads(
            [payload for _, payload, _, _ in accepted_legacy]
        ):
            paths = [str(path) for path, _, _, _ in accepted_legacy]
            raise RuntimeError(
                "Multiple legacy backbone caches match fixed-result metadata "
                f"but contain different state_dict values: {paths}"
            )
        for path, payload, alpha, val_score in accepted_legacy:
            candidates.append(
                (val_score, -abs(alpha - 0.5), -alpha, str(path), path)
            )
            del payload
    if not candidates:
        detail = "\n".join(f"- {reason}" for reason in rejected)
        raise RuntimeError(
            "No compatible backbone cache found among existing candidates"
            + (f":\n{detail}" if detail else "")
        )
    return max(candidates)[-1]


def validate_hidden_cache_metadata(
    actual: dict[str, object],
    expected: dict[str, object],
    path: Path,
) -> None:
    compatibility_keys = set(expected) - {"source"}
    mismatches = {
        key: (actual.get(key), expected[key])
        for key in compatibility_keys
        if actual.get(key) != expected[key]
    }
    if mismatches:
        raise RuntimeError(
            f"Incompatible backbone cache metadata in {path}: {mismatches}"
        )


def compatible_legacy_fixed_rows(
    args,
    expected: dict[str, object],
) -> list[dict[str, str]]:
    config_path = args.compatible_backbone_cache_config
    if config_path is None or not config_path.exists():
        raise RuntimeError(
            "Legacy backbone cache reuse requires an existing "
            "--compatible-backbone-cache-config"
        )
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config_checks = {
        "edge_protocol": expected["edge_protocol"],
        "normalize_features": expected["normalize_features"],
        "hidden_dim": expected["hidden_dim"],
        "num_layers": expected["num_layers"],
        "num_heads": expected["num_heads"],
        "dropout": expected["dropout"],
        "lr": expected["lr"],
        "weight_decay": expected["weight_decay"],
        "expert_epochs": expected["expert_epochs"],
        "patience": expected["patience"],
        "fixed_alphas": expected["fixed_alphas"],
    }
    mismatches = {
        key: (config.get(key), value)
        for key, value in config_checks.items()
        if config.get(key) != value
    }
    fingerprints = config.get("data_fingerprints", {})
    if fingerprints.get(args.dataset) != expected["data_fingerprint"]:
        mismatches["data_fingerprint"] = (
            fingerprints.get(args.dataset),
            expected["data_fingerprint"],
        )
    configured_families = {
        normalize_baseline_family(family)
        for family in config.get("families", [])
    }
    if expected["baseline_family"] not in configured_families:
        mismatches["baseline_family"] = (
            sorted(configured_families),
            expected["baseline_family"],
        )
    if mismatches:
        raise RuntimeError(
            f"Incompatible legacy backbone suite config {config_path}: "
            f"{mismatches}"
        )
    return compatible_legacy_fixed_rows_from_csv(
        args,
        expected,
        config_path.parent,
    )


def compatible_legacy_fixed_rows_from_csv(
    args,
    expected: dict[str, object],
    output_dir: Path,
) -> list[dict[str, str]]:
    candidates = sorted(output_dir.glob(f"{args.dataset}_*_fixed.csv"))
    compatible_rows = []
    rejected_rows = []
    for path in candidates:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if (
                normalize_baseline_family(row.get("family", ""))
                != expected["baseline_family"]
                or int(row["split"]) != expected["split"]
                or int(row["seed"]) != expected["seed"]
            ):
                continue
            checks = {
                "data_fingerprint": expected["data_fingerprint"],
                "preprocess_code_hash": expected["preprocess_code_hash"],
                "edge_protocol": str(expected["edge_protocol"]),
                "normalize_features": str(expected["normalize_features"]),
                "hidden_dim": str(expected["hidden_dim"]),
                "num_layers": str(expected["num_layers"]),
                "num_heads": str(expected["num_heads"]),
                "dropout": str(expected["dropout"]),
                "lr": str(expected["lr"]),
                "weight_decay": str(expected["weight_decay"]),
                "expert_epochs": str(expected["expert_epochs"]),
                "patience": str(expected["patience"]),
                "fixed_alphas": ",".join(
                    str(value) for value in expected["fixed_alphas"]
                ),
            }
            mismatches = {
                key: (row.get(key), value)
                for key, value in checks.items()
                if row.get(key) != value
            }
            if mismatches:
                rejected_rows.append(f"{path.name}: {mismatches}")
                continue
            compatible_rows.append(row)
    if compatible_rows:
        return compatible_rows
    detail = "\n".join(f"- {reason}" for reason in rejected_rows)
    raise RuntimeError(
        "Could not find matching fixed-result metadata beside legacy "
        f"backbone cache config: {output_dir}"
        + (f"\n{detail}" if detail else "")
    )


def legacy_payload_matches_fixed_row(
    payload: dict[str, object],
    alpha: float,
    val_score: float,
    fixed_rows: list[dict[str, str]],
) -> bool:
    result = payload.get("result", {})
    test_score = float(result.get("test_score", math.nan))
    for row in fixed_rows:
        if not close_float(alpha, row.get("base_alpha")):
            continue
        if not close_float(val_score, row.get("best_val_primary")):
            continue
        if math.isfinite(test_score) and not close_float(
            test_score,
            row.get("test_primary_at_best_val"),
        ):
            continue
        return True
    return False


def close_float(left: float, right: object, tolerance: float = 1e-7) -> bool:
    try:
        right_value = float(right)
    except (TypeError, ValueError):
        return False
    return math.isclose(left, right_value, rel_tol=0.0, abs_tol=tolerance)


def equivalent_legacy_payloads(payloads: list[dict[str, object]]) -> bool:
    if len(payloads) < 2:
        return True
    reference = payloads[0].get("state_dict", {})
    for payload in payloads[1:]:
        candidate = payload.get("state_dict", {})
        if reference.keys() != candidate.keys():
            return False
        if any(
            not torch.equal(reference[key], candidate[key])
            for key in reference
        ):
            return False
    return True


def select_logit_alpha(alphas, local_logits, global_logits, data):
    candidates = []
    for alpha in alphas:
        logits = alpha * local_logits + (1.0 - alpha) * global_logits
        result = evaluate_result(logits, data, epoch=-1)
        result["alpha"] = float(alpha)
        candidates.append(result)
    return max(
        candidates,
        key=lambda result: (
            result["val_score"],
            -abs(result["alpha"] - 0.5),
            -result["alpha"],
        ),
    )


def control_reliability(reliability, train_mask, mode: str, seed: int):
    if mode in {"shuffled_reliability", "combined_shuffled"}:
        generator = torch.Generator(device="cpu")
        generator.manual_seed(seed + 300_000)
        permutation = torch.randperm(
            reliability.size(0),
            generator=generator,
            device="cpu",
        ).to(reliability.device)
        return reliability[permutation]
    if mode in {"constant_reliability", "combined_constant"}:
        train_mean = reliability[train_mask].mean(dim=0, keepdim=True)
        return train_mean.expand_as(reliability)
    if mode in {"feature_only", "zero_reliability"}:
        return torch.zeros_like(reliability)
    return reliability


def evaluate_causal_interventions(
    args,
    model,
    data,
    normal_logits,
    reliability_input,
    seed: int,
) -> tuple[dict[str, float], dict[str, object]]:
    if not isinstance(model, IterativeRelationNetwork):
        raise ValueError(
            "--causal-interventions requires an iterative_relation family"
        )

    normal_result = evaluate_result(normal_logits, data, epoch=-1)
    interventions: dict[str, tuple[torch.Tensor, dict[str, float | int]]] = {}

    def evaluate(
        name: str,
        reliability: torch.Tensor,
        scales: list[float],
    ) -> None:
        model.set_relation_scales(scales)
        with torch.no_grad():
            intervention_logits = model(
                data.x,
                data.edge_index,
                reliability,
            )
        interventions[name] = (
            intervention_logits.detach(),
            evaluate_result(intervention_logits, data, epoch=-1),
        )

    num_layers = len(model.layers)
    evaluate("zero_all", reliability_input, [0.0] * num_layers)
    for layer_index in range(num_layers):
        scales = [1.0] * num_layers
        scales[layer_index] = 0.0
        evaluate(
            f"zero_layer_{layer_index}",
            reliability_input,
            scales,
        )

    raw_reliability = data.reliability_gate
    shuffled = shuffled_reliability(
        raw_reliability,
        seed=seed + 900_000,
    )
    train_mean = raw_reliability[data.train_mask].mean(dim=0, keepdim=True)
    constant = train_mean.expand_as(raw_reliability)
    evaluate("shuffled_reliability", shuffled, [1.0] * num_layers)
    evaluate("constant_reliability", constant, [1.0] * num_layers)

    model.reset_relation_scales()
    with torch.no_grad():
        restored_logits = model(
            data.x,
            data.edge_index,
            reliability_input,
        )

    metrics = {
        "causal_normal_test_primary": float(normal_result["test_score"]),
        "causal_normal_test_acc": float(normal_result["test_acc"]),
        "causal_restore_max_abs_logit_delta": float(
            (restored_logits - normal_logits).abs().max().cpu()
        ),
    }
    outputs = {
        "normal": causal_node_output(normal_logits, data.y),
    }
    for name, (intervention_logits, intervention_result) in interventions.items():
        prefix = f"causal_{name}"
        comparison = compare_intervention_predictions(
            normal_logits,
            intervention_logits,
            data.y,
            data.test_mask,
        )
        metrics.update(
            {
                f"{prefix}_test_primary": float(
                    intervention_result["test_score"]
                ),
                f"{prefix}_test_acc": float(
                    intervention_result["test_acc"]
                ),
                f"{prefix}_primary_drop": float(
                    normal_result["test_score"]
                    - intervention_result["test_score"]
                ),
                f"{prefix}_acc_drop": float(
                    normal_result["test_acc"]
                    - intervention_result["test_acc"]
                ),
                **{
                    f"{prefix}_{key}": value
                    for key, value in comparison.items()
                },
            }
        )
        outputs[name] = causal_node_output(intervention_logits, data.y)
    return metrics, outputs


def shuffled_reliability(
    reliability: torch.Tensor,
    seed: int,
) -> torch.Tensor:
    generator = torch.Generator(device="cpu")
    generator.manual_seed(seed)
    permutation = torch.randperm(
        reliability.size(0),
        generator=generator,
        device="cpu",
    ).to(reliability.device)
    return reliability[permutation]


def compare_intervention_predictions(
    normal_logits: torch.Tensor,
    intervention_logits: torch.Tensor,
    targets: torch.Tensor,
    mask: torch.Tensor,
) -> dict[str, float]:
    normal_prediction = normal_logits.argmax(dim=-1)
    intervention_prediction = intervention_logits.argmax(dim=-1)
    normal_correct = normal_prediction.eq(targets)
    intervention_correct = intervention_prediction.eq(targets)
    return {
        "prediction_change_rate": float(
            normal_prediction[mask]
            .ne(intervention_prediction[mask])
            .float()
            .mean()
        ),
        "normal_only_correct_rate": float(
            (normal_correct[mask] & ~intervention_correct[mask]).float().mean()
        ),
        "intervention_only_correct_rate": float(
            (~normal_correct[mask] & intervention_correct[mask]).float().mean()
        ),
    }


def causal_node_output(
    logits: torch.Tensor,
    targets: torch.Tensor,
) -> dict[str, torch.Tensor]:
    prediction = logits.argmax(dim=-1)
    return {
        "prediction": prediction,
        "correct": prediction.eq(targets),
        "margin": classification_margin(logits, targets),
    }


def classification_margin(
    logits: torch.Tensor,
    targets: torch.Tensor,
) -> torch.Tensor:
    true_logits = logits.gather(1, targets[:, None]).squeeze(1)
    other_logits = logits.clone()
    other_logits.scatter_(1, targets[:, None], float("-inf"))
    return true_logits - other_logits.max(dim=1).values


def alpha_correlations(model, data, reliability_input):
    alpha = node_alpha(model)
    output = {
        "alpha_corr_raw_degree": math.nan,
        "alpha_corr_raw_local_similarity": math.nan,
        "alpha_corr_raw_neighbor_variance": math.nan,
        "alpha_corr_raw_rwse": math.nan,
        "alpha_corr_control_input_mean": math.nan,
    }
    if alpha is None or not hasattr(data, "reliability_gate_raw"):
        return output
    values = alpha.view(-1).cpu().numpy()
    raw = data.reliability_gate_raw.cpu()
    if raw.size(1) > 0:
        output["alpha_corr_raw_degree"] = safe_corr(
            values,
            raw[:, 0].numpy(),
        )
    if hasattr(data, "local_similarity"):
        output["alpha_corr_raw_local_similarity"] = safe_corr(
            values,
            data.local_similarity.cpu().numpy(),
        )
    if raw.size(1) > 2:
        output["alpha_corr_raw_neighbor_variance"] = safe_corr(
            values,
            raw[:, 2].numpy(),
        )
    if raw.size(1) > 3:
        output["alpha_corr_raw_rwse"] = safe_corr(
            values,
            raw[:, 3:].mean(dim=1).numpy(),
        )
    if reliability_input.size(1) > 0:
        output["alpha_corr_control_input_mean"] = safe_corr(
            values,
            reliability_input.detach().cpu().mean(dim=1).numpy(),
        )
    return output


def save_node_diagnostics(
    args,
    data,
    model,
    logits,
    reliability_input,
    baseline,
    result,
    diagnostics,
    result_name: str,
    split: int,
    seed: int,
    causal_outputs: dict[str, object] | None = None,
) -> None:
    output_dir = args.node_diagnostics_dir / args.dataset / result_name
    output_dir.mkdir(parents=True, exist_ok=True)
    local_expert_path = expert_cache_path(args, split, seed, "local")
    global_expert_path = expert_cache_path(args, split, seed, "global")
    backbone_path = hidden_cache_path(args, split, seed)
    payload = {
        "meta": {
            "dataset": args.dataset,
            "family": args.family,
            "control_mode": args.control_mode,
            "result_name": result_name,
            "edge_protocol": args.edge_protocol,
            "split": split,
            "seed": seed,
            "run": f"{split}:{seed}",
            "base_alpha": float(baseline["alpha"]),
            "best_epoch": int(result["epoch"]),
            "primary_metric": result["primary_metric"],
            "best_val_primary": float(result["val_score"]),
            "test_primary_at_best_val": float(result["test_score"]),
            "best_train_primary": float(result["train_score"]),
            "best_train_acc": float(result["train_acc"]),
            "best_val_acc": float(result["val_acc"]),
            "test_acc_at_best_val": float(result["test_acc"]),
            "backbone_training_mode": training_mode(
                args.family,
                args.control_mode,
            ),
            "relation_steps": effective_relation_steps(
                args.family,
                args.relation_steps,
            ),
            "reliability_components": list(args.reliability_components),
            "reliability_encoder_mode": args.reliability_encoder_mode,
            "reliability_component_dim": args.reliability_component_dim,
            "component_missing_mode": args.component_missing_mode,
            "alpha_type": args.alpha_type,
            "alpha_groups": args.alpha_groups,
            "hidden_dim": args.hidden_dim,
            "num_layers": args.num_layers,
            "num_heads": args.num_heads,
            "dropout": args.dropout,
            "lr": args.lr,
            "weight_decay": args.weight_decay,
            "expert_epochs": args.expert_epochs,
            "control_epochs": args.control_epochs,
            "patience": args.patience,
            "fixed_alphas": list(args.fixed_alphas),
            "max_adjustment": args.max_adjustment,
            "lambda_init": args.lambda_init,
            "causal_interventions": bool(args.causal_interventions),
            "save_external_expert_logits": bool(
                args.save_external_expert_logits
            ),
            "reuse_compatible_backbone_cache": bool(
                args.reuse_compatible_backbone_cache
            ),
            "compatible_backbone_cache_config": (
                str(args.compatible_backbone_cache_config)
                if args.compatible_backbone_cache_config is not None
                else None
            ),
            "normalize_features": bool(args.normalize_features),
            "rw_steps": args.rw_steps,
            "rw_samples": args.rw_samples,
            "rw_seed": args.rw_seed,
            "data_fingerprint": args.data_fingerprint,
            "preprocess_code_hash": args.preprocess_code_hash,
            "expert_cache_dir": (
                str(args.expert_cache_dir)
                if args.expert_cache_dir is not None
                else None
            ),
            "backbone_cache_dir": (
                str(args.backbone_cache_dir)
                if args.backbone_cache_dir is not None
                else None
            ),
            "local_expert_cache_path": (
                str(local_expert_path)
                if local_expert_path is not None
                else None
            ),
            "global_expert_cache_path": (
                str(global_expert_path)
                if global_expert_path is not None
                else None
            ),
            "backbone_cache_path": (
                str(backbone_path)
                if backbone_path is not None
                else None
            ),
            "external_expert_logits_available": bool(
                isinstance(baseline.get("local_logits"), torch.Tensor)
                and isinstance(baseline.get("global_logits"), torch.Tensor)
            ),
        },
        "diagnostics": diagnostics,
        "targets": detach_to_cpu(data.y),
        "masks": {
            "train": detach_to_cpu(data.train_mask),
            "val": detach_to_cpu(data.val_mask),
            "test": detach_to_cpu(data.test_mask),
        },
        "inputs": {
            "reliability_input": detach_to_cpu(reliability_input),
            "reliability_gate": detach_to_cpu(data.reliability_gate),
            "reliability_gate_raw": detach_to_cpu(
                getattr(data, "reliability_gate_raw", None)
            ),
            "local_similarity": detach_to_cpu(
                getattr(data, "local_similarity", None)
            ),
        },
        "outputs": {
            "logits": detach_to_cpu(logits),
            "node_alpha": detach_to_cpu(node_alpha(model)),
            "causal_interventions": detach_to_cpu(causal_outputs or {}),
        },
        "external_experts": {
            "local_logits": detach_to_cpu(baseline.get("local_logits")),
            "global_logits": detach_to_cpu(baseline.get("global_logits")),
            "local_cache_path": (
                str(local_expert_path)
                if local_expert_path is not None
                else None
            ),
            "global_cache_path": (
                str(global_expert_path)
                if global_expert_path is not None
                else None
            ),
        },
        "model_state": collect_model_node_state(model),
    }
    output_path = output_dir / f"split{split}_seed{seed}.pt"
    torch.save(payload, output_path)


def detach_to_cpu(value):
    if value is None:
        return None
    if isinstance(value, torch.Tensor):
        return value.detach().cpu()
    if isinstance(value, dict):
        return {key: detach_to_cpu(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(detach_to_cpu(item) for item in value)
    return value


def collect_model_node_state(model) -> dict[str, object]:
    state = {
        "node_alpha": detach_to_cpu(node_alpha(model)),
    }
    if isinstance(model, ResidualAlphaFusion):
        state.update(
            {
                "latest_alpha": detach_to_cpu(model.latest_alpha),
                "latest_proposal": detach_to_cpu(model.latest_proposal),
                "latest_adjustment": detach_to_cpu(model.latest_adjustment),
            }
        )
        return state
    if not hasattr(model, "layers"):
        return state
    layer_attrs = (
        "latest_alpha",
        "latest_alpha_raw",
        "latest_proposal",
        "latest_adjustment",
        "latest_relation",
        "latest_state",
        "latest_update_gate",
        "latest_base_mixed",
        "latest_local_h",
        "latest_global_h",
        "latest_mixed",
        "latest_local_delta",
        "latest_global_delta",
    )
    state["layers"] = {
        attr: stack_layer_attr(model.layers, attr)
        for attr in layer_attrs
    }
    return state


def stack_layer_attr(layers, attr: str):
    tensors = [
        getattr(layer, attr)
        for layer in layers
        if getattr(layer, attr, None) is not None
    ]
    if not tensors:
        return None
    return detach_to_cpu(torch.stack(tensors, dim=0))


def node_alpha(model):
    if isinstance(model, ResidualAlphaFusion):
        return model.latest_alpha
    alphas = [
        layer.latest_alpha
        for layer in model.layers
        if layer.latest_alpha is not None
    ]
    if not alphas:
        return None
    alpha = torch.stack(alphas).mean(dim=0)
    if alpha.ndim == 2 and alpha.size(1) > 1:
        alpha = alpha.mean(dim=1, keepdim=True)
    return alpha


def freeze_hidden_backbone(model) -> None:
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    for layer in model.layers:
        if layer.controller is None:
            continue
        for parameter in layer.controller.parameters():
            parameter.requires_grad_(True)


def train_frozen_controller(
    model,
    forward,
    data,
    epochs,
    patience,
    lr,
    weight_decay,
):
    parameters = [
        parameter
        for parameter in model.parameters()
        if parameter.requires_grad
    ]
    if not parameters:
        raise ValueError("Frozen-controller training requires controller parameters")
    optimizer = torch.optim.AdamW(
        parameters,
        lr=lr,
        weight_decay=weight_decay,
    )
    model.eval()
    with torch.no_grad():
        best = evaluate_result(forward(), data, epoch=-1)
    best_state = copy.deepcopy(model.state_dict())
    stale = 0
    for epoch in range(epochs):
        model.eval()
        for layer in model.layers:
            if layer.controller is not None:
                layer.controller.train()
        optimizer.zero_grad()
        logits = forward()
        loss = torch.nn.functional.cross_entropy(
            logits[data.train_mask],
            data.y[data.train_mask],
        )
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            result = evaluate_result(forward(), data, epoch)
        if result["val_score"] > best["val_score"]:
            best = result
            best_state = copy.deepcopy(model.state_dict())
            stale = 0
        else:
            stale += 1
        if stale >= patience:
            break
    model.load_state_dict(best_state)
    return best


def active_controller_parameters(model, control_mode: str) -> int:
    if control_mode == "fixed":
        return 0
    total = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad or "controller." not in name:
            continue
        if control_mode == "feature_only" and "reliability_encoder." in name:
            continue
        if control_mode in {
            "reliability_only",
            "shuffled_reliability",
            "constant_reliability",
            "zero_reliability",
        } and "feature_encoder." in name:
            continue
        total += parameter.numel()
    return total


def backbone_trainable_parameters(model) -> int:
    return sum(
        parameter.numel()
        for name, parameter in model.named_parameters()
        if parameter.requires_grad and "controller." not in name
    )


def hidden_cache_path(args, split: int, seed: int) -> Path | None:
    if args.backbone_cache_dir is None:
        return None
    config = hidden_cache_metadata(args, split, seed)
    suffix = hashlib.sha256(
        json.dumps(config, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return (
        args.backbone_cache_dir
        / args.dataset
        / args.edge_protocol
        / f"hidden_split{split}_seed{seed}_{suffix}.pt"
    )


def hidden_cache_metadata(args, split: int, seed: int) -> dict[str, object]:
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for path in (
        root / "src" / "representation_control.py",
        root / "src" / "models.py",
        root / "src" / "real_data.py",
        Path(__file__),
    ):
        digest.update(path.read_bytes())
    return {
        "source": digest.hexdigest(),
        "data_fingerprint": args.data_fingerprint,
        "preprocess_code_hash": args.preprocess_code_hash,
        "dataset": args.dataset,
        "baseline_family": normalize_baseline_family(args.family),
        "edge_protocol": args.edge_protocol,
        "normalize_features": args.normalize_features,
        "split": split,
        "seed": seed,
        "fixed_alphas": args.fixed_alphas,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "expert_epochs": args.expert_epochs,
        "patience": args.patience,
    }


def normalize_baseline_family(family: str) -> str:
    return family.replace("_frozen", "").replace("_finetune", "")


def training_mode(family: str, control_mode: str) -> str:
    if family == "residual_alpha":
        return "logits_only"
    if family.endswith("_frozen"):
        return "frozen" if control_mode != "fixed" else "fixed_frozen"
    if family.endswith("_finetune"):
        return "finetuned" if control_mode != "fixed" else "fixed_finetuned"
    return "unknown"


def run_assignment(run: int, num_splits: int) -> tuple[int, int]:
    return (0, run) if num_splits == 1 else (run % num_splits, run // num_splits)


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        if not rows:
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
