from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import torch
import torch.nn.functional as F
from tqdm import trange

from src.data import (
    RELIABILITY_COMPONENTS,
    make_synthetic_graph,
    select_reliability_components,
    set_seed,
)
from src.models import build_model


def accuracy(logits: torch.Tensor, y: torch.Tensor, mask: torch.Tensor) -> float:
    pred = logits.argmax(dim=-1)
    return (pred[mask] == y[mask]).float().mean().item()


def train_one(args: argparse.Namespace, seed: int) -> dict[str, float | str | int]:
    set_seed(seed)
    device = torch.device(args.device if torch.cuda.is_available() or args.device == "cpu" else "cpu")
    data = make_synthetic_graph(
        num_nodes=args.num_nodes,
        num_classes=args.num_classes,
        feature_dim=args.feature_dim,
        graph_type=args.graph_type,
        feature_noise=args.feature_noise,
        edge_noise=args.edge_noise,
        seed=seed,
        rw_steps=args.rw_steps,
    )
    data = select_reliability_components(data, args.reliability_components)
    data = move_data(data, device)

    model = build_model(
        name=args.model,
        in_dim=data.x.size(1),
        reliability_dim=data.reliability_gate.size(1),
        qk_reliability_dim=data.reliability_qk.size(1),
        hidden_dim=args.hidden_dim,
        out_dim=args.num_classes,
        num_layers=args.num_layers,
        num_heads=args.num_heads,
        dropout=args.dropout,
        qk_strength_init=args.qk_strength_init,
        fixed_qk_strength=args.fixed_qk_strength,
    ).to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    best_val = 0.0
    best_test = 0.0
    best_diagnostics = empty_diagnostics()
    patience = args.patience
    stale = 0
    start = time.time()

    iterator = trange(args.epochs, disable=not args.verbose, desc=f"{args.model}:{seed}")
    for _ in iterator:
        model.train()
        opt.zero_grad()
        logits = model(data.x, data.edge_index, data.reliability_gate, data.reliability_qk)
        loss = F.cross_entropy(logits[data.train_mask], data.y[data.train_mask])
        loss.backward()
        opt.step()

        model.eval()
        with torch.no_grad():
            logits = model(data.x, data.edge_index, data.reliability_gate, data.reliability_qk)
            val_acc = accuracy(logits, data.y, data.val_mask)
            test_acc = accuracy(logits, data.y, data.test_mask)

        if val_acc > best_val:
            best_val = val_acc
            best_test = test_acc
            best_diagnostics = collect_diagnostics(model, data)
            stale = 0
        else:
            stale += 1
        if stale >= patience:
            break

    row = {
        "model": args.model,
        "graph_type": args.graph_type,
        "seed": seed,
        "reliability_components": ",".join(args.reliability_components),
        "reliability_encoder": (
            "branch_specific" if args.model.endswith("_encoded") else "separate"
        ),
        "best_val_acc": best_val,
        "test_acc_at_best_val": best_test,
        "qk_strength_init": args.qk_strength_init,
        "fixed_qk_strength": args.fixed_qk_strength if args.fixed_qk_strength is not None else float("nan"),
        "elapsed_sec": time.time() - start,
    }
    row.update(best_diagnostics)
    return row


def empty_diagnostics() -> dict[str, float]:
    return {
        "qk_strength_mean": float("nan"),
        "qk_strength_layer1": float("nan"),
        "qk_strength_layer2": float("nan"),
        "qk_gamma_q_abs_dev_mean": float("nan"),
        "qk_gamma_k_abs_dev_mean": float("nan"),
        "qk_gamma_q_std": float("nan"),
        "qk_gamma_k_std": float("nan"),
        "qk_gamma_q_abs_dev_max": float("nan"),
        "qk_gamma_k_abs_dev_max": float("nan"),
        "gate_corr_degree": float("nan"),
        "gate_corr_local_similarity": float("nan"),
        "gate_corr_neighbor_variance": float("nan"),
        "gate_corr_rwse_mean": float("nan"),
        "gate_corr_layer1_local_similarity": float("nan"),
        "gate_corr_layer2_local_similarity": float("nan"),
        "gate_mean": float("nan"),
        "gate_std": float("nan"),
        "gate_min": float("nan"),
        "gate_max": float("nan"),
        "local_branch_norm_mean": float("nan"),
        "global_branch_norm_mean": float("nan"),
        "mixed_branch_norm_mean": float("nan"),
        "local_global_cosine_mean": float("nan"),
    }


