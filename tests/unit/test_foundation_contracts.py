from __future__ import annotations

import logging
from datetime import UTC, datetime

import pytest

from romeo_crt_engine.logging_config import log_event
from romeo_crt_engine.storage import ArtifactRef, DatasetRef


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
    with pytest.raises(ValueError, match="timezone-aware"):
        DatasetRef("prices", "v1", digest, datetime(2026, 8, 12))


def test_dataset_ref_accepts_versioned_integrity_metadata() -> None:
    digest = "b" * 64
    ref = DatasetRef("prices", "v1", digest, datetime(2026, 8, 12, tzinfo=UTC))
    assert ref.dataset_id == "prices"
    assert ref.manifest_sha256 == digest
