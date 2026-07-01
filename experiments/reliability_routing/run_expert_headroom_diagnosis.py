from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

from run_expert_fusion import resolve
from src.data import RELIABILITY_COMPONENTS, select_reliability_components
from src.expert_models import build_expert_model
from src.preference_routing import (
    interpolated_node_accuracy,
    oracle_union_accuracy,
    preference_targets,
    select_fixed_alpha,
)
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    prepare_graph_data,
    primary_metric_for_dataset,
    select_mask,
)


ROUTER_ALIASES = {
    "reliability_only": ("reliability_only",),
    "node_feature_only": ("node_feature_only", "feature_only"),
    "combined": ("combined",),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Diagnose whether each dataset has meaningful local/global expert "
            "headroom and whether reliability separates oracle preference."
        )
    )
    parser.add_argument(
        "--datasets",
        nargs="*",
        choices=REAL_DATASETS,
        help="Defaults to datasets found under the preference-results directory.",
    )
    parser.add_argument(
        "--preference-dir",
        type=Path,
        default=Path("outputs/preference_routing_full_v3"),
    )
    parser.add_argument("--expert-cache-dir", type=Path)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--edge-protocol", choices=EDGE_PROTOCOLS, default="undirected")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/expert_headroom_diagnosis"))
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--no-download", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    preference_dir = resolve(root, args.preference_dir)
    expert_cache_dir = resolve(
        root,
        args.expert_cache_dir or preference_dir / "_expert_cache",
    )
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    device = torch.device(args.device)

    datasets = args.datasets or discover_datasets(preference_dir)
    if not datasets:
        raise SystemExit(
            "No preference-routing result files found. Provide --datasets and "
            "--preference-dir."
        )

    expert_headroom_rows: list[dict[str, object]] = []
    preference_rows: list[dict[str, object]] = []
    dataset_reports: list[dict[str, object]] = []
    skipped_rows: list[dict[str, str]] = []

    for dataset in datasets:
        preference_path = preference_dir / f"{dataset}_preference_routing.csv"
        if not preference_path.exists():
            reason = f"missing preference result {preference_path.name}"
            print(f"skip {dataset}: {reason}")
            skipped_rows.append({"dataset": dataset, "reason": reason})
            continue
        print(f"processing {dataset}", flush=True)
        raw_rows = read_csv(preference_path)
        if not raw_rows:
            reason = f"empty preference result {preference_path.name}"
            print(f"skip {dataset}: {reason}")
            skipped_rows.append({"dataset": dataset, "reason": reason})
            continue

        try:
            pyg_data, validation = load_and_validate_dataset(
                dataset,
                data_root,
                allow_download=not args.no_download,
            )
        except (FileNotFoundError, RuntimeError) as exc:
            reason = str(exc).strip().replace("\n", " | ")
            print(f"skip {dataset}: {reason}")
            skipped_rows.append({"dataset": dataset, "reason": reason})
            continue
        data_by_split = build_data_by_split(
            dataset,
            pyg_data,
            validation,
            raw_rows,
            data_root,
            args.edge_protocol,
        )

        run_groups = group_rows_by_run(raw_rows)
        dataset_headroom: list[dict[str, object]] = []
        dataset_preference: list[dict[str, object]] = []
        for run_key, rows in sorted(run_groups.items()):
            run_row = rows[0]
            split = int(run_row["split"])
            seed = int(run_row["seed"])
            data = data_by_split[split]
            local_logits, global_logits = load_cached_expert_logits(
                dataset=dataset,
                split=split,
                seed=seed,
                run_row=run_row,
                data=data,
                cache_dir=expert_cache_dir,
                edge_protocol=args.edge_protocol,
                device=device,
            )
            router_metrics = collect_router_metrics(rows)
            headroom_row = build_headroom_row(
                dataset,
                split,
                seed,
                data,
                local_logits,
                global_logits,
                run_row,
            )
            preference_row = build_preference_row(
                dataset,
                split,
                seed,
                data,
                local_logits,
                global_logits,
                run_row,
                router_metrics,
            )
            dataset_headroom.append(headroom_row)
            dataset_preference.append(preference_row)

        expert_headroom_rows.extend(dataset_headroom)
        preference_rows.extend(dataset_preference)
        dataset_reports.append(summarize_dataset(dataset, dataset_headroom, dataset_preference))

    write_csv(out_dir / "expert_headroom.csv", expert_headroom_rows)
    write_csv(out_dir / "preference_separability.csv", preference_rows)
    write_csv(out_dir / "dataset_summary.csv", dataset_reports)
    write_csv(out_dir / "skipped_datasets.csv", skipped_rows)
    (out_dir / "analysis.md").write_text(
        render_report(dataset_reports, skipped_rows),
        encoding="utf-8",
    )
    print(f"saved: {out_dir / 'expert_headroom.csv'}")
    print(f"saved: {out_dir / 'preference_separability.csv'}")
    print(f"saved: {out_dir / 'dataset_summary.csv'}")
    print(f"saved: {out_dir / 'skipped_datasets.csv'}")
    print(f"saved: {out_dir / 'analysis.md'}")


