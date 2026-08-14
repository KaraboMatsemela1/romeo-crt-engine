# Phase 6B — Bullish Model #1 Evidence Gate

**Date:** 2026-08-13  
**Candidate:** `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH`  
**Status:** **OPEN / NON-EXECUTABLE**  
**Gate result:** `PENDING`

## Purpose

This gate prevents the project from converting a plausible directional mirror into an executable strategy by assumption.

The existing corpus contains meaningful evidence that bullish CRT and bullish Model #1 concepts exist, but the current project record still marks several bullish predicates as provisional or unresolved. Phase 6B must close those predicates from primary source material before code or historical outcome testing is authorized.

Discovery timestamps and third-party transcript/summary material may identify where to inspect the original video. They are not sufficient by themselves to upgrade a strategy predicate to `VERIFIED`.

## Governing principle

```text
CODE SYMMETRY != SOURCE EVIDENCE
```

A bearish rule may have a mathematically neat inverse and still be invalid as a claimed Romeo-derived rule unless the bullish behavior is directly supported.

If a required bullish predicate remains ambiguous:

```text
EVIDENCE_GATE = FAIL
v0.2 alpha coding = NOT AUTHORIZED
historical outcome access = NOT AUTHORIZED
```

## Required predicate closure

### BULL-01 — bullish parent reference

Question:

> Is an old / selected `CRTL` directly established as the relevant bullish reaction/manipulation reference for this D1 Candle-3 setup family?

Must resolve:

- owning parent timeframe;
- whether the reference is specifically C1 `CRTL` for the selected rolling-parent construction;
- what makes the reference valid/current;
- whether a prior touch consumes it;
- whether the source demonstrates this as rule, example, or optional context.

**Current status:** OPEN.

### BULL-02 — bullish Candle-2 manipulation and reclaim

Candidate mirror to verify, **not yet a rule**:

```text
C2.low < C1.low
C2.high <= C1.high
C1.low < C2.close <= C1.high
C2.high < C1 midpoint   # possible untouched-T1 mirror
```

Questions:

- must the low sweep be strict?
- must C2 avoid sweeping both sides?
- must C2 close back inside C1?
- does midpoint consumption invalidate the same way as the bearish candidate?
- is the completed C2 itself sufficient to establish bullish context for C3?

**Current status:** OPEN. Do not copy the bearish inequalities into code until verified or explicitly frozen as project parameters after evidence review.

### BULL-03 — bullish Model #1 core candle

The current indexed Episode-1 extraction suggests a directional inverse using a qualifying down-close candle around an old low, followed by a confirming close above the selected model candle.

Must directly verify:

- candle direction (`down-close` or another exact property);
- required interaction with old low / CRTL;
- whether wick, body or either may penetrate the reference;
- what price on the selected model candle forms the confirmation reference;
- whether confirmation must be the next H1 candle or may occur later within C3;
- whether a retrace is part of the core rule or an optional entry refinement;
- FVG role: core requirement, optional confluence or unrelated example.

**Current status:** PROVISIONAL / PRIMARY-SOURCE CHECK REQUIRED.

### BULL-04 — `thick` parameter treatment

v0.1 froze:

```text
body / full_range >= 0.50
```

for the bearish Model #1 research candidate.

Phase 6B must decide **before historical testing** whether:

1. the same project formalization is direction-neutral and is inherited unchanged; or
2. bullish source evidence requires a different definition; or
3. `thick` remains too ambiguous, blocking the candidate.

A different threshold may not be selected from v0.1 or v0.2 P&L/trade-count optimization.

**Current status:** OPEN GOVERNANCE DECISION.

### BULL-05 — bullish structural stop

Current Episode-9 research notes contain a demonstrated bullish framework with protection below the Turtle-Soup/structural low.

Must verify:

- exact structural object owning the stop reference: parent sweep low, Model #1 low, Turtle-Soup low, or another reference;
- whether the model candle may create a lower structural reference;
- whether one-tick execution buffer remains a direction-neutral project execution parameter.

**Current status:** PROVISIONAL-HIGH / EXACT OBJECT OPEN.

### BULL-06 — bullish target

First-party corpus supports a broader `CRTH/L -> 50%` relationship, but Phase 6B must establish that the selected bullish setup specifically uses the parent C1 midpoint as the pre-trade objective under the candidate's lifecycle.

Must verify:

- C1 midpoint as T1 for this setup subtype;
- whether target must be untouched before entry;
- whether a prior C2/C3 midpoint interaction consumes the setup;
- whether opposite extreme or another liquidity level supersedes midpoint in the demonstrated bullish example.

