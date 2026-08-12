from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """Immutable reference to persisted bytes with integrity metadata."""

    uri: str
    sha256: str
    size_bytes: int
    media_type: str

    def __post_init__(self) -> None:
        if not self.uri:
            raise ValueError("uri must not be empty")
        if len(self.sha256) != 64:
            raise ValueError("sha256 must be a 64-character hexadecimal digest")
        try:
            int(self.sha256, 16)
        except ValueError as exc:
            raise ValueError("sha256 must be hexadecimal") from exc
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be >= 0")
        if not self.media_type:
            raise ValueError("media_type must not be empty")


@dataclass(frozen=True, slots=True)
class DatasetRef:
    """Versioned dataset identity used to reproduce research and validation runs."""

    dataset_id: str
    version: str
    manifest_sha256: str
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.dataset_id:
            raise ValueError("dataset_id must not be empty")
        if not self.version:
            raise ValueError("version must not be empty")
        if self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        if len(self.manifest_sha256) != 64:
            raise ValueError("manifest_sha256 must be a 64-character hexadecimal digest")
        try:
            int(self.manifest_sha256, 16)
        except ValueError as exc:
            raise ValueError("manifest_sha256 must be hexadecimal") from exc


class ArtifactStore(Protocol):
    """Storage boundary; Phase 3 may implement local, object-store, or database adapters."""

    def put_bytes(self, key: str, payload: bytes, media_type: str) -> ArtifactRef:
        """Persist bytes and return their immutable integrity reference."""
        ...

    def read_bytes(self, ref: ArtifactRef) -> bytes:
        """Read bytes for a previously persisted artifact reference."""
        ...
