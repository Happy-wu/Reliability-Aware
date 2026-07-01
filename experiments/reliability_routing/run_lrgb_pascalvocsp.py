from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import time
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F

from src.data import RELIABILITY_COMPONENTS, set_seed
from src.real_data import apply_edge_protocol, compute_real_reliability, row_normalize_features
from src.representation_control import (
    ALPHA_TYPES,
    COMPONENT_MISSING_MODES,
    CONTROL_MODES,
    IterativeRelationNetwork,
    RELIABILITY_ENCODER_MODES,
)


PASCAL_CONTROLS = (
    "fixed",
    "feature_only",
    "reliability_only",
    "combined",
    "shuffled_reliability",
    "constant_reliability",
    "combined_shuffled",
    "combined_constant",
)
MODEL_MODE_MAP = {
    "shuffled_reliability": "reliability_only",
    "constant_reliability": "reliability_only",
    "combined_shuffled": "combined",
    "combined_constant": "combined",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "PascalVOC-SP sanity/screening runner for the existing iterative "
            "relation controller. Uses batch_size=1 so global attention remains "
            "inside each superpixel graph."
        )
    )
    parser.add_argument("--lrgb-root", type=Path, default=Path("data/lrgb_pyg"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/lrgb_pascalvocsp"))
    parser.add_argument(
        "--controls",
        nargs="+",
        choices=PASCAL_CONTROLS,
        default=[
            "fixed",
            "feature_only",
            "reliability_only",
            "combined",
            "shuffled_reliability",
            "constant_reliability",
            "combined_shuffled",
            "combined_constant",
        ],
    )
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--edge-protocol",
        choices=("undirected", "source_to_target", "target_to_source"),
        default="undirected",
    )
    parser.add_argument(
        "--feature-norm",
        choices=("none", "row", "channel_zscore"),
        default="none",
    )
    parser.add_argument(
        "--normalize-features",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Deprecated compatibility flag; maps True to --feature-norm row and False to none.",
    )
    parser.add_argument("--rw-steps", type=int, default=8)
    parser.add_argument("--rw-samples", type=int, default=64)
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
        default="component_concat",
    )
    parser.add_argument("--reliability-component-dim", type=int, default=32)
    parser.add_argument(
        "--component-missing-mode",
        choices=COMPONENT_MISSING_MODES,
        default="zero_slot",
    )
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--base-alpha", type=float, default=0.5)
    parser.add_argument("--max-adjustment", type=float, default=0.1)
    parser.add_argument("--relation-steps", type=int, default=1)
    parser.add_argument("--alpha-type", choices=ALPHA_TYPES, default="channel")
    parser.add_argument("--alpha-groups", type=int, default=4)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--patience", type=int, default=10)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--max-train-graphs", type=int)
    parser.add_argument("--max-val-graphs", type=int)
    parser.add_argument("--max-test-graphs", type=int)
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_args(args)
    if args.normalize_features is not None:
        args.feature_norm = "row" if args.normalize_features else "none"
    root = Path(__file__).resolve().parent
    args.lrgb_root = resolve(root, args.lrgb_root)
    args.out_dir = resolve(root, args.out_dir)
    args.cache_dir = (
        resolve(root, args.cache_dir)
        if args.cache_dir is not None
        else args.out_dir / "_reliability_cache"
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    device = torch.device(args.device)

    datasets = load_pascal_splits(args.lrgb_root)
    metadata = dataset_metadata(datasets)
    args.feature_mean = None
    args.feature_std = None
    if args.feature_norm == "channel_zscore":
        args.feature_mean, args.feature_std = compute_channel_stats(
            datasets["train"],
            max_graphs=args.max_train_graphs,
        )
        metadata["feature_norm_stats"] = {
            "mean_shape": list(args.feature_mean.size()),
            "std_shape": list(args.feature_std.size()),
            "computed_from_train_graphs": (
                len(datasets["train"])
                if args.max_train_graphs is None
                else min(args.max_train_graphs, len(datasets["train"]))
            ),
        }
    metadata["feature_norm"] = args.feature_norm
    metadata["primary_metric"] = "f1_weighted"
    metadata["secondary_metrics"] = ["f1_macro", "accuracy"]
    write_json(args.out_dir / "pascalvocsp_validation.json", metadata)
    print(
        "PascalVOC-SP: "
        f"train={metadata['splits']['train']['num_graphs']} "
        f"val={metadata['splits']['val']['num_graphs']} "
        f"test={metadata['splits']['test']['num_graphs']} "
        f"in_dim={metadata['in_dim']} classes={metadata['num_classes']}",
        flush=True,
    )

    rows = []
    for run in range(args.runs):
        seed = args.seed + run
        for control in args.controls:
            print(
                f"[run {run + 1}/{args.runs}] control={control} seed={seed}",
                flush=True,
            )
            rows.append(train_one(args, datasets, metadata, control, seed, device))
            write_csv(args.out_dir / "pascalvocsp_results.csv", rows)
    write_analysis(args.out_dir / "analysis.md", args, rows)
    print(f"saved: {(args.out_dir / 'pascalvocsp_results.csv').resolve()}", flush=True)
    print(f"analysis: {(args.out_dir / 'analysis.md').resolve()}", flush=True)


def validate_args(args: argparse.Namespace) -> None:
    if args.runs < 1:
        raise ValueError("--runs must be positive")
    if args.epochs < 1:
        raise ValueError("--epochs must be positive")
    if args.patience < 1:
        raise ValueError("--patience must be positive")
    if args.rw_samples < 1:
        raise ValueError("--rw-samples must be positive")
    if args.alpha_type == "group" and args.hidden_dim % args.alpha_groups != 0:
        raise ValueError("--hidden-dim must be divisible by --alpha-groups")
    unsupported_model_modes = sorted(
        {
            MODEL_MODE_MAP.get(control, control)
            for control in args.controls
        }.difference(CONTROL_MODES)
    )
    if unsupported_model_modes:
        raise ValueError(
            "Controls map to modes not supported by IterativeRelationNetwork: "
            f"{unsupported_model_modes}. Available CONTROL_MODES={CONTROL_MODES}"
        )


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def load_pascal_splits(root: Path) -> dict[str, object]:
    try:
        from torch_geometric.datasets import LRGBDataset
    except ImportError as exc:
        raise RuntimeError(
            "PascalVOC-SP requires torch-geometric with LRGBDataset. "
            "Run prepare_lrgb_manual.py first in the server environment."
        ) from exc
    return {
        split: LRGBDataset(root=str(root), name="PascalVOC-SP", split=split)
        for split in ("train", "val", "test")
    }


def dataset_metadata(datasets: dict[str, object]) -> dict[str, object]:
    train0 = datasets["train"][0]
    in_dim = int(train0.x.size(-1))
    reported_num_classes = getattr(datasets["train"], "num_classes", None)
    max_label = -1
    min_label = math.inf
    unique_labels = set()
    split_info = {}
    for split, dataset in datasets.items():
        graphs = len(dataset)
        sample_nodes = []
        sample_edges = []
        for index in range(min(5, graphs)):
            data = dataset[index]
            sample_nodes.append(int(data.num_nodes))
            sample_edges.append(int(data.edge_index.size(1)))
        for index in range(graphs):
            y = normalize_labels(dataset[index].y)
            valid = y >= 0
            if bool(valid.any()):
                max_label = max(max_label, int(y[valid].max()))
                min_label = min(min_label, int(y[valid].min()))
                unique_labels.update(int(value) for value in torch.unique(y[valid]).tolist())
        split_info[split] = {
            "num_graphs": int(graphs),
            "sample_nodes": sample_nodes,
            "sample_edges": sample_edges,
        }
    if max_label < 0:
        raise RuntimeError("No valid PascalVOC-SP labels found")
    inferred_num_classes = max_label + 1
    num_classes = (
        int(reported_num_classes)
        if reported_num_classes is not None and int(reported_num_classes) >= inferred_num_classes
        else inferred_num_classes
    )
    edge_attr = getattr(train0, "edge_attr", None)
    return {
        "dataset": "PascalVOC-SP",
        "task": "multi-graph node classification",
        "batching": "batch_size=1, one graph per optimization step",
        "edge_attr_ignored": edge_attr is not None,
        "edge_attr_dim": int(edge_attr.size(-1)) if edge_attr is not None and edge_attr.dim() > 1 else None,
        "in_dim": in_dim,
        "num_classes": num_classes,
        "reported_num_classes": reported_num_classes,
        "label_min": int(min_label),
        "label_max": int(max_label),
        "label_unique_count": len(unique_labels),
        "label_unique_sample": sorted(unique_labels)[:30],
        "splits": split_info,
    }


def compute_channel_stats(
    dataset: object,
    max_graphs: int | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    count = 0
    total = None
    total_sq = None
    limit = len(dataset) if max_graphs is None else min(max_graphs, len(dataset))
    for index in range(limit):
        x = dataset[index].x.float().cpu()
        if total is None:
            total = torch.zeros(x.size(-1), dtype=torch.float64)
            total_sq = torch.zeros(x.size(-1), dtype=torch.float64)
        total += x.double().sum(dim=0)
        total_sq += x.double().pow(2).sum(dim=0)
        count += x.size(0)
    if count == 0 or total is None or total_sq is None:
        raise RuntimeError("Cannot compute PascalVOC-SP feature normalization stats")
    mean = total / count
    variance = (total_sq / count - mean.pow(2)).clamp_min(0.0)
    std = variance.sqrt().clamp_min(1e-6)
    return mean.float(), std.float()


def normalize_labels(y: torch.Tensor) -> torch.Tensor:
    if y.dim() > 1 and y.size(-1) == 1:
        y = y.view(-1)
    return y.long()


def train_one(
    args: argparse.Namespace,
    datasets: dict[str, object],
    metadata: dict[str, object],
    control: str,
    seed: int,
    device: torch.device,
) -> dict[str, object]:
    set_seed(seed)
    model_mode = MODEL_MODE_MAP.get(control, control)
    model = IterativeRelationNetwork(
        in_dim=int(metadata["in_dim"]),
        reliability_dim=3 + args.rw_steps,
        hidden_dim=args.hidden_dim,
        out_dim=int(metadata["num_classes"]),
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        dropout=args.dropout,
        mode=model_mode,
        base_alpha=args.base_alpha,
        max_adjustment=args.max_adjustment,
        relation_steps=args.relation_steps,
        reliability_encoder_mode=args.reliability_encoder_mode,
        reliability_components=args.reliability_components,
        reliability_component_dim=args.reliability_component_dim,
        component_missing_mode=args.component_missing_mode,
        alpha_type=args.alpha_type,
        alpha_groups=args.alpha_groups,
    ).to(device)
    disable_gcn_cache(model)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )

    best_val = -math.inf
    best_state = None
    best_epoch = 0
    stale = 0
    start = time.time()
    for epoch in range(1, args.epochs + 1):
        train_metrics = run_epoch(
            args,
            model,
            datasets["train"],
            split="train",
            control=control,
            seed=seed,
            device=device,
            optimizer=optimizer,
            max_graphs=args.max_train_graphs,
            epoch=epoch,
            num_classes=int(metadata["num_classes"]),
        )
        val_metrics = run_epoch(
            args,
            model,
            datasets["val"],
            split="val",
            control=control,
            seed=seed,
            device=device,
            optimizer=None,
            max_graphs=args.max_val_graphs,
            epoch=epoch,
            num_classes=int(metadata["num_classes"]),
        )
        print(
            f"  epoch={epoch:03d} train_loss={train_metrics['loss']:.4f} "
            f"train_f1w={train_metrics['f1_weighted']:.4f} "
            f"val_f1w={val_metrics['f1_weighted']:.4f} "
            f"val_acc={val_metrics['accuracy']:.4f}",
            flush=True,
        )
        if val_metrics["f1_weighted"] > best_val:
            best_val = val_metrics["f1_weighted"]
            best_epoch = epoch
            best_state = {
                key: value.detach().cpu().clone()
                for key, value in model.state_dict().items()
            }
            stale = 0
        else:
            stale += 1
        if stale >= args.patience:
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    test_metrics = run_epoch(
        args,
        model,
        datasets["test"],
        split="test",
        control=control,
        seed=seed,
        device=device,
        optimizer=None,
        max_graphs=args.max_test_graphs,
        epoch=0,
        num_classes=int(metadata["num_classes"]),
    )
    val_metrics = run_epoch(
        args,
        model,
        datasets["val"],
        split="val",
        control=control,
        seed=seed,
        device=device,
        optimizer=None,
        max_graphs=args.max_val_graphs,
        epoch=0,
        num_classes=int(metadata["num_classes"]),
    )
    row = {
        "dataset": "PascalVOC-SP",
        "control": control,
        "model_mode": model_mode,
        "seed": seed,
        "best_epoch": best_epoch,
        "best_val_f1_weighted": best_val,
        "val_f1_weighted_at_best": val_metrics["f1_weighted"],
        "val_f1_macro_at_best": val_metrics["f1_macro"],
        "val_acc_at_best": val_metrics["accuracy"],
        "test_f1_weighted_at_best": test_metrics["f1_weighted"],
        "test_f1_macro_at_best": test_metrics["f1_macro"],
        "test_acc_at_best": test_metrics["accuracy"],
        "test_loss_at_best": test_metrics["loss"],
        "test_nodes": test_metrics["nodes"],
        "test_graphs": test_metrics["graphs"],
        "alpha_mean": test_metrics.get("alpha_mean", math.nan),
        "alpha_std": test_metrics.get("alpha_std", math.nan),
        "relation_relative_strength": test_metrics.get(
            "relation_relative_strength",
            math.nan,
        ),
        "relation_to_branch_disagreement": test_metrics.get(
            "relation_to_branch_disagreement",
            math.nan,
        ),
        "elapsed_sec": time.time() - start,
    }
    return row


def run_epoch(
    args: argparse.Namespace,
    model: torch.nn.Module,
    dataset: object,
    split: str,
    control: str,
    seed: int,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None,
    max_graphs: int | None,
    epoch: int,
    num_classes: int,
) -> dict[str, float]:
    training = optimizer is not None
    model.train(training)
    indices = list(range(len(dataset)))
    if training:
        generator = torch.Generator().manual_seed(seed + epoch * 1_000_003)
        indices = torch.tensor(indices)[
            torch.randperm(len(indices), generator=generator)
        ].tolist()
    if max_graphs is not None:
        indices = indices[:max_graphs]
    totals = defaultdict(float)
    true_positive = torch.zeros(num_classes, dtype=torch.float64)
    pred_count = torch.zeros(num_classes, dtype=torch.float64)
    support = torch.zeros(num_classes, dtype=torch.float64)
    diagnostic_values = defaultdict(list)
    context = torch.enable_grad() if training else torch.no_grad()
    with context:
        for graph_index in indices:
            data = dataset[graph_index]
            x, edge_index, y, reliability = graph_to_tensors(
                args,
                data,
                split=split,
                graph_index=graph_index,
                control=control,
                seed=seed,
                device=device,
            )
            valid = y >= 0
            if not bool(valid.any()):
                continue
            logits = model(x, edge_index, reliability)
            loss = F.cross_entropy(logits[valid], y[valid])
            if training:
                optimizer.zero_grad(set_to_none=True)
                loss.backward()
                if args.grad_clip > 0:
                    torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip)
                optimizer.step()
            with torch.no_grad():
                pred = logits[valid].argmax(dim=-1)
                target = y[valid]
                correct = int((pred == y[valid]).sum().item())
                nodes = int(valid.sum().item())
                totals["loss_sum"] += float(loss.detach().cpu()) * nodes
                totals["correct"] += correct
                totals["nodes"] += nodes
                totals["graphs"] += 1
                pred_cpu = pred.detach().cpu()
                target_cpu = target.detach().cpu()
                for label in range(num_classes):
                    pred_mask = pred_cpu == label
                    target_mask = target_cpu == label
                    true_positive[label] += float((pred_mask & target_mask).sum())
                    pred_count[label] += float(pred_mask.sum())
                    support[label] += float(target_mask.sum())
                if hasattr(model, "diagnostic_stats"):
                    for key, value in model.diagnostic_stats().items():
                        if value == value:
                            diagnostic_values[key].append(float(value))
    if totals["nodes"] == 0:
        raise RuntimeError(f"No valid nodes evaluated for split={split}")
    f1_macro, f1_weighted = f1_scores(true_positive, pred_count, support)
    output = {
        "loss": totals["loss_sum"] / totals["nodes"],
        "accuracy": totals["correct"] / totals["nodes"],
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "nodes": int(totals["nodes"]),
        "graphs": int(totals["graphs"]),
    }
    for key, values in diagnostic_values.items():
        if values:
            output[key] = float(sum(values) / len(values))
    return output


