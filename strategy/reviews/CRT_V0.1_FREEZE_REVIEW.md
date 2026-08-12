# CRT v0.1 Freeze Review

**Candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Review type:** adversarial ReviewAgent / governance review  
**Date:** 2026-08-12  
**Decision:** **PASS FOR `FROZEN_FOR_VALIDATION`**  
**Deployment decision:** **NOT AUTHORIZED**

## Review mandate

Challenge the Phase-2 candidate for:

- hidden discretionary terms;
- look-ahead/hindsight leakage;
- unsupported source claims;
- circular direction logic;
- target/stop ambiguity;
- parameter tuning disguised as interpretation;
- data/calendar ambiguity;
- unsafe promotion semantics.

This review is role-separated and adversarial but is not represented as an external human audit.

## Findings

### 1. Parent selection hindsight — PASS

The candidate no longer attempts to choose the historical Candle 1 that best explains a future move.

Frozen policy:

```text
enumerate every consecutive canonical D1 pair
```

This converts Candle-1 selection from a discretionary alpha choice into exhaustive candidate generation. A later event cannot change which pairs existed at timestamp `t`.

Residual risk: overlapping parent candidates may coexist. Phase 4 must give each candidate a stable parent ID and journal them separately; portfolio/risk policy later decides whether simultaneous approved TradePlans may coexist.

### 2. Calendar / DST — PASS FOR SELECTED ROUTE

The strategy excludes H4 and W1 parents and freezes only the source-supported D1 route:

```text
00:00 America/New_York -> next 00:00 America/New_York
```

Unit contracts include 23-hour and 25-hour DST Daily candles.

H4 anchors remain unresolved in the broader doctrine but are no longer active-path blockers because H4 is excluded from v0.1.

### 3. Execution timeframe — PASS WITH VERSIONED SCOPE

Daily -> H1 Model #1 is retained from the Romeo timeframe-pairing evidence baseline.

No lower execution timeframe is silently substituted.

### 4. Broad HTF direction resolver — PASS BY EXCLUSION

The earlier draft required a universal W1/D1/H4 context-direction algorithm that Phase 1 could not source deterministically.

v0.1 removes that unresolved branch. `context_direction` is defined narrowly as the already-closed bearish D1 parent CRT state before H1 entry detection.

This avoids majority voting, moving averages, hindsight trend classification or SMT circularity.

Tradeoff: v0.1 does **not** claim to reproduce Romeo's entire external market-bias filter. That omission must be considered when interpreting validation results.

### 5. Key-level ambiguity — PASS FOR SELECTED SETUP

The candidate does not implement a generic key-level ranking system.

Frozen reaction level:

```text
C1 CRTH
```

This is compatible with the first-party old-CRTH bearish clarification and removes nearest-support/resistance discretion.

### 6. Turtle Soup confirmation — PASS AS NARROW SUBTYPE

The broad Turtle Soup doctrine remains richer than v0.1.

The candidate freezes a conservative observable subtype:

```text
strict C1-high excursion
+ no opposite-side C1 sweep
+ C2 close back inside C1
```

The project does not claim that every Romeo Turtle Soup requires this exact close rule.

The H1 Model-1-core path also requires a renewed old-high excursion and confirming close, providing a second causal manipulation/confirmation layer inside C3.

### 7. Model #1 — PASS WITH EXPLICIT PARAMETER DEBT

Public evidence is strong enough to retain:

- specific candle;
- bearish up-close candle;
- old-high penetration;
- later close below the selected candle.

The qualitative word `thick` remains non-numeric in the source. The candidate therefore declares, rather than hides, the project parameter:

```text
P2-PARAM-M1-THICK-050 = body/full_range >= 0.50
```

This value was selected for semantic simplicity before profitability testing. Phase 6 must test sensitivity around it. A later change creates a new candidate/config version; it cannot rewrite v0.1 history.

### 8. True MSS — PASS BY EXCLUSION

