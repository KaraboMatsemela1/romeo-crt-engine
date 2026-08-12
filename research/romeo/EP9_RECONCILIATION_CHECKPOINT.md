# Episode 9 Reconciliation Checkpoint

Date: 2026-08-12
Status: Phase 1 / post-Episode-9 checkpoint

## What is now sufficiently coherent to draft

The public CRT corpus through Episode 9 supports a coherent **draft** orchestration model:

```text
W1 → D1 → H4 causal context
        ↓
Parent CRT / candle state
        ↓
Key level + liquidity narrative
        ↓
Direction + target state
        ↓
Candle-2 close / Candle-3 eligibility
        ↓
Failure filters
  - direction conflict
  - Target-1 consumed state
  - confirmed SMT conflict
  - incomplete/unknown CRT
        ↓
Manipulation / cross-market state
  - Turtle Soup
  - qualifying SMT path
        ↓
Entry family
  - Model #1
  - True MSS
        ↓
Structural stop reference
        ↓
Narrative price target / governed time exit
        ↓
Independent risk engine
```

This is enough to begin a **draft strategy specification**, but not enough to freeze an executable implementation.

## Resolved enough for draft use

- Context must be established before entry-pattern detection.
- Initial parent-timeframe scope is H4/D1/W1; top-down notation is W1 → D1 → H4.
- Candle 2 must complete before Candle 3 becomes eligible.
- Candle-3 open is eligibility, not automatic entry.
- Key level is context, not entry.
- Directional alignment is a high-priority filter for the first candidate.
- 50% is Target 1 / a material state boundary; once reached, the original untouched setup state is consumed.
- SMT is not a standalone entry.
- SMT direction is filtered by higher-timeframe direction in the Episode-9 framework.
- The first public entry families are Model #1 and true MSS.
- Stop placement is structural rather than an arbitrary fixed-pip distance; Episode 9 demonstrates reference beyond a Turtle Soup extreme.
- Targets must be selected from the pre-trade narrative rather than chosen retrospectively.
- Price exits and time exits are distinct dimensions.
- `NO_SIGNAL` and pre-entry invalidation are valid terminal states.
- SMT-enabled backtesting requires synchronized multi-market replay.

## Hard blockers before deterministic implementation

### B1 — Model #1 exact predicate
Need source-backed answers for:
- qualifying candle geometry
- exact close condition
- exact retrace/entry price
- role of FVG
- bullish/bearish symmetry
- meaning of `thick`

### B2 — True MSS exact predicate
Need source-backed answers for:
- swing construction
- exact reference high/low
- wick vs close break
- exact entry zone
- relationship to SMT
- whether FVG is required

### B3 — Parent CRT selection/completeness
Need:
- exact Candle-1 selector
- exact Candle-2 manipulation completion
- exact `INCOMPLETE` vs `COMPLETE` predicate
- handling of nested/overlapping/inside-bar CRTs

### B4 — Key-level algorithm
Need:
- exact price/time key-level taxonomy
- level ranking across W1/D1/H4
- level-reached tolerance
- consumed/invalidation state

### B5 — SMT relationship registry
Need:
- verified market pair/group definitions
- correlated/inverse polarity
- reference-high/low matching
- synchronization window
- which instrument is traded after divergence
- local Turtle-Soup substitution conditions

### B6 — Time and candle calendar
Need:
- H4 anchors
- Daily open/close
- Weekly open/close
- DST policy
- instrument/venue calendar differences
- exact session/trading windows

### B7 — Stops and exits
Need:
- exact stop buffer beyond structural extreme
- Target-1/Target-2 hierarchy by setup family
- partial/breakeven policy if any
- exact time-exit predicate

### B8 — KOD ex-ante classifier
Need a real-time predicate that identifies a KOD candidate without using `last Turtle Soup before target` retrospectively.

## Explicit DO NOT IMPLEMENT YET

Do not freeze or optimize:

```text
Model #1 detector
True-MSS detector
KOD detector
SMT pair-direction rules
key-level ranking
stop buffer
session/time exit
complete CRT classifier
```

Any implementation before the above is resolved may exist only as a clearly tagged exploratory hypothesis and must not be presented as Romeo's verified strategy.

## First candidate setup family

Working candidate name:

`CRT-C3-ALIGNED-v0.1-DRAFT`

Scope:

```text
Directionally aligned Candle-3 CRT
+ valid parent context
+ valid key level
+ Candle 2 completed
+ target state valid
+ no confirmed SMT conflict
+ CRT complete
+ valid manipulation state
+ Model #1 OR true MSS
+ structural stop
+ narrative-defined target
```

Status: `DRAFT / BLOCKED`

## Next evidence step

1. Analyze Episode 10 for corpus completeness and close semantics.
2. Perform cross-episode contradiction matrix for Episodes 1–10.
3. Draft `CRT_STRATEGY_SPEC.md` with every unresolved rule explicitly marked.
4. Build a source/fixture list of chart examples to reproduce before broad backtesting.
