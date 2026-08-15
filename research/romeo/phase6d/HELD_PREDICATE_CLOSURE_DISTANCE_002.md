# Phase 6D — Held Predicate Closure Distance 002

**Date:** 2026-08-15  
**Tracking:** Issue #110  
**Baseline:** Recovery 007 plus Model #1 / True MSS closure-exhaustion passes  
**Mode:** first-party evidence synthesis only  
**Issue #16 disposition:** `KEEP_BLOCKED`

## Executive decision

After removing `MODEL_1_GEOMETRY` and `TRUE_MSS_ALGORITHM` from current-corpus active search because both are now `WAIT_FOR_NEW_*_EVIDENCE`, the closest remaining strategy-relevant held predicate is:

```text
1. SMT_EXECUTABLE_SEMANTICS
```

SMT is the only remaining row with provenance-bound first-party evidence already mapped across four of the seven required fields:

- `EXACT_PREDICATE`
- `DIRECTION_TIMEFRAME_OWNERSHIP`
- `CONFIRMATION`
- `DATA_REQUIREMENTS`

All evidence remains `PARTIAL`; no field is promoted to `CLOSING` by this report.

The best next bounded question is:

> **How does Romeo define the corresponding highs/lows and temporal synchronization used to decide that one paired market took an extreme while the other did not?**

This is the smallest high-leverage gap because the basic SMT divergence primitive and a pair registry already exist, but two engineers cannot reproduce identical SMT events without a deterministic corresponding-extreme/synchronization contract.

```text
NEXT_TARGET = SMT_CORRESPONDING_EXTREME_AND_SYNCHRONIZATION
ISSUE_16    = KEEP_BLOCKED
ISSUE_37    = MUST_NOT_START
```

## Method

Ranking uses the latest `PREDICATE_LEDGER_V2.json` and counts **required fields containing direct first-party evidence**, not profitability, visual appeal, historical trade frequency, or outcome behavior.

A field containing evidence is not automatically satisfied. All current ledger evidence is `PARTIAL` unless a later bounded report explicitly narrows a sub-question.

Required-field contract for every held row:

`EXACT_PREDICATE`, `INFORMATION_AVAILABILITY_TIME`, `DIRECTION_TIMEFRAME_OWNERSHIP`, `CONFIRMATION`, `INVALIDATION`, `EXPIRY`, `DATA_REQUIREMENTS`.

## Current-corpus exhausted entry predicates

### `MODEL_1_GEOMETRY`

```text
state = WAIT_FOR_NEW_MODEL1_EVIDENCE
```

Do not reopen through a broad current-corpus pass.

Direct support remains strong for one-candle specificity, close-trigger semantics and public timeframe mappings, but closure-critical old-extreme selection, `thick` semantics and expiry are semantic absences.

### `TRUE_MSS_ALGORITHM`

```text
state = WAIT_FOR_NEW_TRUE_MSS_EVIDENCE
```

Do not reopen through a broad current-corpus pass.

Direct support remains strong for the bullish relational sequence, but raw-candle swing construction, bearish form and expiry are semantic absences.

## Remaining predicate ranking

### Rank 1 — `SMT_EXECUTABLE_SEMANTICS`

Fields with current first-party evidence: **4 / 7**

| Required field | Current state | Evidence summary |
|---|---|---|
| `EXACT_PREDICATE` | `STRONG_PARTIAL` | Episode 6 directly defines the basic primitive: one asset takes a high/low while the paired asset does not; a named FVG-fill SMT variant also exists; Telegram 6520 shows SMT can play the manipulation role when an expected local Turtle Soup does not occur. |
| `INFORMATION_AVAILABILITY_TIME` | `MISSING/PARTIAL_CAUSAL_IMPLICATION` | synchronized comparison is implied, but no explicit machine-safe event timestamp/latching rule is ledger-bound. |
| `DIRECTION_TIMEFRAME_OWNERSHIP` | `PARTIAL` | direct EUR/DXY inverse example exists; universal pair polarity, traded-leg ownership and timeframe contract remain undefined. |
| `CONFIRMATION` | `STRONG_PARTIAL` | Episode 6 directly supports sequencing/hierarchy and non-standalone use; execution still requires an approved entry model. |
| `INVALIDATION` | `MISSING` | no universal event that cancels/rejects an SMT state is ledger-bound. |
| `EXPIRY` | `MISSING` | no deterministic SMT lifetime/expiry. |
| `DATA_REQUIREMENTS` | `STRONG_PARTIAL` | first-party pair inventory: EU–DXY, NQ–ES, BTC–ETH, GOLD–SILVER; exact synchronization/corresponding-extreme data contract remains undefined. |

