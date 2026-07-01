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
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    validation_fingerprint,
)


BASE_MODELS = ("gcn_pyg", "global_only", "ordinary_gate", "reliability_gate")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--datasets", nargs="+", choices=REAL_DATASETS, default=list(REAL_DATASETS))
    parser.add_argument("--models", nargs="+", choices=BASE_MODELS, default=list(BASE_MODELS))
    parser.add_argument("--fixed-alphas", nargs="*", type=float, default=[0.0, 0.25, 0.5, 0.75, 1.0])
    parser.add_argument("--edge-protocol", choices=EDGE_PROTOCOLS, default="undirected")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/expert_fusion_undirected"))
    parser.add_argument("--expert-cache-dir", type=Path)
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
    parser.add_argument("--gate-epochs", type=int, default=300)
    parser.add_argument("--patience", type=int, default=100)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--analyze-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for alpha in args.fixed_alphas:
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("--fixed-alphas values must be between 0 and 1")
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    expert_cache_dir = (
        resolve(root, args.expert_cache_dir)
        if args.expert_cache_dir is not None
        else out_dir / "_expert_cache"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    args.expert_cache_dir = expert_cache_dir
    specs = model_specs(args)
    data_fingerprints = collect_data_fingerprints(args, data_root)
    config = suite_config(args, root, specs, data_fingerprints)
    validate_or_write_config(out_dir, config, args.force)
    if not args.analyze_only:
        run_experiments(args, root, data_root, out_dir, specs)
    missing = [
        f"{dataset}/{name}"
        for dataset in args.datasets
        for _, name, _ in specs
        if not result_complete(
            out_dir / f"{dataset}_{name}.csv",
            args.runs,
            dataset,
            name,
            args.edge_protocol,
        )
    ]
    if missing:
        raise SystemExit("Missing expert-fusion results: " + ", ".join(missing))
    analyze(args, out_dir, specs)


def model_specs(args) -> list[tuple[str, str, float | None]]:
    specs = [(model, model, None) for model in args.models]
    for alpha in args.fixed_alphas:
        name = f"fixed_alpha_{int(round(alpha * 100)):03d}"
        specs.append(("fixed_alpha", name, alpha))
    return specs


def run_experiments(args, root, data_root, out_dir, specs) -> None:
    total = len(args.datasets) * len(specs)
    step = 0
    for dataset in args.datasets:
        for model, name, alpha in specs:
            step += 1
            path = out_dir / f"{dataset}_{name}.csv"
            if not args.force and result_complete(
                path,
                args.runs,
                dataset,
                name,
                args.edge_protocol,
            ):
                print(f"[{step}/{total}] skip {dataset}/{name}", flush=True)
                continue
            if args.force and path.exists():
                path.unlink()
            command = [
                args.python,
                str(root / "run_expert_fusion.py"),
                "--dataset", dataset,
                "--model", model,
                "--result-name", name,
                "--edge-protocol", args.edge_protocol,
                "--runs", str(args.runs),
                "--data-root", str(data_root),
                "--out-dir", str(out_dir),
                "--expert-cache-dir", str(args.expert_cache_dir),
                "--rw-steps", str(args.rw_steps),
                "--rw-samples", str(args.rw_samples),
                "--rw-seed", str(args.rw_seed),
                "--reliability-components", *args.reliability_components,
                "--hidden-dim", str(args.hidden_dim),
                "--num-layers", str(args.num_layers),
                "--num-heads", str(args.num_heads),
                "--dropout", str(args.dropout),
                "--lr", str(args.lr),
                "--weight-decay", str(args.weight_decay),
                "--expert-epochs", str(args.expert_epochs),
                "--gate-epochs", str(args.gate_epochs),
                "--patience", str(args.patience),
                "--device", args.device,
            ]
            if alpha is not None:
                command.extend(["--fixed-alpha", str(alpha)])
            if not args.normalize_features:
                command.append("--no-normalize-features")
            if args.no_download:
                command.append("--no-download")
            print(f"[{step}/{total}] run {dataset}/{name}", flush=True)
            subprocess.run(command, cwd=root, check=True)


def analyze(args, out_dir, specs) -> None:
    rows = []
    names = [name for _, name, _ in specs]
    for dataset in args.datasets:
        for name in names:
            rows.extend(read_csv(out_dir / f"{dataset}_{name}.csv"))
    best_fixed_rows = select_best_fixed_alpha_by_val(rows)
    rows.extend(best_fixed_rows)
    if best_fixed_rows:
        names.append("best_fixed_alpha_by_val")
    summary = summarize(rows)
    comparisons = paired_comparisons(rows, args.datasets, names)
    write_csv(out_dir / "summary.csv", summary)
    write_csv(
        out_dir / "paired_comparisons.csv",
        comparisons,
        [
            "dataset", "comparison", "n", "mean_delta", "ci95_low", "ci95_high",
            "wins", "ties", "losses", "pvalue",
        ],
    )
    report = [
        "# Expert Fusion Preliminary Analysis",
        "",
        f"- Edge protocol: {args.edge_protocol}",
        f"- Runs: {args.runs}",
        f"- Models: {', '.join(names)}",
        "",
        "## Accuracy Summary",
        "",
        "| Dataset | Model | Accuracy | Macro-F1 | Std | Selected alpha |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in summary:
        report.append(
            f"| {row['dataset']} | {row['model']} | {row['test_acc_mean']:.4f} | "
            f"{row['macro_f1_mean']:.4f} | {row['test_acc_std']:.4f} | "
            f"{fmt_plain(row['selected_fixed_alpha'])} |"
        )
    report.extend(
        [
            "",
            "## Expert Complementarity",
            "",
            "| Dataset | Model | Local test | Global test | Local-only correct | Global-only correct | Global correct given local wrong |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary:
        if math.isnan(float(row["test_global_only_correct"])):
            continue
        report.append(
            f"| {row['dataset']} | {row['model']} | "
            f"{fmt_plain(row['local_expert_test_acc'])} | "
            f"{fmt_plain(row['global_expert_test_acc'])} | "
            f"{fmt_plain(row['test_local_only_correct'])} | "
            f"{fmt_plain(row['test_global_only_correct'])} | "
            f"{fmt_plain(row['test_global_correct_given_local_wrong'])} |"
        )
    report.extend(
        [
            "",
            "## Key Paired Comparisons",
            "",
            "| Dataset | Comparison | Delta | 95% CI | W/T/L | p |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in comparisons:
        report.append(
            f"| {row['dataset']} | {row['comparison']} | {row['mean_delta']:+.4f} | "
            f"[{fmt(row['ci95_low'])}, {fmt(row['ci95_high'])}] | "
            f"{row['wins']}/{row['ties']}/{row['losses']} | {fmt(row['pvalue'])} |"
        )
    (out_dir / "preliminary_analysis.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    print(f"analysis: {out_dir / 'preliminary_analysis.md'}")


def summarize(rows):
    groups = {}
    for row in rows:
        groups.setdefault((row["dataset"], row["model"]), []).append(row)
    output = []
    for (dataset, model), group in sorted(groups.items()):
        acc = [float(row["test_acc_at_best_val"]) for row in group]
        f1 = [float(row["test_macro_f1_at_best_val"]) for row in group]
        output.append(
            {
                "dataset": dataset,
                "model": model,
                "n": len(group),
                "test_acc_mean": statistics.mean(acc),
                "test_acc_std": statistics.pstdev(acc),
                "macro_f1_mean": statistics.mean(f1),
                "alpha_mean": finite_mean(group, "alpha_mean"),
                "alpha_corr_local_similarity": finite_mean(
                    group, "alpha_corr_local_similarity"
                ),
                "alpha_corr_label_homophily": finite_mean(
                    group, "alpha_corr_label_homophily"
                ),
                "local_logit_norm_mean": finite_mean(
                    group, "local_logit_norm_mean"
                ),
                "global_logit_norm_mean": finite_mean(
                    group, "global_logit_norm_mean"
                ),
                "local_expert_test_acc": finite_mean(
                    group, "local_expert_test_acc"
                ),
                "global_expert_test_acc": finite_mean(
                    group, "global_expert_test_acc"
                ),
                "test_local_only_correct": finite_mean(
                    group, "test_local_only_correct"
                ),
                "test_global_only_correct": finite_mean(
                    group, "test_global_only_correct"
                ),
                "test_global_correct_given_local_wrong": finite_mean(
                    group, "test_global_correct_given_local_wrong"
                ),
                "selected_fixed_alpha": finite_mean(group, "fixed_alpha"),
                "fallback_max_abs_error": finite_mean(
                    group, "fallback_max_abs_error"
                ),
            }
        )
    return output


def select_best_fixed_alpha_by_val(rows):
    fixed_rows = [
        row for row in rows if row["model"].startswith("fixed_alpha_")
    ]
    groups = {}
    for row in fixed_rows:
        key = (row["dataset"], int(row["split"]), int(row["seed"]))
        groups.setdefault(key, []).append(row)
    selected = []
    for group in groups.values():
        best = max(
            group,
            key=lambda row: (
                float(row["best_val_acc"]),
                -abs(float(row["fixed_alpha"]) - 0.5),
                -float(row["fixed_alpha"]),
            ),
        )
        derived = dict(best)
        derived["model"] = "best_fixed_alpha_by_val"
        derived["model_family"] = "best_fixed_alpha_by_val"
        selected.append(derived)
    return selected


def paired_comparisons(rows, datasets, names):
    pairs = []
    if "ordinary_gate" in names and "reliability_gate" in names:
        pairs.append(("reliability_gate", "ordinary_gate", "Reliability gate - ordinary gate"))
    if "best_fixed_alpha_by_val" in names:
        for model in ("ordinary_gate", "reliability_gate"):
            if model in names:
                pairs.append(
                    (
                        model,
                        "best_fixed_alpha_by_val",
                        f"{model} - validation-selected fixed alpha",
                    )
                )
    if "gcn_pyg" in names:
        if "fixed_alpha_000" in names and "global_only" in names:
            pairs.append(
                (
                    "fixed_alpha_000",
                    "global_only",
                    "alpha=0 fallback - global expert",
                )
            )
        if "fixed_alpha_100" in names:
            pairs.append(
                (
                    "fixed_alpha_100",
                    "gcn_pyg",
                    "alpha=1 fallback - GCN",
                )
            )
        for model in ("ordinary_gate", "reliability_gate"):
            if model in names:
                pairs.append((model, "gcn_pyg", f"{model} - GCN"))
    fixed = [name for name in names if name.startswith("fixed_alpha_")]
    for model in ("ordinary_gate", "reliability_gate"):
        if model in names:
            for baseline in fixed:
                pairs.append((model, baseline, f"{model} - {baseline}"))
    return [
        {
            "dataset": dataset,
            "comparison": label,
            **paired_stats(rows, dataset, left, right),
        }
        for dataset in datasets
        for left, right, label in pairs
    ]


def paired_stats(rows, dataset, left_model, right_model):
    left = keyed(rows, dataset, left_model)
    right = keyed(rows, dataset, right_model)
    keys = sorted(left.keys() & right.keys())
    if not keys:
        return empty_stats()
    differences = [left[key] - right[key] for key in keys]
    delta = statistics.mean(differences)
    half = ci95(differences)
    try:
        from scipy.stats import ttest_rel
        pvalue = float(
            ttest_rel(
                [left[key] for key in keys],
                [right[key] for key in keys],
            ).pvalue
        )
    except ImportError:
        pvalue = math.nan
    wins = sum(value > 0 for value in differences)
    ties = sum(value == 0 for value in differences)
    return {
        "n": len(keys),
        "mean_delta": delta,
        "ci95_low": delta - half,
        "ci95_high": delta + half,
        "wins": wins,
        "ties": ties,
        "losses": len(keys) - wins - ties,
        "pvalue": pvalue,
    }


def keyed(rows, dataset, model):
    return {
        (int(row["split"]), int(row["seed"])): float(row["test_acc_at_best_val"])
        for row in rows
        if row["dataset"] == dataset and row["model"] == model
    }


def ci95(values):
    if len(values) < 2:
        return math.nan
    se = statistics.stdev(values) / math.sqrt(len(values))
    try:
        from scipy.stats import t
        critical = float(t.ppf(0.975, len(values) - 1))
    except ImportError:
        critical = 1.96
    return critical * se


def finite_mean(rows, key):
    values = []
    for row in rows:
        try:
            value = float(row[key])
        except (KeyError, ValueError):
            continue
        if math.isfinite(value):
            values.append(value)
    return statistics.mean(values) if values else math.nan


def suite_config(args, root, specs, data_fingerprints):
    digest = hashlib.sha256()
    for relative in (
        "src/data.py",
        "src/models.py",
        "src/expert_models.py",
        "src/real_data.py",
        "run_expert_fusion.py",
        "run_expert_fusion_suite.py",
    ):
        digest.update((root / relative).read_bytes())
    return {
        "code_fingerprint": digest.hexdigest(),
        "datasets": args.datasets,
        "data_root": str(resolve(root, args.data_root)),
        "expert_cache_dir": str(args.expert_cache_dir),
        "data_fingerprints": data_fingerprints,
        "models": [name for _, name, _ in specs],
        "edge_protocol": args.edge_protocol,
        "runs": args.runs,
        "normalize_features": args.normalize_features,
        "rw_steps": args.rw_steps,
        "rw_samples": args.rw_samples,
        "rw_seed": args.rw_seed,
        "reliability_components": args.reliability_components,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "expert_epochs": args.expert_epochs,
        "gate_epochs": args.gate_epochs,
        "patience": args.patience,
        "device": args.device,
    }


def collect_data_fingerprints(args, data_root):
    fingerprints = {}
    for dataset in args.datasets:
        _, report = load_and_validate_dataset(
            dataset,
            data_root,
            allow_download=not args.no_download,
        )
        fingerprints[dataset] = validation_fingerprint(report)
    return fingerprints


def validate_or_write_config(out_dir, config, force):
    path = out_dir / "suite_config.json"
    if path.exists() and not force:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != config:
            raise RuntimeError("Output directory uses a different configuration")
    path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def result_complete(path, runs, dataset, model, edge_protocol):
    if not path.exists():
        return False
    rows = read_csv(path)
    required = {
        "dataset",
        "model",
        "edge_protocol",
        "split",
        "seed",
        "best_val_acc",
        "test_acc_at_best_val",
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
        "gate_epochs",
        "patience",
        "data_fingerprint",
        "preprocess_code_hash",
    }
    if len(rows) != runs or not rows or not required.issubset(rows[0]):
        return False
    if any(
        row["dataset"] != dataset
        or row["model"] != model
        or row["edge_protocol"] != edge_protocol
        for row in rows
    ):
        return False
    run_keys = {(int(row["split"]), int(row["seed"])) for row in rows}
    return len(run_keys) == runs


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fieldnames=None):
    with path.open("w", newline="", encoding="utf-8") as handle:
        if fieldnames is None:
            fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def empty_stats():
    return {
        "n": 0, "mean_delta": math.nan, "ci95_low": math.nan,
        "ci95_high": math.nan, "wins": 0, "ties": 0, "losses": 0,
        "pvalue": math.nan,
    }


def fmt(value):
    return "n/a" if math.isnan(float(value)) else f"{float(value):+.4f}"


def fmt_plain(value):
    return "n/a" if math.isnan(float(value)) else f"{float(value):.3f}"


def resolve(root, path):
    return path if path.is_absolute() else root / path


if __name__ == "__main__":
    main()
