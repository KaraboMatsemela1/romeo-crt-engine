# P0-03 — Candle Calendar / H4-D1-W1 Construction

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Status:** **PARTIALLY RESOLVED / P0 REMAINS OPEN**  
**Date:** 2026-08-12

## Purpose

Resolve the exact candle boundaries required to reproduce Romeo's CRT candles without inheriting broker/provider-specific bar construction or introducing hidden timezone drift.

This blocker remains P0 because changing candle boundaries changes:

- parent range high/low
- midpoint/50%
- Candle 1/2/3 labels
- key-level interactions
- Turtle Soup events
- Model #1 candles
- direction and target state

## Evidence quality

This pass found a transcript of Romeo's 2024 `What is CRT?` lecture that contains two explicit clock/calendar statements:

1. the **Daily** opportunity resets at **midnight New York**;
2. the **Weekly** candle/open is referenced as **Sunday 5:00 p.m.**.

Episode 4 independently establishes opening time and closing time as part of candle anatomy and restricts the foundational trade-candle set to H4, Daily and Weekly.

A January 8, 2025 archived Romeo X post also gives Model #1 timeframe pairings:

```text
Monthly CRT -> Daily Model #1
Weekly CRT  -> 4H Model #1
Daily CRT   -> 1H Model #1
4H CRT      -> 15m Model #1
```

The pairing post is useful for execution-timeframe relationships, but **does not define the H4 candle's clock anchors**.

## Resolved / high-confidence calendar semantics

### CAL-P001 — canonical timezone is New York local time

**Status:** HIGH_CONFIDENCE / ENGINEERING INTERPRETATION

Romeo explicitly refers to `midnight New York` and a weekly `Sunday 5:00 p.m.` open. The project should therefore represent source calendar semantics using the IANA zone:

```text
America/New_York
```

Do not freeze a constant UTC offset such as `UTC-5` because New York observes daylight-saving transitions.

Engineering consequence:

```python
source_timezone = "America/New_York"
```

All source wall-clock anchors are interpreted in that timezone and converted to UTC only for storage/replay.

---

### CAL-P002 — Daily boundary = New York midnight

**Status:** HIGH_CONFIDENCE / DIRECT TRANSCRIPT EVIDENCE

Working interval:

```text
D1[t] = [00:00 America/New_York, next 00:00 America/New_York)
```

This is a **wall-clock daily candle**, not necessarily a fixed 86,400-second UTC interval on DST transition dates.

Required implementation property:

```python
DailyBoundary(
    timezone="America/New_York",
    local_open="00:00",
)
```

Do not use broker-native D1 bars unless they are verified to match this construction.

---

### CAL-P003 — Weekly reference open = Sunday 17:00 New York

**Status:** HIGH_CONFIDENCE / DIRECT TRANSCRIPT EVIDENCE

Working reference interval:

```text
W1[t] = [Sunday 17:00 America/New_York,
         next Sunday 17:00 America/New_York)
```

This interval is a **calendar/reference envelope**. It does not authorize synthetic weekend prices for markets that are closed.

For venue-limited markets:

```text
calendar interval exists
+
only actual tradable observations are aggregated
```

For 24/7 assets such as crypto, the same Sunday-17:00 anchor may be technically constructible, but whether Romeo intentionally applies the identical weekly boundary to crypto requires explicit cross-market verification before strategy freeze.

---

### CAL-P004 — DST follows New York wall clock

**Status:** ENGINEERING_CONSTRAINT

Because source anchors are stated in New York time, the engine must preserve the named local wall clock through DST.

Correct principle:

```text
00:00 NY stays 00:00 NY
17:00 NY stays 17:00 NY
```

Their UTC representation changes when New York changes offset.

Prohibited:

```python
NEW_YORK_OFFSET = -5  # fixed all year
```

Required tests include both spring-forward and fall-back transitions.

## Still unresolved — H4 anchor sequence

### CAL-B001 — exact H4 opens are not yet source-verified

**Status:** UNRESOLVED / P0

We do **not** yet have reliable primary evidence for Romeo's exact H4 boundary sequence.

Do not silently assume any of these:

```text
00 / 04 / 08 / 12 / 16 / 20 NY
01 / 05 / 09 / 13 / 17 / 21 NY
02 / 06 / 10 / 14 / 18 / 22 NY
provider-native H4 bars
exchange-session-derived H4 bars
```

Even though a midnight-anchored six-way subdivision would neatly nest inside the New-York D1 candle, that is an engineering inference—not a verified Romeo rule.

### Why this remains blocking

A four-hour shift can change:

```text
CRT high / low
Model #1 candle
Turtle Soup reference
Candle 2 close
Candle 3 open
key-level touch
50% level
```

Therefore H4 cannot be used in a frozen backtest until its clock anchors are resolved.

## Instrument-session policy remains unresolved

### CAL-B002 — market class / venue session semantics

**Status:** UNRESOLVED / P0

