# CRT v0.1 Strategy Specification — Frozen for Validation

**Strategy version:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Freeze parameter version:** `P2_FREEZE_2026_08_12`  
**Status:** **FROZEN_FOR_VALIDATION**  
**Live trading:** **NOT AUTHORIZED**  
**Paper trading:** **NOT AUTHORIZED**  
**Profitability claim:** **NOT ESTABLISHED**

This is the first deterministic strategy candidate produced by the Romeo CRT Engine project.

It is deliberately narrower than Romeo's full public methodology. Phase 1 established broad concepts but also documented several strategy-critical ambiguities. Phase 2 resolves those ambiguities by either:

1. excluding the unresolved branch from v0.1; or
2. explicitly freezing a project parameter before profitability testing.

No parameter in this specification was selected because it improved a backtest.

Canonical machine manifest:

- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`

Architectural decision:

- `docs/adr/ADR-004-freeze-narrow-d1-h1-model1-subset.md`

Executable rule contracts:

- `src/romeo_crt_engine/crt/v0_1.py`

Machine-readable fixtures:

- `tests/strategy/fixtures/crt_v0_1_cases.json`

---

## 1. Strategy purpose

The v0.1 objective is **faithful, deterministic reproduction of a narrow Romeo-derived CRT subset**, not maximum historical return.

The strategy asks one question:

> Given a completed New-York Daily Candle 1 and the immediately following Daily Candle 2, did Candle 2 produce a clean bearish sweep/reclaim while the 50% objective remains pending, and during Candle 3 did a qualifying H1 Model-1-core event confirm a short before the setup expired?

If any required condition is unknown, invalid or ambiguous, the result is `NO_SIGNAL`.

---

## 2. Evidence status and project-parameter policy

### Source-supported concepts used

The active path uses source-backed concepts established in Phase 1:

- every candle can be treated as a range;
- a parent/trade candle is selected before lower-timeframe execution;
- Turtle Soup involves an excursion beyond an existing high/low followed by failure/reversal;
- a bearish reaction may use an old `CRTH` reference;
- Daily CRT can map to H1 Model #1;
- Model #1 is based on a specific candle rather than a broad zone;
- bearish Model #1 uses an up-close candle around an old high and requires a later confirming close below the selected candle;
- Candle 2 must be complete before Candle 3 execution can be evaluated;
- the 50% point of the parent CRT is a material objective/state boundary;
- stops are structurally tied to the manipulation/model extreme;
- targets must be predeclared;
- risk approval is independent from strategy validity.

### Frozen project parameters

The source does not provide a numerical formula for every qualitative term. These values are therefore explicit project parameters, not represented as Romeo quotations or universal truths:

| Parameter | Frozen v0.1 value | Why |
|---|---:|---|
| Model #1 `thick` threshold | `body / full_range >= 0.50` | deterministic interpretation of a qualitative adjective |
| Stop execution buffer | `1 instrument tick` | separate structural reference from execution tolerance |
| Parent enumeration | every consecutive D1 pair | avoids hindsight/discretionary Candle-1 selection |
| Direction | bearish-only | first-party bearish old-CRTH clarification is stronger than the unresolved bullish mirror |
| C2 midpoint handling | any C2 touch of 50% rejects setup | conservative way to avoid unknown intrabar sequence |

These values must undergo sensitivity analysis later. They cannot be altered after observing final OOS performance without creating a new candidate version.

---

## 3. Frozen scope

### Included

```text
Doctrine                 CRT_SECRETS_2025
Direction                BEARISH ONLY
Parent timeframe         D1
Execution timeframe      H1
Source timezone          America/New_York
Parent setup             rolling C1 -> C2 -> C3
Key-level role           reaction from C1 CRTH
Parent manipulation      bearish sweep + close reclaim
Entry family             Model #1 core only
Primary target           C1 50% midpoint
Stop reference           Model-1-core high
Stop buffer              1 tick
Risk boundary            independent
Unknown critical state   NO_SIGNAL
```

### Explicitly excluded

- bullish mirror;
- H4 parent setups;
- W1 parent setups;
- monthly/quarterly parent setups;
- broad W1/D1/H4 voting or trend resolver;
- countertrend CRT;
- journey-to-key-level entries;
- true MSS;
- generic BOS/MSS;
- KOD;
- SMT substitution;
- SMT direct entry;
- OTE;
- FVG as a required entry filter;
- Candle-2 entries;
- adaptive `near 50%` rules;
- strong-trend retracement override;
- time exits;
- machine-learning entry overrides;
- 2026 CRTology refinements.

Excluded concepts are not declared false. They are simply outside this strategy version.

---

## 4. Calendar contract

### 4.1 Parent Daily candle

The canonical D1 candle is:

```text
[00:00 America/New_York, next 00:00 America/New_York)
```

The strategy uses the named IANA timezone, not a fixed UTC offset.

Therefore DST days may contain 23 or 25 absolute hours while still representing one New-York wall-clock Daily candle.

Provider-native D1 bars may not be substituted unless they match this boundary exactly.

### 4.2 H1 execution candle

H1 is the frozen execution timeframe for the D1 parent route.

An H1 candle must be a completed one-hour observation whose endpoints lie inside Candle 3's D1 window. An H1 close after Candle 3 closes cannot authorize a v0.1 entry.

### 4.3 Venue observations

The strategy calendar defines analytical boundaries. It does not fabricate prices while a market is closed.

Phase 3 must aggregate only actual observations and retain venue/provider quality metadata.

---

## 5. Parent candidate generation

### Rule `CRT-V01-002-ROLLING-PARENT-ENUMERATION`

The project does not guess which historical D1 candle Romeo would subjectively prefer as Candle 1.

Instead:

```text
for every consecutive pair of canonical completed D1 candles:
    first  = C1 candidate
    second = C2 candidate
