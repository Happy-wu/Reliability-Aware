from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import torch

from src.real_data import (
    load_and_validate_dataset,
    write_validation_report,
)


DATASETS = ("Genius", "Arxiv-year", "WikiCS", "Wiki")
DEFAULT_DATASETS = ("Genius", "Arxiv-year", "WikiCS")
LINKX_WIKI_FILES = (
    "wiki_features2M.pt",
    "wiki_edges2M.pt",
    "wiki_views2M.pt",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare and validate new candidate datasets: LINKX Genius, "
            "LINKX arxiv-year, Wiki-CS, and the large LINKX Wiki tensors."
        )
    )
    parser.add_argument("--datasets", nargs="+", choices=DATASETS, default=list(DEFAULT_DATASETS))
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument(
        "--candidate-root",
        type=Path,
        default=Path("data/new_candidates/Non-Homophily-Large-Scale"),
        help="Original unpacked CUAI repository, kept as a source archive.",
    )
    parser.add_argument(
        "--linkx-root",
        type=Path,
        default=Path("data/linkx"),
        help="Clean local storage for LINKX files used by this project.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("outputs/new_candidate_dataset_validation.json"),
    )
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument(
        "--download-large",
        action="store_true",
        help=(
            "Deprecated placeholder. LINKX Wiki Google Drive links were not "
            "accessible in local testing; manually place tensors under data/linkx/wiki."
        ),
    )
    parser.add_argument(
        "--inspect-large-tensors",
        action="store_true",
        help="Load LINKX Wiki tensors to validate shapes. This can use a lot of RAM.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    data_root = resolve(root, args.data_root)
    candidate_root = resolve(root, args.candidate_root)
    linkx_root = resolve(root, args.linkx_root)
    report_path = resolve(root, args.report)

    reports = []
    for index, name in enumerate(args.datasets, start=1):
        print(f"[{index}/{len(args.datasets)}] preparing {name}", flush=True)
        if name == "Wiki":
            report = prepare_linkx_wiki(
                linkx_root,
                allow_download=not args.no_download,
                download_large=args.download_large,
                inspect_large_tensors=args.inspect_large_tensors,
            )
        else:
            stage_linkx_candidate(name, candidate_root, linkx_root)
            report = prepare_standard_candidate(
                name,
                data_root,
                allow_download=not args.no_download,
            )
        reports.append(report)
        status = report["status"]
        actual = report.get("actual", {})
        shape_text = (
            f" nodes={actual.get('num_nodes')} edges={actual.get('num_edges')} "
            f"features={actual.get('num_features')} classes={actual.get('num_classes')} "
            f"splits={actual.get('num_splits')}"
            if actual
            else ""
        )
        print(f"  {status}:{shape_text}", flush=True)

    write_validation_report(reports, report_path)
    print(f"\nValidation report: {report_path}", flush=True)


def resolve(root: Path, path: Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else root / path


def prepare_standard_candidate(
    name: str,
    data_root: Path,
    allow_download: bool,
) -> dict[str, object]:
    _, report = load_and_validate_dataset(
        name,
        data_root,
        allow_download=allow_download,
    )
    return report


def stage_linkx_candidate(name: str, candidate_root: Path, linkx_root: Path) -> None:
    """Copy files from the unpacked CUAI repository into the clean data/linkx tree."""
    if name == "Genius":
        copy_if_available(
            candidate_root / "data" / "genius.mat",
            linkx_root / "genius" / "genius.mat",
        )
        copy_if_available(
            candidate_root / "data" / "splits" / "genius-splits.npy",
            linkx_root / "genius" / "genius-splits.npy",
        )
    elif name == "Arxiv-year":
        copy_if_available(
            candidate_root / "data" / "splits" / "arxiv-year-splits.npy",
            linkx_root / "arxiv-year" / "arxiv-year-splits.npy",
        )


def copy_if_available(src: Path, dst: Path) -> None:
    if not src.is_file():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_file() and dst.stat().st_size == src.stat().st_size:
        return
    shutil.copy2(src, dst)


def prepare_linkx_wiki(
    linkx_root: Path,
    allow_download: bool,
    download_large: bool,
    inspect_large_tensors: bool,
) -> dict[str, object]:
    data_dir = linkx_root / "wiki"
    data_dir.mkdir(parents=True, exist_ok=True)

    paths = {name: data_dir / name for name in LINKX_WIKI_FILES}
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        message = (
            "LINKX Wiki tensors are unavailable in the current local mirror. "
            "Manually place wiki_features2M.pt, wiki_edges2M.pt, and "
            "wiki_views2M.pt under data/linkx/wiki if obtained from a valid mirror."
        )
        if download_large:
            message += " --download-large is intentionally disabled because the official Google Drive IDs failed via gdown."
        return wiki_missing_report(paths, missing, message)

    raw_files = file_manifest(paths.values())
    report: dict[str, object] = {
        "dataset": "Wiki",
        "status": "downloaded",
        "source": "LINKX Non-Homophily-Large-Scale wiki",
        "source_url": "https://github.com/CUAI/Non-Homophily-Large-Scale",
        "primary_metric": "accuracy",
        "raw_files": raw_files,
        "errors": [],
        "notes": [
            "Large candidate dataset. Full training is not recommended before prescreening.",
            "The main loader creates deterministic 5-way stratified splits if labels are categorical or binned.",
        ],
    }
    if inspect_large_tensors:
        report.update(inspect_wiki_tensors(paths))
        report["status"] = "valid" if not report["errors"] else "invalid"
    return report


def wiki_missing_report(
    paths: dict[str, Path],
    missing: list[str],
    reason: str,
) -> dict[str, object]:
    return {
        "dataset": "Wiki",
        "status": "missing",
        "source": "LINKX Non-Homophily-Large-Scale wiki",
        "source_url": "https://github.com/CUAI/Non-Homophily-Large-Scale",
        "primary_metric": "accuracy",
        "raw_files": file_manifest(paths.values()),
        "missing_files": [str(paths[name]) for name in missing],
        "errors": [reason],
    }


def inspect_wiki_tensors(paths: dict[str, Path]) -> dict[str, object]:
    errors = []
    features = torch.load(paths["wiki_features2M.pt"], map_location="cpu", weights_only=False)
    edges = torch.load(paths["wiki_edges2M.pt"], map_location="cpu", weights_only=False)
    labels = torch.load(paths["wiki_views2M.pt"], map_location="cpu", weights_only=False)
    edge_count = int(edges.size(0) if edges.dim() == 2 and edges.size(1) == 2 else edges.size(1))
    labels_flat = torch.as_tensor(labels).view(-1)
    if features.size(0) != labels_flat.numel():
        errors.append("feature row count does not match label count")
    actual = {
        "num_nodes": int(labels_flat.numel()),
        "num_edges": edge_count,
        "num_features": int(features.size(1)),
        "num_classes": int(torch.unique(labels_flat).numel()),
        "num_splits": 5,
    }
    return {
        "actual": actual,
        "tensor_shapes": {
            "features": list(features.shape),
            "edges": list(edges.shape),
            "labels": list(torch.as_tensor(labels).shape),
        },
        "errors": errors,
    }


def file_manifest(paths: object) -> list[dict[str, object]]:
    output = []
    for path in paths:
        path = Path(path)
        if path.is_file() and path.stat().st_size > 0:
            output.append(
                {
                    "path": str(path.resolve()),
                    "size_bytes": path.stat().st_size,
                }
            )
    return output


if __name__ == "__main__":
    main()
