import pytest

from romeo_crt_engine.validation_guard import ValidationGuard, ValidationState


def test_only_dev_can_open_from_precommit():
    guard = ValidationGuard()
    with pytest.raises(ValueError):
        guard.advance(ValidationState.OOS_ALLOWED)


def test_dev_must_seal_before_oos():
    guard = ValidationGuard().advance(ValidationState.DEV_ALLOWED)
    with pytest.raises(ValueError):
        guard.advance(ValidationState.OOS_ALLOWED)
    sealed = guard.advance(
        ValidationState.DEV_SEALED,
        dataset_hash="dev-data",
        run_hash="dev-run",
    )
    opened = sealed.advance(ValidationState.OOS_ALLOWED)
    assert opened.state is ValidationState.OOS_ALLOWED


def test_oos_seal_is_required_before_confirm():
    guard = ValidationGuard()
    guard = guard.advance(ValidationState.DEV_ALLOWED)
    guard = guard.advance(
        ValidationState.DEV_SEALED,
        dataset_hash="dev-data",
        run_hash="dev-run",
    )
    guard = guard.advance(ValidationState.OOS_ALLOWED)
    with pytest.raises(ValueError):
        guard.advance(ValidationState.CONFIRM_ALLOWED, promotion_eligible=True)


def test_confirm_requires_promotion_and_hashes():
    guard = ValidationGuard()
    guard = guard.advance(ValidationState.DEV_ALLOWED)
    guard = guard.advance(
        ValidationState.DEV_SEALED,
        dataset_hash="dev-data",
        run_hash="dev-run",
    )
    guard = guard.advance(ValidationState.OOS_ALLOWED)
    guard = guard.advance(
        ValidationState.OOS_SEALED,
        dataset_hash="oos-data",
        run_hash="oos-run",
    )
    with pytest.raises(ValueError):
        guard.advance(ValidationState.CONFIRM_ALLOWED)
    confirmed = guard.advance(
        ValidationState.CONFIRM_ALLOWED,
        dataset_hash="confirm-data",
        run_hash="confirm-run",
        promotion_eligible=True,
    )
    assert confirmed.state is ValidationState.CONFIRM_ALLOWED
    assert len(confirmed.audit) == 5


def test_audit_is_immutable():
    guard = ValidationGuard().advance(ValidationState.DEV_ALLOWED)
    assert guard.audit[0].dataset_hash is None
    with pytest.raises(ValueError):
        guard.advance(ValidationState.PRECOMMIT)