def graph_to_tensors(
    args: argparse.Namespace,
    data: object,
    split: str,
    graph_index: int,
    control: str,
    seed: int,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    x = data.x.float().cpu()
    if args.feature_norm == "row":
        x = row_normalize_features(x)
    elif args.feature_norm == "channel_zscore":
        x = (x - args.feature_mean) / args.feature_std
    edge_index = apply_edge_protocol(
        data.edge_index.long().cpu(),
        num_nodes=int(data.num_nodes),
        protocol=args.edge_protocol,
    )
    y = normalize_labels(data.y).cpu()
    reliability = cached_reliability(args, x, edge_index, split, graph_index)
    reliability = select_reliability_columns(reliability, args.reliability_components)
    reliability = control_reliability(reliability, control, seed, split, graph_index)
    return (
        x.to(device),
        edge_index.to(device),
        y.to(device),
        reliability.to(device),
    )


def cached_reliability(
    args: argparse.Namespace,
    x: torch.Tensor,
    edge_index: torch.Tensor,
    split: str,
    graph_index: int,
) -> torch.Tensor:
    cache_path = (
        args.cache_dir
        / f"pascalvocsp_{split}_{graph_index}_"
        f"{args.edge_protocol}_norm{feature_norm_cache_tag(args)}_"
        f"rw{args.rw_steps}_samples{args.rw_samples}_seed{args.rw_seed}.pt"
    )
    if cache_path.is_file():
        payload = torch.load(cache_path, map_location="cpu", weights_only=False)
        return payload["reliability"]
    reliability_edge_index = edge_index.flip(0)
    reliability, _, _ = compute_real_reliability(
        x,
        reliability_edge_index,
        rw_steps=args.rw_steps,
        rw_samples=args.rw_samples,
        rw_seed=args.rw_seed + graph_index,
    )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"reliability": reliability.cpu()}, cache_path)
    return reliability


