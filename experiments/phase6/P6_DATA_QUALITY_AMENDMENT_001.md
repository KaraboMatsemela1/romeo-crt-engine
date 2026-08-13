# Phase 6 Data-Quality Amendment 001

Amendment ID: `P6-DATA-QUALITY-AMENDMENT-001`  
Protocol: `P6-VALIDATION-PROTOCOL-v1`  
Status: **PRE-OUTCOME INFRASTRUCTURE CORRECTION**  
DEV detector/backtest outcomes observed before amendment: **NO**

## Trigger

The first `P6-DEV-001` acquisition run failed before detector execution because the provider-authenticated archive:

```text
BTCUSDT-1m-2019-03-12.zip
```

contains 1,080 one-minute klines rather than 1,440.

The archive passed the Binance-published SHA-256 checksum. This therefore cannot be repaired by replacing it with invented prices or silently ignoring the mismatch.

## Independent historical evidence

The affected date coincides with a documented Binance system upgrade beginning at `2019-03-12 02:00 UTC`. The historical Binance notice stated that deposits, withdrawals and **trading would be suspended** during the upgrade. Contemporaneous completion reporting states the upgrade finished two hours earlier than the original eight-hour estimate and trading resumed at approximately `08:00 UTC`.

Evidence references:

- historical Binance Support article ID `360024825992` — *System Upgrade Notice*;
- Binance Trading public channel mirror of that notice;
- official Binance Spot API changelog entry dated `2019-03-12` documenting matching-engine / API system improvements;
- provider-authenticated `BTCUSDT-1m-2019-03-12.zip` containing exactly 1,080 M1 rows.

The resulting closure interval to be verified against the archive itself is:

```text
2019-03-12T02:00:00Z <= t < 2019-03-12T08:00:00Z
```

A closure-aware parser must verify that the **only** absent minute opens are exactly this interval. A row-count match alone is not sufficient.

## Policy change

For a versioned, evidence-listed venue closure only:

1. do not synthesize M1/H1 prices;
2. do not forward-fill or interpolate the halted interval;
3. permit the exact trusted gap in the M1 chronology;
4. build H1 only from actual complete 60-minute trading buckets;
5. exclude any New-York D1 whose wall-clock interval intersects the approved closure because it is not a complete strategy parent candle under the frozen D1 contract;
6. allow the backtester event clock to advance from the last trusted pre-closure H1 to the first trusted post-closure H1;
7. if a position is already open across such a gap, process the first post-gap H1 using the existing conservative gap-stop/target logic;
8. never treat an arbitrary missing-data gap as a venue closure.

## Simulator patch

Allowing a trusted event-time gap changes an input-validation assumption in the Phase-5 simulator but does not change entry, stop, target, cost, sizing, same-bar or gap-fill rules.

The Phase-6 baseline simulator will therefore receive a patch version:

```text
CRT-BACKTEST-v0.1.1
```

`CRT-BACKTEST-v0.1` remains the historical Phase-5 freeze. The patch must pass the full prior regression suite plus a trusted-gap regression before any DEV outcome is accepted.

## Expected DEV shape after closure-aware normalization

The preregistered calendar window remains unchanged:

```text
2019-01-01 .. 2022-12-31
```

No raw archive is moved to a different date and the maintenance interval is not backfilled.

Expected actual observations after accepting exactly the six-hour venue closure:

```text
raw archives                 1,461
M1 observations          2,103,480
H1 observations             35,058
complete NY D1                1,458
rolling D1 triples            1,456
```

Two New-York D1 candles intersect the UTC closure because `2019-03-12 02:00..08:00 UTC` spans local New-York midnight during EDT. Those two D1 parents are excluded before detector evaluation.

## What this amendment does NOT change

It does not change:

- strategy `CRT-C3-D1-H1-M1-BEAR-v0.1`;
- detector `CRT-DETECTOR-v0.1`;
- DEV/OOS/CONFIRM dates;
- sample-size gates;
- cost scenarios;
- promotion gates;
- sensitivity grids;
- Monte Carlo governance;
- September 2025 quarantine;
- paper/live authorization.

If the archive does not match the exact evidenced closure interval, DEV remains failed and no strategy outcome may be interpreted.

```text
PAPER_TRADING_AUTHORIZED = false
LIVE_TRADING_AUTHORIZED = false
```