def discover_datasets(preference_dir: Path) -> list[str]:
    datasets = []
    for path in sorted(preference_dir.glob("*_preference_routing.csv")):
        name = path.name.removesuffix("_preference_routing.csv")
        if name in REAL_DATASETS:
            datasets.append(name)
    return datasets


def build_data_by_split(
    dataset,
    pyg_data,
    validation,
    raw_rows,
    data_root: Path,
    edge_protocol: str,
):
    template = raw_rows[0]
    normalize_features = parse_bool(template["normalize_features"])
    rw_steps = int(template["rw_steps"])
    rw_samples = int(template["rw_samples"])
    rw_seed = int(template["rw_seed"])
    components = parse_components(template["reliability_components"])
    cache_key = (
        f"{template['data_fingerprint']}:"
        f"relcode={template['preprocess_code_hash']}:"
        f"protocol={edge_protocol}:norm={int(normalize_features)}:"
        f"steps={rw_steps}:samples={rw_samples}:seed={rw_seed}"
    )
    cache_path = (
        data_root
        / "_reliability_cache"
        / (
            f"{dataset}_{edge_protocol}_norm{int(normalize_features)}_"
            f"rw{rw_steps}_samples{rw_samples}_seed{rw_seed}.pt"
        )
    )
    count = int(validation["actual"]["num_splits"])
    output = {}
    for split in range(count):
        data = prepare_graph_data(
            pyg_data,
            split=split,
            rw_steps=rw_steps,
            rw_samples=rw_samples,
            rw_seed=rw_seed,
            normalize_features=normalize_features,
            edge_protocol=edge_protocol,
            cache_path=cache_path,
            cache_key=cache_key,
            primary_metric=primary_metric_for_dataset(dataset),
        )
        output[split] = select_reliability_components(data, components)
    return output


