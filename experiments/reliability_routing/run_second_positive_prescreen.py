from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_DATASETS = (
    "Roman-empire",
    "Amazon-ratings",
    "Questions",
)
RELIABILITY_COMPONENTS = (
    "degree",
    "local_similarity",
    "neighbor_variance",
    "rwse",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the lightweight second-positive prescreen: dataset validation, "
            "preference routing, expert headroom, and a candidate decision report."
        )
    )
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=list(DEFAULT_DATASETS),
    )
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/second_positive_prescreen_v1"),
    )
    parser.add_argument("--edge-protocol", default="undirected")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--oof-folds", type=int, default=3)
    parser.add_argument("--rw-steps", type=int, default=8)
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
    parser.add_argument("--expert-epochs", type=int, default=100)
    parser.add_argument("--router-epochs", type=int, default=100)
    parser.add_argument("--patience", type=int, default=30)
    parser.add_argument(
        "--fixed-alphas",
        nargs="+",
        type=float,
        default=[0.0, 0.25, 0.5, 0.75, 1.0],
    )
    parser.add_argument("--oracle-gap-threshold", type=float, default=0.01)
    parser.add_argument("--reliability-auc-threshold", type=float, default=0.58)
    parser.add_argument("--combined-auc-threshold", type=float, default=0.58)
    parser.add_argument("--combined-over-feature-threshold", type=float, default=0.01)
    parser.add_argument("--min-preference-nodes", type=int, default=200)
    parser.add_argument("--auc-std-threshold", type=float, default=0.05)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--skip-run",
        action="store_true",
        help="Only rebuild the decision report from existing outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    out_dir = resolve(root, args.out_dir)
    data_root = resolve(root, args.data_root)
    preference_dir = out_dir / "preference"
    headroom_dir = out_dir / "headroom"
    expert_cache = out_dir / f"_expert_cache_{cache_tag(args)}"
    out_dir.mkdir(parents=True, exist_ok=True)
    config_path = out_dir / "prescreen_config.json"

    if not args.skip_run:
        validate_or_write_config(config_path, prescreen_config(args), args.force)
        cleanup_for_force(args, preference_dir, headroom_dir, expert_cache)
        validate_datasets(args, root, data_root, out_dir)
        run_preference_suite(args, root, data_root, preference_dir, expert_cache)
        run_headroom_diagnosis(args, root, data_root, preference_dir, headroom_dir, expert_cache)
    else:
        validate_skip_run(config_path, prescreen_config(args), headroom_dir / "dataset_summary.csv")

    summary_path = headroom_dir / "dataset_summary.csv"
    require_summary(summary_path)
    write_decision_report(
        args,
        summary_path,
        out_dir / "candidate_decision.md",
    )
    print(f"decision: {out_dir / 'candidate_decision.md'}", flush=True)


