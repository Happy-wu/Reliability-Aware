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
import torch.nn.functional as F

from run_expert_fusion import (
    code_hash,
    expert_cache_path,
    freeze,
    move_data,
    resolve,
    run_assignment,
    train_module,
    train_or_load_expert,
)
from src.data import RELIABILITY_COMPONENTS, select_reliability_components, set_seed
from src.expert_models import build_expert_model
from src.preference_routing import (
    ROUTERS,
    PreferenceRouter,
    constant_preference_metrics,
    constant_routed_node_accuracy,
    empty_preference_metrics,
    interpolated_node_accuracy,
    majority_preference_choice,
    oracle_union_accuracy,
    preference_label_counts,
    preference_metrics,
    preference_targets,
    routed_node_accuracy,
    routing_switch_rate,
    select_fixed_alpha,
    select_preference_threshold,
    select_utility_threshold,
)
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    prepare_graph_data,
    select_mask,
    validation_fingerprint,
    write_validation_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Diagnose whether reliability predicts local/global expert preference."
    )
    parser.add_argument("--dataset", choices=REAL_DATASETS, required=True)
    parser.add_argument("--routers", nargs="+", choices=ROUTERS, default=list(ROUTERS))
    parser.add_argument("--edge-protocol", choices=EDGE_PROTOCOLS, default="undirected")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--oof-folds", type=int, default=5)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/preference_routing"))
    parser.add_argument("--expert-cache-dir", type=Path)
    parser.add_argument("--preference-cache-dir", type=Path)
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
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--expert-epochs", type=int, default=500)
    parser.add_argument("--router-epochs", type=int, default=300)
    parser.add_argument("--patience", type=int, default=100)
    parser.add_argument(
        "--fixed-alphas",
        nargs="+",
        type=float,
        default=[0.0, 0.25, 0.5, 0.75, 1.0],
    )
    parser.add_argument("--utility-epsilon-nodes", type=int, default=1)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.oof_folds < 2:
        raise ValueError("--oof-folds must be at least 2")
    if any(not 0.0 <= alpha <= 1.0 for alpha in args.fixed_alphas):
        raise ValueError("--fixed-alphas values must be between 0 and 1")
    if args.utility_epsilon_nodes < 0:
        raise ValueError("--utility-epsilon-nodes must be non-negative")
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    args.expert_cache_dir = resolve(
        root,
        args.expert_cache_dir or out_dir / "_expert_cache",
    )
    args.preference_cache_dir = resolve(
        root,
        args.preference_cache_dir or out_dir / "_preference_cache",
    )
    out_dir.mkdir(parents=True, exist_ok=True)
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
    reliability_cache = (
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
        cache_path=reliability_cache,
        cache_key=cache_key,
    )
    data = select_reliability_components(data, args.reliability_components)

    rows: list[dict[str, object]] = []
    num_splits = int(validation["actual"]["num_splits"])
    for run in range(args.runs):
        split, seed = run_assignment(run, num_splits)
        data.train_mask = select_mask(pyg_data.train_mask, split).clone()
        data.val_mask = select_mask(pyg_data.val_mask, split).clone()
        data.test_mask = select_mask(pyg_data.test_mask, split).clone()
        print(
            f"[{run + 1}/{args.runs}] dataset={args.dataset} "
            f"protocol={args.edge_protocol} split={split} seed={seed}",
            flush=True,
        )
        rows.extend(run_one(args, data, device, split, seed))

    path = out_dir / f"{args.dataset}_preference_routing.csv"
    write_csv(path, rows)
    for router in args.routers:
        selected = [row for row in rows if row["router"] == router]
        auc = finite_mean(selected, "test_preference_auc")
        balanced = finite_mean(selected, "test_balanced_accuracy")
        routing = finite_mean(selected, "test_routing_accuracy")
        print(
            f"{router}: AUC={auc:.4f} balanced_acc={balanced:.4f} "
            f"routing_acc={routing:.4f}"
        )
    print(f"saved: {path}")