Current key debt:

```text
corresponding extreme construction
+ synchronization
+ pair polarity / traded-leg ownership
+ lifecycle
```

Why rank 1:

- direct primitive exists;
- pair inventory exists;
- one concrete inverse pair example exists;
- confirmation hierarchy exists;
- a directly captured substitution example exists.

The next gap is therefore narrower than rebuilding the entire concept from scratch.

### Rank 2 — `TURTLE_SOUP_CONFIRMATION`

Fields with current first-party evidence: **2 / 7**

| Required field | Current state | Evidence summary |
|---|---|---|
| `EXACT_PREDICATE` | `STRONG_PARTIAL` | direct proper-entry example plus 2024 primitive; arbitrary-any-extreme selector is explicitly rejected. |
| `INFORMATION_AVAILABILITY_TIME` | `MISSING` | no complete confirmation timestamp contract. |
| `DIRECTION_TIMEFRAME_OWNERSHIP` | `PARTIAL` | one direct daily-timeframe example; not universal. |
| `CONFIRMATION` | `MISSING/PARTIAL_IN_SOURCE_CONTEXT` | no ledger-bound deterministic confirmation rule. |
| `INVALIDATION` | `MISSING` | unresolved. |
| `EXPIRY` | `MISSING` | unresolved. |
| `DATA_REQUIREMENTS` | `MISSING/PARTIAL_IMPLICATION` | old-extreme structure implied; deterministic selector/lifecycle absent. |

Main blocker remains the qualifying-extreme selector plus exact confirmation/lifecycle.

### Rank 3 — `DYNAMIC_BIAS_TRANSITION`

Fields with current first-party evidence: **2 / 7**

| Required field | Current state | Evidence summary |
|---|---|---|
| `EXACT_PREDICATE` | `PARTIAL` | direct text says to consider changing bias when a convincing opposite CRT appears. |
| `INFORMATION_AVAILABILITY_TIME` | `MISSING` | transition timestamp contract absent. |
| `DIRECTION_TIMEFRAME_OWNERSHIP` | `MISSING` | owning timeframe absent. |
| `CONFIRMATION` | `PARTIAL` | `convincing opposite CRT` and trend-change warning signs are direct concepts, but not machine-testable. |
| `INVALIDATION` | `MISSING` | absent. |
| `EXPIRY` | `MISSING` | absent. |
| `DATA_REQUIREMENTS` | `MISSING` | no deterministic data contract. |

Core semantic blocker: `convincing CRT` remains undefined.

### Rank 4 — `TIME_SELECTOR`

Fields with current first-party evidence: **2 / 7**

| Required field | Current state | Evidence summary |
|---|---|---|
| `EXACT_PREDICATE` | `PARTIAL` | Time + Turtle Soup co-dependence is direct; five clock times are direct; get-back-in-sync language is direct. |
| `INFORMATION_AVAILABILITY_TIME` | `MISSING` | paradoxically, listed clock values exist but their semantic eligibility state is undefined. |
| `DIRECTION_TIMEFRAME_OWNERSHIP` | `MISSING` | no universal owning market/timeframe. |
| `CONFIRMATION` | `MISSING` | no state transition from a listed time to trade eligibility. |
| `INVALIDATION` | `MISSING` | absent. |
| `EXPIRY` | `MISSING` | absent. |
| `DATA_REQUIREMENTS` | `PARTIAL` | time-of-day data clearly required; timezone/DST/calendar representation unresolved. |

The published times cannot be made executable without timezone, market/session scope and lifecycle semantics.