The project must distinguish at least:

```text
FX
index futures
metals futures / spot metals
crypto 24/7
```

Open questions:

- Does Romeo use one synthetic New-York candle calendar across all markets?
- Does he use TradingView/provider-native candles for some instruments?
- How are futures maintenance breaks treated inside H4/D1 candles?
- Does the Sunday 17:00 W1 reference apply unchanged to BTC/ETH despite 24/7 trading?
- Are holiday-shortened sessions aggregated normally or treated as special cases?

No answer should be inferred from conventional broker practice.

## Timeframe-pairing reconciliation

The 2024 foundation lecture says there is no universally fixed timeframe sequence because timeframes print at different speeds, while also showing example pairings. A later January 2025 Romeo post gives an explicit operational Model #1 mapping:

```text
Monthly -> Daily
Weekly  -> H4
Daily   -> H1
H4      -> M15
```

### Reconciliation decision

For doctrine version `CRT_SECRETS_2025`:

- treat the January-2025 mapping as the **candidate Model #1 execution pairing**;
- do **not** interpret that mapping as proof of H4 clock anchors;
- do **not** interpret `W1 → D1 → H4` top-down notation as requiring every trade to traverse every level;
- preserve the 2024 statement as a broader fractality principle rather than silently deleting it.

This is a **refinement**, not a license to infer missing calendar construction.

## Proposed non-executable calendar schema

Until H4 and venue policies are resolved:

```python
CandleCalendarDraft(
    source_timezone="America/New_York",
    daily_open_local="00:00",               # HIGH_CONFIDENCE
    weekly_open_local="Sunday 17:00",       # HIGH_CONFIDENCE
    h4_anchor_times=None,                    # BLOCKED
    dst_policy="IANA_WALL_CLOCK",           # ENGINEERING CONSTRAINT
    instrument_session_policy=None,          # BLOCKED
)
```

The presence of `None` is intentional. The builder must fail closed rather than select provider defaults.

## Bar-builder invariants

1. Store raw observations in UTC plus source/venue metadata.
2. Construct CRT bars from an explicit strategy-versioned calendar.
3. Never let the data provider silently decide candle boundaries.
4. Preserve New York wall-clock anchors through DST.
5. Never fabricate prices during market closures.
6. Mark a bar `DATA_INCOMPLETE` when expected tradable observations are missing.
7. A provider mismatch with canonical boundaries is an error, not a warning to ignore.
8. Strategy version must record the exact calendar version/hash used in a backtest.

## Required tests

### Daily

- normal EST date
- normal EDT date
- spring-forward weekend
- fall-back weekend
- midnight boundary converts correctly to UTC

### Weekly

- Sunday 17:00 NY boundary before/after DST
- venue closed over weekend without synthetic observations
- first tradable observation after weekly envelope opens
- holiday-shortened week

### H4 — after source verification

- all exact anchor timestamps
- six expected slots relative to the relevant D1 envelope if that nesting is verified
- H4 boundaries around DST transitions
- provider-native comparison

### Data-quality

- duplicate observation
- missing observation
- stale feed
- venue halt / maintenance window
- out-of-order event

## Acceptance status for P0-03

| Requirement | Status |
|---|---|
| canonical timezone | **PARTIALLY RESOLVED — America/New_York** |
| Daily open/close | **PARTIALLY RESOLVED — midnight NY to next midnight NY** |
| Weekly open | **PARTIALLY RESOLVED — Sunday 17:00 NY** |
| Weekly calendar envelope | **HIGH-CONFIDENCE CANDIDATE** |
| H4 anchor sequence | **OPEN / BLOCKING** |
| DST policy | **ENGINEERING RESOLVED — IANA NY wall clock** |
| instrument session policy | **OPEN / BLOCKING** |
| reproducible bar builder | **NOT IMPLEMENTED** |
| provider cross-check fixtures | **NOT IMPLEMENTED** |

### P0-03 disposition

```text
P0-03 = PARTIALLY_RESOLVED
strategy freeze = BLOCKED
```

We have enough evidence to stop treating Daily and Weekly anchors as fully unknown, but **not enough to authorize H4-dependent validation**.

## Next direct-source verification targets

Priority order:

1. Romeo live tape-reading material showing H4 candle timestamps on chart.
2. Episode 4 visual frames around H4 candle examples.
3. Episode 9 chart frames where the London-session example is nested in a higher-timeframe candle.
4. Romeo's original chart screenshots/X posts where the H4 open timestamp is visible.
5. Cross-market examples (FX, index futures, BTC) to determine whether the calendar is universal or instrument-specific.

## Promotion rule

P0-03 can close only when:

```text
H4 anchor sequence is directly evidenced
AND
instrument/venue session policy is explicitly decided
AND
DST-aware fixtures reproduce source charts
```

Until then:

```text
H4_PARENT_CRT -> NO VALIDATION
H4_DEPENDENT_SIGNAL -> FAIL CLOSED
```
