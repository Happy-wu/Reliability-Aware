from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import statistics
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


GRAPHS = ("heterophily", "homophily", "noisy")
SUITE_SCHEMA_VERSION = 2


@dataclass(frozen=True)
class ExperimentSpec:
    tag: str
    models: tuple[str, ...]
    components: tuple[str, ...]
    label: str
    family: str


EXPERIMENTS = (
    ExperimentSpec(
        tag="reliability_encoder_compare",
        models=(
            "gate_gt",
            "gate_gt_encoded",
            "qk_gt",
            "qk_gt_encoded",
            "reliability_gt",
            "reliability_gt_encoded",
        ),
        components=("degree", "local_similarity", "neighbor_variance", "rwse"),
        label="Separate heads vs branch-specific encoders",
        family="encoder",
    ),
    ExperimentSpec(
        tag="rel_only_degree",
        models=("gate_gt", "reliability_gt"),
        components=("degree",),
        label="Only degree",
        family="only",
    ),
    ExperimentSpec(
        tag="rel_only_local_sim",
        models=("gate_gt", "reliability_gt"),
        components=("local_similarity",),
        label="Only local similarity",
        family="only",
    ),
    ExperimentSpec(
        tag="rel_only_neighbor_var",
        models=("gate_gt", "reliability_gt"),
        components=("neighbor_variance",),
        label="Only neighbor variance",
        family="only",
    ),
    ExperimentSpec(
        tag="rel_only_rwse",
        models=("gate_gt", "reliability_gt"),
        components=("rwse",),
        label="Only RWSE",
        family="only",
    ),
    ExperimentSpec(
        tag="rel_without_degree",
        models=("gate_gt", "reliability_gt"),
        components=("local_similarity", "neighbor_variance", "rwse"),
        label="Without degree",
        family="without",
    ),
    ExperimentSpec(
        tag="rel_without_local_sim",
        models=("gate_gt", "reliability_gt"),
        components=("degree", "neighbor_variance", "rwse"),
        label="Without local similarity",
        family="without",
    ),
    ExperimentSpec(
        tag="rel_without_neighbor_var",
        models=("gate_gt", "reliability_gt"),
        components=("degree", "local_similarity", "rwse"),
        label="Without neighbor variance",
        family="without",
    ),
    ExperimentSpec(
        tag="rel_without_rwse",
        models=("gate_gt", "reliability_gt"),
        components=("degree", "local_similarity", "neighbor_variance"),
        label="Without RWSE",
        family="without",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the nine reliability experiments and generate preliminary analysis."
    )
    parser.add_argument("--python", default=sys.executable, help="Python executable used to run run_batch.py")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--cuda-visible-devices", default=None)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(10)))
    parser.add_argument("--graph-types", nargs="+", choices=GRAPHS, default=list(GRAPHS))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--analysis-dir", type=Path, default=None)
    parser.add_argument("--num-nodes", type=int, default=900)
    parser.add_argument("--num-classes", type=int, default=3)
    parser.add_argument("--feature-dim", type=int, default=32)
    parser.add_argument("--feature-noise", type=float, default=0.7)
    parser.add_argument("--edge-noise", type=float, default=0.0)
    parser.add_argument("--rw-steps", type=int, default=4)
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
    parser.add_argument("--force", action="store_true", help="Re-run completed experiments")
    parser.add_argument("--analyze-only", action="store_true", help="Skip training and analyze existing outputs")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = ROOT
    args.code_fingerprint = compute_code_fingerprint(root)
    args.out_dir = resolve_from_root(root, args.out_dir)
    args.analysis_dir = resolve_from_root(
        root,
        args.analysis_dir or args.out_dir / "reliability_suite_analysis",
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.analysis_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    if args.cuda_visible_devices is not None:
        env["CUDA_VISIBLE_DEVICES"] = args.cuda_visible_devices

    write_manifest(args)
    if not args.analyze_only:
        run_suite(args, root, env)

    missing = missing_outputs(args)
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"Cannot analyze: missing or incomplete outputs for {joined}")

    report_path = analyze_suite(args)
    print(f"\nAnalysis complete: {report_path}")


def resolve_from_root(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def compute_code_fingerprint(root: Path) -> str:
    paths = (
        root / "src" / "data.py",
        root / "src" / "models.py",
        Path(__file__).resolve().parent / "run_synthetic.py",
        Path(__file__).resolve().parent / "run_batch.py",
        Path(__file__).resolve(),
    )
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def write_manifest(args: argparse.Namespace) -> None:
    manifest = {
        "suite_schema_version": SUITE_SCHEMA_VERSION,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "command_args": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in vars(args).items()
        },
        "experiments": [asdict(spec) for spec in EXPERIMENTS],
    }
    path = args.analysis_dir / "suite_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def run_suite(args: argparse.Namespace, root: Path, env: dict[str, str]) -> None:
    for index, spec in enumerate(EXPERIMENTS, start=1):
        batch_dir = args.out_dir / f"batch_{spec.tag}"
        expected_rows = len(args.graph_types) * len(spec.models) * len(args.seeds)
        expected_config = experiment_config(args, spec)
        if not args.force and is_complete(batch_dir, expected_rows, expected_config):
            print(f"[{index}/9] skip completed: {spec.tag}", flush=True)
            continue

        command = build_command(args, root, spec)
        print(f"\n[{index}/9] {spec.label}", flush=True)
        print(format_command(command), flush=True)
        subprocess.run(command, cwd=root, env=env, check=True)
        write_batch_config(batch_dir, expected_config)


def build_command(args: argparse.Namespace, root: Path, spec: ExperimentSpec) -> list[str]:
    command = [
        args.python,
        str(Path(__file__).resolve().parent / "run_batch.py"),
        "--models",
        *spec.models,
        "--graph-types",
        *args.graph_types,
        "--seeds",
        *(str(seed) for seed in args.seeds),
        "--tag",
        spec.tag,
        "--reliability-components",
        *spec.components,
        "--num-nodes",
        str(args.num_nodes),
        "--num-classes",
        str(args.num_classes),
        "--feature-dim",
        str(args.feature_dim),
        "--feature-noise",
        str(args.feature_noise),
        "--edge-noise",
        str(args.edge_noise),
        "--rw-steps",
        str(args.rw_steps),
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
        "--out-dir",
        str(args.out_dir),
    ]
    if args.fixed_qk_strength is not None:
        command.extend(["--fixed-qk-strength", str(args.fixed_qk_strength)])
    if args.verbose:
        command.append("--verbose")
    return command


def format_command(command: list[str]) -> str:
    return " ".join(quote_argument(arg) for arg in command)


def quote_argument(argument: str) -> str:
    if not argument or any(char.isspace() for char in argument):
        return json.dumps(argument)
    return argument


def experiment_config(args: argparse.Namespace, spec: ExperimentSpec) -> dict[str, object]:
    return {
        "suite_schema_version": SUITE_SCHEMA_VERSION,
        "code_fingerprint": args.code_fingerprint,
        "tag": spec.tag,
        "models": list(spec.models),
        "components": list(spec.components),
        "graph_types": list(args.graph_types),
        "seeds": list(args.seeds),
        "device": args.device,
        "num_nodes": args.num_nodes,
        "num_classes": args.num_classes,
        "feature_dim": args.feature_dim,
        "feature_noise": args.feature_noise,
        "edge_noise": args.edge_noise,
        "rw_steps": args.rw_steps,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "qk_strength_init": args.qk_strength_init,
        "fixed_qk_strength": args.fixed_qk_strength,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "epochs": args.epochs,
        "patience": args.patience,
    }


def write_batch_config(batch_dir: Path, config: dict[str, object]) -> None:
    path = batch_dir / "suite_config.json"
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def is_complete(
    batch_dir: Path,
    expected_rows: int,
    expected_config: dict[str, object],
) -> bool:
    raw_path = batch_dir / "raw_results.csv"
    summary_path = batch_dir / "summary.csv"
    config_path = batch_dir / "suite_config.json"
    if not raw_path.exists() or not summary_path.exists() or not config_path.exists():
        return False
    try:
        actual_config = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    if actual_config != expected_config:
        return False
    return len(read_csv(raw_path)) == expected_rows


def missing_outputs(args: argparse.Namespace) -> list[str]:
    missing = []
    for spec in EXPERIMENTS:
        batch_dir = args.out_dir / f"batch_{spec.tag}"
        expected_rows = len(args.graph_types) * len(spec.models) * len(args.seeds)
        if not is_complete(
            batch_dir,
            expected_rows,
            experiment_config(args, spec),
        ):
            missing.append(spec.tag)
    return missing


def analyze_suite(args: argparse.Namespace) -> Path:
    rows_by_tag = {
        spec.tag: read_csv(args.out_dir / f"batch_{spec.tag}" / "raw_results.csv")
        for spec in EXPERIMENTS
    }
    full_rows = rows_by_tag["reliability_encoder_compare"]

    paired_rows = analyze_encoder_comparisons(full_rows, args.graph_types)
    component_rows = analyze_components(rows_by_tag, full_rows, args.graph_types)

    write_csv(args.analysis_dir / "encoder_paired_comparisons.csv", paired_rows)
    write_csv(args.analysis_dir / "component_ablation_summary.csv", component_rows)

    report = build_report(args, paired_rows, component_rows, full_rows)
    report_path = args.analysis_dir / "preliminary_analysis.md"
    report_path.write_text(report, encoding="utf-8")
    return report_path


def analyze_encoder_comparisons(
    rows: list[dict[str, str]],
    graph_types: list[str],
) -> list[dict[str, object]]:
    comparisons = (
        ("gate_gt_encoded", "gate_gt", "gate encoded - static"),
        ("qk_gt_encoded", "qk_gt", "qk encoded - static"),
        ("reliability_gt_encoded", "reliability_gt", "reliability encoded - static"),
        ("reliability_gt", "gate_gt", "static reliability - static gate"),
        ("reliability_gt_encoded", "gate_gt_encoded", "encoded reliability - encoded gate"),
    )
    results = []
    for graph in graph_types:
        for left, right, label in comparisons:
            stats = paired_comparison(rows, graph, left, rows, right)
            results.append(
                {
                    "graph_type": graph,
                    "comparison": label,
                    "left_model": left,
                    "right_model": right,
                    **stats,
                }
            )
    return results


def analyze_components(
    rows_by_tag: dict[str, list[dict[str, str]]],
    full_rows: list[dict[str, str]],
    graph_types: list[str],
) -> list[dict[str, object]]:
    results = []
    for spec in EXPERIMENTS[1:]:
        rows = rows_by_tag[spec.tag]
        for graph in graph_types:
            for model in ("gate_gt", "reliability_gt"):
                stats = paired_comparison(rows, graph, model, full_rows, model)
                results.append(
                    {
                        "tag": spec.tag,
                        "family": spec.family,
                        "label": spec.label,
                        "components": ",".join(spec.components),
                        "graph_type": graph,
                        "model": model,
                        **stats,
                    }
                )
    return results


def paired_comparison(
    left_rows: list[dict[str, str]],
    graph: str,
    left_model: str,
    right_rows: list[dict[str, str]],
    right_model: str,
) -> dict[str, object]:
    left = rows_by_seed(left_rows, graph, left_model)
    right = rows_by_seed(right_rows, graph, right_model)
    seeds = sorted(set(left).intersection(right))
    left_values = [left[seed] for seed in seeds]
    right_values = [right[seed] for seed in seeds]
    differences = [a - b for a, b in zip(left_values, right_values)]

    n = len(differences)
    mean_delta = statistics.mean(differences) if differences else math.nan
    std_delta = statistics.stdev(differences) if n > 1 else 0.0 if n == 1 else math.nan
    ci_half = confidence_interval_half_width(differences)
    p_value = paired_ttest_pvalue(left_values, right_values)
    wins = sum(delta > 0 for delta in differences)
    ties = sum(delta == 0 for delta in differences)

    return {
        "n": n,
        "left_mean": safe_mean(left_values),
        "right_mean": safe_mean(right_values),
        "mean_delta": mean_delta,
        "std_delta": std_delta,
        "ci95_low": mean_delta - ci_half if differences else math.nan,
        "ci95_high": mean_delta + ci_half if differences else math.nan,
        "wins": wins,
        "ties": ties,
        "losses": n - wins - ties,
        "paired_t_pvalue": p_value,
    }


def rows_by_seed(
    rows: list[dict[str, str]],
    graph: str,
    model: str,
) -> dict[int, float]:
    return {
        int(row["seed"]): float(row["test_acc_at_best_val"])
        for row in rows
        if row["graph_type"] == graph and row["model"] == model
    }


def confidence_interval_half_width(values: list[float]) -> float:
    n = len(values)
    if n < 2:
        return math.nan
    standard_error = statistics.stdev(values) / math.sqrt(n)
    return t_critical_975(n - 1) * standard_error


def t_critical_975(df: int) -> float:
    try:
        from scipy.stats import t

        return float(t.ppf(0.975, df))
    except ImportError:
        table = {
            1: 12.706,
            2: 4.303,
            3: 3.182,
            4: 2.776,
            5: 2.571,
            6: 2.447,
            7: 2.365,
            8: 2.306,
            9: 2.262,
            10: 2.228,
            11: 2.201,
            12: 2.179,
            13: 2.160,
            14: 2.145,
            15: 2.131,
            16: 2.120,
            17: 2.110,
            18: 2.101,
            19: 2.093,
            20: 2.086,
            25: 2.060,
            30: 2.042,
        }
        eligible = [key for key in table if key >= df]
        return table[min(eligible)] if eligible else 1.96


def paired_ttest_pvalue(left: list[float], right: list[float]) -> float:
    if len(left) < 2:
        return math.nan
    try:
        from scipy.stats import ttest_rel

        return float(ttest_rel(left, right).pvalue)
    except ImportError:
        return math.nan


def build_report(
    args: argparse.Namespace,
    paired_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    full_rows: list[dict[str, str]],
) -> str:
    lines = [
        "# Reliability Suite Preliminary Analysis",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Seeds: {', '.join(str(seed) for seed in args.seeds)}",
        f"- Graphs: {', '.join(args.graph_types)}",
        f"- Device: {args.device}",
        "- Delta definition: left model minus right/baseline model using matched seeds.",
        "- A 95% CI excluding zero is treated as preliminary evidence, not a final claim.",
        "",
        "## Branch-Specific Encoder Comparisons",
        "",
        "| Graph | Comparison | Left | Right | Delta | 95% CI | W/T/L | p |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in paired_rows:
        lines.append(
            f"| {row['graph_type']} | {row['comparison']} | "
            f"{format_number(row['left_mean'])} | {format_number(row['right_mean'])} | "
            f"{format_signed(row['mean_delta'])} | "
            f"[{format_signed(row['ci95_low'])}, {format_signed(row['ci95_high'])}] | "
            f"{row['wins']}/{row['ties']}/{row['losses']} | "
            f"{format_pvalue(row['paired_t_pvalue'])} |"
        )

    lines.extend(
        [
            "",
            "## Component Ablation",
            "",
            "Each row is compared with the same static model using the full reliability basis "
            "from `batch_reliability_encoder_compare`.",
            "Local similarity and neighbor variance are gate-only components; when selected "
            "alone, the Q/K reliability input is zero.",
            "",
        ]
    )
    for graph in args.graph_types:
        for model in ("gate_gt", "reliability_gt"):
            subset = [
                row
                for row in component_rows
                if row["graph_type"] == graph and row["model"] == model
            ]
            subset.sort(key=lambda row: float(row["mean_delta"]), reverse=True)
            lines.extend(
                [
                    f"### {graph} / {model}",
                    "",
                    "| Ablation | Mean | Delta vs full | 95% CI | W/T/L | p |",
                    "|---|---:|---:|---:|---:|---:|",
                ]
            )
            for row in subset:
                lines.append(
                    f"| {row['label']} | {format_number(row['left_mean'])} | "
                    f"{format_signed(row['mean_delta'])} | "
                    f"[{format_signed(row['ci95_low'])}, {format_signed(row['ci95_high'])}] | "
                    f"{row['wins']}/{row['ties']}/{row['losses']} | "
                    f"{format_pvalue(row['paired_t_pvalue'])} |"
                )
            lines.append("")

    lines.extend(build_preliminary_findings(paired_rows, component_rows, full_rows, args.graph_types))
    return "\n".join(lines) + "\n"


def build_preliminary_findings(
    paired_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    full_rows: list[dict[str, str]],
    graph_types: list[str],
) -> list[str]:
    lines = ["## Automatic Preliminary Findings", ""]

    encoder_rows = [
        row for row in paired_rows if "encoded - static" in str(row["comparison"])
    ]
    positive = [
        row
        for row in encoder_rows
        if int(row["n"]) >= 2 and float(row["ci95_low"]) > 0
    ]
    negative = [
        row
        for row in encoder_rows
        if int(row["n"]) >= 2 and float(row["ci95_high"]) < 0
    ]
    if positive:
        labels = ", ".join(
            f"{row['graph_type']} {row['left_model']} ({format_signed(row['mean_delta'])})"
            for row in positive
        )
        lines.append(
            f"- Branch-specific encoders show positive paired evidence for: {labels}."
        )
    if negative:
        labels = ", ".join(
            f"{row['graph_type']} {row['left_model']} ({format_signed(row['mean_delta'])})"
            for row in negative
        )
        lines.append(
            f"- Branch-specific encoders show negative paired evidence for: {labels}."
        )
    if not positive and not negative:
        lines.append(
            "- No branch-specific encoder comparison has a 95% CI excluding zero."
        )

    for graph in graph_types:
        for model in ("gate_gt", "reliability_gt"):
            only_rows = [
                row
                for row in component_rows
                if row["graph_type"] == graph
                and row["model"] == model
                and row["family"] == "only"
            ]
            if only_rows:
                best = max(only_rows, key=lambda row: float(row["left_mean"]))
                lines.append(
                    f"- Best single component for {graph}/{model}: {best['label']} "
                    f"(mean={format_number(best['left_mean'])}, "
                    f"delta vs full={format_signed(best['mean_delta'])})."
                )

    gamma_lines = summarize_gamma(full_rows, graph_types)
    lines.extend(gamma_lines)
    lines.extend(
        [
            "- Component batches are compared with a baseline trained in a separate run. "
            "Use the paired deltas as screening evidence and re-run finalists in one combined batch.",
            "- Multiple comparisons are exploratory; p-values are uncorrected.",
        ]
    )
    return lines


def summarize_gamma(
    rows: list[dict[str, str]],
    graph_types: list[str],
) -> list[str]:
    lines = []
    for graph in graph_types:
        for model in ("qk_gt", "qk_gt_encoded", "reliability_gt", "reliability_gt_encoded"):
            selected = [
                row for row in rows if row["graph_type"] == graph and row["model"] == model
            ]
            values = [
                float(row["qk_gamma_q_abs_dev_mean"])
                for row in selected
                if not math.isnan(float(row["qk_gamma_q_abs_dev_mean"]))
            ]
            if values:
                lines.append(
                    f"- Gamma Q mean absolute deviation for {graph}/{model}: "
                    f"{statistics.mean(values):.6f}."
                )
    return lines


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def safe_mean(values: list[float]) -> float:
    return statistics.mean(values) if values else math.nan


def format_number(value: object) -> str:
    number = float(value)
    return "nan" if math.isnan(number) else f"{number:.4f}"


def format_signed(value: object) -> str:
    number = float(value)
    return "nan" if math.isnan(number) else f"{number:+.4f}"


def format_pvalue(value: object) -> str:
    number = float(value)
    if math.isnan(number):
        return "n/a"
    return "<0.0001" if number < 0.0001 else f"{number:.4f}"


if __name__ == "__main__":
    main()
