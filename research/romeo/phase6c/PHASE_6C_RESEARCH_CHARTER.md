# Phase 6C — 2026 Doctrine Research Charter

**Date:** 2026-08-14  
**Status:** **IN PROGRESS — 2026 SOURCE RECONCILIATION**  
**Predecessor:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Predecessor result:** `INSUFFICIENT_MULTI_MARKET_SAMPLE`  
**New alpha candidate selected:** **NO**  
**Historical detector-count access for a Phase-6C candidate:** **NOT AUTHORIZED**  
**Backtest / P&L / paper / shadow / live:** **NOT AUTHORIZED**

## Purpose

Phase 6B passed the provider, trusted-data and eligible-universe gates but terminated because the frozen strategy produced 7 pooled TradePlans versus the preregistered minimum of 30.

Phase 6C is a fresh evidence-reconciliation route. It may not repair Phase 6B by lowering thresholds, relaxing the frozen alpha, selecting instruments after observing activity, or changing parameters to manufacture more signals.

The independent research input is Romeo's first-party 2026 doctrine stream plus unresolved first-party evidence debts already recorded in the 2025 corpus.

## Immutable predecessor evidence

```text
Phase 6 v0.1
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
result     INSUFFICIENT_EVIDENCE
TradePlans 4 / required 30

Phase 6B
candidate  CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
result     INSUFFICIENT_MULTI_MARKET_SAMPLE
TradePlans 7 / required 30
trusted instruments 4 / 4
```

v0.1 OOS and CONFIRM remain unopened. Phase 6C does not authorize using them to select or tune a successor.

## Doctrine version boundary

Historical baseline:

```text
CRT_SECRETS_2025
```

New source stream:

```text
CRTOLOGY_2026_RESEARCH
```

No 2026 statement may silently rewrite historical strategy semantics. Every difference must be classified as:

```text
CLARIFICATION
REFINEMENT
NEW_OPTIONAL_BRANCH
SUPERSEDING_RULE
NON_ALPHA_CONTEXT
UNRESOLVED
```

First-party 2026 evidence also states that core CRT and Turtle Soup remain unchanged while the system gains refinements/nuances. Phase 6C therefore defaults to preserving the historical core unless direct evidence proves supersession.

## Completed Phase 6C source gates

### `ROMEO-2026-CRTOLOGY-01` — `CRTology episode 1: SS`

```text
video_id                           4DZWbCzEvhM
source identity                    CONFIRMED
first-party provenance             CONFIRMED
technical meaning of SS            NOT CAPTURED
gate result                        TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT
new executable delta               NONE
```

First-party post-episode clues were preserved—organised recognition, do-not-force language, strong-trend caution and weekly time-context observations—but remain non-executable.

Canonical evidence:

- `research/romeo/phase6c/CRTOLOGY_01_EVIDENCE_GATE.md`
- `research/romeo/phase6c/PRIMARY_SOURCE_PASS_001.md`

### `ROMEO-2026-LIVE-02` — `CRT live tape-reading session (2)`

```text
video_id                           Pmmx41M7KhA
source identity                    CONFIRMED
first-party provenance             CONFIRMED
technical/tape-reading intent      CONFIRMED
new deterministic order predicate NOT CAPTURED
gate result                        TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT
```

First-party surrounding material preserves selection-over-availability, exit-entry duality, quarter-as-candle framing and core-system continuity. The public source stream did not expose enough causal detail to implement a new rule.

Canonical evidence:

- `research/romeo/phase6c/LIVE_02_EVIDENCE_GATE.md`

## Active reconciliation ledger

All direct 2026 clues are compared against the 2025 doctrine in:

- `research/romeo/phase6c/DOCTRINE_RECONCILIATION_2026.md`

Current result:

```text
candidate_ready_rows = 0
```

No alpha candidate may be selected merely because a clue appears likely to increase historical activity.

## Active source-research priorities

The following are prioritized by direct-source relevance and historical evidence debt, not by historical profitability or expected count:

