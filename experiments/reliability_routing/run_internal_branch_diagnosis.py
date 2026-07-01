from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path

import torch


DEFAULT_DATASETS = ("Roman-empire", "Amazon-ratings")
DEFAULT_FAMILIES = (
    "iterative_relation_frozen",
    "iterative_relation_finetune",
)
DEFAULT_CONTROLS = ("reliability_only", "combined")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--node-diagnostics-dir",
        type=Path,
        default=Path("outputs/iter_relation_mechanism_v1/_node_diagnostics"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/internal_branch_diagnosis"),
    )
    parser.add_argument("--datasets", nargs="+", default=list(DEFAULT_DATASETS))
    parser.add_argument("--families", nargs="+", default=list(DEFAULT_FAMILIES))
    parser.add_argument("--controls", nargs="+", default=list(DEFAULT_CONTROLS))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    node_dir = resolve(root, args.node_diagnostics_dir)
    out_dir = resolve(root, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    run_rows: list[dict[str, object]] = []
    total = (
        len(args.datasets)
        * len(args.families)
        * len(args.controls)
        * 10
    )
    step = 0
    for dataset in args.datasets:
        for family in args.families:
            fixed_dir = node_dir / dataset / f"{family}_fixed"
            for split in range(10):
                fixed_path = fixed_dir / f"split{split}_seed0.pt"
                if not fixed_path.exists():
                    raise FileNotFoundError(f"Missing fixed payload: {fixed_path}")
                fixed = torch.load(
                    fixed_path,
                    map_location="cpu",
                    weights_only=False,
                )
                fixed_logits = fixed["outputs"]["logits"].float()
                targets = fixed["targets"].long()
                test_mask = fixed["masks"]["test"].bool()
                del fixed

                for control in args.controls:
                    step += 1
                    path = (
                        node_dir
                        / dataset
                        / f"{family}_{control}"
                        / f"split{split}_seed0.pt"
                    )
                    print(f"[{step}/{total}] {path.name}", flush=True)
                    payload = torch.load(
                        path,
                        map_location="cpu",
                        weights_only=False,
                    )
                    run_rows.append(
                        analyze_run(
                            payload,
                            fixed_logits,
                            targets,
                            test_mask,
                            path,
                        )
                    )
                    del payload

    write_csv(out_dir / "internal_branch_run_summary.csv", run_rows)
    group_rows = summarize_groups(run_rows)
    write_csv(out_dir / "internal_branch_group_summary.csv", group_rows)
    write_report(out_dir / "analysis.md", args, group_rows)
    print(f"analysis: {out_dir / 'analysis.md'}")


def analyze_run(
    payload: dict[str, object],
    fixed_logits: torch.Tensor,
    targets: torch.Tensor,
    test_mask: torch.Tensor,
    path: Path,
) -> dict[str, object]:
    meta = payload["meta"]
    layers = payload["model_state"]["layers"]
    alpha = layers["latest_alpha"].float()
    relation = layers["latest_relation"].float()
    base_mixed = layers["latest_base_mixed"].float()
    local_h = layers["latest_local_h"].float()
    global_h = layers["latest_global_h"].float()
    logits = payload["outputs"]["logits"].float()

    base_alpha = float(meta["base_alpha"])
    difference = local_h - global_h
    adjustment = alpha - base_alpha
    relation_norm = torch.linalg.vector_norm(relation, dim=-1)
    base_norm = torch.linalg.vector_norm(base_mixed, dim=-1)
    difference_sq = difference.square()
    weighted_local_shift = (
        (relation * difference).sum(dim=-1)
        / difference_sq.sum(dim=-1).clamp_min(1e-12)
    ).mean(dim=0)

    node_relation_norm = relation_norm.mean(dim=0)
    node_base_norm = base_norm.mean(dim=0)
    node_alpha_abs = adjustment.abs().mean(dim=(0, 2))
    node_alpha_signed = adjustment.mean(dim=(0, 2))
    node_channel_std = alpha.permute(1, 0, 2).reshape(alpha.size(1), -1).std(
        dim=1,
        unbiased=False,
    )
    node_local_channel_fraction = (adjustment > 0).float().mean(dim=(0, 2))

    pred = logits.argmax(dim=-1)
    fixed_pred = fixed_logits.argmax(dim=-1)
    correct = pred.eq(targets)
    fixed_correct = fixed_pred.eq(targets)
    corrected = test_mask & correct & ~fixed_correct
    harmed = test_mask & ~correct & fixed_correct

    margin = classification_margin(logits, targets)
    fixed_margin = classification_margin(fixed_logits, targets)
    margin_delta = margin - fixed_margin

    external = payload.get("external_experts", {})
    local_logits = external.get("local_logits")
    global_logits = external.get("global_logits")
    preference_mask = torch.zeros_like(test_mask)
    local_preference = torch.zeros_like(test_mask)
    if isinstance(local_logits, torch.Tensor) and isinstance(
        global_logits,
        torch.Tensor,
    ):
        local_correct = local_logits.argmax(dim=-1).eq(targets)
        global_correct = global_logits.argmax(dim=-1).eq(targets)
        preference_mask = test_mask & local_correct.ne(global_correct)
        local_preference = preference_mask & local_correct

    row = {
        "dataset": meta["dataset"],
        "family": meta["family"],
        "control_mode": meta["control_mode"],
        "split": int(meta["split"]),
        "seed": int(meta["seed"]),
        "base_alpha": base_alpha,
        "test_accuracy": mean_bool(correct[test_mask]),
        "fixed_test_accuracy": mean_bool(fixed_correct[test_mask]),
        "accuracy_delta_pp": 100.0
        * (
            mean_bool(correct[test_mask])
            - mean_bool(fixed_correct[test_mask])
        ),
        "corrected_rate": mean_bool(corrected[test_mask]),
        "harmed_rate": mean_bool(harmed[test_mask]),
        "net_correction_rate": mean_bool(corrected[test_mask])
        - mean_bool(harmed[test_mask]),
        "margin_delta_mean": finite_mean(margin_delta[test_mask]),
        "alpha_abs_adjustment_mean": finite_mean(node_alpha_abs[test_mask]),
        "alpha_signed_adjustment_mean": finite_mean(
            node_alpha_signed[test_mask]
        ),
        "alpha_channel_std_mean": finite_mean(node_channel_std[test_mask]),
        "local_channel_fraction_mean": finite_mean(
            node_local_channel_fraction[test_mask]
        ),
        "relation_norm_mean": finite_mean(node_relation_norm[test_mask]),
        "base_mixed_norm_mean": finite_mean(node_base_norm[test_mask]),
        "relation_to_base_norm_mean": stable_ratio(
            node_relation_norm,
            node_base_norm,
            test_mask,
        ),
        "weighted_local_shift_mean": finite_mean(
            weighted_local_shift[test_mask]
        ),
        "corr_relation_ratio_margin_delta": safe_corr(
            node_relation_norm[test_mask],
            margin_delta[test_mask],
        ),
        "corr_alpha_abs_margin_delta": safe_corr(
            node_alpha_abs[test_mask],
            margin_delta[test_mask],
        ),
        "corr_weighted_shift_margin_delta": safe_corr(
            weighted_local_shift[test_mask],
            margin_delta[test_mask],
        ),
        "corrected_relation_norm_mean": masked_mean(
            node_relation_norm,
            corrected,
        ),
        "harmed_relation_norm_mean": masked_mean(
            node_relation_norm,
            harmed,
        ),
        "corrected_relation_to_base_norm": stable_ratio(
            node_relation_norm,
            node_base_norm,
            corrected,
        ),
        "harmed_relation_to_base_norm": stable_ratio(
            node_relation_norm,
            node_base_norm,
            harmed,
        ),
        "corrected_alpha_abs_mean": masked_mean(node_alpha_abs, corrected),
        "harmed_alpha_abs_mean": masked_mean(node_alpha_abs, harmed),
        "corrected_weighted_local_shift_mean": masked_mean(
            weighted_local_shift,
            corrected,
        ),
        "harmed_weighted_local_shift_mean": masked_mean(
            weighted_local_shift,
            harmed,
        ),
        "preference_count": int(preference_mask.sum()),
        "weighted_shift_auc_local_preference": binary_auc(
            weighted_local_shift[preference_mask],
            local_preference[preference_mask],
        ),
        "local_channel_fraction_auc_local_preference": binary_auc(
            node_local_channel_fraction[preference_mask],
            local_preference[preference_mask],
        ),
        "alpha_abs_auc_changed_prediction": binary_auc(
            node_alpha_abs[test_mask],
            pred[test_mask].ne(fixed_pred[test_mask]),
        ),
        "payload_path": str(path),
    }
    return row


def classification_margin(
    logits: torch.Tensor,
    targets: torch.Tensor,
) -> torch.Tensor:
    true_logits = logits.gather(1, targets[:, None]).squeeze(1)
    other = logits.clone()
    other.scatter_(1, targets[:, None], float("-inf"))
    return true_logits - other.max(dim=1).values


def summarize_groups(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    metrics = [
        key
        for key in rows[0]
        if key
        not in {
            "dataset",
            "family",
            "control_mode",
            "split",
            "seed",
            "payload_path",
        }
    ]
    groups: dict[tuple[str, str, str], list[dict[str, object]]] = {}
    for row in rows:
        key = (
            str(row["dataset"]),
            str(row["family"]),
            str(row["control_mode"]),
        )
        groups.setdefault(key, []).append(row)

    output = []
    for (dataset, family, control), group in sorted(groups.items()):
        summary: dict[str, object] = {
            "dataset": dataset,
            "family": family,
            "control_mode": control,
            "n": len(group),
        }
        for metric in metrics:
            values = [
                float(row[metric])
                for row in group
                if is_finite_number(row[metric])
            ]
            summary[f"{metric}_mean"] = (
                statistics.mean(values) if values else math.nan
            )
            summary[f"{metric}_ci95_low"] = ci95(values)[0]
            summary[f"{metric}_ci95_high"] = ci95(values)[1]
        output.append(summary)
    return output


def write_report(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, object]],
) -> None:
    lines = [
        "# Internal Branch Diagnosis",
        "",
        f"- Datasets: {', '.join(args.datasets)}",
        f"- Families: {', '.join(args.families)}",
        f"- Controls: {', '.join(args.controls)}",
        "",
        "## Group Summary",
        "",
        (
            "| Dataset | Family | Control | Acc delta (pp) | "
            "Corrected | Harmed | Alpha abs | Channel std | "
            "Relation/base | Weighted shift AUC | Changed-pred AUC |"
        ),
        (
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"
        ),
    ]
    for row in rows:
        lines.append(
            "| {dataset} | {family} | {control_mode} | {acc} | "
            "{corrected} | {harmed} | {alpha_abs} | {channel_std} | "
            "{ratio} | {shift_auc} | {change_auc} |".format(
                **row,
                acc=fmt(row["accuracy_delta_pp_mean"]),
                corrected=fmt(row["corrected_rate_mean"]),
                harmed=fmt(row["harmed_rate_mean"]),
                alpha_abs=fmt(row["alpha_abs_adjustment_mean_mean"]),
                channel_std=fmt(row["alpha_channel_std_mean_mean"]),
                ratio=fmt(row["relation_to_base_norm_mean_mean"]),
                shift_auc=fmt(
                    row["weighted_shift_auc_local_preference_mean"]
                ),
                change_auc=fmt(
                    row["alpha_abs_auc_changed_prediction_mean"]
                ),
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation Notes",
            "",
            "- `Weighted shift AUC` preserves channel importance by weighting the local/global direction with branch disagreement energy.",
            "- `Changed-pred AUC` asks whether large channel-wise adjustment identifies nodes whose final prediction differs from the fixed model.",
            "- Association with corrected nodes is descriptive and does not establish a causal channel attribution.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def binary_auc(scores: torch.Tensor, labels: torch.Tensor) -> float:
    scores = scores.detach().float().flatten()
    labels = labels.detach().bool().flatten()
    finite = torch.isfinite(scores)
    scores = scores[finite]
    labels = labels[finite]
    positives = int(labels.sum())
    negatives = int((~labels).sum())
    if positives == 0 or negatives == 0:
        return math.nan
    order = torch.argsort(scores)
    sorted_scores = scores[order]
    ranks = torch.empty_like(sorted_scores)
    start = 0
    while start < sorted_scores.numel():
        end = start + 1
        while (
            end < sorted_scores.numel()
            and sorted_scores[end] == sorted_scores[start]
        ):
            end += 1
        ranks[start:end] = 0.5 * (start + end - 1) + 1.0
        start = end
    original_ranks = torch.empty_like(ranks)
    original_ranks[order] = ranks
    positive_rank_sum = float(original_ranks[labels].sum())
    return (
        positive_rank_sum - positives * (positives + 1) / 2
    ) / (positives * negatives)


def safe_corr(left: torch.Tensor, right: torch.Tensor) -> float:
    left = left.detach().float().flatten()
    right = right.detach().float().flatten()
    finite = torch.isfinite(left) & torch.isfinite(right)
    left = left[finite]
    right = right[finite]
    if left.numel() < 2 or left.std(unbiased=False) == 0:
        return math.nan
    if right.std(unbiased=False) == 0:
        return math.nan
    return float(torch.corrcoef(torch.stack([left, right]))[0, 1])


def masked_mean(values: torch.Tensor, mask: torch.Tensor) -> float:
    return finite_mean(values[mask]) if bool(mask.any()) else math.nan


def stable_ratio(
    numerator: torch.Tensor,
    denominator: torch.Tensor,
    mask: torch.Tensor,
) -> float:
    if not bool(mask.any()):
        return math.nan
    denominator_mean = finite_mean(denominator[mask])
    if not math.isfinite(denominator_mean) or denominator_mean <= 1e-12:
        return math.nan
    return finite_mean(numerator[mask]) / denominator_mean


def finite_mean(values: torch.Tensor) -> float:
    values = values.detach().float()
    values = values[torch.isfinite(values)]
    return float(values.mean()) if values.numel() else math.nan


def mean_bool(values: torch.Tensor) -> float:
    return float(values.float().mean()) if values.numel() else math.nan


def ci95(values: list[float]) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    mean = statistics.mean(values)
    if len(values) < 2:
        return mean, mean
    critical = 2.262 if len(values) == 10 else 1.96
    half = critical * statistics.stdev(values) / math.sqrt(len(values))
    return mean - half, mean + half


def is_finite_number(value: object) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def fmt(value: object) -> str:
    return f"{float(value):.4f}" if is_finite_number(value) else "n/a"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        if not rows:
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


if __name__ == "__main__":
    main()
