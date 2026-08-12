from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, date
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from typing import Any

from romeo_crt_engine.market_data.models import CanonicalBar, InstrumentMetadata

MANIFEST_SCHEMA_VERSION = "PHASE3_DATASET_MANIFEST_V1"
NORMALIZER_VERSION = "NY_D1_H1_FROM_UTC_M1_V1"


@dataclass(frozen=True, slots=True)
class RawArtifact:
    archive_date: date
    filename: str
    source_url: str
    checksum_url: str
    sha256: str
    content: bytes

    def __post_init__(self) -> None:
        if len(self.sha256) != 64:
            raise ValueError("raw artifact sha256 must be 64 characters")
        if sha256(self.content).hexdigest() != self.sha256:
            raise ValueError("raw artifact content does not match sha256")


@dataclass(frozen=True, slots=True)
class DatasetManifest:
    schema_version: str
    dataset_version: str
    provider: str
    venue: str
    symbol: str
    asset_class: str
    instrument_metadata_version: str
    instrument_metadata_observed_at: str
    price_tick_size: str
    quantity_step: str
    metadata_temporal_semantics: str
    internal_timezone: str
    analytical_timezone: str
    normalizer_version: str
    code_version: str
    dependency_lock_sha256: str
    coverage_start_utc: str
    coverage_end_utc: str
    m1_rows: int
    h1_rows: int
    d1_rows: int
    normalized_sha256: str
    raw_artifacts: tuple[dict[str, Any], ...]
    quality_status: str
    correction_policy: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":")) + "\n"

    @property
    def manifest_sha256(self) -> str:
        return sha256(self.to_json().encode("utf-8")).hexdigest()


def _decimal_text(value: Decimal) -> str:
    return format(value, "f")


def _bar_record(bar: CanonicalBar) -> dict[str, Any]:
    return {
        "provider": bar.provider,
        "venue": bar.venue,
        "symbol": bar.symbol,
        "timeframe": bar.timeframe.value,
        "open_time_utc": bar.open_time.astimezone(UTC).isoformat(),
        "close_time_utc": bar.close_time.astimezone(UTC).isoformat(),
        "open": _decimal_text(bar.open),
        "high": _decimal_text(bar.high),
        "low": _decimal_text(bar.low),
        "close": _decimal_text(bar.close),
        "volume": _decimal_text(bar.volume),
        "quote_volume": _decimal_text(bar.quote_volume),
        "trade_count": bar.trade_count,
        "source_count": bar.source_count,
        "source_digest": bar.source_digest,
    }


def encode_bars_jsonl(bars: tuple[CanonicalBar, ...]) -> bytes:
    records = [
        json.dumps(_bar_record(bar), sort_keys=True, separators=(",", ":")) for bar in bars
    ]
    return (("\n".join(records) + "\n") if records else "").encode("utf-8")


def normalized_digest(h1: tuple[CanonicalBar, ...], d1: tuple[CanonicalBar, ...]) -> str:
    digest = sha256()
    digest.update(b"H1\n")
    digest.update(encode_bars_jsonl(h1))
    digest.update(b"D1\n")
    digest.update(encode_bars_jsonl(d1))
    return digest.hexdigest()


def build_manifest(
    *,
    metadata: InstrumentMetadata,
    raw_artifacts: tuple[RawArtifact, ...],
    m1_rows: int,
    h1: tuple[CanonicalBar, ...],
    d1: tuple[CanonicalBar, ...],
    code_version: str,
    dependency_lock_sha256: str,
) -> DatasetManifest:
    if not raw_artifacts or not h1 or not d1:
        raise ValueError("trusted dataset requires raw artifacts plus H1 and D1 bars")
    if len(dependency_lock_sha256) != 64:
        raise ValueError("dependency_lock_sha256 must be a SHA-256 digest")

    normalized_sha = normalized_digest(h1, d1)
    metadata_observed_at = metadata.observed_at.astimezone(UTC).isoformat()
    artifact_records = tuple(
        {
            "archive_date": artifact.archive_date.isoformat(),
            "filename": artifact.filename,
            "source_url": artifact.source_url,
            "checksum_url": artifact.checksum_url,
            "sha256": artifact.sha256,
            "size_bytes": len(artifact.content),
        }
        for artifact in raw_artifacts
    )

    version_seed = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "provider": metadata.provider,
        "venue": metadata.venue,
        "symbol": metadata.symbol,
        "instrument_metadata_version": metadata.metadata_version,
        "instrument_metadata_observed_at": metadata_observed_at,
        "analytical_timezone": "America/New_York",
        "normalizer_version": NORMALIZER_VERSION,
        "code_version": code_version,
        "dependency_lock_sha256": dependency_lock_sha256,
        "normalized_sha256": normalized_sha,
        "raw_sha256": [artifact.sha256 for artifact in raw_artifacts],
    }
    dataset_version = sha256(
        json.dumps(version_seed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:24]

    return DatasetManifest(
        schema_version=MANIFEST_SCHEMA_VERSION,
        dataset_version=dataset_version,
        provider=metadata.provider,
        venue=metadata.venue,
        symbol=metadata.symbol,
        asset_class=metadata.asset_class.value,
        instrument_metadata_version=metadata.metadata_version,
        instrument_metadata_observed_at=metadata_observed_at,
        price_tick_size=_decimal_text(metadata.price_tick_size),
        quantity_step=_decimal_text(metadata.quantity_step),
        metadata_temporal_semantics=metadata.temporal_semantics,
        internal_timezone="UTC",
        analytical_timezone="America/New_York",
        normalizer_version=NORMALIZER_VERSION,
        code_version=code_version,
        dependency_lock_sha256=dependency_lock_sha256,
        coverage_start_utc=h1[0].open_time.astimezone(UTC).isoformat(),
        coverage_end_utc=h1[-1].close_time.astimezone(UTC).isoformat(),
        m1_rows=m1_rows,
        h1_rows=len(h1),
        d1_rows=len(d1),
        normalized_sha256=normalized_sha,
        raw_artifacts=artifact_records,
        quality_status="TRUSTED",
        correction_policy="IMMUTABLE_NEW_VERSION_ON_SOURCE_OR_NORMALIZATION_CHANGE",
    )


def _write_or_verify(path: Path, expected: bytes) -> None:
    if path.exists():
        if path.read_bytes() != expected:
            raise ValueError(f"immutable dataset path contains different content: {path}")
        return
    path.write_bytes(expected)


def write_dataset(
    *,
    root: Path,
    raw_artifacts: tuple[RawArtifact, ...],
    h1: tuple[CanonicalBar, ...],
    d1: tuple[CanonicalBar, ...],
    manifest: DatasetManifest,
) -> Path:
    for artifact in raw_artifacts:
        raw_dir = root / "raw" / manifest.provider / manifest.venue / manifest.symbol / "1m"
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / f"{artifact.archive_date.isoformat()}-{artifact.sha256}.zip"
        _write_or_verify(raw_path, artifact.content)

    dataset_dir = root / "normalized" / manifest.dataset_version
    dataset_dir.mkdir(parents=True, exist_ok=True)
    _write_or_verify(dataset_dir / "H1.jsonl", encode_bars_jsonl(h1))
    _write_or_verify(dataset_dir / "D1.jsonl", encode_bars_jsonl(d1))
    _write_or_verify(dataset_dir / "manifest.json", manifest.to_json().encode("utf-8"))
    return dataset_dir
