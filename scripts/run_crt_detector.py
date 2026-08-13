from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from enum import Enum
from pathlib import Path
from typing import Any

from romeo_crt_engine.crt.detector import detect_dataset, load_detector_dataset


def _json_default(value: object) -> Any:
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()  # type: ignore[no-any-return, union-attr]
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the frozen CRT v0.1 detector on a trusted dataset.")
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--require-dataset-version")
    parser.add_argument("--require-manifest-sha256")
    args = parser.parse_args()

    dataset = load_detector_dataset(args.dataset_dir)
    if (
        args.require_dataset_version is not None
        and dataset.identity.dataset_version != args.require_dataset_version
    ):
        raise SystemExit(
            f"dataset version mismatch: {dataset.identity.dataset_version} "
            f"!= {args.require_dataset_version}"
        )
    if (
        args.require_manifest_sha256 is not None
        and dataset.identity.manifest_sha256 != args.require_manifest_sha256
    ):
        raise SystemExit(
            f"manifest SHA mismatch: {dataset.identity.manifest_sha256} "
            f"!= {args.require_manifest_sha256}"
        )

    run = detect_dataset(dataset)
    output = {
        "strategy_version": run.strategy_version,
        "detector_version": run.detector_version,
        "dataset_version": run.dataset.dataset_version,
        "manifest_sha256": run.dataset.manifest_sha256,
        "symbol": run.dataset.symbol,
        "status": run.status.value,
        "candidate_count": len(run.candidates),
        "trade_plan_count": run.trade_plan_count,
        "no_signal_count": run.no_signal_count,
        "run_sha256": run.run_sha256,
        "candidates": [asdict(candidate) for candidate in run.candidates],
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":"), default=_json_default))


if __name__ == "__main__":
    main()