```

This means overlapping parent candidates are allowed as separate strategy instances.

No candidate is chosen because a later trade worked.

Required causal facts:

- C1 is fully closed before C2 uses C1 high/low;
- C2 is fully closed before C3 becomes eligible;
- C1 high/low/midpoint are immutable for that candidate instance.

---

## 6. Parent range and key level

For Candle 1:

```python
CRTH = C1.high
CRTL = C1.low
T1 = (CRTH + CRTL) / 2
```

For this bearish-only setup:

```text
reaction key level = C1 CRTH
```

No nearest-support/resistance algorithm, FVG selector or discretionary ranking is used in v0.1.

---

## 7. Bearish Candle-2 qualification

A C1/C2 pair qualifies only if all rules pass.

### `CRT-V01-003-BEARISH-C2-SWEEP`

```python
C2.high > C1.high
```

The sweep must be strict.

### Single-sided requirement

```python
C2.low >= C1.low
```

If Candle 2 sweeps both C1 high and C1 low, the v0.1 state is ambiguous and fails closed.

### `CRT-V01-004-C2-CLOSE-RECLAIM`

Candle 2 must close back inside Candle 1:

```python
C1.low <= C2.close < C1.high
```

A wick/sweep alone is insufficient for this frozen subtype.

### `CRT-V01-005-T1-PENDING`

The 50% target must remain untouched during C2:

```python
C2.low > T1
```

This is a conservative parameterization. It prevents a candidate from pretending the original midpoint objective is still pristine after price has already traded there.

### Parent context result

If all conditions pass at C2 close:

```text
context_direction = BEARISH
key_level          = C1.high
parent_structural_high = C2.high
T1                 = C1 midpoint
```

The broad external market-bias resolver is not part of v0.1. The completed D1 CRT state itself is the higher-timeframe context for the H1 execution layer.

---

## 8. Candle-3 gate

### `CRT-V01-006-C3-GATE`

Candle 3 becomes eligible only when:

```text
C2 is closed
AND
C3 has opened
AND
parent context is qualified
AND
T1 is still pending
```

At C3 open, the strategy may know:

- final C1 OHLC;
- final C2 OHLC;
- C3 open timestamp and open price;
- frozen parent context.

It may not know:

- future C3 high;
- future C3 low;
- future C3 close;
- whether the setup will win.

`C3_OPEN` never means `ENTER`.

---

## 9. Model #1 core

### Why Model #1 was selected

Phase 2 selects Model #1 and excludes true MSS because Model #1 has the stronger deterministic public evidence baseline.

### `CRT-V01-007-MODEL1-CORE`

A bearish H1 Model-1-core candle must satisfy:

```python
candle.timeframe == H1
candle.close > candle.open                     # up-close
candle.low <= C2.high < candle.high            # crosses old structural high
body_fraction >= 0.50                          # frozen project parameter
```

where:

```python
body_fraction = abs(close - open) / (high - low)
```

Zero-range candles do not qualify.

`0.50` is parameter ID:

```text
P2-PARAM-M1-THICK-050
```

It is not claimed to be Romeo's unpublished numeric threshold.

---

## 10. Model #1 confirmation

### `CRT-V01-008-MODEL1-CONFIRMATION`

After a Model-1-core candle has closed, confirmation requires a later completed H1 candle inside the same C3 window to close below:

```python
min(model1.low, C2.high)
```

The confirmation must occur while price is still above the C1 midpoint target.

Entry reference for validation:

```text
entry = confirming H1 close
```

### Model invalidation before confirmation

If a later H1 candle makes:

```python
later.high > model1.high
```

before confirmation, that Model-1-core instance is invalidated.

The invalidating candle may itself become a new candidate Model-1-core candle if it independently meets all Model-1 rules.

This prevents a stale model candle from remaining active after a new structural extreme forms.

---

## 11. Target-consumption guard during C3

Before entry, if any completed H1 candle trades to or through:

```python
T1 = C1 midpoint
```

then:

```text
NO_SIGNAL
reason = TARGET1_CONSUMED_PRE_ENTRY
```

The strategy does not chase an entry after its primary objective has already printed.

---

## 12. Entry and immutable TradePlan

When confirmation occurs, create an immutable strategy `TradePlan` containing at minimum:

```text
strategy_version
freeze_parameter_version
direction
entry timestamp
entry reference price
stop structural reference
stop execution price
primary target
parent/key-level IDs or references
C1/C2/C3 timestamps
Model-1 timestamp
rule/evidence IDs
```

The strategy ends at `TradePlan`.

It does not determine final order size or bypass independent risk authorization.

---

## 13. Stop policy

### `CRT-V01-009-STRUCTURAL-STOP`

Structural stop reference:

```text
Model-1-core high
```

Execution stop:

```python
stop = model1.high + (1 * instrument_tick_size)
```

Parameter:

```text
P2-PARAM-STOP-1TICK
```

The structural reference and the execution buffer are deliberately separate.

A later version may change the buffer only through a versioned strategy/parameter review.

---

## 14. Target policy

### `CRT-V01-010-PRIMARY-TARGET`

Primary exit objective:

```python
target = C1 midpoint
```

The target is fixed before risk approval.

The opposite C1 low can be journaled as a secondary analytical delivery level, but v0.1 does not require holding or scaling a position to that level.

No partial-profit rule is implied.

No target may be changed after observing trade outcome.

---

## 15. Candle-3 expiry

### `CRT-V01-011-C3-EXPIRY`

New-entry eligibility exists only inside Candle 3.

If no confirmed Model #1 occurs before C3 closes:

```text
NO_SIGNAL
reason = NO_MODEL1_CONFIRMATION
```

A confirming close after Candle 3 closes is future information for that setup and cannot revive it.

There is **no strategy time exit after a position is opened** in v0.1. Open-position handling at the end of a finite research dataset must be reported separately as censored/mark-to-market data rather than silently inventing a time exit.

---

## 16. Fail-closed rules

### `CRT-V01-012-FAIL-CLOSED`

Return `NO_SIGNAL` when any required active-path input is:

- missing;
- stale;
- outside the frozen calendar;
- temporally inconsistent;
- ambiguous;
- based on future information;
- contradictory to the frozen rule set.

Representative reason codes:

```text
INVALID_CALENDAR
NON_CONSECUTIVE_PARENT
NO_BEARISH_PARENT_SWEEP
DOUBLE_OR_OPPOSITE_SWEEP
PARENT_CLOSE_NOT_RECLAIMED
TARGET1_CONSUMED_IN_C2
EXECUTION_DATA_OUTSIDE_C3
TARGET1_CONSUMED_PRE_ENTRY
NO_MODEL1_CONFIRMATION
INVALID_TRADE_GEOMETRY
```

`NO_SIGNAL` is a valid strategy result, not a trading loss.

---

## 17. Independent risk boundary

### `CRT-V01-013-INDEPENDENT-RISK`

Required architecture:

```text
CRT v0.1 strategy
      ↓
