"""Fail-closed sequential validation access guard."""

from dataclasses import dataclass
from enum import StrEnum


class ValidationState(StrEnum):
    PRECOMMIT = "PRECOMMIT"
    DEV_ALLOWED = "DEV_ALLOWED"
    DEV_SEALED = "DEV_SEALED"
    OOS_ALLOWED = "OOS_ALLOWED"
    OOS_SEALED = "OOS_SEALED"
    CONFIRM_ALLOWED = "CONFIRM_ALLOWED"
    COMPLETE = "COMPLETE"


@dataclass(frozen=True)
class Transition:
    from_state: ValidationState
    to_state: ValidationState
    dataset_hash: str | None
    run_hash: str | None


@dataclass(frozen=True)
class ValidationGuard:
    state: ValidationState = ValidationState.PRECOMMIT
    audit: tuple[Transition, ...] = ()

    def advance(
        self,
        target: ValidationState,
        *,
        dataset_hash: str | None = None,
        run_hash: str | None = None,
        promotion_eligible: bool = False,
    ) -> "ValidationGuard":
        allowed = {
            ValidationState.PRECOMMIT: {ValidationState.DEV_ALLOWED},
            ValidationState.DEV_ALLOWED: {ValidationState.DEV_SEALED},
            ValidationState.DEV_SEALED: {ValidationState.OOS_ALLOWED},
            ValidationState.OOS_ALLOWED: {ValidationState.OOS_SEALED},
            ValidationState.OOS_SEALED: {ValidationState.CONFIRM_ALLOWED},
            ValidationState.CONFIRM_ALLOWED: {ValidationState.COMPLETE},
            ValidationState.COMPLETE: set(),
        }
        if target not in allowed[self.state]:
            raise ValueError(f"invalid validation transition: {self.state} -> {target}")
        if target in {
            ValidationState.DEV_SEALED,
            ValidationState.OOS_SEALED,
            ValidationState.CONFIRM_ALLOWED,
            ValidationState.COMPLETE,
        } and (not dataset_hash or not run_hash):
            raise ValueError("sealed or promoted transitions require dataset_hash and run_hash")
        if target is ValidationState.CONFIRM_ALLOWED and not promotion_eligible:
            raise ValueError("CONFIRM requires explicit promotion eligibility")
        if target is ValidationState.COMPLETE and not promotion_eligible:
            raise ValueError("COMPLETE requires explicit promotion eligibility")
        transition = Transition(self.state, target, dataset_hash, run_hash)
        return ValidationGuard(target, self.audit + (transition,))
