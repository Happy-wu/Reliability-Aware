from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from src.data import RELIABILITY_COMPONENTS
from src.real_data import REAL_DATASETS


@dataclass(frozen=True)
class SuiteSpec:
    name: str
    datasets: tuple[str, ...]
    models: tuple[str, ...]
    fixed_alphas: tuple[float, ...]
    edge_protocol: str
    reliability_components: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run and summarize the complete expert-fusion validation matrix."
    )
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--profile",
        choices=["sanity", "full"],
        default="sanity",
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=REAL_DATASETS,
    )
    parser.add_argument(
        "--directed-datasets",
        nargs="+",
        choices=REAL_DATASETS,
        default=["Chameleon", "Squirrel", "Actor"],
    )
    parser.add_argument("--runs", type=int)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/expert_validation_matrix"),
    )
    parser.add_argument(
        "--include-directed",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--include-components",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--expert-epochs", type=int)
    parser.add_argument("--gate-epochs", type=int)
    parser.add_argument("--patience", type=int)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--analyze-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    apply_profile_defaults(args)
    root = Path(__file__).resolve().parent
    out_dir = resolve(root, args.out_dir)
    data_root = resolve(root, args.data_root)
    out_dir.mkdir(parents=True, exist_ok=True)
    shared_cache = out_dir / "_shared_expert_cache"
    specs = build_specs(args)
    write_matrix_config(args, out_dir, specs)

    if not args.analyze_only:
        for index, spec in enumerate(specs, start=1):
            command = build_command(
                args,
                root,
                data_root,
                out_dir,
                shared_cache,
                spec,
            )
            print(
                f"[suite {index}/{len(specs)}] {spec.name}: "
                f"{' '.join(command)}",
                flush=True,
            )
            if not args.dry_run:
                subprocess.run(command, cwd=root, check=True)

    if args.dry_run:
        return
    ensure_outputs(out_dir, specs)
    report_path = analyze_matrix(args, out_dir, specs)
    print(f"\nValidation matrix report: {report_path}")


def apply_profile_defaults(args) -> None:
    if args.profile == "sanity":
        args.datasets = args.datasets or ["Cora", "Chameleon", "Actor"]
        args.runs = args.runs or 3
        args.expert_epochs = args.expert_epochs or 100
        args.gate_epochs = args.gate_epochs or 80
        args.patience = args.patience or 30
        args.fixed_alphas = (0.0, 0.5, 1.0)
    else:
        args.datasets = args.datasets or list(REAL_DATASETS)
        args.runs = args.runs or 10
        args.expert_epochs = args.expert_epochs or 500
        args.gate_epochs = args.gate_epochs or 300
        args.patience = args.patience or 100
        args.fixed_alphas = (0.0, 0.25, 0.5, 0.75, 1.0)


def build_specs(args) -> list[SuiteSpec]:
    datasets = tuple(args.datasets)
    specs = [
        SuiteSpec(
            name="core_undirected",
            datasets=datasets,
            models=(
                "gcn_pyg",
                "global_only",
                "ordinary_gate",
                "reliability_gate",
            ),
            fixed_alphas=tuple(args.fixed_alphas),
            edge_protocol="undirected",
            reliability_components=tuple(RELIABILITY_COMPONENTS),
        )
    ]
    directed = tuple(
        dataset for dataset in args.directed_datasets if dataset in datasets
    )
    if args.include_directed and directed:
        for protocol in ("source_to_target", "target_to_source"):
            specs.append(
                SuiteSpec(
                    name=f"directed_{protocol}",
                    datasets=directed,
                    models=(
                        "gcn_pyg",
                        "global_only",
                        "ordinary_gate",
                        "reliability_gate",
                    ),
                    fixed_alphas=(0.0, 0.5, 1.0),
                    edge_protocol=protocol,
                    reliability_components=tuple(RELIABILITY_COMPONENTS),
                )
            )
    if args.include_components:
        for component in RELIABILITY_COMPONENTS:
            specs.append(
                SuiteSpec(
                    name=f"component_{component}",
                    datasets=datasets,
                    models=("reliability_gate",),
                    fixed_alphas=(),
                    edge_protocol="undirected",
                    reliability_components=(component,),
                )
            )
    return specs


