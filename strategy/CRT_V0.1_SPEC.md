# CRT v0.1 Strategy Specification

**Candidate name:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine version:** `CRT_SECRETS_2025`  
**Status:** DRAFT / RECONCILIATION / NOT FROZEN / NOT VERIFIED  
**Live trading:** NOT AUTHORIZED  
**Validation:** NOT AUTHORIZED until active-path blockers are resolved

## 1. Purpose

This specification is the first integrated strategy draft produced from the 2024 Romeo CRT foundation material and 2025 `CRT Secrets` Episodes 1–10.

It is intentionally narrower than the full public doctrine. The purpose is to define the smallest causally testable Candle-3 candidate while preserving unresolved semantics as explicit blockers.

This document must not be interpreted as a claim that the strategy is profitable or ready for trading.

## 2. Evidence policy

Rule statuses:

- `VERIFIED` — direct primary evidence + deterministic predicate
- `HIGH_CONFIDENCE` — strong cross-source support; narrow direct-source verification still required
- `PROVISIONAL` — source-backed but materially ambiguous
- `HYPOTHESIS` — inference requiring explicit testing/evidence
- `UNRESOLVED` — must not enter executable order path
- `ENGINEERING_CONSTRAINT` — causality/safety requirement rather than alpha rule

Supporting reconciliation artifacts:

- `research/romeo/reconciliation/RULE_EVIDENCE_MATRIX.md`
- `research/romeo/reconciliation/CONTRADICTION_MATRIX.md`
- `research/romeo/reconciliation/BLOCKER_PRIORITY.md`
- `research/romeo/PHASE_1_RECONCILIATION_CHECKPOINT.md`

## 3. Scope of first candidate

### Included

- doctrine snapshot: 2025 CRT Secrets
- setup phase: Candle 3 only
- direction: HTF-aligned only
- initial parent-candle universe: H4, D1, W1
- top-down notation: `W1 → D1 → H4`
- context-first orchestration
- key-level requirement
- Candle-2-close gate
- local Turtle Soup manipulation path for the minimal candidate
- one or both approved entry families once deterministic:
  - Model #1
  - true MSS
- structural stop reference
- predeclared price targets
- independent risk approval
- complete candidate/rejection/no-signal journaling

### Explicitly excluded from first minimal executable version unless separately verified

- countertrend CRT
- Candle-2 trading
- retrospective KOD labeling
- KOD as required setup condition
- SMT substitution for missing local Turtle Soup
- time exits unless directly specified
- monthly/multi-month parent candles
- generic order-block/breaker/FVG entries
- generic retail BOS/MSS substituted for Romeo true MSS
- `clean close` signal
- machine-learning trade override

## 4. Strategy invariants

These are architecture/safety invariants and should be implemented before alpha logic.

1. No signal may use data unavailable at its decision timestamp.
2. Final parent-candle OHLC cannot be used before the candle closes.
3. Higher-timeframe context exists before lower-timeframe entry detection.
4. Key-level/context state exists before entry-model scanning can produce a candidate.
5. Candle 2 must close before Candle 3 becomes eligible.
6. Candle-3 open does not equal entry.
7. SMT can never directly emit an order.
8. KOD can never be labeled using future target knowledge.
9. Target plan must be selected before trade outcome is known.
10. `NO_SIGNAL` is a valid terminal state.
11. Any `UNKNOWN` state on a required active-path predicate fails closed.
12. Risk engine remains independent of strategy confidence.

## 5. Data and calendar prerequisites

### 5.1 Canonical timeframes

Initial parent scope:

```text
W1
D1
H4
```

Hierarchy notation:

```text
W1 → D1 → H4 → execution timeframe
```

**Important:** the exact execution timeframe beneath each parent and exact H4/D1/W1 session anchors remain unresolved.

### 5.2 Candle construction — BLOCKED

Required before backtesting:

```python
CandleCalendar(
    timezone,
    h4_anchor_times,
    daily_open,
    daily_close,
    weekly_open,
    weekly_close,
    dst_policy,
    instrument_session_policy,
)
```

Status: `UNRESOLVED / P0-03`

