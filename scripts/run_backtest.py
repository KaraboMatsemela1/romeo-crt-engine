from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Any

from romeo_crt_engine.backtest.engine import run_backtest
from romeo_crt_engine.backtest.models import (
    BASE_COSTS,
    IDEAL_COSTS,
    SEVERE_COSTS,
    STRESSED_COSTS,
    BacktestConfig,
    CostModel,
)
from romeo_crt_engine.crt.detector import detect_dataset, load_detector_dataset

COST_MODELS: dict[str, CostModel] = {
    "ideal": IDEAL_COSTS,
    "base": BASE_COSTS,
    "stressed": STRESSED_COSTS,
    "severe": SEVERE_COSTS,
}


def _json_default(value: object) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()  # type: ignore[no-any-return, union-attr]
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


def _quantity_step(dataset_dir: Path) -> Decimal:
    document = json.loads((dataset_dir / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise TypeError("dataset manifest must be a JSON object")
    value = document.get("quantity_step")
    if not isinstance(value, str):
        raise TypeError("dataset manifest quantity_step must be a string")
    return Decimal(value)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run CRT-DETECTOR-v0.1 and CRT-BACKTEST-v0.1 on a trusted dataset."
    )
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--require-dataset-version")
    parser.add_argument("--require-manifest-sha256")
    parser.add_argument("--cost-scenario", choices=tuple(COST_MODELS), default="base")
    parser.add_argument("--initial-equity", type=Decimal, default=Decimal(100_000))
    parser.add_argument("--risk-fraction", type=Decimal, default=Decimal("0.005"))
    parser.add_argument("--max-concurrent-positions", type=int, default=1)
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

    detector_run = detect_dataset(dataset)
    config = BacktestConfig(
        initial_equity=args.initial_equity,
        risk_fraction=args.risk_fraction,
        max_concurrent_positions=args.max_concurrent_positions,
        cost_model=COST_MODELS[args.cost_scenario],
    )
    result = run_backtest(
        detector_run,
        dataset,
        quantity_step=_quantity_step(args.dataset_dir),
        config=config,
    )

    output = {
        **result.to_summary_dict(),
        "detector_run_sha256": detector_run.run_sha256,
        "detector_status": detector_run.status.value,
        "detector_candidate_count": len(detector_run.candidates),
        "detector_trade_plan_count": detector_run.trade_plan_count,
        "cost_scenario": args.cost_scenario,
        "completed_trade_records": [asdict(trade) for trade in result.completed_trades],
        "rejection_records": [asdict(rejection) for rejection in result.rejections],
        "open_at_end_records": [asdict(item) for item in result.open_at_end],
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":"), default=_json_default))


if __name__ == "__main__":
    main()