def build_command(args, root, data_root, out_dir, shared_cache, spec):
    command = [
        args.python,
        str(root / "run_expert_fusion_suite.py"),
        "--datasets",
        *spec.datasets,
        "--models",
        *spec.models,
        "--fixed-alphas",
        *[str(alpha) for alpha in spec.fixed_alphas],
        "--edge-protocol",
        spec.edge_protocol,
        "--runs",
        str(args.runs),
        "--data-root",
        str(data_root),
        "--out-dir",
        str(out_dir / spec.name),
        "--expert-cache-dir",
        str(shared_cache),
        "--reliability-components",
        *spec.reliability_components,
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
        "--gate-epochs",
        str(args.gate_epochs),
        "--patience",
        str(args.patience),
        "--device",
        args.device,
    ]
    if args.no_download:
        command.append("--no-download")
    if args.force:
        command.append("--force")
    return command


def analyze_matrix(args, out_dir: Path, specs: list[SuiteSpec]) -> Path:
    core_dir = out_dir / "core_undirected"
    core_summary = index_summary(read_csv(core_dir / "summary.csv"))
    core_pairs = read_csv(core_dir / "paired_comparisons.csv")
    findings = []

    for dataset in args.datasets:
        findings.extend(fallback_findings(dataset, core_pairs))
        findings.append(
            comparison_finding(
                dataset,
                core_pairs,
                "ordinary_gate - validation-selected fixed alpha",
                "H2 ordinary gate beats validation-selected fixed alpha",
            )
        )
        findings.append(
            comparison_finding(
                dataset,
                core_pairs,
                "Reliability gate - ordinary gate",
                "H3 reliability adds value beyond ordinary gating",
            )
        )
        complementarity = core_summary.get((dataset, "ordinary_gate"), {})
        pool = as_float(complementarity.get("test_global_only_correct"))
        conditional = as_float(
            complementarity.get("test_global_correct_given_local_wrong")
        )
        findings.append(
            {
                "dataset": dataset,
                "claim": "H4 global expert provides complementary predictions",
                "status": complementarity_status(pool, conditional),
                "estimate": pool,
                "ci_low": math.nan,
                "ci_high": math.nan,
                "detail": (
                    f"global-only correct fraction={fmt(pool)}, "
                    f"P(global correct | local wrong)={fmt(conditional)}"
                ),
            }
        )

    protocol_summaries = {
        spec.edge_protocol: index_summary(
            read_csv(out_dir / spec.name / "summary.csv")
        )
        for spec in specs
        if spec.name.startswith("directed_")
    }
    if protocol_summaries:
        for dataset in args.directed_datasets:
            if dataset not in args.datasets:
                continue
            values = {
                "undirected": model_accuracy(core_summary, dataset, "gcn_pyg"),
                **{
                    protocol: model_accuracy(summary, dataset, "gcn_pyg")
                    for protocol, summary in protocol_summaries.items()
                },
            }
            finite = [value for value in values.values() if math.isfinite(value)]
            spread = max(finite) - min(finite) if finite else math.nan
            findings.append(
                {
                    "dataset": dataset,
                    "claim": "H5 GCN is sensitive to directed edge protocol",
                    "status": (
                        "SUPPORTED"
                        if math.isfinite(spread) and spread >= 0.02
                        else "NOT_SUPPORTED"
                    ),
                    "estimate": spread,
                    "ci_low": math.nan,
                    "ci_high": math.nan,
                    "detail": ", ".join(
                        f"{protocol}={fmt(value)}"
                        for protocol, value in values.items()
                    ),
                }
            )

    component_specs = [
        spec for spec in specs if spec.name.startswith("component_")
    ]
    if component_specs:
        component_rows = component_findings(
            args,
            out_dir,
            core_dir,
            component_specs,
        )
        findings.extend(component_rows)

    write_csv(out_dir / "validation_findings.csv", findings)
    report = render_report(args, specs, findings)
    path = out_dir / "validation_report.md"
    path.write_text(report, encoding="utf-8")
    return path


