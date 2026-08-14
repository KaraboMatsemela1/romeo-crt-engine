from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal

from romeo_crt_engine.market_data.oanda_qualification import (
    QUALIFICATION_SCHEMA,
    build_instrument_discovery_manifest,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import parse_account_instruments


def _payload(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":")).encode()


def test_account_discovery_captures_execution_metadata_without_deriving_price_tick() -> None:
    observed_at = datetime(2026, 8, 13, 11, 0, tzinfo=UTC)
    payload = _payload(
        {
            "instruments": [
                {
                    "name": "EUR_USD",
                    "displayName": "EUR/USD",
                    "type": "CURRENCY",
                    "displayPrecision": 5,
                    "pipLocation": -4,
                    "tradeUnitsPrecision": 2,
                    "minimumTradeSize": "0.01",
                    "maximumOrderUnits": "100000000",
                    "maximumPositionSize": "50000000",
                    "marginRate": "0.02",
                    "guaranteedStopLossOrderMode": "DISABLED",
                    "commission": {
                        "commission": "5.00",
                        "unitsTraded": "1000000",
                        "minimumCommission": "0.50",
                    },
                    "financing": {
                        "longRate": "-0.0123",
                        "shortRate": "0.0045",
                        "financingDaysOfWeek": [
                            {"dayOfWeek": "MONDAY", "daysCharged": 1},
                            {"dayOfWeek": "WEDNESDAY", "daysCharged": 3},
                        ],
                    },
                }
            ]
        }
    )

    instrument = parse_account_instruments(payload, observed_at=observed_at)[0]

    assert instrument.maximum_order_units == Decimal(100000000)
    assert instrument.maximum_position_size == Decimal(50000000)
    assert instrument.margin_rate == Decimal("0.02")
    assert instrument.provider_unit_precision_step == Decimal("0.01")
    assert instrument.commission is not None
    assert instrument.commission.commission == Decimal("5.00")
    assert instrument.commission.units_traded == Decimal(1000000)
    assert instrument.commission.minimum_commission == Decimal("0.50")
    assert instrument.financing is not None
    assert instrument.financing.long_rate == Decimal("-0.0123")
    assert instrument.financing.short_rate == Decimal("0.0045")
    assert [(day.day_of_week, day.days_charged) for day in instrument.financing.financing_days] == [
        ("MONDAY", 1),
        ("WEDNESDAY", 3),
    ]
    assert instrument.guaranteed_stop_loss_order_mode == "DISABLED"
    assert not hasattr(instrument, "price_tick_size")


def test_discovery_manifest_v2_seals_execution_metadata_without_credentials() -> None:
    observed_at = datetime(2026, 8, 13, 11, 0, tzinfo=UTC)
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
                    "maximumOrderUnits": "100000000",
                    "maximumPositionSize": "0",
                    "marginRate": "0.02",
                    "commission": {
                        "commission": "0",
                        "unitsTraded": "1000000",
                        "minimumCommission": "0",
                    },
                    "financing": {
                        "longRate": "-0.01",
                        "shortRate": "0.002",
                        "financingDaysOfWeek": [],
                    },
                }
            ]
        }
    )
    instruments = parse_account_instruments(payload, observed_at=observed_at)

    manifest = build_instrument_discovery_manifest(
        instruments,
        environment="practice",
        observed_at=observed_at,
    )

    assert manifest["schema_version"] == QUALIFICATION_SCHEMA
    assert QUALIFICATION_SCHEMA == "P6B_OANDA_INSTRUMENT_DISCOVERY_V2"
    matches = manifest["source_family_matches"]
    assert isinstance(matches, list)
    eur_match = next(item for item in matches if item["family"] == "EUR_USD")
    instrument = eur_match["instrument"]
    assert isinstance(instrument, dict)
    assert instrument["provider_unit_precision_step"] == "1"
    assert instrument["maximum_order_units"] == "100000000"
    assert instrument["margin_rate"] == "0.02"
    assert instrument["commission"] == {
        "commission_account_home": "0",
        "units_traded": "1000000",
        "minimum_commission_account_home": "0",
    }
    assert instrument["financing"] == {
        "long_rate": "-0.01",
        "short_rate": "0.002",
        "financing_days": [],
    }
    serialized = json.dumps(manifest, sort_keys=True).lower()
    assert "api_token" not in serialized
    assert "authorization" not in serialized
    assert manifest["strategy_outcome_access_authorized"] is False
