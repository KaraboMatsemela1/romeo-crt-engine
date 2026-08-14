"""Fail-closed sequential access guard for DEV, OOS, and CONFIRM validation."""

from __future__ import annotations

import argparse
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

SHA256_PATTERN = r"^[0-9a-f]{64}$"


class ValidationState(StrEnum):
    """Canonical validation access states."""

    PRECOMMIT = "PRECOMMIT"
    DEV_ALLOWED = "DEV_ALLOWED"
    DEV_SEALED = "DEV_SEALED"
    OOS_ALLOWED = "OOS_ALLOWED"
    OOS_SEALED = "OOS_SEALED"
    CONFIRM_ALLOWED = "CONFIRM_ALLOWED"
    COMPLETE = "COMPLETE"


class TerminalDisposition(StrEnum):
    """Dispositions that may terminate validation without opening later windows."""

    REJECT = "REJECT"
    REVISE_AS_NEW_VERSION = "REVISE_AS_NEW_VERSION"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    PROMOTE_TO_PAPER_CANDIDATE = "PROMOTE_TO_PAPER_CANDIDATE"


class TransitionEvidence(BaseModel):
    """Hash-bound evidence supplied for one state transition."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    recorded_at: str = Field(min_length=1)
    preregistration_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    dataset_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    run_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    report_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    eligibility_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    confirm_eligible: bool | None = None
    terminal_disposition: TerminalDisposition | None = None


class TransitionRecord(BaseModel):
    """Immutable audit record for one accepted transition."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    from_state: ValidationState
    to_state: ValidationState
    evidence: TransitionEvidence


class ValidationAccessGuard(BaseModel):
    """Immutable state machine enforcing sequential validation access."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidate_id: str = Field(min_length=1)
    state: ValidationState = ValidationState.PRECOMMIT
    audit: tuple[TransitionRecord, ...] = ()

    @model_validator(mode="after")
    def audit_matches_state(self) -> Self:
        if self.audit and self.audit[-1].to_state != self.state:
            raise ValueError("final audit transition must match current state")
        if not self.audit and self.state != ValidationState.PRECOMMIT:
            raise ValueError("non-PRECOMMIT state requires an audit trail")
        for previous, current in zip(self.audit, self.audit[1:], strict=False):
            if previous.to_state != current.from_state:
                raise ValueError("audit trail transitions must be contiguous")
        return self

    def transition(
        self, target: ValidationState, evidence: TransitionEvidence
    ) -> ValidationAccessGuard:
        """Return a new guard after validating the requested transition."""
        self._validate_transition(target, evidence)
        record = TransitionRecord(from_state=self.state, to_state=target, evidence=evidence)
        return self.model_copy(update={"state": target, "audit": (*self.audit, record)})

    def _validate_transition(
        self, target: ValidationState, evidence: TransitionEvidence
    ) -> None:
        allowed = {
            ValidationState.PRECOMMIT: {ValidationState.DEV_ALLOWED},
            ValidationState.DEV_ALLOWED: {ValidationState.DEV_SEALED},
            ValidationState.DEV_SEALED: {ValidationState.OOS_ALLOWED, ValidationState.COMPLETE},
            ValidationState.OOS_ALLOWED: {ValidationState.OOS_SEALED},
            ValidationState.OOS_SEALED: {ValidationState.CONFIRM_ALLOWED, ValidationState.COMPLETE},
            ValidationState.CONFIRM_ALLOWED: {ValidationState.COMPLETE},
            ValidationState.COMPLETE: set(),
        }
        if target not in allowed[self.state]:
            raise ValueError(f"prohibited validation transition: {self.state} -> {target}")

        if self.state == ValidationState.PRECOMMIT:
            self._require(evidence.preregistration_sha256, "preregistration_sha256")
            self._reject_outcome_fields(evidence)
            return

        if target in {ValidationState.DEV_SEALED, ValidationState.OOS_SEALED}:
            self._require_window_seal_hashes(evidence)
            return

        if target == ValidationState.OOS_ALLOWED:
            self._require(evidence.preregistration_sha256, "preregistration_sha256")
            self._reject_outcome_fields(evidence)
            return

        if target == ValidationState.CONFIRM_ALLOWED:
            if evidence.confirm_eligible is not True:
                raise ValueError("CONFIRM access requires explicit confirm_eligible=true")
            self._require(evidence.eligibility_sha256, "eligibility_sha256")
            self._require(evidence.preregistration_sha256, "preregistration_sha256")
            if evidence.terminal_disposition is not None:
                raise ValueError("CONFIRM authorization cannot include terminal_disposition")
            return

        if target == ValidationState.COMPLETE:
            self._validate_completion(evidence)

    @staticmethod
    def _require(value: str | None, field_name: str) -> None:
        if value is None:
            raise ValueError(f"{field_name} is required for this transition")

    @classmethod
    def _require_window_seal_hashes(cls, evidence: TransitionEvidence) -> None:
        cls._require(evidence.dataset_sha256, "dataset_sha256")
        cls._require(evidence.run_sha256, "run_sha256")
        cls._require(evidence.report_sha256, "report_sha256")
        if evidence.terminal_disposition is not None:
            raise ValueError("window seal transition cannot include terminal_disposition")

    @staticmethod
    def _reject_outcome_fields(evidence: TransitionEvidence) -> None:
        if any(
            value is not None
            for value in (
                evidence.dataset_sha256,
                evidence.run_sha256,
                evidence.report_sha256,
                evidence.eligibility_sha256,
                evidence.confirm_eligible,
                evidence.terminal_disposition,
            )
        ):
            raise ValueError("access authorization transition contains premature outcome evidence")

    def _validate_completion(self, evidence: TransitionEvidence) -> None:
        self._require(evidence.report_sha256, "report_sha256")
        disposition = evidence.terminal_disposition
        if disposition is None:
            raise ValueError("terminal_disposition is required for COMPLETE")

        if self.state == ValidationState.CONFIRM_ALLOWED:
            self._require(evidence.dataset_sha256, "dataset_sha256")
            self._require(evidence.run_sha256, "run_sha256")
            if disposition == TerminalDisposition.PROMOTE_TO_PAPER_CANDIDATE:
                self._require(evidence.eligibility_sha256, "eligibility_sha256")
            return

        if disposition == TerminalDisposition.PROMOTE_TO_PAPER_CANDIDATE:
            raise ValueError("paper-candidate promotion requires completed CONFIRM")
        if evidence.dataset_sha256 is not None or evidence.run_sha256 is not None:
            raise ValueError("early terminal completion must not introduce unopened-window results")


def _load_guard(path: Path) -> ValidationAccessGuard:
    return ValidationAccessGuard.model_validate_json(path.read_text(encoding="utf-8"))


def _write_guard(path: Path, guard: ValidationAccessGuard) -> None:
    path.write_text(guard.model_dump_json(indent=2) + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sequential validation access guard")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("state_file", type=Path)
    init.add_argument("candidate_id")

    transition = subparsers.add_parser("transition")
    transition.add_argument("state_file", type=Path)
    transition.add_argument("target", choices=[state.value for state in ValidationState])
    transition.add_argument("--evidence-json", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for machine-enforced validation transitions."""
    args = _build_parser().parse_args(argv)
    if args.command == "init":
        _write_guard(args.state_file, ValidationAccessGuard(candidate_id=args.candidate_id))
        return 0

    guard = _load_guard(args.state_file)
    evidence = TransitionEvidence.model_validate_json(args.evidence_json.read_text(encoding="utf-8"))
    updated = guard.transition(ValidationState(args.target), evidence)
    _write_guard(args.state_file, updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
