from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class LrgbManualSpec:
    name: str
    pyg_name: str
    manual_dir: str
    raw_files: tuple[str, ...]
    task: str


DATASETS = {
    "PascalVOC-SP": LrgbManualSpec(
        name="PascalVOC-SP",
        pyg_name="PascalVOC-SP",
        manual_dir="pascalvocsp",
        raw_files=("train.pickle", "val.pickle", "test.pickle"),
        task="multi-graph node classification",
    ),
    "PCQM-Contact": LrgbManualSpec(
        name="PCQM-Contact",
        pyg_name="PCQM-Contact",
        manual_dir="pcqmcontact",
        raw_files=("train.pt", "val.pt", "test.pt"),
        task="multi-graph link prediction",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage manually downloaded LRGB raw files and smoke-test PyG LRGBDataset."
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=tuple(DATASETS),
        default=list(DATASETS),
    )
    parser.add_argument("--manual-root", type=Path, default=Path("data/lrgb_manual"))
    parser.add_argument("--pyg-root", type=Path, default=Path("data/lrgb_pyg"))
    parser.add_argument(
        "--link-mode",
        choices=("hardlink", "copy", "symlink"),
        default="hardlink",
        help="How to stage raw files into the PyG LRGBDataset directory.",
    )
    parser.add_argument(
        "--process",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Instantiate PyG LRGBDataset and build processed train/val/test files.",
    )
    parser.add_argument(
        "--force-restage",
        action="store_true",
        help="Replace existing staged raw files.",
    )
    parser.add_argument(
        "--force-reprocess",
        action="store_true",
        help="Delete processed files before constructing PyG LRGBDataset.",
    )
    parser.add_argument("--smoke-items", type=int, default=2)
    parser.add_argument("--report", type=Path, default=Path("outputs/lrgb_manual_validation.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reports = []
    for dataset_name in args.datasets:
        spec = DATASETS[dataset_name]
        print(f"[{dataset_name}] staging raw files", flush=True)
        staged = stage_dataset(
            spec,
            manual_root=args.manual_root,
            pyg_root=args.pyg_root,
            link_mode=args.link_mode,
            force=args.force_restage,
        )
        report = {
            "dataset": dataset_name,
            "task": spec.task,
            "pyg_name": spec.pyg_name,
            "manual_raw_dir": str((args.manual_root / spec.manual_dir / "raw").resolve()),
            "pyg_raw_dir": str((args.pyg_root / spec.pyg_name.lower() / "raw").resolve()),
            "raw_files": staged,
        }
        if args.process:
            print(f"[{dataset_name}] processing/smoke-testing PyG LRGBDataset", flush=True)
            report["processed"] = process_and_summarize(
                spec,
                pyg_root=args.pyg_root,
                force_reprocess=args.force_reprocess,
                smoke_items=args.smoke_items,
            )
        reports.append(report)
    write_report(reports, args.report)
    print(f"report: {args.report.resolve()}", flush=True)


def stage_dataset(
    spec: LrgbManualSpec,
    manual_root: Path,
    pyg_root: Path,
    link_mode: str,
    force: bool,
) -> list[dict[str, object]]:
    source_dir = manual_root / spec.manual_dir / "raw"
    target_dir = pyg_root / spec.pyg_name.lower() / "raw"
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Missing manual raw directory: {source_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    staged = []
    for filename in spec.raw_files:
        source = source_dir / filename
        target = target_dir / filename
        if not source.is_file() or source.stat().st_size == 0:
            raise FileNotFoundError(f"Missing raw file: {source}")
        if target.exists() or target.is_symlink():
            if not force and same_file_size(source, target):
                pass
            else:
                target.unlink()
                link_or_copy(source, target, link_mode)
        else:
            link_or_copy(source, target, link_mode)
        staged.append(
            {
                "name": filename,
                "source": str(source.resolve()),
                "target": str(target.resolve()),
                "size_bytes": source.stat().st_size,
            }
        )
    return staged


def same_file_size(source: Path, target: Path) -> bool:
    try:
        return source.stat().st_size == target.stat().st_size
    except FileNotFoundError:
        return False


def link_or_copy(source: Path, target: Path, mode: str) -> None:
    if mode == "copy":
        shutil.copy2(source, target)
        return
    if mode == "symlink":
        try:
            target.symlink_to(source.resolve())
            return
        except OSError:
            shutil.copy2(source, target)
            return
    try:
        os.link(source, target)
    except OSError:
        shutil.copy2(source, target)


def process_and_summarize(
    spec: LrgbManualSpec,
    pyg_root: Path,
    force_reprocess: bool,
    smoke_items: int,
) -> dict[str, object]:
    try:
        from torch_geometric.datasets import LRGBDataset
    except ImportError as exc:
        raise RuntimeError(
            "PyTorch Geometric with LRGBDataset is required for LRGB processing. "
            "Run this script in the server environment."
        ) from exc

    processed_dir = pyg_root / spec.pyg_name.lower() / "processed"
    if force_reprocess and processed_dir.exists():
        shutil.rmtree(processed_dir)

    summary = {}
    for split in ("train", "val", "test"):
        dataset = LRGBDataset(root=str(pyg_root), name=spec.pyg_name, split=split)
        split_summary = summarize_dataset(dataset, smoke_items)
        split_summary["processed_file"] = str((processed_dir / f"{split}.pt").resolve())
        summary[split] = split_summary
    return summary


def summarize_dataset(dataset: object, smoke_items: int) -> dict[str, object]:
    length = len(dataset)
    node_counts = []
    edge_counts = []
    y_shapes = []
    extra_keys = set()
    for index in range(min(smoke_items, length)):
        data = dataset[index]
        node_counts.append(int(getattr(data, "num_nodes", data.x.size(0))))
        edge_counts.append(int(data.edge_index.size(1)))
        y_shapes.append(list(data.y.size()) if hasattr(data.y, "size") else [])
        for key in getattr(data, "keys", lambda: [])():
            extra_keys.add(str(key))
    return {
        "num_graphs": int(length),
        "sample_node_counts": node_counts,
        "sample_edge_counts": edge_counts,
        "sample_y_shapes": y_shapes,
        "sample_keys": sorted(extra_keys),
    }


def write_report(reports: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
