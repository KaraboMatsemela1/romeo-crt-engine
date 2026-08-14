# Phase 6C — Session Consecutiveness Hypothesis 001

**Date:** 2026-08-14  
**Status:** `DEFERRED_RESEARCH_HYPOTHESIS`  
**Executable delta authorized:** **NO**  
**Detector activity / backtest / P&L / paper / shadow / live:** **NOT AUTHORIZED**

## Observation

The terminal Phase 6B multi-market activity result records `NON_CONSECUTIVE_PARENT = 416` for each of the four trusted instruments, for 1,664 pooled rejections.

The frozen v0.1 parent qualifier requires both:

```text
c1.close_time == c2.open_time
c2.close_time == c3.open_time
```

The canonical v2 datasets represent observed market sessions rather than synthetic weekend daily candles. A Friday-to-Monday transition can therefore contain adjacent canonical market-session bars whose civil timestamps are not contiguous.

## Research hypothesis

A future source-backed candidate may need to distinguish:

```text
consecutive civil-calendar D1 bars
```

from:

```text
consecutive canonical trading-session D1 bars
```

The hypothesis is that Romeo's intended Candle-1 / Candle-2 / Candle-3 sequence may refer to consecutive valid trading sessions rather than requiring a synthetic daily candle for every civil date.

## Why this is not implemented now

This observation was discovered after Phase 6B detector activity counts were opened. Implementing it immediately would alter historical signal eligibility after observing rejection counts.

Phase 6C requires any successor rule delta to be independently justified by direct first-party Romeo evidence and frozen before historical detector outcomes are opened. No currently captured first-party evidence has yet closed the exact calendar/session consecutiveness predicate.

Therefore:

```text
SESSION_CONSECUTIVENESS_PREDICATE_DEFINED = false
DIRECT_FIRST_PARTY_EVIDENCE_SUFFICIENT     = false
PHASE6C_CANDIDATE_READY                     = false
IMPLEMENTATION_AUTHORIZED                   = false
ACTIVITY_RECOUNT_AUTHORIZED                 = false
```

## Evidence needed to promote this hypothesis

Promotion requires direct first-party Romeo material that deterministically establishes at least:

1. whether Candle-1, Candle-2 and Candle-3 are consecutive trading sessions or consecutive civil-calendar days;
2. how weekends and full-market holidays are treated;
3. whether a missing/non-trading civil day breaks the parent sequence;
4. whether instrument-specific market closures alter parent ownership;
5. the information-availability time for identifying the next valid parent candle.

Positive and negative fixtures must be derivable without hindsight before any detector activity recount.

## Frozen inheritance if eventually promoted

Unless independently changed by separate source-backed evidence, any future candidate based solely on this hypothesis must preserve all other predecessor semantics unchanged, including:

- bearish parent sweep;
- opposite/double-sweep rejection;
- parent close reclaim;
- Target-1 pending requirement;
- C3 execution window;
- Model-1 core and confirmation;
- target-consumption guards;
- structural stop and one-tick buffer;
- primary target geometry;
- four-instrument trusted universe;
- MID signal component;
- sealed TradePlan outcomes and P&L until a newly preregistered activity gate passes.

## Anti-overfit guard

The observed count of 1,664 `NON_CONSECUTIVE_PARENT` rejections is diagnostic evidence only. It must not be used to estimate, promise, or select a future TradePlan count, and no candidate may be chosen merely because this predicate increases activity.

## Current decision

```text
HYPOTHESIS_RETAINED          = true
NEW_ALPHA_CANDIDATE_SELECTED = false
DETECTOR_MUTATION            = false
ACTIVITY_RECOUNT             = false
BACKTEST                     = false
PNL_OUTCOME_ACCESS           = false
PHASE7                       = BLOCKED
```