def select_reliability_columns(
    reliability: torch.Tensor,
    components: list[str] | tuple[str, ...],
) -> torch.Tensor:
    selected = set(components)
    output = reliability.clone()
    if "degree" not in selected:
        output[:, 0] = 0.0
    if "local_similarity" not in selected:
        output[:, 1] = 0.0
    if "neighbor_variance" not in selected:
        output[:, 2] = 0.0
    if "rwse" not in selected and output.size(1) > 3:
        output[:, 3:] = 0.0
    return output


def control_reliability(
    reliability: torch.Tensor,
    control: str,
    seed: int,
    split: str,
    graph_index: int,
) -> torch.Tensor:
    if control in {"fixed", "feature_only", "reliability_only", "combined"}:
        return reliability
    if control in {"constant_reliability", "combined_constant"}:
        return reliability.mean(dim=0, keepdim=True).expand_as(reliability).clone()
    if control in {"shuffled_reliability", "combined_shuffled"}:
        split_offset = {"train": 0, "val": 1_000_000, "test": 2_000_000}[split]
        generator = torch.Generator().manual_seed(seed * 1_000_003 + split_offset + graph_index)
        return reliability[torch.randperm(reliability.size(0), generator=generator)]
    raise ValueError(f"Unsupported PascalVOC-SP control: {control}")


