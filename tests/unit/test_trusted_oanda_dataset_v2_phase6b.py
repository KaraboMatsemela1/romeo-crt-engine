from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.canonical_coverage_v2 import (
    CANONICAL_TAIL_END_UTC,
    CANONICAL_TAIL_START_UTC,
)
from romeo_crt_engine.market_data.history_qualification_v2 import (
    enumerate_missing_intervals,
    gap_digest,
    missing_interval_record,
    normalized_m1_sha256,
)
from romeo_crt_engine.market_data.price_data_v2 import PriceQuantumSource
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    OandaInstrumentRecord,
    OandaPriceCandle,
)
from romeo_crt_engine.market_data.trusted_oanda_dataset_v2 import (
    market_gaps_from_canonical_tail_evidence,
    oanda_instrument_metadata_sha256,
    oanda_price_quantum,
    validate_yearly_reconstruction,
)

SOURCE_SHA = "a" * 64
REQUEST_SHA = "b" * 64
RESPONSE_SHA = "c" * 64


def _instrument() -> OandaInstrumentRecord:
    return OandaInstrumentRecord(
        name="EUR_USD",
        display_name="EUR/USD",
        instrument_type="CURRENCY",
        display_precision=5,
        pip_location=-4,
        trade_units_precision=0,
        minimum_trade_size=Decimal(1),
        observed_at=datetime(2026, 8, 14, 10, 0, tzinfo=UTC),
        raw_sha256="d" * 64,
    )


def _candle(open_time: datetime, value: str) -> OandaPriceCandle:
    price = Decimal(value)
    return OandaPriceCandle(
        instrument="EUR_USD",
        price_component="M",
        open_time=open_time,
        close_time=open_time + timedelta(minutes=1),
        open=price,
        high=price + Decimal("0.00002"),
        low=price - Decimal("0.00002"),
        close=price + Decimal("0.00001"),
        price_count=3,
        complete=True,
        source_sha256=SOURCE_SHA,
    )


def test_provider_display_precision_binds_representation_quantum_not_tick_claim() -> None:
    instrument = _instrument()
    quantum, source = oanda_price_quantum(instrument)

    assert quantum == Decimal("0.00001")
    assert source is PriceQuantumSource.PROVIDER_PRICE_PRECISION_POLICY
    assert len(oanda_instrument_metadata_sha256(instrument)) == 64


def test_fresh_yearly_reconstruction_must_match_sealed_values_and_gap_inventory() -> None:
    start = datetime(2019, 1, 1, 0, 0, tzinfo=UTC)
    end = start + timedelta(minutes=3)
    candles = (
        _candle(start, "1.10000"),
        _candle(start + timedelta(minutes=2), "1.10002"),
    )
    missing = enumerate_missing_intervals(candles, requested_start=start, requested_end=end)
    assert len(missing) == 1

    reconciliation = {
        "schema_version": "P6B_OANDA_RECONCILIATION_EVIDENCE_V2",
        "observation_policy_version": "P6B_OANDA_OBSERVATION_POLICY_V2",
        "provider": "OANDA_V20",
        "environment": "practice",
        "instrument": "EUR_USD",
        "year": 2019,
        "price_component": "MID",
        "granularity": "M1",
        "requested_start_utc": start.isoformat(),
        "requested_end_utc": end.isoformat(),
        "complete_candle_count": len(candles),
        "normalized_provider_values_sha256": normalized_m1_sha256(candles),
        "missing_interval_count": len(missing),
        "missing_minutes": 1,
        "missing_intervals_sha256": gap_digest(missing),
        "missing_intervals": [missing_interval_record(item) for item in missing],
        "refetch": {"status": "EXACT_PROVIDER_VALUE_MATCH"},
    }
    s5 = {
        "schema_version": "P6B_OANDA_S5_GAP_EVIDENCE_V1",
        "observation_policy_version": "P6B_OANDA_OBSERVATION_POLICY_V2",
        "provider": "OANDA_V20",
        "environment": "practice",
        "instrument": "EUR_USD",
        "year": 2019,
        "source_missing_intervals_sha256": reconciliation["missing_intervals_sha256"],
        "eligible_gap_count": 1,
        "no_price_observation_gap_count": 1,
        "no_price_observation_minutes": 1,
        "unresolved_provider_gap_count": 0,
        "unresolved_provider_gap_minutes": 0,
        "classifications": [
            {
                "gap_index": 0,
                "start_utc": missing[0].start.isoformat(),
                "end_utc": missing[0].end.isoformat(),
                "missing_minutes": 1,
                "classification": "NO_PRICE_OBSERVATION",
                "s5_complete_observations_inside_gap": 0,
                "evidence": [
                    {
                        "request_sha256": REQUEST_SHA,
                        "raw_response_sha256": RESPONSE_SHA,
                        "complete_s5_count_in_gap": 0,
                    }
                ],
            }
        ],
    }

    gaps = validate_yearly_reconstruction(candles, reconciliation, s5)
    assert len(gaps) == 1
    assert gaps[0].start_time == start + timedelta(minutes=1)

    changed = (_candle(start, "1.20000"), candles[1])
    with pytest.raises(ValueError, match="provider values differ"):
        validate_yearly_reconstruction(changed, reconciliation, s5)