**Current status:** PARTIALLY SUPPORTED / SETUP-SPECIFIC RULE OPEN.

### BULL-07 — Candle-3 timing and expiry

The project may inherit the general causal rule that Candle 2 completes before Candle 3 becomes eligible, but direction-specific examples must not imply a different execution window.

Must resolve:

- confirmation occurs only after C2 close;
- no use of final C3 state at C3 open;
- whether the bullish entry expires at C3 close under this setup family;
- treatment of a target touch before H1 confirmation.

**Current status:** GENERAL TIMING HIGH-CONFIDENCE; BULLISH FIXTURE VERIFICATION REQUIRED.

## Primary-source verification queue

### Source 1 — `CRT secrets ep.1: One CRT model for life`

Canonical research record: `research/romeo/videos/ROMEO-2025-S1.md`.

Discovery hints from the existing indexed extraction:

- around `15:23`: bullish/bearish Model #1 examples;
- around `19:12`: Model #1 as a specific-candle object;
- around `19:24`: close/entry-trigger discussion;
- around `20:24`: bearish Model #1 recap useful for symmetry comparison.

**Required action:** inspect the original Romeo video/audio/chart frames at these regions and record exact observations. Timestamps are navigation hints only.

### Source 2 — `CRT secrets ep.9: Connecting the dots`

Canonical research record: `research/romeo/videos/ROMEO-2025-S9.md`.

Priority verification:

- demonstrated bullish Turtle-Soup / stop reference;
- relationship among SMT, manipulation and the approved entry model;
- exact structural object protected by the stop.

### Source 3 — first-party Romeo post: `CRTH/L -> 50%`

Use this to verify the broad extreme-to-midpoint doctrine, then determine whether the Episode-1 bullish Model #1 example belongs to that exact target family.

### Source 4 — first-party Romeo bullish CRT / bias-transition examples

Use these only to establish that bullish CRT states are explicit in the doctrine. They do not by themselves define the Model #1 entry geometry.

## Evidence recording requirements

For every promoted predicate, record:

```text
source ID / URL
source type
exact timestamp or post identifier
observation in neutral language
candidate rule derived from it
confidence
causal availability timestamp
contradictions / alternatives
promotion decision
```

Do not copy a summary's interpretation as if it were Romeo's exact language.

## Fixture gate

After source predicates close and **before historical backtesting**, build a minimum fixture set that includes:

### Positive fixtures

At least 3 independently distinct bullish cases:

1. clean CRTL sweep/reclaim + qualifying Model #1 + valid confirmation;
2. valid setup around a different candle geometry still inside the frozen definition;
3. valid case near a timing/session boundary without look-ahead.

### Negative fixtures

At least 5 rejection classes:

1. no strict qualifying parent sweep;
2. both parent extremes swept / ambiguous state;
3. target already consumed before confirmation;
4. wrong Model #1 candle direction/geometry;
5. no qualifying close confirmation before expiry.

Add further negative fixtures for every ambiguity uncovered during primary-source review.

## Deterministic specification gate

Gate 6B-1 can pass only if every required v0.2 order-path field is expressible without discretionary adjectives or future information.

Required machine-level decisions include:

```text
parent selector
calendar
key/reference level
parent manipulation
context direction
Model #1 selection
confirmation reference
entry timestamp/price rule
structural stop reference
execution buffer policy
target
target-consumption behavior
expiry
UNKNOWN behavior
```

## Gate outcome vocabulary

### `EVIDENCE_SUFFICIENT_TO_SPECIFY`

Use only when the primary-source review plus reconciliation supports a deterministic draft.

This authorizes **specification and fixtures**, not historical outcome access.

### `EVIDENCE_INSUFFICIENT`

Use if any critical predicate cannot be closed without inventing semantics.

If this occurs:

- preserve this failed research path;
- do not approximate the missing rule;
- return to the Phase-6B candidate-selection ledger and choose the next independently justified hypothesis.

## Current gate state

```text
BULL-01 parent reference          OPEN
BULL-02 C2 manipulation/reclaim   OPEN
BULL-03 Model #1 core             OPEN
BULL-04 thick parameter           OPEN
BULL-05 structural stop           OPEN
BULL-06 target                    OPEN
BULL-07 timing/expiry fixtures    OPEN

GATE 6B-1                         PENDING
V0.2 SPECIFICATION                NOT AUTHORIZED
V0.2 ALPHA IMPLEMENTATION         NOT AUTHORIZED
V0.2 HISTORICAL OUTCOME ACCESS    NOT AUTHORIZED
```