def f1_scores(
    true_positive: torch.Tensor,
    pred_count: torch.Tensor,
    support: torch.Tensor,
) -> tuple[float, float]:
    precision = true_positive / pred_count.clamp_min(1.0)
    recall = true_positive / support.clamp_min(1.0)
    f1 = 2.0 * precision * recall / (precision + recall).clamp_min(1e-12)
    macro_labels = (support > 0) | (pred_count > 0)
    weighted_labels = support > 0
    if not bool(weighted_labels.any()):
        return 0.0, 0.0
    macro = float(f1[macro_labels].mean()) if bool(macro_labels.any()) else 0.0
    weighted = float(
        (f1[weighted_labels] * support[weighted_labels]).sum()
        / support[weighted_labels].sum().clamp_min(1.0)
    )
    return macro, weighted


def feature_norm_cache_tag(args: argparse.Namespace) -> str:
    if args.feature_norm != "channel_zscore":
        return args.feature_norm
    if args.feature_mean is None or args.feature_std is None:
        raise RuntimeError("channel_zscore cache tag requires feature stats")
    digest = hashlib.sha256()
    digest.update(args.feature_mean.detach().cpu().numpy().tobytes())
    digest.update(args.feature_std.detach().cpu().numpy().tobytes())
    return f"channel_zscore_{digest.hexdigest()[:12]}"


