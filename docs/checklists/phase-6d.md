# Phase 6D — First-Party Research Infrastructure Checklist

**Status:** **COMPLETE — V1 + CORPUS MIGRATION 001 + FIRST-PARTY RECOVERY 002**  
**Mode:** research infrastructure / provenance only

## A. Preserve historical boundaries

- [x] Keep Phase 6 v0.1 `INSUFFICIENT_EVIDENCE` immutable.
- [x] Keep Phase 6B `INSUFFICIENT_MULTI_MARKET_SAMPLE` immutable.
- [x] Keep Phase 6C `BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE`.
- [x] Keep v0.1 OOS / CONFIRM unopened.
- [x] Keep detector/count/P&L/paper/shadow/live unauthorized.
- [x] Do not create a Phase-6C candidate from partial evidence.

## B. Research infrastructure V1

- [x] Registry-bound first-party source identity.
- [x] SHA-256 capture-artifact provenance.
- [x] Canonical acquisition manifest + digest.
- [x] Strict registry schema / row-width validation.
- [x] Predicate evidence ledger.
- [x] Explicit causal closure fields.
- [x] Doctrine delta validation.
- [x] Positive + negative fixture gate.
- [x] Deterministic evidence corpus index.
- [x] Research readiness audit.
- [x] Fail-closed unit tests.
- [x] V1 CI green.

## C. Predicate evidence semantics

- [x] Preserve `P6D_PREDICATE_LEDGER_V2`.
- [x] Distinguish `PARTIAL` from `CLOSING` evidence.
- [x] Permit `PARTIAL` evidence to be observed without satisfying a field.
- [x] Permit only `CLOSING` evidence to contribute to `satisfied_fields`.
- [x] Keep candidate readiness dependent on all declared fields closing.
- [x] Keep fixture generation downstream of predicate closure.

## D. Existing corpus migration 001

- [x] Bound migration to the six Phase-6C acquisition sources.
- [x] Create deterministic acquisition manifests.
- [x] Admit only replayable artifact-backed evidence.
- [x] Preserve exact SHA-256 chain for the legacy Time + Turtle Soup capture.
- [x] Add cross-file registry/manifest/corpus/ledger audit.
- [x] Keep `closing_field_evidence = 0`.
- [x] Keep `candidate_ready_rows = 0`.
- [x] Merge PR #23 with CI green.

## E. First-party artifact recovery 002

- [x] Create tracking Issue #24.
- [x] Recover exact first-party Romeo Telegram locators for quarantined claims.
- [x] Register 15 recovered direct source records.
- [x] Recover Model #1 prioritization source.
- [x] Recover Turtle Soup entry-example source.
- [x] Recover example-specific daily-timeframe source.
- [x] Recover key-level journey/reaction source.
- [x] Recover Episode-5 key-level ownership source.
- [x] Recover five published key times.
- [x] Recover key-time synchronization guidance.
- [x] Recover opposite-CRT bias-change source.
- [x] Recover basic SMT pair registry.
- [x] Recover SMT-for-expected-local-TS example.
- [x] Recover Episode-9 SMT source-ownership statement.
- [x] Recover exact CRTology Episode-1 first-party link.
- [x] Recover organized-application / do-not-force CRTology clues.
- [x] Recover trend-warning guidance.
- [x] Preserve all recovered ledger claims as `PARTIAL` only.
- [x] Leave `TRUE_MSS_ALGORITHM` unresolved because no direct algorithm was recovered.

## F. Payload-store hardening

- [x] Persist every corpus-admitted text artifact as `payloads/<sha256>.txt`.
- [x] Require the payload file to exist.
- [x] Recompute SHA-256 from exact payload bytes.
- [x] Verify byte length against acquisition manifest.
- [x] Verify manifest digest.
- [x] Verify manifest source URL against source registry.
- [x] Verify corpus index ownership.
- [x] Verify ledger artifact SHA resolves to admitted corpus evidence.
- [x] Verify 18 / 18 corpus payload files.

## G. Recovery 002 predicate coverage

- [x] `SS_MEANING_AND_CAUSAL_RULE` — artifact-backed `PARTIAL`.
- [x] `SMT_EXECUTABLE_SEMANTICS` — artifact-backed `PARTIAL`.
- [x] `MODEL_1_GEOMETRY` — artifact-backed `PARTIAL`.
- [x] `TRUE_MSS_ALGORITHM` — remains `UNRESOLVED`.
- [x] `TURTLE_SOUP_CONFIRMATION` — artifact-backed `PARTIAL`.
- [x] `KEY_LEVEL_SELECTOR` — artifact-backed `PARTIAL`.
- [x] `TIME_SELECTOR` — artifact-backed `PARTIAL`.
- [x] `DYNAMIC_BIAS_TRANSITION` — artifact-backed `PARTIAL`.
- [x] `CLOSING field evidence = 0`.
- [x] `candidate_ready_rows = 0`.

## H. Direct technical acquisition exhaustion

- [x] Attempt direct first-party CRTology Episode-1 technical/caption route.
- [x] Attempt direct first-party CRT Secrets Episode-6 technical/caption route.
- [x] Attempt direct first-party CRT Secrets Episode-9 technical/caption route.
- [x] Attempt direct first-party original Turtle Soup technical/caption route.
- [x] Search first-party Romeo material for explicit true-MSS algorithm.
- [x] Record unavailable technical semantics without substituting third-party inference.
- [x] Treat remaining debts as evidence-availability blockers.

## I. Validation

- [x] Ruff PASS on Recovery-002 implementation head.
- [x] MyPy PASS on Recovery-002 implementation head.
- [x] pytest **137 PASS** on Recovery-002 implementation head.
- [x] Migration audit reports 21 manifests / 16 captured / 5 partial.
- [x] Migration audit reports 16 corpus sources / 18 artifacts / 18 verified payload files.
- [x] Migration audit reports 7 predicate rows with artifact evidence / 17 observed field evidences.
- [x] Migration audit reports 0 closing evidence / 0 candidate-ready rows.
- [ ] Final governance-head CI green after `STATUS.md` and this checklist are reconciled.
- [ ] PR #25 merged to `main`.
- [ ] Issue #24 closed as completed.
- [ ] Issue #16 remains open and BLOCKED with updated evidence boundary.

## Exit condition

Recovery 002 is complete when the final governance head is green and merged while:

```text
CLOSING_FIELD_EVIDENCE       = 0
CANDIDATE_READY_ROWS         = 0
NEW_ALPHA_CANDIDATE          = NOT_SELECTED
DETECTOR_ACTIVITY            = NOT_AUTHORIZED
BACKTEST_PNL                 = NOT_AUTHORIZED
V0_1_OOS_CONFIRM             = UNOPENED
PHASE_7                      = BLOCKED
```

The remaining work is not strategy implementation. Phase 6C may reopen only when a new or newly accessible first-party technical artifact closes a deterministic held predicate and passes the existing Phase-6D research gates.
