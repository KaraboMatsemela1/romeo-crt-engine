from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class SourceRegistryRowV1:
    source_id: str
    title: str
    url: str
    published_date: str
    duration: str
    source_type: str
    relevance: str
    status: str
    concepts: str
    notes: str

    def __post_init__(self) -> None:
        required = (
            self.source_id,
            self.title,
            self.url,
            self.source_type,
            self.relevance,
            self.status,
        )
        if any(not value.strip() for value in required):
            raise ValueError("source registry required fields must not be empty")
        parsed = urlparse(self.url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("source registry URL must be an absolute HTTPS URL")


_REQUIRED_COLUMNS = (
    "source_id",
    "title",
    "url",
    "published_date",
    "duration",
    "source_type",
    "relevance",
    "status",
    "concepts",
    "notes",
)


def load_source_registry_v1(path: Path) -> tuple[SourceRegistryRowV1, ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or tuple(reader.fieldnames) != _REQUIRED_COLUMNS:
            raise ValueError("unexpected source registry columns")
        rows = tuple(
            SourceRegistryRowV1(**{column: raw[column] for column in _REQUIRED_COLUMNS})
            for raw in reader
        )
    identifiers = [row.source_id for row in rows]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("source registry IDs must be unique")
    return rows
