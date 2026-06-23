from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from run_expert_fusion import safe_corr
from src.expert_models import GlobalExpert, LocalExpert
from src.preference_routing import preference_targets
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    prepare_graph_data,
    primary_metric_for_dataset,
    validation_fingerprint,
)


DEFAULT_DATASETS = ("Roman-empire", "Amazon-ratings")
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
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--node-diagnostics-dir",
        type=Path,
        default=Path("outputs/iter_relation_mechanism_v1/_node_diagnostics"),
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("data"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs/node_mechanism_diagnosis"),
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=REAL_DATASETS,
        default=list(DEFAULT_DATASETS),
    )
    parser.add_argument(
        "--families",
        nargs="+",
        default=list(DEFAULT_FAMILIES),
    )
    parser.add_argument(
        "--controls",
        nargs="+",
        default=list(DEFAULT_CONTROLS),
    )
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--alpha-low-quantile", type=float, default=0.25)
    parser.add_argument("--alpha-high-quantile", type=float, default=0.75)
    parser.add_argument(
        "--strict-expert-alignment",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--no-download", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_args(args)
    root = Path(__file__).resolve().parent
    node_dir = resolve(root, args.node_diagnostics_dir)
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    device = torch.device(args.device)

    payload_paths = discover_payloads(
        node_dir,
        set(args.datasets),
        set(args.families),
        set(args.controls),
    )
    if not payload_paths:
        raise SystemExit(f"No payloads found under {node_dir}")

    data_cache = GraphDataCache(data_root, not args.no_download, device)
    expert_cache = ExpertLogitCache(
        device,
        strict_alignment=args.strict_expert_alignment,
    )

    run_rows: list[dict[str, object]] = []
    bucket_rows: list[dict[str, object]] = []
    component_rows: list[dict[str, object]] = []

    total = len(payload_paths)
    for index, path in enumerate(payload_paths, start=1):
        print(f"[{index}/{total}] {path.name}", flush=True)
        payload = torch.load(path, map_location="cpu", weights_only=False)
        run_row, bucket_part, component_part = analyze_payload(
            payload,
            path,
            data_cache,
            expert_cache,
            args,
        )
        run_rows.append(run_row)
        bucket_rows.extend(bucket_part)
        component_rows.extend(component_part)
        del payload

    write_csv(out_dir / "node_mechanism_summary.csv", run_rows)
    write_csv(out_dir / "node_bucket_summary.csv", bucket_rows)
    write_csv(out_dir / "component_correlation.csv", component_rows)
    write_analysis(out_dir / "analysis.md", run_rows, args)
    print(f"saved: {out_dir}", flush=True)


def validate_args(args: argparse.Namespace) -> None:
    if not 0.0 < args.alpha_low_quantile < args.alpha_high_quantile < 1.0:
        raise ValueError("Require 0 < alpha-low-quantile < alpha-high-quantile < 1")


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def discover_payloads(
    node_dir: Path,
    datasets: set[str],
    families: set[str],
    controls: set[str],
) -> list[Path]:
    output = []
    for path in sorted(node_dir.rglob("*.pt")):
        payload = torch.load(path, map_location="cpu", weights_only=False)
        meta = payload.get("meta", {})
        keep = (
            meta.get("dataset") in datasets
            and meta.get("family") in families
            and meta.get("control_mode") in controls
        )
        del payload
        if keep:
            output.append(path)
    return output


class GraphDataCache:
    def __init__(self, data_root: Path, allow_download: bool, device: torch.device):
        self.data_root = data_root
        self.allow_download = allow_download
        self.device = device
        self.dataset_cache: dict[str, tuple[object, dict[str, object]]] = {}
        self.graph_cache: dict[tuple[object, ...], object] = {}

    def get(self, meta: dict[str, object], split: int):
        dataset = str(meta["dataset"])
        if dataset not in self.dataset_cache:
            pyg_data, report = load_and_validate_dataset(
                dataset,
                self.data_root,
                allow_download=self.allow_download,
            )
            self.dataset_cache[dataset] = (pyg_data, report)
        pyg_data, report = self.dataset_cache[dataset]
        key = (
            dataset,
            split,
            str(meta["edge_protocol"]),
            parse_bool_value(meta["normalize_features"]),
            int(meta["rw_steps"]),
            int(meta["rw_samples"]),
            int(meta["rw_seed"]),
        )
        if key not in self.graph_cache:
            cache_key = (
                f"{validation_fingerprint(report)}:"
                f"relcode={meta['preprocess_code_hash']}:"
                f"protocol={meta['edge_protocol']}:"
                f"norm={int(parse_bool_value(meta['normalize_features']))}:"
                f"steps={int(meta['rw_steps'])}:"
                f"samples={int(meta['rw_samples'])}:"
                f"seed={int(meta['rw_seed'])}"
            )
            cache_path = (
                self.data_root
                / "_reliability_cache"
                / (
                    f"{dataset}_{meta['edge_protocol']}_norm"
                    f"{int(parse_bool_value(meta['normalize_features']))}_"
                    f"rw{int(meta['rw_steps'])}_samples{int(meta['rw_samples'])}_"
                    f"seed{int(meta['rw_seed'])}.pt"
                )
            )
            data = prepare_graph_data(
                pyg_data,
                split=split,
                rw_steps=int(meta["rw_steps"]),
                rw_samples=int(meta["rw_samples"]),
                rw_seed=int(meta["rw_seed"]),
                normalize_features=parse_bool_value(meta["normalize_features"]),
                edge_protocol=str(meta["edge_protocol"]),
                cache_path=cache_path,
                cache_key=cache_key,
                primary_metric=primary_metric_for_dataset(dataset),
            )
            data.x = data.x.to(self.device)
            data.y = data.y.to(self.device)
            data.edge_index = data.edge_index.to(self.device)
            self.graph_cache[key] = data
        return self.graph_cache[key]


class ExpertLogitCache:
    def __init__(self, device: torch.device, strict_alignment: bool = False):
        self.device = device
        self.strict_alignment = strict_alignment
        self.cache: dict[tuple[str, str], tuple[torch.Tensor, torch.Tensor]] = {}

    def get_from_payload(
        self,
        payload: dict[str, object],
    ) -> tuple[torch.Tensor | None, torch.Tensor | None]:
        external = payload.get("external_experts", {})
        local_logits = external.get("local_logits")
        global_logits = external.get("global_logits")
        if isinstance(local_logits, torch.Tensor) and isinstance(global_logits, torch.Tensor):
            return local_logits.cpu(), global_logits.cpu()
        return None, None

    def get_from_cache(
        self,
        payload_path: Path,
        meta: dict[str, object],
        data,
        payload: dict[str, object],
    ) -> tuple[torch.Tensor | None, torch.Tensor | None]:
        external = payload.get("external_experts", {})
        local_path = external.get("local_cache_path") or meta.get("local_expert_cache_path")
        global_path = external.get("global_cache_path") or meta.get("global_expert_cache_path")
        if not local_path or not global_path:
            return None, None
        split = int(meta["split"])
        seed = int(meta["seed"])
        local_path = self.resolve_cache_path(local_path, payload_path)
        global_path = self.resolve_cache_path(global_path, payload_path)
        local_path = self.ensure_existing_cache_path(
            local_path,
            prefix=f"local_split{split}_seed{seed}_",
            dataset=str(meta["dataset"]),
        )
        global_path = self.ensure_existing_cache_path(
            global_path,
            prefix=f"global_split{split}_seed{seed}_",
            dataset=str(meta["dataset"]),
        )
        key = (str(local_path), str(global_path))
        if key in self.cache:
            return self.cache[key]
        try:
            local_payload = torch.load(local_path, map_location="cpu", weights_only=False)
            global_payload = torch.load(global_path, map_location="cpu", weights_only=False)
        except FileNotFoundError:
            if self.strict_alignment:
                raise
            return None, None
        out_dim = int(payload["targets"].max().item()) + 1

        local_model = LocalExpert(
            in_dim=int(data.x.size(1)),
            hidden_dim=int(meta["hidden_dim"]),
            out_dim=out_dim,
            dropout=float(meta["dropout"]),
        ).to(self.device)
        local_model.load_state_dict(local_payload["state_dict"])
        local_model.eval()

        global_model = GlobalExpert(
            in_dim=int(data.x.size(1)),
            hidden_dim=int(meta["hidden_dim"]),
            out_dim=out_dim,
            num_layers=int(meta["num_layers"]),
            num_heads=int(meta["num_heads"]),
            dropout=float(meta["dropout"]),
        ).to(self.device)
        global_model.load_state_dict(global_payload["state_dict"])
        global_model.eval()

        with torch.no_grad():
            local_logits = local_model(data.x, data.edge_index).detach().cpu()
            global_logits = global_model(data.x).detach().cpu()
        self.cache[key] = (local_logits, global_logits)
        return local_logits, global_logits

    def resolve_cache_path(self, value: str | Path, payload_path: Path) -> Path:
        path = Path(value)
        if path.is_absolute():
            return path
        return (payload_path.parent / path).resolve()

    def ensure_existing_cache_path(
        self,
        path: Path,
        prefix: str,
        dataset: str,
    ) -> Path:
        if path.exists():
            return path
        parent = path.parent
        matches = sorted(parent.glob(f"{prefix}*.pt")) if parent.exists() else []
        if matches:
            return matches[0]
        dataset_root = parent
        while dataset_root.name != dataset and dataset_root.parent != dataset_root:
            dataset_root = dataset_root.parent
        if dataset_root.name == dataset and dataset_root.exists():
            recursive_matches = sorted(dataset_root.rglob(f"{prefix}*.pt"))
            if recursive_matches:
                return recursive_matches[0]
        if self.strict_alignment:
            raise FileNotFoundError(
                f"Missing cache file {path}; no fallback match for prefix {prefix}"
            )
        return path


def analyze_payload(
    payload: dict[str, object],
    path: Path,
    data_cache: GraphDataCache,
    expert_cache: ExpertLogitCache,
    args: argparse.Namespace,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    meta = payload["meta"]
    split = int(meta["split"])
    seed = int(meta["seed"])
    dataset = str(meta["dataset"])
    family = str(meta["family"])
    control = str(meta["control_mode"])

    alpha = flatten_alpha(payload["outputs"]["node_alpha"])
    logits = payload["outputs"]["logits"].float()
    y = payload["targets"].long()
    train_mask = payload["masks"]["train"].bool()
    val_mask = payload["masks"]["val"].bool()
    test_mask = payload["masks"]["test"].bool()

    raw = payload["inputs"].get("reliability_gate_raw")
    local_similarity = payload["inputs"].get("local_similarity")
    components = component_views(raw, local_similarity)

    local_logits, global_logits = expert_cache.get_from_payload(payload)
    if local_logits is None or global_logits is None:
        data = data_cache.get(meta, split)
        local_logits, global_logits = expert_cache.get_from_cache(
            path,
            meta,
            data,
            payload,
        )
    alignment = compute_alignment_metrics(
        alpha=alpha,
        y=y,
        test_mask=test_mask,
        local_logits=local_logits,
        global_logits=global_logits,
        low_q=args.alpha_low_quantile,
        high_q=args.alpha_high_quantile,
    )

    row = {
        "dataset": dataset,
        "family": family,
        "control_mode": control,
        "split": split,
        "seed": seed,
        "run": meta["run"],
        "payload_path": str(path),
        "best_epoch": meta["best_epoch"],
        "test_primary_at_best_val": meta["test_primary_at_best_val"],
        "test_acc_at_best_val": meta["test_acc_at_best_val"],
        "alpha_mean_test": masked_mean(alpha, test_mask),
        "alpha_std_test": masked_std(alpha, test_mask),
        "alpha_low_quantile": quantile(alpha[test_mask], args.alpha_low_quantile),
        "alpha_high_quantile": quantile(alpha[test_mask], args.alpha_high_quantile),
        "test_correct_rate": masked_rate(
            logits.argmax(dim=-1) == y,
            test_mask,
        ),
        "expert_alignment_available": int(local_logits is not None and global_logits is not None),
        "preference_count": alignment["preference_count"],
        "local_preference_count": alignment["local_preference_count"],
        "global_preference_count": alignment["global_preference_count"],
        "alpha_auc_for_local_preference": alignment["alpha_auc_for_local_preference"],
        "alpha_corr_signed_preference": alignment["alpha_corr_signed_preference"],
        "alpha_corr_local_minus_global_correct": alignment["alpha_corr_local_minus_global_correct"],
        "alpha_corr_local_advantage": alignment["alpha_corr_local_advantage"],
        "mean_alpha_local_win_nodes": alignment["mean_alpha_local_win_nodes"],
        "mean_alpha_global_win_nodes": alignment["mean_alpha_global_win_nodes"],
        "mean_alpha_both_correct": alignment["mean_alpha_both_correct"],
        "mean_alpha_both_wrong": alignment["mean_alpha_both_wrong"],
        "alpha_gap_local_minus_global": alignment["alpha_gap_local_minus_global"],
        "high_alpha_local_preference_rate": alignment["high_alpha_local_preference_rate"],
        "low_alpha_global_preference_rate": alignment["low_alpha_global_preference_rate"],
    }
    for key in (
        "alpha_mean",
        "alpha_std",
        "adjustment_mean",
        "adjustment_max",
        "relation_abs_mean",
        "relation_norm_mean",
        "relation_to_base_norm",
        "relation_state_norm_mean",
        "relation_update_gate_mean",
        "relation_update_gate_std",
        "alpha_corr_raw_degree",
        "alpha_corr_raw_local_similarity",
        "alpha_corr_raw_neighbor_variance",
        "alpha_corr_raw_rwse",
        "alpha_corr_control_input_mean",
    ):
        row[key] = to_float(payload["diagnostics"].get(key))

    component_rows = []
    for component_name, values in components.items():
        component_rows.append(
            component_correlation_row(
                dataset=dataset,
                family=family,
                control=control,
                split=split,
                seed=seed,
                component=component_name,
                alpha=alpha,
                values=values,
                test_mask=test_mask,
                alignment=alignment,
            )
        )
        row[f"alpha_corr_{component_name}_test"] = safe_corr(
            alpha[test_mask].cpu().numpy(),
            values[test_mask].cpu().numpy(),
        )
        row[f"alpha_spearman_{component_name}_test"] = spearman_corr(
            alpha[test_mask],
            values[test_mask],
        )

    bucket_rows = bucket_summary_rows(
        dataset=dataset,
        family=family,
        control=control,
        split=split,
        seed=seed,
        alpha=alpha,
        logits=logits,
        y=y,
        test_mask=test_mask,
        components=components,
        alignment=alignment,
        low_q=args.alpha_low_quantile,
        high_q=args.alpha_high_quantile,
    )
    return row, bucket_rows, component_rows


def flatten_alpha(alpha: torch.Tensor) -> torch.Tensor:
    alpha = alpha.float()
    if alpha.ndim == 2:
        return alpha.mean(dim=1)
    return alpha.view(-1)


def component_views(
    raw: torch.Tensor | None,
    local_similarity: torch.Tensor | None,
) -> dict[str, torch.Tensor]:
    output: dict[str, torch.Tensor] = {}
    if isinstance(raw, torch.Tensor) and raw.size(1) > 0:
        output["degree"] = raw[:, 0].float()
    if isinstance(local_similarity, torch.Tensor):
        output["local_similarity"] = local_similarity.float()
    elif isinstance(raw, torch.Tensor) and raw.size(1) > 1:
        output["local_similarity"] = raw[:, 1].float()
    if isinstance(raw, torch.Tensor) and raw.size(1) > 2:
        output["neighbor_variance"] = raw[:, 2].float()
    if isinstance(raw, torch.Tensor) and raw.size(1) > 3:
        output["rwse"] = raw[:, 3:].float().mean(dim=1)
    return output


def compute_alignment_metrics(
    alpha: torch.Tensor,
    y: torch.Tensor,
    test_mask: torch.Tensor,
    local_logits: torch.Tensor | None,
    global_logits: torch.Tensor | None,
    low_q: float,
    high_q: float,
) -> dict[str, object]:
    empty = {
        "preference_count": 0,
        "local_preference_count": 0,
        "global_preference_count": 0,
        "alpha_auc_for_local_preference": math.nan,
        "alpha_corr_signed_preference": math.nan,
        "alpha_corr_local_minus_global_correct": math.nan,
        "alpha_corr_local_advantage": math.nan,
        "mean_alpha_local_win_nodes": math.nan,
        "mean_alpha_global_win_nodes": math.nan,
        "mean_alpha_both_correct": math.nan,
        "mean_alpha_both_wrong": math.nan,
        "alpha_gap_local_minus_global": math.nan,
        "high_alpha_local_preference_rate": math.nan,
        "low_alpha_global_preference_rate": math.nan,
        "targets": None,
        "local_advantage": None,
        "local_win": None,
        "global_win": None,
    }
    if local_logits is None or global_logits is None:
        return empty

    targets = preference_targets(local_logits, global_logits, y, test_mask).cpu()
    local_correct = (local_logits.argmax(dim=-1) == y).cpu()
    global_correct = (global_logits.argmax(dim=-1) == y).cpu()
    selected = test_mask.cpu() & (targets >= 0)
    correctness_delta = local_correct.float() - global_correct.float()
    local_loss = F.cross_entropy(local_logits, y, reduction="none").cpu()
    global_loss = F.cross_entropy(global_logits, y, reduction="none").cpu()
    local_advantage = global_loss - local_loss
    local_win = selected & (targets == 1)
    global_win = selected & (targets == 0)
    both_correct = test_mask.cpu() & local_correct & global_correct
    both_wrong = test_mask.cpu() & ~local_correct & ~global_correct

    high_threshold = quantile(alpha[test_mask.cpu()], high_q)
    low_threshold = quantile(alpha[test_mask.cpu()], low_q)
    high_alpha = test_mask.cpu() & (alpha >= high_threshold)
    low_alpha = test_mask.cpu() & (alpha <= low_threshold)
    alpha_gap = masked_mean(alpha, local_win) - masked_mean(alpha, global_win)
    return {
        "preference_count": int(selected.sum()),
        "local_preference_count": int((targets[selected] == 1).sum()),
        "global_preference_count": int((targets[selected] == 0).sum()),
        "alpha_auc_for_local_preference": binary_auc(alpha[selected], targets[selected]),
        "alpha_corr_signed_preference": safe_corr(
            alpha[selected].numpy(),
            (targets[selected].float().numpy() * 2.0) - 1.0,
        ),
        "alpha_corr_local_minus_global_correct": safe_corr(
            alpha[test_mask.cpu()].numpy(),
            correctness_delta[test_mask.cpu()].numpy(),
        ),
        "alpha_corr_local_advantage": safe_corr(
            alpha[test_mask.cpu()].numpy(),
            local_advantage[test_mask.cpu()].numpy(),
        ),
        "mean_alpha_local_win_nodes": masked_mean(alpha, local_win),
        "mean_alpha_global_win_nodes": masked_mean(alpha, global_win),
        "mean_alpha_both_correct": masked_mean(alpha, both_correct),
        "mean_alpha_both_wrong": masked_mean(alpha, both_wrong),
        "alpha_gap_local_minus_global": alpha_gap,
        "high_alpha_local_preference_rate": masked_rate(local_win, high_alpha & selected),
        "low_alpha_global_preference_rate": masked_rate(global_win, low_alpha & selected),
        "targets": targets,
        "local_advantage": local_advantage,
        "local_win": local_win,
        "global_win": global_win,
    }


def component_correlation_row(
    dataset: str,
    family: str,
    control: str,
    split: int,
    seed: int,
    component: str,
    alpha: torch.Tensor,
    values: torch.Tensor,
    test_mask: torch.Tensor,
    alignment: dict[str, object],
) -> dict[str, object]:
    selected = (
        test_mask.cpu() & (alignment["targets"] >= 0)
        if alignment["targets"] is not None
        else None
    )
    local_pref_target = alignment["targets"][selected] if selected is not None else None
    local_advantage = alignment["local_advantage"]
    return {
        "dataset": dataset,
        "family": family,
        "control_mode": control,
        "split": split,
        "seed": seed,
        "component": component,
        "test_count": int(test_mask.sum()),
        "alpha_pearson_test": safe_corr(
            alpha[test_mask].cpu().numpy(),
            values[test_mask].cpu().numpy(),
        ),
        "alpha_spearman_test": spearman_corr(
            alpha[test_mask],
            values[test_mask],
        ),
        "component_auc_for_local_preference": (
            binary_auc(values[selected], local_pref_target)
            if selected is not None and int(selected.sum()) > 0
            else math.nan
        ),
        "component_corr_local_advantage": (
            safe_corr(
                values[test_mask].cpu().numpy(),
                local_advantage[test_mask].cpu().numpy(),
            )
            if local_advantage is not None
            else math.nan
        ),
    }


def bucket_summary_rows(
    dataset: str,
    family: str,
    control: str,
    split: int,
    seed: int,
    alpha: torch.Tensor,
    logits: torch.Tensor,
    y: torch.Tensor,
    test_mask: torch.Tensor,
    components: dict[str, torch.Tensor],
    alignment: dict[str, object],
    low_q: float,
    high_q: float,
) -> list[dict[str, object]]:
    low_threshold = quantile(alpha[test_mask], low_q)
    high_threshold = quantile(alpha[test_mask], high_q)
    bucket_masks = {
        "low": test_mask & (alpha <= low_threshold),
        "mid": test_mask & (alpha > low_threshold) & (alpha < high_threshold),
        "high": test_mask & (alpha >= high_threshold),
    }
    prediction = logits.argmax(dim=-1)
    rows = []
    for bucket, mask in bucket_masks.items():
        row = {
            "dataset": dataset,
            "family": family,
            "control_mode": control,
            "split": split,
            "seed": seed,
            "bucket": bucket,
            "count": int(mask.sum()),
            "fraction_of_test": (
                float(mask.sum()) / max(int(test_mask.sum()), 1)
            ),
            "alpha_mean": masked_mean(alpha, mask),
            "test_accuracy": masked_rate(prediction == y, mask),
            "local_preference_rate": (
                masked_rate(alignment["local_win"], mask & (alignment["targets"] >= 0))
                if alignment["local_win"] is not None
                else math.nan
            ),
            "global_preference_rate": (
                masked_rate(alignment["global_win"], mask & (alignment["targets"] >= 0))
                if alignment["global_win"] is not None
                else math.nan
            ),
            "local_advantage_mean": (
                masked_mean(alignment["local_advantage"], mask)
                if alignment["local_advantage"] is not None
                else math.nan
            ),
        }
        for name, values in components.items():
            row[f"{name}_mean"] = masked_mean(values, mask)
        rows.append(row)
    return rows


def spearman_corr(a: torch.Tensor, b: torch.Tensor) -> float:
    a_np = a.detach().cpu().numpy().reshape(-1)
    b_np = b.detach().cpu().numpy().reshape(-1)
    finite = np.isfinite(a_np) & np.isfinite(b_np)
    if finite.sum() < 2:
        return math.nan
    try:
        from scipy.stats import spearmanr
    except ImportError:
        return math.nan
    value = spearmanr(a_np[finite], b_np[finite]).correlation
    return float(value) if value is not None else math.nan


def masked_mean(values: torch.Tensor, mask: torch.Tensor) -> float:
    if int(mask.sum()) == 0:
        return math.nan
    return float(values[mask].float().mean())


def masked_std(values: torch.Tensor, mask: torch.Tensor) -> float:
    if int(mask.sum()) == 0:
        return math.nan
    return float(values[mask].float().std(unbiased=False))


def masked_rate(event_mask: torch.Tensor, subset_mask: torch.Tensor) -> float:
    count = int(subset_mask.sum())
    if count == 0:
        return math.nan
    return float(event_mask[subset_mask].float().mean())


def binary_auc(score: torch.Tensor, target: torch.Tensor) -> float:
    score_np = score.detach().cpu().numpy()
    target_np = target.detach().cpu().numpy()
    if score_np.size == 0 or np.unique(target_np).size < 2:
        return math.nan
    from sklearn.metrics import roc_auc_score

    return float(roc_auc_score(target_np, score_np))


def quantile(values: torch.Tensor, q: float) -> float:
    if values.numel() == 0:
        return math.nan
    return float(torch.quantile(values.float(), q))


def to_float(value) -> float:
    if value in {"", None, "nan", "NaN"}:
        return math.nan
    return float(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        if not rows:
            handle.write("")
            return
        fieldnames = sorted({key for row in rows for key in row.keys()})
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_bool_value(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def write_analysis(path: Path, rows: list[dict[str, object]], args: argparse.Namespace) -> None:
    groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(row["dataset"], row["family"], row["control_mode"])].append(row)

    lines = [
        "# Node Mechanism Diagnosis",
        "",
        f"- Datasets: {', '.join(args.datasets)}",
        f"- Families: {', '.join(args.families)}",
        f"- Controls: {', '.join(args.controls)}",
        f"- Node diagnostics dir: `{args.node_diagnostics_dir}`",
        "",
        "## Group Summary",
        "",
        "| Dataset | Family | Control | n | Align avail | Alpha AUC | Alpha corr(local advantage) | Alpha gap(local-global) | High-alpha local pref rate | Low-alpha global pref rate | Alpha corr degree | Alpha corr variance | Alpha corr rwse |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    ordered = sorted(groups.items())
    for (dataset, family, control), group in ordered:
        lines.append(
            "| "
            + " | ".join(
                [
                    dataset,
                    family,
                    control,
                    str(len(group)),
                    fmt(mean(group, "expert_alignment_available")),
                    fmt(mean(group, "alpha_auc_for_local_preference")),
                    fmt(mean(group, "alpha_corr_local_advantage")),
                    fmt(mean(group, "alpha_gap_local_minus_global")),
                    fmt(mean(group, "high_alpha_local_preference_rate")),
                    fmt(mean(group, "low_alpha_global_preference_rate")),
                    fmt(mean(group, "alpha_corr_degree_test")),
                    fmt(mean(group, "alpha_corr_neighbor_variance_test")),
                    fmt(mean(group, "alpha_corr_rwse_test")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Takeaways",
            "",
            "- Interpret `Roman-empire` and `Amazon-ratings` side by side using the chain `headroom -> separability -> alpha alignment -> accuracy gain`.",
            "- `Align avail` reports whether external local/global expert logits were successfully recovered for the group.",
            "- If `Align avail` is below 1.0000, treat preference-alignment metrics as partially observed for that group.",
            "- `alpha_auc_for_local_preference` and `alpha_corr_local_advantage` are the primary node-level alignment metrics.",
            "- `high_alpha_local_preference_rate` and `low_alpha_global_preference_rate` summarize whether extreme alpha buckets match expert preference.",
            "- `alpha_corr_degree_test`, `alpha_corr_neighbor_variance_test`, and `alpha_corr_rwse_test` summarize structural association on test nodes.",
            "- Treat `fixed` mainly as a sanity baseline: its constant alpha is useful for confirming the absence of node-level routing information, not as mechanism evidence.",
            "- Extremely large `relation_to_base_norm` values should be treated as unstable ratio diagnostics rather than publication-ready evidence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def mean(rows: list[dict[str, object]], key: str) -> float:
    values = [to_float(row.get(key)) for row in rows]
    values = [value for value in values if math.isfinite(value)]
    return float(sum(values) / len(values)) if values else math.nan


def fmt(value: object) -> str:
    if not isinstance(value, (int, float)):
        return str(value)
    if math.isnan(value):
        return "n/a"
    return f"{value:.4f}"


if __name__ == "__main__":
    main()
