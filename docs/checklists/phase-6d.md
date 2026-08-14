# Phase 6D — First-Party Research Infrastructure Checklist

**Status:** **COMPLETE — RESEARCH INFRASTRUCTURE V1**  
**Mode:** research infrastructure only

## A. Preserve historical boundaries

- [x] Keep Phase 6 v0.1 `INSUFFICIENT_EVIDENCE` immutable.
- [x] Keep Phase 6B `INSUFFICIENT_MULTI_MARKET_SAMPLE` immutable.
- [x] Keep Phase 6C `BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE` as the evidence-acquisition result.
- [x] Keep v0.1 OOS / CONFIRM unopened.
- [x] Keep detector/count/P&L/paper/shadow/live unauthorized.

## B. Source acquisition and provenance

- [x] Add first-party source identity contract.
- [x] Add typed capture artifact contract.
- [x] Hash captured payloads with SHA-256.
- [x] Add canonical deterministic acquisition manifest + digest.
- [x] Reject non-first-party captures.
- [x] Bind capture CLI to `SOURCE_REGISTRY.csv` instead of caller-supplied URLs.
- [x] Reject unregistered source IDs.
- [x] Permit metadata/text/captions/transcript/frame/chart evidence types.
- [x] Enforce exact registry row width and fail closed on malformed column alignment.

## C. Predicate evidence engine

- [x] Add machine-readable `PREDICATE_LEDGER_V1.json`.
- [x] Define required causal closure fields.
- [x] Require direct first-party evidence for each satisfied field.
- [x] Keep qualitative/partial doctrine from becoming `CLOSED`.
- [x] Seed all current Phase-6C evidence debts as unresolved rows.
- [x] Expose `candidate_ready_rows` without authorizing a candidate.

## D. Doctrine reconciliation automation

- [x] Encode allowed doctrine delta classifications.
- [x] Require explicit research classification rather than opaque semantic inference.
- [x] Prevent `UNRESOLVED` or `NON_ALPHA_CONTEXT` from claiming deterministic alpha effect.

## E. Evidence-to-fixture gate

- [x] Require predicate closure before fixture gate.
- [x] Require at least one positive causal fixture.
- [x] Require at least one negative/counterexample fixture.
- [x] Require information-availability metadata in fixtures.

## F. Corpus hardening

- [x] Add deterministic evidence corpus index contract.
- [x] Bind manifests to artifact SHA-256 values.
- [x] Reject duplicate manifest hashes.
- [x] Keep large/raw copyrighted media optional outside Git while preserving hashes and locators.

## G. Readiness audit

- [x] Add `scripts/audit_phase6d_research_readiness.py`.
- [x] Validate source registry schema and unique IDs.
- [x] Reject predicate evidence referencing unknown source IDs.
- [x] Emit candidate-ready row count only.
- [x] Emit candidate/detector/outcome authorizations as false.
- [x] Run the audit against the checked-in registry + ledger in pytest.

## H. Validation

- [x] Add unit tests for manifest determinism and provenance rejection.
- [x] Add unit tests for predicate closure semantics.
- [x] Add unit tests for doctrine promotion rejection.
- [x] Add unit tests for positive/negative fixture gate.
- [x] Add unit tests for registry schema/duplicate handling.
- [x] Add unit tests for corpus index determinism.
- [x] CI green on implementation head: Ruff PASS, MyPy PASS, **133 pytest tests PASS**.

## Exit condition

**Phase 6D V1 exit condition is satisfied.** The research-infrastructure implementation is green and all historical strategy/outcome authorizations remain false. Merge of PR #20 is the repository promotion step.

A future verified source may use this infrastructure to close a predicate, but **predicate closure alone does not authorize strategy implementation**. A separate preregistered candidate decision is still required.