Provider-native bars must not be assumed equivalent until verified.

### 5.3 Causal candle snapshot

For an active candle at time `t`:

```python
CandleSnapshot(
    timeframe,
    open_time,
    scheduled_close_time,
    open_price,
    high_so_far,
    low_so_far,
    current_price,
    observed_at,
)
```

Final close/high/low/body/wick values are unavailable until the relevant information actually exists.

## 6. Core domain objects

### 6.1 Parent CRT

```python
CRTContext(
    parent_crt_id,
    doctrine_version,
    instrument,
    context_timeframe,
    parent_candle_id,
    range_high,
    range_low,
    midpoint_50,
    context_direction,
    completion_state,
    target1_status,
    target2_status,
    selected_at,
    evidence_ids,
)
```

Blocked fields:

- parent-candle selector: `P0-01`
- context direction: `P0-05`
- completion predicate: `P2-04` unless excluded by stricter parent definition

### 6.2 Key level

```python
KeyLevel(
    key_level_id,
    source_timeframe,
    level_type,
    price_or_range,
    time_window,
    role,                 # DESTINATION | REACTION_ORIGIN
    state,                # PENDING | REACHED | CONSUMED | INVALID
    valid_from,
    invalidated_at,
    evidence_ids,
)
```

Status: `UNRESOLVED / P0-02`

No generic support/resistance replacement is authorized.

### 6.3 Turtle Soup event

```python
TurtleSoupEvent(
    event_id,
    parent_crt_id,
    reference_extreme_id,
    direction,
    sweep_timestamp,
    sweep_price,
    confirmation_timestamp,
    confirmation_type,
    structural_extreme,
    evidence_available_at,
)
```

Status: `UNRESOLVED / P0-04`

The detector must define qualifying reference extreme, sweep and continuation-failure semantics before use.

### 6.4 SMT state

```python
SMTState(
    relationship_id,
    primary_instrument,
    comparison_instrument,
    reference_type,
    direction,
    status,               # NONE | CANDIDATE | CONFIRMED | CONFLICT | UNKNOWN
    observed_at,
    stale_guard_passed,
    evidence_ids,
)
```

For the minimal first executable candidate:

```text
allow_smt_substitution = False
```

SMT may be journaled as context, but it may not replace required local manipulation until P2-01/P2-02 are resolved.

### 6.5 TradePlan

```python
TradePlan(
    plan_id,
    created_at,
    strategy_version,
    doctrine_version,
    instrument,
    direction,
    context_timeframe,
    trade_candle_timeframe,
    execution_timeframe,
    parent_crt_id,
    key_level_id,
    manipulation_event_id,
    entry_model,
    entry_reference,
    stop_reference,
    price_targets,
    time_exit_policy,
    invalidation_reasons,
    evidence_ids,
)
```

A `TradePlan` must be immutable once submitted to the risk engine.

## 7. Candidate state machine

```text
WAIT_FOR_CALENDAR_READY
        ↓
WAIT_FOR_PARENT_CONTEXT
        ↓
PARENT_CRT_SELECTED
        ↓
WAIT_FOR_KEY_LEVEL
        ↓
KEY_LEVEL_QUALIFIED
        ↓
DIRECTION_ALIGNED?
    ├── NO → REJECT_COUNTERTREND
    ↓ YES
TARGET_STATE_VALID?
    ├── NO → REASSESS_OR_REJECT
    ↓ YES
WAIT_FOR_CANDLE_2_CLOSE
        ↓
CANDLE_2_CLOSED
        ↓
CANDLE_3_OPENED
        ↓
C3_ELIGIBLE
        ↓
CRT_COMPLETE / REQUIRED STATE KNOWN?
    ├── NO/UNKNOWN → REJECT_UNKNOWN_CONTEXT
    ↓ YES
CONFIRMED SMT CONFLICT?
    ├── YES → INVALIDATE_OR_DOWNGRADE
    ↓ NO
WAIT_FOR_LOCAL_TURTLE_SOUP
        ↓
LOCAL_MANIPULATION_CONFIRMED
        ↓
WAIT_FOR_ENTRY_MODEL
    ├── MODEL_1
    └── TRUE_MSS
        ↓
ENTRY_CONFIRMED
        ↓
BUILD_IMMUTABLE_TRADE_PLAN
        ↓
RISK_CHECK
    ├── DENIED → JOURNAL_RISK_REJECT
    ↓ APPROVED
ORDER_INTENT
        ↓
POSITION_MANAGEMENT
        ↓
EXIT
        ↓
JOURNAL_OUTCOME
```

