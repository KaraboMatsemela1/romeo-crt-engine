from __future__ import annotations

import csv
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from romeo_crt_engine.research.source_acquisition_v1 import SourceIdentityV1, SourceKind


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


def _required_cell(raw: Mapping[str, str], key: str) -> str:
    try:
        return raw[key]
    except KeyError as exc:
        raise ValueError(f"source registry row is missing cell: {key}") from exc


def _row_from_mapping(raw: Mapping[str, str]) -> SourceRegistryRowV1:
    return SourceRegistryRowV1(
        source_id=_required_cell(raw, "source_id"),
        title=_required_cell(raw, "title"),
        url=_required_cell(raw, "url"),
        published_date=_required_cell(raw, "published_date"),
        duration=_required_cell(raw, "duration"),
        source_type=_required_cell(raw, "source_type"),
        relevance=_required_cell(raw, "relevance"),
        status=_required_cell(raw, "status"),
        concepts=_required_cell(raw, "concepts"),
        notes=_required_cell(raw, "notes"),
    )


def load_source_registry_v1(path: Path) -> tuple[SourceRegistryRowV1, ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = tuple(next(reader))
        except StopIteration as exc:
            raise ValueError("source registry must contain a header") from exc
        if header != _REQUIRED_COLUMNS:
            raise ValueError("unexpected source registry columns")

        parsed_rows: list[SourceRegistryRowV1] = []
        for line_number, values in enumerate(reader, start=2):
            if len(values) != len(_REQUIRED_COLUMNS):
                raise ValueError(
                    f"source registry row {line_number} has {len(values)} columns; "
                    f"expected {len(_REQUIRED_COLUMNS)}"
                )
            raw = dict(zip(_REQUIRED_COLUMNS, values, strict=True))
            parsed_rows.append(_row_from_mapping(raw))

    rows = tuple(parsed_rows)
    identifiers = [row.source_id for row in rows]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("source registry IDs must be unique")
    return rows


def get_registered_source_v1(
    rows: tuple[SourceRegistryRowV1, ...], source_id: str
) -> SourceRegistryRowV1:
    matches = tuple(row for row in rows if row.source_id == source_id)
    if len(matches) != 1:
        raise ValueError(f"source_id must resolve to exactly one registered source: {source_id}")
    return matches[0]


def source_identity_from_registry_v1(row: SourceRegistryRowV1) -> SourceIdentityV1:
    kind_by_type = {
        "youtube": SourceKind.YOUTUBE,
        "telegram": SourceKind.TELEGRAM,
    }
    source_kind = kind_by_type.get(row.source_type.lower(), SourceKind.OTHER_FIRST_PARTY)
    provenance = row.notes.strip() or f"Registered first-party source: {row.title}"
    return SourceIdentityV1(
        source_id=row.source_id,
        url=row.url,
        source_kind=source_kind,
        provenance_statement=provenance,
    )
