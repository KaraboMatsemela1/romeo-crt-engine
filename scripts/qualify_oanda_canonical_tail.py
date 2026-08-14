from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import collect_oanda_history_shard as collector

from romeo_crt_engine.market_data.canonical_coverage_v2 import (
    CANONICAL_COVERAGE_POLICY_VERSION,
    CANONICAL_TAIL_END_UTC,
    CANONICAL_TAIL_START_UTC,
)
from romeo_crt_engine.market_data.history_qualification_v2 import (
    candle_value_record,
    enumerate_missing_intervals,
    gap_digest,
    missing_interval_record,
    normalized_m1_sha256,
)
from romeo_crt_engine.market_data.providers.oanda_history import (
    OandaHistoryRequestWindow,
    fetch_m1_history_page,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import PRACTICE_BASE_URL

FROZEN_INSTRUMENTS = ("EUR_USD", "XAU_USD", "NAS100_USD", "SPX500_USD")
TAIL_EVIDENCE_SCHEMA_VERSION = "P6B_OANDA_CANONICAL_TAIL_EVIDENCE_V1"
OBSERVATION_POLICY_VERSION = "P6B_OANDA_OBSERVATION_POLICY_V2"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Qualify the exact five-hour UTC tail required to complete the frozen "
            "Phase-6B New-York DEV window. This is read-only provider-data work."
        )
    )
    parser.add_argument("--instrument", required=True, choices=FROZEN_INSTRUMENTS)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def _safe(document: dict[str, object]) -> None:
    serialized = json.dumps(document, sort_keys=True).lower()
    for marker in (
        "authorization",
        "bearer ",
        "oanda_api_token",
        "oanda_account_id",
        '"balance"',
        '"nav"',
    ):
        if marker in serialized:
            raise ValueError(f"forbidden persisted marker found: {marker}")

    for flag in (
        "trusted_dataset_authorized",
        "detector_execution_authorized",
        "tradeplan_count_access_authorized",
        "backtester_authorized",
        "pnl_outcome_access_authorized",
        "paper_trading_authorized",
        "shadow_trading_authorized",
        "live_trading_authorized",
    ):
        if document.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")


