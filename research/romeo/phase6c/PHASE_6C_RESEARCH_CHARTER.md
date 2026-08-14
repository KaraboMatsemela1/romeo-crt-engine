# Phase 6C — CRTology 2026 Research Charter

**Date:** 2026-08-14  
**Status:** **IN PROGRESS — PRIMARY-SOURCE EVIDENCE GATE**  
**Predecessor:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Predecessor result:** `INSUFFICIENT_MULTI_MARKET_SAMPLE`  
**New alpha candidate selected:** **NO**  
**Historical detector-count access for a Phase-6C candidate:** **NOT AUTHORIZED**  
**Backtest / P&L / paper / shadow / live:** **NOT AUTHORIZED**

## Purpose

Phase 6B completed the provider, trusted-data and multi-market activity gates successfully but terminated because the frozen strategy produced 7 pooled TradePlans versus the preregistered minimum of 30.

Phase 6C must not repair that result by lowering thresholds, relaxing the frozen alpha, selecting instruments after observing activity, or changing numerical parameters to manufacture more signals.

The next independently motivated research input is new first-party Romeo material published under the **2026 CRTology** series. The repository already registered `ROMEO-2026-CRTOLOGY-01` as `DISCOVERED`, but no technical evidence pass has yet decoded the title term `SS` or established whether the episode changes any executable CRT predicate.

Phase 6C therefore begins as an **evidence-reconciliation phase**, not a strategy-implementation phase.

## Immutable predecessor evidence

The following results remain historical and may not be rewritten:

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

The Phase-6 v0.1 OOS and CONFIRM windows remain unopened. Phase 6C does not authorize using them to select or tune a successor.

## Doctrine version boundary

The 2025 baseline remains:

```text
CRT_SECRETS_2025
```

New CRTology material is initially quarantined under:

```text
CRTOLOGY_2026_RESEARCH
```

No 2026 statement may silently rewrite the 2025 strategy specification. A difference must be classified as one of:

```text
CLARIFICATION
REFINEMENT
NEW_OPTIONAL_BRANCH
SUPERSEDING_RULE
NON_ALPHA_CONTEXT
UNRESOLVED
```

Only a source-supported and causally specifiable delta may become a future strategy candidate.

## Phase 6C source priority

Primary target:

```text
source_id  ROMEO-2026-CRTOLOGY-01
title      CRTology episode 1: SS
video_id   4DZWbCzEvhM
status     EVIDENCE GATE OPEN
```

Supporting first-party source stream:

- Romeo official Telegram publication/corroboration of the video identity;
- Romeo's CRTology introduction video;
- later CRTology episodes only when they are actually published and source-verified;
- source-linked chart frames/posts where they clarify the same predicate.

Third-party summaries may be used only for discovery. They cannot independently authorize an executable rule.

## Questions that must be answered before candidate selection

1. What does `SS` mean in Romeo's 2026 terminology?
2. Is `SS` an alpha predicate, a context state, an entry model, a session/time concept, or non-alpha teaching language?
3. What exact inputs make an `SS` state/event true or false?
4. At what timestamp does the state become knowable?
5. Does the rule depend on active-candle information that would create look-ahead if backtested naively?
6. Does it change parent CRT selection, key-level selection, direction, Turtle Soup, Model #1, true MSS, SMT, target state, or timing?
7. Does it refine a 2025 rule or introduce a genuinely new branch?
8. Is the rule symmetric across bullish/bearish direction, or does source evidence distinguish them?
9. What positive and negative examples are directly observable?
10. Can the rule be implemented without discretionary adjectives, hindsight selection or outcome-based ranking?

## Candidate-selection rule

Phase 6C may select a successor only after the evidence gate closes and only when the proposed delta is:

1. directly motivated by pre-outcome Romeo evidence;
2. causally deterministic;
3. narrow enough to isolate one hypothesis;
4. compatible with trusted data or accompanied by a separately qualified data requirement;
5. fixed before detector activity/P&L is opened; and
6. not chosen because it is expected to increase trade count.

If CRTology Episode 1 does not provide a deterministic alpha delta, Phase 6C must record that result honestly and continue source research rather than forcing a candidate.

## Gates

### Gate 6C-1 — source identity and technical capture

Require:

- exact source/video identity;
- first-party provenance;
- publication ordering;
- direct transcript/caption/frame evidence sufficient to interpret the technical lesson;
- no guessed meaning for `SS`.

Exit:

```text
TECHNICAL_SOURCE_CAPTURE_SUFFICIENT
or
TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT
```

### Gate 6C-2 — semantic extraction

For every candidate rule, record:

- source evidence;
- deterministic predicate;
- information-availability time;
- lifecycle/expiry;
- positive examples;
- negative/counterexamples;
- confidence level;
- unresolved fields.

Exit only if no unresolved value lies on the proposed signal path.

### Gate 6C-3 — 2025 vs 2026 reconciliation

Compare any extracted rule against:

- `strategy/CRT_V0.1_SPEC.md`;
- `research/romeo/reconciliation/RULE_EVIDENCE_MATRIX.md`;
- deferred branches recorded by Phase 1/2;
- Phase 6B bullish and multi-market decisions.

No silent overwrite is allowed.

### Gate 6C-4 — candidate precommitment

Only after Gates 6C-1 through 6C-3 pass may Phase 6C create a named strategy research candidate.

The precommitment must freeze:

- exact rule delta;
- inherited rules;
- excluded rules;
- market universe;
- timeframes/calendars;
- data requirements;
- activity threshold;
- outcome access policy.

### Gate 6C-5 — implementation and validation planning

Only after candidate precommitment:

- create deterministic spec and fixtures;
- implement in a new version without mutating v0.1/v0.2 history;
- prove fixture parity;
- preregister detector/activity protocol;
- keep P&L closed until its own future authorization gate.

## Anti-overfit invariants

```text
LOWER_ACTIVITY_THRESHOLD_TO_REPAIR_6B      = false
MUTATE_V0_1_OR_V0_2_IN_PLACE               = false
SELECT_RULE_BY_HISTORICAL_TRADE_COUNT       = false
SELECT_RULE_BY_HISTORICAL_PNL               = false
OPEN_V0_1_OOS_OR_CONFIRM                    = false
PARAMETER_OPTIMIZATION                      = false
POST_OUTCOME_INSTRUMENT_SELECTION           = false
BACKTEST_AUTHORIZED                         = false
MULTI_MARKET_PNL_OUTCOME_ACCESS             = false
PAPER_TRADING_AUTHORIZED                    = false
SHADOW_TRADING_AUTHORIZED                   = false
LIVE_TRADING_AUTHORIZED                     = false
```

## Immediate handoff

```text
Phase 6C                         IN PROGRESS — PRIMARY-SOURCE EVIDENCE GATE
New alpha candidate              NOT SELECTED
Primary research target          ROMEO-2026-CRTOLOGY-01
Technical meaning of SS          UNRESOLVED
2025 doctrine                    PRESERVED
Phase 6B terminal result         PRESERVED
Detector activity                NOT AUTHORIZED
P&L / backtest                   NOT AUTHORIZED
Phase 7                          BLOCKED
```
