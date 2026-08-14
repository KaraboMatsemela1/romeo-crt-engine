import pytest
from pydantic import ValidationError

from romeo_crt_engine.validation_guard import (
    TerminalDisposition,
    TransitionEvidence,
    ValidationAccessGuard,
    ValidationState,
)

SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64


def evidence(**overrides):
    payload = {"recorded_at": "2026-08-14T18:30:00Z"}
    payload.update(overrides)
    return TransitionEvidence(**payload)


def move_to_dev_sealed() -> ValidationAccessGuard:
    guard = ValidationAccessGuard(candidate_id="CRT-TEST-v0.3")
    guard = guard.transition(
        ValidationState.DEV_ALLOWED,
        evidence(preregistration_sha256=SHA_A),
    )
    return guard.transition(
        ValidationState.DEV_SEALED,
        evidence(dataset_sha256=SHA_A, run_sha256=SHA_B, report_sha256=SHA_C),
    )


def move_to_oos_sealed() -> ValidationAccessGuard:
    guard = move_to_dev_sealed()
    guard = guard.transition(
        ValidationState.OOS_ALLOWED,
        evidence(preregistration_sha256=SHA_D),
    )
    return guard.transition(
        ValidationState.OOS_SEALED,
        evidence(dataset_sha256=SHA_A, run_sha256=SHA_B, report_sha256=SHA_C),
    )


def test_oos_cannot_open_before_dev_is_sealed():
    guard = ValidationAccessGuard(candidate_id="CRT-TEST-v0.3")
    with pytest.raises(ValueError, match="prohibited validation transition"):
        guard.transition(
            ValidationState.OOS_ALLOWED,
            evidence(preregistration_sha256=SHA_A),
        )


def test_confirm_cannot_open_before_oos_is_sealed():
    guard = move_to_dev_sealed()
    with pytest.raises(ValueError, match="prohibited validation transition"):
        guard.transition(
            ValidationState.CONFIRM_ALLOWED,
            evidence(
                preregistration_sha256=SHA_A,
                eligibility_sha256=SHA_B,
                confirm_eligible=True,
            ),
        )


def test_confirm_requires_explicit_eligibility_and_hash():
    guard = move_to_oos_sealed()
    with pytest.raises(ValueError, match="confirm_eligible"):
        guard.transition(
            ValidationState.CONFIRM_ALLOWED,
            evidence(preregistration_sha256=SHA_A, eligibility_sha256=SHA_B),
        )
    with pytest.raises(ValueError, match="eligibility_sha256"):
        guard.transition(
            ValidationState.CONFIRM_ALLOWED,
            evidence(preregistration_sha256=SHA_A, confirm_eligible=True),
        )


def test_window_seal_requires_dataset_run_and_report_hashes():
    guard = ValidationAccessGuard(candidate_id="CRT-TEST-v0.3").transition(
        ValidationState.DEV_ALLOWED,
        evidence(preregistration_sha256=SHA_A),
    )
    with pytest.raises(ValueError, match="dataset_sha256"):
        guard.transition(ValidationState.DEV_SEALED, evidence())


def test_early_terminal_disposition_preserves_oos_closed():
    guard = move_to_dev_sealed()
    complete = guard.transition(
        ValidationState.COMPLETE,
        evidence(
            report_sha256=SHA_A,
            terminal_disposition=TerminalDisposition.INSUFFICIENT_EVIDENCE,
        ),
    )
    assert complete.state == ValidationState.COMPLETE
    assert all(record.to_state != ValidationState.OOS_ALLOWED for record in complete.audit)


def test_paper_promotion_requires_confirm_completion():
    guard = move_to_oos_sealed()
    with pytest.raises(ValueError, match="requires completed CONFIRM"):
        guard.transition(
            ValidationState.COMPLETE,
            evidence(
                report_sha256=SHA_A,
                terminal_disposition=TerminalDisposition.PROMOTE_TO_PAPER_CANDIDATE,
            ),
        )


def test_confirm_complete_records_hash_bound_result():
    guard = move_to_oos_sealed().transition(
        ValidationState.CONFIRM_ALLOWED,
        evidence(
            preregistration_sha256=SHA_A,
            eligibility_sha256=SHA_B,
            confirm_eligible=True,
        ),
    )
    complete = guard.transition(
        ValidationState.COMPLETE,
        evidence(
            dataset_sha256=SHA_A,
            run_sha256=SHA_B,
            report_sha256=SHA_C,
            eligibility_sha256=SHA_D,
            terminal_disposition=TerminalDisposition.PROMOTE_TO_PAPER_CANDIDATE,
        ),
    )
    assert complete.state == ValidationState.COMPLETE
    assert len(complete.audit) == 6


def test_guard_is_immutable_and_audit_must_match_state():
    guard = move_to_dev_sealed()
    with pytest.raises(ValidationError):
        guard.state = ValidationState.OOS_ALLOWED
    with pytest.raises(ValidationError, match="final audit transition"):
        ValidationAccessGuard(
            candidate_id=guard.candidate_id,
            state=ValidationState.OOS_ALLOWED,
            audit=guard.audit,
        )


@pytest.mark.parametrize(
    ("start", "target"),
    [
        (ValidationState.PRECOMMIT, ValidationState.CONFIRM_ALLOWED),
        (ValidationState.DEV_ALLOWED, ValidationState.OOS_ALLOWED),
        (ValidationState.OOS_ALLOWED, ValidationState.CONFIRM_ALLOWED),
        (ValidationState.CONFIRM_ALLOWED, ValidationState.OOS_ALLOWED),
        (ValidationState.COMPLETE, ValidationState.DEV_ALLOWED),
    ],
)
def test_representative_prohibited_transitions_fail_closed(start, target):
    guard = ValidationAccessGuard(candidate_id="CRT-TEST-v0.3")
    object.__setattr__(guard, "state", start)
    with pytest.raises(ValueError, match="prohibited validation transition"):
        guard.transition(target, evidence(preregistration_sha256=SHA_A))
