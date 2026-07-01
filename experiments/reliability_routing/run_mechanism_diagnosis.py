from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expert-findings",
        type=Path,
        default=Path("outputs/expert_validation_full/validation_findings.csv"),
    )
    parser.add_argument(
        "--preference-summary",
        type=Path,
        default=Path("outputs/preference_routing_full_v3/summary.csv"),
    )
    parser.add_argument(
        "--utility-summary",
        type=Path,
        default=Path("outputs/utility_routing_full_v3/summary.csv"),
    )
    parser.add_argument(
        "--representation-summary",
        type=Path,
        default=Path("outputs/representation_control_confirm_s010_r10/summary.csv"),
    )
    parser.add_argument(
        "--representation-paired",
        type=Path,
        default=Path("outputs/representation_control_confirm_s010_r10/paired_comparisons.csv"),
    )
    parser.add_argument(
        "--iterative-summary",
        type=Path,
        default=Path("outputs/iterative_relation_k1_screen/summary.csv"),
    )
    parser.add_argument(
        "--iterative-paired",
        type=Path,
        default=Path("outputs/iterative_relation_k1_screen/paired_comparisons.csv"),
    )
    parser.add_argument(
        "--binary-summary",
        dest="iterative_summary",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--binary-paired",
        dest="iterative_paired",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--datasets", nargs="*")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/mechanism_diagnosis"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    out_dir = resolve(root, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    expert_path = resolve(root, args.expert_findings)
    preference_path = resolve(root, args.preference_summary)
    utility_path = resolve(root, args.utility_summary)
    representation_summary_path = resolve(root, args.representation_summary)
    representation_paired_path = resolve(root, args.representation_paired)
    iterative_summary_path = resolve(root, args.iterative_summary)
    iterative_paired_path = resolve(root, args.iterative_paired)

    expert_rows = read_csv_if_exists(expert_path)
    preference_rows = read_csv_if_exists(preference_path)
    utility_rows = read_csv_if_exists(utility_path)
    representation_summary_rows = read_csv_if_exists(representation_summary_path)
    representation_paired_rows = read_csv_if_exists(representation_paired_path)
    iterative_summary_rows = read_csv_if_exists(iterative_summary_path)
    iterative_paired_rows = read_csv_if_exists(iterative_paired_path)
    missing_layers = [
        label
        for label, rows in (
            ("expert findings", expert_rows),
            ("preference routing summary", preference_rows),
            ("utility routing summary", utility_rows),
            ("representation summary", representation_summary_rows),
            ("representation paired comparisons", representation_paired_rows),
            ("iterative relation K=1 summary", iterative_summary_rows),
            ("iterative relation K=1 paired comparisons", iterative_paired_rows),
        )
        if not rows
    ]

    datasets = sorted(
        set(args.datasets)
        if args.datasets
        else (
            collect_datasets(expert_rows)
            | collect_datasets(preference_rows)
            | collect_datasets(utility_rows)
            | collect_datasets(representation_summary_rows)
            | collect_datasets(representation_paired_rows)
            | collect_datasets(iterative_summary_rows)
            | collect_datasets(iterative_paired_rows)
        )
    )

    scorecard = [
        build_scorecard_row(
            dataset,
            expert_rows,
            preference_rows,
            utility_rows,
            representation_summary_path.parent,
            representation_summary_rows,
            representation_paired_rows,
            iterative_summary_path.parent,
            iterative_summary_rows,
            iterative_paired_rows,
        )
        for dataset in datasets
    ]
    write_csv(out_dir / "dataset_scorecard.csv", scorecard)
    (out_dir / "analysis.md").write_text(
        render_report(scorecard, missing_layers),
        encoding="utf-8",
    )
    print(f"saved: {out_dir / 'dataset_scorecard.csv'}")
    print(f"saved: {out_dir / 'analysis.md'}")


def build_scorecard_row(
    dataset: str,
    expert_rows: list[dict[str, str]],
    preference_rows: list[dict[str, str]],
    utility_rows: list[dict[str, str]],
    representation_summary_dir: Path,
    representation_summary_rows: list[dict[str, str]],
    representation_paired_rows: list[dict[str, str]],
    iterative_summary_dir: Path,
    iterative_summary_rows: list[dict[str, str]],
    iterative_paired_rows: list[dict[str, str]],
) -> dict[str, object]:
    h2 = find_expert_claim(
        expert_rows,
        dataset,
        "H2 ordinary gate beats validation-selected fixed alpha",
    )
    h3 = find_expert_claim(
        expert_rows,
        dataset,
        "H3 reliability adds value beyond ordinary gating",
    )
    h4 = find_expert_claim(
        expert_rows,
        dataset,
        "H4 global expert provides complementary predictions",
    )

    pref_rel = find_router_row(preference_rows, dataset, "reliability_only")
    pref_feat = find_router_row_any(
        preference_rows,
        dataset,
        "node_feature_only",
        "feature_only",
    )
    pref_combined = find_router_row(preference_rows, dataset, "combined")

    utility_rel = find_router_row(utility_rows, dataset, "reliability_only")
    utility_feat = find_router_row_any(
        utility_rows,
        dataset,
        "node_feature_only",
        "feature_only",
    )
    utility_combined = find_router_row(utility_rows, dataset, "combined")

    repr_frozen_rel = find_summary_row(
        representation_summary_rows,
        dataset,
        "hidden_mixing_frozen",
        "reliability_only",
    )
    repr_frozen_combined = find_summary_row(
        representation_summary_rows,
        dataset,
        "hidden_mixing_frozen",
        "combined",
    )
    repr_finetune_rel = find_summary_row(
        representation_summary_rows,
        dataset,
        "hidden_mixing_finetune",
        "reliability_only",
    )
    repr_finetune_combined = find_summary_row(
        representation_summary_rows,
        dataset,
        "hidden_mixing_finetune",
        "combined",
    )

    iterative_frozen_rel = find_summary_row(
        iterative_summary_rows,
        dataset,
        "iterative_relation_frozen",
        "reliability_only",
    )
    iterative_finetune_rel = find_summary_row(
        iterative_summary_rows,
        dataset,
        "iterative_relation_finetune",
        "reliability_only",
    )

    return {
        "dataset": dataset,
        "expert_h2_status": claim_status(h2),
        "expert_h2_delta": claim_estimate(h2),
        "expert_h3_status": claim_status(h3),
        "expert_h3_delta": claim_estimate(h3),
        "expert_h4_status": claim_status(h4),
        "expert_h4_estimate": claim_estimate(h4),
        "preference_rel_auc": get_float(pref_rel, "test_preference_auc_mean"),
        "preference_feature_auc": get_float(pref_feat, "test_preference_auc_mean"),
        "preference_combined_auc": get_float(pref_combined, "test_preference_auc_mean"),
        "preference_rel_minus_feature_auc": diff(
            get_float(pref_rel, "test_preference_auc_mean"),
            get_float(pref_feat, "test_preference_auc_mean"),
        ),
        "preference_combined_minus_feature_auc": diff(
            get_float(pref_combined, "test_preference_auc_mean"),
            get_float(pref_feat, "test_preference_auc_mean"),
        ),
        "utility_fixed_alpha": get_float(
            utility_rel,
            "validation_selected_fixed_alpha_test_accuracy_mean",
        ),
        "utility_oracle_union": get_float(
            utility_rel,
            "test_oracle_union_accuracy_mean",
        ),
        "utility_headroom": diff(
            get_float(utility_rel, "test_oracle_union_accuracy_mean"),
            get_float(
                utility_rel,
                "validation_selected_fixed_alpha_test_accuracy_mean",
            ),
        ),
        "utility_rel_minus_fixed": diff(
            get_float(utility_rel, "test_utility_routed_node_accuracy_mean"),
            get_float(
                utility_rel,
                "validation_selected_fixed_alpha_test_accuracy_mean",
            ),
        ),
        "utility_combined_minus_fixed": diff(
            get_float(utility_combined, "test_utility_routed_node_accuracy_mean"),
            get_float(
                utility_combined,
                "validation_selected_fixed_alpha_test_accuracy_mean",
            ),
        ),
        "utility_combined_minus_feature_router": diff(
            get_float(utility_combined, "test_utility_routed_node_accuracy_mean"),
            get_float(utility_feat, "test_utility_routed_node_accuracy_mean"),
        ),
        "repr_frozen_rel_minus_fixed": get_paired_delta(
            representation_paired_rows,
            dataset,
            "hidden_mixing_frozen",
            "reliability_only - fixed",
        ),
        "repr_frozen_true_minus_shuffled": get_paired_delta(
            representation_paired_rows,
            dataset,
            "hidden_mixing_frozen",
            "true reliability - shuffled reliability",
        ),
        "repr_frozen_combined_minus_feature": get_paired_delta(
            representation_paired_rows,
            dataset,
            "hidden_mixing_frozen",
            "combined - feature_only",
        ),
        "repr_finetune_rel_minus_fixed": get_paired_delta(
            representation_paired_rows,
            dataset,
            "hidden_mixing_finetune",
            "reliability_only - fixed",
        ),
        "repr_finetune_true_minus_shuffled": get_paired_delta(
            representation_paired_rows,
            dataset,
            "hidden_mixing_finetune",
            "true reliability - shuffled reliability",
        ),
        "repr_finetune_true_minus_constant": get_paired_delta(
            representation_paired_rows,
            dataset,
            "hidden_mixing_finetune",
            "true reliability - constant reliability",
        ),
        "repr_finetune_combined_minus_feature": get_paired_delta(
            representation_paired_rows,
            dataset,
            "hidden_mixing_finetune",
            "combined - feature_only",
        ),
        "repr_frozen_alpha_corr_degree": summary_stat(
            repr_frozen_rel,
            representation_summary_dir,
            dataset,
            "hidden_mixing_frozen",
            "reliability_only",
            "alpha_corr_raw_degree",
            "alpha_corr_degree",
        ),
        "repr_frozen_alpha_corr_neighbor_variance": summary_stat(
            repr_frozen_rel,
            representation_summary_dir,
            dataset,
            "hidden_mixing_frozen",
            "reliability_only",
            "alpha_corr_raw_neighbor_variance",
            "alpha_corr_neighbor_variance",
        ),
        "repr_finetune_alpha_corr_degree": summary_stat(
            repr_finetune_rel,
            representation_summary_dir,
            dataset,
            "hidden_mixing_finetune",
            "reliability_only",
            "alpha_corr_raw_degree",
            "alpha_corr_degree",
        ),
        "repr_finetune_alpha_corr_neighbor_variance": summary_stat(
            repr_finetune_rel,
            representation_summary_dir,
            dataset,
            "hidden_mixing_finetune",
            "reliability_only",
            "alpha_corr_raw_neighbor_variance",
            "alpha_corr_neighbor_variance",
        ),
        "iterative_frozen_rel_minus_fixed": get_paired_delta(
            iterative_paired_rows,
            dataset,
            "iterative_relation_frozen",
            "reliability_only - fixed",
        ),
        "iterative_frozen_true_minus_shuffled": get_paired_delta(
            iterative_paired_rows,
            dataset,
            "iterative_relation_frozen",
            "true reliability - shuffled reliability",
        ),
        "iterative_frozen_true_minus_constant": get_paired_delta(
            iterative_paired_rows,
            dataset,
            "iterative_relation_frozen",
            "true reliability - constant reliability",
        ),
        "iterative_finetune_rel_minus_fixed": get_paired_delta(
            iterative_paired_rows,
            dataset,
            "iterative_relation_finetune",
            "reliability_only - fixed",
        ),
        "iterative_finetune_true_minus_shuffled": get_paired_delta(
            iterative_paired_rows,
            dataset,
            "iterative_relation_finetune",
            "true reliability - shuffled reliability",
        ),
        "iterative_finetune_true_minus_constant": get_paired_delta(
            iterative_paired_rows,
            dataset,
            "iterative_relation_finetune",
            "true reliability - constant reliability",
        ),
        "iterative_frozen_alpha_std": summary_stat(
            iterative_frozen_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_frozen",
            "reliability_only",
            "alpha_std",
        ),
        "iterative_frozen_adjustment_mean": summary_stat(
            iterative_frozen_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_frozen",
            "reliability_only",
            "adjustment_mean",
        ),
        "iterative_frozen_relation_to_base_norm": summary_stat(
            iterative_frozen_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_frozen",
            "reliability_only",
            "relation_to_base_norm",
        ),
        "iterative_frozen_update_gate_mean": summary_stat(
            iterative_frozen_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_frozen",
            "reliability_only",
            "relation_update_gate_mean",
        ),
        "iterative_frozen_alpha_corr_degree": summary_stat(
            iterative_frozen_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_frozen",
            "reliability_only",
            "alpha_corr_degree",
            "alpha_corr_raw_degree",
        ),
        "iterative_frozen_alpha_corr_neighbor_variance": summary_stat(
            iterative_frozen_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_frozen",
            "reliability_only",
            "alpha_corr_neighbor_variance",
            "alpha_corr_raw_neighbor_variance",
        ),
        "iterative_finetune_alpha_std": summary_stat(
            iterative_finetune_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_finetune",
            "reliability_only",
            "alpha_std",
        ),
        "iterative_finetune_adjustment_mean": summary_stat(
            iterative_finetune_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_finetune",
            "reliability_only",
            "adjustment_mean",
        ),
        "iterative_finetune_relation_to_base_norm": summary_stat(
            iterative_finetune_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_finetune",
            "reliability_only",
            "relation_to_base_norm",
        ),
        "iterative_finetune_update_gate_mean": summary_stat(
            iterative_finetune_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_finetune",
            "reliability_only",
            "relation_update_gate_mean",
        ),
        "iterative_finetune_alpha_corr_degree": summary_stat(
            iterative_finetune_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_finetune",
            "reliability_only",
            "alpha_corr_degree",
            "alpha_corr_raw_degree",
        ),
        "iterative_finetune_alpha_corr_neighbor_variance": summary_stat(
            iterative_finetune_rel,
            iterative_summary_dir,
            dataset,
            "iterative_relation_finetune",
            "reliability_only",
            "alpha_corr_neighbor_variance",
            "alpha_corr_raw_neighbor_variance",
        ),
        "diagnosis": dataset_diagnosis(
            dataset,
            h4,
            pref_rel,
            pref_feat,
            pref_combined,
            utility_rel,
            utility_combined,
            representation_paired_rows,
            iterative_paired_rows,
        ),
    }


def dataset_diagnosis(
    dataset: str,
    h4: dict[str, str] | None,
    pref_rel: dict[str, str] | None,
    pref_feat: dict[str, str] | None,
    pref_combined: dict[str, str] | None,
    utility_rel: dict[str, str] | None,
    utility_combined: dict[str, str] | None,
    representation_paired_rows: list[dict[str, str]],
    iterative_paired_rows: list[dict[str, str]],
) -> str:
    rel_pref_gain = diff(
        get_float(pref_rel, "test_preference_auc_mean"),
        get_float(pref_feat, "test_preference_auc_mean"),
    )
    combined_pref_gain = diff(
        get_float(pref_combined, "test_preference_auc_mean"),
        get_float(pref_feat, "test_preference_auc_mean"),
    )
    utility_headroom = diff(
        get_float(utility_rel, "test_oracle_union_accuracy_mean"),
        get_float(
            utility_rel,
            "validation_selected_fixed_alpha_test_accuracy_mean",
        ),
    )
    repr_gain = get_paired_delta(
        representation_paired_rows,
        dataset,
        "hidden_mixing_finetune",
        "reliability_only - fixed",
    )
    repr_true = get_paired_delta(
        representation_paired_rows,
        dataset,
        "hidden_mixing_finetune",
        "true reliability - shuffled reliability",
    )
    repr_const = get_paired_delta(
        representation_paired_rows,
        dataset,
        "hidden_mixing_finetune",
        "true reliability - constant reliability",
    )
    iter_frozen_gain = get_paired_delta(
        iterative_paired_rows,
        dataset,
        "iterative_relation_frozen",
        "reliability_only - fixed",
    )
    iter_frozen_true = get_paired_delta(
        iterative_paired_rows,
        dataset,
        "iterative_relation_frozen",
        "true reliability - shuffled reliability",
    )
    iter_frozen_const = get_paired_delta(
        iterative_paired_rows,
        dataset,
        "iterative_relation_frozen",
        "true reliability - constant reliability",
    )
    iter_ft_gain = get_paired_delta(
        iterative_paired_rows,
        dataset,
        "iterative_relation_finetune",
        "reliability_only - fixed",
    )
    iter_ft_true = get_paired_delta(
        iterative_paired_rows,
        dataset,
        "iterative_relation_finetune",
        "true reliability - shuffled reliability",
    )
    iter_ft_const = get_paired_delta(
        iterative_paired_rows,
        dataset,
        "iterative_relation_finetune",
        "true reliability - constant reliability",
    )
    if positive_against_controls(iter_frozen_gain, iter_frozen_true, iter_frozen_const):
        return "iterative-relation-frozen-positive"
    if positive_against_controls(iter_ft_gain, iter_ft_true, iter_ft_const):
        return "iterative-relation-finetune-positive"
    if positive_against_controls(repr_gain, repr_true, repr_const):
        return "legacy-hidden-mixing-positive"
    if positive_missing_constant(iter_frozen_gain, iter_frozen_true, iter_frozen_const):
        return "iterative-relation-frozen-positive-missing-constant"
    if positive_missing_constant(iter_ft_gain, iter_ft_true, iter_ft_const):
        return "iterative-relation-finetune-positive-missing-constant"
    if positive_missing_constant(repr_gain, repr_true, repr_const):
        return "legacy-hidden-mixing-positive-missing-constant"
    if combined_pref_gain > 0.02 and utility_headroom <= 0.01:
        return "preference-signal-but-little-utility-headroom"
    if (
        rel_pref_gain > 0.01
        and present_values_all_leq(
            (
                iter_ft_gain,
                iter_ft_true,
                iter_ft_const,
                repr_gain,
                repr_true,
                repr_const,
            ),
            0.002,
        )
    ):
        return "preference-signal-not-converted"
    if claim_status(h4) == "SUPPORTED" and utility_headroom > 0.02:
        return "expert-complementarity-with-unrealized-headroom"
    return "mixed-or-negative"


def render_report(
    rows: list[dict[str, object]],
    missing_layers: list[str],
) -> str:
    lines = [
        "# Mechanism Diagnosis",
        "",
        "This report aligns four evidence layers:",
        "",
        "1. expert complementarity and fixed-alpha fallback,",
        "2. preference routing signal,",
        "3. utility routing conversion,",
        "4. representation-control conversion.",
        "",
    ]
    if missing_layers:
        lines.extend(
            [
                "Missing evidence layers:",
                "",
                *[f"- {label}" for label in missing_layers],
                "",
            ]
        )
    lines.extend(
        [
        "",
        "## Scorecard",
        "",
        "| Dataset | Expert H4 | Pref rel-feat AUC | Pref comb-feat AUC | Utility headroom | Iter K1 ft rel-fixed | Iter K1 ft true-shuffled | Iter K1 ft true-constant | Iter K1 ft rel/base | Iter K1 ft alpha std | Legacy repr ft true-shuffled | Diagnosis |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['expert_h4_status']} | "
            f"{fmt(row['preference_rel_minus_feature_auc'])} | "
            f"{fmt(row['preference_combined_minus_feature_auc'])} | "
            f"{fmt(row['utility_headroom'])} | "
            f"{fmt(row['iterative_finetune_rel_minus_fixed'])} | "
            f"{fmt(row['iterative_finetune_true_minus_shuffled'])} | "
            f"{fmt(row['iterative_finetune_true_minus_constant'])} | "
            f"{fmt(row['iterative_finetune_relation_to_base_norm'])} | "
            f"{fmt(row['iterative_finetune_alpha_std'])} | "
            f"{fmt(row['repr_finetune_true_minus_shuffled'])} | "
            f"{row['diagnosis']} |"
        )
    lines.extend(
        [
            "",
            "## Dataset Notes",
            "",
        ]
    )
    for row in rows:
        lines.extend(
            [
                f"### {row['dataset']}",
                "",
                f"- Expert complementarity: {row['expert_h4_status']} "
                f"({fmt(row['expert_h4_estimate'])}).",
                f"- Preference routing: reliability-feature AUC delta "
                f"{fmt(row['preference_rel_minus_feature_auc'])}, combined-feature AUC delta "
                f"{fmt(row['preference_combined_minus_feature_auc'])}.",
                f"- Utility routing headroom: oracle-fixed delta "
                f"{fmt(row['utility_headroom'])}; reliability router-fixed delta "
                f"{fmt(row['utility_rel_minus_fixed'])}; combined router-fixed delta "
                f"{fmt(row['utility_combined_minus_fixed'])}.",
                f"- Iterative relation K=1: frozen reliability-fixed "
                f"{fmt(row['iterative_frozen_rel_minus_fixed'])}; frozen true-shuffled "
                f"{fmt(row['iterative_frozen_true_minus_shuffled'])}; frozen true-constant "
                f"{fmt(row['iterative_frozen_true_minus_constant'])}; finetune reliability-fixed "
                f"{fmt(row['iterative_finetune_rel_minus_fixed'])}; finetune true-shuffled "
                f"{fmt(row['iterative_finetune_true_minus_shuffled'])}; finetune true-constant "
                f"{fmt(row['iterative_finetune_true_minus_constant'])}.",
                f"- Iterative mechanism stats: finetune alpha std "
                f"{fmt(row['iterative_finetune_alpha_std'])}; finetune adjustment mean "
                f"{fmt(row['iterative_finetune_adjustment_mean'])}; finetune relation/base "
                f"{fmt(row['iterative_finetune_relation_to_base_norm'])}; finetune update gate "
                f"{fmt(row['iterative_finetune_update_gate_mean'])}; finetune alpha corr degree "
                f"{fmt(row['iterative_finetune_alpha_corr_degree'])}; finetune alpha corr neighbor variance "
                f"{fmt(row['iterative_finetune_alpha_corr_neighbor_variance'])}.",
                f"- Representation control: finetune reliability-fixed "
                f"{fmt(row['repr_finetune_rel_minus_fixed'])}; finetune true-shuffled "
                f"{fmt(row['repr_finetune_true_minus_shuffled'])}; finetune true-constant "
                f"{fmt(row['repr_finetune_true_minus_constant'])}.",
                f"- Diagnosis: `{row['diagnosis']}`.",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def find_expert_claim(
    rows: list[dict[str, str]],
    dataset: str,
    claim: str,
) -> dict[str, str] | None:
    for row in rows:
        if row.get("dataset") == dataset and row.get("claim") == claim:
            return row
    return None


def find_router_row(
    rows: list[dict[str, str]],
    dataset: str,
    router: str,
) -> dict[str, str] | None:
    for row in rows:
        if row.get("dataset") == dataset and row.get("router") == router:
            return row
    return None


def find_router_row_any(
    rows: list[dict[str, str]],
    dataset: str,
    *routers: str,
) -> dict[str, str] | None:
    for router in routers:
        row = find_router_row(rows, dataset, router)
        if row is not None:
            return row
    return None


def find_summary_row(
    rows: list[dict[str, str]],
    dataset: str,
    family: str,
    control_mode: str,
) -> dict[str, str] | None:
    for row in rows:
        if (
            row.get("dataset") == dataset
            and row.get("family") == family
            and row.get("control_mode") == control_mode
        ):
            return row
    return None


def get_paired_delta(
    rows: list[dict[str, str]],
    dataset: str,
    family: str,
    comparison: str,
) -> float:
    for row in rows:
        if (
            row.get("dataset") == dataset
            and row.get("family") == family
            and row.get("comparison") == comparison
        ):
            return get_float(row, "mean_delta")
    return math.nan


def summary_stat(
    row: dict[str, str] | None,
    summary_dir: Path,
    dataset: str,
    family: str,
    control_mode: str,
    *keys: str,
) -> float:
    value = get_float_any(row, *keys)
    if not math.isnan(value):
        return value
    raw_path = summary_dir / f"{dataset}_{family}_{control_mode}.csv"
    raw_rows = read_csv_if_exists(raw_path)
    if not raw_rows:
        return math.nan
    values = [
        get_float_any(raw_row, *keys)
        for raw_row in raw_rows
    ]
    values = [value for value in values if not math.isnan(value)]
    if not values:
        return math.nan
    return sum(values) / len(values)


def claim_status(row: dict[str, str] | None) -> str:
    if row is None:
        return "n/a"
    return row.get("status", "n/a")


def claim_estimate(row: dict[str, str] | None) -> float:
    return get_float(row, "estimate")


def collect_datasets(rows: list[dict[str, str]]) -> set[str]:
    return {row["dataset"] for row in rows if row.get("dataset")}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_csv_if_exists(path: Path) -> list[dict[str, str]]:
    return read_csv(path) if path.exists() else []


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        if not rows:
            handle.write("")
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def get_float(row: dict[str, str] | None, key: str) -> float:
    if row is None:
        return math.nan
    value = row.get(key, "")
    if value in {"", "nan", "NaN", None}:
        return math.nan
    return float(value)


def get_float_any(row: dict[str, str] | None, *keys: str) -> float:
    for key in keys:
        value = get_float(row, key)
        if not math.isnan(value):
            return value
    return math.nan


def diff(left: float, right: float) -> float:
    if math.isnan(left) or math.isnan(right):
        return math.nan
    return left - right


def positive_against_controls(
    gain: float,
    shuffled_gain: float,
    constant_gain: float,
) -> bool:
    return (
        not math.isnan(gain)
        and not math.isnan(shuffled_gain)
        and not math.isnan(constant_gain)
        and gain > 0.005
        and shuffled_gain > 0.005
        and constant_gain > 0.005
    )


def positive_missing_constant(
    gain: float,
    shuffled_gain: float,
    constant_gain: float,
) -> bool:
    return (
        not math.isnan(gain)
        and not math.isnan(shuffled_gain)
        and math.isnan(constant_gain)
        and gain > 0.005
        and shuffled_gain > 0.005
    )


def present_values_all_leq(values: tuple[float, ...], threshold: float) -> bool:
    present = [value for value in values if not math.isnan(value)]
    return bool(present) and all(value <= threshold for value in present)


def fmt(value: object) -> str:
    if not isinstance(value, (int, float)):
        return str(value)
    if math.isnan(value):
        return "n/a"
    return f"{value:+.4f}"


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


if __name__ == "__main__":
    main()
