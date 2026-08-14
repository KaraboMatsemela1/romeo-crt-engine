from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from typing import Mapping

from romeo_crt_engine.market_data.canonical_coverage_v2 import (
    CANONICAL_COVERAGE_END_UTC,
    CANONICAL_COVERAGE_POLICY_VERSION,
    CANONICAL_TAIL_END_UTC,
    CANONICAL_TAIL_START_UTC,
)
from romeo_crt_engine.market_data.history_qualification_v2 import (
    enumerate_missing_intervals,
    gap_digest,
    normalized_m1_sha256,
)
from romeo_crt_engine.market_data.price_data_v2 import (
    PriceComponent,
    PriceDatasetIdentityV2,
    PriceQuantumSource,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    PROVIDER,
    VENUE,
    OandaInstrumentRecord,
    OandaPriceCandle,
)
from romeo_crt_engine.market_data.s5_gap_policy_v2 import (
    OBSERVATION_POLICY_VERSION,
    market_gaps_from_complete_s5_evidence,
)
from romeo_crt_engine.market_data.session_policy_v2 import GapCategory, MarketGapV2

TAIL_EVIDENCE_SCHEMA_VERSION = "P6B_OANDA_CANONICAL_TAIL_EVIDENCE_V1"
TRUSTED_BUILD_SCHEMA_VERSION = "P6B_OANDA_TRUSTED_DATASET_BUILD_V1"
TRUSTED_DATASET_VERSION_PREFIX = "P6B-OANDA-MID-NYDEV-v1"


def _parse_utc(value: object, *, field: str) -> datetime:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return parsed.astimezone(UTC)