def run_one(args, base_data, device, split: int, seed: int) -> list[dict[str, object]]:
    start = time.time()
    data = move_data(copy.copy(base_data), device)
    set_seed(seed)
    model = build_expert_model(
        name="ordinary_gate",
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        hidden_dim=args.hidden_dim,
        out_dim=int(data.y.max().item()) + 1,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        dropout=args.dropout,
        fixed_alpha=0.5,
    ).to(device)

    train_or_load_expert(
        expert_cache_path(args, split, seed, "local"),
        model.local_expert,
        lambda: model.local_expert(data.x, data.edge_index),
        data,
        args,
    )
    set_seed(seed + 100_000)
    train_or_load_expert(
        expert_cache_path(args, split, seed, "global"),
        model.global_expert,
        lambda: model.global_expert(data.x),
        data,
        args,
    )
    freeze(model.local_expert)
    freeze(model.global_expert)
    model.eval()
    with torch.no_grad():
        full_local_logits = model.local_expert(data.x, data.edge_index)
        full_global_logits = model.global_expert(data.x)

    train_targets, oof_stats = load_or_build_oof_targets(
        args,
        data,
        split,
        seed,
    )
    val_targets = preference_targets(
        full_local_logits,
        full_global_logits,
        data.y,
        data.val_mask,
    )
    test_targets = preference_targets(
        full_local_logits,
        full_global_logits,
        data.y,
        data.test_mask,
    )
    majority_choice = majority_preference_choice(
        val_targets,
        data.val_mask,
    )
    majority_test_metrics = constant_preference_metrics(
        majority_choice,
        test_targets,
        data.test_mask,
    )
    majority_test_routed_accuracy = constant_routed_node_accuracy(
        majority_choice,
        full_local_logits,
        full_global_logits,
        data.y,
        data.test_mask,
    )
    local_val_accuracy = node_accuracy(
        full_local_logits,
        data.y,
        data.val_mask,
    )
    global_val_accuracy = node_accuracy(
        full_global_logits,
        data.y,
        data.val_mask,
    )
    best_expert_choice = int(local_val_accuracy >= global_val_accuracy)
    best_expert_test_accuracy = constant_routed_node_accuracy(
        best_expert_choice,
        full_local_logits,
        full_global_logits,
        data.y,
        data.test_mask,
    )
    fixed_alpha_result = select_fixed_alpha(
        args.fixed_alphas,
        full_local_logits,
        full_global_logits,
        data.y,
        data.val_mask,
    )
    fixed_alpha_test_accuracy = interpolated_node_accuracy(
        fixed_alpha_result["alpha"],
        full_local_logits,
        full_global_logits,
        data.y,
        data.test_mask,
    )
    test_oracle_union_accuracy = oracle_union_accuracy(
        full_local_logits,
        full_global_logits,
        data.y,
        data.test_mask,
    )

    rows = []
    for index, router_name in enumerate(args.routers):
        set_seed(seed + 300_000 + index)
        router = PreferenceRouter(
            feature_dim=data.x.size(1),
            reliability_dim=data.reliability_gate.size(1),
            hidden_dim=args.hidden_dim,
            dropout=args.dropout,
            mode=router_name,
        ).to(device)
        result = train_router(
            router,
            data,
            train_targets,
            val_targets,
            full_local_logits,
            full_global_logits,
            args,
        )
        if result["status"].startswith("ok"):
            router.eval()
            with torch.no_grad():
                router_logits = router(data.x, data.reliability_gate)
            utility_result = select_utility_threshold(
                router_logits,
                full_local_logits,
                full_global_logits,
                data.y,
                data.val_mask,
                epsilon_nodes=args.utility_epsilon_nodes,
            )
            utility_threshold = float(utility_result["threshold"])
            preference_threshold = float(result["decision_threshold"])
            if math.isfinite(preference_threshold):
                train_metrics = preference_metrics(
                    router_logits,
                    train_targets,
                    data.train_mask,
                    preference_threshold,
                )
                val_metrics = preference_metrics(
                    router_logits,
                    val_targets,
                    data.val_mask,
                    preference_threshold,
                )
                test_metrics = preference_metrics(
                    router_logits,
                    test_targets,
                    data.test_mask,
                    preference_threshold,
                )
                preference_test_routed_accuracy = routed_node_accuracy(
                    router_logits,
                    full_local_logits,
                    full_global_logits,
                    data.y,
                    data.test_mask,
                    preference_threshold,
                )
            else:
                train_metrics = unavailable_metrics(
                    train_targets,
                    data.train_mask,
                )
                val_metrics = unavailable_metrics(
                    val_targets,
                    data.val_mask,
                )
                test_metrics = unavailable_metrics(
                    test_targets,
                    data.test_mask,
                )
                preference_test_routed_accuracy = math.nan
            fixed_test_metrics = preference_metrics(
                router_logits,
                test_targets,
                data.test_mask,
                0.5,
            )
            fixed_test_routed_accuracy = routed_node_accuracy(
                router_logits,
                full_local_logits,
                full_global_logits,
                data.y,
                data.test_mask,
                0.5,
            )
            utility_test_metrics = preference_metrics(
                router_logits,
                test_targets,
                data.test_mask,
                utility_threshold,
            )
            utility_test_routed_accuracy = routed_node_accuracy(
                router_logits,
                full_local_logits,
                full_global_logits,
                data.y,
                data.test_mask,
                utility_threshold,
            )
            utility_test_switch_rate = routing_switch_rate(
                router_logits,
                data.test_mask,
                utility_threshold,
                int(utility_result["default_choice"]),
            )
        else:
            preference_threshold = math.nan
            utility_threshold = math.nan
            train_metrics = unavailable_metrics(train_targets, data.train_mask)
            val_metrics = unavailable_metrics(val_targets, data.val_mask)
            test_metrics = unavailable_metrics(test_targets, data.test_mask)
            preference_test_routed_accuracy = math.nan
            fixed_test_metrics = unavailable_metrics(
                test_targets,
                data.test_mask,
            )
            fixed_test_routed_accuracy = math.nan
            utility_test_metrics = unavailable_metrics(
                test_targets,
                data.test_mask,
            )
            utility_test_routed_accuracy = math.nan
            utility_test_switch_rate = math.nan
            utility_result = {
                "validation_accuracy": math.nan,
                "validation_best_accuracy": math.nan,
                "validation_switch_rate": math.nan,
                "default_choice": -1,
            }
        if result["status"].startswith("ok"):
            preference_state = copy.deepcopy(router.state_dict())
            router.load_state_dict(result["utility_state_dict"])
            router.eval()
            with torch.no_grad():
                utility_checkpoint_logits = router(
                    data.x,
                    data.reliability_gate,
                )
            utility_checkpoint_threshold = float(
                result["utility_decision_threshold"]
            )
            utility_checkpoint_test_accuracy = routed_node_accuracy(
                utility_checkpoint_logits,
                full_local_logits,
                full_global_logits,
                data.y,
                data.test_mask,
                utility_checkpoint_threshold,
            )
            utility_checkpoint_switch_rate = routing_switch_rate(
                utility_checkpoint_logits,
                data.test_mask,
                utility_checkpoint_threshold,
                int(result["utility_default_choice"]),
            )
            router.load_state_dict(preference_state)
        else:
            utility_checkpoint_threshold = math.nan
            utility_checkpoint_test_accuracy = math.nan
            utility_checkpoint_switch_rate = math.nan
        rows.append(
            {
                "dataset": args.dataset,
                "router": router_name,
                "status": result["status"],
                "status_detail": result["status_detail"],
                "edge_protocol": args.edge_protocol,
                "run": f"{split}:{seed}",
                "split": split,
                "seed": seed,
                "oof_folds": args.oof_folds,
                "best_epoch": result["epoch"],
                "best_val_balanced_accuracy": result["balanced_accuracy"],
                "best_val_preference_auc": result["preference_auc"],
                "decision_threshold": preference_threshold,
                "preference_threshold": preference_threshold,
                "utility_threshold": utility_threshold,
                "utility_default_choice": choice_name(
                    int(utility_result["default_choice"])
                ),
                "utility_validation_accuracy": utility_result[
                    "validation_accuracy"
                ],
                "utility_validation_best_accuracy": utility_result[
                    "validation_best_accuracy"
                ],
                "utility_validation_switch_rate": utility_result[
                    "validation_switch_rate"
                ],
                "utility_epsilon_nodes": args.utility_epsilon_nodes,
                **prefix_metrics("train", train_metrics),
                **prefix_metrics("val", val_metrics),
                **prefix_metrics("test", test_metrics),
                "test_routed_node_accuracy": preference_test_routed_accuracy,
                "test_fixed_050_balanced_accuracy": fixed_test_metrics[
                    "balanced_accuracy"
                ],
                "test_fixed_050_routing_accuracy": fixed_test_metrics[
                    "routing_accuracy"
                ],
                "test_fixed_050_routed_node_accuracy": (
                    fixed_test_routed_accuracy
                ),
                "test_utility_balanced_accuracy": utility_test_metrics[
                    "balanced_accuracy"
                ],
                "test_utility_routing_accuracy": utility_test_metrics[
                    "routing_accuracy"
                ],
                "test_utility_routed_node_accuracy": (
                    utility_test_routed_accuracy
                ),
                "test_utility_switch_rate": utility_test_switch_rate,
                "utility_checkpoint_epoch": result[
                    "utility_checkpoint_epoch"
                ],
                "utility_checkpoint_threshold": (
                    utility_checkpoint_threshold
                ),
                "utility_checkpoint_validation_accuracy": result[
                    "utility_checkpoint_validation_accuracy"
                ],
                "test_utility_checkpoint_routed_node_accuracy": (
                    utility_checkpoint_test_accuracy
                ),
                "test_utility_checkpoint_switch_rate": (
                    utility_checkpoint_switch_rate
                ),
                "validation_majority_choice": (
                    "local" if majority_choice == 1 else "global"
                    if majority_choice == 0
                    else "unavailable"
                ),
                "test_majority_routing_accuracy": majority_test_metrics[
                    "routing_accuracy"
                ],
                "test_majority_balanced_accuracy": majority_test_metrics[
                    "balanced_accuracy"
                ],
                "test_majority_routed_node_accuracy": (
                    majority_test_routed_accuracy
                ),
                "validation_best_expert_choice": choice_name(
                    best_expert_choice
                ),
                "validation_best_expert_accuracy": max(
                    local_val_accuracy,
                    global_val_accuracy,
                ),
                "validation_best_expert_test_accuracy": (
                    best_expert_test_accuracy
                ),
                "validation_selected_fixed_alpha": fixed_alpha_result["alpha"],
                "validation_selected_fixed_alpha_accuracy": (
                    fixed_alpha_result["validation_accuracy"]
                ),
                "validation_selected_fixed_alpha_test_accuracy": (
                    fixed_alpha_test_accuracy
                ),
                "test_oracle_union_accuracy": test_oracle_union_accuracy,
                "local_expert_test_accuracy": node_accuracy(
                    full_local_logits,
                    data.y,
                    data.test_mask,
                ),
                "global_expert_test_accuracy": node_accuracy(
                    full_global_logits,
                    data.y,
                    data.test_mask,
                ),
                "reliability_components": ",".join(args.reliability_components),
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
                "router_epochs": args.router_epochs,
                "patience": args.patience,
                "fixed_alphas": ",".join(
                    str(alpha) for alpha in args.fixed_alphas
                ),
                "data_fingerprint": args.data_fingerprint,
                "preprocess_code_hash": args.preprocess_code_hash,
                "oof_cache_hit": oof_stats["cache_hit"],
                "elapsed_sec": time.time() - start,
            }
        )
    return rows