def resolve(root: Path, path: Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else root / path


def cache_tag(args: argparse.Namespace) -> str:
    dropout = str(args.dropout).replace(".", "p")
    lr = str(args.lr).replace(".", "p")
    wd = str(args.weight_decay).replace(".", "p")
    alphas = "-".join(str(alpha).replace(".", "p") for alpha in args.fixed_alphas)
    return (
        f"{args.edge_protocol}_h{args.hidden_dim}_l{args.num_layers}_"
        f"heads{args.num_heads}_drop{dropout}_lr{lr}_wd{wd}_rw{args.rw_steps}_"
        f"samples{args.rw_samples}_folds{args.oof_folds}_"
        f"ee{args.expert_epochs}_re{args.router_epochs}_pat{args.patience}_"
        f"alpha{alphas}"
    )


def prescreen_config(args: argparse.Namespace) -> dict[str, object]:
    return {
        "datasets": list(args.datasets),
        "edge_protocol": args.edge_protocol,
        "runs": args.runs,
        "oof_folds": args.oof_folds,
        "rw_steps": args.rw_steps,
        "rw_samples": args.rw_samples,
        "rw_seed": args.rw_seed,
        "reliability_components": list(args.reliability_components),
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "expert_epochs": args.expert_epochs,
        "router_epochs": args.router_epochs,
        "patience": args.patience,
        "fixed_alphas": list(args.fixed_alphas),
        "oracle_gap_threshold": args.oracle_gap_threshold,
        "reliability_auc_threshold": args.reliability_auc_threshold,
        "combined_auc_threshold": args.combined_auc_threshold,
        "combined_over_feature_threshold": args.combined_over_feature_threshold,
        "min_preference_nodes": args.min_preference_nodes,
        "auc_std_threshold": args.auc_std_threshold,
    }


def validate_or_write_config(path: Path, config: dict[str, object], force: bool) -> None:
    if path.exists() and not force:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != config:
            raise RuntimeError(
                "Output directory uses a different prescreen configuration; "
                "choose another --out-dir or pass --force."
            )
        return
    path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_skip_run(
    config_path: Path,
    config: dict[str, object],
    summary_path: Path,
) -> None:
    if not summary_path.exists():
        raise FileNotFoundError(
            f"Missing {summary_path}. Run without --skip-run first."
        )
    if not config_path.exists():
        raise FileNotFoundError(
            f"Missing {config_path}. Cannot verify --skip-run configuration."
        )
    existing = json.loads(config_path.read_text(encoding="utf-8"))
    if existing != config:
        raise RuntimeError(
            "--skip-run configuration does not match prescreen_config.json; "
            "use the original arguments or choose another --out-dir."
        )


def cleanup_for_force(
    args: argparse.Namespace,
    preference_dir: Path,
    headroom_dir: Path,
    expert_cache: Path,
) -> None:
    if not args.force:
        return
    for path in (preference_dir, headroom_dir, expert_cache):
        if path.exists():
            shutil.rmtree(path)


def require_summary(summary_path: Path) -> None:
    if not summary_path.exists():
        raise FileNotFoundError(
            f"Missing {summary_path}; run_expert_headroom_diagnosis.py did not "
            "produce dataset_summary.csv."
        )


def run(command: list[str], root: Path) -> None:
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=root, check=True)


def validate_datasets(args: argparse.Namespace, root: Path, data_root: Path, out_dir: Path) -> None:
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
    run(command, root)


def run_preference_suite(
    args: argparse.Namespace,
    root: Path,
    data_root: Path,
    preference_dir: Path,
    expert_cache: Path,
) -> None:
    command = [
        args.python,
        str(root / "run_preference_routing_suite.py"),
        "--datasets",
        *args.datasets,
        "--routers",
        "reliability_only",
        "node_feature_only",
        "combined",
        "--edge-protocol",
        args.edge_protocol,
        "--runs",
        str(args.runs),
        "--oof-folds",
        str(args.oof_folds),
        "--data-root",
        str(data_root),
        "--out-dir",
        str(preference_dir),
        "--expert-cache-dir",
        str(expert_cache),
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
        "--fixed-alphas",
        *[str(alpha) for alpha in args.fixed_alphas],
        "--utility-epsilon-nodes",
        "1",
        "--device",
        args.device,
    ]
    if args.no_download:
        command.append("--no-download")
    if args.force:
        command.append("--force")
    run(command, root)


def run_headroom_diagnosis(
    args: argparse.Namespace,
    root: Path,
    data_root: Path,
    preference_dir: Path,
    headroom_dir: Path,
    expert_cache: Path,
) -> None:
    command = [
        args.python,
        str(root / "run_expert_headroom_diagnosis.py"),
        "--datasets",
        *args.datasets,
        "--preference-dir",
        str(preference_dir),
        "--expert-cache-dir",
        str(expert_cache),
        "--data-root",
        str(data_root),
        "--edge-protocol",
        args.edge_protocol,
        "--out-dir",
        str(headroom_dir),
        "--device",
        args.device,
    ]
    if args.no_download:
        command.append("--no-download")
    run(command, root)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def to_float(value: object) -> float:
    if value is None:
        return math.nan
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def fmt(value: float) -> str:
    return "" if math.isnan(value) else f"{value:.4f}"


