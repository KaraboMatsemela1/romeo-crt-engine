from __future__ import annotations

from enum import StrEnum

from romeo_crt_engine.market_data.models import ProviderVerificationEvidence
from romeo_crt_engine.market_data.providers.binance_public import (
    ARCHIVE_BASE_URL,
    PROVIDER,
    VENUE,
    RawArchive,
    crosscheck_bars_with_rest,
    parse_1m_archive,
)

CHECKSUM_VERIFICATION_METHOD = "PROVIDER_SHA256_CHECKSUM_V1"


class VerificationPolicy(StrEnum):
    REST_EVERY_ARCHIVE = "rest-every-archive"
    CHECKSUM_ALL_REST_MONTHLY = "checksum-all-rest-monthly"


def monthly_rest_sample_hashes(
    archives: tuple[RawArchive, ...],
    *,
    excluded_source_hashes: frozenset[str] = frozenset(),
) -> frozenset[str]:
    """Select the first strict-parser-eligible archive present in each UTC month."""
    if not archives:
        return frozenset()
    selected: dict[tuple[int, int], RawArchive] = {}
    for archive in sorted(archives, key=lambda item: item.archive_date):
        if archive.sha256 in excluded_source_hashes:
            continue
        key = (archive.archive_date.year, archive.archive_date.month)
        selected.setdefault(key, archive)
    return frozenset(archive.sha256 for archive in selected.values())


def checksum_verification_evidence(
    archive: RawArchive,
    *,
    symbol: str,
) -> ProviderVerificationEvidence:
    """Record provider-checksum evidence already verified by fetch_daily_archive()."""
    return ProviderVerificationEvidence(
        provider=PROVIDER,
        venue=VENUE,
        symbol=symbol.upper(),
        source_sha256=archive.sha256,
        sample_refs=(archive.checksum_url,),
        endpoint_base=ARCHIVE_BASE_URL,
        verification_method=CHECKSUM_VERIFICATION_METHOD,
    )


def build_provider_verification_evidence(
    archives: tuple[RawArchive, ...],
    *,
    symbol: str,
    policy: VerificationPolicy,
    excluded_source_hashes: frozenset[str] = frozenset(),
) -> tuple[ProviderVerificationEvidence, ...]:
    """Build exactly one auditable verification record per raw provider archive."""
    if not archives:
        raise ValueError("archives must not be empty")
    raw_hashes = frozenset(archive.sha256 for archive in archives)
    if not excluded_source_hashes <= raw_hashes:
        raise ValueError("excluded source hashes must belong to requested archives")

    monthly_rest_hashes = (
        monthly_rest_sample_hashes(
            archives,
            excluded_source_hashes=excluded_source_hashes,
        )
        if policy is VerificationPolicy.CHECKSUM_ALL_REST_MONTHLY
        else raw_hashes - excluded_source_hashes
    )

    evidence: list[ProviderVerificationEvidence] = []
    for archive in archives:
        if archive.sha256 in excluded_source_hashes:
            evidence.append(checksum_verification_evidence(archive, symbol=symbol))
        elif archive.sha256 in monthly_rest_hashes:
            bars = parse_1m_archive(archive, symbol=symbol)
            evidence.append(crosscheck_bars_with_rest(bars))
        else:
            evidence.append(checksum_verification_evidence(archive, symbol=symbol))
    return tuple(evidence)
