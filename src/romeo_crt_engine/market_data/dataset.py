from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from typing import Any

from romeo_crt_engine.market_data.models import (
    CanonicalBar,
    InstrumentMetadata,
    ProviderVerificationEvidence,
)
from romeo_crt_engine.storage import DatasetRef, LocalArtifactStore

MANIFEST_SCHEMA_VERSION = "PHASE3_DATASET_MANIFEST_V1"
RECEIPT_SCHEMA_VERSION = "PHASE3_INGESTION_RECEIPT_V1"
NORMALIZER_VERSION = "NY_D1_H1_FROM_UTC_M1_V1"


@dataclass(frozen=True, slots=True)
class RawArtifact:
    archive_date: str
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
    market_data_code_sha256: str
    dependency_lock_sha256: str
    coverage_start_utc: str
    coverage_end_utc: str
    m1_rows: int
    h1_rows: int
    d1_rows: int
    normalized_sha256: str
    raw_artifacts: tuple[dict[str, Any], ...]
    provider_crosschecks: tuple[dict[str, Any], ...]
    quality_status: str
    correction_policy: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":")) + "\n"

    @property
    def manifest_sha256(self) -> str:
        return sha256(self.to_json().encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class IngestionReceipt:
    schema_version: str
    dataset_id: str
    dataset_version: str
    manifest_sha256: str
    retrieved_at_utc: str
    git_revision: str
    raw_sha256: tuple[str, ...]
    provider_crosscheck_digests: tuple[str, ...]

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":")) + "\n"

    @property
    def receipt_sha256(self) -> str:
        return sha256(self.to_json().encode("utf-8")).hexdigest()

    def to_dataset_ref(self) -> DatasetRef:
        return DatasetRef(
            dataset_id=self.dataset_id,
            version=self.dataset_version,
            manifest_sha256=self.manifest_sha256,
            created_at=datetime.fromisoformat(self.retrieved_at_utc),
        )


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
    provider_crosschecks: tuple[ProviderVerificationEvidence, ...],
    m1_rows: int,
    h1: tuple[CanonicalBar, ...],
    d1: tuple[CanonicalBar, ...],
    market_data_code_sha256: str,
    dependency_lock_sha256: str,
) -> DatasetManifest:
    if not raw_artifacts or not h1 or not d1:
        raise ValueError("trusted dataset requires raw artifacts plus H1 and D1 bars")
    for name, digest in (
        ("market_data_code_sha256", market_data_code_sha256),
        ("dependency_lock_sha256", dependency_lock_sha256),
    ):
        if len(digest) != 64:
            raise ValueError(f"{name} must be a SHA-256 digest")

    raw_hashes = {artifact.sha256 for artifact in raw_artifacts}
    evidence_hashes = {evidence.source_sha256 for evidence in provider_crosschecks}
    if evidence_hashes != raw_hashes or len(provider_crosschecks) != len(raw_artifacts):
        raise ValueError("every raw artifact requires exactly one provider REST cross-check")

    normalized_sha = normalized_digest(h1, d1)
    metadata_observed_at = metadata.observed_at.astimezone(UTC).isoformat()
    artifact_records = tuple(
        {
            "archive_date": artifact.archive_date,
            "filename": artifact.filename,
            "source_url": artifact.source_url,
            "checksum_url": artifact.checksum_url,
            "sha256": artifact.sha256,
            "size_bytes": len(artifact.content),
        }
        for artifact in raw_artifacts
    )
    crosscheck_records = tuple(
        {
            "provider": evidence.provider,
            "venue": evidence.venue,
            "symbol": evidence.symbol,
            "source_sha256": evidence.source_sha256,
            "sample_refs": evidence.sample_refs,
            "endpoint_base": evidence.endpoint_base,
            "verification_method": evidence.verification_method,
            "evidence_digest": evidence.evidence_digest,
        }
        for evidence in provider_crosschecks
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
        "market_data_code_sha256": market_data_code_sha256,
        "dependency_lock_sha256": dependency_lock_sha256,
        "normalized_sha256": normalized_sha,
        "raw_sha256": [artifact.sha256 for artifact in raw_artifacts],
        "provider_crosscheck_digest": [
            evidence.evidence_digest for evidence in provider_crosschecks
        ],
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
        market_data_code_sha256=market_data_code_sha256,
        dependency_lock_sha256=dependency_lock_sha256,
        coverage_start_utc=h1[0].open_time.astimezone(UTC).isoformat(),
        coverage_end_utc=h1[-1].close_time.astimezone(UTC).isoformat(),
        m1_rows=m1_rows,
        h1_rows=len(h1),
        d1_rows=len(d1),
        normalized_sha256=normalized_sha,
        raw_artifacts=artifact_records,
        provider_crosschecks=crosscheck_records,
        quality_status="TRUSTED",
        correction_policy="IMMUTABLE_NEW_VERSION_ON_SOURCE_OR_NORMALIZATION_CHANGE",
    )


def build_receipt(
    *,
    manifest: DatasetManifest,
    raw_artifacts: tuple[RawArtifact, ...],
    provider_crosschecks: tuple[ProviderVerificationEvidence, ...],
    retrieved_at: datetime,
    git_revision: str,
) -> IngestionReceipt:
    if retrieved_at.utcoffset() is None:
        raise ValueError("retrieved_at must be timezone-aware")
    if not git_revision:
        raise ValueError("git_revision must not be empty")
    return IngestionReceipt(
        schema_version=RECEIPT_SCHEMA_VERSION,
        dataset_id=f"{manifest.provider}:{manifest.venue}:{manifest.symbol}",
        dataset_version=manifest.dataset_version,
        manifest_sha256=manifest.manifest_sha256,
        retrieved_at_utc=retrieved_at.astimezone(UTC).isoformat(),
        git_revision=git_revision,
        raw_sha256=tuple(artifact.sha256 for artifact in raw_artifacts),
        provider_crosscheck_digests=tuple(
            evidence.evidence_digest for evidence in provider_crosschecks
        ),
    )


def write_dataset(
    *,
    root: Path,
    raw_artifacts: tuple[RawArtifact, ...],
    h1: tuple[CanonicalBar, ...],
    d1: tuple[CanonicalBar, ...],
    manifest: DatasetManifest,
    receipt: IngestionReceipt,
) -> Path:
    if receipt.dataset_version != manifest.dataset_version:
        raise ValueError("ingestion receipt does not belong to manifest dataset version")
    store = LocalArtifactStore(root)
    for artifact in raw_artifacts:
        store.put_bytes(
            (
                f"raw/{manifest.provider}/{manifest.venue}/{manifest.symbol}/1m/"
                f"{artifact.archive_date}-{artifact.sha256}.zip"
            ),
            artifact.content,
            "application/zip",
        )

    dataset_key = f"normalized/{manifest.dataset_version}"
    store.put_bytes(f"{dataset_key}/H1.jsonl", encode_bars_jsonl(h1), "application/x-ndjson")
    store.put_bytes(f"{dataset_key}/D1.jsonl", encode_bars_jsonl(d1), "application/x-ndjson")
    store.put_bytes(
        f"{dataset_key}/manifest.json",
        manifest.to_json().encode("utf-8"),
        "application/json",
    )
    store.put_bytes(
        f"receipts/{manifest.dataset_version}/{receipt.receipt_sha256}.json",
        receipt.to_json().encode("utf-8"),
        "application/json",
    )
    return root / "normalized" / manifest.dataset_version
