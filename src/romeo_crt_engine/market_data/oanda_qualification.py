from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from typing import Final

from romeo_crt_engine.market_data.models import BarTimeframe
from romeo_crt_engine.market_data.price_data_v2 import (
    ActivityMeasure,
    ActivitySemantic,
    CanonicalPriceBarV2,
    PriceComponent,
)
from romeo_crt_engine.market_data.providers.oanda_account import (
    OandaAccountQualificationRecord,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    PROVIDER,
    VENUE,
    OandaInstrumentRecord,
    OandaPriceCandle,
)

QUALIFICATION_SCHEMA: Final = "P6B_OANDA_INSTRUMENT_DISCOVERY_V2"
ACCOUNT_SCOPE: Final = "REDACTED_RUNTIME_ACCOUNT"

# These are candidate API aliases, not assertions that every OANDA division/account
# exposes them. The actual account instrument response is always the source of truth.
SOURCE_FAMILY_ALIASES: Final[dict[str, tuple[str, ...]]] = {
    "US_NAS_100_NQ_PROXY": ("NAS100_USD",),
    "US_SPX_500_ES_PROXY": ("SPX500_USD",),
    "EUR_USD": ("EUR_USD",),
    "GOLD_USD": ("XAU_USD",),
}


@dataclass(frozen=True, slots=True)
class OandaFamilyMatch:
    family: str
    candidate_aliases: tuple[str, ...]
    matched_instrument: OandaInstrumentRecord | None

    @property
    def status(self) -> str:
        return "MATCHED" if self.matched_instrument is not None else "UNAVAILABLE_OR_UNMAPPED"


def select_source_relevant_instruments(
    instruments: tuple[OandaInstrumentRecord, ...],
) -> tuple[OandaFamilyMatch, ...]:
    """Intersect the precommitted source families with the actual account universe."""

    by_name = {instrument.name: instrument for instrument in instruments}
    matches: list[OandaFamilyMatch] = []
    for family in sorted(SOURCE_FAMILY_ALIASES):
        aliases = SOURCE_FAMILY_ALIASES[family]
        matched = next((by_name[alias] for alias in aliases if alias in by_name), None)
        matches.append(
            OandaFamilyMatch(
                family=family,
                candidate_aliases=aliases,
                matched_instrument=matched,
            )
        )
    return tuple(matches)


def _instrument_record(instrument: OandaInstrumentRecord) -> dict[str, object]:
    commission: dict[str, object] | None = None
    if instrument.commission is not None:
        commission = {
            "commission_account_home": format(instrument.commission.commission, "f"),
            "units_traded": format(instrument.commission.units_traded, "f"),
            "minimum_commission_account_home": format(
                instrument.commission.minimum_commission, "f"
            ),
        }

    financing: dict[str, object] | None = None
    if instrument.financing is not None:
        financing = {
            "long_rate": format(instrument.financing.long_rate, "f"),
            "short_rate": format(instrument.financing.short_rate, "f"),
            "financing_days": [
                {
                    "day_of_week": day.day_of_week,
                    "days_charged": day.days_charged,
                }
                for day in instrument.financing.financing_days
            ],
        }

    return {
        "name": instrument.name,
        "display_name": instrument.display_name,
        "instrument_type": instrument.instrument_type,
        "display_precision": instrument.display_precision,
        "pip_location": instrument.pip_location,
        "trade_units_precision": instrument.trade_units_precision,
        "provider_unit_precision_step": format(
            instrument.provider_unit_precision_step, "f"
        ),
        "minimum_trade_size": format(instrument.minimum_trade_size, "f"),
        "maximum_order_units": (
            format(instrument.maximum_order_units, "f")
            if instrument.maximum_order_units is not None
            else None
        ),
        "maximum_position_size": (
            format(instrument.maximum_position_size, "f")
            if instrument.maximum_position_size is not None
            else None
        ),
        "margin_rate": (
            format(instrument.margin_rate, "f") if instrument.margin_rate is not None else None
        ),
        "commission": commission,
        "financing": financing,
        "guaranteed_stop_loss_order_mode": instrument.guaranteed_stop_loss_order_mode,
        "metadata_observed_at_utc": instrument.observed_at.astimezone(UTC).isoformat(),
        "raw_instrument_response_sha256": instrument.raw_sha256,
    }