def fallback_findings(dataset, pairs):
    output = []
    for label, claim in (
        ("alpha=1 fallback - GCN", "H1 alpha=1 recovers GCN"),
        ("alpha=0 fallback - global expert", "H1 alpha=0 recovers global expert"),
    ):
        row = find_pair(pairs, dataset, label)
        if row is None:
            output.append(inconclusive(dataset, claim, "comparison missing"))
            continue
        delta = as_float(row["mean_delta"])
        output.append(
            {
                "dataset": dataset,
                "claim": claim,
                "status": "PASS" if abs(delta) <= 1e-7 else "FAIL",
                "estimate": delta,
                "ci_low": as_float(row["ci95_low"]),
                "ci_high": as_float(row["ci95_high"]),
                "detail": f"paired delta={fmt(delta)}",
            }
        )
    return output


def comparison_finding(dataset, pairs, label, claim):
    row = find_pair(pairs, dataset, label)
    if row is None:
        return inconclusive(dataset, claim, "comparison missing")
    delta = as_float(row["mean_delta"])
    low = as_float(row["ci95_low"])
    high = as_float(row["ci95_high"])
    if math.isfinite(low) and low > 0:
        status = "SUPPORTED"
    elif math.isfinite(high) and high < 0:
        status = "NOT_SUPPORTED"
    else:
        status = "INCONCLUSIVE"
    return {
        "dataset": dataset,
        "claim": claim,
        "status": status,
        "estimate": delta,
        "ci_low": low,
        "ci_high": high,
        "detail": f"delta={fmt(delta)}, CI=[{fmt(low)}, {fmt(high)}]",
    }


def component_findings(args, out_dir, core_dir, specs):
    output = []
    ordinary = load_model_rows(core_dir, args.datasets, "ordinary_gate")
    full = load_model_rows(core_dir, args.datasets, "reliability_gate")
    for spec in specs:
        component = spec.reliability_components[0]
        candidate = load_model_rows(
            out_dir / spec.name,
            args.datasets,
            "reliability_gate",
        )
        for dataset in args.datasets:
            for baseline, baseline_name in (
                (ordinary, "ordinary gate"),
                (full, "full reliability"),
            ):
                stats = paired_from_rows(
                    candidate,
                    baseline,
                    dataset,
                )
                output.append(
                    {
                        "dataset": dataset,
                        "claim": (
                            f"H6 {component} reliability vs {baseline_name}"
                        ),
                        "status": ci_status(stats),
                        "estimate": stats["mean_delta"],
                        "ci_low": stats["ci95_low"],
                        "ci_high": stats["ci95_high"],
                        "detail": (
                            f"delta={fmt(stats['mean_delta'])}, "
                            f"CI=[{fmt(stats['ci95_low'])}, "
                            f"{fmt(stats['ci95_high'])}]"
                        ),
                    }
                )
    return output


def paired_from_rows(left_rows, right_rows, dataset):
    left = keyed_values(left_rows, dataset)
    right = keyed_values(right_rows, dataset)
    keys = sorted(left.keys() & right.keys())
    if not keys:
        return {
            "mean_delta": math.nan,
            "ci95_low": math.nan,
            "ci95_high": math.nan,
        }
    differences = [left[key] - right[key] for key in keys]
    delta = statistics.mean(differences)
    half = ci95(differences)
    return {
        "mean_delta": delta,
        "ci95_low": delta - half,
        "ci95_high": delta + half,
    }