def load_or_build_oof_targets(args, data, split: int, seed: int):
    cache_path, cache_key = oof_cache_path(args, split, seed)
    if cache_path.exists():
        payload = torch.load(cache_path, map_location=data.x.device, weights_only=False)
        if payload.get("cache_key") == cache_key:
            return payload["targets"].to(data.x.device), {"cache_hit": True}

    from sklearn.model_selection import StratifiedKFold

    train_indices = torch.nonzero(data.train_mask, as_tuple=False).view(-1)
    labels = data.y[train_indices].detach().cpu().numpy()
    _, class_counts = np.unique(labels, return_counts=True)
    if int(class_counts.min()) < args.oof_folds:
        raise RuntimeError(
            f"--oof-folds={args.oof_folds} exceeds the smallest training "
            f"class count ({int(class_counts.min())})"
        )
    splitter = StratifiedKFold(
        n_splits=args.oof_folds,
        shuffle=True,
        random_state=seed,
    )
    oof_local = data.x.new_zeros(
        (data.y.numel(), int(data.y.max().item()) + 1)
    )
    oof_global = torch.zeros_like(oof_local)
    filled = torch.zeros_like(data.train_mask)

    for fold, (fit_pos, holdout_pos) in enumerate(
        splitter.split(np.zeros(labels.size), labels)
    ):
        fold_data = copy.copy(data)
        fold_data.train_mask = torch.zeros_like(data.train_mask)
        fit_indices = train_indices[
            torch.as_tensor(fit_pos, device=train_indices.device)
        ]
        holdout_indices = train_indices[
            torch.as_tensor(holdout_pos, device=train_indices.device)
        ]
        fold_data.train_mask[fit_indices] = True
        set_seed(seed + 10_000 * (fold + 1))
        fold_model = build_expert_model(
            name="ordinary_gate",
            in_dim=data.x.size(1),
            reliability_dim=data.reliability_gate.size(1),
            hidden_dim=args.hidden_dim,
            out_dim=int(data.y.max().item()) + 1,
            num_layers=args.num_layers,
            num_heads=args.num_heads,
            dropout=args.dropout,
            fixed_alpha=0.5,
        ).to(data.x.device)
        train_module(
            fold_model.local_expert,
            lambda: fold_model.local_expert(data.x, data.edge_index),
            fold_data,
            args.expert_epochs,
            args.patience,
            args.lr,
            args.weight_decay,
        )
        set_seed(seed + 100_000 + 10_000 * (fold + 1))
        train_module(
            fold_model.global_expert,
            lambda: fold_model.global_expert(data.x),
            fold_data,
            args.expert_epochs,
            args.patience,
            args.lr,
            args.weight_decay,
        )
        fold_model.eval()
        with torch.no_grad():
            local_logits = fold_model.local_expert(data.x, data.edge_index)
            global_logits = fold_model.global_expert(data.x)
        oof_local[holdout_indices] = local_logits[holdout_indices]
        oof_global[holdout_indices] = global_logits[holdout_indices]
        filled[holdout_indices] = True
        print(
            f"  OOF fold {fold + 1}/{args.oof_folds}: "
            f"fit={fit_indices.numel()} holdout={holdout_indices.numel()}",
            flush=True,
        )

    if not torch.equal(filled, data.train_mask):
        raise AssertionError("OOF folds did not cover every training node exactly once")
    targets = preference_targets(
        oof_local,
        oof_global,
        data.y,
        data.train_mask,
    )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "cache_key": cache_key,
            "targets": targets.detach().cpu(),
        },
        cache_path,
    )
    return targets, {"cache_hit": False}


