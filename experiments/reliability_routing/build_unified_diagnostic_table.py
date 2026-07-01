from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


DATASET_RESULT_DIRS = {
    "Roman-empire": "phaseC_rw8_dim32_confirm_r10",
    "Amazon-ratings": "phaseC_rw8_dim32_confirm_r10",
    "Questions": "phaseC1_questions_bestparams_channel_r10",
    "Squirrel": "phaseC1_squirrel_bestparams_channel_r10",
    "Texas": "webkb_best_config_screen",
    "Cornell": "webkb_best_config_screen",
    "Wisconsin": "webkb_best_config_screen",
    "Actor": "phaseC0_existing_datasets_channel_screen",
    "Minesweeper": "phaseC0_existing_datasets_channel_screen",
}

DATASET_ORDER = (
    "Roman-empire",
    "Questions",
    "Amazon-ratings",
    "Texas",
    "Cornell",
    "Wisconsin",
    "Squirrel",
    "Actor",
    "Minesweeper",
)

CONTROL_COLUMNS = {
    "fixed": "fixed",
    "reliability_only": "reliability_only",
    "shuffled_reliability": "shuffled",
    "constant_reliability": "constant",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outputs-root", type=Path, default=Path("outputs"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/unified_diagnostics"))
    parser.add_argument(
        "--family",
        default="iterative_relation_finetune",
        help="Family used for the main representation-control columns.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary_rows, paired_rows = load_representation_rows(args.outputs_root)
    preference_auc = load_preference_auc(args.outputs_root)
    headroom = load_headroom(args.outputs_root)
    mechanism = load_node_mechanism(args.outputs_root)

    rows = []
    for dataset in DATASET_ORDER:
        row = build_dataset_row(
            dataset,
            args.family,
            summary_rows,
            paired_rows,
            preference_auc,
            headroom,
            mechanism,
        )
        rows.append(row)
    write_csv(args.out_dir / "unified_diagnostic_table.csv", rows)
    write_markdown(args.out_dir / "analysis.md", rows)
    print(f"saved: {(args.out_dir / 'unified_diagnostic_table.csv').resolve()}")
    print(f"analysis: {(args.out_dir / 'analysis.md').resolve()}")


def load_representation_rows(outputs_root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    summaries = []
    paired = []
    for dataset, dirname in DATASET_RESULT_DIRS.items():
        root = outputs_root / dirname
        summary_path = root / "summary.csv"
        paired_path = root / "paired_comparisons.csv"
        if summary_path.exists():
            for row in read_csv(summary_path):
                if row.get("dataset") == dataset:
                    row["_source_dir"] = dirname
                    summaries.append(row)
        if paired_path.exists():
            for row in read_csv(paired_path):
                if row.get("dataset") == dataset:
                    row["_source_dir"] = dirname
                    paired.append(row)
    return summaries, paired


def load_preference_auc(outputs_root: Path) -> dict[str, float]:
    output: dict[str, float] = {}
    for path in (
        outputs_root / "preference_routing_full_v3" / "summary.csv",
        outputs_root / "preference_routing_sanity_v2" / "summary.csv",
    ):
        if not path.exists():
            continue
        for row in read_csv(path):
            if row.get("router") == "reliability_only":
                output.setdefault(row["dataset"], to_float(row.get("test_preference_auc_mean")))
    return output


def load_headroom(outputs_root: Path) -> dict[str, dict[str, float]]:
    path = outputs_root / "expert_headroom_diagnosis_v1" / "expert_headroom.csv"
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    if path.exists():
        for row in read_csv(path):
            dataset = row.get("dataset", "")
            for key in (
                "oracle_union_minus_best_fixed",
                "oracle_union_minus_best_single",
                "disagreement_rate",
            ):
                value = to_float(row.get(key))
                if is_finite(value):
                    grouped[dataset][key].append(value)
    return {
        dataset: {key: mean(values) for key, values in metrics.items()}
        for dataset, metrics in grouped.items()
    }


def load_node_mechanism(outputs_root: Path) -> dict[str, dict[str, float]]:
    path = outputs_root / "node_mechanism_diagnosis_with_alignment" / "node_mechanism_summary.csv"
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    if path.exists():
        for row in read_csv(path):
            if row.get("family") != "iterative_relation_finetune":
                continue
            if row.get("control_mode") not in {"reliability_only", "combined"}:
                continue
            dataset = row.get("dataset", "")
            for key in (
                "alpha_auc_for_local_preference",
                "alpha_corr_local_advantage",
                "alpha_gap_local_minus_global",
            ):
                value = to_float(row.get(key))
                if is_finite(value):
                    grouped[dataset][key].append(value)
    return {
        dataset: {key: mean(values) for key, values in metrics.items()}
        for dataset, metrics in grouped.items()
    }


def build_dataset_row(
    dataset: str,
    family: str,
    summary_rows: list[dict[str, str]],
    paired_rows: list[dict[str, str]],
    preference_auc: dict[str, float],
    headroom: dict[str, dict[str, float]],
    mechanism: dict[str, dict[str, float]],
) -> dict[str, object]:
    row: dict[str, object] = {
        "dataset": dataset,
        "family": family,
        "source_dir": DATASET_RESULT_DIRS.get(dataset, ""),
        "metric": "",
    }
    by_control = {}
    for item in summary_rows:
        if item.get("dataset") == dataset and item.get("family") == family:
            by_control[item.get("control_mode", "")] = item
    for control, column in CONTROL_COLUMNS.items():
        item = by_control.get(control, {})
        row[column] = to_float(item.get("test_primary_mean"))
        row["metric"] = row["metric"] or item.get("primary_metric", "")
    row["true_minus_fixed"] = diff(row.get("reliability_only"), row.get("fixed"))
    row["true_minus_shuffled"] = comparison_delta(
        paired_rows,
        dataset,
        family,
        "true reliability - shuffled reliability",
    )
    row["true_minus_constant"] = comparison_delta(
        paired_rows,
        dataset,
        family,
        "true reliability - constant reliability",
    )
    rel_item = by_control.get("reliability_only", {})
    row["relation_strength"] = to_float(rel_item.get("relation_relative_strength"))
    row["relation_disagreement"] = to_float(rel_item.get("relation_to_branch_disagreement"))
    row["alpha_std"] = to_float(rel_item.get("alpha_std"))
    row["alpha_mean"] = to_float(rel_item.get("alpha_mean"))
    row["oracle_union_gap"] = headroom.get(dataset, {}).get("oracle_union_minus_best_fixed", math.nan)
    row["oracle_gap_single"] = headroom.get(dataset, {}).get("oracle_union_minus_best_single", math.nan)
    row["expert_disagreement_rate"] = headroom.get(dataset, {}).get("disagreement_rate", math.nan)
    row["preference_auc"] = preference_auc.get(dataset, math.nan)
    row["alpha_preference_auc"] = mechanism.get(dataset, {}).get("alpha_auc_for_local_preference", math.nan)
    row["alpha_corr_local_advantage"] = mechanism.get(dataset, {}).get("alpha_corr_local_advantage", math.nan)
    row["status"] = classify(row)
    return row


def comparison_delta(
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
            return to_float(row.get("mean_delta"))
    return math.nan


def classify(row: dict[str, object]) -> str:
    true_fixed = row.get("true_minus_fixed", math.nan)
    true_shuf = row.get("true_minus_shuffled", math.nan)
    true_const = row.get("true_minus_constant", math.nan)
    if is_finite(true_shuf) and is_finite(true_const):
        if true_shuf > 0.002 and true_const > 0.002 and true_fixed > 0:
            return "positive"
        if abs(true_shuf) < 1e-9 and abs(true_const) < 1e-9:
            return "not reliability-specific"
        if true_shuf <= 0 or true_const <= 0:
            return "negative/control-failed"
    return "needs more diagnostics"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Unified Diagnostic Table",
        "",
        "This table aggregates existing representation-control, headroom, preference-routing, and node-mechanism outputs. Blank values mean the diagnostic has not been run for that dataset yet.",
        "",
        "| Dataset | Metric | Fixed | True | Shuffled | Constant | True-Fixed | True-Shuffled | True-Constant | Rel strength | Rel/disagree | Alpha std | Oracle gap | Pref AUC | Status |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {dataset} | {metric} | {fixed} | {true} | {shuffled} | {constant} | "
            "{tf} | {ts} | {tc} | {rs} | {rd} | {astd} | {ogap} | {pauc} | {status} |".format(
                dataset=row["dataset"],
                metric=row.get("metric", ""),
                fixed=fmt(row.get("fixed")),
                true=fmt(row.get("reliability_only")),
                shuffled=fmt(row.get("shuffled")),
                constant=fmt(row.get("constant")),
                tf=fmt(row.get("true_minus_fixed"), signed=True),
                ts=fmt(row.get("true_minus_shuffled"), signed=True),
                tc=fmt(row.get("true_minus_constant"), signed=True),
                rs=fmt(row.get("relation_strength")),
                rd=fmt(row.get("relation_disagreement")),
                astd=fmt(row.get("alpha_std")),
                ogap=fmt(row.get("oracle_union_gap"), signed=True),
                pauc=fmt(row.get("preference_auc")),
                status=row.get("status", ""),
            )
        )
    lines += [
        "",
        "## Reading",
        "",
        "- `True` is `reliability_only` under the selected representation-control family.",
        "- A dataset is a positive candidate only when true reliability beats fixed and also beats shuffled/constant reliability.",
        "- `Oracle gap` and `Pref AUC` are imported from prior diagnostic runs when available; missing values should be filled before final claims.",
    ]
    path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")


def to_float(value: object) -> float:
    try:
        if value is None or value == "":
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def is_finite(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def diff(left: object, right: object) -> float:
    left_v = to_float(left)
    right_v = to_float(right)
    if not is_finite(left_v) or not is_finite(right_v):
        return math.nan
    return left_v - right_v


def fmt(value: object, signed: bool = False) -> str:
    value_f = to_float(value)
    if not is_finite(value_f):
        return ""
    if signed:
        return f"{value_f:+.4f}"
    return f"{value_f:.4f}"


if __name__ == "__main__":
    main()