Any eligible context that expires without an entry transitions to:

```text
C3_NO_SIGNAL
```

not a forced trade.

## 8. Directional alignment

### Candidate policy

```text
allow_countertrend = False
```

Required:

```python
context_direction ∈ {BULLISH, BEARISH, NEUTRAL, UNKNOWN}
```

Candidate direction must match context direction.

If direction is `NEUTRAL` or `UNKNOWN`:

```text
NO TRADE
```

Status of direction algorithm: `UNRESOLVED / P0-05`.

## 9. Candle 2 → Candle 3 gate

High-confidence candidate rule:

```text
Candle 2 must be complete before Candle 3 is eligible.
```

At Candle-3 open the engine may know:

- prior candle histories
- final Candle-2 values
- Candle-3 open/time
- pre-existing context/key-level/target state

It may not know:

- Candle-3 eventual high
- Candle-3 eventual low
- Candle-3 eventual close
- Candle-3 eventual success/failure

Therefore:

```text
C3_OPENED → C3_ELIGIBLE
```

never:

```text
C3_OPENED → ENTER
```

Status: `HIGH_CONFIDENCE`, direct-source verification still required before freeze.

## 10. Key-level gate — BLOCKED

A Candle-3 candidate requires a valid key-level/narrative state.

The project currently distinguishes:

```text
DESTINATION key level
REACTION_ORIGIN key level
```

But exact calculation/ranking remains `P0-02`.

Prohibited shortcut:

```python
key_level = nearest_support_resistance
```

unless directly source-backed and frozen.

## 11. Target state

### 11.1 Midpoint

For a parent range:

```python
midpoint_50 = (range_high + range_low) / 2
```

### 11.2 Target-1 state

Current high-confidence doctrine:

```text
T1_PENDING
   ↓ price reaches 50% under applicable setup semantics
T1_REACHED
```

Reaching 50% changes the original setup state. The engine must not keep pretending the pristine T1 premise is untouched.

### 11.3 Do not force 50% as universal entry touch

The project will calculate 50% on every parent CRT but will not encode:

```python
price_must_touch_50_before_entry = True
```

without setup-specific evidence.

### 11.4 Target hierarchy — BLOCKED

Possible narrative objectives appearing in the corpus include:

- 50% midpoint
- opposite CRT extreme
- prior day high/low
- key-level / liquidity objectives

The exact setup-family hierarchy is `P1-03`.

Every target used in a backtest must be frozen before the test begins.

## 12. Manipulation path

### Minimal v0.1 policy

Require a deterministic local Turtle Soup event after the candidate context is valid.

```text
require_local_turtle_soup = True
allow_smt_substitution = False
```

This is a project scope decision to reduce ambiguity, not a claim that Romeo never uses SMT substitution.

Turtle Soup detector remains `P0-04`.

## 13. SMT policy

### Architecture rules

- SMT requires explicit related-market relationships.
- synchronized causal data is required.
- stale comparison data => `SMT = UNKNOWN`.
- SMT cannot directly generate an order.
- HTF direction filters SMT interpretation.

### First minimal candidate

SMT may be logged as:

```text
NONE | SUPPORTIVE | CONFLICT | UNKNOWN
```

but no SMT-dependent trade path is allowed until pair/polarity semantics are resolved.

If a directly verified `CONFIRMED SMT CONFLICT` predicate is later activated, it may invalidate/downgrade the pending CRT before entry.

## 14. Entry models

Entry-family whitelist:

```text
MODEL_1
TRUE_MSS
```

No other entry type is allowed in v0.1 without a new strategy version.

### 14.1 Model #1 — BLOCKED