def _tail_evidence() -> dict[str, object]:
    classification = {
        "gap_index": 0,
        "start_utc": CANONICAL_TAIL_START_UTC.isoformat(),
        "end_utc": CANONICAL_TAIL_END_UTC.isoformat(),
        "missing_minutes": 300,
        "classification": "NO_PRICE_OBSERVATION",
        "s5_complete_observations_inside_gap": 0,
    }
    return {
        "schema_version": "P6B_OANDA_CANONICAL_TAIL_EVIDENCE_V1",
        "canonical_coverage_policy_version": "P6B_CANONICAL_COVERAGE_V1",
        "observation_policy_version": "P6B_OANDA_OBSERVATION_POLICY_V2",
        "provider": "OANDA_V20",
        "venue": "OANDA_FXTRADE",
        "environment": "practice",
        "instrument": "EUR_USD",
        "price_component": "MID",
        "granularity": "M1",
        "requested_start_utc": CANONICAL_TAIL_START_UTC.isoformat(),
        "requested_end_utc": CANONICAL_TAIL_END_UTC.isoformat(),
        "primary": {
            "request_sha256": REQUEST_SHA,
            "raw_response_sha256": RESPONSE_SHA,
            "complete_candle_count": 0,
        },
        "refetch": {
            "request_sha256": "e" * 64,
            "raw_response_sha256": "f" * 64,
            "complete_candle_count": 0,
            "status": "EXACT_PROVIDER_EMPTY_MATCH",
        },
        "missing_interval_count": 1,
        "missing_minutes": 300,
        "classifications": [classification],
        "s5_evidence": {
            "request_sha256": "1" * 64,
            "raw_response_sha256": "2" * 64,
            "complete_s5_count": 0,
        },
        "no_price_observation_gap_count": 1,
        "no_price_observation_minutes": 300,
        "unresolved_provider_gap_count": 0,
        "unresolved_provider_gap_minutes": 0,
    }


def test_canonical_tail_only_becomes_gap_policy_after_exact_empty_refetch_and_s5() -> None:
    gaps = market_gaps_from_canonical_tail_evidence(_tail_evidence())
    assert len(gaps) == 1
    assert gaps[0].start_time == CANONICAL_TAIL_START_UTC
    assert gaps[0].end_time == CANONICAL_TAIL_END_UTC

    invalid = _tail_evidence()
    invalid["unresolved_provider_gap_count"] = 1
    with pytest.raises(ValueError, match="unresolved gap"):
        market_gaps_from_canonical_tail_evidence(invalid)
