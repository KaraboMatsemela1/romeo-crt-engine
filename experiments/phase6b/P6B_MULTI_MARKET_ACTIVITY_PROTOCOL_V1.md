# Phase 6B Multi-Market Activity Protocol v1

**Protocol:** `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`  
**Frozen:** 2026-08-13  
**Research candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Underlying alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.2-MULTI-MARKET`  
**Signal component:** `MID`  
**P&L outcome access:** **PROHIBITED BY THIS PROTOCOL**

## Purpose

The v0.1 BTCUSDT Phase-6 candidate stopped at the preregistered DEV activity gate because it produced only four closed trades against a minimum of 30.

Phase 6B is testing a narrower question before investing in a multi-market execution simulator:

> Does the unchanged frozen bearish D1 -> H1 Model #1 alpha produce a statistically workable number of valid TradePlans when observed across a preregistered, Romeo-relevant market universe?

This protocol measures **signal activity only**.

It must not calculate, expose, rank, or optimize:

- P&L;
- win rate;
- expectancy;
- profit factor;
- drawdown;
- target/stop outcome labels;
- friction-adjusted returns;
- instrument profitability rankings.

## Why this gate is separated from performance

The provider-backed OANDA execution model still requires account-specific commission, conversion, quantity and bid/ask contracts.

If the frozen strategy remains too sparse even after an ex-ante multi-market expansion, those execution details cannot rescue the statistical sample problem.

The project therefore tests frequency first while outcome access remains sealed.

## Fixed DEV activity window

The activity window is frozen to the same historical DEV period used by v0.1:

```text
2019-01-01 00:00:00 America/New_York
through
2022-12-31 23:59:59.999... America/New_York
```

Operational data bounds must be represented in UTC by the provider-data manifests while preserving New-York wall-clock D1 construction.

### Why reuse this period

- it was selected before the multi-market provider outcomes exist;
- it permits direct comparison of opportunity frequency over the same broad regime period;
- it avoids choosing a different history window because another period creates more setups;
- it does not open the reserved v0.1 OOS or CONFIRM periods.

No Phase-6B market may be moved to a different DEV interval because preliminary signal counts are disappointing.

If an instrument lacks sufficient provider coverage for the fixed window, that is a **pre-outcome data-eligibility failure**, not permission to select a more favorable period.

## Precommitted source-family universe

The source-family whitelist remains:

```text
US NAS 100 / NQ proxy
US SPX 500 / ES proxy
EUR/USD
Gold/USD
```

Exact OANDA API symbols are intentionally not named as facts until the actual practice account instrument list is discovered.

### Exact-symbol freeze amendment

Before detector execution, a machine-readable universe amendment must record for each family:

```text
family
exact OANDA instrument symbol or UNAVAILABLE
account/division metadata digest
data coverage status
session-policy version
price-quantum decision
inclusion/exclusion reason
```

Allowed exclusion reasons are limited to pre-outcome provider/data facts such as:

- not available to the account/division;
- insufficient fixed-window history;
- unresolved session/holiday semantics;
- unresolved price quantum;
- failed trusted-data quality/re-fetch gate.

Prohibited exclusion reasons include:

- low TradePlan count;
- poor P&L;
- low win rate;
- unfavorable chart appearance;
- comparison with another instrument's strategy result.

The exact-symbol amendment must be committed **before any detector activity count is opened**.

## Minimum universe eligibility

A multi-market activity run requires at least **two accepted instruments** from the precommitted source-family whitelist.

If fewer than two instruments pass the provider/data eligibility gate:

```text
protocol result = INSUFFICIENT_ELIGIBLE_UNIVERSE
```

No detector outcome is opened under this protocol.

## Dataset requirements

Each accepted instrument requires its own frozen `P6B_CANONICAL_PRICE_DATASET_V2` identity with:

```text
quality_status           TRUSTED
price_component          MID
price_quantum            positive and pre-frozen
session_policy_version   frozen
normalized digest        sealed
provider retrieval       sealed/re-fetch verified
coverage                 fixed DEV window eligibility established
```

No instrument may borrow another instrument's session policy, price quantum, metadata identity or dataset digest.

## Detector requirements

The activity run must use the frozen compatibility baseline:

```text
candidate_version       CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version  CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version        CRT-DETECTOR-v0.2-MULTI-MARKET
```

Every emitted `TradePlan` must retain the v0.1 alpha strategy version.

No provider-specific field beyond the approved provider-neutral OHLC/time/price-quantum contract may enter alpha validity.

## Activity metrics allowed

For each accepted instrument the run may expose only:

```text
complete D1 bars
rolling C1/C2/C3 detector candidates
NO_SIGNAL count
TRADE_PLAN count
ReasonCode counts
```

Pooled output may expose:

```text
accepted instrument count
contributing instrument count
pooled detector candidates
pooled TRADE_PLAN count
per-instrument TRADE_PLAN counts
per-instrument share of pooled TRADE_PLAN count
```

Trade timestamps, entries, stops and targets should not be printed in the normal gate report because they invite manual outcome inspection. Detailed detector artifacts may be sealed for audit if required but are not part of the routine review surface.

## Primary activity threshold

The original Phase-6 minimum is retained rather than moved after observing the four-trade BTCUSDT result:

```text
MINIMUM_POOLED_TRADE_PLANS = 30
```

The pooled count is calculated across all accepted instruments in the exact-symbol freeze amendment.

## Multi-market contribution requirement

At least **two accepted instruments must contribute one or more TradePlans**.

This is not a profitability/diversification claim. It prevents a run from being called a multi-market activity success when every valid setup came from a single instrument.

No stronger concentration threshold is frozen in this protocol. Concentration must be reported descriptively and considered when designing the later performance-validation protocol.

## Gate outcomes

### `INSUFFICIENT_ELIGIBLE_UNIVERSE`

Use when fewer than two source-family instruments pass provider/data eligibility before detector access.

Consequence:

```text
no activity result opened
no simulator work authorized by this protocol
return to provider/data research or new candidate governance
```

### `INSUFFICIENT_MULTI_MARKET_SAMPLE`

Use when:

```text
pooled TradePlans < 30
```

or fewer than two accepted instruments contribute at least one TradePlan.

Consequence:

```text
Phase 6B activity hypothesis fails
P&L remains unopened
provider-backed simulator completion is not justified for this candidate
candidate preserved as insufficient sample evidence
```

### `SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL`

Use only when:

```text
accepted instruments >= 2
contributing instruments >= 2
pooled TradePlans >= 30
```

Consequence:

```text
activity gate passes
P&L is STILL NOT AUTHORIZED
```

A pass authorizes only the next engineering/governance work:

1. complete/freeze provider-backed bid/ask execution semantics;
2. complete/freeze commission/home-conversion/quantity handling;
3. create and verify a separately versioned simulator compatibility baseline;
4. preregister the full multi-market performance validation protocol;
5. only that later protocol may authorize historical P&L access.

## No instrument selection after count access

Once activity counts are opened:

- the exact instrument universe is sealed;
- instruments may not be dropped because they contribute few/no setups;
- instruments may not be added to lift pooled count above 30;
- thresholds may not be lowered;
- the DEV window may not be extended;
- alpha parameters may not change.

Any later universe change creates a new research candidate/protocol and preserves this result.

## OOS / CONFIRM protection

This protocol does not authorize access to:

```text
v0.1 OOS      2023-01-01 .. 2025-08-31
v0.1 CONFIRM  2025-10-01 .. 2026-07-31
```

It also does not define or open new multi-market OOS/CONFIRM windows.

Those are deferred to the full performance-validation protocol if the activity gate passes.

## Outcome firewall

The activity workflow must not invoke the backtester.

Required assertion:

```text
BACKTEST_EXECUTED             = false
PNL_OUTCOME_ACCESS_AUTHORIZED = false
```

A workflow that calculates trade P&L, stop/target outcomes, or profitability metrics violates this protocol even if those values are not printed.

## Frozen decision summary

```text
protocol                         P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1
candidate                        CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha                            CRT-C3-D1-H1-M1-BEAR-v0.1
detector                         CRT-DETECTOR-v0.2-MULTI-MARKET
signal price                     MID
DEV activity window              2019-01-01 .. 2022-12-31 NY
source-family universe           NAS100 / SPX500 / EURUSD / GOLDUSD families
minimum accepted instruments     2
minimum contributing instruments 2
minimum pooled TradePlans        30
P&L access                       PROHIBITED
backtest execution               PROHIBITED
v0.1 OOS/CONFIRM access          PROHIBITED
paper/shadow/live                NOT AUTHORIZED
```
