# ADR-001: Deterministic CRT Core Before ML

**Status:** Accepted

## Decision
Implement the first CRT strategy candidate as deterministic rules/state transitions. ML may later rank already-valid setups but does not define live setup validity initially.

## Rationale
This maximizes explainability, source fidelity, testability, and the ability to distinguish strategy failure from model behavior.
