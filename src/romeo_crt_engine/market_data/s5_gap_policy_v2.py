from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from hashlib import sha256

from romeo_crt_engine.market_data.session_policy_v2 import GapCategory, MarketGapV2

RECONCILIATION_SCHEMA_VERSION = "P6B_OANDA_RECONCILIATION_EVIDENCE_V2"
S5_EVIDENCE_SCHEMA_VERSION = "P6B_OANDA_S5_GAP_EVIDENCE_V1"
OBSERVATION_POLICY_VERSION = "P6B_OANDA_OBSERVATION_POLICY_V2"


def _parse_utc(value: object) -> datetime:
    if not isinstance(value, str):
        raise TypeError("evidence timestamp must be a string")
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError("evidence timestamp must be timezone-aware")
    parsed = parsed.astimezone(UTC)
    if parsed.second or parsed.microsecond:
        raise ValueError("gap evidence timestamps must be minute-aligned")
    return parsed


def _sha256_text(value: object, *, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"{field} must be a SHA-256 digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"{field} must be hexadecimal") from exc
    return value.lower()


def _gap_minutes(start: datetime, end: datetime) -> int:
    delta = end - start
    if delta <= timedelta(0) or delta.total_seconds() % 60:
        raise ValueError("gap evidence must span positive whole minutes")
    return int(delta.total_seconds() // 60)


def _validate_identity(
    reconciliation: Mapping[str, object],
    s5_evidence: Mapping[str, object],
) -> tuple[str, int, str]:
    if reconciliation.get("schema_version") != RECONCILIATION_SCHEMA_VERSION:
        raise ValueError("unexpected reconciliation evidence schema")
    if s5_evidence.get("schema_version") != S5_EVIDENCE_SCHEMA_VERSION:
        raise ValueError("unexpected S5 evidence schema")
    if reconciliation.get("observation_policy_version") != OBSERVATION_POLICY_VERSION:
        raise ValueError("unexpected reconciliation observation policy")
    if s5_evidence.get("observation_policy_version") != OBSERVATION_POLICY_VERSION:
        raise ValueError("unexpected S5 observation policy")
    if reconciliation.get("provider") != "OANDA_V20" or s5_evidence.get("provider") != "OANDA_V20":
        raise ValueError("S5 gap policy accepts OANDA_V20 evidence only")
    if reconciliation.get("environment") != "practice" or s5_evidence.get("environment") != "practice":
        raise ValueError("S5 gap policy accepts practice evidence only")
    if reconciliation.get("price_component") != "MID" or reconciliation.get("granularity") != "M1":
        raise ValueError("reconciliation evidence must describe MID/M1 observations")

    instrument = reconciliation.get("instrument")
    year = reconciliation.get("year")
    if not isinstance(instrument, str) or not instrument:
        raise ValueError("reconciliation instrument is required")
    if not isinstance(year, int):
        raise ValueError("reconciliation year is required")
    if s5_evidence.get("instrument") != instrument or s5_evidence.get("year") != year:
        raise ValueError("S5 evidence identity does not match reconciliation evidence")

    missing_digest = _sha256_text(
        reconciliation.get("missing_intervals_sha256"),
        field="missing_intervals_sha256",
    )
    if s5_evidence.get("source_missing_intervals_sha256") != missing_digest:
        raise ValueError("S5 evidence does not bind to the raw missing-interval inventory")
    return instrument, year, missing_digest


def market_gaps_from_complete_s5_evidence(
    reconciliation: Mapping[str, object],
    s5_evidence: Mapping[str, object],
    *,
    venue: str = "OANDA_FXTRADE",
) -> tuple[MarketGapV2, ...]:
    """Convert complete cross-granularity evidence into approved omission policy.

    This adapter is deliberately fail-closed. It accepts only an all-gap S5
    evidence set whose classification inventory exactly matches the raw M1 gap
    inventory. Every accepted interval must contain zero complete S5 price
    observations. A single unresolved interval prevents construction of a
    detector-facing gap policy.
    """

    instrument, year, missing_digest = _validate_identity(reconciliation, s5_evidence)
    if not venue:
        raise ValueError("venue must not be empty")

    missing = reconciliation.get("missing_intervals")
    classifications = s5_evidence.get("classifications")
    if not isinstance(missing, list):
        raise TypeError("reconciliation evidence lacks missing intervals")
    if not isinstance(classifications, list):
        raise TypeError("S5 evidence lacks classifications")

    declared_missing_count = reconciliation.get("missing_interval_count")
    declared_eligible_count = s5_evidence.get("eligible_gap_count")
    if declared_missing_count != len(missing):
        raise ValueError("raw missing-interval count does not match inventory")
    if declared_eligible_count != len(missing):
        raise ValueError("complete all-gap S5 evidence is required")
    if len(classifications) != len(missing):
        raise ValueError("S5 classification count must equal raw missing-interval count")

    declared_no_price = s5_evidence.get("no_price_observation_gap_count")
    declared_unresolved = s5_evidence.get("unresolved_provider_gap_count")
    if not isinstance(declared_no_price, int) or not isinstance(declared_unresolved, int):
        raise ValueError("S5 classification counters are required")
    if declared_no_price + declared_unresolved != len(missing):
        raise ValueError("S5 classification counters do not balance")
    if declared_unresolved != 0:
        raise ValueError("UNRESOLVED_PROVIDER_GAP prevents trusted gap policy construction")

    by_index: dict[int, Mapping[str, object]] = {}
    for raw in classifications:
        if not isinstance(raw, Mapping):
            raise TypeError("S5 classification must be an object")
        index = raw.get("gap_index")
        if not isinstance(index, int) or index < 0 or index in by_index:
            raise ValueError("S5 gap indexes must be unique non-negative integers")
        by_index[index] = raw
    if set(by_index) != set(range(len(missing))):
        raise ValueError("S5 gap indexes must cover the raw inventory exactly")

    output: list[MarketGapV2] = []
    for index, raw_missing in enumerate(missing):
        if not isinstance(raw_missing, Mapping):
            raise TypeError("raw missing interval must be an object")
        raw_classification = by_index[index]

        start = _parse_utc(raw_missing.get("start_utc"))
        end = _parse_utc(raw_missing.get("end_utc"))
        minutes = _gap_minutes(start, end)
        if raw_missing.get("missing_minutes") != minutes:
            raise ValueError("raw missing-minute count does not match coordinates")
        if raw_classification.get("start_utc") != start.isoformat():
            raise ValueError("S5 classification start does not match raw gap")
        if raw_classification.get("end_utc") != end.isoformat():
            raise ValueError("S5 classification end does not match raw gap")
        if raw_classification.get("missing_minutes") != minutes:
            raise ValueError("S5 classification minute count does not match raw gap")
        if raw_classification.get("classification") != "NO_PRICE_OBSERVATION":
            raise ValueError("non-terminal S5 classification prevents trusted gap policy")
        if raw_classification.get("s5_complete_observations_inside_gap") != 0:
            raise ValueError("NO_PRICE_OBSERVATION evidence must contain zero S5 observations")

        refs = raw_classification.get("evidence")
        if not isinstance(refs, list) or not refs:
            raise ValueError("NO_PRICE_OBSERVATION classification requires provider evidence")
        for ref in refs:
            if not isinstance(ref, Mapping):
                raise TypeError("S5 evidence reference must be an object")
            _sha256_text(ref.get("request_sha256"), field="request_sha256")
            _sha256_text(ref.get("raw_response_sha256"), field="raw_response_sha256")
            count_inside = ref.get("complete_s5_count_in_gap")
            if not isinstance(count_inside, int) or count_inside != 0:
                raise ValueError("S5 evidence reference contradicts NO_PRICE_OBSERVATION")

        evidence_record = {
            "schema_version": S5_EVIDENCE_SCHEMA_VERSION,
            "instrument": instrument,
            "year": year,
            "source_missing_intervals_sha256": missing_digest,
            "classification": raw_classification,
        }
        evidence_sha = sha256(
            json.dumps(evidence_record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        output.append(
            MarketGapV2(
                provider="OANDA_V20",
                venue=venue,
                instrument=instrument,
                start_time=start,
                end_time=end,
                category=GapCategory.NO_PRICE_OBSERVATION,
                policy_version=OBSERVATION_POLICY_VERSION,
                evidence_id=f"P6B-S5-{evidence_sha}",
                evidence_source=(
                    "OANDA practice MID/S5 cross-granularity provider evidence; "
                    f"schema={S5_EVIDENCE_SCHEMA_VERSION}"
                ),
            )
        )

    return tuple(output)
