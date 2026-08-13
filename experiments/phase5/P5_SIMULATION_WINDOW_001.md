# P5-SIM-001 — First Historical Simulation Window Preregistration

**Registered:** 2026-08-13  
**Status:** PREREGISTERED — RESULTS NOT YET OBSERVED  
**Strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.1`  
**Simulator:** `CRT-BACKTEST-v0.1`

## Hypothesis

The purpose of this run is **simulator/data integration**, not to establish profitability.

The frozen strategy and detector should be able to consume a larger trusted BTCUSDT canonical history and produce deterministic candidate, TradePlan and simulated lifecycle outputs under explicit cost assumptions without lookahead or manual period selection after seeing results.

## Predeclared historical window

```text
Provider       Binance Public Data
Venue          Binance Spot
Symbol         BTCUSDT
Raw interval   1m
UTC start day  2025-09-01
UTC end day    2025-09-30
Selection      entire calendar month
```

This window is chosen **before observing detector or P&L results** because:

1. Phase 3 already established the trusted provider route on BTCUSDT;
2. the compact frozen integration fixture used 2025-09-17 and 2025-09-18;
3. expanding to the complete September 2025 calendar month is a mechanical, non-outcome-based extension around those already-selected dates;
4. it avoids choosing individual days, weeks or months because they appear profitable.

If this window produces zero TradePlans, losing trades, or otherwise unattractive results, the result must be preserved. A different period may later be studied only as a separately declared experiment, not as a replacement chosen to hide this result.

## Expected data shape before retrieval

For a 24/7 crypto venue, the raw request should contain:

```text
30 daily archives
43,200 M1 observations
720 canonical H1 observations
approximately 29 complete New-York D1 observations
approximately 27 rolling C1/C2/C3 candidates
```

Exact D1 count is determined by canonical New-York edge-day completeness and must come from the data pipeline rather than being forced to match this estimate.

## Frozen simulation semantics

The run must use:

```text
same-bar stop+target    STOP_FIRST_CONSERVATIVE
stop gap                worse bar open
favorable target gap    disabled
finite dataset end      leave open/censored; no invented time exit
entry activation        only after confirmation H1 close
max concurrent          1
execution assumption    SYNTHETIC_LINEAR_SHORT_RESEARCH_V1
```

BTCUSDT Spot is the observation source. The bearish short simulation is a synthetic linear research assumption and is **not** a claim that Binance Spot directly supports the modeled naked-short execution.

## Cost scenarios

Run all four predeclared project scenarios:

```text
IDEAL     fee 0 bps/side,  half-spread 0 bps/side, slippage 0 bps/side
BASE      fee 10 bps/side, half-spread 1 bp/side,  slippage 2 bps/side
STRESSED  fee 15 bps/side, half-spread 3 bps/side, slippage 5 bps/side
SEVERE    fee 20 bps/side, half-spread 5 bps/side, slippage 10 bps/side
```

These are **project research assumptions**, not factual claims about historical Binance fees/spreads.

## Research account assumptions

```text
initial_equity          100,000 quote-currency units
risk_fraction           0.5% of realized equity per accepted plan
max_concurrent          1
quantity_step           trusted instrument metadata snapshot
```

The 0.5% risk fraction is a research control, not an optimal sizing conclusion.

## Required outputs

For each cost scenario preserve:

- detector run SHA;
- backtest run SHA;
- candidate count;
- TradePlan count;
- rejected-plan count;
- completed-trade count;
- open-at-end count;
- gross and net P&L;
- total fees;
- win rate if defined;
- expectancy/average R if defined;
- profit factor if defined;
- max realized drawdown;
- every trade and exit reason;
- all censored/open positions.

## Interpretation boundary

This one-month sample may prove or disprove simulator integration assumptions. It **cannot** establish robust strategy profitability because it is not an OOS/walk-forward validation program and the execution route is still synthetic for a short-only strategy observed on Spot data.

Phase 6 remains responsible for formal robustness testing after Phase-5 simulation integrity is frozen.
