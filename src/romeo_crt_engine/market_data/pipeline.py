from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from romeo_crt_engine.market_data.aggregate import build_complete_new_york_d1, build_h1
from romeo_crt_engine.market_data.closures import archive_exclusion, closures_for
from romeo_crt_engine.market_data.dataset import (
    DatasetManifest,
    IngestionReceipt,
    RawArtifact,
    build_manifest,
    build_receipt,
)
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
    receipt: IngestionReceipt


def build_trusted_binance_dataset(
    *,
    archives: tuple[RawArchive, ...],
    provider_crosschecks: tuple[ProviderVerificationEvidence, ...],
    metadata: InstrumentMetadata,
    market_data_code_sha256: str,
    dependency_lock_sha256: str,
    git_revision: str,
    created_at: datetime,
    excluded_source_hashes: frozenset[str] = frozenset(),
) -> TrustedDataset:
    if not archives:
        raise ValueError("at least one archive is required")

    ordered_archives = tuple(sorted(archives, key=lambda archive: archive.archive_date))
    raw_hashes = {archive.sha256 for archive in ordered_archives}
    if not excluded_source_hashes <= raw_hashes:
        raise ValueError("excluded source hashes must belong to requested archives")
    usable_archives = tuple(
        archive for archive in ordered_archives if archive.sha256 not in excluded_source_hashes
    )
    if not usable_archives:
        raise ValueError("trusted dataset requires at least one strict-parser-eligible archive")

    closures = closures_for(
        provider=metadata.provider,
        venue=metadata.venue,
        symbol=metadata.symbol,
    )
    exclusions = tuple(
        archive_exclusion(
            provider=metadata.provider,
            venue=metadata.venue,
            symbol=metadata.symbol,
            archive_date=archive.archive_date,
            source_sha256=archive.sha256,
        )
        for archive in ordered_archives
        if archive.sha256 in excluded_source_hashes
    )
    allowed_gaps = (*closures, *exclusions)

    minute_parts = [parse_1m_archive(archive, symbol=metadata.symbol) for archive in usable_archives]
    minute_bars = tuple(bar for part in minute_parts for bar in part)
    validate_minute_series(minute_bars, as_of=created_at, allowed_closures=allowed_gaps)

    evidence_hashes = {evidence.source_sha256 for evidence in provider_crosschecks}
    if evidence_hashes != raw_hashes or len(provider_crosschecks) != len(ordered_archives):
        raise ValueError(
            "trusted promotion requires exactly one provider cross-check/verification per archive"
        )
    for evidence in provider_crosschecks:
        if (
            evidence.provider != metadata.provider
            or evidence.venue != metadata.venue
            or evidence.symbol != metadata.symbol
        ):
            raise ValueError("provider cross-check identity does not match instrument metadata")

    h1_bars = build_h1(minute_bars, allowed_closures=allowed_gaps)
    d1_bars = build_complete_new_york_d1(h1_bars, allowed_closures=allowed_gaps)
    raw_artifacts = tuple(
        RawArtifact(
            archive_date=archive.archive_date.isoformat(),
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
        market_data_code_sha256=market_data_code_sha256,
        dependency_lock_sha256=dependency_lock_sha256,
    )
    receipt = build_receipt(
        manifest=manifest,
        raw_artifacts=raw_artifacts,
        provider_crosschecks=provider_crosschecks,
        retrieved_at=created_at,
        git_revision=git_revision,
    )
    return TrustedDataset(
        metadata=metadata,
        raw_artifacts=raw_artifacts,
        provider_crosschecks=provider_crosschecks,
        minute_bars=minute_bars,
        h1_bars=h1_bars,
        d1_bars=d1_bars,
        manifest=manifest,
        receipt=receipt,
    )
