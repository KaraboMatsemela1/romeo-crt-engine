from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


@dataclass(frozen=True, slots=True)
class CorpusEntryV1:
    source_id: str
    manifest_sha256: str
    artifact_sha256s: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("corpus source_id must not be empty")
        if not _is_sha256(self.manifest_sha256):
            raise ValueError("manifest_sha256 must be a lowercase SHA-256 digest")
        if not self.artifact_sha256s:
            raise ValueError("corpus entry must bind at least one artifact")
        if any(not _is_sha256(value) for value in self.artifact_sha256s):
            raise ValueError("artifact_sha256s must contain lowercase SHA-256 digests")
        if len(set(self.artifact_sha256s)) != len(self.artifact_sha256s):
            raise ValueError("artifact_sha256s must be unique within an entry")


@dataclass(frozen=True, slots=True)
class CorpusIndexV1:
    entries: tuple[CorpusEntryV1, ...]

    def __post_init__(self) -> None:
        manifest_hashes = [entry.manifest_sha256 for entry in self.entries]
        if len(manifest_hashes) != len(set(manifest_hashes)):
            raise ValueError("corpus manifest hashes must be unique")

    def canonical_record(self) -> dict[str, object]:
        entries = sorted(self.entries, key=lambda item: (item.source_id, item.manifest_sha256))
        return {
            "schema_version": "P6D_EVIDENCE_CORPUS_INDEX_V1",
            "entries": [
                {
                    "source_id": entry.source_id,
                    "manifest_sha256": entry.manifest_sha256,
                    "artifact_sha256s": sorted(entry.artifact_sha256s),
                }
                for entry in entries
            ],
        }

    def digest(self) -> str:
        encoded = json.dumps(
            self.canonical_record(), sort_keys=True, separators=(",", ":")
        ).encode()
        return sha256(encoded).hexdigest()
