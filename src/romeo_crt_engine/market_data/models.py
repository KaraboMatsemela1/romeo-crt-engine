from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from hashlib import sha256


class AssetClass(StrEnum):
    CRYPTO_SPOT = "CRYPTO_SPOT"


class BarTimeframe(StrEnum):
    M1 = "M1"
    H1 = "H1"
    D1 = "D1"


def _require_aware(timestamp: datetime, field_name: str) -> None:
    if timestamp.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


def _require_utc(timestamp: datetime, field_name: str) -> None:
    _require_aware(timestamp, field_name)
    if timestamp.utcoffset() != UTC.utcoffset(timestamp):
        raise ValueError(f"{field_name} must be UTC")


def _require_positive_decimal(value: Decimal, field_name: str) -> None:
    if not value.is_finite() or value <= 0:
        raise ValueError(f"{field_name} must be positive and finite")


def _require_non_negative_decimal(value: Decimal, field_name: str) -> None:
    if not value.is_finite() or value < 0:
        raise ValueError(f"{field_name} must be non-negative and finite")


def _validate_ohlc(open_: Decimal, high: Decimal, low: Decimal, close: Decimal) -> None:
    values = (open_, high, low, close)
    if not all(value.is_finite() for value in values):
        raise ValueError("OHLC values must be finite")
    if high < low:
        raise ValueError("high must be >= low")
    if high < max(open_, close):
        raise ValueError("high must contain open and close")
    if low > min(open_, close):
        raise ValueError("low must contain open and close")


@dataclass(frozen=True, slots=True)
class InstrumentMetadata:
    provider: str
    venue: str
    symbol: str
    asset_class: AssetClass
    price_tick_size: Decimal
    quantity_step: Decimal
    observed_at: datetime
    metadata_version: str
    temporal_semantics: str = "SNAPSHOT_AT_INGESTION"

    def __post_init__(self) -> None:
        if not self.provider or not self.venue or not self.symbol or not self.metadata_version:
            raise ValueError("instrument identity fields must not be empty")
        _require_positive_decimal(self.price_tick_size, "price_tick_size")
        _require_positive_decimal(self.quantity_step, "quantity_step")
        _require_aware(self.observed_at, "observed_at")

    @property
    def instrument_id(self) -> str:
        return f"{self.provider}:{self.venue}:{self.symbol}"


@dataclass(frozen=True, slots=True)
class ProviderVerificationEvidence:
    provider: str
    venue: str
    symbol: str
    source_sha256: str
    sample_refs: tuple[str, ...]
    endpoint_base: str
    verification_method: str

    def __post_init__(self) -> None:
        if not self.provider or not self.venue or not self.symbol:
            raise ValueError("verification identity fields must not be empty")
        if len(self.source_sha256) != 64:
            raise ValueError("source_sha256 must be a SHA-256 digest")
        if not self.sample_refs or not self.endpoint_base or not self.verification_method:
            raise ValueError("verification evidence fields must not be empty")

    @property
    def evidence_digest(self) -> str:
        payload = {
            "provider": self.provider,
            "venue": self.venue,
            "symbol": self.symbol,
            "source_sha256": self.source_sha256,
            "sample_refs": self.sample_refs,
            "endpoint_base": self.endpoint_base,
            "verification_method": self.verification_method,
        }
        return sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()


@dataclass(frozen=True, slots=True)
class MinuteBar:
    provider: str
    venue: str
    symbol: str
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    quote_volume: Decimal
    trade_count: int
    source_sha256: str

    def __post_init__(self) -> None:
        if not self.provider or not self.venue or not self.symbol:
            raise ValueError("bar identity fields must not be empty")
        _require_utc(self.open_time, "open_time")
        _require_utc(self.close_time, "close_time")
        if self.close_time.timestamp() - self.open_time.timestamp() != 60.0:
            raise ValueError("MinuteBar must span exactly 60 elapsed seconds")
        _validate_ohlc(self.open, self.high, self.low, self.close)
        _require_non_negative_decimal(self.volume, "volume")
        _require_non_negative_decimal(self.quote_volume, "quote_volume")
        if self.trade_count < 0:
            raise ValueError("trade_count must be >= 0")
        if len(self.source_sha256) != 64:
            raise ValueError("source_sha256 must be a 64-character SHA-256 hex digest")


@dataclass(frozen=True, slots=True)
class CanonicalBar:
    provider: str
    venue: str
    symbol: str
    timeframe: BarTimeframe
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    quote_volume: Decimal
    trade_count: int
    source_count: int
    source_digest: str

    def __post_init__(self) -> None:
        if self.timeframe is BarTimeframe.M1:
            raise ValueError("CanonicalBar is reserved for aggregated H1/D1 bars")
        _require_utc(self.open_time, "open_time")
        _require_utc(self.close_time, "close_time")
        if self.close_time.timestamp() <= self.open_time.timestamp():
            raise ValueError("close_time must be after open_time")
        _validate_ohlc(self.open, self.high, self.low, self.close)
        _require_non_negative_decimal(self.volume, "volume")
        _require_non_negative_decimal(self.quote_volume, "quote_volume")
        if self.trade_count < 0 or self.source_count <= 0:
            raise ValueError("trade_count/source_count are invalid")
        if len(self.source_digest) != 64:
            raise ValueError("source_digest must be a 64-character SHA-256 hex digest")
