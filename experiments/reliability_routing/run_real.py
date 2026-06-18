from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from run_synthetic import collect_diagnostics, move_data
from src.data import RELIABILITY_COMPONENTS, select_reliability_components, set_seed
from src.models import build_model
from src.real_data import (
    REAL_DATASETS,
    load_and_validate_dataset,
    prepare_graph_data,
    select_mask,
    validation_fingerprint,
    write_validation_report,
)


REAL_MODELS = ("mlp", "gcn", "linear_gt", "qk_gt", "gate_gt", "reliability_gt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=REAL_DATASETS, required=True)
    parser.add_argument("--model", choices=REAL_MODELS, required=True)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/real"))
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--normalize-features", action=argparse.BooleanOptionalAction, default=True)
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
    parser.add_argument("--qk-strength-init", type=float, default=-5.0)
    parser.add_argument("--fixed-qk-strength", type=float, default=None)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--epochs", type=int, default=500)
    parser.add_argument("--patience", type=int, default=100)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    data_root = args.data_root if args.data_root.is_absolute() else root / args.data_root
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but torch.cuda.is_available() is False")
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

    num_splits = int(validation["actual"]["num_splits"])
    cache_key = (
        f"{validation_fingerprint(validation)}:"
        f"norm={int(args.normalize_features)}:"
        f"steps={args.rw_steps}:samples={args.rw_samples}:seed={args.rw_seed}"
    )
    cache_path = (
        data_root
        / "_reliability_cache"
        / (
            f"{args.dataset}_norm{int(args.normalize_features)}_"
            f"rw{args.rw_steps}_samples{args.rw_samples}_seed{args.rw_seed}.pt"
        )
    )
    base_data = prepare_graph_data(
        pyg_data,
        split=0,
        rw_steps=args.rw_steps,
        rw_samples=args.rw_samples,
        rw_seed=args.rw_seed,
        normalize_features=args.normalize_features,
        cache_path=cache_path,
        cache_key=cache_key,
    )
    base_data = select_reliability_components(base_data, args.reliability_components)
    rows = []
    for run in range(args.runs):
        split, seed = run_assignment(run, num_splits)
        base_data.train_mask = select_mask(pyg_data.train_mask, split).clone()
        base_data.val_mask = select_mask(pyg_data.val_mask, split).clone()
        base_data.test_mask = select_mask(pyg_data.test_mask, split).clone()
        print(
            f"[{run + 1}/{args.runs}] dataset={args.dataset} model={args.model} "
            f"split={split} seed={seed}",
            flush=True,
        )
        rows.append(train_one_real(args, base_data, device, split, seed))

    path = out_dir / f"{args.dataset}_{args.model}.csv"
    write_csv(path, rows)
    values = np.array([float(row["test_acc_at_best_val"]) for row in rows])
    print(f"test_acc mean={values.mean():.4f} std={values.std():.4f}")
    print(f"saved: {path}")


def run_assignment(run: int, num_splits: int) -> tuple[int, int]:
    if num_splits == 1:
        return 0, run
    return run % num_splits, run // num_splits


def train_one_real(
    args: argparse.Namespace,
    base_data,
    device: torch.device,
    split: int,
    seed: int,
) -> dict[str, float | str | int]:
    set_seed(seed)
    data = move_data(base_data, device)
    model = build_model(
        name=args.model,
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        qk_reliability_dim=data.reliability_qk.size(1),
        hidden_dim=args.hidden_dim,
        out_dim=int(data.y.max().item()) + 1,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        dropout=args.dropout,
        qk_strength_init=args.qk_strength_init,
        fixed_qk_strength=args.fixed_qk_strength,
    ).to(device)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )

    best_val = -1.0
    best_test = 0.0
    best_epoch = -1
    best_diagnostics = collect_diagnostics(model, data)
    stale = 0
    start = time.time()
    for epoch in range(args.epochs):
        model.train()
        optimizer.zero_grad()
        logits = model(
            data.x,
            data.edge_index,
            data.reliability_gate,
            data.reliability_qk,
        )
        loss = F.cross_entropy(logits[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            logits = model(
                data.x,
                data.edge_index,
                data.reliability_gate,
                data.reliability_qk,
            )
            val_acc = accuracy(logits, data.y, data.val_mask)
            test_acc = accuracy(logits, data.y, data.test_mask)
        if val_acc > best_val:
            best_val = val_acc
            best_test = test_acc
            best_epoch = epoch
            best_diagnostics = collect_diagnostics(model, data)
            stale = 0
        else:
            stale += 1
        if stale >= args.patience:
            break

    row = {
        "dataset": args.dataset,
        "model": args.model,
        "run": split if args.runs == 1 else f"{split}:{seed}",
        "split": split,
        "seed": seed,
        "best_epoch": best_epoch,
        "best_val_acc": best_val,
        "test_acc_at_best_val": best_test,
        "reliability_components": ",".join(args.reliability_components),
        "normalize_features": args.normalize_features,
        "rw_steps": args.rw_steps,
        "rw_samples": args.rw_samples,
        "qk_strength_init": args.qk_strength_init,
        "fixed_qk_strength": (
            args.fixed_qk_strength
            if args.fixed_qk_strength is not None
            else float("nan")
        ),
        "elapsed_sec": time.time() - start,
    }
    row.update(best_diagnostics)
    return row


def accuracy(logits: torch.Tensor, y: torch.Tensor, mask: torch.Tensor) -> float:
    return float((logits[mask].argmax(dim=-1) == y[mask]).float().mean())


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
