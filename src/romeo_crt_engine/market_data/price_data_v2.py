from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from hashlib import sha256

from romeo_crt_engine.market_data.models import BarTimeframe

CANONICAL_PRICE_SCHEMA_VERSION = "P6B_CANONICAL_PRICE_DATASET_V2"


class PriceComponent(StrEnum):
    TRADED = "TRADED"
    MID = "MID"
    BID = "BID"
    ASK = "ASK"


class ActivitySemantic(StrEnum):
    PRICE_COUNT = "PRICE_COUNT"
    BASE_VOLUME = "BASE_VOLUME"
    QUOTE_VOLUME = "QUOTE_VOLUME"
    TRADE_COUNT = "TRADE_COUNT"


class PriceQuantumSource(StrEnum):
    PROVIDER_EXPLICIT = "PROVIDER_EXPLICIT"
    PROVIDER_PRICE_PRECISION_POLICY = "PROVIDER_PRICE_PRECISION_POLICY"
    VENUE_CONTRACT_SPECIFICATION = "VENUE_CONTRACT_SPECIFICATION"
    PROJECT_EXECUTION_PARAMETER = "PROJECT_EXECUTION_PARAMETER"


@dataclass(frozen=True, slots=True)
class ActivityMeasure:
    semantic: ActivitySemantic
    value: Decimal

    def __post_init__(self) -> None:
        if not self.value.is_finite() or self.value < 0:
            raise ValueError("activity value must be non-negative and finite")


@dataclass(frozen=True, slots=True)
class CanonicalPriceBarV2:
    """Provider-neutral OHLC bar with explicitly typed optional activity metadata."""

    provider: str
    venue: str
    instrument: str
    price_component: PriceComponent
    timeframe: BarTimeframe
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    source_count: int
    source_digest: str
    session_policy_version: str
    activity: tuple[ActivityMeasure, ...] = ()

    def __post_init__(self) -> None:
        if not self.provider or not self.venue or not self.instrument:
            raise ValueError("price-bar identity fields must not be empty")
        if not self.session_policy_version:
            raise ValueError("session_policy_version must not be empty")
        if self.open_time.utcoffset() != timedelta(0) or self.close_time.utcoffset() != timedelta(0):
            raise ValueError("canonical price timestamps must be UTC")
        if self.close_time <= self.open_time:
            raise ValueError("close_time must be after open_time")
        if self.timeframe is BarTimeframe.M1 and self.close_time - self.open_time != timedelta(minutes=1):
            raise ValueError("M1 canonical price bar must span exactly one minute")
        if self.timeframe is BarTimeframe.H1 and self.close_time - self.open_time != timedelta(hours=1):
            raise ValueError("H1 canonical price bar must span exactly one hour")

        values = (self.open, self.high, self.low, self.close)
        if not all(value.is_finite() for value in values):
            raise ValueError("OHLC values must be finite")
        if self.high < self.low:
            raise ValueError("high must be >= low")
        if self.high < max(self.open, self.close):
            raise ValueError("high must contain open and close")
        if self.low > min(self.open, self.close):
            raise ValueError("low must contain open and close")
        if self.source_count <= 0:
            raise ValueError("source_count must be > 0")
        if len(self.source_digest) != 64:
            raise ValueError("source_digest must be a SHA-256 digest")

        semantics = [measure.semantic for measure in self.activity]
        if len(semantics) != len(set(semantics)):
            raise ValueError("activity semantic may occur at most once per bar")


@dataclass(frozen=True, slots=True)
class PriceDatasetIdentityV2:
    dataset_version: str
    provider: str
    venue: str
    instrument: str
    price_component: PriceComponent
    price_quantum: Decimal
    price_quantum_source: PriceQuantumSource
    price_quantum_observed_at: datetime
    instrument_metadata_sha256: str
    session_policy_version: str
    normalized_sha256: str
    h1_rows: int
    d1_rows: int
    quality_status: str
    schema_version: str = CANONICAL_PRICE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != CANONICAL_PRICE_SCHEMA_VERSION:
            raise ValueError("unsupported Phase-6B price dataset schema")
        if not self.dataset_version or not self.provider or not self.venue or not self.instrument:
            raise ValueError("dataset identity fields must not be empty")
        if not self.price_quantum.is_finite() or self.price_quantum <= 0:
            raise ValueError("price_quantum must be positive and finite")
        if self.price_quantum_observed_at.utcoffset() is None:
            raise ValueError("price_quantum_observed_at must be timezone-aware")
        if not self.session_policy_version:
            raise ValueError("session_policy_version must not be empty")
        for digest in (self.instrument_metadata_sha256, self.normalized_sha256):
            if len(digest) != 64:
                raise ValueError("dataset digests must be SHA-256 values")
        if self.h1_rows < 0 or self.d1_rows < 0:
            raise ValueError("dataset row counts must be non-negative")
        if self.quality_status != "TRUSTED":
            raise ValueError("detector-facing Phase-6B data must be TRUSTED")


def _decimal_text(value: Decimal) -> str:
    return format(value, "f")


def canonical_price_bar_record(bar: CanonicalPriceBarV2) -> dict[str, object]:
    return {
        "provider": bar.provider,
        "venue": bar.venue,
        "instrument": bar.instrument,
        "price_component": bar.price_component.value,
        "timeframe": bar.timeframe.value,
        "open_time_utc": bar.open_time.astimezone(UTC).isoformat(),
        "close_time_utc": bar.close_time.astimezone(UTC).isoformat(),
        "open": _decimal_text(bar.open),
        "high": _decimal_text(bar.high),
        "low": _decimal_text(bar.low),
        "close": _decimal_text(bar.close),
        "source_count": bar.source_count,
        "source_digest": bar.source_digest,
        "session_policy_version": bar.session_policy_version,
        "activity": [
            {"semantic": measure.semantic.value, "value": _decimal_text(measure.value)}
            for measure in sorted(bar.activity, key=lambda item: item.semantic.value)
        ],
    }


def encode_canonical_price_bars_jsonl(bars: tuple[CanonicalPriceBarV2, ...]) -> bytes:
    records = [
        json.dumps(canonical_price_bar_record(bar), sort_keys=True, separators=(",", ":"))
        for bar in bars
    ]
    return (("\n".join(records) + "\n") if records else "").encode()


def normalized_price_digest_v2(
    h1: tuple[CanonicalPriceBarV2, ...],
    d1: tuple[CanonicalPriceBarV2, ...],
) -> str:
    if any(bar.timeframe is not BarTimeframe.H1 for bar in h1):
        raise ValueError("H1 digest input contains a non-H1 price bar")
    if any(bar.timeframe is not BarTimeframe.D1 for bar in d1):
        raise ValueError("D1 digest input contains a non-D1 price bar")
    digest = sha256()
    digest.update(b"P6B_PRICE_H1\n")
    digest.update(encode_canonical_price_bars_jsonl(h1))
    digest.update(b"P6B_PRICE_D1\n")
    digest.update(encode_canonical_price_bars_jsonl(d1))
    return digest.hexdigest()
