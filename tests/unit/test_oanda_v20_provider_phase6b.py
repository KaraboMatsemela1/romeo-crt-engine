from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.providers.oanda_v20 import (
    parse_account_instruments,
    parse_m1_candles,
    request_fingerprint,
)
from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError


def _payload(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":")).encode("utf-8")


def test_parse_account_instruments_preserves_provider_semantics_without_inventing_tick_size() -> None:
    observed_at = datetime(2026, 8, 13, 10, 0, tzinfo=UTC)
    payload = _payload(
        {
            "instruments": [
                {
                    "name": "EUR_USD",
                    "displayName": "EUR/USD",
                    "type": "CURRENCY",
                    "displayPrecision": 5,
                    "pipLocation": -4,
                    "tradeUnitsPrecision": 0,
                    "minimumTradeSize": "1",
                },
                {
                    "name": "NAS100_USD",
                    "displayName": "US Nas 100",
                    "type": "CFD",
                    "displayPrecision": 1,
                    "pipLocation": 0,
                    "tradeUnitsPrecision": 2,
                    "minimumTradeSize": "0.01",
                },
            ]
        }
    )

    instruments = parse_account_instruments(payload, observed_at=observed_at)

    assert [instrument.name for instrument in instruments] == ["EUR_USD", "NAS100_USD"]
    eurusd = instruments[0]
    assert eurusd.instrument_type == "CURRENCY"
    assert eurusd.display_precision == 5
    assert eurusd.pip_location == -4
    assert eurusd.minimum_trade_size == Decimal(1)
    assert eurusd.observed_at == observed_at
    assert len(eurusd.raw_sha256) == 64

    nasdaq = instruments[1]
    assert nasdaq.instrument_type == "CFD"
    assert nasdaq.trade_units_precision == 2
    assert nasdaq.minimum_trade_size == Decimal("0.01")


def test_parse_m1_candles_keeps_oanda_price_count_separate_from_trade_volume() -> None:
    payload = _payload(
        {
            "instrument": "EUR_USD",
            "granularity": "M1",
            "candles": [
                {
                    "complete": True,
                    "volume": 12,
                    "time": "2026-08-13T08:00:00.000000000Z",
                    "mid": {
                        "o": "1.10000",
                        "h": "1.10050",
                        "l": "1.09990",
                        "c": "1.10030",
                    },
                },
                {
                    "complete": True,
                    "volume": 7,
                    "time": "2026-08-13T08:01:00Z",
                    "mid": {
                        "o": "1.10030",
                        "h": "1.10040",
                        "l": "1.10010",
                        "c": "1.10020",
                    },
                },
            ],
        }
    )

    candles = parse_m1_candles(payload, instrument="EUR_USD", price_component="M")

    assert len(candles) == 2
    assert candles[0].open_time == datetime(2026, 8, 13, 8, 0, tzinfo=UTC)
    assert candles[0].close_time == datetime(2026, 8, 13, 8, 1, tzinfo=UTC)
    assert candles[0].open == Decimal("1.10000")
    assert candles[0].high == Decimal("1.10050")
    assert candles[0].low == Decimal("1.09990")
    assert candles[0].close == Decimal("1.10030")
    assert candles[0].price_count == 12
    assert candles[0].complete is True
    assert candles[0].source_sha256 == candles[1].source_sha256


def test_parse_m1_candles_does_not_fill_session_gap() -> None:
    payload = _payload(
        {
            "instrument": "NAS100_USD",
            "granularity": "M1",
            "candles": [
                {
                    "complete": True,
                    "volume": 4,
                    "time": "2026-08-13T08:00:00Z",
                    "mid": {"o": "20000", "h": "20001", "l": "19999", "c": "20000.5"},
                },
                {
                    "complete": True,
                    "volume": 3,
                    "time": "2026-08-13T08:05:00Z",
                    "mid": {"o": "20002", "h": "20004", "l": "20001", "c": "20003"},
                },
            ],
        }
    )

    candles = parse_m1_candles(payload, instrument="NAS100_USD")

    assert [candle.open_time.minute for candle in candles] == [0, 5]
    assert len(candles) == 2


def test_parse_m1_candles_skips_incomplete_tail_by_default() -> None:
    payload = _payload(
        {
            "instrument": "EUR_USD",
            "granularity": "M1",
            "candles": [
                {
                    "complete": True,
                    "volume": 2,
                    "time": "2026-08-13T08:00:00Z",
                    "mid": {"o": "1.1", "h": "1.2", "l": "1.0", "c": "1.1"},
                },
                {
                    "complete": False,
                    "volume": 1,
                    "time": "2026-08-13T08:01:00Z",
                    "mid": {"o": "1.1", "h": "1.2", "l": "1.0", "c": "1.15"},
                },
            ],
        }
    )

    candles = parse_m1_candles(payload, instrument="EUR_USD")
    assert len(candles) == 1
    assert candles[0].open_time.minute == 0


def test_parse_m1_candles_rejects_wrong_identity() -> None:
    payload = _payload({"instrument": "GBP_USD", "granularity": "M1", "candles": []})

    with pytest.raises(DataQualityError) as captured:
        parse_m1_candles(payload, instrument="EUR_USD")

    assert captured.value.code is DataQualityCode.IDENTITY_MISMATCH


def test_parse_m1_candles_rejects_out_of_order_provider_rows() -> None:
    payload = _payload(
        {
            "instrument": "EUR_USD",
            "granularity": "M1",
            "candles": [
                {
                    "complete": True,
                    "volume": 1,
                    "time": "2026-08-13T08:01:00Z",
                    "mid": {"o": "1", "h": "2", "l": "1", "c": "1.5"},
                },
                {
                    "complete": True,
                    "volume": 1,
                    "time": "2026-08-13T08:00:00Z",
                    "mid": {"o": "1", "h": "2", "l": "1", "c": "1.5"},
                },
            ],
        }
    )

    with pytest.raises(DataQualityError) as captured:
        parse_m1_candles(payload, instrument="EUR_USD")

    assert captured.value.code is DataQualityCode.OUT_OF_ORDER


def test_request_fingerprint_is_deterministic_and_parameter_order_independent() -> None:
    first = request_fingerprint(
        "/v3/accounts/123/instruments/EUR_USD/candles",
        {"granularity": "M1", "price": "M", "smooth": "false"},
    )
    second = request_fingerprint(
        "/v3/accounts/123/instruments/EUR_USD/candles",
        {"smooth": "false", "price": "M", "granularity": "M1"},
    )

    assert first == second
    assert len(first) == 64
