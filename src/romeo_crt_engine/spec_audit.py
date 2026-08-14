"""Independent leakage and implementation-spec audit."""

from dataclasses import dataclass
from enum import StrEnum


class AuditStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class AuditInput:
    future_d1_h1_used: bool
    unfinished_candle_ohlc_used: bool
    retrospective_parent_selection: bool
    date_window_immutable: bool
    cost_config_immutable: bool
    hashes_bound: bool
    same_bar_policy_declared: bool
    gap_policy_declared: bool
    quarantined_windows_excluded: bool
    spec_matches_code: bool


@dataclass(frozen=True)
class AuditFinding:
    check: str
    status: AuditStatus
    evidence: str


@dataclass(frozen=True)
class AuditReport:
    status: AuditStatus
    findings: tuple[AuditFinding, ...]


def audit(candidate: AuditInput) -> AuditReport:
    checks = (
        ("future_d1_h1_use", not candidate.future_d1_h1_used),
        ("unfinished_candle_ohlc", not candidate.unfinished_candle_ohlc_used),
        ("retrospective_parent_selection", not candidate.retrospective_parent_selection),
        ("date_window_immutable", candidate.date_window_immutable),
        ("cost_config_immutable", candidate.cost_config_immutable),
        ("detector_simulator_data_hashes_bound", candidate.hashes_bound),
        ("same_bar_fill_policy_declared", candidate.same_bar_policy_declared),
        ("gap_handling_declared", candidate.gap_policy_declared),
        ("quarantined_windows_excluded", candidate.quarantined_windows_excluded),
        ("spec_matches_code", candidate.spec_matches_code),
    )
    findings = tuple(
        AuditFinding(
            check=name,
            status=AuditStatus.PASS if passed else AuditStatus.FAIL,
            evidence=f"synthetic audit input: {name}",
        )
        for name, passed in checks
    )
    status = AuditStatus.PASS if all(f.status is AuditStatus.PASS for f in findings) else AuditStatus.FAIL
    return AuditReport(status=status, findings=findings)