Current safe abstraction:

```text
QUALIFYING SPECIFIC CANDLE
        ↓
REQUIRED CLOSE / DISPLACEMENT
        ↓
RETRACE INTO MODEL-1 AREA
        ↓
ENTRY CANDIDATE
```

Unresolved (`P1-01`):

- `thick` definition
- body/wick geometry
- old-extreme relation
- exact close predicate
- exact retrace region
- bullish/bearish mirror
- FVG role

No numerical proxy may be invented to close these gaps.

### 14.2 True MSS — BLOCKED

Current safe abstraction:

```text
QUALIFIED CONTEXT / MANIPULATION
        ↓
LTF STRUCTURAL SEQUENCE
        ↓
BREAK OF SPECIFIC REFERENCE SWING
        ↓
TRUE_MSS_CONFIRMED
        ↓
ENTRY REGION
```

Unresolved (`P1-02`):

- swing construction
- exact reference high/low
- wick vs close break
- entry region
- relation to SMT/Turtle Soup/FVG

Generic BOS/MSS logic is explicitly prohibited as a substitute.

## 15. Stop-loss policy

Current candidate principle:

```text
stop reference = qualifying structural invalidation extreme
```

Episode 9 supports a bullish example below the Turtle Soup low.

Represent separately:

```python
StructuralStop(
    reference_type,
    reference_price,
    side,
    buffer_policy,
)
```

The strategy source determines the structural reference. Execution policy determines any approved buffer.

Exact buffer and bearish mirror: `P1-04`.

## 16. Exit policy

### Price exits

Allowed only if predeclared in `TradePlan`.

### Time exits

Status: unresolved.

For the first deterministic candidate, time exits should be disabled unless directly specified before backtesting.

Prohibited:

```text
select historically best exit timestamp after observing results
```

## 17. Invalidation and no-trade states

Pre-entry candidate may terminate as:

```text
REJECT_COUNTERTREND
REJECT_INVALID_KEY_LEVEL
REJECT_TARGET_STATE_CONSUMED
REJECT_SMT_CONFLICT
REJECT_INCOMPLETE_CONTEXT
REJECT_UNKNOWN_CONTEXT
REJECT_DATA_STALE
C3_NO_SIGNAL
RISK_REJECTED
```

These are not strategy losses unless an actual position was opened.

## 18. Outcome model

Trade/candidate analytics must preserve at least:

```text
NO_ENTRY
INVALIDATED_PRE_ENTRY
RISK_REJECTED
STOPPED_BEFORE_T1
T1_REACHED
T1_REACHED_T2_REACHED
T1_REACHED_T2_NOT_REACHED
INVALIDATED_AFTER_ENTRY
TIME_EXIT
DATA_FAILURE
```

A trade that reaches T1 and not T2 must not be mislabeled as equivalent to a trade stopped before T1.

## 19. Backtesting causality rules

Mandatory:

1. event-time replay
2. no future parent-candle OHLC
3. no future swing/reference selection
4. no retrospective Candle-1/2/3 labels as inputs
5. no `last_turtle_soup_before_target`
6. fixed target policy before each experiment
7. fixed pair registry before SMT experiments
8. synchronized cross-market observations
9. stale stream => unknown/fail closed
10. fixed strategy version throughout test segment
11. transaction costs, spread and slippage modeled separately

## 20. Candidate rule register

