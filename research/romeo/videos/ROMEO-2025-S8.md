# Video Analysis — ROMEO-2025-S8

## Metadata
- Title: CRT secrets ep.8: When does CRT fail?
- URL: https://www.youtube.com/watch?v=-mWYppebugo
- Published: 2025-10-09
- Duration: 18:14
- Creator: Romeo / @Romeotpt
- Analyst/date: ChatGPT / 2026-08-12
- Evidence pass: 1

## Evidence quality

Romeo's official Telegram directly posted the exact YouTube ID `-mWYppebugo`, announced Episode 8, and labeled the technical section as approximately 04:30–18:13. The same official feed later posted follow-up material from Episode 8, including an `incomplete CRT` trap example and a direct statement that successful careers can be built around trading CRT highs/lows to the 50% objective.

Publication date and duration are independently indexed by Video Highlight as 2025-10-09 and 18:14.

The detailed semantic extraction below uses an indexed AI-generated YouTube summary because a first-party YouTube transcript was not directly accessible in the research environment. Therefore all rules remain `PROVISIONAL` until verified against the original video/audio or an authoritative transcript.

## Relevance
- CRT relevance: critical
- Primary concepts: failure taxonomy, SMT conflict, target-1 state, 50% objective, directional alignment, incomplete CRT, bias invalidation, no-trade filters
- Main engineering value: supplies the first explicit reject/downgrade logic for an otherwise valid-looking CRT/Candle-3 candidate

## Source-backed / summary-backed observations

| ID | Observation | Evidence type | Confidence |
|---|---|---|---|
| FAIL-O01 | Romeo's official Telegram identifies this exact video as Episode 8 and explicitly frames it around when CRT fails. | First-party Telegram | High |
| FAIL-O02 | The indexed summary says Romeo groups apparent CRT failures into three main cases: SMT interference before the expected target, 50% already reached, and choosing a CRT against prevailing direction/context. | Indexed Episode 8 summary | High |
| FAIL-O03 | SMT plus confirmation can invalidate the trader's expectation that the CRT will continue to its remaining extreme. | Indexed Episode 8 summary | High |
| FAIL-O04 | The 50% midpoint is presented as CRT Target 1. Once 50% is reached, the original setup state has changed and continuation to the opposite extreme is no longer assumed blindly. | Indexed Episode 8 summary + first-party Telegram follow-up | High |
| FAIL-O05 | Romeo's official Telegram later posts `There goes the 50%` and says trading CRT highs/lows to 50% can itself form a career approach. | First-party Telegram | High |
| FAIL-O06 | The summary says traders should avoid bearish CRTs in bullish higher-timeframe conditions and bullish CRTs in bearish higher-timeframe conditions if they want more consistency. | Indexed Episode 8 summary | High |
| FAIL-O07 | Counter-trend CRTs are not described as impossible, but are treated as lower-quality/more difficult compared with directionally aligned setups. | Indexed Episode 8 summary | Medium-High |
| FAIL-O08 | Romeo's official Telegram posts an Episode-8 `Market maker CRT trap: incomplete CRTs` example, confirming that incomplete/unfinished CRT interpretation is a distinct practical failure/trap category. | First-party Telegram | High |
| FAIL-O09 | The indexed SMT example references Model #1 confirmation rather than treating SMT alone as sufficient. | Indexed Episode 8 summary | High |
| FAIL-O10 | The video framing is about avoiding blind target-chasing after state changes, not declaring that the CRT framework itself becomes invalid whenever a target is missed. | Indexed Episode 8 summary + official promotion language | High |

## Primary conclusion: failure should be modeled as state invalidation, not post-hoc blame

For the engine, `CRT_FAIL` should not mean simply:

```text
trade lost
```

The useful deterministic abstraction is closer to:

```text
CRT_CANDIDATE
      ↓
CHECK CURRENT STATE
      ↓
FAILURE / DOWNGRADE FILTERS
   ├── SMT_CONFLICT_CONFIRMED
   ├── TARGET_1_ALREADY_REACHED
   ├── DIRECTIONAL_CONTEXT_CONFLICT
   └── INCOMPLETE / MISREAD CRT STATE
      ↓
ALLOW / DOWNGRADE / INVALIDATE
```

This turns Episode 8 into a **pre-trade and in-trade state-validation layer**.

## Failure class 1 — SMT conflict before remaining target

The safest current interpretation is:

```text
ACTIVE CRT EXPECTATION
      ↓
REMAINING TARGET PENDING
      ↓
CROSS-MARKET SMT APPEARS
      ↓
SMT GETS REQUIRED CONFIRMATION
      ↓
ORIGINAL DIRECTIONAL EXPECTATION INVALIDATED / DOWNGRADED
```

This reinforces Episode 6:

```text
SMT alone ≠ entry
SMT alone ≠ automatic invalidation
CONFIRMED SMT IN CONTEXT = state modifier
```

