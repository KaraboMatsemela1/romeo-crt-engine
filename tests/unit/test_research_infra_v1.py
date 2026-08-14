from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from romeo_crt_engine.research.corpus_index_v1 import CorpusEntryV1, CorpusIndexV1
from romeo_crt_engine.research.doctrine_diff_v1 import (
    DoctrineDeltaClassification,
    DoctrineStatementV1,
    record_doctrine_delta,
)
from romeo_crt_engine.research.fixture_gate_v1 import (
    FixtureKind,
    PredicateFixtureV1,
    assert_fixture_gate,
)
from romeo_crt_engine.research.predicate_ledger_v1 import (
    PredicateEvidenceV1,
    PredicateField,
    PredicateLedgerRowV1,
    PredicateLedgerV1,
    PredicateStatus,
)
from romeo_crt_engine.research.registry_v1 import load_source_registry_v1
from romeo_crt_engine.research.source_acquisition_v1 import (
    AcquisitionStatus,
    CaptureKind,
    SourceAcquisitionManifestV1,
    SourceArtifactV1,
    SourceIdentityV1,
    SourceKind,
)


def _source() -> SourceIdentityV1:
    return SourceIdentityV1(
        source_id="ROMEO-TEST",
        url="https://example.com/source",
        source_kind=SourceKind.FIRST_PARTY_WEB,
        provenance_statement="Direct Romeo publication.",
    )


def _artifact(kind: CaptureKind, payload: bytes, locator: str) -> SourceArtifactV1:
    return SourceArtifactV1.from_bytes(
        source_id="ROMEO-TEST",
        capture_kind=kind,
        payload=payload,
        content_type="text/plain",
        locator=locator,
        retrieved_at=datetime(2026, 8, 14, 12, 0, tzinfo=UTC),
    )


def _closed_predicate(predicate_id: str = "PREDICATE") -> PredicateLedgerRowV1:
    fields = tuple(PredicateField)
    evidence = tuple(
        PredicateEvidenceV1(
            field=field,
            source_id="ROMEO-TEST",
            locator=f"00:00-{field.value}",
            artifact_sha256="a" * 64,
            statement=f"Direct evidence for {field.value}",
            first_party_verified=True,
        )
        for field in fields
    )
    return PredicateLedgerRowV1(
        predicate_id=predicate_id,
        description="Fully closed test predicate",
        required_fields=fields,
        evidence=evidence,
    )


def test_source_manifest_digest_is_order_independent() -> None:
    first = _artifact(CaptureKind.TEXT, b"alpha", "post:1")
    second = _artifact(CaptureKind.CAPTIONS, b"beta", "00:00-00:05")
    manifest_a = SourceAcquisitionManifestV1(
        source=_source(),
        status=AcquisitionStatus.CAPTURED,
        artifacts=(first, second),
        notes="Direct capture.",
    )
    manifest_b = SourceAcquisitionManifestV1(
        source=_source(),
        status=AcquisitionStatus.CAPTURED,
        artifacts=(second, first),
        notes="Direct capture.",
    )
    assert manifest_a.digest() == manifest_b.digest()


def test_source_manifest_rejects_non_first_party_source() -> None:
    with pytest.raises(ValueError, match="first-party"):
        SourceIdentityV1(
            source_id="SECONDARY",
            url="https://example.com/secondary",
            source_kind=SourceKind.OTHER_FIRST_PARTY,
            provenance_statement="Not direct.",
            first_party=False,
        )


def test_unavailable_manifest_rejects_artifacts() -> None:
    with pytest.raises(ValueError, match="UNAVAILABLE"):
        SourceAcquisitionManifestV1(
            source=_source(),
            status=AcquisitionStatus.UNAVAILABLE,
            artifacts=(_artifact(CaptureKind.TEXT, b"x", "post:1"),),
            notes="Unavailable contradiction.",
        )


