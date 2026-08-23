from __future__ import annotations

import csv
import hashlib
import io
import urllib.request
import zipfile
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from romeo_crt_engine.alpha_lab.models import Bar, Dataset

BASE_URL = "https://data.binance.vision/data/spot/monthly/klines"


def _month_start(value: date) -> date:
    return date(value.year, value.month, 1)


def _next_month(value: date) -> date:
    if value.month == 12:
        return date(value.year + 1, 1, 1)
    return date(value.year, value.month + 1, 1)


def _months(start: datetime, end: datetime) -> tuple[date, ...]:
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("dataset boundaries must be timezone-aware")
    if start >= end:
        raise ValueError("dataset start must be before end")
    current = _month_start(start.date())
    last = _month_start((end - timedelta(microseconds=1)).date())
    result: list[date] = []
    while current <= last:
        result.append(current)
        current = _next_month(current)
    return tuple(result)


def _read_url(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "romeo-crt-alpha-lab/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    if not isinstance(payload, bytes):
        raise TypeError("provider response must be bytes")
    return payload


def _download_verified(url: str, path: Path) -> str:
    checksum_path = path.with_suffix(path.suffix + ".CHECKSUM")
    checksum_url = url + ".CHECKSUM"

    if not checksum_path.exists():
        checksum_path.write_bytes(_read_url(checksum_url))
    checksum_text = checksum_path.read_text(encoding="utf-8").strip()
    expected = checksum_text.split()[0].lower()
    if len(expected) != 64:
        raise ValueError(f"invalid provider checksum for {url}")

    if not path.exists():
        path.write_bytes(_read_url(url))
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"checksum mismatch for {path.name}: {actual} != {expected}")
    return actual


def _timestamp_utc(raw: str) -> datetime:
    value = int(raw)
    divisor = 1_000_000.0 if value >= 10**15 else 1_000.0
    return datetime.fromtimestamp(value / divisor, tz=UTC)


def _parse_zip(path: Path, start: datetime, end: datetime) -> list[Bar]:
    bars: list[Bar] = []
    with zipfile.ZipFile(path) as archive:
        members = [name for name in archive.namelist() if name.endswith(".csv")]
        if len(members) != 1:
            raise ValueError(f"expected one CSV member in {path.name}")
        with archive.open(members[0]) as binary:
            text = io.TextIOWrapper(binary, encoding="utf-8", newline="")
            for row in csv.reader(text):
                if len(row) < 6:
                    raise ValueError(f"invalid kline row in {path.name}")
                open_time = _timestamp_utc(row[0])
                if open_time < start or open_time >= end:
                    continue
                bars.append(
                    Bar(
                        open_time=open_time,
                        open=float(row[1]),
                        high=float(row[2]),
                        low=float(row[3]),
                        close=float(row[4]),
                        volume=float(row[5]),
                    )
                )
    return bars


def _dataset_hash(bars: tuple[Bar, ...], source_hashes: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    for source_hash in source_hashes:
        digest.update(source_hash.encode("ascii"))
        digest.update(b"\n")
    for bar in bars:
        row = (
            f"{bar.open_time.isoformat()}|{bar.open:.12g}|{bar.high:.12g}|{bar.low:.12g}|"
            f"{bar.close:.12g}|{bar.volume:.12g}\n"
        )
        digest.update(row.encode("utf-8"))
    return digest.hexdigest()


def load_binance_h1(
    *,
    symbol: str,
    start: datetime,
    end: datetime,
    cache_dir: Path,
) -> Dataset:
    """Download checksum-verified Binance H1 monthly archives for a bounded research window."""
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("dataset boundaries must be timezone-aware")
    start_utc = start.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    if start_utc >= end_utc:
        raise ValueError("dataset start must be before end")

    cache_dir.mkdir(parents=True, exist_ok=True)
    bars: list[Bar] = []
    hashes: list[str] = []
    for month in _months(start_utc, end_utc):
        filename = f"{symbol}-1h-{month.year:04d}-{month.month:02d}.zip"
        url = f"{BASE_URL}/{symbol}/1h/{filename}"
        path = cache_dir / filename
        hashes.append(_download_verified(url, path))
        bars.extend(_parse_zip(path, start_utc, end_utc))

    bars.sort(key=lambda item: item.open_time)
    for index in range(1, len(bars)):
        if bars[index].open_time <= bars[index - 1].open_time:
            raise ValueError("downloaded H1 bars are not strictly ordered and unique")
    if not bars:
        raise ValueError("dataset contains no bars")

    frozen_bars = tuple(bars)
    frozen_hashes = tuple(hashes)
    return Dataset(
        symbol=symbol,
        start=start_utc,
        end=end_utc,
        bars=frozen_bars,
        dataset_sha256=_dataset_hash(frozen_bars, frozen_hashes),
        source_hashes=frozen_hashes,
    )
