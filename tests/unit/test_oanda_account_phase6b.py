from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.oanda_qualification import (
    build_instrument_discovery_manifest,
)
from romeo_crt_engine.market_data.providers.oanda_account import (
    parse_account_summary,
    parse_authorized_account_ids,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import OandaInstrumentRecord
from romeo_crt_engine.market_data.quality import DataQualityError

OBSERVED_AT = datetime(2026, 8, 13, 11, 15, tzinfo=UTC)


def _payload(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":")).encode()


def test_authorized_account_preflight_parses_ids_for_in_memory_comparison() -> None:
    account_ids = parse_authorized_account_ids(
        _payload(
            {
                "accounts": [
                    {"id": "001-001-EXAMPLE-ONE", "tags": []},
                    {"id": "001-001-EXAMPLE-TWO", "tags": []},
                ]
            }
        )
    )

    assert account_ids == ("001-001-EXAMPLE-ONE", "001-001-EXAMPLE-TWO")


def test_authorized_account_preflight_rejects_duplicate_ids() -> None:
    payload = _payload(
        {
            "accounts": [
                {"id": "001-001-EXAMPLE", "tags": []},
                {"id": "001-001-EXAMPLE", "tags": []},
            ]
        }
    )

    with pytest.raises(DataQualityError, match="duplicate OANDA authorized-account ID"):
        parse_authorized_account_ids(payload)


def test_account_summary_parsing_omits_account_identity() -> None:
    payload = _payload(
        {
            "account": {
                "id": "001-001-SECRET-ACCOUNT",
                "currency": "ZAR",
                "marginRate": "0.05",
                "hedgingEnabled": True,
                "guaranteedStopLossOrderMode": "ALLOWED",
                "balance": "100000.00",
                "NAV": "100000.00",
            },
            "lastTransactionID": "123",
        }
    )

    record = parse_account_summary(payload, observed_at=OBSERVED_AT)

    assert record.home_currency == "ZAR"
    assert record.margin_rate == Decimal("0.05")
    assert record.hedging_enabled is True
    assert record.guaranteed_stop_loss_order_mode == "ALLOWED"
    assert len(record.raw_sha256) == 64
    assert not hasattr(record, "account_id")
    assert not hasattr(record, "balance")
    assert not hasattr(record, "nav")


def test_discovery_manifest_can_include_redacted_account_execution_profile() -> None:
    account = parse_account_summary(
        _payload(
            {
                "account": {
                    "id": "001-001-SECRET-ACCOUNT",
                    "currency": "USD",
                    "marginRate": "0.02",
                    "hedgingEnabled": False,
                }
            }
        ),
        observed_at=OBSERVED_AT,
    )
    instruments = (
        OandaInstrumentRecord(
            name="EUR_USD",
            display_name="EUR/USD",
            instrument_type="CURRENCY",
            display_precision=5,
            pip_location=-4,
            trade_units_precision=0,
            minimum_trade_size=Decimal(1),
            observed_at=OBSERVED_AT,
            raw_sha256="a" * 64,
        ),
    )

    manifest = build_instrument_discovery_manifest(
        instruments,
        environment="practice",
        observed_at=OBSERVED_AT,
        account=account,
    )

    assert manifest["account_scope"] == "REDACTED_RUNTIME_ACCOUNT"
    assert manifest["account_profile"] == {
        "home_currency": "USD",
        "margin_rate": "0.02",
        "hedging_enabled": False,
        "guaranteed_stop_loss_order_mode": None,
        "metadata_observed_at_utc": OBSERVED_AT.isoformat(),
        "raw_account_summary_sha256": account.raw_sha256,
    }
    serialized = json.dumps(manifest, sort_keys=True)
    assert "001-001-SECRET-ACCOUNT" not in serialized
    assert "balance" not in serialized.lower()
    assert manifest["strategy_outcome_access_authorized"] is False
