from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from typing import Any, cast

from romeo_crt_engine.market_data.dataset import write_dataset
from romeo_crt_engine.market_data.models import AssetClass, InstrumentMetadata
from romeo_crt_engine.market_data.pipeline import build_trusted_binance_dataset
from romeo_crt_engine.market_data.providers.binance_public import (
    PROVIDER,
    VENUE,
    crosscheck_bars_with_rest,
    fetch_daily_archive,
    parse_1m_archive,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARKET_DATA_ROOT = PROJECT_ROOT / "src" / "romeo_crt_engine" / "market_data"
DEFAULT_MANIFEST = (
    PROJECT_ROOT
    / "data"
    / "manifests"
    / "PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7.json"
)


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


def _document(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("frozen dataset manifest must be a JSON object")
    return cast(dict[str, Any], raw)


def _metadata(document: dict[str, Any]) -> InstrumentMetadata:
    if document.get("provider") != PROVIDER or document.get("venue") != VENUE:
        raise ValueError("reconstruction currently supports the frozen Binance Spot route only")
    return InstrumentMetadata(
        provider=str(document["provider"]),
        venue=str(document["venue"]),
        symbol=str(document["symbol"]),
        asset_class=AssetClass(str(document["asset_class"])),
        price_tick_size=Decimal(str(document["price_tick_size"])),
        quantity_step=Decimal(str(document["quantity_step"])),
        observed_at=datetime.fromisoformat(str(document["instrument_metadata_observed_at"])),
        metadata_version=str(document["instrument_metadata_version"]),
        temporal_semantics=str(document["metadata_temporal_semantics"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstruct an exact frozen Phase-3 dataset from its committed manifest."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--data-root", type=Path, default=PROJECT_ROOT / "data")
    parser.add_argument("--lock-file", type=Path, default=PROJECT_ROOT / "requirements.lock")
    args = parser.parse_args()

    manifest_bytes = args.manifest.read_bytes()
    expected_manifest_sha = sha256(manifest_bytes).hexdigest()
    document = _document(args.manifest)
    metadata = _metadata(document)
    raw_records = document.get("raw_artifacts")
    if not isinstance(raw_records, list) or not raw_records:
        raise ValueError("frozen manifest raw_artifacts must be a non-empty list")

    archives = tuple(
        fetch_daily_archive(metadata.symbol, datetime.fromisoformat(str(record["archive_date"])).date())
        for record in raw_records
        if isinstance(record, dict)
    )
    if len(archives) != len(raw_records):
        raise ValueError("invalid raw artifact record in frozen manifest")

    expected_raw_hashes = tuple(str(record["sha256"]) for record in raw_records)
    observed_raw_hashes = tuple(archive.sha256 for archive in archives)
    if observed_raw_hashes != expected_raw_hashes:
        raise ValueError("provider raw artifact hash drifted from frozen manifest")

    crosschecks = tuple(
        crosscheck_bars_with_rest(parse_1m_archive(archive, symbol=metadata.symbol))
        for archive in archives
    )
    retrieved_at = datetime.now(UTC)
    dataset = build_trusted_binance_dataset(
        archives=archives,
        provider_crosschecks=crosschecks,
        metadata=metadata,
        market_data_code_sha256=_market_data_code_digest(),
        dependency_lock_sha256=_file_digest(args.lock_file),
        git_revision=_git_sha(),
        created_at=retrieved_at,
    )

    expected_version = str(document["dataset_version"])
    if dataset.manifest.dataset_version != expected_version:
        raise ValueError(
            f"dataset reconstruction drift: {dataset.manifest.dataset_version} != {expected_version}"
        )
    if dataset.manifest.manifest_sha256 != expected_manifest_sha:
        raise ValueError(
            "reconstructed canonical manifest bytes do not match the committed frozen manifest"
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
    print(f"output={output}")


if __name__ == "__main__":
    main()