def main() -> int:
    args = _parser().parse_args()
    account_id = os.environ.get("OANDA_ACCOUNT_ID", "")
    token = os.environ.get("OANDA_API_TOKEN", "")
    if not account_id or not token:
        raise RuntimeError("OANDA practice credentials are required at runtime")

    window = OandaHistoryRequestWindow(
        start=CANONICAL_TAIL_START_UTC,
        end=CANONICAL_TAIL_END_UTC,
    )
    primary = fetch_m1_history_page(
        base_url=PRACTICE_BASE_URL,
        account_id=account_id,
        token=token,
        instrument=args.instrument,
        window=window,
        price_component="M",
        timeout_seconds=45.0,
    )
    refetch = fetch_m1_history_page(
        base_url=PRACTICE_BASE_URL,
        account_id=account_id,
        token=token,
        instrument=args.instrument,
        window=window,
        price_component="M",
        timeout_seconds=45.0,
    )

    primary_values = tuple(candle_value_record(candle) for candle in primary.candles)
    refetch_values = tuple(candle_value_record(candle) for candle in refetch.candles)
    if primary_values != refetch_values:
        raise ValueError("independent canonical-tail provider refetch does not match")
    refetch_status = (
        "EXACT_PROVIDER_VALUE_MATCH" if primary_values else "EXACT_PROVIDER_EMPTY_MATCH"
    )

    missing = enumerate_missing_intervals(
        primary.candles,
        requested_start=CANONICAL_TAIL_START_UTC,
        requested_end=CANONICAL_TAIL_END_UTC,
    )

    s5_result: dict[str, object] | None = None
    s5_timestamps: tuple[str, ...] = ()
    if missing:
        raw_s5 = collector._fetch_s5_bucket(
            account_id=account_id,
            token=token,
            instrument=args.instrument,
            start=CANONICAL_TAIL_START_UTC,
            end=CANONICAL_TAIL_END_UTC,
        )
        raw_timestamps = raw_s5.get("timestamps")
        if not isinstance(raw_timestamps, list) or not all(
            isinstance(value, str) for value in raw_timestamps
        ):
            raise TypeError("canonical-tail S5 timestamps must be a string list")
        s5_timestamps = tuple(raw_timestamps)
        s5_result = {
            "start_utc": raw_s5["start_utc"],
            "end_utc": raw_s5["end_utc"],
            "request_sha256": raw_s5["request_sha256"],
            "raw_response_sha256": raw_s5["raw_response_sha256"],
            "complete_s5_count": raw_s5["complete_s5_count"],
        }

    classifications: list[dict[str, object]] = []
    no_price_gaps = 0
    no_price_minutes = 0
    unresolved_gaps = 0
    unresolved_minutes = 0
    for index, gap in enumerate(missing):
        count_inside = sum(
            1
            for raw_timestamp in s5_timestamps
            if gap.start <= collector._parse_utc(raw_timestamp) < gap.end
        )
        classification = (
            "NO_PRICE_OBSERVATION" if count_inside == 0 else "UNRESOLVED_PROVIDER_GAP"
        )
        if classification == "NO_PRICE_OBSERVATION":
            no_price_gaps += 1
            no_price_minutes += gap.missing_minutes
        else:
            unresolved_gaps += 1
            unresolved_minutes += gap.missing_minutes
        record = missing_interval_record(gap)
        record.update(
            {
                "gap_index": index,
                "classification": classification,
                "s5_complete_observations_inside_gap": count_inside,
            }
        )
        classifications.append(record)

    total_missing_minutes = sum(gap.missing_minutes for gap in missing)
    if no_price_gaps + unresolved_gaps != len(missing):
        raise ValueError("tail gap classifications do not balance")
    if no_price_minutes + unresolved_minutes != total_missing_minutes:
        raise ValueError("tail missing-minute classifications do not balance")

    evidence: dict[str, object] = {
        "schema_version": TAIL_EVIDENCE_SCHEMA_VERSION,
        "canonical_coverage_policy_version": CANONICAL_COVERAGE_POLICY_VERSION,
        "observation_policy_version": OBSERVATION_POLICY_VERSION,
        "provider": "OANDA_V20",
        "venue": "OANDA_FXTRADE",
        "environment": "practice",
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "instrument": args.instrument,
        "price_component": "MID",
        "granularity": "M1",
        "requested_start_utc": CANONICAL_TAIL_START_UTC.isoformat(),
        "requested_end_utc": CANONICAL_TAIL_END_UTC.isoformat(),
        "primary": {
            "request_sha256": primary.request_sha256,
            "raw_response_sha256": primary.raw_response_sha256,
            "complete_candle_count": len(primary.candles),
            "normalized_provider_values_sha256": normalized_m1_sha256(primary.candles),
        },
        "refetch": {
            "request_sha256": refetch.request_sha256,
            "raw_response_sha256": refetch.raw_response_sha256,
            "complete_candle_count": len(refetch.candles),
            "status": refetch_status,
        },
        "missing_interval_count": len(missing),
        "missing_minutes": total_missing_minutes,
        "missing_intervals_sha256": gap_digest(missing),
        "classifications": classifications,
        "s5_evidence": s5_result,
        "no_price_observation_gap_count": no_price_gaps,
        "no_price_observation_minutes": no_price_minutes,
        "unresolved_provider_gap_count": unresolved_gaps,
        "unresolved_provider_gap_minutes": unresolved_minutes,
        "trusted_dataset_authorized": False,
        "detector_execution_authorized": False,
        "tradeplan_count_access_authorized": False,
        "backtester_authorized": False,
        "pnl_outcome_access_authorized": False,
        "paper_trading_authorized": False,
        "shadow_trading_authorized": False,
        "live_trading_authorized": False,
    }
    _safe(evidence)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")

    print(f"canonical_tail={args.instrument}")
    print(f"m1_complete={len(primary.candles)}")
    print(f"missing_gaps={len(missing)}")
    print(f"missing_minutes={total_missing_minutes}")
    print(f"no_price_gaps={no_price_gaps}")
    print(f"unresolved_gaps={unresolved_gaps}")
    print(f"refetch={refetch_status}")
    print("detector_execution_authorized=false")
    print("pnl_outcome_access_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
