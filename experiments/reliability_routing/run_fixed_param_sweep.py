from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

from src.real_data import EDGE_PROTOCOLS, REAL_DATASETS


DEFAULT_SWEEP_CONFIGS = (
    "h64,l2,drop0.3,lr0.003,wd0.0001",
    "h128,l2,drop0.3,lr0.003,wd0.0001",
    "h256,l2,drop0.3,lr0.003,wd0.0001",
    "h128,l3,drop0.3,lr0.003,wd0.0001",
    "h256,l3,drop0.3,lr0.003,wd0.0001",
    "h256,l3,drop0.5,lr0.003,wd0.0001",
    "h256,l3,drop0.5,lr0.005,wd0.0001",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run fixed-only representation-control parameter sweeps."
    )
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=REAL_DATASETS,
        default=["OGBN-Arxiv"],
    )
    parser.add_argument(
        "--families",
        nargs="+",
        choices=(
            "hidden_mixing_frozen",
            "hidden_mixing_finetune",
            "iterative_relation_frozen",
            "iterative_relation_finetune",
            "gps_like_frozen",
            "gps_like_finetune",
        ),
        default=["iterative_relation_finetune"],
    )
    parser.add_argument(
        "--sweep-configs",
        nargs="+",
        default=list(DEFAULT_SWEEP_CONFIGS),
        help=(
            "Parameter configs like h128,l2,drop0.3,lr0.003,wd0.0001. "
            "Supported keys: h/hidden, l/layers, drop/dropout, lr, wd/weight_decay."
        ),
    )
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/fixed_param_sweep"),
    )
    parser.add_argument(
        "--edge-protocol",
        choices=EDGE_PROTOCOLS,
        default="undirected",
    )
    parser.add_argument("--rw-steps", type=int, default=8)
    parser.add_argument("--rw-samples", type=int, default=128)
    parser.add_argument("--rw-seed", type=int, default=0)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--expert-epochs", type=int, default=300)
    parser.add_argument("--control-epochs", type=int, default=200)
    parser.add_argument("--patience", type=int, default=60)
    parser.add_argument("--fixed-alphas", nargs="+", default=["0.0", "0.25", "0.5", "0.75", "1.0"])
    parser.add_argument("--max-adjustment", type=float, default=0.1)
    parser.add_argument("--lambda-init", type=float, default=0.001)
    parser.add_argument("--relation-steps", type=int, default=1)
    parser.add_argument("--reliability-encoder-mode", default="component_concat")
    parser.add_argument("--reliability-component-dim", type=int, default=32)
    parser.add_argument("--component-missing-mode", default="zero_slot")
    parser.add_argument("--alpha-type", default="channel")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--analyze-only", action="store_true")
    parser.add_argument("--no-download", action="store_true", default=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configs = [parse_sweep_config(value) for value in args.sweep_configs]
    root = Path(__file__).resolve().parent
    out_dir = resolve(root, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not args.analyze_only:
        total = len(args.datasets) * len(configs)
        step = 0
        for dataset in args.datasets:
            for config in configs:
                step += 1
                run_config(args, root, out_dir, step, total, dataset, config)

    rows = collect_summary(out_dir, args.datasets, configs)
    write_csv(out_dir / "sweep_summary.csv", rows)
    write_analysis(out_dir / "analysis.md", rows)
    print(f"summary: {out_dir / 'sweep_summary.csv'}", flush=True)
    print(f"analysis: {out_dir / 'analysis.md'}", flush=True)


def parse_sweep_config(text: str) -> dict[str, object]:
    output: dict[str, object] = {}
    for part in text.split(","):
        key, value = split_key_value(part.strip())
        if key in {"h", "hidden", "hidden_dim"}:
            output["hidden_dim"] = int(value)
        elif key in {"l", "layers", "num_layers"}:
            output["num_layers"] = int(value)
        elif key in {"drop", "dropout"}:
            output["dropout"] = float(value)
        elif key == "lr":
            output["lr"] = float(value)
        elif key in {"wd", "weight_decay"}:
            output["weight_decay"] = float(value)
        else:
            raise ValueError(f"Unknown sweep key in {text!r}: {key!r}")
    required = ("hidden_dim", "num_layers", "dropout", "lr", "weight_decay")
    missing = [key for key in required if key not in output]
    if missing:
        raise ValueError(f"Sweep config {text!r} is missing: {missing}")
    output["name"] = config_name(output)
    output["spec"] = text
    return output


def split_key_value(part: str) -> tuple[str, str]:
    if "=" in part:
        key, value = part.split("=", 1)
        return key.strip(), value.strip()
    prefixes = ("hidden_dim", "num_layers", "weight_decay", "hidden", "layers", "dropout", "drop", "lr", "wd", "h", "l")
    for prefix in sorted(prefixes, key=len, reverse=True):
        if part.startswith(prefix):
            return prefix, part[len(prefix) :]
    raise ValueError(f"Cannot parse sweep config part: {part!r}")


def config_name(config: dict[str, object]) -> str:
    return (
        f"h{config['hidden_dim']}_"
        f"l{config['num_layers']}_"
        f"drop{compact_float(config['dropout'])}_"
        f"lr{compact_float(config['lr'])}_"
        f"wd{compact_float(config['weight_decay'])}"
    )


def compact_float(value: object) -> str:
    text = f"{float(value):g}"
    return text.replace(".", "p").replace("-", "m")


def run_config(
    args: argparse.Namespace,
    root: Path,
    out_dir: Path,
    step: int,
    total: int,
    dataset: str,
    config: dict[str, object],
) -> None:
    config_out = out_dir / safe_name(dataset) / str(config["name"])
    command = [
        args.python,
        str(root / "run_representation_control_suite.py"),
        "--datasets",
        dataset,
        "--families",
        *args.families,
        "--controls",
        "fixed",
        "--edge-protocol",
        args.edge_protocol,
        "--runs",
        str(args.runs),
        "--data-root",
        str(resolve(root, args.data_root)),
        "--out-dir",
        str(config_out),
        "--reliability-components",
        "degree",
        "local_similarity",
        "neighbor_variance",
        "rwse",
        "--rw-steps",
        str(args.rw_steps),
        "--rw-samples",
        str(args.rw_samples),
        "--rw-seed",
        str(args.rw_seed),
        "--hidden-dim",
        str(config["hidden_dim"]),
        "--num-layers",
        str(config["num_layers"]),
        "--num-heads",
        str(args.num_heads),
        "--dropout",
        str(config["dropout"]),
        "--lr",
        str(config["lr"]),
        "--weight-decay",
        str(config["weight_decay"]),
        "--expert-epochs",
        str(args.expert_epochs),
        "--control-epochs",
        str(args.control_epochs),
        "--patience",
        str(args.patience),
        "--fixed-alphas",
        *args.fixed_alphas,
        "--max-adjustment",
        str(args.max_adjustment),
        "--lambda-init",
        str(args.lambda_init),
        "--relation-steps",
        str(args.relation_steps),
        "--reliability-encoder-mode",
        args.reliability_encoder_mode,
        "--reliability-component-dim",
        str(args.reliability_component_dim),
        "--component-missing-mode",
        args.component_missing_mode,
        "--alpha-type",
        args.alpha_type,
        "--device",
        args.device,
    ]
    if args.no_download:
        command.append("--no-download")
    if args.force:
        command.append("--force")

    print(
        f"[{step}/{total}] run dataset={dataset} config={config['name']} -> {config_out}",
        flush=True,
    )
    subprocess.run(command, cwd=root, check=True)


def collect_summary(
    out_dir: Path,
    datasets: list[str],
    configs: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for dataset in datasets:
        for config in configs:
            summary_path = out_dir / safe_name(dataset) / str(config["name"]) / "summary.csv"
            if not summary_path.is_file():
                rows.append(
                    {
                        "dataset": dataset,
                        "config": config["name"],
                        "status": "missing",
                        "family": "",
                        "test_primary_mean": "",
                        "test_primary_std": "",
                        "train_acc_mean": "",
                        "val_acc_mean": "",
                        "test_acc_mean": "",
                        "base_alpha_mean": "",
                        "sanity": "missing",
                        "best_for_dataset": "",
                        **config,
                    }
                )
                continue
            run_stats = load_run_stats(summary_path.parent, dataset)
            with summary_path.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    family = row["family"]
                    rows.append(
                        {
                            "dataset": dataset,
                            "config": config["name"],
                            "status": "ok",
                            "family": family,
                            "test_primary_mean": row["test_primary_mean"],
                            "test_primary_std": row["test_primary_std"],
                            "train_acc_mean": run_stats.get(family, {}).get("train_acc_mean", ""),
                            "val_acc_mean": run_stats.get(family, {}).get("val_acc_mean", ""),
                            "test_acc_mean": run_stats.get(family, {}).get("test_acc_mean", row["test_primary_mean"]),
                            "base_alpha_mean": row["base_alpha_mean"],
                            "sanity": sanity_label(float(row["test_primary_mean"])),
                            "best_for_dataset": "",
                            **config,
                        }
                    )
    mark_best(rows)
    return rows


def mark_best(rows: list[dict[str, object]]) -> None:
    datasets = sorted({str(row["dataset"]) for row in rows if row.get("status") == "ok"})
    for dataset in datasets:
        group = [
            row
            for row in rows
            if row.get("status") == "ok" and row["dataset"] == dataset
        ]
        best_value = max(float(row["test_primary_mean"]) for row in group)
        for row in group:
            if float(row["test_primary_mean"]) == best_value:
                row["best_for_dataset"] = "yes"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "dataset",
        "config",
        "status",
        "family",
        "test_primary_mean",
        "test_primary_std",
        "train_acc_mean",
        "val_acc_mean",
        "test_acc_mean",
        "base_alpha_mean",
        "sanity",
        "best_for_dataset",
        "hidden_dim",
        "num_layers",
        "dropout",
        "lr",
        "weight_decay",
        "name",
        "spec",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_analysis(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Fixed Parameter Sweep",
        "",
        "Fixed-only sweep for representation-control backbones.",
        "",
        "Sanity labels: `<60 = BAD`, `60-70 = usable`, `70-72 = good`, `>=72 = strong`.",
        "",
    ]
    datasets = sorted({str(row["dataset"]) for row in rows})
    for dataset in datasets:
        lines.extend(
            [
                f"## {dataset}",
                "",
                "| Config | Family | Train | Val | Test | Std | Base alpha | Sanity | Best |",
                "|---|---|---:|---:|---:|---:|---:|---|---|",
            ]
        )
        for row in [item for item in rows if item["dataset"] == dataset]:
            if row.get("status") != "ok":
                lines.append(f"| {row['config']} | missing | n/a | n/a | n/a | |")
                continue
            lines.append(
                "| "
                f"{row['config']} | "
                f"{row['family']} | "
                f"{percent_or_na(row['train_acc_mean'])} | "
                f"{percent_or_na(row['val_acc_mean'])} | "
                f"{percent(row['test_primary_mean'])} | "
                f"{percent(row['test_primary_std'])} | "
                f"{float(row['base_alpha_mean']):.2f} | "
                f"{row['sanity']} | "
                f"{row['best_for_dataset']} |"
            )
        best_rows = [
            item
            for item in rows
            if item["dataset"] == dataset and item.get("best_for_dataset") == "yes"
        ]
        if best_rows:
            lines.extend(["", "Best:", ""])
            for best in best_rows:
                lines.append(
                    (
                        f"- {best['config']} / {best['family']}: "
                        f"{percent(best['test_primary_mean'])} ({best['sanity']})."
                    )
                )
            lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def load_run_stats(config_dir: Path, dataset: str) -> dict[str, dict[str, object]]:
    output: dict[str, dict[str, object]] = {}
    for path in config_dir.glob(f"{dataset}_*_fixed.csv"):
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            continue
        family = rows[0].get("family", "")
        output[family] = {
            "train_acc_mean": mean_from_rows(rows, "best_train_acc"),
            "val_acc_mean": mean_from_rows(rows, "best_val_acc"),
            "test_acc_mean": mean_from_rows(rows, "test_acc_at_best_val"),
        }
    return output


def mean_from_rows(rows: list[dict[str, str]], key: str) -> object:
    values = [
        float(row[key])
        for row in rows
        if key in row and row[key] not in {"", "nan", "NaN"}
    ]
    if not values:
        return ""
    return sum(values) / len(values)


def sanity_label(value: float) -> str:
    if value < 0.60:
        return "BAD"
    if value < 0.70:
        return "usable"
    if value < 0.72:
        return "good"
    return "strong"


def safe_name(value: str) -> str:
    return value.replace("/", "_").replace(" ", "_")


def percent(value: object) -> str:
    return f"{float(value) * 100:.2f}"


def percent_or_na(value: object) -> str:
    if value in {"", None}:
        return "n/a"
    return percent(value)


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


if __name__ == "__main__":
    main()
