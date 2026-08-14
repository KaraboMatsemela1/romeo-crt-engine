from __future__ import annotations

import json
import subprocess
import sys

import pytest

from romeo_crt_engine.research.predicate_ledger_v2 import (
    EvidenceCoverage,
    PredicateEvidenceV2,
    PredicateField,
    PredicateLedgerRowV2,
    PredicateStatus,
)


def _evidence(field: PredicateField, coverage: EvidenceCoverage) -> PredicateEvidenceV2:
    return PredicateEvidenceV2(
        field=field,
        source_id="ROMEO-TEST",
        locator="post:1",
        artifact_sha256="a" * 64,
        statement="Direct source evidence.",
        coverage=coverage,
        first_party_verified=True,
    )


def test_partial_evidence_is_observed_but_does_not_satisfy_field() -> None:
    row = PredicateLedgerRowV2(
        predicate_id="TIME_SELECTOR",
        description="Time selector",
        required_fields=(PredicateField.EXACT_PREDICATE, PredicateField.EXPIRY),
        evidence=(
            _evidence(PredicateField.EXACT_PREDICATE, EvidenceCoverage.PARTIAL),
        ),
    )
    assert row.observed_fields == frozenset({PredicateField.EXACT_PREDICATE})
    assert row.satisfied_fields == frozenset()
    assert row.missing_fields == (
        PredicateField.EXACT_PREDICATE,
        PredicateField.EXPIRY,
    )
    assert row.status is PredicateStatus.PARTIAL
    assert not row.candidate_ready


def test_only_closing_evidence_satisfies_required_field() -> None:
    row = PredicateLedgerRowV2(
        predicate_id="CLOSED",
        description="Closed one-field predicate",
        required_fields=(PredicateField.EXACT_PREDICATE,),
        evidence=(
            _evidence(PredicateField.EXACT_PREDICATE, EvidenceCoverage.CLOSING),
        ),
    )
    assert row.satisfied_fields == frozenset({PredicateField.EXACT_PREDICATE})
    assert row.missing_fields == ()
    assert row.status is PredicateStatus.CLOSED
    assert row.candidate_ready


def test_evidence_cannot_target_undeclared_field() -> None:
    with pytest.raises(ValueError, match="declared"):
        PredicateLedgerRowV2(
            predicate_id="INVALID",
            description="Invalid evidence field",
            required_fields=(PredicateField.EXACT_PREDICATE,),
            evidence=(
                _evidence(PredicateField.EXPIRY, EvidenceCoverage.PARTIAL),
            ),
        )


def test_checked_in_corpus_migration_audit_remains_research_only() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/audit_phase6d_corpus_migration.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    summary = json.loads(completed.stdout)
    assert summary["acquisition_manifests"] == 21
    assert summary["captured_manifests"] == 16
    assert summary["partial_manifests"] == 5
    assert summary["corpus_sources"] == 16
    assert summary["corpus_artifacts"] == 18
    assert summary["payload_files_verified"] == 18
    assert summary["predicate_rows_with_artifact_evidence"] == 7
    assert summary["observed_field_evidence"] == 17
    assert summary["closing_field_evidence"] == 0
    assert summary["candidate_ready_rows"] == 0
    assert summary["candidate_creation_authorized"] is False
    assert summary["detector_activity_authorized"] is False
    assert summary["outcome_access_authorized"] is False


def test_recovery_003_route_audit_remains_bounded_and_research_only() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/audit_phase6d_recovery_003.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    summary = json.loads(completed.stdout)
    assert summary["bounded_routes"] == 6
    assert summary["new_artifacts"] == 0
    assert summary["new_payload_sha256s"] == 0
    assert summary["source_availability_observed"] == 0
    assert summary["candidate_creation_authorized"] is False
    assert summary["detector_activity_authorized"] is False
    assert summary["outcome_access_authorized"] is False


def test_recovery_004_route_audit_remains_bounded_and_research_only() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/audit_phase6d_recovery_004.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    summary = json.loads(completed.stdout)
    assert summary["bounded_routes"] == 6
    assert summary["availability_checks"] == 6
    assert summary["official_channel_index_searches"] == 6
    assert summary["source_unavailable_routes"] == 6
    assert summary["new_artifacts"] == 0
    assert summary["new_payload_sha256s"] == 0
    assert summary["closing_field_evidence"] == 0
    assert summary["candidate_ready_rows"] == 0
    assert summary["candidate_creation_authorized"] is False
    assert summary["detector_activity_authorized"] is False
    assert summary["outcome_access_authorized"] is False
