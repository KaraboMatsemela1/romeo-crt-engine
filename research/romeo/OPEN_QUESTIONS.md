# Open Strategy Questions — Phase 2 Evidence-Debt Ledger

**Updated:** 2026-08-12  
**Phase 1 status:** COMPLETE  
**Strategy:** `CRT-C3-ALIGNED-v0.1-DRAFT` — NOT FROZEN / NON-EXECUTABLE

## Purpose

Phase 1 is closed. This file now tracks only questions that can materially change the first executable strategy or future separately-versioned expansions.

Questions are classified as:

- `P0-ACTIVE` — must be resolved before the first candidate can be frozen;
- `P1-ACTIVE` — required after the P0 context path is deterministic;
- `DEFERRED` — explicitly outside first v0.1;
- `VERSIONED` — belongs to a later doctrine/strategy version.

A missing answer never becomes a trading default. Required unknown state => `NO_SIGNAL`.

---

# P0-ACTIVE — blocks first deterministic candidate

## ED-P0-01 — Parent CRT / Candle-1 selector

Resolved contract:

- parent/trade candle is selected before LTF pattern detection;
- selected closed range is immutable for that parent instance;
- hindsight selection is prohibited;
- ambiguity fails closed.

Still required:

1. What exact observable predicate makes one completed candle the parent/Candle 1?
2. Are C1/C2/C3 necessarily consecutive chronological candles?
3. How are inside, nested and overlapping candidate ranges owned?
4. When does a parent expire or become superseded?
5. How are simultaneous W1/D1/H4 parent candidates resolved for the selected first route?

**Freeze criterion:** deterministic selector + lifecycle + positive/negative fixtures.

---

## ED-P0-02 — KeyLevelSelector

Resolved contract:

- key level is context, not entry;
- roles are `DESTINATION` and `REACTION_ORIGIN`;
- first v0.1 uses `REACTION_FROM_KEY_LEVEL` only;
- pre-level LTF reversals cannot be retrofitted into valid reactions.

Still required:

1. Which exact structures are eligible price/time key levels for first v0.1?
2. How are competing levels ranked without hindsight?
3. What exact event means `LEVEL_REACHED` — touch, wick, trade-through, close or another rule?
4. What marks a level `CONSUMED`, `INVALIDATED` or `SUPERSEDED`?
5. Is a time qualifier mandatory for the selected level family?

**Freeze criterion:** versioned registry + ranking + lifecycle + counterexample fixtures.

---

## ED-P0-03 — Candle calendar for selected route

Resolved/high-confidence:

- source calendar uses New York semantics for D1/W1 examples;
- D1 candidate boundary: `00:00 America/New_York`;
- W1 candidate reference open: Sunday `17:00 America/New_York`;
- DST must preserve named wall-clock semantics;
- asset-class H4 shorthand is strongly interpreted as:
  - Forex: `01/05/09/13/17/21`
  - index futures: `02/06/10/14/18/22`
  - crypto: `00/04/08/12/16/20`.

Still required for the first active route:

1. Are those H4 values candle opens or only high-probability CRT formation times?
2. What timezone applies to the shorthand?
3. What venue/session/maintenance policy applies?
4. How are holidays and missing observations handled?
5. Can provider-native bars be proven identical to canonical construction?

**Scope option:** if an H4 route cannot be resolved, exclude H4 rather than using provider defaults.

---

## ED-P0-04 — Turtle Soup confirmation / lifecycle

Resolved contract:

```text
PRE-EXISTING REFERENCE
    ↓
STRICT EXCURSION
    ↓
TURTLE_SOUP_CANDIDATE
    ↓
FAILURE / REVERSAL CONFIRMATION
    ↓
TURTLE_SOUP_CONFIRMED
```

A sweep alone cannot create an entry.

First-party narrowing supports an `OLD_CRTH` bearish reaction-reference subtype.

Still required:

1. Exact eligible reference taxonomy for first v0.1.
2. Meaning of `old` / reference freshness.
3. Exact failure/reversal confirmation event.
4. Same-candle vs later-candle confirmation rules.
5. Expiry/timeout after excursion.
6. True-breakout invalidation.
7. Reference consumption / reuse.
8. Bullish mirror only if directly evidenced or explicitly specified as a project symmetry assumption in a separate experiment.

**Freeze criterion:** causal bullish/bearish or intentionally one-sided predicate + lifecycle + fixtures.

---

## ED-P0-05 — Context-direction resolver

Resolved contract:

- direction precedes SMT/entry interpretation;
- `context_direction` and `candidate_direction` are separate;
- countertrend disabled in first v0.1;
- direction is stateful and can transition when qualifying opposite evidence appears;
- future active-candle close is prohibited;
- unresolved timeframe conflict => `UNKNOWN`.

Still required:

