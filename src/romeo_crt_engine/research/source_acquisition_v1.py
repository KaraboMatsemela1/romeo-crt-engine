from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from urllib.parse import urlparse

SOURCE_ACQUISITION_SCHEMA_VERSION = "P6D_FIRST_PARTY_SOURCE_ACQUISITION_V1"


class SourceKind(StrEnum):
    YOUTUBE = "YOUTUBE"
    TELEGRAM = "TELEGRAM"
    FIRST_PARTY_WEB = "FIRST_PARTY_WEB"
    OTHER_FIRST_PARTY = "OTHER_FIRST_PARTY"


class CaptureKind(StrEnum):
    METADATA = "METADATA"
    TEXT = "TEXT"
    CAPTIONS = "CAPTIONS"
    TRANSCRIPT = "TRANSCRIPT"
    FRAME = "FRAME"
    CHART = "CHART"


class AcquisitionStatus(StrEnum):
    CAPTURED = "CAPTURED"
    PARTIAL = "PARTIAL"
    UNAVAILABLE = "UNAVAILABLE"


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def _canonical_json_bytes(record: dict[str, object]) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode()


@dataclass(frozen=True, slots=True)
class SourceIdentityV1:
    source_id: str
    url: str
    source_kind: SourceKind
    provenance_statement: str
    first_party: bool = True

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must not be empty")
        parsed = urlparse(self.url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("source URL must be an absolute HTTPS URL")
        if not self.first_party:
            raise ValueError("Phase-6D acquisition accepts first-party sources only")
        if not self.provenance_statement.strip():
            raise ValueError("provenance_statement must not be empty")


@dataclass(frozen=True, slots=True)
class SourceArtifactV1:
    source_id: str
    capture_kind: CaptureKind
    retrieved_at: datetime
    payload_sha256: str
    byte_length: int
    content_type: str
    locator: str
    first_party_verified: bool

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("artifact source_id must not be empty")
        if self.retrieved_at.utcoffset() is None:
            raise ValueError("retrieved_at must be timezone-aware")
        if not _is_sha256(self.payload_sha256):
            raise ValueError("payload_sha256 must be a lowercase SHA-256 digest")
        if self.byte_length < 0:
            raise ValueError("byte_length must be non-negative")
        if not self.content_type.strip():
            raise ValueError("content_type must not be empty")
        if not self.locator.strip():
            raise ValueError("locator must not be empty")
        if not self.first_party_verified:
            raise ValueError("artifact must be directly verified as first-party")

    @classmethod
    def from_bytes(
        cls,
        *,
        source_id: str,
        capture_kind: CaptureKind,
        payload: bytes,
        content_type: str,
        locator: str,
        retrieved_at: datetime | None = None,
    ) -> SourceArtifactV1:
        observed_at = retrieved_at or datetime.now(UTC)
        return cls(
            source_id=source_id,
            capture_kind=capture_kind,
            retrieved_at=observed_at,
            payload_sha256=sha256(payload).hexdigest(),
            byte_length=len(payload),
            content_type=content_type,
            locator=locator,
            first_party_verified=True,
        )


@dataclass(frozen=True, slots=True)
class SourceAcquisitionManifestV1:
    source: SourceIdentityV1
    status: AcquisitionStatus
    artifacts: tuple[SourceArtifactV1, ...]
    notes: str
    schema_version: str = SOURCE_ACQUISITION_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SOURCE_ACQUISITION_SCHEMA_VERSION:
            raise ValueError("unsupported source-acquisition schema")
        if any(artifact.source_id != self.source.source_id for artifact in self.artifacts):
            raise ValueError("all artifacts must belong to the manifest source")
        artifact_keys = {(artifact.capture_kind, artifact.locator) for artifact in self.artifacts}
        if len(artifact_keys) != len(self.artifacts):
            raise ValueError("duplicate capture_kind/locator artifact")
        if self.status is AcquisitionStatus.CAPTURED and not self.artifacts:
            raise ValueError("CAPTURED status requires at least one artifact")
        if self.status is AcquisitionStatus.UNAVAILABLE and self.artifacts:
            raise ValueError("UNAVAILABLE status cannot contain captured artifacts")
        if not self.notes.strip():
            raise ValueError("manifest notes must not be empty")

    def canonical_record(self) -> dict[str, object]:
        artifacts = sorted(
            self.artifacts,
            key=lambda item: (item.capture_kind.value, item.locator, item.payload_sha256),
        )
        return {
            "schema_version": self.schema_version,
            "source": {
                "source_id": self.source.source_id,
                "url": self.source.url,
                "source_kind": self.source.source_kind.value,
                "provenance_statement": self.source.provenance_statement,
                "first_party": self.source.first_party,
            },
            "status": self.status.value,
            "artifacts": [
                {
                    "source_id": artifact.source_id,
                    "capture_kind": artifact.capture_kind.value,
                    "retrieved_at_utc": artifact.retrieved_at.astimezone(UTC).isoformat(),
                    "payload_sha256": artifact.payload_sha256,
                    "byte_length": artifact.byte_length,
                    "content_type": artifact.content_type,
                    "locator": artifact.locator,
                    "first_party_verified": artifact.first_party_verified,
                }
                for artifact in artifacts
            ],
            "notes": self.notes,
        }

    def digest(self) -> str:
        return sha256(_canonical_json_bytes(self.canonical_record())).hexdigest()
