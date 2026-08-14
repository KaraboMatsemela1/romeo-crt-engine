from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from romeo_crt_engine.market_data.oanda_qualification import (
    ACCOUNT_SCOPE,
    build_instrument_discovery_manifest,
    select_source_relevant_instruments,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import OandaInstrumentRecord

RAW_SHA = "a" * 64
OBSERVED_AT = datetime(2026, 8, 13, 10, 30, tzinfo=UTC)


def _instrument(name: str, *, instrument_type: str = "CFD") -> OandaInstrumentRecord:
    return OandaInstrumentRecord(
        name=name,
        display_name=name,
        instrument_type=instrument_type,
        display_precision=5,
        pip_location=-4,
        trade_units_precision=0,
        minimum_trade_size=Decimal(1),
        observed_at=OBSERVED_AT,
        raw_sha256=RAW_SHA,
    )


def test_source_family_selection_is_ex_ante_and_account_intersected() -> None:
    instruments = (
        _instrument("EUR_USD", instrument_type="CURRENCY"),
        _instrument("NAS100_USD"),
        _instrument("GBP_USD", instrument_type="CURRENCY"),
    )

    matches = select_source_relevant_instruments(instruments)
    by_family = {match.family: match for match in matches}

    assert by_family["EUR_USD"].status == "MATCHED"
    assert by_family["EUR_USD"].matched_instrument is not None
    assert by_family["EUR_USD"].matched_instrument.name == "EUR_USD"
    assert by_family["US_NAS_100_NQ_PROXY"].status == "MATCHED"
    assert by_family["US_SPX_500_ES_PROXY"].status == "UNAVAILABLE_OR_UNMAPPED"
    assert by_family["GOLD_USD"].status == "UNAVAILABLE_OR_UNMAPPED"


def test_discovery_manifest_contains_no_account_or_token_field() -> None:
    instruments = (
        _instrument("EUR_USD", instrument_type="CURRENCY"),
        _instrument("XAU_USD"),
    )

    manifest = build_instrument_discovery_manifest(
        instruments,
        environment="practice",
        observed_at=OBSERVED_AT,
    )

    assert manifest["account_scope"] == ACCOUNT_SCOPE
    assert "account_id" not in manifest
    assert "token" not in manifest
    assert manifest["raw_instrument_response_sha256"] == RAW_SHA
    assert manifest["status"] == "DISCOVERED_NOT_FROZEN"
    assert manifest["strategy_outcome_access_authorized"] is False
    assert manifest["live_trading_authorized"] is False


def test_discovery_manifest_universe_digest_is_order_independent() -> None:
    first = build_instrument_discovery_manifest(
        (_instrument("EUR_USD"), _instrument("XAU_USD")),
        environment="practice",
        observed_at=OBSERVED_AT,
    )
    second = build_instrument_discovery_manifest(
        (_instrument("XAU_USD"), _instrument("EUR_USD")),
        environment="practice",
        observed_at=OBSERVED_AT,
    )

    assert first["available_instrument_names_sha256"] == second[
        "available_instrument_names_sha256"
    ]
