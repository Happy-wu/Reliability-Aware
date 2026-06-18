from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from src.data import RELIABILITY_COMPONENTS, select_reliability_components, set_seed
from src.expert_models import EXPERT_MODELS, build_expert_model
from src.real_data import (
    EDGE_PROTOCOLS,
    REAL_DATASETS,
    load_and_validate_dataset,
    prepare_graph_data,
    select_mask,
    validation_fingerprint,
    write_validation_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=REAL_DATASETS, required=True)
    parser.add_argument("--model", choices=EXPERT_MODELS, required=True)
    parser.add_argument("--result-name")
    parser.add_argument("--fixed-alpha", type=float, default=0.5)
    parser.add_argument("--edge-protocol", choices=EDGE_PROTOCOLS, default="undirected")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/expert_fusion"))
    parser.add_argument("--expert-cache-dir", type=Path)
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
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-layers", type=int, default=2)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--expert-epochs", type=int, default=500)
    parser.add_argument("--gate-epochs", type=int, default=300)
    parser.add_argument("--patience", type=int, default=100)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0.0 <= args.fixed_alpha <= 1.0:
        raise ValueError("--fixed-alpha must be between 0 and 1")
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    out_dir = resolve(root, args.out_dir)
    args.expert_cache_dir = (
        resolve(root, args.expert_cache_dir)
        if args.expert_cache_dir is not None
        else None
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available")
    device = torch.device(args.device)

    pyg_data, validation = load_and_validate_dataset(
        args.dataset,
        data_root,
        allow_download=not args.no_download,
    )
    write_validation_report(
        [validation],
        out_dir / f"{args.dataset}_validation.json",
    )
    cache_key = (
        f"{validation_fingerprint(validation)}:"
        f"protocol={args.edge_protocol}:norm={int(args.normalize_features)}:"
        f"steps={args.rw_steps}:samples={args.rw_samples}:seed={args.rw_seed}"
    )
    cache_path = (
        data_root
        / "_reliability_cache"
        / (
            f"{args.dataset}_{args.edge_protocol}_norm{int(args.normalize_features)}_"
            f"rw{args.rw_steps}_samples{args.rw_samples}_seed{args.rw_seed}.pt"
        )
    )
    data = prepare_graph_data(
        pyg_data,
        split=0,
        rw_steps=args.rw_steps,
        rw_samples=args.rw_samples,
        rw_seed=args.rw_seed,
        normalize_features=args.normalize_features,
        edge_protocol=args.edge_protocol,
        cache_path=cache_path,
        cache_key=cache_key,
    )
    data = select_reliability_components(data, args.reliability_components)
    num_splits = int(validation["actual"]["num_splits"])
    rows = []
    for run in range(args.runs):
        split, seed = run_assignment(run, num_splits)
        data.train_mask = select_mask(pyg_data.train_mask, split).clone()
        data.val_mask = select_mask(pyg_data.val_mask, split).clone()
        data.test_mask = select_mask(pyg_data.test_mask, split).clone()
        print(
            f"[{run + 1}/{args.runs}] dataset={args.dataset} model={args.model} "
            f"protocol={args.edge_protocol} split={split} seed={seed}",
            flush=True,
        )
        rows.append(train_one(args, data, device, split, seed))

    result_name = args.result_name or args.model
    path = out_dir / f"{args.dataset}_{result_name}.csv"
    write_csv(path, rows)
    values = np.array([float(row["test_acc_at_best_val"]) for row in rows])
    macro_f1 = np.array([float(row["test_macro_f1_at_best_val"]) for row in rows])
    print(
        f"test_acc mean={values.mean():.4f} std={values.std():.4f}; "
        f"macro_f1 mean={macro_f1.mean():.4f}"
    )
    print(f"saved: {path}")


def train_one(args, base_data, device, split: int, seed: int) -> dict[str, object]:
    set_seed(seed)
    data = move_data(base_data, device)
    model = build_expert_model(
        name=args.model,
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        hidden_dim=args.hidden_dim,
        out_dim=int(data.y.max().item()) + 1,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        dropout=args.dropout,
        fixed_alpha=args.fixed_alpha,
    ).to(device)
    start = time.time()

    local_result = None
    global_result = None
    if args.model != "global_only":
        set_seed(seed)
        local_result = train_or_load_expert(
            cache_path=expert_cache_path(args, split, seed, "local"),
            module=model.local_expert,
            forward=lambda: model.local_expert(data.x, data.edge_index),
            data=data,
            args=args,
        )
    if args.model != "gcn_pyg":
        set_seed(seed + 100_000)
        global_result = train_or_load_expert(
            cache_path=expert_cache_path(args, split, seed, "global"),
            module=model.global_expert,
            forward=lambda: model.global_expert(data.x),
            data=data,
            args=args,
        )

    if args.model in {"ordinary_gate", "reliability_gate"}:
        freeze(model.local_expert)
        freeze(model.global_expert)
        set_seed(seed + 200_000)
        final_result = train_module(
            model.node_gate,
            lambda: model(data.x, data.edge_index, data.reliability_gate),
            data,
            args.gate_epochs,
            args.patience,
            args.lr,
            args.weight_decay,
        )
    else:
        model.eval()
        with torch.no_grad():
            logits = model(data.x, data.edge_index, data.reliability_gate)
        final_result = evaluate_result(logits, data, epoch=0)

    model.eval()
    with torch.no_grad():
        logits = model(data.x, data.edge_index, data.reliability_gate)
        if args.model == "fixed_alpha" and args.fixed_alpha == 1.0:
            local_logits = model.forward_local(data.x, data.edge_index)
            if not torch.equal(logits, local_logits):
                max_error = float((logits - local_logits).abs().max().cpu())
                raise AssertionError(
                    f"alpha=1 failed exact GCN fallback; max_error={max_error}"
                )
        if args.model == "fixed_alpha" and args.fixed_alpha == 0.0:
            global_logits = model.global_expert(data.x)
            if not torch.equal(logits, global_logits):
                max_error = float((logits - global_logits).abs().max().cpu())
                raise AssertionError(
                    f"alpha=0 failed exact global fallback; max_error={max_error}"
                )

    diagnostics = model.diagnostic_stats()
    diagnostics.update(gate_correlations(model, data))
    result_name = args.result_name or args.model
    return {
        "dataset": args.dataset,
        "model": result_name,
        "model_family": args.model,
        "edge_protocol": args.edge_protocol,
        "run": f"{split}:{seed}",
        "split": split,
        "seed": seed,
        "best_epoch": final_result["epoch"],
        "best_val_acc": final_result["val_acc"],
        "test_acc_at_best_val": final_result["test_acc"],
        "test_macro_f1_at_best_val": final_result["test_macro_f1"],
        "local_expert_val_acc": value_or_nan(local_result, "val_acc"),
        "global_expert_val_acc": value_or_nan(global_result, "val_acc"),
        "fixed_alpha": args.fixed_alpha if args.model == "fixed_alpha" else math.nan,
        "reliability_components": ",".join(args.reliability_components),
        "elapsed_sec": time.time() - start,
        **diagnostics,
    }


def train_or_load_expert(
    cache_path: Path | None,
    module: torch.nn.Module,
    forward,
    data,
    args,
) -> dict[str, float | int]:
    if cache_path is not None and cache_path.exists():
        payload = torch.load(cache_path, map_location=data.x.device, weights_only=False)
        module.load_state_dict(payload["state_dict"])
        return payload["result"]
    result = train_module(
        module,
        forward,
        data,
        args.expert_epochs,
        args.patience,
        args.lr,
        args.weight_decay,
    )
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "state_dict": {
                    key: value.detach().cpu()
                    for key, value in module.state_dict().items()
                },
                "result": result,
            },
            cache_path,
        )
    return result