def load_cached_expert_logits(
    dataset: str,
    split: int,
    seed: int,
    run_row: dict[str, str],
    data,
    cache_dir: Path,
    edge_protocol: str,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor]:
    model = build_expert_model(
        name="ordinary_gate",
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        hidden_dim=int(run_row["hidden_dim"]),
        out_dim=int(data.y.max().item()) + 1,
        num_layers=int(run_row["num_layers"]),
        num_heads=int(run_row["num_heads"]),
        dropout=float(run_row["dropout"]),
        fixed_alpha=0.5,
    ).to(device)
    local_path = find_cache_file(
        cache_dir / dataset / edge_protocol,
        f"local_split{split}_seed{seed}_*.pt",
    )
    global_path = find_cache_file(
        cache_dir / dataset / "edge_independent",
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
    if len(matches) > 1:
        return max(matches, key=lambda path: path.stat().st_mtime)
    return matches[0]


def build_headroom_row(
    dataset: str,
    split: int,
    seed: int,
    data,
    local_logits: torch.Tensor,
    global_logits: torch.Tensor,
    run_row: dict[str, str],
) -> dict[str, object]:
    y = data.y.cpu()
    val_mask = data.val_mask.cpu()
    test_mask = data.test_mask.cpu()
    alphas = parse_float_list(run_row.get("fixed_alphas", "0.0,0.25,0.5,0.75,1.0"))
    fixed = select_fixed_alpha(alphas, local_logits, global_logits, y, val_mask)
    local_acc = accuracy(local_logits, y, test_mask)
    global_acc = accuracy(global_logits, y, test_mask)
    fixed_test = interpolated_node_accuracy(
        fixed["alpha"],
        local_logits,
        global_logits,
        y,
        test_mask,
    )
    oracle = oracle_union_accuracy(local_logits, global_logits, y, test_mask)

    local_correct = local_logits[test_mask].argmax(dim=-1) == y[test_mask]
    global_correct = global_logits[test_mask].argmax(dim=-1) == y[test_mask]
    both_correct = float((local_correct & global_correct).float().mean())
    both_wrong = float((~local_correct & ~global_correct).float().mean())
    local_only = float((local_correct & ~global_correct).float().mean())
    global_only = float((~local_correct & global_correct).float().mean())
    disagreement = local_only + global_only

    best_single = max(local_acc, global_acc)
    best_single_name = "local" if local_acc >= global_acc else "global"
    return {
        "dataset": dataset,
        "split": split,
        "seed": seed,
        "primary_metric": getattr(data, "primary_metric", "accuracy"),
        "local_only": local_acc,
        "global_only": global_acc,
        "best_fixed_alpha": fixed["alpha"],
        "best_fixed_alpha_score": fixed_test,
        "oracle_union": oracle,
        "oracle_union_minus_best_fixed": oracle - fixed_test,
        "oracle_union_minus_best_single": oracle - best_single,
        "local_minus_global": local_acc - global_acc,
        "best_single_expert": best_single_name,
        "local_win_rate": local_only,
        "global_win_rate": global_only,
        "both_correct_rate": both_correct,
        "both_wrong_rate": both_wrong,
        "disagreement_rate": disagreement,
    }


def build_preference_row(
    dataset: str,
    split: int,
    seed: int,
    data,
    local_logits: torch.Tensor,
    global_logits: torch.Tensor,
    run_row: dict[str, str],
    router_metrics: dict[str, dict[str, float]],
) -> dict[str, object]:
    y = data.y.cpu()
    test_mask = data.test_mask.cpu()
    targets = preference_targets(local_logits, global_logits, y, test_mask)
    selected = test_mask & (targets >= 0)
    local_pref = int((targets[selected] == 1).sum())
    global_pref = int((targets[selected] == 0).sum())
    total_pref = int(selected.sum())
    balance = (
        min(local_pref, global_pref) / total_pref
        if total_pref > 0
        else math.nan
    )

    reliability = data.reliability_gate_raw.cpu()
    degree = reliability[:, 0]
    local_similarity = data.local_similarity.cpu()
    neighbor_variance = reliability[:, 2]
    rwse = reliability[:, 3:].mean(dim=1)

    local_win = selected & (targets == 1)
    global_win = selected & (targets == 0)

    return {
        "dataset": dataset,
        "split": split,
        "seed": seed,
        "preference_label_balance": balance,
        "preference_count": total_pref,
        "local_preference_count": local_pref,
        "global_preference_count": global_pref,
        "reliability_preference_auc": router_value(router_metrics, "reliability_only", "test_preference_auc"),
        "feature_preference_auc": router_value(router_metrics, "node_feature_only", "test_preference_auc"),
        "combined_preference_auc": router_value(router_metrics, "combined", "test_preference_auc"),
        "degree_auc": binary_auc(degree[selected], targets[selected]),
        "neighbor_variance_auc": binary_auc(neighbor_variance[selected], targets[selected]),
        "local_similarity_auc": binary_auc(local_similarity[selected], targets[selected]),
        "rwse_auc": binary_auc(rwse[selected], targets[selected]),
        "mean_degree_local_win": masked_mean(degree, local_win),
        "mean_degree_global_win": masked_mean(degree, global_win),
        "mean_neighbor_variance_local_win": masked_mean(neighbor_variance, local_win),
        "mean_neighbor_variance_global_win": masked_mean(neighbor_variance, global_win),
        "mean_local_similarity_local_win": masked_mean(local_similarity, local_win),
        "mean_local_similarity_global_win": masked_mean(local_similarity, global_win),
        "mean_rwse_local_win": masked_mean(rwse, local_win),
        "mean_rwse_global_win": masked_mean(rwse, global_win),
    }


def collect_router_metrics(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {}
    for canonical, aliases in ROUTER_ALIASES.items():
        for alias in aliases:
            row = next((item for item in rows if item.get("router") == alias), None)
            if row is not None:
                output[canonical] = {
                    "test_preference_auc": to_float(row.get("test_preference_auc")),
                    "test_balanced_accuracy": to_float(row.get("test_balanced_accuracy")),
                    "test_routing_accuracy": to_float(row.get("test_routing_accuracy")),
                    "test_routed_node_accuracy": to_float(row.get("test_routed_node_accuracy")),
                }
                break
    return output


def router_value(
    router_metrics: dict[str, dict[str, float]],
    router: str,
    field: str,
) -> float:
    return router_metrics.get(router, {}).get(field, math.nan)


def summarize_dataset(dataset, headroom_rows, preference_rows):
    return {
        "dataset": dataset,
        "runs": len(headroom_rows),
        "local_only_mean": mean(headroom_rows, "local_only"),
        "global_only_mean": mean(headroom_rows, "global_only"),
        "best_fixed_alpha_score_mean": mean(headroom_rows, "best_fixed_alpha_score"),
        "oracle_union_mean": mean(headroom_rows, "oracle_union"),
        "oracle_union_minus_best_fixed_mean": mean(headroom_rows, "oracle_union_minus_best_fixed"),
        "oracle_union_minus_best_fixed_std": std(headroom_rows, "oracle_union_minus_best_fixed"),
        "oracle_union_minus_best_single_mean": mean(headroom_rows, "oracle_union_minus_best_single"),
        "oracle_union_minus_best_single_std": std(headroom_rows, "oracle_union_minus_best_single"),
        "disagreement_rate_mean": mean(headroom_rows, "disagreement_rate"),
        "local_win_rate_mean": mean(headroom_rows, "local_win_rate"),
        "global_win_rate_mean": mean(headroom_rows, "global_win_rate"),
        "preference_count_mean": mean(preference_rows, "preference_count"),
        "preference_count_std": std(preference_rows, "preference_count"),
        "local_preference_count_mean": mean(preference_rows, "local_preference_count"),
        "global_preference_count_mean": mean(preference_rows, "global_preference_count"),
        "preference_label_balance_mean": mean(preference_rows, "preference_label_balance"),
        "reliability_preference_auc_mean": mean(preference_rows, "reliability_preference_auc"),
        "reliability_preference_auc_std": std(preference_rows, "reliability_preference_auc"),
        "feature_preference_auc_mean": mean(preference_rows, "feature_preference_auc"),
        "feature_preference_auc_std": std(preference_rows, "feature_preference_auc"),
        "combined_preference_auc_mean": mean(preference_rows, "combined_preference_auc"),
        "combined_preference_auc_std": std(preference_rows, "combined_preference_auc"),
        "degree_auc_mean": mean(preference_rows, "degree_auc"),
        "neighbor_variance_auc_mean": mean(preference_rows, "neighbor_variance_auc"),
        "local_similarity_auc_mean": mean(preference_rows, "local_similarity_auc"),
        "rwse_auc_mean": mean(preference_rows, "rwse_auc"),
    }


def render_report(
    rows: list[dict[str, object]],
    skipped_rows: list[dict[str, str]],
) -> str:
    lines = [
        "# Expert Headroom Diagnosis",
        "",
        "This report checks two preconditions before adding new control modules:",
        "",
        "1. whether each dataset has meaningful local/global expert headroom,",
        "2. whether handcrafted reliability separates oracle preference.",
        "",
    ]
    if skipped_rows:
        lines.extend(
            [
                "## Skipped Datasets",
                "",
                "| Dataset | Reason |",
                "|---|---|",
            ]
        )
        for row in skipped_rows:
            lines.append(f"| {row['dataset']} | {row['reason']} |")
        lines.append("")
    lines.extend(
        [
            "## Dataset Summary",
            "",
            "| Dataset | Runs | Oracle-best fixed | Pref nodes | Disagreement | Pref balance | Rel AUC | Rel std | Feat AUC | Comb AUC | Comb std | Degree AUC | Local-sim AUC | Var AUC | RWSE AUC |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['dataset']} | {row['runs']} | "
            f"{fmt(row['oracle_union_minus_best_fixed_mean'])} | "
            f"{fmt(row['preference_count_mean'])} | "
            f"{fmt(row['disagreement_rate_mean'])} | "
            f"{fmt(row['preference_label_balance_mean'])} | "
            f"{fmt(row['reliability_preference_auc_mean'])} | "
            f"{fmt(row['reliability_preference_auc_std'])} | "
            f"{fmt(row['feature_preference_auc_mean'])} | "
            f"{fmt(row['combined_preference_auc_mean'])} | "
            f"{fmt(row['combined_preference_auc_std'])} | "
            f"{fmt(row['degree_auc_mean'])} | "
            f"{fmt(row['local_similarity_auc_mean'])} | "
            f"{fmt(row['neighbor_variance_auc_mean'])} | "
            f"{fmt(row['rwse_auc_mean'])} |"
        )
    lines.extend(["", "## Notes", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['dataset']}",
                "",
                f"- Oracle headroom over validation-selected fixed alpha: {fmt(row['oracle_union_minus_best_fixed_mean'])}.",
                f"- Oracle headroom over the best single expert: {fmt(row['oracle_union_minus_best_single_mean'])}.",
                f"- Effective preference nodes: {fmt(row['preference_count_mean'])}.",
                f"- Test disagreement rate: {fmt(row['disagreement_rate_mean'])}.",
                f"- Preference balance: {fmt(row['preference_label_balance_mean'])}.",
                f"- Preference AUCs: reliability {fmt(row['reliability_preference_auc_mean'])}, "
                f"feature {fmt(row['feature_preference_auc_mean'])}, combined {fmt(row['combined_preference_auc_mean'])}.",
                f"- Raw component AUCs: degree {fmt(row['degree_auc_mean'])}, "
                f"local similarity {fmt(row['local_similarity_auc_mean'])}, "
                f"neighbor variance {fmt(row['neighbor_variance_auc_mean'])}, "
                f"rwse {fmt(row['rwse_auc_mean'])}.",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def group_rows_by_run(rows: list[dict[str, str]]) -> dict[tuple[int, int], list[dict[str, str]]]:
    grouped: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["split"]), int(row["seed"]))].append(row)
    return grouped


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


def accuracy(logits: torch.Tensor, y: torch.Tensor, mask: torch.Tensor) -> float:
    if int(mask.sum()) == 0:
        return math.nan
    return float((logits[mask].argmax(dim=-1) == y[mask]).float().mean())


def binary_auc(score: torch.Tensor, target: torch.Tensor) -> float:
    score_np = score.detach().cpu().numpy()
    target_np = target.detach().cpu().numpy()
    if score_np.size == 0 or np.unique(target_np).size < 2:
        return math.nan
    from sklearn.metrics import roc_auc_score

    return float(roc_auc_score(target_np, score_np))


def masked_mean(values: torch.Tensor, mask: torch.Tensor) -> float:
    if int(mask.sum()) == 0:
        return math.nan
    return float(values[mask].float().mean())


def mean(rows: list[dict[str, object]], key: str) -> float:
    values = [to_float(row.get(key)) for row in rows]
    values = [value for value in values if math.isfinite(value)]
    return float(sum(values) / len(values)) if values else math.nan


def std(rows: list[dict[str, object]], key: str) -> float:
    values = [to_float(row.get(key)) for row in rows]
    values = [value for value in values if math.isfinite(value)]
    if len(values) < 2:
        return 0.0 if len(values) == 1 else math.nan
    avg = sum(values) / len(values)
    variance = sum((value - avg) ** 2 for value in values) / (len(values) - 1)
    return float(math.sqrt(variance))


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
