from __future__ import annotations

import argparse
import json
from collections import Counter
from enum import Enum
from pathlib import Path
from zoneinfo import ZoneInfo

from romeo_crt_engine.crt.detector import detect_dataset, load_detector_dataset

NEW_YORK = ZoneInfo("America/New_York")


def _enum_text(value: object) -> str:
    if isinstance(value, Enum):
        return str(value.value)
    return str(value)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run frozen CRT detector frequency analysis without emitting P&L or TradePlan prices."
        )
    )
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument(
        "--c3-local-year",
        type=int,
        help=(
            "Restrict reported rolling candidates to C3 candles whose America/New_York local "
            "open year equals this value. Raw data may include fixed context padding."
        ),
    )
    args = parser.parse_args()

    dataset = load_detector_dataset(args.dataset_dir)
    detector_run = detect_dataset(dataset)

    candidates = detector_run.candidates
    if args.c3_local_year is not None:
        candidates = tuple(
            candidate
            for candidate in candidates
            if candidate.c3_open_time.astimezone(NEW_YORK).year == args.c3_local_year
        )

    reason_counts = Counter(_enum_text(candidate.reason) for candidate in candidates)
    state_counts = Counter(_enum_text(candidate.state) for candidate in candidates)
    plan_candidates = tuple(candidate for candidate in candidates if candidate.trade_plan is not None)

    output = {
        "schema_version": "P6_FREQUENCY_REPORT_V1",
        "analysis_mode": "FREQUENCY_ONLY_NO_PNL",
        "strategy_version": detector_run.strategy_version,
        "detector_version": detector_run.detector_version,
        "dataset_version": detector_run.dataset.dataset_version,
        "manifest_sha256": detector_run.dataset.manifest_sha256,
        "normalized_sha256": detector_run.dataset.normalized_sha256,
        "provider": detector_run.dataset.provider,
        "venue": detector_run.dataset.venue,
        "symbol": detector_run.dataset.symbol,
        "h1_rows": dataset.identity.h1_rows,
        "d1_rows": dataset.identity.d1_rows,
        "detector_run_sha256": detector_run.run_sha256,
        "c3_local_year_filter": args.c3_local_year,
        "candidate_count": len(candidates),
        "trade_plan_count": len(plan_candidates),
        "reason_counts": dict(sorted(reason_counts.items())),
        "state_counts": dict(sorted(state_counts.items())),
        "trade_plan_timestamps": [
            candidate.trade_plan.entry_time.isoformat()
            for candidate in plan_candidates
            if candidate.trade_plan is not None
        ],
        "pnl_fields_emitted": False,
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
