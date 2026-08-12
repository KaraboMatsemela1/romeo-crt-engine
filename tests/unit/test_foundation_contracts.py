from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path

import pytest

from romeo_crt_engine.logging_config import log_event
from romeo_crt_engine.storage import ArtifactRef, DatasetRef, LocalArtifactStore


def test_log_event_emits_structured_json(caplog: pytest.LogCaptureFixture) -> None:
    logger = logging.getLogger("romeo_crt_engine.test")
    with caplog.at_level(logging.INFO, logger=logger.name):
        log_event(logger, "dataset.created", fields={"dataset_version": "v1", "rows": 42})

    assert '"event":"dataset.created"' in caplog.text
    assert '"dataset_version":"v1"' in caplog.text
    assert '"rows":42' in caplog.text


def test_log_event_rejects_event_field_override() -> None:
    logger = logging.getLogger("romeo_crt_engine.test")
    with pytest.raises(ValueError, match="reserved"):
        log_event(logger, "dataset.created", fields={"event": "spoofed"})


def test_artifact_ref_requires_valid_sha256() -> None:
    with pytest.raises(ValueError, match="64-character"):
        ArtifactRef("file:///tmp/a", "bad", 1, "application/octet-stream")


def test_dataset_ref_requires_timezone_aware_created_at() -> None:
    digest = "a" * 64
    naive_created_at = datetime(2026, 8, 12, tzinfo=UTC).replace(tzinfo=None)
    with pytest.raises(ValueError, match="timezone-aware"):
        DatasetRef("prices", "v1", digest, naive_created_at)


def test_dataset_ref_accepts_versioned_integrity_metadata() -> None:
    digest = "b" * 64
    ref = DatasetRef("prices", "v1", digest, datetime(2026, 8, 12, tzinfo=UTC))
    assert ref.dataset_id == "prices"
    assert ref.manifest_sha256 == digest


def test_local_artifact_store_round_trip_is_integrity_checked(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path)
    ref = store.put_bytes("raw/example.bin", b"immutable", "application/octet-stream")

    assert store.read_bytes(ref) == b"immutable"
    assert ref.size_bytes == len(b"immutable")


def test_local_artifact_store_rejects_mutation_and_path_traversal(tmp_path: Path) -> None:
    store = LocalArtifactStore(tmp_path)
    store.put_bytes("raw/example.bin", b"first", "application/octet-stream")

    with pytest.raises(ValueError, match="different bytes"):
        store.put_bytes("raw/example.bin", b"second", "application/octet-stream")
    with pytest.raises(ValueError, match="relative path"):
        store.put_bytes("../escape.bin", b"bad", "application/octet-stream")
