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


def _date(value: str) -> date:
    return date.fromisoformat(value)


def _git_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _lock_digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


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
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--lock-file", type=Path, default=Path("requirements.lock"))
    args = parser.parse_args()

    created_at = datetime.now(UTC)
    metadata = fetch_exchange_info(args.symbol, observed_at=created_at)
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
        code_version=_git_sha(),
        dependency_lock_sha256=_lock_digest(args.lock_file),
        created_at=created_at,
    )
    output = write_dataset(
        root=args.data_root,
        raw_artifacts=dataset.raw_artifacts,
        h1=dataset.h1_bars,
        d1=dataset.d1_bars,
        manifest=dataset.manifest,
    )
    print(f"dataset_version={dataset.manifest.dataset_version}")
    print(f"manifest_sha256={dataset.manifest.manifest_sha256}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
