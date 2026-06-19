from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path

from src.data import RELIABILITY_COMPONENTS
from src.preference_routing import ROUTERS
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    validation_fingerprint,
)


DEFAULT_DATASETS = (
    "Cora",
    "Citeseer",
    "Pubmed",
    "Chameleon",
    "Squirrel",
    "Actor",
    "Roman-empire",
    "Amazon-ratings",
    "Minesweeper",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run and summarize preference-routing diagnostics."
    )
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=REAL_DATASETS,
        default=list(DEFAULT_DATASETS),
    )
    parser.add_argument("--routers", nargs="+", choices=ROUTERS, default=list(ROUTERS))
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--oof-folds", type=int, default=5)
    parser.add_argument(
        "--edge-protocol",
        choices=EDGE_PROTOCOLS,
        default="undirected",
    )
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/preference_routing"),
    )
    parser.add_argument("--expert-cache-dir", type=Path)
    parser.add_argument("--preference-cache-dir", type=Path)
    parser.add_argument(
        "--reliability-components",
        nargs="+",
        choices=RELIABILITY_COMPONENTS,
        default=list(RELIABILITY_COMPONENTS),
    )
    parser.add_argument("--rw-steps", type=int, default=4)
    parser.add_argument("--rw-samples", type=int, default=128)
    parser.add_argument("--rw-seed", type=int, default=0)
    parser.add_argument(
        "--normalize-features",
        action=argparse.BooleanOptionalAction,
        default=True,
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
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--analyze-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    expert_cache = resolve(
        root,
        args.expert_cache_dir or out_dir / "_expert_cache",
    )
    preference_cache = resolve(
        root,
        args.preference_cache_dir or out_dir / "_preference_cache",
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    config = suite_config(
        args,
        root,
        data_root,
        expert_cache,
        preference_cache,
    )
    validate_or_write_config(out_dir, config, args.force)

    if not args.analyze_only:
        total = len(args.datasets)
        for index, dataset in enumerate(args.datasets, start=1):
            result_path = out_dir / f"{dataset}_preference_routing.csv"
            if result_complete(
                result_path,
                args.runs,
                args.routers,
                dataset,
                args,
                config["data_fingerprints"][dataset],
            ) and not args.force:
                print(f"[{index}/{total}] skip {dataset}", flush=True)
                continue
            if args.force and result_path.exists():
                result_path.unlink()
            command = [
                args.python,
                str(root / "run_preference_routing.py"),
                "--dataset",
                dataset,
                "--routers",
                *args.routers,
                "--edge-protocol",
                args.edge_protocol,
                "--runs",
                str(args.runs),
                "--oof-folds",
                str(args.oof_folds),
                "--data-root",
                str(data_root),
                "--out-dir",
                str(out_dir),
                "--expert-cache-dir",
                str(expert_cache),
                "--preference-cache-dir",
                str(preference_cache),
                "--reliability-components",
                *args.reliability_components,
                "--rw-steps",
                str(args.rw_steps),
                "--rw-samples",
                str(args.rw_samples),
                "--rw-seed",
                str(args.rw_seed),
                "--hidden-dim",
                str(args.hidden_dim),
                "--num-layers",
                str(args.num_layers),
                "--num-heads",
                str(args.num_heads),
                "--dropout",
                str(args.dropout),
                "--lr",
                str(args.lr),
                "--weight-decay",
                str(args.weight_decay),
                "--expert-epochs",
                str(args.expert_epochs),
                "--router-epochs",
                str(args.router_epochs),
                "--patience",
                str(args.patience),
                "--device",
                args.device,
            ]
            if not args.normalize_features:
                command.append("--no-normalize-features")
            if args.no_download:
                command.append("--no-download")
            print(f"[{index}/{total}] run {dataset}", flush=True)
            subprocess.run(command, cwd=root, check=True)

    rows = []
    for dataset in args.datasets:
        path = out_dir / f"{dataset}_preference_routing.csv"
        if not result_complete(
            path,
            args.runs,
            args.routers,
            dataset,
            args,
            config["data_fingerprints"][dataset],
        ):
            raise SystemExit(f"Missing or incomplete preference result: {path}")
        rows.extend(read_csv(path))
    summary = summarize(rows)
    comparisons = compare_routers(rows, args.datasets, args.routers)
    write_csv(out_dir / "summary.csv", summary)
    write_csv(out_dir / "paired_comparisons.csv", comparisons)
    write_report(out_dir / "analysis.md", summary, comparisons)
    print(f"analysis: {out_dir / 'analysis.md'}")


def summarize(rows):
    output = []
    for dataset in sorted({row["dataset"] for row in rows}):
        for router in ROUTERS:
            selected = [
                row for row in rows
                if row["dataset"] == dataset and row["router"] == router
            ]
            if not selected:
                continue
            output.append(
                {
                    "dataset": dataset,
                    "router": router,
                    "n": len(selected),
                    "successful_n": sum(row.get("status") == "ok" for row in selected),
                    "status_counts": status_counts(selected),
                    "test_preference_count_mean": mean(selected, "test_preference_count"),
                    "test_preference_auc_mean": mean(selected, "test_preference_auc"),
                    "test_preference_auc_std": std(selected, "test_preference_auc"),
                    "test_preference_auc_ci95_low": mean(selected, "test_preference_auc")
                    - ci95(finite_values(selected, "test_preference_auc")),
                    "test_preference_auc_ci95_high": mean(selected, "test_preference_auc")
                    + ci95(finite_values(selected, "test_preference_auc")),
                    "decision_threshold_mean": mean(selected, "decision_threshold"),
                    "test_balanced_accuracy_mean": mean(selected, "test_balanced_accuracy"),
                    "test_routing_accuracy_mean": mean(selected, "test_routing_accuracy"),
                    "test_routed_node_accuracy_mean": mean(selected, "test_routed_node_accuracy"),
                    "test_majority_routing_accuracy_mean": mean(
                        selected,
                        "test_majority_routing_accuracy",
                    ),
                    "test_majority_balanced_accuracy_mean": mean(
                        selected,
                        "test_majority_balanced_accuracy",
                    ),
                    "test_majority_routed_node_accuracy_mean": mean(
                        selected,
                        "test_majority_routed_node_accuracy",
                    ),
                }
            )
    return output


def compare_routers(rows, datasets, routers):
    pairs = (
        ("reliability_only", "node_feature_only"),
        ("combined", "node_feature_only"),
    )
    output = []
    selected = set(routers)
    for dataset in datasets:
        for left, right in pairs:
            if left not in selected or right not in selected:
                continue
            for metric in (
                "test_preference_auc",
                "test_balanced_accuracy",
                "test_routing_accuracy",
            ):
                stats = paired_stats(rows, dataset, left, right, metric)
                output.append(
                    {
                        "dataset": dataset,
                        "comparison": f"{left} - {right}",
                        "metric": metric,
                        **stats,
                    }
                )
    return output


def paired_stats(rows, dataset, left, right, metric):
    left_values = run_values(rows, dataset, left, metric)
    right_values = run_values(rows, dataset, right, metric)
    keys = sorted(set(left_values).intersection(right_values))
    differences = [
        left_values[key] - right_values[key]
        for key in keys
        if math.isfinite(left_values[key]) and math.isfinite(right_values[key])
    ]
    if not differences:
        return {
            "n": 0,
            "mean_delta": math.nan,
            "ci95_low": math.nan,
            "ci95_high": math.nan,
            "wins": 0,
            "ties": 0,
            "losses": 0,
        }
    delta = statistics.mean(differences)
    half = ci95(differences)
    return {
        "n": len(differences),
        "mean_delta": delta,
        "ci95_low": delta - half,
        "ci95_high": delta + half,
        "wins": sum(value > 1e-12 for value in differences),
        "ties": sum(abs(value) <= 1e-12 for value in differences),
        "losses": sum(value < -1e-12 for value in differences),
    }


def write_report(path, summary, comparisons):
    lines = [
        "# Preference Routing Diagnostic",
        "",
        "Primary question: can reliability predict which frozen expert is correct?",
        "",
        "## Summary",
        "",
        "| Dataset | Router | Valid/Total | Status | Preference nodes | AUC [95% CI] | Threshold | Balanced acc | Routing acc | Majority routing | Routed node acc | Majority node acc |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['dataset']} | {row['router']} | "
            f"{row['successful_n']}/{row['n']} | {row['status_counts']} | "
            f"{fmt(row['test_preference_count_mean'], 1)} | "
            f"{fmt(row['test_preference_auc_mean'])} "
            f"[{fmt(row['test_preference_auc_ci95_low'])}, "
            f"{fmt(row['test_preference_auc_ci95_high'])}] | "
            f"{fmt(row['decision_threshold_mean'])} | "
            f"{fmt(row['test_balanced_accuracy_mean'])} | "
            f"{fmt(row['test_routing_accuracy_mean'])} | "
            f"{fmt(row['test_majority_routing_accuracy_mean'])} | "
            f"{fmt(row['test_routed_node_accuracy_mean'])} | "
            f"{fmt(row['test_majority_routed_node_accuracy_mean'])} |"
        )
    lines.extend(
        [
            "",
            "## Paired Comparisons",
            "",
            "| Dataset | Comparison | Metric | N | Delta | 95% CI | W/T/L |",
            "|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in comparisons:
        lines.append(
            f"| {row['dataset']} | {row['comparison']} | {row['metric']} | "
            f"{row['n']} | {fmt(row['mean_delta'])} | "
            f"[{fmt(row['ci95_low'])}, {fmt(row['ci95_high'])}] | "
            f"{row['wins']}/{row['ties']}/{row['losses']} |"
        )
    lines.extend(
        [
            "",
            "## Decision Rule",
            "",
            "- Continue reliability routing only if reliability-only AUC is clearly above 0.5 and combined reliably exceeds node-feature-only on at least two undirected heterophilous datasets.",
            "- Treat routed node accuracy as secondary; preference AUC and balanced accuracy diagnose whether the routing signal exists.",
            "- Training preference labels are generated from out-of-fold expert predictions to avoid in-sample expert leakage.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def result_complete(path, runs, routers, dataset, args, data_fingerprint):
    if not path.exists():
        return False
    rows = read_csv(path)
    required = {
        "dataset",
        "router",
        "status",
        "edge_protocol",
        "run",
        "split",
        "seed",
        "oof_folds",
        "decision_threshold",
        "validation_majority_choice",
        "test_majority_routing_accuracy",
        "test_majority_balanced_accuracy",
        "test_majority_routed_node_accuracy",
        "reliability_components",
        "normalize_features",
        "rw_steps",
        "rw_samples",
        "rw_seed",
        "hidden_dim",
        "num_layers",
        "num_heads",
        "dropout",
        "lr",
        "weight_decay",
        "expert_epochs",
        "router_epochs",
        "patience",
        "data_fingerprint",
        "preprocess_code_hash",
    }
    if len(rows) != runs * len(routers):
        return False
    if not rows or not required.issubset(rows[0]):
        return False
    expected = {
        "dataset": dataset,
        "edge_protocol": args.edge_protocol,
        "oof_folds": str(args.oof_folds),
        "reliability_components": ",".join(args.reliability_components),
        "normalize_features": str(args.normalize_features),
        "rw_steps": str(args.rw_steps),
        "rw_samples": str(args.rw_samples),
        "rw_seed": str(args.rw_seed),
        "hidden_dim": str(args.hidden_dim),
        "num_layers": str(args.num_layers),
        "num_heads": str(args.num_heads),
        "dropout": str(args.dropout),
        "lr": str(args.lr),
        "weight_decay": str(args.weight_decay),
        "expert_epochs": str(args.expert_epochs),
        "router_epochs": str(args.router_epochs),
        "patience": str(args.patience),
        "data_fingerprint": data_fingerprint,
    }
    if any(
        any(row.get(key) != value for key, value in expected.items())
        or not row.get("preprocess_code_hash")
        for row in rows
    ):
        return False
    if len({row["preprocess_code_hash"] for row in rows}) != 1:
        return False
    run_sets = []
    for router in routers:
        router_rows = [row for row in rows if row["router"] == router]
        run_ids = {row["run"] for row in router_rows}
        if len(router_rows) != runs or len(run_ids) != runs:
            return False
        run_sets.append(run_ids)
    return all(run_ids == run_sets[0] for run_ids in run_sets[1:])


def run_values(rows, dataset, router, metric):
    return {
        row["run"]: float(row[metric])
        for row in rows
        if row["dataset"] == dataset and row["router"] == router
    }


def finite_values(rows, field):
    values = [float(row[field]) for row in rows]
    return [value for value in values if math.isfinite(value)]


def mean(rows, field):
    values = finite_values(rows, field)
    return statistics.mean(values) if values else math.nan


def std(rows, field):
    values = finite_values(rows, field)
    return statistics.stdev(values) if len(values) > 1 else 0.0


def ci95(values):
    if len(values) < 2:
        return math.nan
    try:
        from scipy.stats import t

        critical = float(t.ppf(0.975, len(values) - 1))
    except ImportError:
        critical = 1.96
    return critical * statistics.stdev(values) / math.sqrt(len(values))


def suite_config(args, root, data_root, expert_cache, preference_cache):
    digest = hashlib.sha256()
    for relative in (
        "src/data.py",
        "src/models.py",
        "src/expert_models.py",
        "src/preference_routing.py",
        "src/real_data.py",
        "run_expert_fusion.py",
        "run_preference_routing.py",
        "run_preference_routing_suite.py",
    ):
        digest.update((root / relative).read_bytes())
    data_fingerprints = {}
    for dataset in args.datasets:
        _, report = load_and_validate_dataset(
            dataset,
            data_root,
            allow_download=not args.no_download,
        )
        data_fingerprints[dataset] = validation_fingerprint(report)
    return {
        "code_fingerprint": digest.hexdigest(),
        "datasets": args.datasets,
        "routers": args.routers,
        "runs": args.runs,
        "oof_folds": args.oof_folds,
        "edge_protocol": args.edge_protocol,
        "data_root": str(data_root),
        "expert_cache_dir": str(expert_cache),
        "preference_cache_dir": str(preference_cache),
        "data_fingerprints": data_fingerprints,
        "reliability_components": args.reliability_components,
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
        "device": args.device,
    }


def validate_or_write_config(out_dir, config, force):
    path = out_dir / "suite_config.json"
    if path.exists() and not force:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != config:
            raise RuntimeError(
                "Output directory uses a different configuration. "
                "Choose a new --out-dir or rerun with --force."
            )
    path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def status_counts(rows):
    counts = {}
    for row in rows:
        status = row.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    return ";".join(f"{key}:{counts[key]}" for key in sorted(counts))


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        if not rows:
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fmt(value, digits=4):
    value = float(value)
    return "n/a" if not math.isfinite(value) else f"{value:.{digits}f}"


def resolve(root, path):
    return path if path.is_absolute() else root / path


if __name__ == "__main__":
    main()