| Rule ID | Category | Status | Draft statement | Blocker |
|---|---|---|---|---|
| CRT-001 | Calendar | UNRESOLVED | Canonical H4/D1/W1 construction must be defined. | P0-03 |
| CRT-002 | Parent CRT | UNRESOLVED | Select parent CRT/candle causally. | P0-01 |
| CRT-003 | Context | UNRESOLVED | Compute HTF direction. | P0-05 |
| CRT-004 | Key level | UNRESOLVED | Select/rank valid key level before LTF entry scan. | P0-02 |
| CRT-005 | Phase | HIGH_CONFIDENCE | Candle 2 closes before Candle 3 becomes eligible. | direct-source check |
| CRT-006 | Direction | HIGH_CONFIDENCE / BLOCKED | Reject countertrend candidates. | depends CRT-003 |
| CRT-007 | Target state | HIGH_CONFIDENCE | Track parent midpoint and T1 consumed state. | setup-specific T1 verification |
| CRT-008 | Turtle Soup | UNRESOLVED | Require deterministic local Turtle Soup for minimal v0.1. | P0-04 |
| CRT-009 | SMT | HIGH_CONFIDENCE / SCOPED OUT | SMT cannot directly enter; substitution disabled initially. | P2-01/P2-02 |
| CRT-010 | Entry family | HIGH_CONFIDENCE | Entry whitelist = Model #1 or true MSS. | internal rules unresolved |
| CRT-011 | Model #1 | UNRESOLVED | Specific-candle close/retrace entry. | P1-01 |
| CRT-012 | True MSS | UNRESOLVED | Context-qualified structural entry. | P1-02 |
| CRT-013 | Stop | PROVISIONAL-HIGH | Structural stop reference beyond invalidation extreme. | P1-04 |
| CRT-014 | Target | UNRESOLVED | Predeclared narrative target hierarchy. | P1-03 |
| CRT-015 | C3 expiry | UNRESOLVED | Eligible setup may expire to `C3_NO_SIGNAL`. | P1-05 |
| CRT-016 | KOD | EXCLUDED | Not required for first v0.1. | P2-03 |
| CRT-017 | Incomplete CRT | FAIL-CLOSED | Unknown completeness cannot authorize a trade. | P2-04 |
| CRT-018 | Time exit | EXCLUDED UNTIL VERIFIED | No invented time exit. | P2-05 |
| CRT-019 | Causality | ENGINEERING_CONSTRAINT | Information available at `t` only. | none |
| CRT-020 | Risk | ENGINEERING_CONSTRAINT | Independent risk engine decides permission. | none |

## 21. Independent risk boundary

The strategy may only produce a `TradePlan`.

```text
STRATEGY
   ↓
TradePlan
   ↓
RISK ENGINE
   ↓
OrderIntent or Denial
```

The risk engine may deny any otherwise valid strategy candidate.

AI/LLM components may not bypass the risk engine or directly submit broker orders.

## 22. Journal requirements

Journal every:

- context candidate
- parent selection
- key-level selection
- direction decision
- invalidation/rejection reason
- Turtle Soup event
- SMT state when enabled
- entry-model evidence
- risk denial
- no-signal expiry
- entry/exit
- T1/T2 state transitions
- strategy version
- evidence/rule IDs

This journal serves both audit and later learning datasets.

## 23. Freeze blockers

### P0

- Parent CRT selector
- Key-level selector
- Candle/session construction
- Turtle Soup primitive
- HTF direction algorithm

### Selected-entry P1

At least one entry family must be fully deterministic:

- Model #1, or
- true MSS

Then also:

- target hierarchy
- stop buffer/policy
- Candle-3 confirmation/expiry

## 24. Phase 1 freeze checklist

- [x] First broad corpus pass through CRT Secrets Episode 10
- [x] Rule evidence matrix created
- [x] Contradiction/refinement matrix created
- [x] Blocker priority created
- [x] First integrated strategy draft created
- [ ] P0 direct-source verification complete
- [ ] Parent CRT fixtures complete
- [ ] Key-level fixtures complete
- [ ] Candle calendar tests complete
- [ ] Turtle Soup fixtures complete
- [ ] Context-direction fixtures complete
- [ ] One entry family fully deterministic
- [ ] Positive and negative examples for every active rule
- [ ] Machine-readable fixtures exist
- [ ] No active-path `UNRESOLVED` state remains
- [ ] Independent strategy review complete
- [ ] Version freeze commit/tag created

## 25. Current promotion decision

`CRT-C3-ALIGNED-v0.1-DRAFT` remains:

```text
RESEARCH
```

It is **not** promoted to:

```text
FROZEN_FOR_VALIDATION
PAPER
SHADOW
LIVE_CANARY
LIVE_APPROVED
```

The next work is direct-source resolution of P0 blockers, not profitability optimization.
