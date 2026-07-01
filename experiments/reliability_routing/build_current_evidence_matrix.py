from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
OUT_DIR = OUTPUTS / "evidence_matrix"
UNIFIED_PATH = OUTPUTS / "unified_diagnostics_v1" / "unified_diagnostic_table.csv"
REAL_SUITE_PATH = (
    OUTPUTS / "archive" / "2026-06-19" / "04_real_data" / "real_suite" / "summary.csv"
)
GRAPHGPS_ROOT = ROOT.parents[1] / "GraphGPS-main"
PREFERENCE_SUMMARY_PATH = OUTPUTS / "preference_routing_full_v3" / "summary.csv"
HEADROOM_SUMMARY_PATH = OUTPUTS / "expert_headroom_diagnosis_v1" / "dataset_summary.csv"

EXTRA_SUMMARY_SOURCES = {
    "Tolokers": {
        "path": OUTPUTS / "iterative_relation_binary_k1_screen" / "summary.csv",
        "family": "iterative_relation_finetune",
        "source": "iterative_relation_binary_k1_screen",
    },
    "Chameleon": {
        "path": OUTPUTS / "phaseC0_existing_datasets_channel_screen" / "summary.csv",
        "family": "iterative_relation_finetune",
        "source": "phaseC0_existing_datasets_channel_screen",
    },
}


