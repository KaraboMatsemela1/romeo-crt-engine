# Phase 6D — First-Party Research Infrastructure Checklist

**Status:** **COMPLETE — RESEARCH INFRASTRUCTURE V1 + CORPUS MIGRATION 001**  
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

## H. V1 validation

- [x] Add unit tests for manifest determinism and provenance rejection.
- [x] Add unit tests for predicate closure semantics.
- [x] Add unit tests for doctrine promotion rejection.
- [x] Add unit tests for positive/negative fixture gate.
- [x] Add unit tests for registry schema/duplicate handling.
- [x] Add unit tests for corpus index determinism.
- [x] CI green on V1 implementation head: Ruff PASS, MyPy PASS, **133 pytest tests PASS**.

## I. Existing corpus migration 001

- [x] Freeze the migration to the six-source Phase-6C bounded acquisition set.
- [x] Create six deterministic acquisition manifests.
- [x] Record one replayable `CAPTURED` source and five `PARTIAL` identity-only sources.
- [x] Admit only replayable artifact-backed evidence to `CORPUS_INDEX_V1.json`.
- [x] Preserve exact SHA-256 chain of custody for `ROMEO-2026-TG-TIME-TS-6361`.
- [x] Add `P6D_PREDICATE_LEDGER_V2` with explicit `PARTIAL` vs `CLOSING` evidence semantics.
- [x] Attach Time + Turtle Soup evidence to `TIME_SELECTOR` as `PARTIAL` only.
- [x] Keep `satisfied_fields = 0` for `TIME_SELECTOR`.
- [x] Keep all other held predicates unresolved because no replayable direct technical artifact exists in the bounded corpus.
- [x] Add `scripts/audit_phase6d_corpus_migration.py` to cross-check registry, manifest, corpus, and ledger provenance.
- [x] Validate migration audit in pytest.
- [x] Implementation-head CI green: Ruff PASS, MyPy PASS, **137 pytest tests PASS**.
- [x] `closing_field_evidence = 0`.
- [x] `candidate_ready_rows = 0`.
- [x] Keep candidate/detector/outcome authorization false.

## Exit condition

**Phase 6D V1 and Corpus Migration 001 exit conditions are satisfied on the implementation branch.** PR #23 is the repository promotion step.

The migration result is `COMPLETE_NO_PREDICATE_CLOSURE`: provenance quality improved, but Phase 6C remains blocked and no strategy implementation is authorized.

A future verified source may use this infrastructure to close a predicate, but **predicate closure alone does not authorize strategy implementation**. A separate preregistered candidate decision is still required.
