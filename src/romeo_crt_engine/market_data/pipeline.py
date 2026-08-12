from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from romeo_crt_engine.market_data.aggregate import build_complete_new_york_d1, build_h1
from romeo_crt_engine.market_data.dataset import DatasetManifest, RawArtifact, build_manifest
from romeo_crt_engine.market_data.models import (
    CanonicalBar,
    InstrumentMetadata,
    MinuteBar,
    ProviderVerificationEvidence,
)
from romeo_crt_engine.market_data.providers.binance_public import RawArchive, parse_1m_archive
from romeo_crt_engine.market_data.quality import validate_minute_series


@dataclass(frozen=True, slots=True)
class TrustedDataset:
    metadata: InstrumentMetadata
    raw_artifacts: tuple[RawArtifact, ...]
    provider_crosschecks: tuple[ProviderVerificationEvidence, ...]
    minute_bars: tuple[MinuteBar, ...]
    h1_bars: tuple[CanonicalBar, ...]
    d1_bars: tuple[CanonicalBar, ...]
    manifest: DatasetManifest


def build_trusted_binance_dataset(
    *,
    archives: tuple[RawArchive, ...],
    provider_crosschecks: tuple[ProviderVerificationEvidence, ...],
    metadata: InstrumentMetadata,
    code_version: str,
    dependency_lock_sha256: str,
    created_at: datetime,
) -> TrustedDataset:
    if not archives:
        raise ValueError("at least one archive is required")

    ordered_archives = tuple(sorted(archives, key=lambda archive: archive.archive_date))
    minute_parts = [parse_1m_archive(archive, symbol=metadata.symbol) for archive in ordered_archives]
    minute_bars = tuple(bar for part in minute_parts for bar in part)
    validate_minute_series(minute_bars, as_of=created_at)

    raw_hashes = {archive.sha256 for archive in ordered_archives}
    evidence_hashes = {evidence.source_sha256 for evidence in provider_crosschecks}
    if evidence_hashes != raw_hashes or len(provider_crosschecks) != len(ordered_archives):
        raise ValueError("trusted promotion requires exactly one provider cross-check per archive")
    for evidence in provider_crosschecks:
        if (
            evidence.provider != metadata.provider
            or evidence.venue != metadata.venue
            or evidence.symbol != metadata.symbol
        ):
            raise ValueError("provider cross-check identity does not match instrument metadata")

    h1_bars = build_h1(minute_bars)
    d1_bars = build_complete_new_york_d1(h1_bars)
    raw_artifacts = tuple(
        RawArtifact(
            archive_date=archive.archive_date,
            filename=archive.filename,
            source_url=archive.source_url,
            checksum_url=archive.checksum_url,
            sha256=archive.sha256,
            content=archive.content,
        )
        for archive in ordered_archives
    )
    manifest = build_manifest(
        metadata=metadata,
        raw_artifacts=raw_artifacts,
        provider_crosschecks=provider_crosschecks,
        m1_rows=len(minute_bars),
        h1=h1_bars,
        d1=d1_bars,
        code_version=code_version,
        dependency_lock_sha256=dependency_lock_sha256,
    )
    return TrustedDataset(
        metadata=metadata,
        raw_artifacts=raw_artifacts,
        provider_crosschecks=provider_crosschecks,
        minute_bars=minute_bars,
        h1_bars=h1_bars,
        d1_bars=d1_bars,
        manifest=manifest,
    )
