from __future__ import annotations

import argparse
from pathlib import Path

from src.real_data import REAL_DATASETS, load_and_validate_dataset, write_validation_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download missing PyG datasets and validate provenance/integrity."
    )
    parser.add_argument("--datasets", nargs="+", choices=REAL_DATASETS, default=list(REAL_DATASETS))
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--report", type=Path, default=Path("outputs/real_dataset_validation.json"))
    parser.add_argument("--no-download", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parent
    data_root = args.data_root if args.data_root.is_absolute() else root / args.data_root
    report_path = args.report if args.report.is_absolute() else root / args.report

    reports = []
    for index, name in enumerate(args.datasets, start=1):
        print(f"[{index}/{len(args.datasets)}] validating {name}", flush=True)
        _, report = load_and_validate_dataset(
            name,
            data_root,
            allow_download=not args.no_download,
        )
        reports.append(report)
        actual = report["actual"]
        print(
            f"  valid: nodes={actual['num_nodes']} edges={actual['num_edges']} "
            f"features={actual['num_features']} classes={actual['num_classes']} "
            f"splits={actual['num_splits']}",
            flush=True,
        )

    write_validation_report(reports, report_path)
    print(f"\nValidation report: {report_path}")


if __name__ == "__main__":
    main()