immutable TradePlan
      ↓
independent Risk Engine
      ↓
OrderIntent OR denial
```

A valid strategy setup may still be denied by risk.

No LLM, setup score or strategy confidence may override hard risk controls.

---

## 18. Anti-look-ahead invariants

The following are mandatory tests and implementation constraints:

1. C1 final range is unavailable before C1 closes.
2. C2 final close is unavailable before C2 closes.
3. C3 final OHLC is never an entry input.
4. Parent candidates are enumerated forward in time rather than selected after outcome.
5. A model candle is only available after it closes.
6. Confirmation is only available after the confirming H1 closes.
7. A confirmation after C3 expiry cannot authorize an earlier trade.
8. The primary target is frozen before order approval.
9. Final test/OOS results may not be used to revise this version in place.

---

## 19. Machine-readable fixture requirements

The frozen fixture suite must contain at least:

- one positive trade-plan case;
- no parent sweep;
- double/opposite sweep;
- sweep without reclaim;
- T1 consumed in C2;
- T1 consumed during C3 before entry;
- non-qualifying Model-1 body;
- future confirmation outside C3.

These are committed under:

```text
tests/strategy/fixtures/crt_v0_1_cases.json
```

The fixture suite is a **specification test**, not evidence of profitability.

---

## 20. Frozen rule register

| Rule | Frozen statement | Type |
|---|---|---|
| CRT-V01-001 | D1 uses NY-midnight wall-clock boundaries; H1 is execution timeframe | source + calendar contract |
| CRT-V01-002 | enumerate every consecutive D1 C1/C2 pair | anti-hindsight project policy |
| CRT-V01-003 | bearish C2 strictly sweeps C1 high only | source-derived subset |
| CRT-V01-004 | C2 must close back inside C1 range | conservative project formalization |
| CRT-V01-005 | C1 midpoint must remain unconsumed through C2 | source-derived target state + conservative guard |
| CRT-V01-006 | C2 close precedes C3 eligibility | source-derived causal rule |
| CRT-V01-007 | H1 up-close old-high sweep + body fraction >= 0.50 | source-derived Model #1 + explicit parameter |
| CRT-V01-008 | later H1 close below model/reference confirms | source-derived + deterministic formalization |
| CRT-V01-009 | stop above Model-1 high + 1 tick | structural source principle + execution parameter |
| CRT-V01-010 | full primary objective = C1 midpoint | source-derived narrow target policy |
| CRT-V01-011 | no new entry after C3 close | causal project expiry policy |
| CRT-V01-012 | unknown/invalid required state => NO_SIGNAL | engineering constraint |
| CRT-V01-013 | strategy emits TradePlan only; risk remains independent | architecture constraint |

No active rule remains `UNRESOLVED` inside this strategy version.

---

## 21. Required validation work after freeze

`FROZEN_FOR_VALIDATION` means the rules stop moving while evidence/edge is tested.

The next phases must perform:

1. trusted D1/H1 data construction;
2. known-fixture reproduction;
3. independent no-lookahead review;
4. event-driven historical detection;
5. transaction-cost modeling;
6. parameter sensitivity around the `0.50` body threshold and one-tick buffer;
7. in-sample exploration separated from final OOS;
8. walk-forward/OOS only after data and simulator are frozen;
9. negative-result preservation;
10. written reject/revise/promote decision.

If the candidate performs poorly, that is a valid Phase-6 outcome. The rules must not be silently rewritten to rescue the equity curve.

---

## 22. Promotion state

The strategy lifecycle is now:

```text
RESEARCH
   ↓
FROZEN_FOR_VALIDATION   ← current state
   ↓
PAPER                   not authorized
   ↓
SHADOW                  not authorized
   ↓
LIVE_CANARY             not authorized
   ↓
LIVE_APPROVED           not authorized
```

**Live trading remains false.**

Phase 2 is complete when the freeze manifest, deterministic contracts, fixtures, review record, docs and CI all agree with this specification.
