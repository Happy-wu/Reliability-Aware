from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from run_synthetic import train_one


FINALISTS = {
    "heterophily": {
        "gate_gt": ("local_similarity",),
        "reliability_gt": ("degree", "local_similarity", "rwse"),
    },
    "homophily": {
        "gate_gt": ("rwse",),
        "reliability_gt": ("local_similarity",),
    },
    "noisy": {
        "gate_gt": ("degree",),
        "reliability_gt": ("rwse",),
    },
}
FULL_COMPONENTS = ("degree", "local_similarity", "neighbor_variance", "rwse")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(30)))
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/synthetic_finalists"))
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
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = ROOT
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    config = finalist_config(args, root)
    validate_or_write_config(out_dir, config, args.force)
    raw_path = out_dir / "raw_results.csv"

    if raw_path.exists() and not args.force:
        rows = read_csv(raw_path)
        expected = 3 * 2 * 2 * len(args.seeds)
        if len(rows) != expected:
            raise RuntimeError("Existing finalist output is incomplete; pass --force to replace it.")
    else:
        rows = run_finalists(args, raw_path)

    comparisons = analyze(rows)
    write_csv(out_dir / "paired_comparisons.csv", comparisons)
    write_report(out_dir / "preliminary_analysis.md", comparisons)
    print(f"Finalist analysis: {out_dir / 'preliminary_analysis.md'}")


def finalist_config(args: argparse.Namespace, root: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    for relative in (
        "src/data.py",
        "src/models.py",
        "scripts/legacy_synthetic/run_synthetic.py",
        "scripts/legacy_synthetic/run_synthetic_finalists.py",
    ):
        digest.update((root / relative).read_bytes())
    return {
        "code_fingerprint": digest.hexdigest(),
        "finalists": FINALISTS,
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


def validate_or_write_config(
    out_dir: Path,
    config: dict[str, object],
    force: bool,
) -> None:
    config = json.loads(json.dumps(config))
    path = out_dir / "suite_config.json"
    if path.exists() and not force:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != config:
            raise RuntimeError(
                "Existing finalist outputs use a different configuration. "
                "Use a new --out-dir or pass --force."
            )
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def run_finalists(args: argparse.Namespace, raw_path: Path) -> list[dict]:
    rows = []
    total = 3 * 2 * 2 * len(args.seeds)
    step = 0
    for graph, models in FINALISTS.items():
        for model, candidate_components in models.items():
            for variant, components in (
                ("full", FULL_COMPONENTS),
                ("candidate", candidate_components),
            ):
                for seed in args.seeds:
                    step += 1
                    print(
                        f"[{step}/{total}] graph={graph} model={model} "
                        f"variant={variant} seed={seed}",
                        flush=True,
                    )
                    run_args = SimpleNamespace(**vars(args))
                    run_args.graph_type = graph
                    run_args.model = model
                    run_args.reliability_components = list(components)
                    run_args.verbose = False
                    row = train_one(run_args, seed)
                    row["variant"] = variant
                    rows.append(row)
                    write_csv(raw_path, rows)
    return rows


def analyze(rows: list[dict]) -> list[dict[str, object]]:
    output = []
    for graph, models in FINALISTS.items():
        for model in models:
            full = values(rows, graph, model, "full")
            candidate = values(rows, graph, model, "candidate")
            seeds = sorted(set(full).intersection(candidate))
            differences = [candidate[seed] - full[seed] for seed in seeds]
            mean_delta = statistics.mean(differences)
            ci_half = ci95(differences)
            p_t, p_w = paired_pvalues(
                [candidate[seed] for seed in seeds],
                [full[seed] for seed in seeds],
                differences,
            )
            wins = sum(value > 0 for value in differences)
            ties = sum(value == 0 for value in differences)
            output.append(
                {
                    "graph_type": graph,
                    "model": model,
                    "candidate_components": ",".join(models[model]),
                    "n": len(seeds),
                    "full_mean": statistics.mean(full.values()),
                    "candidate_mean": statistics.mean(candidate.values()),
                    "mean_delta": mean_delta,
                    "ci95_low": mean_delta - ci_half,
                    "ci95_high": mean_delta + ci_half,
                    "wins": wins,
                    "ties": ties,
                    "losses": len(seeds) - wins - ties,
                    "paired_t_pvalue": p_t,
                    "wilcoxon_pvalue": p_w,
                }
            )
    return output


def paired_pvalues(
    candidate: list[float],
    full: list[float],
    differences: list[float],
) -> tuple[float, float]:
    if len(differences) < 2:
        return math.nan, math.nan
    try:
        from scipy.stats import ttest_rel, wilcoxon

        p_t = float(ttest_rel(candidate, full).pvalue)
        nonzero = [value for value in differences if value != 0]
        p_w = (
            float(wilcoxon(differences, zero_method="wilcox").pvalue)
            if nonzero
            else math.nan
        )
        return p_t, p_w
    except ImportError:
        return math.nan, math.nan


def values(rows: list[dict], graph: str, model: str, variant: str) -> dict[int, float]:
    return {
        int(row["seed"]): float(row["test_acc_at_best_val"])
        for row in rows
        if row["graph_type"] == graph
        and row["model"] == model
        and row["variant"] == variant
    }


def ci95(values_: list[float]) -> float:
    if len(values_) < 2:
        return math.nan
    standard_error = statistics.stdev(values_) / math.sqrt(len(values_))
    try:
        from scipy.stats import t

        critical = float(t.ppf(0.975, len(values_) - 1))
    except ImportError:
        critical = 1.96
    return critical * standard_error


def write_report(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Synthetic Finalist Confirmatory Analysis",
        "",
        "| Graph | Model | Candidate | Full | Candidate | Delta | 95% CI | W/T/L | t p | Wilcoxon p |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['graph_type']} | {row['model']} | {row['candidate_components']} | "
            f"{row['full_mean']:.4f} | {row['candidate_mean']:.4f} | "
            f"{row['mean_delta']:+.4f} | "
            f"[{row['ci95_low']:+.4f}, {row['ci95_high']:+.4f}] | "
            f"{row['wins']}/{row['ties']}/{row['losses']} | "
            f"{format_stat(row['paired_t_pvalue'])} | "
            f"{format_stat(row['wilcoxon_pvalue'])} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def format_stat(value: object) -> str:
    number = float(value)
    return "n/a" if math.isnan(number) else f"{number:.4f}"


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