def _account_record(account: OandaAccountQualificationRecord) -> dict[str, object]:
    return {
        "home_currency": account.home_currency,
        "margin_rate": format(account.margin_rate, "f"),
        "hedging_enabled": account.hedging_enabled,
        "guaranteed_stop_loss_order_mode": account.guaranteed_stop_loss_order_mode,
        "metadata_observed_at_utc": account.observed_at.astimezone(UTC).isoformat(),
        "raw_account_summary_sha256": account.raw_sha256,
    }


def build_instrument_discovery_manifest(
    instruments: tuple[OandaInstrumentRecord, ...],
    *,
    environment: str,
    observed_at: datetime,
    account: OandaAccountQualificationRecord | None = None,
) -> dict[str, object]:
    """Build a deterministic, credential-free Phase-6B discovery record.

    The manifest deliberately omits the OANDA account ID and access token. It is
    a discovery artifact only; it does not freeze an instrument universe or
    authorize strategy outcome access.
    """

    if environment not in {"practice", "live"}:
        raise ValueError("environment must be practice or live")
    if observed_at.utcoffset() is None:
        raise ValueError("observed_at must be timezone-aware")
    if not instruments:
        raise ValueError("instrument discovery returned no instruments")

    raw_hashes = {instrument.raw_sha256 for instrument in instruments}
    if len(raw_hashes) != 1:
        raise ValueError("instrument records must come from one sealed provider response")

    matches = select_source_relevant_instruments(instruments)
    match_records: list[dict[str, object]] = []
    for match in matches:
        record: dict[str, object] = {
            "family": match.family,
            "candidate_aliases": list(match.candidate_aliases),
            "status": match.status,
            "instrument": None,
        }
        if match.matched_instrument is not None:
            record["instrument"] = _instrument_record(match.matched_instrument)
        match_records.append(record)

    available_names = sorted(instrument.name for instrument in instruments)
    universe_digest_seed = "\n".join(available_names).encode()

    return {
        "schema_version": QUALIFICATION_SCHEMA,
        "provider": PROVIDER,
        "venue": VENUE,
        "environment": environment,
        "account_scope": ACCOUNT_SCOPE,
        "account_profile": _account_record(account) if account is not None else None,
        "observed_at_utc": observed_at.astimezone(UTC).isoformat(),
        "raw_instrument_response_sha256": next(iter(raw_hashes)),
        "available_instrument_count": len(instruments),
        "available_instrument_names_sha256": sha256(universe_digest_seed).hexdigest(),
        "source_family_matches": match_records,
        "status": "DISCOVERED_NOT_FROZEN",
        "strategy_outcome_access_authorized": False,
        "paper_trading_authorized": False,
        "live_trading_authorized": False,
    }


def _price_component(value: str) -> PriceComponent:
    mapping = {
        "M": PriceComponent.MID,
        "B": PriceComponent.BID,
        "A": PriceComponent.ASK,
    }
    try:
        return mapping[value]
    except KeyError as error:
        raise ValueError(f"unsupported OANDA price component: {value}") from error


def canonicalize_oanda_m1(
    candles: tuple[OandaPriceCandle, ...],
    *,
    session_policy_version: str,
) -> tuple[CanonicalPriceBarV2, ...]:
    """Map provider M1 candles into v2 price data without fabricating activity semantics."""

    if not candles:
        raise ValueError("OANDA M1 canonicalization requires at least one candle")
    if not session_policy_version:
        raise ValueError("session_policy_version must not be empty")

    identity = (candles[0].instrument, candles[0].price_component)
    output: list[CanonicalPriceBarV2] = []
    for candle in candles:
        if (candle.instrument, candle.price_component) != identity:
            raise ValueError("OANDA M1 canonicalization requires one instrument/price component")
        source_digest = sha256(
            f"{candle.source_sha256}|{candle.open_time.isoformat()}".encode()
        ).hexdigest()
        output.append(
            CanonicalPriceBarV2(
                provider=PROVIDER,
                venue=VENUE,
                instrument=candle.instrument,
                price_component=_price_component(candle.price_component),
                timeframe=BarTimeframe.M1,
                open_time=candle.open_time,
                close_time=candle.close_time,
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                source_count=1,
                source_digest=source_digest,
                session_policy_version=session_policy_version,
                activity=(
                    ActivityMeasure(
                        semantic=ActivitySemantic.PRICE_COUNT,
                        value=Decimal(candle.price_count),
                    ),
                ),
            )
        )
    return tuple(output)