DATASET_NOTES = {
    "Roman-empire": {
        "group": "main positive",
        "verdict": "strong positive",
        "paper_use": "main positive",
        "reliability_specific": "yes",
        "config_tag": "dim32-rw8-channel",
        "protocol_level": "main 10-run current best",
        "role": "cleanest evidence that reliability-conditioned local/global correction can work",
        "next": "final package: same-protocol GraphGPS check, mechanism closure, causal intervention",
    },
    "Questions": {
        "group": "boundary positive",
        "verdict": "weak / inconclusive positive",
        "paper_use": "supplemental weak evidence",
        "reliability_specific": "weak yes, finetune-only",
        "config_tag": "dim32-rw8-channel",
        "protocol_level": "supplemental 10-run",
        "role": "small ROC-AUC gain; useful as supplemental evidence only",
        "next": "fill headroom/preference diagnostics before claiming mechanism evidence",
    },
    "Amazon-ratings": {
        "group": "negative with headroom",
        "verdict": "negative / signal failure",
        "paper_use": "negative boundary",
        "reliability_specific": "no",
        "config_tag": "dim32-rw8-channel",
        "protocol_level": "main negative 10-run",
        "role": "rules out the idea that official undirected heterophily alone is enough",
        "next": "do not tune small parameters; use as failure case for signal expansion",
    },
    "Texas": {
        "group": "WebKB negative",
        "verdict": "negative",
        "paper_use": "negative boundary",
        "reliability_specific": "no",
        "config_tag": "webkb-best-config-screen",
        "protocol_level": "screening negative 3-run",
        "role": "WebKB does not provide Roman-like evidence",
        "next": "no 10-run confirmation",
    },
    "Cornell": {
        "group": "WebKB negative",
        "verdict": "non-specific controller effect",
        "paper_use": "negative boundary",
        "reliability_specific": "no, copied by shuffled/constant",
        "config_tag": "webkb-best-config-screen",
        "protocol_level": "screening negative 3-run",
        "role": "gain is copied by shuffled/constant reliability",
        "next": "no 10-run confirmation",
    },
    "Wisconsin": {
        "group": "WebKB negative",
        "verdict": "non-specific / negative",
        "paper_use": "negative boundary",
        "reliability_specific": "no, copied by shuffled/constant",
        "config_tag": "webkb-best-config-screen",
        "protocol_level": "screening negative 3-run",
        "role": "small gain is copied by controls; no node-level reliability effect",
        "next": "no 10-run confirmation",
    },
    "Squirrel": {
        "group": "protocol-sensitive stress test",
        "verdict": "negative/control-failed",
        "paper_use": "protocol caution only",
        "reliability_specific": "failed control",
        "config_tag": "dim32-rw8-channel",
        "protocol_level": "protocol caution 10-run",
        "role": "preference signal exists, but utility control does not beat shuffled/constant",
        "next": "only use for directed-sensitivity analysis",
    },
    "Chameleon": {
        "group": "protocol-sensitive stress test",
        "verdict": "protocol-sensitive / control-failed",
        "paper_use": "protocol caution only",
        "reliability_specific": "failed control",
        "config_tag": "phaseC0-channel-screen",
        "protocol_level": "protocol caution 3-run",
        "role": "available channel-screen run shows shuffled reliability above true reliability",
        "next": "only use for directed-sensitivity analysis",
    },
    "Actor": {
        "group": "negative",
        "verdict": "negative",
        "paper_use": "negative boundary",
        "reliability_specific": "no",
        "config_tag": "phaseC0-channel-screen",
        "protocol_level": "negative diagnostic 3-run",
        "role": "controller has essentially no effect under current setup",
        "next": "deprioritize",
    },
    "Minesweeper": {
        "group": "negative",
        "verdict": "negative",
        "paper_use": "negative boundary",
        "reliability_specific": "no",
        "config_tag": "phaseC0-channel-screen",
        "protocol_level": "negative diagnostic 3-run",
        "role": "ROC-AUC baseline is high and reliability controls do not change utility",
        "next": "deprioritize",
    },
    "Tolokers": {
        "group": "binary heterophily boundary",
        "verdict": "non-specific / weak",
        "paper_use": "negative boundary",
        "reliability_specific": "no, constant higher",
        "config_tag": "binary-k1-screen",
        "protocol_level": "binary ROC-AUC screening 3-run",
        "role": "available binary ROC-AUC screening; combined not summarized in this source and reliability-only is not the best control",
        "next": "do not treat as second positive unless a clean best-config 10-run beats shuffled/constant",
    },
    "Cora": {
        "group": "homophily fallback",
        "verdict": "fallback / old architecture under GCN",
        "paper_use": "historical diagnostic only",
        "reliability_specific": "not comparable",
        "config_tag": "old-real-suite",
        "protocol_level": "historical old-architecture 10-run",
        "role": "checks whether earlier GT-style modules damage homophily baselines",
        "next": "not a second-positive target",
    },
    "Citeseer": {
        "group": "homophily fallback",
        "verdict": "fallback / old architecture under GCN",
        "paper_use": "historical diagnostic only",
        "reliability_specific": "not comparable",
        "config_tag": "old-real-suite",
        "protocol_level": "historical old-architecture 10-run",
        "role": "checks whether earlier GT-style modules damage homophily baselines",
        "next": "not a second-positive target",
    },
    "Pubmed": {
        "group": "homophily fallback",
        "verdict": "fallback / old architecture under GCN",
        "paper_use": "historical diagnostic only",
        "reliability_specific": "not comparable",
        "config_tag": "old-real-suite",
        "protocol_level": "historical old-architecture 10-run",
        "role": "checks whether earlier GT-style modules damage homophily baselines",
        "next": "not a second-positive target",
    },
    "PascalVOC-SP": {
        "group": "broader benchmark",
        "verdict": "not yet summarized",
        "paper_use": "broader benchmark pending",
        "reliability_specific": "pending",
        "config_tag": "lrgb-edge-index-only",
        "protocol_level": "broader benchmark pending",
        "role": "tests whether the controller can be adapted to LRGB-style multi-graph tasks",
        "next": "do not treat as Roman-like evidence; run only as broader benchmark",
    },
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    unified = {row["dataset"]: row for row in read_csv(UNIFIED_PATH)}
    preferences = collect_preference_summaries()
    graphgps_all = collect_graphgps_all_results()
    graphgps = select_best_graphgps_results(graphgps_all)
    rows = []
    for dataset in [
        "Roman-empire",
        "Questions",
        "Amazon-ratings",
        "Minesweeper",
        "Tolokers",
        "Texas",
        "Cornell",
        "Wisconsin",
        "Cora",
        "Citeseer",
        "Pubmed",
        "Chameleon",
        "Squirrel",
        "Actor",
        "PascalVOC-SP",
    ]:
        rows.append(
            build_row(
                dataset,
                unified.get(dataset),
                graphgps.get(dataset),
                preferences.get(dataset, {}),
            )
        )
    write_csv(OUT_DIR / "current_evidence_matrix.csv", rows)
    write_csv(OUT_DIR / "graphgps_results.csv", graphgps_all)
    (OUT_DIR / "current_evidence_matrix.md").write_text(render_markdown(rows), encoding="utf-8")
    print(f"saved: {OUT_DIR / 'current_evidence_matrix.csv'}")
    print(f"saved: {OUT_DIR / 'graphgps_results.csv'}")
    print(f"saved: {OUT_DIR / 'current_evidence_matrix.md'}")


def build_row(
    dataset: str,
    unified_row: dict[str, str] | None,
    graphgps_row: dict[str, object] | None,
    preference_row: dict[str, object],
) -> dict[str, object]:
    note = DATASET_NOTES[dataset]
    row = {
        "dataset": dataset,
        "group": note["group"],
        "metric": "",
        "source": "",
        "runs": "",
        "family": "",
        "config_tag": note["config_tag"],
        "protocol_level": note["protocol_level"],
        "fixed": "",
        "feature_only": "",
        "reliability_only": "",
        "combined": "",
        "shuffled": "",
        "constant": "",
        "local_graphgps_repro": "",
        "local_graphgps_repro_source": "",
        "best_method": "",
        "best_value": "",
        "true_minus_fixed": "",
        "true_minus_shuffled": "",
        "true_minus_constant": "",
        "combined_minus_feature": "",
        "relation_strength": "",
        "alpha_std": "",
        "rel_pref_auc": "",
        "feature_pref_auc": "",
        "combined_pref_auc": "",
        "oracle_headroom": "",
        "verdict": note["verdict"],
        "reliability_specific": note["reliability_specific"],
        "paper_use": note["paper_use"],
        "evidence_role": note["role"],
        "next_action": note["next"],
    }
    if unified_row:
        row.update(
            {
                "metric": unified_row.get("metric", ""),
                "source": unified_row.get("source_dir", ""),
                "family": unified_row.get("family", ""),
                "fixed": pct(unified_row.get("fixed")),
                "reliability_only": pct(unified_row.get("reliability_only")),
                "shuffled": pct(unified_row.get("shuffled")),
                "constant": pct(unified_row.get("constant")),
                "true_minus_fixed": pp(unified_row.get("true_minus_fixed")),
                "true_minus_shuffled": pp(unified_row.get("true_minus_shuffled")),
                "true_minus_constant": pp(unified_row.get("true_minus_constant")),
                "relation_strength": num(unified_row.get("relation_strength")),
                "alpha_std": num(unified_row.get("alpha_std")),
                "rel_pref_auc": num(unified_row.get("preference_auc")),
                "oracle_headroom": pp(unified_row.get("oracle_union_gap")),
            }
        )
        add_summary_values(row, dataset, unified_row)
    elif dataset in EXTRA_SUMMARY_SOURCES:
        add_extra_summary_values(row, dataset)
    elif dataset in {"Cora", "Citeseer", "Pubmed"}:
        add_real_suite_values(row, dataset)

    add_preference_values(row, preference_row)
    add_graphgps_values(row, graphgps_row)
    mark_best(row)
    return row


def add_summary_values(row: dict[str, object], dataset: str, unified_row: dict[str, str]) -> None:
    source = unified_row.get("source_dir", "")
    family = unified_row.get("family", "")
    summary_path = OUTPUTS / source / "summary.csv"
    rows = read_csv(summary_path)
    controls = {
        item["control_mode"]: item
        for item in rows
        if item.get("dataset") == dataset and item.get("family") == family
    }
    if controls:
        row["runs"] = controls.get("fixed", {}).get("n", "")
        row["feature_only"] = pct(controls.get("feature_only", {}).get("test_primary_mean"))
        row["combined"] = pct(controls.get("combined", {}).get("test_primary_mean"))
        feature = to_float(controls.get("feature_only", {}).get("test_primary_mean"))
        combined = to_float(controls.get("combined", {}).get("test_primary_mean"))
        if math.isfinite(feature) and math.isfinite(combined):
            row["combined_minus_feature"] = pp(combined - feature)


def add_extra_summary_values(row: dict[str, object], dataset: str) -> None:
    source = EXTRA_SUMMARY_SOURCES[dataset]
    rows = read_csv(source["path"])
    controls = {
        item["control_mode"]: item
        for item in rows
        if item.get("dataset") == dataset and item.get("family") == source["family"]
    }
    if not controls:
        return
    fixed = controls.get("fixed", {})
    reliability = controls.get("reliability_only", {})
    shuffled = controls.get("shuffled_reliability", {})
    constant = controls.get("constant_reliability", {})
    feature = controls.get("feature_only", {})
    combined = controls.get("combined", {})
    row["metric"] = fixed.get("primary_metric", reliability.get("primary_metric", ""))
    row["source"] = source["source"]
    row["family"] = source["family"]
    row["runs"] = fixed.get("n", reliability.get("n", ""))
    row["fixed"] = pct(fixed.get("test_primary_mean"))
    row["feature_only"] = pct(feature.get("test_primary_mean"))
    row["reliability_only"] = pct(reliability.get("test_primary_mean"))
    row["combined"] = pct(combined.get("test_primary_mean"))
    row["shuffled"] = pct(shuffled.get("test_primary_mean"))
    row["constant"] = pct(constant.get("test_primary_mean"))
    true_value = to_float(reliability.get("test_primary_mean"))
    row["true_minus_fixed"] = pp(true_value - to_float(fixed.get("test_primary_mean")))
    row["true_minus_shuffled"] = pp(true_value - to_float(shuffled.get("test_primary_mean")))
    row["true_minus_constant"] = pp(true_value - to_float(constant.get("test_primary_mean")))
    row["combined_minus_feature"] = pp(
        to_float(combined.get("test_primary_mean")) - to_float(feature.get("test_primary_mean"))
    )
    row["relation_strength"] = num(reliability.get("relation_abs_mean"))
    row["alpha_std"] = num(reliability.get("alpha_std"))


def add_real_suite_values(row: dict[str, object], dataset: str) -> None:
    rows = read_csv(REAL_SUITE_PATH)
    by_model = {item["model"]: item for item in rows if item.get("dataset") == dataset}
    gcn = by_model.get("gcn", {})
    reliability = by_model.get("reliability_gt", {})
    gate = by_model.get("gate_gt", {})
    row["metric"] = "accuracy"
    row["source"] = "archive/2026-06-19/04_real_data/real_suite"
    row["family"] = "old_architecture"
    row["runs"] = gcn.get("n", "")
    row["fixed"] = pct(gcn.get("test_acc_mean"))
    row["reliability_only"] = pct(reliability.get("test_acc_mean"))
    row["combined"] = pct(gate.get("test_acc_mean"))
    row["true_minus_fixed"] = pp(
        to_float(reliability.get("test_acc_mean")) - to_float(gcn.get("test_acc_mean"))
    )


def collect_preference_summaries() -> dict[str, dict[str, object]]:
    output: dict[str, dict[str, object]] = {}
    for row in read_csv(HEADROOM_SUMMARY_PATH):
        output[row["dataset"]] = {
            "rel_pref_auc": row.get("reliability_preference_auc_mean", ""),
            "feature_pref_auc": row.get("feature_preference_auc_mean", ""),
            "combined_pref_auc": row.get("combined_preference_auc_mean", ""),
        }
    for row in read_csv(PREFERENCE_SUMMARY_PATH):
        dataset = row.get("dataset", "")
        router = row.get("router", "")
        output.setdefault(dataset, {})
        if router == "reliability_only":
            output[dataset]["rel_pref_auc"] = row.get("test_preference_auc_mean", "")
        elif router == "node_feature_only":
            output[dataset]["feature_pref_auc"] = row.get("test_preference_auc_mean", "")
        elif router == "combined":
            output[dataset]["combined_pref_auc"] = row.get("test_preference_auc_mean", "")
    return output


def add_preference_values(row: dict[str, object], preference_row: dict[str, object]) -> None:
    for key in ("rel_pref_auc", "feature_pref_auc", "combined_pref_auc"):
        if preference_row.get(key):
            row[key] = num(preference_row.get(key))


def collect_graphgps_all_results() -> list[dict[str, object]]:
    if not GRAPHGPS_ROOT.exists():
        return []
    results: list[dict[str, object]] = []
    for path in sorted(GRAPHGPS_ROOT.glob("results*/**/agg/test/best.json")):
        task = path.parents[2].name
        dataset = graphgps_dataset_name(task)
        if not dataset:
            continue
        payload = read_json(path)
        metric = "roc_auc" if dataset == "Questions" else "accuracy"
        key = "auc" if metric == "roc_auc" else "accuracy"
        value = to_float(payload.get(key))
        if not math.isfinite(value):
            continue
        results.append(
            {
                "dataset": dataset,
                "metric": metric,
                "value": f"{100.0 * value:.2f}",
                "std": f"{100.0 * to_float(payload.get(f'{key}_std')):.2f}",
                "accuracy": pct(payload.get("accuracy")),
                "accuracy_std": pct(payload.get("accuracy_std")),
                "roc_auc": pct(payload.get("auc")),
                "roc_auc_std": pct(payload.get("auc_std")),
                "f1": pct(payload.get("f1")),
                "f1_std": pct(payload.get("f1_std")),
                "epoch": payload.get("epoch", ""),
                "source": str(path.relative_to(GRAPHGPS_ROOT)),
            }
        )
    return results


def select_best_graphgps_results(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    output: dict[str, dict[str, object]] = {}
    for row in rows:
        dataset = str(row["dataset"])
        value = to_float(row["value"]) / 100.0
        previous = output.get(dataset)
        if previous is None or value > to_float(previous.get("value")):
            output[dataset] = {
                "metric": row["metric"],
                "value": value,
                "std": to_float(row.get("std")) / 100.0,
                "source": row["source"],
            }
    return output


def graphgps_dataset_name(task: str) -> str | None:
    name = task.removesuffix("-GPS")
    aliases = {
        "roman-empire": "Roman-empire",
        "questions": "Questions",
        "actor": "Actor",
        "wn-chameleon": "Chameleon",
        "wn-squirrel": "Squirrel",
        "webkb-tex": "Texas",
        "webkb-cor": "Cornell",
        "webkb-wis": "Wisconsin",
    }
    return aliases.get(name)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_graphgps_values(row: dict[str, object], graphgps_row: dict[str, object] | None) -> None:
    if not graphgps_row:
        return
    if row["metric"] and row["metric"] != graphgps_row["metric"]:
        return
    if not row["metric"]:
        row["metric"] = str(graphgps_row["metric"])
    row["local_graphgps_repro"] = pct(graphgps_row.get("value"))
    row["local_graphgps_repro_source"] = graphgps_row.get("source", "")


def mark_best(row: dict[str, object]) -> None:
    candidates = {
        "fixed": row.get("fixed"),
        "feature_only": row.get("feature_only"),
        "reliability_only": row.get("reliability_only"),
        "combined": row.get("combined"),
        "shuffled": row.get("shuffled"),
        "constant": row.get("constant"),
        "local_graphgps_repro": row.get("local_graphgps_repro"),
    }
    numeric = {name: to_float(value) for name, value in candidates.items()}
    numeric = {name: value for name, value in numeric.items() if math.isfinite(value)}
    if not numeric:
        return
    best_name, best_value = max(numeric.items(), key=lambda item: item[1])
    row["best_method"] = best_name
    row["best_value"] = f"{best_value:.2f}"


def render_markdown(rows: list[dict[str, object]]) -> str:
    lines = [
        "# Current Evidence Matrix",
        "",
        "This document consolidates the current evidence for whether structural reliability can control local/global representation correction.",
        "",
        "## Current Best Representation-Control Configuration",
        "",
        "| Parameter | Value |",
        "|---|---|",
        "| reliability_encoder_mode | component_concat |",
        "| reliability_component_dim | 32 |",
        "| component_missing_mode | zero_slot |",
        "| rw_steps | 8 |",
        "| alpha_type | channel |",
        "| relation_steps | 1 |",
        "| hidden_dim | 64 |",
        "| num_layers | 2 |",
        "| num_heads | 4 |",
        "| max_adjustment | 0.1 |",
        "| lambda_init | 0.001 |",
        "",
        "## Current Main Evidence Table",
        "",
        "| Dataset | Runs | Source | Config tag | Protocol level | Metric | Fixed | Reliability | Combined | Shuffled | Constant | Local GraphGPS Repro | Best | True-Fixed | True-Shuffled | True-Constant | Rel Pref AUC | Feature Pref AUC | Combined Pref AUC | Oracle Gap | Reliability-specific? | Paper Use | Verdict |",
        "|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    main_datasets = {
        "Roman-empire",
        "Questions",
        "Amazon-ratings",
        "Minesweeper",
        "Tolokers",
        "Texas",
        "Cornell",
        "Wisconsin",
        "Actor",
    }
    for row in rows:
        if row["dataset"] in main_datasets:
            lines.append(main_evidence_row(row))
    lines.extend(
        [
            "",
            "## Historical / Protocol-Caution Table",
            "",
            "| Dataset | Group | Runs | Source | Config tag | Protocol level | Metric | Fixed / Baseline | Reliability | Combined | Shuffled | Constant | Best | Reliability-specific? | Paper Use | Note |",
            "|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|",
        ]
    )
    caution_datasets = {"Cora", "Citeseer", "Pubmed", "Chameleon", "Squirrel"}
    for row in rows:
        if row["dataset"] in caution_datasets:
            lines.append(caution_row(row))
    lines.extend(
        [
            "",
            "## Broader Benchmark Table",
            "",
            "| Dataset | Metric | Status | Protocol note | Paper Use |",
            "|---|---|---|---|---|",
        ]
    )
    for row in rows:
        if row["dataset"] == "PascalVOC-SP":
            lines.append(
                "| PascalVOC-SP | weighted F1 | not yet summarized | edge-index-only adaptation; edge_attr ignored | broader benchmark pending |"
            )
    lines.extend(
        [
            "",
            "## Local GraphGPS Reproduction Table",
            "",
            "These are local reproductions under available configs, not values copied from the original GraphGPS paper.",
            "",
            "| Dataset | Metric | Best Local GraphGPS Repro | Source |",
            "|---|---|---:|---|",
        ]
    )
    for row in rows:
        if row.get("local_graphgps_repro"):
            lines.append(
                f"| {row['dataset']} | {row['metric']} | {row['local_graphgps_repro']} | {row['local_graphgps_repro_source']} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation By Category",
            "",
            "### Strong Positive",
            "",
            "- Roman-empire is the only clean strong positive so far. True reliability beats fixed, shuffled, and constant controls by about 2 pp under the current best configuration.",
            "- Roman values in this table use the current best `dim32-rw8-channel` configuration, not the earlier strength=0.10 formal confirm table.",
            "- Roman-empire also has strong preference separability when reliability is combined with node/features: Rel AUC 0.6997, Feature AUC 0.7674, Combined AUC 0.8379.",
            "- Local GraphGPS reproduction is integrated when a completed `agg/test/best.json` exists. Roman-empire local GraphGPS best is 84.15 accuracy, while our best current combined controller is 84.59.",
            "",
            "### Weak Or Inconclusive Positive",
            "",
            "- Questions shows a small 10-run ROC-AUC gain (+0.22 pp over fixed, +0.23 pp over shuffled), but the effect is small and headroom/preference diagnostics are missing. It is supplemental, not a second main positive yet.",
            "- Questions is therefore labeled `weak yes, finetune-only`, not a clean mechanism-positive dataset.",
            "- Questions local GraphGPS reproductions currently have lower ROC-AUC than our current best configuration, but this comparison should still be treated as local reproduction rather than an official benchmark claim.",
            "",
            "### Negative Or Non-Specific Evidence",
            "",
            "- Amazon-ratings has large oracle headroom, but current reliability preference AUC is weak and final utility does not improve.",
            "- Texas/Cornell/Wisconsin do not provide Roman-like evidence. Cornell/Wisconsin gains are copied by shuffled/constant controls, so they are non-specific controller effects.",
            "- WebKB should be treated as a family-level negative result: web/text/hyperlink structure alone is insufficient. This rules out the simple explanation that Roman works merely because it is a text/web graph.",
            "- Tolokers and Chameleon now have available run values in the table. Tolokers is from binary ROC-AUC screening with combined not summarized in that source; Chameleon is a protocol/control caution case. Neither is a clean second positive under the displayed controls.",
            "- Minesweeper, Actor, and the homophily fallback datasets do not currently support the main mechanism.",
            "",
            "### Protocol-Sensitive Stress Tests",
            "",
            "- Chameleon and Squirrel should not be treated as core evidence because edge protocol sensitivity and shuffled/constant controls make the story less clean.",
            "",
            "### Broader Benchmark",
            "",
            "- PascalVOC-SP is useful for checking whether the controller can be adapted to LRGB-style tasks, but it should not be used as Roman-like evidence unless the same reliability-specific controls pass.",
            "",
            "## Current Decision",
            "",
            "The prescreen wrapper should remain a utility, not a research centerpiece. The next research-relevant step is to find and load new candidate datasets, then use headroom/preference checks only as a gate before full representation-control runs.",
            "",
            "## Candidate Dataset Direction",
            "",
            "Priority candidates: LINKX wiki / Non-Homophily-Large-Scale wiki, Wiki-CS, genius, arxiv-year. These should be added with dataset validation and only then passed through the prescreen gate.",
        ]
    )
    return "\n".join(lines) + "\n"


def main_evidence_row(row: dict[str, object]) -> str:
    return (
        "| "
        f"{row['dataset']} | {row['runs']} | {row['source']} | "
        f"{row['config_tag']} | {row['protocol_level']} | {row['metric']} | "
        f"{display_value(row, 'fixed')} | {display_value(row, 'reliability_only')} | "
        f"{display_value(row, 'combined')} | {display_value(row, 'shuffled')} | "
        f"{display_value(row, 'constant')} | {display_value(row, 'local_graphgps_repro')} | "
        f"{row['best_method']} {row['best_value']} | {row['true_minus_fixed']} | "
        f"{row['true_minus_shuffled']} | {row['true_minus_constant']} | "
        f"{row['rel_pref_auc']} | {row['feature_pref_auc']} | {row['combined_pref_auc']} | "
        f"{row['oracle_headroom']} | {row['reliability_specific']} | {row['paper_use']} | {row['verdict']} |"
    )


def caution_row(row: dict[str, object]) -> str:
    return (
        "| "
        f"{row['dataset']} | {row['group']} | {row['runs']} | {row['source']} | "
        f"{row['config_tag']} | {row['protocol_level']} | {row['metric']} | "
        f"{display_value(row, 'fixed')} | {display_value(row, 'reliability_only')} | "
        f"{display_value(row, 'combined')} | {display_value(row, 'shuffled')} | "
        f"{display_value(row, 'constant')} | {row['best_method']} {row['best_value']} | "
        f"{row['reliability_specific']} | {row['paper_use']} | {row['evidence_role']} |"
    )


def display_value(row: dict[str, object], key: str) -> str:
    value = str(row.get(key, ""))
    if not value:
        return ""
    if row.get("best_method") == key:
        return f"**{value}**"
    return value


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: object) -> float:
    if value in {None, "", "nan", "NaN"}:
        return math.nan
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def pct(value: object) -> str:
    numeric = to_float(value)
    return "" if not math.isfinite(numeric) else f"{100.0 * numeric:.2f}"


def pp(value: object) -> str:
    numeric = to_float(value)
    return "" if not math.isfinite(numeric) else f"{100.0 * numeric:+.2f}"


def num(value: object) -> str:
    numeric = to_float(value)
    return "" if not math.isfinite(numeric) else f"{numeric:.4f}"


if __name__ == "__main__":
    main()