def oof_cache_path(args, split: int, seed: int) -> tuple[Path, str]:
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for path in (
        root / "run_preference_routing.py",
        root / "run_expert_fusion.py",
        root / "src" / "models.py",
        root / "src" / "expert_models.py",
        root / "src" / "preference_routing.py",
    ):
        digest.update(path.read_bytes())
    config = {
        "source": digest.hexdigest(),
        "data_fingerprint": args.data_fingerprint,
        "preprocess_code_hash": args.preprocess_code_hash,
        "dataset": args.dataset,
        "edge_protocol": args.edge_protocol,
        "normalize_features": args.normalize_features,
        "split": split,
        "seed": seed,
        "oof_folds": args.oof_folds,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "expert_epochs": args.expert_epochs,
        "patience": args.patience,
    }
    cache_key = hashlib.sha256(
        json.dumps(config, sort_keys=True).encode("utf-8")
    ).hexdigest()
    path = (
        args.preference_cache_dir
        / args.dataset
        / args.edge_protocol
        / f"oof_split{split}_seed{seed}_{cache_key[:16]}.pt"
    )
    return path, cache_key


def train_router(
    router,
    data,
    train_targets,
    val_targets,
    local_logits,
    global_logits,
    args,
):
    train_selected = data.train_mask & (train_targets >= 0)
    if int(train_selected.sum()) < 2:
        return unavailable_router_result(
            "insufficient_preference_labels",
            "fewer than two OOF preference examples",
        )
    train_values = train_targets[train_selected]
    positives = int((train_values == 1).sum())
    negatives = int((train_values == 0).sum())
    if positives == 0 or negatives == 0:
        return unavailable_router_result(
            "insufficient_preference_labels",
            f"OOF preference labels contain one class: local={positives}, "
            f"global={negatives}",
        )
    val_counts = preference_label_counts(val_targets, data.val_mask)
    validation_has_two_classes = not (
        val_counts["local_preference_count"] == 0
        or val_counts["global_preference_count"] == 0
    )
    positive_weight = torch.tensor(
        negatives / positives,
        device=data.x.device,
    )
    optimizer = torch.optim.AdamW(
        router.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
    best = evaluate_router(
        router,
        data,
        val_targets,
        data.val_mask,
        epoch=-1,
    )
    best_state = copy.deepcopy(router.state_dict())
    utility_best = evaluate_utility_checkpoint(
        router,
        data,
        local_logits,
        global_logits,
        epoch=-1,
        epsilon_nodes=args.utility_epsilon_nodes,
    )
    utility_best_state = copy.deepcopy(router.state_dict())
    stale = 0
    for epoch in range(args.router_epochs):
        router.train()
        optimizer.zero_grad()
        logits = router(data.x, data.reliability_gate)
        loss = F.binary_cross_entropy_with_logits(
            logits[train_selected],
            train_targets[train_selected].float(),
            pos_weight=positive_weight,
        )
        loss.backward()
        optimizer.step()

        result = evaluate_router(
            router,
            data,
            val_targets,
            data.val_mask,
            epoch,
        )
        utility_result = evaluate_utility_checkpoint(
            router,
            data,
            local_logits,
            global_logits,
            epoch,
            epsilon_nodes=args.utility_epsilon_nodes,
        )
        improved = False
        if router_score(result) > router_score(best):
            best = result
            best_state = copy.deepcopy(router.state_dict())
            improved = True
        if utility_checkpoint_score(utility_result) > utility_checkpoint_score(
            utility_best
        ):
            utility_best = utility_result
            utility_best_state = copy.deepcopy(router.state_dict())
            improved = True
        stale = 0 if improved else stale + 1
        if stale >= args.patience:
            break
    router.load_state_dict(best_state)
    status = "ok" if validation_has_two_classes else "ok_utility_only"
    detail = (
        ""
        if validation_has_two_classes
        else "validation preference labels contain one class; "
        "preference checkpoint selected by validation BCE"
    )
    return {
        "status": status,
        "status_detail": detail,
        **best,
        "utility_state_dict": utility_best_state,
        "utility_checkpoint_epoch": utility_best["epoch"],
        "utility_decision_threshold": utility_best["threshold"],
        "utility_checkpoint_validation_accuracy": utility_best[
            "validation_accuracy"
        ],
        "utility_default_choice": utility_best["default_choice"],
    }


def evaluate_router(router, data, targets, mask, epoch: int):
    router.eval()
    with torch.no_grad():
        logits = router(data.x, data.reliability_gate)
    threshold = select_preference_threshold(
        logits,
        targets,
        mask,
    )
    metrics = preference_metrics(logits, targets, mask, threshold)
    selected = mask & (targets >= 0)
    if int(selected.sum()):
        validation_loss = float(
            F.binary_cross_entropy_with_logits(
                logits[selected],
                targets[selected].float(),
            ).cpu()
        )
    else:
        validation_loss = math.nan
    return {
        "epoch": epoch,
        "decision_threshold": threshold,
        "validation_loss": validation_loss,
        **metrics,
    }


def router_score(result) -> tuple[float, float, float]:
    balanced = float(result["balanced_accuracy"])
    auc = float(result["preference_auc"])
    if math.isfinite(balanced):
        return (1.0, balanced, auc if math.isfinite(auc) else -math.inf)
    loss = float(result["validation_loss"])
    return (0.0, -loss if math.isfinite(loss) else -math.inf, -math.inf)


def evaluate_utility_checkpoint(
    router,
    data,
    local_logits,
    global_logits,
    epoch: int,
    epsilon_nodes: int,
):
    router.eval()
    with torch.no_grad():
        logits = router(data.x, data.reliability_gate)
    result = select_utility_threshold(
        logits,
        local_logits,
        global_logits,
        data.y,
        data.val_mask,
        epsilon_nodes=epsilon_nodes,
    )
    return {"epoch": epoch, **result}


def utility_checkpoint_score(result):
    accuracy = float(result["validation_accuracy"])
    switch_rate = float(result["validation_switch_rate"])
    return (
        accuracy if math.isfinite(accuracy) else -math.inf,
        -switch_rate if math.isfinite(switch_rate) else -math.inf,
    )


def prefix_metrics(prefix: str, metrics: dict[str, object]) -> dict[str, object]:
    return {f"{prefix}_{key}": value for key, value in metrics.items()}


def unavailable_metrics(targets, mask):
    return {
        **preference_label_counts(targets, mask),
        **{
            key: value
            for key, value in empty_preference_metrics().items()
            if key not in {
                "preference_count",
                "local_preference_count",
                "global_preference_count",
            }
        },
    }


def unavailable_router_result(status: str, detail: str):
    return {
        "status": status,
        "status_detail": detail,
        "epoch": -1,
        "balanced_accuracy": math.nan,
        "preference_auc": math.nan,
        "decision_threshold": math.nan,
        "utility_checkpoint_epoch": -1,
        "utility_decision_threshold": math.nan,
        "utility_checkpoint_validation_accuracy": math.nan,
        "utility_default_choice": -1,
    }


def node_accuracy(logits, y, mask) -> float:
    return float((logits[mask].argmax(dim=-1) == y[mask]).float().mean())


def choice_name(choice: int) -> str:
    return "local" if choice == 1 else "global" if choice == 0 else "unavailable"


def finite_mean(rows, field: str) -> float:
    values = np.asarray([float(row[field]) for row in rows])
    values = values[np.isfinite(values)]
    return float(values.mean()) if values.size else math.nan


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        if not rows:
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