1. **SMT semantics and substitution** — first-party pair registry is now directly captured; first-party follow-up also confirms a case where SMT performed the manipulation role without the expected local Turtle Soup. Exact divergence polarity, synchronization and execution ownership still require closure.
2. **Dynamic context / bias transition** — direct first-party evidence says a convincing opposite CRT can justify changing bias and cautions against fading strong trends without warning signs; `convincing`/trend-state predicates remain unresolved.
3. **Time-context / weekly organisation** — first-party weekday observations exist but are not yet a deterministic state machine.
4. **Exit-entry structural theory** — explicitly named by Romeo, but causal lifecycle remains unavailable in public text.
5. **Quarterly parent/fractality expansion** — directly stated as a concept, but calendar/execution mapping remains unresolved.

## Candidate-selection rule

Phase 6C may select a successor only when a proposed delta is:

1. directly motivated by pre-outcome first-party evidence;
2. causally deterministic;
3. narrow enough to isolate one hypothesis;
4. compatible with trusted data or accompanied by a separately qualified data requirement;
5. frozen before detector activity or P&L is opened; and
6. not selected because it is expected to increase trade count.

If no source branch closes all strategy-critical fields, Phase 6C must record `NO_EXECUTABLE_DELTA` rather than force a candidate.

## Gate sequence

### Gate 6C-1 — technical source capture

For each source/branch, require exact identity, first-party provenance and technical evidence sufficient to avoid guessing.

Possible source-gate result:

```text
TECHNICAL_SOURCE_CAPTURE_SUFFICIENT
TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT
```

### Gate 6C-2 — semantic extraction

Any candidate rule must freeze:

- deterministic predicate;
- information-availability timestamp;
- timeframe/direction ownership;
- lifecycle/expiry;
- positive examples;
- negative/counterexamples;
- unknown/fail-closed behavior.

No unresolved field may remain on the proposed signal path.

### Gate 6C-3 — 2025 vs 2026 reconciliation

Compare against:

- `strategy/CRT_V0.1_SPEC.md`;
- `research/romeo/reconciliation/RULE_EVIDENCE_MATRIX.md`;
- `research/romeo/OPEN_QUESTIONS.md`;
- Phase 6B decisions.

No silent overwrite.

### Gate 6C-4 — candidate precommitment

Only after Gates 6C-1 through 6C-3 pass may Phase 6C create a named candidate. Precommit exact rule delta, inherited/excluded rules, universe, calendars/timeframes, data requirements, activity threshold and outcome-access policy.

### Gate 6C-5 — implementation and validation planning

Only after precommitment:

- create a new strategy version;
- write positive/negative fixtures before historical detector outcomes;
- implement without mutating v0.1/v0.2 history;
- prove fixture parity;
- preregister detector-only activity protocol;
- keep P&L closed until a separate future authorization gate.

## Anti-overfit invariants

```text
LOWER_ACTIVITY_THRESHOLD_TO_REPAIR_6B      = false
MUTATE_V0_1_OR_V0_2_IN_PLACE               = false
SELECT_RULE_BY_HISTORICAL_TRADE_COUNT       = false
SELECT_RULE_BY_HISTORICAL_PNL               = false
OPEN_V0_1_OOS_OR_CONFIRM                    = false
PARAMETER_OPTIMIZATION                      = false
POST_OUTCOME_INSTRUMENT_SELECTION           = false
PHASE6C_ALPHA_IMPLEMENTATION_AUTHORIZED     = false
PHASE6C_DETECTOR_ACTIVITY_AUTHORIZED        = false
BACKTEST_AUTHORIZED                         = false
MULTI_MARKET_PNL_OUTCOME_ACCESS             = false
PAPER_TRADING_AUTHORIZED                    = false
SHADOW_TRADING_AUTHORIZED                   = false
LIVE_TRADING_AUTHORIZED                     = false
```

## Current handoff

```text
Phase 6C                         IN PROGRESS — 2026 SOURCE RECONCILIATION
Episode-1 gate                   CLOSED — TECHNICAL CAPTURE INSUFFICIENT
Live-02 gate                     CLOSED — TECHNICAL CAPTURE INSUFFICIENT
2025 doctrine                    PRESERVED
2026 reconciliation ledger       ACTIVE
Next evidence priority           SMT SEMANTICS / SUBSTITUTION
New alpha candidate              NOT SELECTED
Detector activity                NOT AUTHORIZED
P&L / backtest                   NOT AUTHORIZED
Phase 7                          BLOCKED
```
