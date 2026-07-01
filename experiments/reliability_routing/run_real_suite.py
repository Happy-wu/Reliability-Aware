from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.real_data import REAL_DATASETS


MODELS = (
    "mlp",
    "gcn",
    "gcn_pyg",
    "local_only_gt",
    "linear_gt",
    "qk_gt",
    "gate_gt",
    "reliability_gt",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--datasets", nargs="+", choices=REAL_DATASETS, default=list(REAL_DATASETS))
    parser.add_argument("--models", nargs="+", choices=MODELS, default=list(MODELS))
    parser.add_argument(
        "--training-profile",
        choices=["standard", "classic_gcn"],
        default="standard",
    )
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/real_suite"))
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--normalize-features", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--rw-steps", type=int, default=4)
    parser.add_argument("--rw-samples", type=int, default=128)
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--qk-strength-init", type=float, default=-5.0)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--epochs", type=int, default=500)
    parser.add_argument("--patience", type=int, default=100)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--analyze-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.training_profile == "classic_gcn" and args.models != ["gcn_pyg"]:
        raise SystemExit(
            "--training-profile classic_gcn requires exactly: --models gcn_pyg"
        )
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    config = suite_config(args, root)
    validate_or_write_config(out_dir, config, args.force)

    if not args.analyze_only:
        prepare_datasets(args, root, data_root, out_dir)
        run_experiments(args, root, data_root, out_dir)

    missing = [
        f"{dataset}/{model}"
        for dataset in args.datasets
        for model in args.models
        if not result_complete(out_dir / f"{dataset}_{model}.csv", args.runs)
    ]
    if missing:
        raise SystemExit("Missing real results: " + ", ".join(missing))

    report = analyze(args, out_dir)
    print(f"\nReal-data analysis: {report}")


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def suite_config(args: argparse.Namespace, root: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    for relative in (
        "src/data.py",
        "src/models.py",
        "src/real_data.py",
        "run_real.py",
        "run_real_suite.py",
    ):
        digest.update((root / relative).read_bytes())
    return {
        "code_fingerprint": digest.hexdigest(),
        "datasets": list(args.datasets),
        "models": list(args.models),
        "training_profile": args.training_profile,
        "runs": args.runs,
        "normalize_features": args.normalize_features,
        "rw_steps": args.rw_steps,
        "rw_samples": args.rw_samples,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "qk_strength_init": args.qk_strength_init,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "epochs": args.epochs,
        "patience": args.patience,
        "device": args.device,
    }


def validate_or_write_config(
    out_dir: Path,
    config: dict[str, object],
    force: bool,
) -> None:
    path = out_dir / "suite_config.json"
    if path.exists() and not force:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != config:
            raise RuntimeError(
                "Existing real-suite outputs use a different configuration. "
                "Use a new --out-dir or pass --force to replace them."
            )
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def prepare_datasets(
    args: argparse.Namespace,
    root: Path,
    data_root: Path,
    out_dir: Path,
) -> None:
    command = [
        args.python,
        str(root / "prepare_real_datasets.py"),
        "--datasets",
        *args.datasets,
        "--data-root",
        str(data_root),
        "--report",
        str(out_dir / "dataset_validation.json"),
    ]
    if args.no_download:
        command.append("--no-download")
    print("Validating real datasets before training", flush=True)
    subprocess.run(command, cwd=root, check=True)


def run_experiments(
    args: argparse.Namespace,
    root: Path,
    data_root: Path,
    out_dir: Path,
) -> None:
    total = len(args.datasets) * len(args.models)
    step = 0
    for dataset in args.datasets:
        for model in args.models:
            step += 1
            result_path = out_dir / f"{dataset}_{model}.csv"
            if not args.force and result_complete(result_path, args.runs):
                print(f"[{step}/{total}] skip {dataset}/{model}", flush=True)
                continue
            if args.force and result_path.exists():
                result_path.unlink()
            command = [
                args.python,
                str(root / "run_real.py"),
                "--dataset",
                dataset,
                "--model",
                model,
                "--runs",
                str(args.runs),
                "--training-profile",
                args.training_profile,
                "--data-root",
                str(data_root),
                "--out-dir",
                str(out_dir),
                "--rw-steps",
                str(args.rw_steps),
                "--rw-samples",
                str(args.rw_samples),
                "--hidden-dim",
                str(args.hidden_dim),
                "--num-layers",
                str(args.num_layers),
                "--num-heads",
                str(args.num_heads),
                "--dropout",
                str(args.dropout),
                "--qk-strength-init",
                str(args.qk_strength_init),
                "--lr",
                str(args.lr),
                "--weight-decay",
                str(args.weight_decay),
                "--epochs",
                str(args.epochs),
                "--patience",
                str(args.patience),
                "--device",
                args.device,
            ]
            if not args.normalize_features:
                command.append("--no-normalize-features")
            command.append("--no-download")
            print(f"[{step}/{total}] run {dataset}/{model}", flush=True)
            subprocess.run(command, cwd=root, check=True)


def result_complete(path: Path, runs: int) -> bool:
    return path.exists() and len(read_csv(path)) == runs


def analyze(args: argparse.Namespace, out_dir: Path) -> Path:
    rows = []
    for dataset in args.datasets:
        for model in args.models:
            rows.extend(read_csv(out_dir / f"{dataset}_{model}.csv"))

    summary = summarize(rows)
    diagnostics = summarize_diagnostics(rows)
    comparisons = compare_models(rows, args.datasets)
    write_csv(out_dir / "summary.csv", summary)
    write_csv(
        out_dir / "diagnostics_summary.csv",
        diagnostics,
        fieldnames=[
            "dataset",
            "model",
            "gate_mean",
            "gate_std",
            "local_branch_norm_mean",
            "global_branch_norm_mean",
            "mixed_branch_norm_mean",
            "local_global_cosine_mean",
        ],
    )
    write_csv(
        out_dir / "paired_comparisons.csv",
        comparisons,
        fieldnames=[
            "dataset",
            "comparison",
            "n",
            "mean_delta",
            "ci95_low",
            "ci95_high",
            "wins",
            "ties",
            "losses",
            "pvalue",
        ],
    )

    lines = [
        "# Real Dataset Preliminary Analysis",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Datasets: {', '.join(args.datasets)}",
        f"- Models: {', '.join(args.models)}",
        f"- Runs per dataset/model: {args.runs}",
        "- Planetoid uses its public split with repeated training seeds.",
        "- Chameleon, Squirrel, and Actor cycle through official Geom-GCN splits.",
        "",
        "## Accuracy Summary",
        "",
        "| Dataset | Model | Mean | Std |",
        "|---|---|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['dataset']} | {row['model']} | "
            f"{row['test_acc_mean']:.4f} | {row['test_acc_std']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Paired Comparisons",
            "",
            "| Dataset | Comparison | Delta | 95% CI | W/T/L | p |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in comparisons:
        lines.append(
            f"| {row['dataset']} | {row['comparison']} | {row['mean_delta']:+.4f} | "
            f"[{fmt(row['ci95_low'])}, {fmt(row['ci95_high'])}] | "
            f"{row['wins']}/{row['ties']}/{row['losses']} | {fmt(row['pvalue'])} |"
        )
    lines.extend(
        [
            "",
            "## Routing Diagnostics",
            "",
            "| Dataset | Model | Gate mean | Gate std | Local norm | Global norm | Mixed norm | Local/global cosine |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in diagnostics:
        lines.append(
            f"| {row['dataset']} | {row['model']} | {fmt_plain(row['gate_mean'])} | "
            f"{fmt_plain(row['gate_std'])} | {fmt_plain(row['local_branch_norm_mean'])} | "
            f"{fmt_plain(row['global_branch_norm_mean'])} | "
            f"{fmt_plain(row['mixed_branch_norm_mean'])} | "
            f"{fmt_plain(row['local_global_cosine_mean'])} |"
        )
    lines.extend(
        [
            "",
            "## Decision Rule",
            "",
            "- If Reliability-GT consistently exceeds Gate-GT, Q/K remains a candidate contribution.",
            "- If Reliability-GT is approximately equal to Gate-GT, routing is the primary contribution.",
            "- If Gate-GT does not exceed LinearGT, inspect reliability transfer and tuning before adding architecture.",
            "- These p-values are exploratory and uncorrected across datasets.",
        ]
    )
    path = out_dir / "preliminary_analysis.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def summarize(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str], list[float]] = {}
    for row in rows:
        groups.setdefault((row["dataset"], row["model"]), []).append(
            float(row["test_acc_at_best_val"])
        )
    return [
        {
            "dataset": dataset,
            "model": model,
            "n": len(values),
            "test_acc_mean": statistics.mean(values),
            "test_acc_std": statistics.pstdev(values),
        }
        for (dataset, model), values in sorted(groups.items())
    ]


def summarize_diagnostics(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    metrics = (
        "gate_mean",
        "gate_std",
        "local_branch_norm_mean",
        "global_branch_norm_mean",
        "mixed_branch_norm_mean",
        "local_global_cosine_mean",
    )
    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault((row["dataset"], row["model"]), []).append(row)

    output = []
    for (dataset, model), group in sorted(groups.items()):
        values = {
            metric: finite_mean(row.get(metric, "") for row in group)
            for metric in metrics
        }
        if all(math.isnan(value) for value in values.values()):
            continue
        output.append({"dataset": dataset, "model": model, **values})
    return output


def finite_mean(values) -> float:
    numbers = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            numbers.append(number)
    return statistics.mean(numbers) if numbers else math.nan


def compare_models(
    rows: list[dict[str, str]],
    datasets: list[str],
) -> list[dict[str, object]]:
    pairs = (
        ("gcn_pyg", "gcn", "PyG-GCN - custom GCN"),
        ("local_only_gt", "gcn_pyg", "Local-only GT - PyG-GCN"),
        ("qk_gt", "linear_gt", "QK-GT - LinearGT"),
        ("gate_gt", "linear_gt", "Gate-GT - LinearGT"),
        ("reliability_gt", "linear_gt", "Reliability-GT - LinearGT"),
        ("reliability_gt", "gate_gt", "Reliability-GT - Gate-GT"),
    )
    output = []
    for dataset in datasets:
        for left, right, label in pairs:
            available = {
                row["model"] for row in rows if row["dataset"] == dataset
            }
            if left not in available or right not in available:
                continue
            output.append(
                {
                    "dataset": dataset,
                    "comparison": label,
                    **paired_stats(rows, dataset, left, right),
                }
            )
    return output


def paired_stats(
    rows: list[dict[str, str]],
    dataset: str,
    left_model: str,
    right_model: str,
) -> dict[str, object]:
    left = keyed_values(rows, dataset, left_model)
    right = keyed_values(rows, dataset, right_model)
    keys = sorted(set(left).intersection(right))
    if not keys:
        return {
            "n": 0,
            "mean_delta": math.nan,
            "ci95_low": math.nan,
            "ci95_high": math.nan,
            "wins": 0,
            "ties": 0,
            "losses": 0,
            "pvalue": math.nan,
        }
    differences = [left[key] - right[key] for key in keys]
    mean_delta = statistics.mean(differences)
    ci_half = ci95(differences)
    try:
        from scipy.stats import ttest_rel

        pvalue = float(
            ttest_rel([left[key] for key in keys], [right[key] for key in keys]).pvalue
        )
    except ImportError:
        pvalue = math.nan
    wins = sum(value > 0 for value in differences)
    ties = sum(value == 0 for value in differences)
    return {
        "n": len(keys),
        "mean_delta": mean_delta,
        "ci95_low": mean_delta - ci_half,
        "ci95_high": mean_delta + ci_half,
        "wins": wins,
        "ties": ties,
        "losses": len(keys) - wins - ties,
        "pvalue": pvalue,
    }


def keyed_values(
    rows: list[dict[str, str]],
    dataset: str,
    model: str,
) -> dict[tuple[int, int], float]:
    return {
        (int(row["split"]), int(row["seed"])): float(row["test_acc_at_best_val"])
        for row in rows
        if row["dataset"] == dataset and row["model"] == model
    }


def ci95(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    standard_error = statistics.stdev(values) / math.sqrt(len(values))
    try:
        from scipy.stats import t

        critical = float(t.ppf(0.975, len(values) - 1))
    except ImportError:
        critical = 1.96
    return critical * standard_error


def fmt(value: object) -> str:
    number = float(value)
    return "n/a" if math.isnan(number) else f"{number:+.4f}"


def fmt_plain(value: object) -> str:
    number = float(value)
    return "n/a" if math.isnan(number) else f"{number:.4f}"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(
    path: Path,
    rows: list[dict[str, object]],
    fieldnames: list[str] | None = None,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        if fieldnames is None:
            if not rows:
                raise ValueError(f"Cannot infer CSV columns for empty rows: {path}")
            fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