def verdict(args: argparse.Namespace, row: dict[str, str]) -> tuple[str, str]:
    oracle_gap = to_float(row.get("oracle_union_minus_best_fixed_mean"))
    rel_auc = to_float(row.get("reliability_preference_auc_mean"))
    feat_auc = to_float(row.get("feature_preference_auc_mean"))
    comb_auc = to_float(row.get("combined_preference_auc_mean"))
    pref_count = to_float(row.get("preference_count_mean"))
    rel_auc_std = to_float(row.get("reliability_preference_auc_std"))
    comb_auc_std = to_float(row.get("combined_preference_auc_std"))
    enough_headroom = oracle_gap >= args.oracle_gap_threshold
    enough_samples = pref_count >= args.min_preference_nodes
    stable_rel = math.isnan(rel_auc_std) or rel_auc_std <= args.auc_std_threshold
    stable_comb = math.isnan(comb_auc_std) or comb_auc_std <= args.auc_std_threshold
    rel_signal = rel_auc >= args.reliability_auc_threshold and stable_rel
    comb_signal = (
        comb_auc >= args.combined_auc_threshold
        and (math.isnan(feat_auc) or comb_auc - feat_auc >= args.combined_over_feature_threshold)
        and stable_comb
    )
    if not enough_samples:
        return ("STOP or deprioritize", "too few effective preference nodes")
    if enough_headroom and (rel_signal or comb_signal):
        return (
            "RUN representation-control 3-run",
            "headroom and routing separability pass the prescreen",
        )
    if not enough_headroom:
        return ("STOP or deprioritize", "oracle headroom is too small")
    return (
        "HOLD for signal expansion",
        "headroom exists, but current reliability/features do not separate preference enough",
    )


def write_decision_report(args: argparse.Namespace, summary_path: Path, output_path: Path) -> None:
    rows = read_csv(summary_path)
    backfill_preference_counts(rows, summary_path)
    lines = [
        "# Second Positive Prescreen Decision",
        "",
        "This report is generated from expert headroom and preference-routing diagnostics.",
        "",
        "## Criteria",
        "",
        f"- Oracle union minus best fixed >= {args.oracle_gap_threshold:.4f}",
        f"- Effective preference nodes >= {args.min_preference_nodes}",
        f"- Reliability preference AUC >= {args.reliability_auc_threshold:.4f}, or",
        (
            f"- Combined preference AUC >= {args.combined_auc_threshold:.4f} and "
            f"combined - feature >= {args.combined_over_feature_threshold:.4f}"
        ),
        f"- Relevant AUC std <= {args.auc_std_threshold:.4f}",
        "",
        "## Dataset Decisions",
        "",
        "| Dataset | Runs | Oracle-Fixed | Pref nodes | Rel AUC | Rel std | Feature AUC | Combined AUC | Combined std | Decision | Reason |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    if not rows:
        lines.append("| n/a | 0 |  |  |  |  |  |  |  | missing diagnostics | Run prescreen first |")
    for row in rows:
        decision, reason = verdict(args, row)
        lines.append(
            "| "
            f"{row.get('dataset', '')} | "
            f"{row.get('runs', '')} | "
            f"{fmt(to_float(row.get('oracle_union_minus_best_fixed_mean')))} | "
            f"{fmt(to_float(row.get('preference_count_mean')))} | "
            f"{fmt(to_float(row.get('reliability_preference_auc_mean')))} | "
            f"{fmt(to_float(row.get('reliability_preference_auc_std')))} | "
            f"{fmt(to_float(row.get('feature_preference_auc_mean')))} | "
            f"{fmt(to_float(row.get('combined_preference_auc_mean')))} | "
            f"{fmt(to_float(row.get('combined_preference_auc_std')))} | "
            f"{decision} | "
            f"{reason} |"
        )
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            (
                "Only datasets marked `RUN representation-control 3-run` should receive the "
                "full component-concat iterative-relation screening. Datasets marked `HOLD` "
                "are useful for controller-signal expansion but should not consume 10-run "
                "confirmation budget yet."
            ),
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def backfill_preference_counts(rows: list[dict[str, str]], summary_path: Path) -> None:
    if not rows or all(row.get("preference_count_mean") for row in rows):
        return
    preference_summary = summary_path.parent.parent / "preference" / "summary.csv"
    if not preference_summary.exists():
        return
    counts: dict[str, str] = {}
    for row in read_csv(preference_summary):
        if row.get("router") == "reliability_only":
            counts[row.get("dataset", "")] = row.get("test_preference_count_mean", "")
    for row in rows:
        if not row.get("preference_count_mean"):
            row["preference_count_mean"] = counts.get(row.get("dataset", ""), "")


if __name__ == "__main__":
    main()