def disable_gcn_cache(model: torch.nn.Module) -> None:
    for module in model.modules():
        if hasattr(module, "cached"):
            module.cached = False
        if hasattr(module, "_cached_edge_index"):
            module._cached_edge_index = None
        if hasattr(module, "_cached_adj_t"):
            module._cached_adj_t = None


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_analysis(path: Path, args: argparse.Namespace, rows: list[dict[str, object]]) -> None:
    lines = [
        "# PascalVOC-SP Iterative Relation Screening",
        "",
        f"- Runs: {args.runs}",
        f"- Controls: {', '.join(args.controls)}",
        f"- Edge protocol: {args.edge_protocol}",
        f"- Feature norm: {args.feature_norm}",
        f"- Feature norm cache tag: {feature_norm_cache_tag(args)}",
        f"- Reliability encoder: {args.reliability_encoder_mode}",
        f"- Reliability component dim: {args.reliability_component_dim}",
        f"- RW steps: {args.rw_steps}",
        f"- Alpha type: {args.alpha_type}",
        f"- Relation steps: {args.relation_steps}",
        f"- Batch policy: one graph per step; GCNConv cache disabled",
        "- Primary metric: weighted F1; macro F1 and accuracy are secondary.",
        "- Edge attributes are ignored in this runner, so it is an edge-index-only adaptation and not a same-input-protocol comparison to edge-aware GraphGPS/GatedGCN.",
        "- Shuffled/constant reliability controls are mapped to reliability_only or combined model modes; the fake reliability is applied at the input.",
        "",
        "## Results",
        "",
        "| Control | Model mode | Seed | Best Val F1w | Test F1w | Test F1m | Test Acc | Alpha | Relation strength |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {control} | {model_mode} | {seed} | {best_val_f1_weighted:.4f} | "
            "{test_f1_weighted_at_best:.4f} | {test_f1_macro_at_best:.4f} | "
            "{test_acc_at_best:.4f} | {alpha_mean:.4f} | "
            "{relation_relative_strength:.4f} |".format(
                **format_row(row)
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_row(row: dict[str, object]) -> dict[str, object]:
    output = dict(row)
    for key in (
        "best_val_f1_weighted",
        "test_f1_weighted_at_best",
        "test_f1_macro_at_best",
        "test_acc_at_best",
        "alpha_mean",
        "relation_relative_strength",
    ):
        value = output.get(key, math.nan)
        output[key] = float(value) if value == value else math.nan
    return output


if __name__ == "__main__":
    main()
