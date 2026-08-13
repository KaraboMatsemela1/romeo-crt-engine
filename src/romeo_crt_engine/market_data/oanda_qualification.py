from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from typing import Final

from romeo_crt_engine.market_data.providers.oanda_v20 import OandaInstrumentRecord

QUALIFICATION_SCHEMA: Final = "P6B_OANDA_INSTRUMENT_DISCOVERY_V1"
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
    return {
        "name": instrument.name,
        "display_name": instrument.display_name,
        "instrument_type": instrument.instrument_type,
        "display_precision": instrument.display_precision,
        "pip_location": instrument.pip_location,
        "trade_units_precision": instrument.trade_units_precision,
        "minimum_trade_size": format(instrument.minimum_trade_size, "f"),
        "metadata_observed_at_utc": instrument.observed_at.astimezone(UTC).isoformat(),
        "raw_instrument_response_sha256": instrument.raw_sha256,
    }


def build_instrument_discovery_manifest(
    instruments: tuple[OandaInstrumentRecord, ...],
    *,
    environment: str,
    observed_at: datetime,
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
        "provider": "OANDA_V20",
        "venue": "OANDA_FXTRADE",
        "environment": environment,
        "account_scope": ACCOUNT_SCOPE,
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