### Rank 5 — `KEY_LEVEL_SELECTOR`

Fields with current first-party evidence: **1 / 7**

| Required field | Current state | Evidence summary |
|---|---|---|
| `EXACT_PREDICATE` | `STRONG_PARTIAL` | journey-to-level vs reaction-from-level taxonomy and reaction-area/HTF context are direct. |
| all other required fields | `MISSING/PARTIAL_CONTEXT` | no deterministic selector/ranking, availability, ownership, confirmation, invalidation, expiry or full data contract. |

This row contains useful doctrine but remains far from an executable selector.

## `SS_MEANING_AND_CAUSAL_RULE`

SS is not ranked as an alpha candidate.

Recovery 007 directly clarified SS as a weekend review/preparation routine with recurring operational cadence. That is useful operating context, but the current evidence does not make SS an independent causal trade predicate.

Safe state:

```text
SS = DIRECT_NON_ALPHA_CONTEXT
```

Do not spend strategy-closure budget trying to force SS into an entry predicate unless new first-party evidence explicitly gives it causal trade eligibility semantics.

## Closure-distance summary

| Rank | Predicate | Required fields with first-party evidence | Current-corpus disposition |
|---:|---|---:|---|
| — | `MODEL_1_GEOMETRY` | multiple | `WAIT_FOR_NEW_MODEL1_EVIDENCE` |
| — | `TRUE_MSS_ALGORITHM` | multiple | `WAIT_FOR_NEW_TRUE_MSS_EVIDENCE` |
| 1 | `SMT_EXECUTABLE_SEMANTICS` | 4/7 | `CONTINUE_TARGETED_RECOVERY` |
| 2 | `TURTLE_SOUP_CONFIRMATION` | 2/7 | `PARTIAL / larger semantic debt` |
| 3 | `DYNAMIC_BIAS_TRANSITION` | 2/7 | `PARTIAL / convincing-CRT blocker` |
| 4 | `TIME_SELECTOR` | 2/7 | `PARTIAL / timezone-scope-lifecycle blocker` |
| 5 | `KEY_LEVEL_SELECTOR` | 1/7 | `PARTIAL / selector-ranking blocker` |
| context | `SS_MEANING_AND_CAUSAL_RULE` | 3/7 | `DIRECT_NON_ALPHA_CONTEXT` |

The counts are **coverage counts**, not closure scores. Rank also considers whether the existing evidence narrows a deterministic machine question.

## Exact next bounded recovery

Target:

`SMT_EXECUTABLE_SEMANTICS`

Question:

> **For a paired-market SMT comparison, how does Romeo identify the corresponding high/low in each market and what timing/synchronization rule determines whether one market took that extreme while the other did not?**

Priority first-party sources already in corpus:

1. Episode 6 around the basic divergence definition (03:23–03:44).
2. Episode 6 concrete EUR/DXY example (22:59–23:19).
3. Episode 6 surrounding confirmation section (28:13 onward) only if it explicitly clarifies temporal latching.
4. Existing official pair-registry Telegram post 6363.

Search hypotheses only, not assumptions:

- same candle/time window;
- same session extreme;
- corresponding structural swing;
- paired prior high/low;
- inverse-market mapped extreme.

No one of these may be promoted unless Romeo directly defines/demonstrates it sufficiently.

Expected classifications:

```text
DETERMINISTIC_CORRESPONDENCE_FOUND
FRAME_BINDABLE_EXAMPLE_ONLY
PARTIAL_CONTEXT_ONLY
NO_DETERMINISTIC_CORRESPONDENCE_FOUND
```

## Why no predicate closes now

Every remaining alpha-relevant row still contains at least one closure-critical semantic absence. No row passes the two-engineer test from raw market data.

Therefore:

```text
CLOSED_PREDICATES    = 0
CANDIDATE_READY_ROWS = 0
ISSUE_16             = KEEP_BLOCKED
ISSUE_37             = MUST_NOT_START
```

This ranking changes research priority only. It does not authorize candidate creation, detector/count work, performance evaluation, protected-window access, paper orders or live trading.