def collect_diagnostics(model: torch.nn.Module, data) -> dict[str, float]:
    diagnostics = empty_diagnostics()

    strengths = getattr(model, "qk_strengths", lambda: [])()
    if strengths:
        diagnostics["qk_strength_mean"] = float(np.mean(strengths))
        diagnostics["qk_strength_layer1"] = strengths[0] if len(strengths) >= 1 else float("nan")
        diagnostics["qk_strength_layer2"] = strengths[1] if len(strengths) >= 2 else float("nan")

    gamma_stats = getattr(model, "qk_gamma_stats", lambda: {})()
    diagnostics.update(gamma_stats)
    diagnostics.update(getattr(model, "branch_stats", lambda: {})())

    gate = getattr(model, "latest_gate", None)
    if gate is not None:
        gate_np = gate.detach().cpu().view(-1).numpy()
        rel = data.reliability_gate_raw.detach().cpu()
        diagnostics["gate_corr_degree"] = safe_corr(gate_np, rel[:, 0].numpy())
        diagnostics["gate_corr_local_similarity"] = safe_corr(
            gate_np,
            data.local_similarity.detach().cpu().view(-1).numpy(),
        )
        diagnostics["gate_corr_neighbor_variance"] = safe_corr(gate_np, rel[:, 2].numpy())
        diagnostics["gate_corr_rwse_mean"] = safe_corr(gate_np, rel[:, 3:].mean(dim=1).numpy())

    gates_by_layer = getattr(model, "latest_gates_by_layer", [])
    if len(gates_by_layer) >= 1:
        diagnostics["gate_corr_layer1_local_similarity"] = safe_corr(
            gates_by_layer[0].detach().cpu().view(-1).numpy(),
            data.local_similarity.detach().cpu().view(-1).numpy(),
        )
    if len(gates_by_layer) >= 2:
        diagnostics["gate_corr_layer2_local_similarity"] = safe_corr(
            gates_by_layer[1].detach().cpu().view(-1).numpy(),
            data.local_similarity.detach().cpu().view(-1).numpy(),
        )

    return diagnostics


def safe_corr(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) < 1e-8 or np.std(b) < 1e-8:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def move_data(data, device: torch.device):
    data.x = data.x.to(device)
    data.y = data.y.to(device)
    data.edge_index = data.edge_index.to(device)
    data.reliability = data.reliability.to(device)
    data.reliability_gate = data.reliability_gate.to(device)
    data.reliability_qk = data.reliability_qk.to(device)
    data.reliability_gate_raw = data.reliability_gate_raw.to(device)
    data.reliability_qk_raw = data.reliability_qk_raw.to(device)
    data.train_mask = data.train_mask.to(device)
    data.val_mask = data.val_mask.to(device)
    data.test_mask = data.test_mask.to(device)
    data.local_similarity = data.local_similarity.to(device)
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        choices=[
            "mlp",
            "gcn",
            "linear_gt",
            "q_only_gt",
            "k_only_gt",
            "qk_gt",
            "gate_gt",
            "reliability_gt",
            "qk_gt_encoded",
            "gate_gt_encoded",
            "reliability_gt_encoded",
        ],
        default="reliability_gt",
    )
    parser.add_argument("--graph-type", choices=["homophily", "heterophily", "mixed", "noisy"], default="heterophily")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--num-nodes", type=int, default=900)
    parser.add_argument("--num-classes", type=int, default=3)
    parser.add_argument("--feature-dim", type=int, default=32)
    parser.add_argument("--feature-noise", type=float, default=0.7)
    parser.add_argument("--edge-noise", type=float, default=0.0)
    parser.add_argument("--rw-steps", type=int, default=4)
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
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--patience", type=int, default=60)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows = [train_one(args, seed) for seed in args.seeds]

    acc = np.array([r["test_acc_at_best_val"] for r in rows], dtype=float)
    print(f"model={args.model} graph={args.graph_type}")
    print(f"test_acc mean={acc.mean():.4f} std={acc.std():.4f}")
    corr = np.array([r["gate_corr_local_similarity"] for r in rows], dtype=float)
    if not np.isnan(corr).all():
        print(f"gate/local-sim corr mean={np.nanmean(corr):.4f} std={np.nanstd(corr):.4f}")

    component_tag = "-".join(args.reliability_components)
    strength_tag = (
        f"fixed-{format_tag_float(args.fixed_qk_strength)}"
        if args.fixed_qk_strength is not None
        else f"init-{format_tag_float(args.qk_strength_init)}"
    )
    out_path = args.out_dir / (
        f"{args.graph_type}_{args.model}_{component_tag}_{strength_tag}.csv"
    )
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"saved: {out_path}")


def format_tag_float(value: float) -> str:
    return f"{value:g}".replace("-", "m").replace(".", "p")


if __name__ == "__main__":
    main()