def render_report(args, specs, findings):
    lines = [
        "# Expert Fusion Validation Matrix",
        "",
        f"- Profile: {args.profile}",
        f"- Runs per model: {args.runs}",
        f"- Datasets: {', '.join(args.datasets)}",
        f"- Suites: {', '.join(spec.name for spec in specs)}",
        "",
        "## Claim Summary",
        "",
        "| Dataset | Claim | Status | Estimate | Detail |",
        "|---|---|---|---:|---|",
    ]
    for row in findings:
        lines.append(
            f"| {row['dataset']} | {row['claim']} | {row['status']} | "
            f"{fmt(row['estimate'])} | {row['detail']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation Rules",
            "",
            "- `PASS`: deterministic fallback difference is numerically zero.",
            "- `SUPPORTED`: paired 95% CI is entirely above zero.",
            "- `NOT_SUPPORTED`: paired 95% CI is entirely below zero.",
            "- `INCONCLUSIVE`: CI crosses zero or required output is missing.",
            "- Complementarity is marked supported when the global-only correct "
            "fraction is at least 1 percentage point or conditional correction "
            "is at least 10%.",
        ]
    )
    return "\n".join(lines) + "\n"


def complementarity_status(pool, conditional):
    if not math.isfinite(pool) and not math.isfinite(conditional):
        return "INCONCLUSIVE"
    return (
        "SUPPORTED"
        if (math.isfinite(pool) and pool >= 0.01)
        or (math.isfinite(conditional) and conditional >= 0.10)
        else "NOT_SUPPORTED"
    )


def ci_status(stats):
    low = stats["ci95_low"]
    high = stats["ci95_high"]
    if math.isfinite(low) and low > 0:
        return "SUPPORTED"
    if math.isfinite(high) and high < 0:
        return "NOT_SUPPORTED"
    return "INCONCLUSIVE"


def ensure_outputs(out_dir, specs):
    missing = [
        str(out_dir / spec.name / "summary.csv")
        for spec in specs
        if not (out_dir / spec.name / "summary.csv").exists()
    ]
    if missing:
        raise SystemExit("Missing suite summaries: " + ", ".join(missing))


def load_model_rows(directory, datasets, model):
    rows = []
    for dataset in datasets:
        path = directory / f"{dataset}_{model}.csv"
        if path.exists():
            rows.extend(read_csv(path))
    return rows


def keyed_values(rows, dataset):
    return {
        (int(row["split"]), int(row["seed"])): float(
            row["test_acc_at_best_val"]
        )
        for row in rows
        if row["dataset"] == dataset
    }


def index_summary(rows):
    return {(row["dataset"], row["model"]): row for row in rows}


def model_accuracy(summary, dataset, model):
    row = summary.get((dataset, model))
    return as_float(row["test_acc_mean"]) if row else math.nan


def find_pair(rows, dataset, comparison):
    return next(
        (
            row
            for row in rows
            if row["dataset"] == dataset
            and row["comparison"] == comparison
        ),
        None,
    )


def ci95(values):
    if len(values) < 2:
        return math.nan
    standard_error = statistics.stdev(values) / math.sqrt(len(values))
    try:
        from scipy.stats import t

        critical = float(t.ppf(0.975, len(values) - 1))
    except ImportError:
        critical = 1.96
    return critical * standard_error


def inconclusive(dataset, claim, detail):
    return {
        "dataset": dataset,
        "claim": claim,
        "status": "INCONCLUSIVE",
        "estimate": math.nan,
        "ci_low": math.nan,
        "ci_high": math.nan,
        "detail": detail,
    }


def write_matrix_config(args, out_dir, specs):
    payload = {
        "profile": args.profile,
        "datasets": args.datasets,
        "directed_datasets": args.directed_datasets,
        "runs": args.runs,
        "include_directed": args.include_directed,
        "include_components": args.include_components,
        "expert_epochs": args.expert_epochs,
        "gate_epochs": args.gate_epochs,
        "patience": args.patience,
        "suites": [
            {
                "name": spec.name,
                "datasets": spec.datasets,
                "models": spec.models,
                "fixed_alphas": spec.fixed_alphas,
                "edge_protocol": spec.edge_protocol,
                "reliability_components": spec.reliability_components,
            }
            for spec in specs
        ],
    }
    (out_dir / "validation_matrix_config.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def as_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def fmt(value):
    number = as_float(value)
    return "n/a" if not math.isfinite(number) else f"{number:+.4f}"


def resolve(root, path):
    return path if path.is_absolute() else root / path


if __name__ == "__main__":
    main()
