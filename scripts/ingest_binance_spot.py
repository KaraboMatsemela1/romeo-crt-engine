from __future__ import annotations

import argparse
import subprocess
from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from pathlib import Path

from romeo_crt_engine.market_data.dataset import write_dataset
from romeo_crt_engine.market_data.pipeline import build_trusted_binance_dataset
from romeo_crt_engine.market_data.providers.binance_public import (
    crosscheck_bars_with_rest,
    fetch_daily_archive,
    fetch_exchange_info,
    parse_1m_archive,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARKET_DATA_ROOT = PROJECT_ROOT / "src" / "romeo_crt_engine" / "market_data"


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a trusted BTCUSDT-style dataset from Binance daily 1m archives."
    )
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--start-utc-day", type=_date, required=True)
    parser.add_argument("--end-utc-day", type=_date, required=True)
    parser.add_argument("--data-root", type=Path, default=PROJECT_ROOT / "data")
    parser.add_argument("--lock-file", type=Path, default=PROJECT_ROOT / "requirements.lock")
    args = parser.parse_args()

    retrieved_at = datetime.now(UTC)
    git_revision = _git_sha()
    metadata = fetch_exchange_info(args.symbol, observed_at=retrieved_at)
    archives = tuple(
        fetch_daily_archive(args.symbol, day)
        for day in _days(args.start_utc_day, args.end_utc_day)
    )
    provider_crosschecks = tuple(
        crosscheck_bars_with_rest(parse_1m_archive(archive, symbol=args.symbol))
        for archive in archives
    )

    dataset = build_trusted_binance_dataset(
        archives=archives,
        provider_crosschecks=provider_crosschecks,
        metadata=metadata,
        market_data_code_sha256=_market_data_code_digest(),
        dependency_lock_sha256=_file_digest(args.lock_file),
        git_revision=git_revision,
        created_at=retrieved_at,
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
    print(f"output={output}")


if __name__ == "__main__":
    main()
