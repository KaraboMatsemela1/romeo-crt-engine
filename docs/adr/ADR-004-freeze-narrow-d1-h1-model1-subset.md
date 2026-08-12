# ADR-004 — Freeze a Narrow D1→H1 Bearish Model-1 Subset

**Status:** Accepted  
**Date:** 2026-08-12  
**Decision owner:** project strategy governance  
**Applies to:** `CRT-C3-D1-H1-M1-BEAR-v0.1`

## Context

Phase 1 completed the Romeo CRT corpus/reconciliation baseline but left several discretionary or incompletely evidenced concepts unresolved: selective Candle-1 choice, a universal key-level hierarchy, a broad multi-timeframe bias resolver, exact Turtle Soup confirmation, the qualitative word `thick` in Model #1, stop buffers, and several optional branches such as SMT substitution, KOD and time exits.

The project bible allows Phase 2 to finish by excluding unresolved material or explicitly parameterizing it. The alternative—choosing definitions because a backtest looks profitable—would violate the project's evidence and validation rules.

## Decision

Freeze the first validation candidate as a deliberately narrow, bearish-only subset:

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
```

The active path is:

```text
canonical New-York D1 candles
  -> enumerate every consecutive C1/C2 pair
  -> C2 strictly sweeps C1 high only
  -> C2 closes back inside C1 range
  -> C1 midpoint remains unconsumed
  -> Candle 3 opens
  -> H1 Model-1-core candle sweeps C2 structural high
  -> later H1 close confirms below the model candle / swept high
  -> immutable TradePlan
  -> independent risk boundary
```

### Parent selection

Do not attempt to guess Romeo's discretionary Candle-1 ranking rule. Instead, enumerate **every** consecutive D1 pair as a parent candidate. Downstream predicates decide whether a pair qualifies. This is an exhaustive candidate-generation policy, not an alpha selector, and prevents hindsight selection.

### Calendar

Freeze the parent route to source-backed New-York Daily candles:

```text
D1 = [00:00 America/New_York, next 00:00 America/New_York)
```

Use the public Romeo mapping:

```text
Daily CRT -> H1 Model #1
```

H4 is excluded because its exact anchors remain unresolved.

### Direction

The broad external W1/D1/H4 market-bias resolver is excluded from v0.1. For this narrow candidate, `context_direction` means the already-closed D1 parent CRT direction inferred from the C2 manipulation/reclaim state before any H1 entry scan. v0.1 is bearish-only, so no bullish symmetry is inferred.

### Key level

For this one setup family, the reaction level is explicitly the selected C1 high (`CRTH`). No generic support/resistance or discretionary key-level ranking enters the active path.

### Turtle Soup

The broad Romeo Turtle Soup concept remains larger than this implementation. v0.1 freezes a conservative **close-reclaim subtype**:

```text
C2.high > C1.high
C2.low >= C1.low
C1.low <= C2.close < C1.high
```

A strict sweep without the reclaim does not qualify.

### Model #1

Choose Model #1, not true MSS, because public evidence specifies it more concretely.

The word `thick` remains qualitative in the source. v0.1 therefore introduces a transparent project parameter:

```text
P2-PARAM-M1-THICK-050:
body / full_range >= 0.50
```

This number is **not represented as a Romeo claim**. It is frozen before profitability testing and must be included in later sensitivity analysis.

A bearish Model-1-core candle must:

- be H1;
- be an up-close candle;
- cross the pre-existing C2 structural high from at/below it to above it;
- satisfy the frozen body-fraction parameter.

Confirmation is the first later completed H1 close below both the model candle low and the swept structural high, provided the target has not already been consumed. A new higher high before confirmation invalidates that model candle and allows later candles to be evaluated afresh.

### Stop and target

Freeze:

```text
stop reference = Model-1-core high
execution buffer = 1 instrument tick
primary target = C1 50% midpoint
```

The one-tick buffer is an explicit execution parameter, not a claimed Romeo alpha rule. Opposite C1 extreme remains an analytical secondary objective but is not part of v0.1 position exit logic.

### Candle-3 expiry

New entries are allowed only from C3 open until C3 close. If no Model #1 confirmation occurs in that window, outcome is `C3_NO_SIGNAL` / `NO_MODEL1_CONFIRMATION`. A confirmation after C3 close cannot authorize a v0.1 entry.

### Target consumption

To avoid ambiguous intrabar sequence reconstruction in the first candidate:

- if C2 reaches the C1 midpoint at all, reject the setup;
- if C3 reaches the midpoint before entry, reject the setup.

This is intentionally conservative.

## Explicit exclusions

v0.1 excludes:

- bullish symmetry;
- H4 and W1 parent routes;
- external multi-timeframe direction voting;
- journey-to-key-level setups;
- countertrend CRT;
- true MSS;
- KOD;
- SMT substitution or SMT-dependent entry;
- FVG requirements;
- OTE;
- time exits;
- Candle-2 entries;
- adaptive `near 50%` logic;
- ML ranking or override.

## Consequences

### Positive

- every active-path term becomes deterministic;
- no unresolved discretionary selector is hidden in code;
- no profitability result was used to choose the frozen parameters;
- the candidate can now progress to detector/data implementation and validation;
- later variants can isolate one change at a time.

### Negative

- this candidate is deliberately narrower than Romeo's full public doctrine;
- the 50% body threshold and one-tick buffer are project parameters that require sensitivity testing;
- bearish-only results cannot be generalized to bullish setups;
- excluding broader context filters may reduce performance; that is a validation question, not a reason to rewrite the rule after seeing results.

## Governance

This ADR authorizes **strategy freeze for validation only**. It does not authorize live trading, paper promotion, profitability claims, or parameter optimization against final out-of-sample data.
