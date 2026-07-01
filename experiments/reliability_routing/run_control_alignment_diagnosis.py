from __future__ import annotations

import argparse
import copy
import csv
import math
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch
import torch.nn.functional as F

from run_expert_fusion import move_data, resolve, safe_corr
from run_representation_control import (
    control_reliability,
    node_alpha,
    train_hidden_mixing,
)
from src.data import RELIABILITY_COMPONENTS, select_reliability_components
from src.expert_models import build_expert_model
from src.preference_routing import preference_targets
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    prepare_graph_data,
    primary_metric_for_dataset,
    select_mask,
)


SUPPORTED_FAMILIES = (
    "hidden_mixing_frozen",
    "hidden_mixing_finetune",
    "iterative_relation_frozen",
    "iterative_relation_finetune",
    "gps_like_frozen",
    "gps_like_finetune",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reproduce trained representation-control runs and diagnose whether "
            "node-wise alpha aligns with local/global expert preference."
        )
    )
    parser.add_argument(
        "--representation-dir",
        type=Path,
        default=Path("outputs/iterative_relation_k1_screen"),
    )
    parser.add_argument("--expert-cache-dir", type=Path)
    parser.add_argument("--backbone-cache-dir", type=Path)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/control_alignment_diagnosis"))
    parser.add_argument(
        "--datasets",
        nargs="*",
        choices=REAL_DATASETS,
        help="Defaults to datasets found in representation result CSVs.",
    )
    parser.add_argument(
        "--families",
        nargs="*",
        choices=SUPPORTED_FAMILIES,
        default=["iterative_relation_frozen", "iterative_relation_finetune"],
    )
    parser.add_argument(
        "--controls",
        nargs="*",
        default=[
            "feature_only",
            "reliability_only",
            "combined",
            "shuffled_reliability",
            "constant_reliability",
        ],
    )
    parser.add_argument("--edge-protocol", choices=EDGE_PROTOCOLS, default="undirected")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    parser.add_argument("--no-download", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    representation_dir = resolve(root, args.representation_dir)
    expert_cache_dir = resolve(
        root,
        args.expert_cache_dir
        or Path("outputs/preference_routing_full_v3/_expert_cache"),
    )
    backbone_cache_dir = resolve(
        root,
        args.backbone_cache_dir or representation_dir / "_backbone_cache",
    )
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    device = torch.device(args.device)

    grouped_rows = discover_representation_rows(
        representation_dir,
        args.datasets,
        set(args.families or []),
        set(args.controls or []),
        args.edge_protocol,
    )
    if not grouped_rows:
        raise SystemExit("No matching representation-control CSV rows found.")

    data_cache: dict[tuple, tuple[object, dict[str, object], dict[int, object]]] = {}
    run_rows: list[dict[str, object]] = []
    skipped_rows: list[dict[str, str]] = []

    for key, rows in sorted(grouped_rows.items()):
        dataset, family, control = key
        template = rows[0]
        print(f"processing {dataset} / {family} / {control}", flush=True)
        try:
            pyg_data, validation, data_by_split = load_dataset_bundle(
                dataset,
                template,
                data_root,
                args.edge_protocol,
                args.no_download,
                data_cache,
            )
        except (FileNotFoundError, RuntimeError, ValueError) as exc:
            reason = str(exc).strip().replace("\n", " | ")
            print(f"skip {dataset}/{family}/{control}: {reason}")
            skipped_rows.append(
                {
                    "dataset": dataset,
                    "family": family,
                    "control_mode": control,
                    "reason": reason,
                }
            )
            continue

        for row in rows:
            split = int(row["split"])
            seed = int(row["seed"])
            try:
                record = reproduce_alignment_run(
                    template=row,
                    dataset=dataset,
                    family=family,
                    control=control,
                    split=split,
                    seed=seed,
                    data_template=data_by_split[split],
                    device=device,
                    expert_cache_dir=expert_cache_dir,
                    backbone_cache_dir=backbone_cache_dir,
                    edge_protocol=args.edge_protocol,
                )
            except (FileNotFoundError, RuntimeError, ValueError) as exc:
                reason = str(exc).strip().replace("\n", " | ")
                print(
                    f"skip run {dataset}/{family}/{control} split={split} seed={seed}: {reason}"
                )
                skipped_rows.append(
                    {
                        "dataset": dataset,
                        "family": family,
                        "control_mode": control,
                        "reason": f"split={split} seed={seed}: {reason}",
                    }
                )
                continue
            run_rows.append(record)

    summary_rows = summarize_runs(run_rows)
    write_csv(out_dir / "control_alignment.csv", run_rows)
    write_csv(out_dir / "control_alignment_summary.csv", summary_rows)
    write_csv(out_dir / "skipped_runs.csv", skipped_rows)
    (out_dir / "analysis.md").write_text(
        render_report(summary_rows, skipped_rows),
        encoding="utf-8",
    )
    print(f"saved: {out_dir / 'control_alignment.csv'}")
    print(f"saved: {out_dir / 'control_alignment_summary.csv'}")
    print(f"saved: {out_dir / 'skipped_runs.csv'}")
    print(f"saved: {out_dir / 'analysis.md'}")


def discover_representation_rows(
    representation_dir: Path,
    datasets: list[str] | None,
    families: set[str],
    controls: set[str],
    edge_protocol: str,
) -> dict[tuple[str, str, str], list[dict[str, str]]]:
    skip_names = {
        "summary.csv",
        "paired_comparisons.csv",
        "analysis.md",
        "suite_config.json",
    }
    selected_datasets = set(datasets or [])
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for path in sorted(representation_dir.glob("*.csv")):
        if path.name in skip_names or path.name.endswith("_validation.json"):
            continue
        rows = read_csv(path)
        if not rows:
            continue
        sample = rows[0]
        if not {"dataset", "family", "control_mode", "split", "seed"}.issubset(sample):
            continue
        dataset = sample["dataset"]
        family = sample["family"]
        control = sample["control_mode"]
        if selected_datasets and dataset not in selected_datasets:
            continue
        if families and family not in families:
            continue
        if controls and control not in controls:
            continue
        filtered = [row for row in rows if row.get("edge_protocol") == edge_protocol]
        if filtered:
            grouped[(dataset, family, control)].extend(filtered)
    return grouped


def load_dataset_bundle(
    dataset: str,
    template: dict[str, str],
    data_root: Path,
    edge_protocol: str,
    no_download: bool,
    cache: dict[tuple, tuple[object, dict[str, object], dict[int, object]]],
):
    cache_key = (
        dataset,
        edge_protocol,
        template["normalize_features"],
        template["rw_steps"],
        template["rw_samples"],
        template["rw_seed"],
        template["reliability_components"],
    )
    if cache_key in cache:
        return cache[cache_key]

    pyg_data, validation = load_and_validate_dataset(
        dataset,
        data_root,
        allow_download=not no_download,
    )
    num_splits = int(validation["actual"]["num_splits"])
    normalize_features = parse_bool(template["normalize_features"])
    rw_steps = int(template["rw_steps"])
    rw_samples = int(template["rw_samples"])
    rw_seed = int(template["rw_seed"])
    components = parse_components(template["reliability_components"])
    data_fingerprint = template["data_fingerprint"]
    preprocess_code_hash = template["preprocess_code_hash"]
    reliability_cache_key = (
        f"{data_fingerprint}:relcode={preprocess_code_hash}:"
        f"protocol={edge_protocol}:norm={int(normalize_features)}:"
        f"steps={rw_steps}:samples={rw_samples}:seed={rw_seed}"
    )
    reliability_cache_path = (
        data_root
        / "_reliability_cache"
        / (
            f"{dataset}_{edge_protocol}_norm{int(normalize_features)}_"
            f"rw{rw_steps}_samples{rw_samples}_seed{rw_seed}.pt"
        )
    )
    data_by_split = {}
    for split in range(num_splits):
        data = prepare_graph_data(
            pyg_data,
            split=split,
            rw_steps=rw_steps,
            rw_samples=rw_samples,
            rw_seed=rw_seed,
            normalize_features=normalize_features,
            edge_protocol=edge_protocol,
            cache_path=reliability_cache_path,
            cache_key=reliability_cache_key,
            primary_metric=primary_metric_for_dataset(dataset),
        )
        data_by_split[split] = select_reliability_components(data, components)
    cache[cache_key] = (pyg_data, validation, data_by_split)
    return cache[cache_key]


def reproduce_alignment_run(
    template: dict[str, str],
    dataset: str,
    family: str,
    control: str,
    split: int,
    seed: int,
    data_template,
    device: torch.device,
    expert_cache_dir: Path,
    backbone_cache_dir: Path,
    edge_protocol: str,
) -> dict[str, object]:
    args = args_from_row(
        template,
        dataset,
        family,
        control,
        expert_cache_dir,
        backbone_cache_dir,
        edge_protocol,
    )
    data = move_data(copy.copy(data_template), device)
    reliability_input = control_reliability(
        data.reliability_gate,
        data.train_mask,
        control,
        seed,
    )
    result, baseline, model = train_hidden_mixing(
        args,
        data,
        reliability_input,
        split,
        seed,
    )
    model.eval()
    with torch.no_grad():
        model(data.x, data.edge_index, reliability_input)
    alpha = node_alpha(model)
    if alpha is None:
        raise RuntimeError("Model did not expose node alpha diagnostics")
    alpha = alpha.view(-1).detach().cpu()

    local_logits, global_logits = load_cached_expert_logits(
        dataset=dataset,
        split=split,
        seed=seed,
        template=template,
        data=data_template,
        cache_dir=expert_cache_dir,
        edge_protocol=edge_protocol,
        device=device,
    )
    y = data_template.y.cpu()
    test_mask = data_template.test_mask.cpu()
    targets = preference_targets(local_logits, global_logits, y, test_mask)
    selected = test_mask & (targets >= 0)
    local_correct = local_logits.argmax(dim=-1) == y
    global_correct = global_logits.argmax(dim=-1) == y
    correctness_delta = (
        local_correct.float() - global_correct.float()
    ).cpu()
    local_loss = F.cross_entropy(local_logits, y, reduction="none")
    global_loss = F.cross_entropy(global_logits, y, reduction="none")
    local_advantage = (global_loss - local_loss).cpu()

    local_win = selected & (targets == 1)
    global_win = selected & (targets == 0)
    both_correct = test_mask & local_correct & global_correct
    both_wrong = test_mask & ~local_correct & ~global_correct

    high_threshold = quantile(alpha[test_mask], 0.75)
    low_threshold = quantile(alpha[test_mask], 0.25)
    high_alpha = test_mask & (alpha >= high_threshold)
    low_alpha = test_mask & (alpha <= low_threshold)

    diagnostics = model.diagnostic_stats()
    reported_primary = reported_test_primary(template, dataset)
    reproduction_delta = float(result["test_score"]) - reported_primary
    reproduction_status = (
        "suspect" if math.isfinite(reproduction_delta) and abs(reproduction_delta) > 1e-3 else "ok"
    )
    return {
        "dataset": dataset,
        "family": family,
        "control_mode": control,
        "split": split,
        "seed": seed,
        "reported_test_primary_at_best_val": reported_primary,
        "recomputed_test_primary_at_best_val": float(result["test_score"]),
        "reproduction_delta": reproduction_delta,
        "reproduction_status": reproduction_status,
        "base_alpha": float(baseline["alpha"]),
        "alpha_mean": float(alpha.mean()),
        "alpha_std": float(alpha.std(unbiased=False)),
        "adjustment_mean": to_float(diagnostics.get("adjustment_mean")),
        "relation_to_base_norm": to_float(diagnostics.get("relation_to_base_norm")),
        "relation_update_gate_mean": to_float(diagnostics.get("relation_update_gate_mean")),
        "preference_count": int(selected.sum()),
        "local_preference_count": int((targets[selected] == 1).sum()),
        "global_preference_count": int((targets[selected] == 0).sum()),
        "alpha_auc_for_local_preference": binary_auc(alpha[selected], targets[selected]),
        "alpha_corr_signed_preference": safe_corr(
            alpha[selected].numpy(),
            (targets[selected].float().numpy() * 2.0) - 1.0,
        ),
        "alpha_corr_local_minus_global_correct": safe_corr(
            alpha[test_mask].numpy(),
            correctness_delta[test_mask].numpy(),
        ),
        "alpha_corr_local_advantage": safe_corr(
            alpha[test_mask].numpy(),
            local_advantage[test_mask].numpy(),
        ),
        "mean_alpha_local_win_nodes": masked_mean(alpha, local_win),
        "mean_alpha_global_win_nodes": masked_mean(alpha, global_win),
        "mean_alpha_both_correct": masked_mean(alpha, both_correct),
        "mean_alpha_both_wrong": masked_mean(alpha, both_wrong),
        "alpha_gap_local_minus_global": masked_mean(alpha, local_win) - masked_mean(alpha, global_win),
        "high_alpha_local_preference_rate": masked_rate(local_win, high_alpha & selected),
        "low_alpha_global_preference_rate": masked_rate(global_win, low_alpha & selected),
    }


def args_from_row(
    row: dict[str, str],
    dataset: str,
    family: str,
    control: str,
    expert_cache_dir: Path,
    backbone_cache_dir: Path,
    edge_protocol: str,
):
    return SimpleNamespace(
        dataset=dataset,
        family=family,
        control_mode=control,
        edge_protocol=edge_protocol,
        expert_cache_dir=expert_cache_dir,
        backbone_cache_dir=backbone_cache_dir,
        hidden_dim=int(row["hidden_dim"]),
        num_layers=int(row["num_layers"]),
        num_heads=int(row["num_heads"]),
        dropout=float(row["dropout"]),
        lr=float(row["lr"]),
        weight_decay=float(row["weight_decay"]),
        expert_epochs=int(row["expert_epochs"]),
        control_epochs=int(row["control_epochs"]),
        patience=int(row["patience"]),
        fixed_alphas=parse_float_list(row["fixed_alphas"]),
        max_adjustment=float(row["max_adjustment"]),
        lambda_init=float(row["lambda_init"]),
        relation_steps=int(row.get("relation_steps") or 0),
        data_fingerprint=row["data_fingerprint"],
        preprocess_code_hash=row["preprocess_code_hash"],
        normalize_features=parse_bool(row["normalize_features"]),
        rw_steps=int(row["rw_steps"]),
        rw_samples=int(row["rw_samples"]),
        rw_seed=int(row["rw_seed"]),
        reliability_components=parse_components(row["reliability_components"]),
    )


def load_cached_expert_logits(
    dataset: str,
    split: int,
    seed: int,
    template: dict[str, str],
    data,
    cache_dir: Path,
    edge_protocol: str,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    model = build_expert_model(
        name="ordinary_gate",
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        hidden_dim=int(template["hidden_dim"]),
        out_dim=int(data.y.max().item()) + 1,
        num_layers=int(template["num_layers"]),
        num_heads=int(template["num_heads"]),
        dropout=float(template["dropout"]),
        fixed_alpha=0.5,
    ).to(device)
    local_path = find_cache_file_with_fallbacks(
        cache_dir,
        dataset,
        edge_protocol,
        f"local_split{split}_seed{seed}_*.pt",
    )
    global_path = find_cache_file_with_fallbacks(
        cache_dir,
        dataset,
        "edge_independent",
        f"global_split{split}_seed{seed}_*.pt",
    )
    local_payload = torch.load(local_path, map_location=device, weights_only=False)
    global_payload = torch.load(global_path, map_location=device, weights_only=False)
    model.local_expert.load_state_dict(local_payload["state_dict"])
    model.global_expert.load_state_dict(global_payload["state_dict"])
    model.eval()
    with torch.no_grad():
        x = data.x.to(device)
        edge_index = data.edge_index.to(device)
        local_logits = model.local_expert(x, edge_index).detach().cpu()
        global_logits = model.global_expert(x).detach().cpu()
    return local_logits, global_logits


def find_cache_file(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"Missing cache file under {directory} matching {pattern}")
    if len(matches) == 1:
        return matches[0]
    return max(matches, key=lambda path: path.stat().st_mtime)


def find_cache_file_with_fallbacks(
    primary_cache_dir: Path,
    dataset: str,
    subdir: str,
    pattern: str,
) -> Path:
    errors: list[str] = []
    for cache_root in candidate_expert_cache_dirs(primary_cache_dir):
        directory = cache_root / dataset / subdir
        try:
            return find_cache_file(directory, pattern)
        except FileNotFoundError as exc:
            errors.append(str(exc))
            continue
    raise FileNotFoundError(" | ".join(errors))


def candidate_expert_cache_dirs(primary_cache_dir: Path) -> list[Path]:
    candidates: list[Path] = []

    def add(path: Path) -> None:
        if path not in candidates:
            candidates.append(path)

    add(primary_cache_dir)
    outputs_root = primary_cache_dir.parent.parent
    add(outputs_root / "preference_routing_full_v3" / "_expert_cache")
    add(outputs_root / "utility_routing_full_v3" / "_expert_cache")
    add(outputs_root / "representation_control_screen_v3" / "_expert_cache")
    add(outputs_root / "expert_validation_full" / "_shared_expert_cache")
    add(outputs_root / "expert_validation_sanity" / "_shared_expert_cache")
    return candidates


def summarize_runs(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(row["dataset"], row["family"], row["control_mode"])].append(row)
    output = []
    for (dataset, family, control), group in sorted(groups.items()):
        output.append(
            {
                "dataset": dataset,
                "family": family,
                "control_mode": control,
                "runs": len(group),
                "suspect_runs": sum(
                    1 for row in group if row.get("reproduction_status") == "suspect"
                ),
                "preference_count_mean": mean(group, "preference_count"),
                "local_preference_frac_mean": ratio_mean(
                    group,
                    "local_preference_count",
                    "preference_count",
                ),
                "global_preference_frac_mean": ratio_mean(
                    group,
                    "global_preference_count",
                    "preference_count",
                ),
                "recomputed_test_primary_mean": mean(group, "recomputed_test_primary_at_best_val"),
                "reported_test_primary_mean": mean(group, "reported_test_primary_at_best_val"),
                "reproduction_delta_mean": mean(group, "reproduction_delta"),
                "reproduction_delta_abs_max": abs_max(group, "reproduction_delta"),
                "alpha_mean": mean(group, "alpha_mean"),
                "alpha_std": mean(group, "alpha_std"),
                "alpha_auc_for_local_preference_mean": mean(group, "alpha_auc_for_local_preference"),
                "alpha_corr_signed_preference_mean": mean(group, "alpha_corr_signed_preference"),
                "alpha_corr_local_minus_global_correct_mean": mean(group, "alpha_corr_local_minus_global_correct"),
                "alpha_corr_local_advantage_mean": mean(group, "alpha_corr_local_advantage"),
                "alpha_gap_local_minus_global_mean": mean(group, "alpha_gap_local_minus_global"),
                "high_alpha_local_preference_rate_mean": mean(group, "high_alpha_local_preference_rate"),
                "low_alpha_global_preference_rate_mean": mean(group, "low_alpha_global_preference_rate"),
                "relation_to_base_norm_mean": mean(group, "relation_to_base_norm"),
                "relation_update_gate_mean": mean(group, "relation_update_gate_mean"),
            }
        )
    return output


def render_report(
    rows: list[dict[str, object]],
    skipped_rows: list[dict[str, str]],
) -> str:
    lines = [
        "# Control Alignment Diagnosis",
        "",
        "This report replays trained representation-control runs and checks whether",
        "node-wise alpha aligns with frozen external local/global expert preference.",
        "",
        "Important scope note: these alignment targets come from cached external",
        "local/global experts, not from the representation model's internal",
        "branch-level counterfactual utility.",
        "",
    ]
    if skipped_rows:
        lines.extend(
            [
                "## Skipped",
                "",
                "| Dataset | Family | Control | Reason |",
                "|---|---|---|---|",
            ]
        )
        for row in skipped_rows:
            lines.append(
                f"| {row.get('dataset','')} | {row.get('family','')} | "
                f"{row.get('control_mode','')} | {row.get('reason','')} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Summary",
            "",
            "| Dataset | Family | Control | Runs | Suspect | Pref count | Local frac | Reprod delta | Max | Alpha std | Alpha AUC(local pref) | Alpha corr(pref) | Alpha corr(correct) | Alpha corr(local advantage) | Alpha gap(local-global) | Rel/Base | Update gate |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['family']} | {row['control_mode']} | "
            f"{row['runs']} | {row['suspect_runs']} | "
            f"{fmt(row['preference_count_mean'])} | "
            f"{fmt(row['local_preference_frac_mean'])} | "
            f"{fmt(row['reproduction_delta_mean'])} | "
            f"{fmt(row['reproduction_delta_abs_max'])} | "
            f"{fmt(row['alpha_std'])} | {fmt(row['alpha_auc_for_local_preference_mean'])} | "
            f"{fmt(row['alpha_corr_signed_preference_mean'])} | "
            f"{fmt(row['alpha_corr_local_minus_global_correct_mean'])} | "
            f"{fmt(row['alpha_corr_local_advantage_mean'])} | "
            f"{fmt(row['alpha_gap_local_minus_global_mean'])} | "
            f"{fmt(row['relation_to_base_norm_mean'])} | "
            f"{fmt(row['relation_update_gate_mean'])} |"
        )
    return "\n".join(lines) + "\n"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        if not rows:
            handle.write("")
            return
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_bool(value: str) -> bool:
    return str(value).lower() == "true"


def parse_components(value: str) -> list[str]:
    components = [item.strip() for item in value.split(",") if item.strip()]
    unknown = set(components).difference(RELIABILITY_COMPONENTS)
    if unknown:
        raise ValueError(f"Unknown reliability components: {sorted(unknown)}")
    return components


def parse_float_list(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def reported_test_primary(row: dict[str, str], dataset: str) -> float:
    direct = to_float(row.get("test_primary_at_best_val"))
    if math.isfinite(direct):
        return direct
    metric = row.get("primary_metric") or primary_metric_for_dataset(dataset)
    if metric == "roc_auc":
        return to_float(row.get("test_roc_auc_at_best_val"))
    return to_float(row.get("test_acc_at_best_val"))


def masked_mean(values: torch.Tensor, mask: torch.Tensor) -> float:
    if int(mask.sum()) == 0:
        return math.nan
    return float(values[mask].float().mean())


def masked_rate(event_mask: torch.Tensor, subset_mask: torch.Tensor) -> float:
    count = int(subset_mask.sum())
    if count == 0:
        return math.nan
    return float((event_mask[subset_mask]).float().mean())


def binary_auc(score: torch.Tensor, target: torch.Tensor) -> float:
    score_np = score.detach().cpu().numpy()
    target_np = target.detach().cpu().numpy()
    if score_np.size == 0 or np.unique(target_np).size < 2:
        return math.nan
    from sklearn.metrics import roc_auc_score

    return float(roc_auc_score(target_np, score_np))


def mean(rows: list[dict[str, object]], key: str) -> float:
    values = [to_float(row.get(key)) for row in rows]
    values = [value for value in values if math.isfinite(value)]
    return float(sum(values) / len(values)) if values else math.nan


def ratio_mean(
    rows: list[dict[str, object]],
    numerator_key: str,
    denominator_key: str,
) -> float:
    values = []
    for row in rows:
        numerator = to_float(row.get(numerator_key))
        denominator = to_float(row.get(denominator_key))
        if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator <= 0:
            continue
        values.append(numerator / denominator)
    return float(sum(values) / len(values)) if values else math.nan


def abs_max(rows: list[dict[str, object]], key: str) -> float:
    values = [abs(to_float(row.get(key))) for row in rows]
    values = [value for value in values if math.isfinite(value)]
    return max(values) if values else math.nan


def quantile(values: torch.Tensor, q: float) -> float:
    if values.numel() == 0:
        return math.nan
    return float(torch.quantile(values.float(), q))


def to_float(value) -> float:
    if value in {"", None, "nan", "NaN"}:
        return math.nan
    return float(value)


def fmt(value: object) -> str:
    if not isinstance(value, (int, float)):
        return str(value)
    if math.isnan(value):
        return "n/a"
    return f"{value:.4f}"


if __name__ == "__main__":
    main()