True MSS is not sufficiently deterministic in the current corpus baseline and is fully excluded from v0.1.

No generic BOS/MSS substitute exists in the active path.

### 9. Target hierarchy — PASS

The first candidate has one primary target only:

```text
C1 midpoint / 50%
```

The setup is rejected if that objective is consumed before entry.

The opposite C1 extreme is analytical only and does not affect v0.1 exit logic.

This eliminates discretionary target switching after entry.

### 10. Stop ambiguity — PASS WITH EXPLICIT EXECUTION PARAMETER

Structural reference:

```text
Model-1-core high
```

Execution stop:

```text
reference + 1 instrument tick
```

The one-tick buffer is explicitly labeled project execution policy, not Romeo alpha evidence.

### 11. Candle-3 expiry — PASS

A new entry must confirm inside the same C3 D1 window.

A confirmation after C3 close returns `NO_SIGNAL` for that parent instance and cannot be backdated.

A regression test explicitly covers this future-confirmation case.

### 12. Final C3 OHLC leakage — PASS

The executable contract receives a `CandleWindow` for C3 rather than a completed C3 candle. Only open time, scheduled close time and open price exist at the gate.

This data model makes accidental use of future final C3 high/low/close harder by construction.

### 13. Target-state sequence ambiguity — PASS CONSERVATIVELY

Because D1 OHLC alone cannot determine whether a midpoint touch occurred before or after an intraday sweep, v0.1 rejects any C2 whose low reaches the midpoint.

This sacrifices setups rather than fabricating intrabar order.

Within C3, completed H1 chronology is used, and any midpoint touch before entry invalidates the candidate.

### 14. Risk boundary — PASS

The strategy contract produces an immutable `TradePlan` only.

No sizing, broker write, live credential or risk override is added.

`LIVE_TRADING_AUTHORIZED` remains false.

### 15. Parameter-overfit risk — PASS FOR FREEZE, OPEN FOR VALIDATION

No backtest was used to choose:

- 0.50 Model-1 body threshold;
- 1-tick buffer;
- bearish-only scope;
- midpoint-only target.

These choices are frozen **before** profitability evaluation.

They must be included in later sensitivity analysis rather than tuned on final OOS data.

## Known limitations carried into validation

1. v0.1 is bearish-only.
2. It is a narrow Romeo-derived subset, not the complete public doctrine.
3. It omits the broad external HTF bias filter.
4. It omits bullish old-CRTL symmetry until separately reconciled.
5. It omits SMT, KOD, true MSS, FVG filtering, OTE and time exits.
6. Overlapping Daily parent candidates are possible.
7. A position may remain open beyond C3 because no source-backed time exit is invented; finite-dataset handling must report censored open trades honestly.
8. The two explicit project parameters require sensitivity testing.

None of these limitations is hidden inside an `UNKNOWN` active-path predicate.

## Freeze-gate checklist

- [x] active parent generation deterministic
- [x] selected calendar route deterministic
- [x] selected execution timeframe deterministic
- [x] direction state deterministic for this bearish-only variant
- [x] key level deterministic for this setup family
- [x] Turtle-Soup/reclaim subtype deterministic
- [x] one entry family deterministic
- [x] target deterministic
- [x] structural stop and buffer deterministic
- [x] C3 expiry deterministic
- [x] positive fixture exists
- [x] negative fixtures cover active rejection rules
- [x] machine-readable fixture file exists
- [x] future-confirmation regression exists
- [x] no active-path `UNRESOLVED` term remains
- [x] excluded doctrines are named
- [x] project parameters are labeled as project parameters
- [x] independent risk boundary preserved
- [x] live trading remains unauthorized

## Decision

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
RESEARCH -> FROZEN_FOR_VALIDATION
```

The candidate may proceed to trusted-data and detector implementation.

It may **not** be called profitable, paper-ready, shadow-ready or live-ready without completing the later project gates.
