from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from romeo_crt_engine.crt.detector_v2 import DetectorDatasetV2, detect_dataset_v2
from romeo_crt_engine.market_data.models import BarTimeframe
from romeo_crt_engine.market_data.price_data_v2 import (
    ActivityMeasure,
    ActivitySemantic,
    CanonicalPriceBarV2,
    PriceComponent,
    PriceDatasetIdentityV2,
    PriceQuantumSource,
)

EXPECTED_SCHEMA = "P6B_CANONICAL_PRICE_DATASET_V2"
EXPECTED_QUALITY = "TRUSTED"
EXPECTED_COMPONENT = PriceComponent.MID


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the frozen Phase-6B detector against one already-frozen TRUSTED dataset "
            "and emit preregistered activity metrics only. This entry point does not import "
            "or invoke the backtester and does not expose P&L, trade geometry, timestamps, "
            "or candidate details."
        )
    )
    parser.add_argument("--identity", required=True, type=Path)
    parser.add_argument("--h1", required=True, type=Path)
    parser.add_argument("--d1", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def _load_json(path: Path) -> dict[str, object]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise TypeError(f"expected JSON object: {path}")
    return document


def _identity(path: Path) -> PriceDatasetIdentityV2:
    raw = _load_json(path)
    if raw.get("schema_version") != EXPECTED_SCHEMA:
        raise ValueError("activity runner requires the frozen Phase-6B dataset schema")
    if raw.get("quality_status") != EXPECTED_QUALITY:
        raise ValueError("activity runner accepts TRUSTED datasets only")
    if raw.get("price_component") != EXPECTED_COMPONENT.value:
        raise ValueError("activity runner accepts frozen MID signal data only")
    return PriceDatasetIdentityV2(
        dataset_version=str(raw["dataset_version"]),
        provider=str(raw["provider"]),
        venue=str(raw["venue"]),
        instrument=str(raw["instrument"]),
        price_component=PriceComponent(str(raw["price_component"])),
        price_quantum=Decimal(str(raw["price_quantum"])),
        price_quantum_source=PriceQuantumSource(str(raw["price_quantum_source"])),
        price_quantum_observed_at=datetime.fromisoformat(str(raw["price_quantum_observed_at_utc"])),
        instrument_metadata_sha256=str(raw["instrument_metadata_sha256"]),
        session_policy_version=str(raw["session_policy_version"]),
        normalized_sha256=str(raw["normalized_sha256"]),
        h1_rows=int(raw["h1_rows"]),
        d1_rows=int(raw["d1_rows"]),
        quality_status=str(raw["quality_status"]),
        schema_version=str(raw["schema_version"]),
    )


def _bar(raw: dict[str, object], expected: BarTimeframe) -> CanonicalPriceBarV2:
    activity_raw = raw.get("activity", [])
    if not isinstance(activity_raw, list):
        raise TypeError("canonical activity must be a list")
    activity: list[ActivityMeasure] = []
    for item in activity_raw:
        if not isinstance(item, dict):
            raise TypeError("canonical activity record must be an object")
        activity.append(
            ActivityMeasure(
                semantic=ActivitySemantic(str(item["semantic"])),
                value=Decimal(str(item["value"])),
            )
        )
    timeframe = BarTimeframe(str(raw["timeframe"]))
    if timeframe is not expected:
        raise ValueError(f"expected {expected.value} bars only")
    return CanonicalPriceBarV2(
        provider=str(raw["provider"]),
        venue=str(raw["venue"]),
        instrument=str(raw["instrument"]),
        price_component=PriceComponent(str(raw["price_component"])),
        timeframe=timeframe,
        open_time=datetime.fromisoformat(str(raw["open_time_utc"])),
        close_time=datetime.fromisoformat(str(raw["close_time_utc"])),
        open=Decimal(str(raw["open"])),
        high=Decimal(str(raw["high"])),
        low=Decimal(str(raw["low"])),
        close=Decimal(str(raw["close"])),
        source_count=int(raw["source_count"]),
        source_digest=str(raw["source_digest"]),
        session_policy_version=str(raw["session_policy_version"]),
        activity=tuple(activity),
    )


def _bars(path: Path, expected: BarTimeframe) -> tuple[CanonicalPriceBarV2, ...]:
    output: list[CanonicalPriceBarV2] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            raw = json.loads(line)
            if not isinstance(raw, dict):
                raise TypeError(f"canonical JSONL line {line_number} must be an object")
            output.append(_bar(raw, expected))
    return tuple(output)


def main() -> int:
    args = _parser().parse_args()
    identity = _identity(args.identity)
    dataset = DetectorDatasetV2(
        identity=identity,
        h1=_bars(args.h1, BarTimeframe.H1),
        d1=_bars(args.d1, BarTimeframe.D1),
    )
    run = detect_dataset_v2(dataset)
    reason_counts = Counter(candidate.reason.value for candidate in run.candidates)
    result = {
        "candidate_version": run.candidate_version,
        "alpha_strategy_version": run.alpha_strategy_version,
        "detector_version": run.detector_version,
        "dataset_version": run.dataset.dataset_version,
        "dataset_identity_sha256": run.dataset_identity_sha256,
        "provider": run.dataset.provider,
        "venue": run.dataset.venue,
        "instrument": run.dataset.instrument,
        "price_component": run.dataset.price_component.value,
        "status": run.status.value,
        "complete_d1_bars": identity.d1_rows,
        "candidate_count": len(run.candidates),
        "no_signal_count": run.no_signal_count,
        "trade_plan_count": run.trade_plan_count,
        "reason_code_counts": dict(sorted(reason_counts.items())),
        "run_sha256": run.run_sha256,
        "candidate_details_persisted": False,
        "trade_plan_details_persisted": False,
        "backtester_invoked": False,
        "pnl_outcome_accessed": False,
        "paper_trading_authorized": False,
        "shadow_trading_authorized": False,
        "live_trading_authorized": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("phase6b_detector_activity=COMPLETE")
    print(f"instrument={run.dataset.instrument}")
    print(f"complete_d1_bars={identity.d1_rows}")
    print(f"candidate_count={len(run.candidates)}")
    print(f"no_signal_count={run.no_signal_count}")
    print(f"trade_plan_count={run.trade_plan_count}")
    print("reason_code_counts=" + json.dumps(dict(sorted(reason_counts.items())), sort_keys=True))
    print(f"run_sha256={run.run_sha256}")
    print("backtester_invoked=false")
    print("pnl_outcome_accessed=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