def test_predicate_requires_every_declared_field_to_close() -> None:
    row = PredicateLedgerRowV1(
        predicate_id="TIME_SELECTOR",
        description="Executable time selector",
        required_fields=(PredicateField.EXACT_PREDICATE, PredicateField.EXPIRY),
        evidence=(
            PredicateEvidenceV1(
                field=PredicateField.EXACT_PREDICATE,
                source_id="ROMEO-TEST",
                locator="post:1",
                artifact_sha256="b" * 64,
                statement="Exact predicate only.",
                first_party_verified=True,
            ),
        ),
    )
    assert row.status is PredicateStatus.PARTIAL
    assert row.missing_fields == (PredicateField.EXPIRY,)
    assert not row.candidate_ready


def test_predicate_ledger_exposes_only_closed_rows_as_ready() -> None:
    open_row = PredicateLedgerRowV1(
        predicate_id="OPEN",
        description="Open predicate",
        required_fields=(PredicateField.EXACT_PREDICATE,),
    )
    closed_row = _closed_predicate("CLOSED")
    ledger = PredicateLedgerV1(rows=(open_row, closed_row))
    assert ledger.candidate_ready_rows == (closed_row,)


def test_unresolved_doctrine_cannot_have_deterministic_effect() -> None:
    baseline = DoctrineStatementV1("BASE", "Old statement", ("ROMEO-OLD",))
    incoming = DoctrineStatementV1("NEW", "New statement", ("ROMEO-NEW",))
    with pytest.raises(ValueError, match="deterministic alpha effect"):
        record_doctrine_delta(
            baseline=baseline,
            incoming=incoming,
            classification=DoctrineDeltaClassification.UNRESOLVED,
            deterministic_effect=True,
            rationale="Still unresolved.",
        )


def test_fixture_gate_requires_positive_and_negative_examples() -> None:
    predicate = _closed_predicate()
    positive = PredicateFixtureV1(
        fixture_id="POS-1",
        predicate_id=predicate.predicate_id,
        kind=FixtureKind.POSITIVE,
        source_ids=("ROMEO-TEST",),
        information_available_at="2026-08-14T12:00:00Z",
        observed_inputs="Causal pre-event inputs",
        expected_label="QUALIFIES",
    )
    with pytest.raises(ValueError, match="positive and one negative"):
        assert_fixture_gate(predicate, (positive,))

    negative = PredicateFixtureV1(
        fixture_id="NEG-1",
        predicate_id=predicate.predicate_id,
        kind=FixtureKind.NEGATIVE,
        source_ids=("ROMEO-TEST",),
        information_available_at="2026-08-14T12:00:00Z",
        observed_inputs="Causal counterexample inputs",
        expected_label="REJECTS",
    )
    assert_fixture_gate(predicate, (positive, negative))


def test_registry_loader_validates_schema_and_unique_ids(tmp_path: Path) -> None:
    path = tmp_path / "registry.csv"
    header = (
        "source_id,title,url,published_date,duration,source_type,relevance,status,concepts,notes\n"
    )
    path.write_text(
        header
        + "ROMEO-1,Title,https://example.com/1,2026,,telegram,critical,DISCOVERED,x,note\n",
        encoding="utf-8",
    )
    rows = load_source_registry_v1(path)
    assert rows[0].source_id == "ROMEO-1"

    path.write_text(
        header
        + "ROMEO-1,Title,https://example.com/1,2026,,telegram,critical,DISCOVERED,x,note\n"
        + "ROMEO-1,Title 2,https://example.com/2,2026,,telegram,critical,DISCOVERED,y,note\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unique"):
        load_source_registry_v1(path)


def test_corpus_index_is_deterministic_and_rejects_duplicate_manifest() -> None:
    first = CorpusEntryV1("ROMEO-A", "a" * 64, ("1" * 64,))
    second = CorpusEntryV1("ROMEO-B", "b" * 64, ("2" * 64, "3" * 64))
    assert CorpusIndexV1((first, second)).digest() == CorpusIndexV1((second, first)).digest()
    with pytest.raises(ValueError, match="manifest hashes"):
        CorpusIndexV1((first, first))


def test_checked_in_phase6d_readiness_audit_stays_research_only() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/audit_phase6d_research_readiness.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(completed.stdout)
    assert summary["candidate_ready_rows"] == 0
    assert summary["candidate_creation_authorized"] is False
    assert summary["detector_activity_authorized"] is False
    assert summary["outcome_access_authorized"] is False
