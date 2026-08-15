from __future__ import annotations

import json
from pathlib import Path

import pytest

from romeo_crt_engine.research.phase6c_closure_audit import (
    ClosureAuditError,
    ClosureAuditPaths,
    build_closure_report,
    report_with_digest,
    validate_checked_in_report,
)

ROOT = Path(__file__).resolve().parents[2]


def _paths(ledger: Path | None = None) -> ClosureAuditPaths:
    return ClosureAuditPaths(
        registry=ROOT / "research/romeo/SOURCE_REGISTRY.csv",
        acquisitions=ROOT / "research/romeo/phase6d/acquisitions",
        corpus_index=ROOT / "research/romeo/phase6d/CORPUS_INDEX_V1.json",
        ledger=ledger or ROOT / "research/romeo/phase6d/PREDICATE_LEDGER_V2.json",
        payloads=ROOT / "research/romeo/phase6d/payloads",
    )


def _ledger_copy(tmp_path: Path) -> tuple[Path, dict[str, object]]:
    raw = json.loads(_paths().ledger.read_text(encoding="utf-8"))
    path = tmp_path / "ledger.json"
    return path, raw


def _write(path: Path, raw: dict[str, object]) -> None:
    path.write_text(json.dumps(raw), encoding="utf-8")


def test_checked_in_closure_audit_is_complete_and_remains_open() -> None:
    report = validate_checked_in_report(
        _paths(), ROOT / "research/romeo/phase6c/PHASE_6C_CLOSURE_AUDIT_001.json"
    )
    assert report["summary"]["held_predicates"] == 8
    assert report["summary"]["open_predicates"] == 8
    assert report["summary"]["closed_predicates"] == 0
    assert report["summary"]["field_status_counts"] == {
        "contradictory": 0,
        "explicitly_satisfied": 0,
        "missing": 38,
        "partial": 18,
    }


def test_closure_audit_rejects_unknown_evidence_status(tmp_path: Path) -> None:
    path, raw = _ledger_copy(tmp_path)
    rows = raw["rows"]
    assert isinstance(rows, list)
    rows[0]["evidence"][0]["coverage"] = "UNVERIFIED"
    _write(path, raw)
    with pytest.raises(ClosureAuditError, match="unknown field or coverage status"):
        build_closure_report(_paths(path))


def test_closure_audit_rejects_mismatched_evidence_source(tmp_path: Path) -> None:
    path, raw = _ledger_copy(tmp_path)
    rows = raw["rows"]
    assert isinstance(rows, list)
    rows[0]["evidence"][0]["source_id"] = "ROMEO-TG-SMT-PAIRS-6363"
    _write(path, raw)
    with pytest.raises(ClosureAuditError, match="does not match registry, manifest, and corpus"):
        build_closure_report(_paths(path))


def test_closure_audit_rejects_mismatched_evidence_locator(tmp_path: Path) -> None:
    path, raw = _ledger_copy(tmp_path)
    rows = raw["rows"]
    assert isinstance(rows, list)
    rows[0]["evidence"][0]["locator"] = "https://t.me/officialRomeotpt/6912#altered"
    _write(path, raw)
    with pytest.raises(ClosureAuditError, match="manifest artifact locator"):
        build_closure_report(_paths(path))


def test_closure_audit_rejects_duplicate_contradictory_claim(tmp_path: Path) -> None:
    path, raw = _ledger_copy(tmp_path)
    rows = raw["rows"]
    assert isinstance(rows, list)
    claim = dict(rows[0]["evidence"][0])
    claim["statement"] = "A contradictory duplicate claim."
    rows[0]["evidence"].append(claim)
    _write(path, raw)
    with pytest.raises(ClosureAuditError, match="duplicate contradictory evidence claim"):
        build_closure_report(_paths(path))


def test_closure_audit_rejects_unreviewed_predicate_closure(tmp_path: Path) -> None:
    path, raw = _ledger_copy(tmp_path)
    rows = raw["rows"]
    assert isinstance(rows, list)
    row = rows[0]
    row["required_fields"] = ["EXACT_PREDICATE"]
    row["evidence"] = [dict(row["evidence"][0], coverage="CLOSING")]
    _write(path, raw)
    report = report_with_digest(build_closure_report(_paths(path)))
    report_path = tmp_path / "report.json"
    _write(report_path, report)
    with pytest.raises(ClosureAuditError, match="not authorized"):
        validate_checked_in_report(_paths(path), report_path)
