# Phase 6 Annual Validation Data Windows

**Registered:** 2026-08-13  
**Results observed:** NO — calendar construction frozen before Phase-6 historical detector runs.

## Purpose

The detector evaluates rolling `C1 -> C2 -> C3` Daily triples.

If a target year were ingested using only that year's UTC archive days, the first local-year C3 candles would be missing prior C1/C2 context and the final local-year C3 could be incomplete because New-York midnight does not align with UTC midnight.

Phase 6 therefore freezes a mechanical raw-context policy before results.

## Annual membership rule

Validation membership is determined by:

```text
candidate.c3_open_time converted to America/New_York
```

A candidate belongs to target year `Y` only when:

```text
C3 New-York local year == Y
```

Adjacent raw archive days exist only to construct causal context. Their C3 candidates are not counted in the target-year report.

## Raw context padding

For target local year `Y`, ingest:

```text
UTC start archive day = (Y-1)-12-30
UTC end archive day   = (Y+1)-01-02
```

This provides:

- enough completed D1 history for Jan-1 C3 to have preceding C1/C2;
- enough UTC coverage for Dec-31 New-York D1/H1 completion;
- deterministic, symmetric calendar construction independent of results.

No padding day may be added or removed because a candidate or trade occurs near the boundary.

## Preregistered windows

| Experiment | Role | Target C3 local year | Raw UTC archive start | Raw UTC archive end | Expected target C3 count |
|---|---|---:|---|---|---:|
| `P6-FREQ-2019` | Development/frequency | 2019 | 2018-12-30 | 2020-01-02 | 365 |
| `P6-FREQ-2020` | Development/frequency | 2020 | 2019-12-30 | 2021-01-02 | 366 |
| `P6-FREQ-2021` | Development/frequency | 2021 | 2020-12-30 | 2022-01-02 | 365 |
| `P6-OOS-2022` | Historical OOS | 2022 | 2021-12-30 | 2023-01-02 | 365 |
| `P6-CONF-2023` | Historical confirmatory | 2023 | 2022-12-30 | 2024-01-02 | 365 |

`Expected target C3 count` is purely calendar-derived. A different count indicates data/calendar/detector coverage that must be investigated before interpreting strategy frequency.

## Expected raw/canonical shapes

For a non-leap target year:

```text
raw UTC archive days  369
M1 rows                531,360
H1 rows                8,856
complete NY D1         368
reported target C3     365
```

For leap-year target 2020:

```text
raw UTC archive days  370
M1 rows                532,800
H1 rows                8,880
complete NY D1         369
reported target C3     366
```

These expected row counts apply to the current 24/7 Binance Spot daily-M1 route. Any provider correction or route change must create a separately reviewed/versioned data contract.

## Annual isolation

Development years may be processed independently for operational reasons. Frequency aggregation is the sum of target-year reports only.

The context-padding mechanism ensures a Jan-1 or Dec-31 C3 is not lost merely because acquisition is annualized.

## P&L blindness

Stage 6A annual workflows invoke `scripts/run_validation_frequency.py` only.

They must not call `scripts/run_backtest.py` and must not emit:

- entry/stop/target prices;
- fills;
- P&L;
- equity;
- expectancy;
- profit factor;
- drawdown.

Only after the development-frequency gate passes and Stage 6B is separately preregistered may historical P&L be opened.