def _sha256_text(value: object, *, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"{field} must be a SHA-256 digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"{field} must be hexadecimal") from exc
    return value.lower()


def _decimal_text(value: Decimal | None) -> str | None:
    return None if value is None else format(value, "f")


def oanda_price_quantum(
    instrument: OandaInstrumentRecord,
) -> tuple[Decimal, PriceQuantumSource]:
    """Bind price representation precision without claiming an exchange tick size.

    OANDA documents displayPrecision as the number of decimal places used to
    display prices for an instrument. Phase 6B uses that provider precision
    policy as the pre-frozen price quantum for detector-neutral price arithmetic.
    It is deliberately not labelled as a venue tick-size contract.
    """

    if instrument.display_precision < 0:
        raise ValueError("display_precision must be non-negative")
    quantum = Decimal(1).scaleb(-instrument.display_precision)
    return quantum, PriceQuantumSource.PROVIDER_PRICE_PRECISION_POLICY


def oanda_instrument_metadata_record(instrument: OandaInstrumentRecord) -> dict[str, object]:
    """Return the credential-free metadata fields that bind one dataset identity."""

    return {
        "provider": PROVIDER,
        "venue": VENUE,
        "instrument": instrument.name,
        "display_name": instrument.display_name,
        "instrument_type": instrument.instrument_type,
        "display_precision": instrument.display_precision,
        "pip_location": instrument.pip_location,
        "trade_units_precision": instrument.trade_units_precision,
        "provider_unit_precision_step": format(instrument.provider_unit_precision_step, "f"),
        "minimum_trade_size": format(instrument.minimum_trade_size, "f"),
        "maximum_order_units": _decimal_text(instrument.maximum_order_units),
        "maximum_position_size": _decimal_text(instrument.maximum_position_size),
        "margin_rate": _decimal_text(instrument.margin_rate),
        "guaranteed_stop_loss_order_mode": instrument.guaranteed_stop_loss_order_mode,
        "raw_instrument_response_sha256": _sha256_text(
            instrument.raw_sha256,
            field="raw_instrument_response_sha256",
        ),
    }


def oanda_instrument_metadata_sha256(instrument: OandaInstrumentRecord) -> str:
    record = oanda_instrument_metadata_record(instrument)
    return sha256(
        json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def validate_yearly_reconstruction(
    candles: tuple[OandaPriceCandle, ...],
    reconciliation: Mapping[str, object],
    s5_evidence: Mapping[str, object],
) -> tuple[MarketGapV2, ...]:
    """Bind a fresh provider reconstruction to one sealed all-gap evidence shard."""

    instrument = reconciliation.get("instrument")
    year = reconciliation.get("year")
    if not isinstance(instrument, str) or not instrument:
        raise ValueError("reconciliation instrument is required")
    if not isinstance(year, int):
        raise TypeError("reconciliation year must be an integer")
    if reconciliation.get("provider") != PROVIDER:
        raise ValueError("yearly reconstruction requires OANDA_V20 evidence")
    if reconciliation.get("environment") != "practice":
        raise ValueError("yearly reconstruction requires practice evidence")
    if reconciliation.get("price_component") != "MID" or reconciliation.get("granularity") != "M1":
        raise ValueError("yearly reconstruction requires MID/M1 evidence")

    if not candles:
        raise ValueError("yearly reconstruction requires provider M1 observations")
    if any(
        candle.instrument != instrument
        or candle.price_component != "M"
        or candle.complete is not True
        for candle in candles
    ):
        raise ValueError("fresh provider candles do not match sealed evidence identity")

    start = _parse_utc(reconciliation.get("requested_start_utc"), field="requested_start_utc")
    end = _parse_utc(reconciliation.get("requested_end_utc"), field="requested_end_utc")
    if end <= start:
        raise ValueError("sealed yearly interval is invalid")
    if any(candle.open_time < start or candle.close_time > end for candle in candles):
        raise ValueError("fresh provider candle lies outside sealed yearly interval")

    declared_count = reconciliation.get("complete_candle_count")
    if declared_count != len(candles):
        raise ValueError("fresh provider candle count differs from sealed evidence")
    current_values_sha = normalized_m1_sha256(candles)
    if current_values_sha != reconciliation.get("normalized_provider_values_sha256"):
        raise ValueError("fresh provider values differ from sealed normalized history")

    current_missing = enumerate_missing_intervals(
        candles,
        requested_start=start,
        requested_end=end,
    )
    if len(current_missing) != reconciliation.get("missing_interval_count"):
        raise ValueError("fresh missing-interval count differs from sealed evidence")
    if sum(item.missing_minutes for item in current_missing) != reconciliation.get("missing_minutes"):
        raise ValueError("fresh missing-minute count differs from sealed evidence")
    if gap_digest(current_missing) != reconciliation.get("missing_intervals_sha256"):
        raise ValueError("fresh missing-interval coordinates differ from sealed evidence")

    refetch = reconciliation.get("refetch")
    if not isinstance(refetch, Mapping) or refetch.get("status") != "EXACT_PROVIDER_VALUE_MATCH":
        raise ValueError("sealed yearly evidence lacks exact independent provider refetch")

    return market_gaps_from_complete_s5_evidence(
        reconciliation,
        s5_evidence,
        venue=VENUE,
    )


def market_gaps_from_canonical_tail_evidence(
    evidence: Mapping[str, object],
) -> tuple[MarketGapV2, ...]:
    """Convert the separately qualified NY-boundary tail into fail-closed gap policy."""

    if evidence.get("schema_version") != TAIL_EVIDENCE_SCHEMA_VERSION:
        raise ValueError("unexpected canonical-tail evidence schema")
    if evidence.get("canonical_coverage_policy_version") != CANONICAL_COVERAGE_POLICY_VERSION:
        raise ValueError("unexpected canonical coverage policy")
    if evidence.get("observation_policy_version") != OBSERVATION_POLICY_VERSION:
        raise ValueError("unexpected tail observation policy")
    if evidence.get("provider") != PROVIDER or evidence.get("venue") != VENUE:
        raise ValueError("canonical-tail evidence provider/venue mismatch")
    if evidence.get("environment") != "practice":
        raise ValueError("canonical-tail evidence must come from practice")
    if evidence.get("price_component") != "MID" or evidence.get("granularity") != "M1":
        raise ValueError("canonical-tail evidence must describe MID/M1")

    instrument = evidence.get("instrument")
    if not isinstance(instrument, str) or not instrument:
        raise ValueError("canonical-tail instrument is required")
    start = _parse_utc(evidence.get("requested_start_utc"), field="requested_start_utc")
    end = _parse_utc(evidence.get("requested_end_utc"), field="requested_end_utc")
    if start != CANONICAL_TAIL_START_UTC or end != CANONICAL_TAIL_END_UTC:
        raise ValueError("canonical-tail evidence does not cover the exact frozen boundary")
    if end != CANONICAL_COVERAGE_END_UTC:
        raise ValueError("canonical-tail end does not complete frozen DEV coverage")

    primary = evidence.get("primary")
    refetch = evidence.get("refetch")
    if not isinstance(primary, Mapping) or not isinstance(refetch, Mapping):
        raise TypeError("canonical-tail primary/refetch evidence is required")
    if primary.get("complete_candle_count") != 0 or refetch.get("complete_candle_count") != 0:
        raise ValueError("sealed canonical tail is expected to contain zero M1 observations")
    if refetch.get("status") != "EXACT_PROVIDER_EMPTY_MATCH":
        raise ValueError("canonical-tail independent refetch must exactly confirm empty provider data")
    _sha256_text(primary.get("request_sha256"), field="primary.request_sha256")
    _sha256_text(primary.get("raw_response_sha256"), field="primary.raw_response_sha256")
    _sha256_text(refetch.get("request_sha256"), field="refetch.request_sha256")
    _sha256_text(refetch.get("raw_response_sha256"), field="refetch.raw_response_sha256")

    if evidence.get("unresolved_provider_gap_count") != 0:
        raise ValueError("canonical-tail unresolved gap prevents trusted dataset construction")
    if evidence.get("unresolved_provider_gap_minutes") != 0:
        raise ValueError("canonical-tail unresolved minutes prevent trusted dataset construction")

    classifications = evidence.get("classifications")
    if not isinstance(classifications, list):
        raise TypeError("canonical-tail classifications must be a list")
    if len(classifications) != evidence.get("missing_interval_count"):
        raise ValueError("canonical-tail classification inventory is incomplete")

    s5 = evidence.get("s5_evidence")
    if not isinstance(s5, Mapping):
        raise TypeError("canonical-tail S5 provider evidence is required")
    if s5.get("complete_s5_count") != 0:
        raise ValueError("canonical-tail S5 evidence contradicts NO_PRICE_OBSERVATION")
    _sha256_text(s5.get("request_sha256"), field="tail_s5.request_sha256")
    _sha256_text(s5.get("raw_response_sha256"), field="tail_s5.raw_response_sha256")

    gaps: list[MarketGapV2] = []
    total_minutes = 0
    for index, raw in enumerate(classifications):
        if not isinstance(raw, Mapping):
            raise TypeError("canonical-tail classification must be an object")
        if raw.get("gap_index") != index:
            raise ValueError("canonical-tail gap indexes must be exact and ordered")
        if raw.get("classification") != "NO_PRICE_OBSERVATION":
            raise ValueError("non-terminal canonical-tail classification prevents trust")
        if raw.get("s5_complete_observations_inside_gap") != 0:
            raise ValueError("canonical-tail classification contains S5 observations")
        gap_start = _parse_utc(raw.get("start_utc"), field="tail_gap.start_utc")
        gap_end = _parse_utc(raw.get("end_utc"), field="tail_gap.end_utc")
        delta = gap_end - gap_start
        if delta <= timedelta(0) or delta.total_seconds() % 60:
            raise ValueError("canonical-tail gap must span positive whole minutes")
        minutes = int(delta.total_seconds() // 60)
        if raw.get("missing_minutes") != minutes:
            raise ValueError("canonical-tail missing-minute count mismatches coordinates")
        total_minutes += minutes
        evidence_seed = {
            "instrument": instrument,
            "classification": dict(raw),
            "s5_request_sha256": s5["request_sha256"],
            "s5_raw_response_sha256": s5["raw_response_sha256"],
        }
        evidence_sha = sha256(
            json.dumps(evidence_seed, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        gaps.append(
            MarketGapV2(
                provider=PROVIDER,
                venue=VENUE,
                instrument=instrument,
                start_time=gap_start,
                end_time=gap_end,
                category=GapCategory.NO_PRICE_OBSERVATION,
                policy_version=OBSERVATION_POLICY_VERSION,
                evidence_id=f"P6B-TAIL-{evidence_sha}",
                evidence_source=(
                    "OANDA practice MID/M1 independent empty refetch plus MID/S5 "
                    f"cross-granularity evidence; schema={TAIL_EVIDENCE_SCHEMA_VERSION}"
                ),
            )
        )

    if total_minutes != evidence.get("missing_minutes"):
        raise ValueError("canonical-tail missing-minute inventory does not balance")
    if len(gaps) != evidence.get("no_price_observation_gap_count"):
        raise ValueError("canonical-tail no-price gap count does not balance")
    if total_minutes != evidence.get("no_price_observation_minutes"):
        raise ValueError("canonical-tail no-price minute count does not balance")
    return tuple(gaps)


def trusted_dataset_identity(
    *,
    instrument: OandaInstrumentRecord,
    normalized_sha256: str,
    h1_rows: int,
    d1_rows: int,
) -> PriceDatasetIdentityV2:
    quantum, source = oanda_price_quantum(instrument)
    _sha256_text(normalized_sha256, field="normalized_sha256")
    return PriceDatasetIdentityV2(
        dataset_version=f"{TRUSTED_DATASET_VERSION_PREFIX}-{instrument.name}",
        provider=PROVIDER,
        venue=VENUE,
        instrument=instrument.name,
        price_component=PriceComponent.MID,
        price_quantum=quantum,
        price_quantum_source=source,
        price_quantum_observed_at=instrument.observed_at,
        instrument_metadata_sha256=oanda_instrument_metadata_sha256(instrument),
        session_policy_version=OBSERVATION_POLICY_VERSION,
        normalized_sha256=normalized_sha256,
        h1_rows=h1_rows,
        d1_rows=d1_rows,
        quality_status="TRUSTED",
    )


def price_dataset_identity_record(identity: PriceDatasetIdentityV2) -> dict[str, object]:
    return {
        "schema_version": identity.schema_version,
        "dataset_version": identity.dataset_version,
        "provider": identity.provider,
        "venue": identity.venue,
        "instrument": identity.instrument,
        "price_component": identity.price_component.value,
        "price_quantum": format(identity.price_quantum, "f"),
        "price_quantum_source": identity.price_quantum_source.value,
        "price_quantum_observed_at_utc": identity.price_quantum_observed_at.astimezone(UTC).isoformat(),
        "instrument_metadata_sha256": identity.instrument_metadata_sha256,
        "session_policy_version": identity.session_policy_version,
        "normalized_sha256": identity.normalized_sha256,
        "h1_rows": identity.h1_rows,
        "d1_rows": identity.d1_rows,
        "quality_status": identity.quality_status,
    }
