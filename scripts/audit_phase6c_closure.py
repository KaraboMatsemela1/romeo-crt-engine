from __future__ import annotations

import argparse
import json
from pathlib import Path

from romeo_crt_engine.research.phase6c_closure_audit import (
    ClosureAuditPaths,
    build_closure_report,
    report_with_digest,
    validate_checked_in_report,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "research/romeo/phase6c/PHASE_6C_CLOSURE_AUDIT_001.json"


def _paths() -> ClosureAuditPaths:
    return ClosureAuditPaths(
        registry=ROOT / "research/romeo/SOURCE_REGISTRY.csv",
        acquisitions=ROOT / "research/romeo/phase6d/acquisitions",
        corpus_index=ROOT / "research/romeo/phase6d/CORPUS_INDEX_V1.json",
        ledger=ROOT / "research/romeo/phase6d/PREDICATE_LEDGER_V2.json",
        payloads=ROOT / "research/romeo/phase6d/payloads",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Phase 6C first-party closure audit.")
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="regenerate the deterministic checked-in report after intentional corpus changes",
    )
    args = parser.parse_args()
    paths = _paths()
    if args.write_report:
        report = report_with_digest(build_closure_report(paths))
        REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = validate_checked_in_report(paths, REPORT_PATH)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