### FAIL-P001 — confirmed SMT can invalidate remaining-target expectation
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: invalidation / cross-market
- Human description: If a CRT has a pending target and a qualifying SMT plus confirmation forms against that expectation before the target is reached, the engine must not blindly maintain the original target bias.
- Evidence: FAIL-O02, FAIL-O03, FAIL-O09
- Engineering implication: active CRT objects need a `bias_status` / `target_expectation_status` field that can be updated by cross-market evidence.

### FAIL-P002 — SMT invalidation requires confirmation
- Status: PROVISIONAL
- Category: confirmation
- Human description: SMT should not automatically invalidate a CRT; the indexed example includes confirmation via Model #1.
- Evidence: FAIL-O03, FAIL-O09
- Cross-source support: ROMEO-2025-S6
- Blocker: exact mandatory confirmation path remains unresolved until Episode 9 reconciliation.

## Failure class 2 — 50% already reached

Episode 8 materially changes the way the engine should treat 50%.

Earlier research showed 50% as an important midpoint / Target 1. Episode 8 makes the state transition explicit:

```text
TARGET_1_PENDING
      ↓
PRICE REACHES 50%
      ↓
TARGET_1_COMPLETE
      ↓
ORIGINAL CRT IS NO LONGER `UNTOUCHED`
      ↓
REASSESS
   ├── CONTINUE TO TARGET_2
   └── REVERSAL / NEW CRT STATE
```

### FAIL-P003 — 50% is Target 1 state completion
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: target state
- Human description: Reaching the parent CRT midpoint completes Target 1 and must transition the CRT's state.
- Evidence: FAIL-O04, FAIL-O05
- Engineering implication: add explicit `target1_status = PENDING | REACHED`.

### FAIL-P004 — do not chase the opposite extreme after 50% without reassessment
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: no-trade / target governance
- Human description: Once 50% is reached, continuation toward the opposite CRT extreme is no longer an untouched original assumption; fresh price behavior must be evaluated.
- Evidence: FAIL-O04, FAIL-O10
- Engineering implication: a trade opened after Target 1 completion must be classified as a **new decision** using the current information set, not as the same pristine setup.

### FAIL-P005 — 50% reached is not equivalent to CRT failure
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: semantics
- Human description: If Target 1 at 50% was reached, the CRT delivered its first objective. Failure should not be labeled merely because Target 2 was not subsequently reached.
- Evidence: FAIL-O04, FAIL-O05
- Engineering implication: metrics must distinguish `T1_SUCCESS_T2_FAIL` from `SETUP_FAILURE`.

This is critical for honest backtesting.

A naive binary label:

```python
success = opposite_extreme_reached
```

would misclassify a setup that legitimately reached Target 1 and then reversed.

Use outcome states such as:

```text
NO_ENTRY
INVALIDATED_PRE_ENTRY
T1_REACHED
T1_REACHED_T2_REACHED
T1_REACHED_T2_NOT_REACHED
STOPPED_BEFORE_T1
```

## Failure class 3 — directional context conflict

The indexed summary explicitly warns against taking lower-timeframe CRTs opposite the prevailing higher-timeframe direction when seeking consistency.

### FAIL-P006 — directional alignment is a setup-quality filter
- Status: PROVISIONAL / HIGH CONFIDENCE
- Category: context
- Human description: Prefer bullish CRTs when higher-timeframe context is bullish and bearish CRTs when higher-timeframe context is bearish.
- Evidence: FAIL-O06
- Engineering implication: every CRT candidate must carry `candidate_direction` and `context_direction`.

### FAIL-P007 — counter-trend CRT is downgrade, not globally impossible
- Status: PROVISIONAL
- Category: setup quality
- Human description: Counter-trend CRTs may still work, but Romeo frames them as less consistent / more difficult; therefore the first production candidate should reject or quarantine them rather than claiming they never work.
- Evidence: FAIL-O07
- Engineering implication: initial CRT-v0.1 research candidate should likely set `allow_countertrend = False`; any counter-trend model should be a separate experiment/strategy variant.

This avoids silently mixing two different expectancy distributions.

## Incomplete CRT trap

Romeo's official Telegram explicitly posts an Episode-8 example titled `Market maker CRT trap: incomplete CRTs`.

The current public evidence does not fully define a deterministic `incomplete CRT` predicate, but it is important enough to model as a separate research blocker rather than folding it into generic failure.

### FAIL-P008 — incomplete CRTs must be distinguishable from completed/valid CRTs
- Status: PROVISIONAL / RESEARCH DIRECTIVE
- Category: setup completeness
- Human description: Some apparent CRT structures are incomplete and can trap traders; the engine needs an explicit completeness state before a signal may be approved.
- Evidence: FAIL-O08
- Blocker: exact incomplete-vs-complete definition requires direct visual/video verification and Episode 9 reconciliation.