def expert_cache_path(
    args,
    split: int,
    seed: int,
    expert: str,
) -> Path | None:
    if args.expert_cache_dir is None:
        return None
    source_digest = hashlib.sha256()
    root = Path(__file__).resolve().parent
    source_digest.update((root / "src" / "expert_models.py").read_bytes())
    source_digest.update(Path(__file__).read_bytes())
    config = {
        "source": source_digest.hexdigest(),
        "dataset": args.dataset,
        "edge_protocol": args.edge_protocol,
        "normalize_features": args.normalize_features,
        "split": split,
        "seed": seed,
        "expert": expert,
        "hidden_dim": args.hidden_dim,
        "num_layers": args.num_layers,
        "num_heads": args.num_heads,
        "dropout": args.dropout,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "expert_epochs": args.expert_epochs,
        "patience": args.patience,
    }
    digest = hashlib.sha256(
        json.dumps(config, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]
    return (
        args.expert_cache_dir
        / args.dataset
        / args.edge_protocol
        / f"{expert}_split{split}_seed{seed}_{digest}.pt"
    )


def train_module(
    module: torch.nn.Module,
    forward,
    data,
    epochs: int,
    patience: int,
    lr: float,
    weight_decay: float,
) -> dict[str, float | int]:
    optimizer = torch.optim.AdamW(
        module.parameters(),
        lr=lr,
        weight_decay=weight_decay,
    )
    best_state = copy.deepcopy(module.state_dict())
    best = {"epoch": -1, "val_acc": -1.0, "test_acc": 0.0, "test_macro_f1": 0.0}
    stale = 0
    for epoch in range(epochs):
        module.train()
        optimizer.zero_grad()
        logits = forward()
        loss = F.cross_entropy(logits[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()

        module.eval()
        with torch.no_grad():
            result = evaluate_result(forward(), data, epoch)
        if result["val_acc"] > best["val_acc"]:
            best = result
            best_state = copy.deepcopy(module.state_dict())
            stale = 0
        else:
            stale += 1
        if stale >= patience:
            break
    module.load_state_dict(best_state)
    return best


def evaluate_result(logits, data, epoch: int) -> dict[str, float | int]:
    return {
        "epoch": epoch,
        "val_acc": accuracy(logits, data.y, data.val_mask),
        "test_acc": accuracy(logits, data.y, data.test_mask),
        "test_macro_f1": macro_f1(logits, data.y, data.test_mask),
    }


def gate_correlations(model, data) -> dict[str, float]:
    output = {
        "alpha_corr_degree": math.nan,
        "alpha_corr_local_similarity": math.nan,
        "alpha_corr_neighbor_variance": math.nan,
        "alpha_corr_rwse": math.nan,
        "alpha_corr_label_homophily": math.nan,
    }
    alpha = model.latest_alpha
    if alpha is None:
        return output
    alpha_np = alpha.view(-1).cpu().numpy()
    reliability = data.reliability_gate_raw.cpu()
    output["alpha_corr_degree"] = safe_corr(alpha_np, reliability[:, 0].numpy())
    output["alpha_corr_local_similarity"] = safe_corr(
        alpha_np,
        data.local_similarity.cpu().numpy(),
    )
    output["alpha_corr_neighbor_variance"] = safe_corr(
        alpha_np,
        reliability[:, 2].numpy(),
    )
    output["alpha_corr_rwse"] = safe_corr(
        alpha_np,
        reliability[:, 3:].mean(dim=1).numpy(),
    )
    homophily = received_label_homophily(
        data.edge_index.cpu(),
        data.y.cpu(),
        data.y.numel(),
    )
    output["alpha_corr_label_homophily"] = safe_corr(alpha_np, homophily.numpy())
    return output


def received_label_homophily(edge_index, y, num_nodes: int) -> torch.Tensor:
    source, target = edge_index
    same = (y[source] == y[target]).float()
    counts = torch.bincount(target, minlength=num_nodes).float()
    totals = torch.zeros(num_nodes).scatter_add_(0, target, same)
    return totals / counts.clamp_min(1.0)


def freeze(module: torch.nn.Module) -> None:
    module.eval()
    for parameter in module.parameters():
        parameter.requires_grad_(False)


def move_data(data, device):
    for field in (
        "x",
        "y",
        "edge_index",
        "reliability",
        "reliability_gate",
        "reliability_qk",
        "reliability_gate_raw",
        "reliability_qk_raw",
        "train_mask",
        "val_mask",
        "test_mask",
        "local_similarity",
    ):
        setattr(data, field, getattr(data, field).to(device))
    return data


def accuracy(logits, y, mask) -> float:
    return float((logits[mask].argmax(dim=-1) == y[mask]).float().mean())


def macro_f1(logits, y, mask) -> float:
    prediction = logits[mask].argmax(dim=-1).cpu().numpy()
    target = y[mask].cpu().numpy()
    try:
        from sklearn.metrics import f1_score
    except ImportError as exc:
        raise RuntimeError("macro-F1 requires scikit-learn") from exc
    return float(f1_score(target, prediction, average="macro", zero_division=0))


def safe_corr(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) < 1e-8 or np.std(b) < 1e-8:
        return math.nan
    return float(np.corrcoef(a, b)[0, 1])


def value_or_nan(result, key: str) -> float:
    return float(result[key]) if result is not None else math.nan


def run_assignment(run: int, num_splits: int) -> tuple[int, int]:
    return (0, run) if num_splits == 1 else (run % num_splits, run // num_splits)


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
