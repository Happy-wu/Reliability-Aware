from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import mean, pstdev
from types import SimpleNamespace

from run_synthetic import train_one
from src.data import RELIABILITY_COMPONENTS


DEFAULT_MODELS = [
    "mlp",
    "gcn",
    "linear_gt",
    "q_only_gt",
    "k_only_gt",
    "qk_gt",
    "gate_gt",
    "reliability_gt",
]
DEFAULT_GRAPHS = ["heterophily", "homophily", "noisy"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--graph-types", nargs="+", default=DEFAULT_GRAPHS)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    parser.add_argument("--tag", default="default")

    parser.add_argument("--num-nodes", type=int, default=900)
    parser.add_argument("--num-classes", type=int, default=3)
    parser.add_argument("--feature-dim", type=int, default=32)
    parser.add_argument("--feature-noise", type=float, default=0.7)
    parser.add_argument("--edge-noise", type=float, default=0.0)
    parser.add_argument("--rw-steps", type=int, default=4)
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
    parser.add_argument("--qk-strength-init", type=float, default=-5.0)
    parser.add_argument("--fixed-qk-strength", type=float, default=None)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--patience", type=int, default=60)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    batch_dir = args.out_dir / f"batch_{args.tag}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    raw_rows = []
    total = len(args.graph_types) * len(args.models) * len(args.seeds)
    step = 0
    for graph_type in args.graph_types:
        for model in args.models:
            for seed in args.seeds:
                step += 1
                print(f"[{step}/{total}] graph={graph_type} model={model} seed={seed}")
                run_args = SimpleNamespace(**vars(args))
                run_args.graph_type = graph_type
                run_args.model = model
                run_args.seeds = [seed]
                row = train_one(run_args, seed)
                raw_rows.append(row)
                write_csv(batch_dir / "raw_results.csv", raw_rows)

    summary_rows = summarize(raw_rows)
    write_csv(batch_dir / "summary.csv", summary_rows)
    print_summary(summary_rows)
    print(f"\nraw results: {batch_dir / 'raw_results.csv'}")
    print(f"summary:     {batch_dir / 'summary.csv'}")


def summarize(rows: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        groups.setdefault((row["graph_type"], row["model"]), []).append(row)

    summary = []
    mean_by_graph_model = {}
    for (graph_type, model), group_rows in sorted(groups.items()):
        test_values = [float(r["test_acc_at_best_val"]) for r in group_rows]
        val_values = [float(r["best_val_acc"]) for r in group_rows]
        elapsed_values = [float(r["elapsed_sec"]) for r in group_rows]
        test_mean = mean(test_values)
        mean_by_graph_model[(graph_type, model)] = test_mean
        summary.append(
            {
                "graph_type": graph_type,
                "model": model,
                "reliability_components": group_rows[0]["reliability_components"],
                "reliability_encoder": group_rows[0]["reliability_encoder"],
                "n": len(group_rows),
                "test_acc_mean": test_mean,
                "test_acc_std": pstdev(test_values) if len(test_values) > 1 else 0.0,
                "best_val_acc_mean": mean(val_values),
                "qk_strength_mean": mean_non_nan(group_rows, "qk_strength_mean"),
                "qk_gamma_q_abs_dev_mean": mean_non_nan(group_rows, "qk_gamma_q_abs_dev_mean"),
                "qk_gamma_k_abs_dev_mean": mean_non_nan(group_rows, "qk_gamma_k_abs_dev_mean"),
                "qk_gamma_q_std_mean": mean_non_nan(group_rows, "qk_gamma_q_std"),
                "qk_gamma_k_std_mean": mean_non_nan(group_rows, "qk_gamma_k_std"),
                "qk_gamma_q_abs_dev_max_mean": mean_non_nan(group_rows, "qk_gamma_q_abs_dev_max"),
                "qk_gamma_k_abs_dev_max_mean": mean_non_nan(group_rows, "qk_gamma_k_abs_dev_max"),
                "gate_corr_degree_mean": mean_non_nan(group_rows, "gate_corr_degree"),
                "gate_corr_local_similarity_mean": mean_non_nan(group_rows, "gate_corr_local_similarity"),
                "gate_corr_neighbor_variance_mean": mean_non_nan(group_rows, "gate_corr_neighbor_variance"),
                "gate_corr_rwse_mean": mean_non_nan(group_rows, "gate_corr_rwse_mean"),
                "gate_corr_layer1_local_similarity_mean": mean_non_nan(group_rows, "gate_corr_layer1_local_similarity"),
                "gate_corr_layer2_local_similarity_mean": mean_non_nan(group_rows, "gate_corr_layer2_local_similarity"),
                "elapsed_sec_mean": mean(elapsed_values),
            }
        )

    for row in summary:
        baseline = mean_by_graph_model.get((row["graph_type"], "linear_gt"))
        row["delta_vs_linear_gt"] = (
            row["test_acc_mean"] - baseline
            if baseline is not None and row["model"] != "linear_gt"
            else 0.0 if row["model"] == "linear_gt" else math.nan
        )
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict]) -> None:
    print("\nSummary")
    header = (
        f"{'graph':<12} {'model':<16} {'n':>3} "
        f"{'test_mean':>10} {'test_std':>9} {'delta_lgt':>10} "
        f"{'qk_str':>8} {'gq_dev':>8} {'gk_dev':>8} {'gate_loc':>9}"
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            f"{row['graph_type']:<12} {row['model']:<16} {int(row['n']):>3} "
            f"{float(row['test_acc_mean']):>10.4f} {float(row['test_acc_std']):>9.4f} "
            f"{float(row['delta_vs_linear_gt']):>10.4f} "
            f"{format_float(row['qk_strength_mean']):>8} "
            f"{format_float(row['qk_gamma_q_abs_dev_mean']):>8} "
            f"{format_float(row['qk_gamma_k_abs_dev_mean']):>8} "
            f"{format_float(row['gate_corr_local_similarity_mean']):>9}"
        )


def format_float(value) -> str:
    value = float(value)
    if is_nan(value):
        return "nan"
    return f"{value:.4f}"


def mean_non_nan(rows: list[dict], key: str) -> float:
    values = []
    for row in rows:
        if key not in row:
            continue
        value = float(row[key])
        if not is_nan(value):
            values.append(value)
    return mean(values) if values else math.nan


def is_nan(value: float) -> bool:
    return math.isnan(value)


if __name__ == "__main__":
    main()