1. Exact bullish/bearish/neutral predicate.
2. Which timeframe owns direction for the selected first parent route?
3. What exact close/wick/reference relationship establishes or changes direction?
4. What makes an opposite CRT sufficiently `convincing` to flip bias?
5. What is the conflict-resolution rule when multiple HTFs disagree?

**Freeze criterion:** deterministic `BULLISH | BEARISH | NEUTRAL | UNKNOWN` resolver + transition fixtures.

---

# P1-ACTIVE — entry / management freeze debts

## ED-P1-01 — Choose first entry family

Phase 2 must choose **one** based on evidence completeness and determinism, not backtest returns:

```text
MODEL_1
OR
TRUE_MSS
```

### Model #1 questions

- exact bullish/bearish candle geometry;
- exact meaning of `thick`;
- relation to old high/low / Turtle Soup;
- close requirement;
- retrace/entry zone;
- FVG mandatory vs optional.

### True MSS questions

- exact structural swing construction;
- exact reference high/low;
- wick vs close break;
- exact entry region after shift;
- whether SMT/Turtle Soup/FVG are required for this setup family.

Generic BOS/MSS may not substitute for Romeo true MSS.

---

## ED-P1-02 — Target hierarchy

Need a deterministic immutable `TargetPlan` created before risk approval.

Questions:

1. When is 50% T1 versus context/reaction level?
2. What setup-specific conditions allow T2 at opposite CRT extreme?
3. When are prior-day high/low or other liquidity objectives selected instead?
4. What state change is required after T1 before continuation to T2?

No target may be chosen after observing which level was historically reached.

---

## ED-P1-03 — Structural stop + execution buffer

Source evidence supports a structural invalidation reference in the demonstrated framework.

Need:

- exact strategy stop reference by selected setup;
- bullish/bearish handling;
- separate tick/spread/slippage execution buffer;
- buffer policy frozen before validation rather than optimized against the final test.

---

## ED-P1-04 — Candle-3 confirmation and expiry

Known:

```text
C2_COMPLETE -> C3_OPEN -> C3_ELIGIBLE
```

Need:

- exact event producing `C3_ENTRY_CONFIRMED`;
- relation to selected key level and Turtle Soup;
- expiry if no confirmation occurs;
- `C3_NO_SIGNAL` versus `C3_FAILED` semantics;
- pre-entry and post-entry invalidation events.

---

# DEFERRED — not blockers for first v0.1

## SMT

First v0.1:

```text
allow_smt_substitution = False
SMTEvent -> OrderIntent = prohibited
```

Later version must resolve:

- pair/group registry and polarity;
- corresponding-extreme construction;
- synchronization window;
- stale-data rules;
- traded-instrument selection;
- exact substitution relationship with local Turtle Soup.

First-party public pair examples recorded during research include major FX/DXY, NQ/ES, BTC/ETH and Gold/Silver relationships; exact semantics remain versioned research work.

## Kiss of Death

Deferred until an ex-ante classifier exists.

Never use retrospective:

```text
last_turtle_soup_before_target
```

as a historical signal feature.

## Time exits

Disabled until deterministic source semantics exist.

## Journey-to-key-level trading

Excluded from first v0.1; reaction-from-level only initially.

## Countertrend CRT

Excluded from first v0.1; must become separate strategy variant if researched later.

## Candle-2 trading

Deferred until base Candle-3 strategy is frozen and validated.

## Adaptive / regime rules

Deferred:

- `near 50%` thresholds;
- strong-trend shallow retracement;
- optional confluence scoring;
- broad market-regime model.

No numerical threshold may be selected because it produces a prettier backtest.

---

# VERSIONED — doctrine evolution

## 2024 vs 2025 vs 2026

The engine must preserve doctrine versions instead of silently merging them:

```text
CRT_FOUNDATION_2024
CRT_SECRETS_2025
CRTOLOGY_2026
```

The first candidate uses:

```text
CRT_SECRETS_2025
```

Any 2026 rule that changes a 2025 interpretation requires an explicit doctrine-diff / strategy-version decision.

---

# Information-set safety — mandatory, not open

The following are already resolved engineering invariants:

- no final HTF OHLC before close;
- no future swing points;
- no retrospective parent/key-level selection;
- no retrospective KOD;
- no target selected after outcome;
- no Candle-3 final state at Candle-3 open;
- synchronized causal timestamps for cross-market data;
- stale/missing required data => `UNKNOWN`;
- provider candle-boundary mismatch is an error, not silent acceptance;
- every strategy decision must retain `information_available_at` and rule/evidence provenance.

---

# Phase 2 completion condition

This ledger is clear enough to start formalization but **not** to execute the strategy.

`CRT-C3-ALIGNED-v0.1` can move to `FROZEN_FOR_VALIDATION` only when every active-path P0 and selected-entry P1 debt is either:

1. resolved deterministically with evidence + fixtures; or
2. explicitly removed from the strategy path.

There may be no unresolved placeholder on the order path.
