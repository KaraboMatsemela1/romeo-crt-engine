from __future__ import annotations

import argparse
import csv
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from functools import partial
from hashlib import sha256
from io import BytesIO, TextIOWrapper
from itertools import pairwise
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from romeo_crt_engine.market_data.dataset import write_dataset
from romeo_crt_engine.market_data.pipeline import build_trusted_binance_dataset
from romeo_crt_engine.market_data.providers.binance_public import (
    RawArchive,
    fetch_daily_archive,
    fetch_exchange_info,
    parse_1m_archive,
)
from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError
from romeo_crt_engine.market_data.verification import (
    VerificationPolicy,
    build_provider_verification_evidence,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARKET_DATA_ROOT = PROJECT_ROOT / "src" / "romeo_crt_engine" / "market_data"
ARCHIVE_EXCLUSION_POLICY_ID = "P6-DATA-QUALITY-AMENDMENT-002"
ARCHIVE_EXCLUSION_SCHEMA = "P6_ARCHIVE_EXCLUSIONS_V1"


@dataclass(frozen=True, slots=True)
class ArchiveExclusionDiagnostic:
    archive_date: date
    filename: str
    source_sha256: str
    error_code: str
    diagnostic: str

    def to_record(self) -> dict[str, str]:
        return {
            "archive_date": self.archive_date.isoformat(),
            "filename": self.filename,
            "source_sha256": self.source_sha256,
            "error_code": self.error_code,
            "diagnostic": self.diagnostic,
        }


def _date(value: str) -> date:
    return date.fromisoformat(value)


def _git_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    return result.stdout.strip()


def _file_digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _market_data_code_digest() -> str:
    digest = sha256()
    files = sorted(MARKET_DATA_ROOT.rglob("*.py"))
    if not files:
        raise RuntimeError("market-data source files not found")
    for path in files:
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _days(start: date, end: date) -> tuple[date, ...]:
    if end < start:
        raise ValueError("end must be >= start")
    count = (end - start).days + 1
    return tuple(start + timedelta(days=offset) for offset in range(count))


def _fetch_archives(
    symbol: str,
    days: tuple[date, ...],
    *,
    workers: int,
) -> tuple[RawArchive, ...]:
    if workers <= 0:
        raise ValueError("download workers must be > 0")
    fetch = partial(fetch_daily_archive, symbol)
    if workers == 1:
        return tuple(fetch(day) for day in days)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return tuple(executor.map(fetch, days))


def _diagnostic_timestamp(value: int) -> datetime:
    scale = 1_000_000 if value >= 10**15 else 1_000
    seconds, remainder = divmod(value, scale)
    microseconds = remainder * (1_000_000 // scale)
    return datetime.fromtimestamp(seconds, UTC).replace(microsecond=microseconds)


def _archive_chronology_diagnostic(archive: RawArchive) -> str:
    """Describe authenticated provider chronology without accepting it as trusted market data."""
    try:
        with ZipFile(BytesIO(archive.content)) as zipped:
            csv_names = [name for name in zipped.namelist() if name.lower().endswith(".csv")]
            if len(csv_names) != 1:
                return f"csv_count={len(csv_names)}"
            with zipped.open(csv_names[0]) as raw_file:
                rows = list(csv.reader(TextIOWrapper(raw_file, encoding="utf-8", newline="")))
    except BadZipFile:
        return "invalid_zip=true"

    day_start = datetime.combine(archive.archive_date, datetime.min.time(), tzinfo=UTC)
    day_end = day_start + timedelta(days=1)
    opens: list[datetime] = []
    irregular_rows: list[str] = []
    malformed_rows: list[str] = []

    for row_number, row in enumerate(rows, start=1):
        if len(row) != 12:
            malformed_rows.append(f"row={row_number}:columns={len(row)}")
            continue
        try:
            raw_open = int(row[0])
            raw_close = int(row[6])
        except ValueError:
            malformed_rows.append(f"row={row_number}:invalid_timestamp")
            continue
        scale = 1_000_000 if raw_open >= 10**15 else 1_000
        open_time = _diagnostic_timestamp(raw_open)
        opens.append(open_time)
        expected_close = raw_open + (60 * scale) - 1
        if raw_close != expected_close:
            duration_seconds = (raw_close - raw_open + 1) / scale
            irregular_rows.append(
                f"row={row_number}:open={open_time.isoformat()}:duration_seconds={duration_seconds}"
            )

    gaps: list[str] = []
    if opens:
        if opens[0] > day_start:
            missing = int((opens[0] - day_start).total_seconds() // 60)
            gaps.append(f"{day_start.isoformat()}..{opens[0].isoformat()}:{missing}m")
        for previous, current in pairwise(opens):
            expected = previous + timedelta(minutes=1)
            if current > expected:
                missing = int((current - expected).total_seconds() // 60)
                gaps.append(f"{expected.isoformat()}..{current.isoformat()}:{missing}m")
            elif current < expected:
                gaps.append(f"overlap:{previous.isoformat()}->{current.isoformat()}")
        expected_after_last = opens[-1] + timedelta(minutes=1)
        if expected_after_last < day_end:
            missing = int((day_end - expected_after_last).total_seconds() // 60)
            gaps.append(f"{expected_after_last.isoformat()}..{day_end.isoformat()}:{missing}m")

    parts = [f"rows={len(rows)}"]
    if opens:
        parts.extend((f"first={opens[0].isoformat()}", f"last={opens[-1].isoformat()}"))
    if gaps:
        parts.append("gaps=[" + ";".join(gaps) + "]")
    if irregular_rows:
        parts.append("irregular=[" + ";".join(irregular_rows) + "]")
    if malformed_rows:
        parts.append("malformed=[" + ";".join(malformed_rows) + "]")
    return " ".join(parts)


def _classify_archive_exclusions(
    archives: tuple[RawArchive, ...],
    *,
    symbol: str,
) -> tuple[frozenset[str], tuple[ArchiveExclusionDiagnostic, ...]]:
    """Conservatively exclude authenticated daily archives that fail the strict parser."""
    exclusions: list[ArchiveExclusionDiagnostic] = []
    allowed_codes = {DataQualityCode.INCOMPLETE_BUCKET, DataQualityCode.PROVIDER_SCHEMA}
    for archive in archives:
        try:
            parse_1m_archive(archive, symbol=symbol)
        except DataQualityError as error:
            if error.code not in allowed_codes:
                raise
            exclusions.append(
                ArchiveExclusionDiagnostic(
                    archive_date=archive.archive_date,
                    filename=archive.filename,
                    source_sha256=archive.sha256,
                    error_code=error.code.value,
                    diagnostic=_archive_chronology_diagnostic(archive),
                )
            )
    return frozenset(item.source_sha256 for item in exclusions), tuple(exclusions)


def _exclusion_ledger(
    diagnostics: tuple[ArchiveExclusionDiagnostic, ...],
) -> tuple[str, str]:
    payload = {
        "schema_version": ARCHIVE_EXCLUSION_SCHEMA,
        "policy_id": ARCHIVE_EXCLUSION_POLICY_ID,
        "records": [item.to_record() for item in diagnostics],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return encoded, sha256(encoded.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a trusted BTCUSDT-style dataset from Binance daily 1m archives."
    )
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--start-utc-day", type=_date, required=True)
    parser.add_argument("--end-utc-day", type=_date, required=True)
    parser.add_argument("--data-root", type=Path, default=PROJECT_ROOT / "data")
    parser.add_argument("--lock-file", type=Path, default=PROJECT_ROOT / "requirements.lock")
    parser.add_argument(
        "--verification-policy",
        choices=[policy.value for policy in VerificationPolicy],
        default=VerificationPolicy.REST_EVERY_ARCHIVE.value,
        help=(
            "Provider verification contract. The default preserves Phase-3 REST verification "
            "for every strict-parser-eligible archive; validation windows may use "
            "checksum-all-rest-monthly."
        ),
    )
    parser.add_argument(
        "--download-workers",
        type=int,
        default=1,
        help="Concurrent Binance archive downloads. Output ordering remains chronological.",
    )
    args = parser.parse_args()

    retrieved_at = datetime.now(UTC)
    git_revision = _git_sha()
    metadata = fetch_exchange_info(args.symbol, observed_at=retrieved_at)
    requested_days = _days(args.start_utc_day, args.end_utc_day)
    archives = _fetch_archives(
        args.symbol,
        requested_days,
        workers=args.download_workers,
    )
    excluded_source_hashes, exclusion_diagnostics = _classify_archive_exclusions(
        archives,
        symbol=args.symbol,
    )
    exclusion_json, exclusion_sha = _exclusion_ledger(exclusion_diagnostics)

    policy = VerificationPolicy(args.verification_policy)
    provider_crosschecks = build_provider_verification_evidence(
        archives,
        symbol=args.symbol,
        policy=policy,
        excluded_source_hashes=excluded_source_hashes,
    )

    dataset = build_trusted_binance_dataset(
        archives=archives,
        provider_crosschecks=provider_crosschecks,
        metadata=metadata,
        market_data_code_sha256=_market_data_code_digest(),
        dependency_lock_sha256=_file_digest(args.lock_file),
        git_revision=git_revision,
        created_at=retrieved_at,
        excluded_source_hashes=excluded_source_hashes,
    )
    output = write_dataset(
        root=args.data_root,
        raw_artifacts=dataset.raw_artifacts,
        h1=dataset.h1_bars,
        d1=dataset.d1_bars,
        manifest=dataset.manifest,
        receipt=dataset.receipt,
    )
    print(f"dataset_version={dataset.manifest.dataset_version}")
    print(f"manifest_sha256={dataset.manifest.manifest_sha256}")
    print(f"receipt_sha256={dataset.receipt.receipt_sha256}")
    print(f"git_revision={dataset.receipt.git_revision}")
    print(f"verification_policy={policy.value}")
    print(f"archive_count={len(archives)}")
    print(f"excluded_archive_count={len(exclusion_diagnostics)}")
    print(f"exclusion_ledger_sha256={exclusion_sha}")
    print(f"archive_exclusions_json={exclusion_json}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