Proposed state field:

```python
completion_state: UNKNOWN | INCOMPLETE | COMPLETE
```

Until defined:

```text
UNKNOWN → no production trade
```

## Revised Candle-3 qualification flow

Episode 7 gave us Candle-3 eligibility. Episode 8 now adds rejection logic:

```text
PARENT CRT
    ↓
KEY LEVEL
    ↓
CANDLE 2 CLOSED
    ↓
CANDLE 3 OPENED
    ↓
C3_ELIGIBLE
    ↓
DIRECTION ALIGNED?
    ├── NO → REJECT / SEPARATE COUNTERTREND EXPERIMENT
    ↓ YES
TARGET 1 ALREADY REACHED?
    ├── YES → ORIGINAL SETUP STATE CONSUMED; REASSESS
    ↓ NO
CONFIRMED SMT AGAINST EXPECTATION?
    ├── YES → INVALIDATE / DOWNGRADE
    ↓ NO
CRT COMPLETE / VALID?
    ├── UNKNOWN/NO → NO TRADE
    ↓ YES
LOCATION + MANIPULATION + CONFIRMATION
    ↓
ENTRY CANDIDATE
    ↓
RISK ENGINE
```

This is the strongest candidate decision tree produced by the corpus so far.

## State object update

The parent context should now carry at least:

```python
CRTState(
    parent_crt_id,
    direction,
    context_direction,
    direction_alignment,
    completion_state,
    target1_price,
    target1_status,
    target2_price,
    target2_status,
    bias_status,
    smt_conflict_status,
    invalidation_reason,
    information_available_at,
)
```

## Backtesting implications

### 1. Multi-stage outcomes

Do not reduce every setup to win/loss. Record target path explicitly.

### 2. Consumed setup state

A setup observed after 50% was already touched must not be tested as though Target 1 were still pending.

### 3. Direction filter must be frozen

`context_direction` cannot be defined retrospectively from the future trend. The higher-timeframe bias algorithm must be source-backed and causal.

### 4. SMT invalidation must be causal

A later SMT may not invalidate a trade before the SMT event actually existed.

### 5. Incomplete-CRT labels cannot use future completion

Do not classify a CRT as incomplete at time `t` merely because it later failed. The incompleteness predicate must use only evidence visible at `t`.

## Cross-source reconciliation

### Episode 5 — Key Level
- Fake MSS before the actual key level may trap premature traders.
- Episode 8 broadens the rejection framework: key-level context can still be overruled/downgraded by target state, directional context, or confirmed SMT.

### Episode 6 — SMT
- SMT is a cross-market state modifier, not standalone entry.
- Episode 8 strengthens this by showing confirmed SMT as an explicit reason not to force the original CRT target expectation.

### Episode 7 — Candle 3
- Candle 3 becomes eligible after Candle 2 closes.
- Episode 8 shows that eligibility is not enough: failure filters must pass before entry.

### Episode 9 — Connecting the dots
- Required next because Romeo's own promotion says Episode 9 explains how to use SMT correctly while trading and should reconcile execution, stop logic, target state, and the exact relationships among Model #1, true MSS, SMT and CRT failures.

## What this source does NOT yet establish

Do not guess:

- exact algorithm for higher-timeframe directional bias
- exact definition of `with trend`
- exact SMT direction/pair mapping
- exact confirmation needed for SMT invalidation
- exact incomplete-CRT predicate
- exact moment Target 1 is considered touched (tick, wick, close, tolerance)
- whether 50% is universally Target 1 across every CRT variant
- exact continuation criteria from T1 to T2
- exact stop/management change after T1
- whether counter-trend setups are always prohibited or only discouraged
- exact handling of nested CRTs where one timeframe is aligned and another is not

## Candidate failure taxonomy

```text
FAILURE / REJECTION REASONS

PRE-ENTRY
├── DIRECTION_CONFLICT
├── INCOMPLETE_CRT
├── CONFIRMED_SMT_CONFLICT
├── TARGET_STATE_ALREADY_CONSUMED
├── INVALID_KEY_LEVEL
├── INVALID_TIME
└── NO_CONFIRMATION

POST-ENTRY OUTCOMES
├── STOP_BEFORE_T1
├── T1_REACHED
├── T1_REACHED_T2_REACHED
├── T1_REACHED_T2_FAILED
└── INVALIDATED_AFTER_ENTRY
```

These must remain separate in analytics.

## Promotion decision

No FAIL-Pxxx rule is promoted to `VERIFIED` yet.

However, Episode 8 provides enough source-backed structure to require an explicit **Failure/Invalidation Engine** between context detection and trade authorization.

The next source, `ROMEO-2025-S9 — CRT secrets ep.9: Connecting the dots`, is now the highest-value reconciliation pass before we can draft the first complete `CRT-v0.1` candidate decision tree.
