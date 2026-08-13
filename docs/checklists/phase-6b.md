# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS**  
**Selected research target:** `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH`  
**Phase 7:** **BLOCKED UNTIL A FUTURE CANDIDATE PASSES VALIDATION**

## A. Preserve predecessor evidence

- [x] Preserve `CRT-C3-D1-H1-M1-BEAR-v0.1` unchanged.
- [x] Preserve the Phase-6 `INSUFFICIENT_EVIDENCE` disposition.
- [x] Keep v0.1 OOS outcomes unopened.
- [x] Keep v0.1 CONFIRM outcomes unopened.
- [x] Keep parameter optimization disabled for v0.1.
- [x] Keep paper, shadow and live trading unauthorized.

## B. Candidate-selection precommitment

- [x] Review the post-Phase-2 evidence-debt ledger.
- [x] Review deferred direction, timeframe, entry-family, SMT, KOD and management variants.
- [x] Reject H4/W1 expansion while H4 anchors remain unresolved.
- [x] Reject True MSS expansion while the Romeo-specific structural algorithm remains unresolved.
- [x] Reject SMT/KOD/countertrend/journey-to-level bundling for the first successor.
- [x] Prohibit tuning v0.1 numerical parameters merely to increase trade count.
- [x] Select one isolated successor research hypothesis before any v0.2 outcome access.
- [x] Record `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH` as the selected research target.

## C. Gate 6B-1 — bullish primary-source evidence

- [ ] Verify bullish `old CRTL` / parent-reference semantics from primary source material.
- [ ] Verify bullish Candle-2 sweep/reclaim semantics.
- [ ] Verify whether double-sided parent sweeps invalidate the bullish setup.
- [ ] Verify bullish midpoint/T1 consumption semantics.
- [ ] Verify bullish Model #1 candle direction and reference interaction.
- [ ] Verify exact bullish Model #1 confirmation reference.
- [ ] Verify confirmation timing and expiry within Candle 3.
- [ ] Verify FVG role for the selected Model #1 subtype.
- [ ] Verify bullish structural stop reference.
- [ ] Decide whether the one-tick execution buffer is inherited unchanged as direction-neutral execution policy.
- [ ] Verify parent 50% as the selected setup's pre-trade target.
- [ ] Resolve all contradictions against the canonical evidence matrix.
- [ ] Record neutral source observations with timestamp/post provenance.
- [ ] Produce Gate 6B-1 written decision: `EVIDENCE_SUFFICIENT_TO_SPECIFY` or `EVIDENCE_INSUFFICIENT`.

## D. Gate 6B-2 — deterministic v0.2 specification

**Blocked until Gate 6B-1 passes.**

- [ ] Assign final strategy version ID.
- [ ] Write `CRT_V0.2_SPEC.md` without modifying the v0.1 specification.
- [ ] Define every order-path predicate deterministically.
- [ ] Separate source-derived rules from project parameters.
- [ ] Define `UNKNOWN -> NO_SIGNAL` for all critical state.
- [ ] Freeze calendar/version dependencies.
- [ ] Freeze target and stop semantics before outcome access.
- [ ] Define exact strategy expiry.
- [ ] Create a v0.2 evidence/rule matrix.
- [ ] Conduct independent freeze review.

## E. Gate 6B-2 fixtures

- [ ] Create at least 3 positive bullish fixtures before historical outcome testing.
- [ ] Create at least 5 negative bullish fixture classes before historical outcome testing.
- [ ] Include no-sweep rejection.
- [ ] Include double-sweep/ambiguous rejection.
- [ ] Include target-consumed rejection.
- [ ] Include Model #1 geometry rejection.
- [ ] Include no-confirmation-before-expiry rejection.
- [ ] Include causal timestamp assertions.
- [ ] Demonstrate deterministic repeated fixture results.

## F. Gate 6B-3 — implementation and compatibility

**Blocked until strategy/fixture freeze.**

- [ ] Implement v0.2 contracts separately from `v0_1.py`.
- [ ] Preserve v0.1 regression suite unchanged.
- [ ] Add v0.2 unit tests.
- [ ] Add v0.2 detector tests.
- [ ] Confirm no future D1/H1 information leaks into decisions.
- [ ] Confirm detector emits immutable TradePlans.
- [ ] Confirm simulator consumes v0.2 plans without reimplementing alpha validity.
- [ ] Confirm costs, sizing, same-bar handling and gap behavior are not changed to improve results.
- [ ] Freeze detector implementation/version if parity passes.
- [ ] Freeze simulator compatibility/version if required.

## G. Gate 6B-4 — new validation preregistration

**No validation outcome access until complete.**

- [ ] Define a new v0.2 DEV window policy.
- [ ] Define a new v0.2 OOS window policy.
- [ ] Define a new final-confirmatory window policy.
- [ ] Explicitly decide whether any v0.1 reserved window may be reused; default is **NO AUTHORIZATION**.
- [ ] Freeze minimum sample/activity gates before results.
- [ ] Freeze friction scenarios before results.
- [ ] Freeze sensitivity plan before results.
- [ ] Freeze walk-forward / robustness gates before results.
- [ ] Freeze Monte Carlo eligibility threshold before results.
- [ ] Freeze promotion/rejection decision rules before results.
- [ ] Independently review leakage and overfit controls.
- [ ] Seal data identity before outcome access.

## H. Promotion boundary

- [ ] Do not start Phase 7 unless a candidate receives `PROMOTE_TO_PAPER_CANDIDATE` from its own validation protocol.
- [ ] Do not treat sufficient trade count as proof of edge.
- [ ] Do not treat positive DEV P&L as permission to skip OOS/confirmatory gates.
- [ ] Do not combine bearish and bullish candidates without separately defining interaction/portfolio semantics.
- [ ] Keep hard risk controls independent from strategy scoring.
- [ ] Keep live trading disabled until the full roadmap authorizes it.

## Current handoff

```text
Phase 6B                       IN PROGRESS
Candidate selection            COMPLETE
Selected research hypothesis   BULLISH D1 -> H1 MODEL #1
Primary-source evidence gate   OPEN
v0.2 specification             BLOCKED
v0.2 implementation            BLOCKED
v0.2 historical backtest       BLOCKED
Phase 7                        BLOCKED
```
