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

from run_expert_fusion import code_hash
from src.data import RELIABILITY_COMPONENTS
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    primary_metric_for_dataset,
    validation_fingerprint,
)
from src.representation_control import (
    ALPHA_TYPES,
    COMPONENT_MISSING_MODES,
    CONTROL_MODES,
    RELIABILITY_ENCODER_MODES,
)


FAMILIES = (
    "residual_alpha",
    "hidden_mixing_frozen",
    "hidden_mixing_finetune",
    "iterative_relation_frozen",
    "iterative_relation_finetune",
    "gps_like_frozen",
    "gps_like_finetune",
)
DEFAULT_DATASETS = (
    "Roman-empire",
    "Amazon-ratings",
    "Cora",
    "Pubmed",
)
DEFAULT_FAMILIES = (
    "iterative_relation_frozen",
    "iterative_relation_finetune",
)
DEFAULT_CONTROLS = (
    "fixed",
    "feature_only",
    "reliability_only",
    "combined",
    "shuffled_reliability",
    "constant_reliability",
    "zero_reliability",
    "combined_shuffled",
    "combined_constant",
)
CAUSAL_CONTROLS = {
    "fixed",
    "reliability_only",
    "combined",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=REAL_DATASETS,
        default=list(DEFAULT_DATASETS),
    )
    parser.add_argument(
        "--families",
        nargs="+",
        choices=FAMILIES,
        default=list(DEFAULT_FAMILIES),
    )
    parser.add_argument(
        "--controls",
        nargs="+",
        choices=CONTROL_MODES,
        default=list(DEFAULT_CONTROLS),
    )
    parser.add_argument("--edge-protocol", choices=EDGE_PROTOCOLS, default="undirected")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/representation_control_screen"),
    )
    parser.add_argument("--expert-cache-dir", type=Path)
    parser.add_argument("--backbone-cache-dir", type=Path)
    parser.add_argument(
        "--reuse-compatible-backbone-cache",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--compatible-backbone-cache-config", type=Path)
    parser.add_argument(
        "--save-node-diagnostics",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--node-diagnostics-dir", type=Path)
    parser.add_argument(
        "--save-external-expert-logits",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--causal-interventions",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
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
    parser.add_argument(
        "--reliability-encoder-mode",
        choices=RELIABILITY_ENCODER_MODES,
        default="raw_concat",
    )
    parser.add_argument("--reliability-component-dim", type=int, default=16)
    parser.add_argument(
        "--component-missing-mode",
        choices=COMPONENT_MISSING_MODES,
        default="zero_slot",
    )
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--expert-epochs", type=int, default=300)
    parser.add_argument("--control-epochs", type=int, default=200)
    parser.add_argument("--patience", type=int, default=60)
    parser.add_argument(
        "--fixed-alphas",
        nargs="+",
        type=float,
        default=[0.0, 0.25, 0.5, 0.75, 1.0],
    )
    parser.add_argument("--max-adjustment", type=float, default=0.1)
    parser.add_argument("--lambda-init", type=float, default=0.001)
    parser.add_argument("--relation-steps", type=int, default=1)
    parser.add_argument("--alpha-type", choices=ALPHA_TYPES, default="channel")
    parser.add_argument("--alpha-groups", type=int, default=4)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--analyze-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_args(args)
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    args.expert_cache_dir = (
        resolve(root, args.expert_cache_dir)
        if args.expert_cache_dir is not None
        else out_dir / "_expert_cache"
    )
    args.backbone_cache_dir = (
        resolve(root, args.backbone_cache_dir)
        if args.backbone_cache_dir is not None
        else out_dir / "_backbone_cache"
    )
    args.compatible_backbone_cache_config = (
        resolve(root, args.compatible_backbone_cache_config)
        if args.compatible_backbone_cache_config is not None
        else None
    )
    args.node_diagnostics_dir = (
        resolve(root, args.node_diagnostics_dir)
        if args.node_diagnostics_dir is not None
        else out_dir / "_node_diagnostics"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.save_node_diagnostics:
        args.node_diagnostics_dir.mkdir(parents=True, exist_ok=True)

    fingerprints = collect_data_fingerprints(args, data_root)
    preprocess_code_hash = code_hash(
        [root / "src" / "real_data.py", root / "src" / "data.py"]
    )
    config = suite_config(args, root, fingerprints)
    validate_or_write_config(out_dir, config, args.force)
    total_experiments = (
        len(args.datasets)
        * len(args.families)
        * len(args.controls)
        * args.runs
    )
    print(
        "Representation-control suite: "
        f"{len(args.datasets)} datasets x "
        f"{len(args.families)} families x "
        f"{len(args.controls)} controls x "
        f"{args.runs} runs = {total_experiments} requested run records",
        flush=True,
    )
    if not args.analyze_only:
        run_experiments(
            args,
            root,
            data_root,
            out_dir,
            fingerprints,
            preprocess_code_hash,
        )

    missing = [
        f"{dataset}/{family}/{control}"
        for dataset in args.datasets
        for family in args.families
        for control in args.controls
        if not result_complete(
            result_path(out_dir, dataset, family, control),
            args.runs,
            dataset,
            family,
            control,
            args.edge_protocol,
            args,
            fingerprints[dataset],
            preprocess_code_hash,
        )
    ]
    if missing:
        raise SystemExit("Missing representation-control results: " + ", ".join(missing))
    analyze(args, out_dir)


def validate_args(args) -> None:
    if args.runs < 1:
        raise ValueError("--runs must be positive")
    if args.reliability_component_dim < 1:
        raise ValueError("--reliability-component-dim must be positive")
    alpha_type = getattr(args, "alpha_type", "channel")
    alpha_groups = getattr(args, "alpha_groups", 4)
    if alpha_groups < 1:
        raise ValueError("--alpha-groups must be positive")
    if alpha_type == "group" and args.hidden_dim % alpha_groups != 0:
        raise ValueError("--hidden-dim must be divisible by --alpha-groups")
    if len(set(args.datasets)) != len(args.datasets):
        raise ValueError("--datasets contains duplicates")
    if len(set(args.families)) != len(args.families):
        raise ValueError("--families contains duplicates")
    if len(set(args.controls)) != len(args.controls):
        raise ValueError("--controls contains duplicates")
    if any(not 0.0 <= alpha <= 1.0 for alpha in args.fixed_alphas):
        raise ValueError("--fixed-alphas values must be between 0 and 1")
    if not 0.0 < args.lambda_init < args.max_adjustment <= 1.0:
        raise ValueError("Require 0 < lambda-init < max-adjustment <= 1")
    if args.relation_steps < 0:
        raise ValueError("--relation-steps must not be negative")
    if (
        any(
            family.startswith("iterative_relation_")
            for family in args.families
        )
        and args.relation_steps < 1
    ):
        raise ValueError("--relation-steps must be positive")
    if args.causal_interventions and any(
        not family.startswith("iterative_relation_")
        for family in args.families
    ):
        raise ValueError(
            "--causal-interventions requires only iterative_relation families"
        )
    if args.causal_interventions and any(
        control not in CAUSAL_CONTROLS
        for control in args.controls
    ):
        raise ValueError(
            "--causal-interventions supports only fixed, reliability_only, "
            "or combined controls"
        )
    if (
        args.reuse_compatible_backbone_cache
        and args.compatible_backbone_cache_config is None
    ):
        raise ValueError(
            "--reuse-compatible-backbone-cache requires "
            "--compatible-backbone-cache-config"
        )
    if args.save_external_expert_logits and not args.save_node_diagnostics:
        raise ValueError(
            "--save-external-expert-logits requires --save-node-diagnostics"
        )


def run_experiments(
    args,
    root,
    data_root,
    out_dir,
    fingerprints,
    preprocess_code_hash,
) -> None:
    total = len(args.datasets) * len(args.families) * len(args.controls)
    step = 0
    for dataset in args.datasets:
        for family in args.families:
            for control in args.controls:
                step += 1
                path = result_path(out_dir, dataset, family, control)
                if not args.force and result_complete(
                    path,
                    args.runs,
                    dataset,
                    family,
                    control,
                    args.edge_protocol,
                    args,
                    fingerprints[dataset],
                    preprocess_code_hash,
                ):
                    print(
                        f"[{step}/{total}] skip {dataset}/{family}/{control}",
                        flush=True,
                    )
                    continue
                if args.force and path.exists():
                    path.unlink()
                command = [
                    args.python,
                    str(root / "run_representation_control.py"),
                    "--dataset", dataset,
                    "--family", family,
                    "--control-mode", control,
                    "--result-name", f"{family}_{control}",
                    "--edge-protocol", args.edge_protocol,
                    "--runs", str(args.runs),
                    "--data-root", str(data_root),
                    "--out-dir", str(out_dir),
                    "--expert-cache-dir", str(args.expert_cache_dir),
                    "--backbone-cache-dir", str(args.backbone_cache_dir),
                    "--rw-steps", str(args.rw_steps),
                    "--rw-samples", str(args.rw_samples),
                    "--rw-seed", str(args.rw_seed),
                    "--reliability-components", *args.reliability_components,
                    "--reliability-encoder-mode", args.reliability_encoder_mode,
                    "--reliability-component-dim",
                    str(args.reliability_component_dim),
                    "--component-missing-mode",
                    args.component_missing_mode,
                    "--hidden-dim", str(args.hidden_dim),
                    "--num-layers", str(args.num_layers),
                    "--num-heads", str(args.num_heads),
                    "--dropout", str(args.dropout),
                    "--lr", str(args.lr),
                    "--weight-decay", str(args.weight_decay),
                    "--expert-epochs", str(args.expert_epochs),
                    "--control-epochs", str(args.control_epochs),
                    "--patience", str(args.patience),
                    "--fixed-alphas", *[str(value) for value in args.fixed_alphas],
                    "--max-adjustment", str(args.max_adjustment),
                    "--lambda-init", str(args.lambda_init),
                    "--relation-steps", str(args.relation_steps),
                    "--alpha-type", args.alpha_type,
                    "--alpha-groups", str(args.alpha_groups),
                    "--device", args.device,
                ]
                if args.save_node_diagnostics:
                    command.extend(
                        [
                            "--save-node-diagnostics",
                            "--node-diagnostics-dir",
                            str(args.node_diagnostics_dir),
                        ]
                    )
                if args.causal_interventions:
                    command.append("--causal-interventions")
                if args.reuse_compatible_backbone_cache:
                    command.extend(
                        [
                            "--reuse-compatible-backbone-cache",
                            "--compatible-backbone-cache-config",
                            str(args.compatible_backbone_cache_config),
                        ]
                    )
                if args.save_external_expert_logits:
                    command.append("--save-external-expert-logits")
                if not args.normalize_features:
                    command.append("--no-normalize-features")
                if args.no_download:
                    command.append("--no-download")
                print(
                    f"[{step}/{total}] run {dataset}/{family}/{control}",
                    flush=True,
                )
                subprocess.run(command, cwd=root, check=True)


def analyze(args, out_dir) -> None:
    rows = []
    for dataset in args.datasets:
        for family in args.families:
            for control in args.controls:
                rows.extend(
                    read_csv(result_path(out_dir, dataset, family, control))
                )
    summary = summarize(rows)
    comparisons = paired_comparisons(
        rows,
        args.datasets,
        args.families,
        args.controls,
    )
    causal_summary = (
        summarize_causal_interventions(rows)
        if args.causal_interventions
        else []
    )
    write_csv(out_dir / "summary.csv", summary)
    write_csv(
        out_dir / "paired_comparisons.csv",
        comparisons,
        [
            "dataset",
            "family",
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
    if causal_summary:
        write_csv(
            out_dir / "causal_interventions.csv",
            causal_summary,
        )
    uses_iterative = any(
        family.startswith("iterative_relation_")
        for family in args.families
    )
    uses_scalar_controller = any(
        family in {
            "residual_alpha",
            "hidden_mixing_frozen",
            "hidden_mixing_finetune",
            "gps_like_frozen",
            "gps_like_finetune",
        }
        for family in args.families
    )
    report = [
        "# Representation Control Screening",
        "",
        f"- Datasets: {', '.join(args.datasets)}",
        f"- Families: {', '.join(args.families)}",
        f"- Runs: {args.runs}",
        f"- Edge protocol: {args.edge_protocol}",
        f"- Reliability encoder mode: {args.reliability_encoder_mode}",
        f"- Reliability component dim: {args.reliability_component_dim}",
        f"- Component missing mode: {args.component_missing_mode}",
        (
            f"- Iterative alpha type: {args.alpha_type}"
            if uses_iterative
            else "- Iterative alpha type: n/a"
        ),
        (
            f"- Iterative alpha groups: {args.alpha_groups}"
            if uses_iterative and args.alpha_type == "group"
            else "- Iterative alpha groups: n/a"
        ),
        f"- Max adjustment: {args.max_adjustment}",
        (
            f"- Initial scalar-alpha adjustment: {args.lambda_init}"
            if uses_scalar_controller
            else "- Initial scalar-alpha adjustment: n/a"
        ),
        (
            f"- Iterative relation steps: {args.relation_steps}"
            if uses_iterative
            else "- Iterative relation steps: n/a"
        ),
        "- `zero_reliability` is a learnable controller receiving an all-zero "
        "reliability input; `fixed` is the no-controller baseline.",
        (
            "- External local/global expert logits are embedded in node diagnostics "
            "for preference-alignment analysis."
            if args.save_external_expert_logits
            else "- External local/global expert logits are not embedded; node "
            "diagnostics support internal branch analysis but do not by themselves "
            "guarantee preference-alignment availability."
        ),
        "- `relation_relative_strength` and "
        "`relation_to_branch_disagreement` are the stable relation-magnitude "
        "diagnostics. Per-node `relation_to_base_norm` is retained only as an "
        "auxiliary diagnostic because small base norms can inflate it.",
    ]
    if any(family.startswith("hidden_mixing_") for family in args.families):
        report.extend(
            [
                "- `hidden_mixing_frozen/fixed` is the untouched selected "
                "hidden baseline.",
                "- `hidden_mixing_finetune/fixed` is the same-architecture "
                "fixed-mixing fine-tuning control.",
            ]
        )
    if any(family.startswith("gps_like_") for family in args.families):
        report.extend(
            [
                "- `gps_like_frozen/fixed` is the untouched selected GPS-like "
                "backbone baseline.",
                "- `gps_like_finetune/fixed` is the same GPS-like "
                "fixed-mixing fine-tuning control.",
            ]
        )
    if uses_iterative:
        report.extend(
            [
                "- `iterative_relation_frozen/fixed` is the same selected "
                "hidden baseline with zero relation correction.",
                "- `iterative_relation_finetune/fixed` fine-tunes the fixed "
                "mixing architecture without a relation controller.",
            ]
        )
    report.extend(
        [
            "",
            "## Summary",
            "",
            "| Dataset | Metric | Family | Control | Primary | Baseline | Delta | Std | Accuracy | Alpha | Adjustment | Relation strength | Relation/disagreement | Update gate | Active ctrl params | Backbone params |",
            "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in summary:
        report.append(
            f"| {row['dataset']} | {row['primary_metric']} | "
            f"{row['family']} | {row['control_mode']} | "
            f"{row['test_primary_mean']:.4f} | "
            f"{row['baseline_test_primary_mean']:.4f} | "
            f"{row['gain_over_own_baseline']:+.4f} | "
            f"{row['test_primary_std']:.4f} | "
            f"{row['test_acc_mean']:.4f} | "
            f"{fmt_plain(row['alpha_mean'])} | "
            f"{fmt_plain(row['adjustment_mean'])} | "
            f"{fmt_plain(row['relation_relative_strength'])} | "
            f"{fmt_plain(row['relation_to_branch_disagreement'])} | "
            f"{fmt_plain(row['relation_update_gate_mean'])} | "
            f"{fmt_integer(row['active_controller_parameters'])} | "
            f"{fmt_integer(row['backbone_trainable_parameters'])} |"
        )
    report.extend(
        [
            "",
            "## Paired Comparisons",
            "",
            "| Dataset | Family | Comparison | Delta | 95% CI | W/T/L | p |",
            "|---|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in comparisons:
        report.append(
            f"| {row['dataset']} | {row['family']} | {row['comparison']} | "
            f"{row['mean_delta']:+.4f} | "
            f"[{fmt(row['ci95_low'])}, {fmt(row['ci95_high'])}] | "
            f"{row['wins']}/{row['ties']}/{row['losses']} | "
            f"{fmt(row['pvalue'])} |"
        )
    if causal_summary:
        report.extend(
            [
                "",
                "## Causal Interventions",
                "",
                "- Each intervention reuses the exact trained model and changes only "
                "the named inference-time mechanism.",
                "- Positive drop means the intact learned mechanism performs better "
                "than its counterfactual intervention.",
                "- For frozen families, `zero_all` returns to the unchanged fixed "
                "backbone. For finetuned families, it means the same jointly trained "
                "model evaluated without relation correction, not the original fixed "
                "baseline.",
                "- Layer-wise relation ablation measures the total downstream effect "
                "of disabling that relation block; it is not an additive decomposition "
                "of independent layer contributions.",
                "- `fixed` is a sanity control: relation and reliability interventions "
                "should have approximately zero effect.",
                "",
                "| Dataset | Family | Control | Intervention | Primary drop | 95% CI | Accuracy drop | Changed predictions | Normal-only correct | Intervention-only correct | W/T/L |",
                "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in causal_summary:
            report.append(
                f"| {row['dataset']} | {row['family']} | "
                f"{row['control_mode']} | {row['intervention']} | "
                f"{row['primary_drop_mean']:+.4f} | "
                f"[{fmt(row['ci95_low'])}, {fmt(row['ci95_high'])}] | "
                f"{row['acc_drop_mean']:+.4f} | "
                f"{row['prediction_change_rate_mean']:.4f} | "
                f"{row['normal_only_correct_rate_mean']:.4f} | "
                f"{row['intervention_only_correct_rate_mean']:.4f} | "
                f"{row['wins']}/{row['ties']}/{row['losses']} |"
            )
    report.extend(
        [
            "",
            "## Screening Rule",
            "",
            "- A mechanism is a screening candidate when it wins at least 2/3 runs, "
            "has a mean gain of at least 0.005, and true reliability exceeds its "
            "shuffled or constant counterpart.",
            "- Three-run intervals are descriptive only. Confirm selected mechanisms "
            "with 10 official splits or seeds before making statistical claims.",
        ]
    )
    (out_dir / "analysis.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    print(f"analysis: {out_dir / 'analysis.md'}")


def summarize(rows):
    groups = {}
    for row in rows:
        key = (row["dataset"], row["family"], row["control_mode"])
        groups.setdefault(key, []).append(row)
    output = []
    for (dataset, family, control), group in sorted(groups.items()):
        primary = [float(row["test_primary_at_best_val"]) for row in group]
        accuracy = [float(row["test_acc_at_best_val"]) for row in group]
        baseline = [float(row["baseline_test_primary"]) for row in group]
        output.append(
            {
                "dataset": dataset,
                "family": family,
                "control_mode": control,
                "primary_metric": group[0]["primary_metric"],
                "n": len(group),
                "test_primary_mean": statistics.mean(primary),
                "test_primary_std": statistics.pstdev(primary),
                "test_acc_mean": statistics.mean(accuracy),
                "test_acc_std": statistics.pstdev(accuracy),
                "macro_f1_mean": finite_mean(group, "test_macro_f1_at_best_val"),
                "backbone_training_mode": group[0].get(
                    "backbone_training_mode",
                    "unknown",
                ),
                "baseline_test_primary_mean": statistics.mean(baseline),
                "gain_over_own_baseline": statistics.mean(
                    left - right
                    for left, right in zip(primary, baseline)
                ),
                "base_alpha_mean": finite_mean(group, "base_alpha"),
                "alpha_mean": finite_mean(group, "alpha_mean"),
                "alpha_std": finite_mean(group, "alpha_std"),
                "adjustment_mean": finite_mean(group, "adjustment_mean"),
                "adjustment_max": finite_mean(group, "adjustment_max"),
                "relation_abs_mean": finite_mean(group, "relation_abs_mean"),
                "relation_norm_mean": finite_mean(group, "relation_norm_mean"),
                "relation_to_base_norm": finite_mean(
                    group,
                    "relation_to_base_norm",
                ),
                "relation_relative_strength": finite_mean(
                    group,
                    "relation_relative_strength",
                ),
                "relation_to_branch_disagreement": finite_mean(
                    group,
                    "relation_to_branch_disagreement",
                ),
                "relation_state_norm_mean": finite_mean(
                    group,
                    "relation_state_norm_mean",
                ),
                "relation_update_gate_mean": finite_mean(
                    group,
                    "relation_update_gate_mean",
                ),
                "relation_update_gate_std": finite_mean(
                    group,
                    "relation_update_gate_std",
                ),
                "alpha_corr_local_similarity": finite_mean(
                    group,
                    "alpha_corr_raw_local_similarity",
                ),
                "alpha_corr_degree": finite_mean(
                    group,
                    "alpha_corr_raw_degree",
                ),
                "alpha_corr_neighbor_variance": finite_mean(
                    group,
                    "alpha_corr_raw_neighbor_variance",
                ),
                "alpha_corr_rwse": finite_mean(group, "alpha_corr_raw_rwse"),
                "alpha_corr_control_input_mean": finite_mean(
                    group,
                    "alpha_corr_control_input_mean",
                ),
                "declared_trainable_parameters": finite_mean(
                    group,
                    "declared_trainable_parameters",
                ),
                "active_controller_parameters": finite_mean(
                    group,
                    "active_controller_parameters",
                ),
                "backbone_trainable_parameters": finite_mean(
                    group,
                    "backbone_trainable_parameters",
                ),
            }
        )
    return output


def summarize_causal_interventions(rows):
    if not rows:
        return []
    suffix = "_primary_drop"
    interventions = sorted(
        {
            key[len("causal_") : -len(suffix)]
            for row in rows
            for key in row
            if key.startswith("causal_") and key.endswith(suffix)
        },
        key=causal_intervention_sort_key,
    )
    groups = {}
    for row in rows:
        key = (row["dataset"], row["family"], row["control_mode"])
        groups.setdefault(key, []).append(row)

    output = []
    for (dataset, family, control), group in sorted(groups.items()):
        for intervention in interventions:
            prefix = f"causal_{intervention}"
            primary_drop = finite_values(group, f"{prefix}_primary_drop")
            if not primary_drop:
                continue
            half = ci95(primary_drop)
            mean_drop = statistics.mean(primary_drop)
            wins = sum(value > 0 for value in primary_drop)
            ties = sum(value == 0 for value in primary_drop)
            output.append(
                {
                    "dataset": dataset,
                    "family": family,
                    "control_mode": control,
                    "intervention": intervention,
                    "n": len(primary_drop),
                    "primary_drop_mean": mean_drop,
                    "ci95_low": mean_drop - half,
                    "ci95_high": mean_drop + half,
                    "acc_drop_mean": finite_mean(
                        group,
                        f"{prefix}_acc_drop",
                    ),
                    "prediction_change_rate_mean": finite_mean(
                        group,
                        f"{prefix}_prediction_change_rate",
                    ),
                    "normal_only_correct_rate_mean": finite_mean(
                        group,
                        f"{prefix}_normal_only_correct_rate",
                    ),
                    "intervention_only_correct_rate_mean": finite_mean(
                        group,
                        f"{prefix}_intervention_only_correct_rate",
                    ),
                    "wins": wins,
                    "ties": ties,
                    "losses": len(primary_drop) - wins - ties,
                }
            )
    return output


def causal_intervention_sort_key(name):
    if name == "zero_all":
        return (0, 0)
    if name.startswith("zero_layer_"):
        return (1, int(name.rsplit("_", 1)[1]))
    if name == "shuffled_reliability":
        return (2, 0)
    if name == "constant_reliability":
        return (3, 0)
    return (4, name)


def finite_values(rows, key):
    values = []
    for row in rows:
        try:
            value = float(row[key])
        except (KeyError, TypeError, ValueError):
            continue
        if math.isfinite(value):
            values.append(value)
    return values


def paired_comparisons(rows, datasets, families, controls):
    requested = set(controls)
    pairs = []
    for control in (
        "feature_only",
        "reliability_only",
        "combined",
        "shuffled_reliability",
        "constant_reliability",
        "zero_reliability",
        "combined_shuffled",
        "combined_constant",
    ):
        if control in requested and "fixed" in requested:
            pairs.append((control, "fixed", f"{control} - fixed"))
    for pair in (
        (
            "reliability_only",
            "feature_only",
            "reliability_only - feature_only",
        ),
        (
            "reliability_only",
            "shuffled_reliability",
            "true reliability - shuffled reliability",
        ),
        (
            "reliability_only",
            "constant_reliability",
            "true reliability - constant reliability",
        ),
        (
            "reliability_only",
            "zero_reliability",
            "true reliability - zero reliability",
        ),
        ("combined", "feature_only", "combined - feature_only"),
        (
            "combined",
            "combined_shuffled",
            "combined - combined_shuffled",
        ),
        (
            "combined",
            "combined_constant",
            "combined - combined_constant",
        ),
    ):
        if pair[0] in requested and pair[1] in requested:
            pairs.append(pair)
    output = [
        {
            "dataset": dataset,
            "family": family,
            "comparison": label,
            **paired_stats(rows, dataset, family, left, right),
        }
        for dataset in datasets
        for family in families
        for left, right, label in pairs
    ]
    for frozen, finetune, label in (
        (
            "hidden_mixing_frozen",
            "hidden_mixing_finetune",
            "hidden_protocol",
        ),
        (
            "iterative_relation_frozen",
            "iterative_relation_finetune",
            "iterative_relation_protocol",
        ),
    ):
        if {frozen, finetune}.issubset(families):
            for dataset in datasets:
                for control in controls:
                    output.append(
                        {
                            "dataset": dataset,
                            "family": label,
                            "comparison": f"{control}: finetune - frozen",
                            **paired_family_stats(
                                rows,
                                dataset,
                                control,
                                finetune,
                                frozen,
                            ),
                        }
                    )
    return output


def paired_stats(rows, dataset, family, left_control, right_control):
    left = keyed(rows, dataset, family, left_control)
    right = keyed(rows, dataset, family, right_control)
    keys = sorted(left.keys() & right.keys())
    return paired_values(left, right, keys)


def paired_family_stats(rows, dataset, control, left_family, right_family):
    left = keyed(rows, dataset, left_family, control)
    right = keyed(rows, dataset, right_family, control)
    keys = sorted(left.keys() & right.keys())
    return paired_values(left, right, keys)


def paired_values(left, right, keys):
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


def keyed(rows, dataset, family, control):
    return {
        (int(row["split"]), int(row["seed"])): float(
            row["test_primary_at_best_val"]
        )
        for row in rows
        if row["dataset"] == dataset
        and row["family"] == family
        and row["control_mode"] == control
    }


def suite_config(args, root, fingerprints):
    digest = hashlib.sha256()
    for relative in (
        "src/data.py",
        "src/models.py",
        "src/expert_models.py",
        "src/real_data.py",
        "src/representation_control.py",
        "run_expert_fusion.py",
        "run_representation_control.py",
        "run_representation_control_suite.py",
    ):
        digest.update((root / relative).read_bytes())
    return {
        "code_fingerprint": digest.hexdigest(),
        "datasets": args.datasets,
        "families": args.families,
        "controls": args.controls,
        "runs": args.runs,
        "edge_protocol": args.edge_protocol,
        "data_root": str(resolve(root, args.data_root)),
        "expert_cache_dir": str(args.expert_cache_dir),
        "backbone_cache_dir": str(args.backbone_cache_dir),
        "save_node_diagnostics": args.save_node_diagnostics,
        "node_diagnostics_dir": (
            str(args.node_diagnostics_dir)
            if args.save_node_diagnostics
            else None
        ),
        "causal_interventions": args.causal_interventions,
        "save_external_expert_logits": args.save_external_expert_logits,
        "reuse_compatible_backbone_cache": (
            args.reuse_compatible_backbone_cache
        ),
        "compatible_backbone_cache_config": (
            str(args.compatible_backbone_cache_config)
            if args.compatible_backbone_cache_config is not None
            else None
        ),
        "data_fingerprints": fingerprints,
        "normalize_features": args.normalize_features,
        "rw_steps": args.rw_steps,
        "rw_samples": args.rw_samples,
        "rw_seed": args.rw_seed,
        "reliability_components": args.reliability_components,
        "reliability_encoder_mode": args.reliability_encoder_mode,
        "reliability_component_dim": args.reliability_component_dim,
        "component_missing_mode": args.component_missing_mode,
        "alpha_type": args.alpha_type,
        "alpha_groups": args.alpha_groups,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "expert_epochs": args.expert_epochs,
        "control_epochs": args.control_epochs,
        "patience": args.patience,
        "fixed_alphas": args.fixed_alphas,
        "max_adjustment": args.max_adjustment,
        "lambda_init": args.lambda_init,
        "relation_steps": (
            args.relation_steps
            if any(
                family.startswith("iterative_relation_")
                for family in args.families
            )
            else None
        ),
        "device": args.device,
    }


def collect_data_fingerprints(args, data_root):
    output = {}
    for dataset in args.datasets:
        _, report = load_and_validate_dataset(
            dataset,
            data_root,
            allow_download=not args.no_download,
        )
        output[dataset] = validation_fingerprint(report)
    return output


def validate_or_write_config(out_dir, config, force):
    path = out_dir / "suite_config.json"
    if path.exists() and not force:
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != config:
            raise RuntimeError(
                "Output directory uses a different configuration; "
                "choose another --out-dir or use --force"
            )
    path.write_text(json.dumps(config, indent=2), encoding="utf-8")


def result_complete(
    path,
    runs,
    dataset,
    family,
    control,
    edge_protocol,
    args,
    data_fingerprint,
    preprocess_code_hash,
):
    if not path.exists():
        return False
    rows = read_csv(path)
    required = {
        "dataset",
        "family",
        "control_mode",
        "edge_protocol",
        "split",
        "seed",
        "best_val_acc",
        "primary_metric",
        "best_val_primary",
        "test_primary_at_best_val",
        "best_val_roc_auc",
        "test_roc_auc_at_best_val",
        "test_acc_at_best_val",
        "baseline_test_acc",
        "baseline_val_primary",
        "baseline_test_primary",
        "baseline_val_roc_auc",
        "baseline_test_roc_auc",
        "declared_trainable_parameters",
        "active_controller_parameters",
        "backbone_trainable_parameters",
        "backbone_training_mode",
        "reliability_components",
        "reliability_encoder_mode",
        "reliability_component_dim",
        "component_missing_mode",
        "alpha_type",
        "alpha_groups",
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
        "control_epochs",
        "patience",
        "fixed_alphas",
        "max_adjustment",
        "lambda_init",
        "data_fingerprint",
        "preprocess_code_hash",
        "causal_interventions",
        "save_external_expert_logits",
        "reuse_compatible_backbone_cache",
    }
    if family.startswith("iterative_relation_"):
        required.update(
            {
                "relation_steps",
                "relation_relative_strength",
                "relation_to_branch_disagreement",
            }
        )
    if len(rows) != runs or not rows or not required.issubset(rows[0]):
        return False
    if any(
        row["dataset"] != dataset
        or row["family"] != family
        or row["control_mode"] != control
        or row["edge_protocol"] != edge_protocol
        for row in rows
    ):
        return False
    expected = {
        "reliability_components": ",".join(args.reliability_components),
        "reliability_encoder_mode": args.reliability_encoder_mode,
        "reliability_component_dim": str(args.reliability_component_dim),
        "component_missing_mode": args.component_missing_mode,
        "alpha_type": args.alpha_type,
        "alpha_groups": str(args.alpha_groups),
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
        "control_epochs": str(args.control_epochs),
        "patience": str(args.patience),
        "fixed_alphas": ",".join(str(value) for value in args.fixed_alphas),
        "max_adjustment": str(args.max_adjustment),
        "lambda_init": str(args.lambda_init),
        "data_fingerprint": data_fingerprint,
        "preprocess_code_hash": preprocess_code_hash,
        "backbone_training_mode": expected_training_mode(family, control),
        "causal_interventions": str(args.causal_interventions),
        "save_external_expert_logits": str(
            args.save_external_expert_logits
        ),
        "reuse_compatible_backbone_cache": str(
            args.reuse_compatible_backbone_cache
        ),
    }
    expected["primary_metric"] = primary_metric_for_dataset(dataset)
    if family.startswith("iterative_relation_"):
        expected["relation_steps"] = str(args.relation_steps)
    if args.causal_interventions:
        for field in (
            "causal_zero_all_primary_drop",
            "causal_shuffled_reliability_primary_drop",
            "causal_constant_reliability_primary_drop",
        ):
            if field not in rows[0]:
                return False
    if any(
        any(row.get(key) != value for key, value in expected.items())
        for row in rows
    ):
        return False
    return len({(int(row["split"]), int(row["seed"])) for row in rows}) == runs


def result_path(out_dir, dataset, family, control):
    return out_dir / f"{dataset}_{family}_{control}.csv"


def expected_training_mode(family, control):
    if family == "residual_alpha":
        return "logits_only"
    if family.endswith("_frozen"):
        return "fixed_frozen" if control == "fixed" else "frozen"
    if family.endswith("_finetune"):
        return "fixed_finetuned" if control == "fixed" else "finetuned"
    return "unknown"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fieldnames=None):
    with path.open("w", newline="", encoding="utf-8") as handle:
        if not rows:
            return
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames or list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)


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


def empty_stats():
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


def fmt(value):
    return "n/a" if math.isnan(float(value)) else f"{float(value):+.4f}"


def fmt_plain(value):
    return "n/a" if math.isnan(float(value)) else f"{float(value):.4f}"


def fmt_integer(value):
    return "n/a" if math.isnan(float(value)) else str(int(round(float(value))))


def resolve(root, path):
    return path if path.is_absolute() else root / path


if __name__ == "__main__":
    main()
