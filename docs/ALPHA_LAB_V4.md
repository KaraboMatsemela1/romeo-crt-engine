# Alpha Lab V4 — Fresh-Holdout Trend Following

V4 resets the validation methodology after V3 failed its final BTC CONFIRM period. BTCUSDT 2019–July 2026 is now treated as a consumed research surface. V4 may optimize only on the already-consumed BTC 2019–2022 DEV window and must earn promotion on preregistered fresh market holdouts.

## Strategy family

V4 is a long-only H1 Donchian/time-series-momentum family:

1. signal close breaks the prior Donchian high, excluding the current bar;
2. optional regime requires close above EMA-200 and EMA-200 higher than 24 H1 bars earlier;
3. signal is known only at H1 close and entry occurs at the next H1 open;
4. initial stop is ATR-normalized;
5. there is no fixed profit target;
6. winners use a Chandelier-style trailing stop;
7. a trailing stop calculated from a completed H1 bar becomes active only on the next bar;
8. maximum hold is a fallback exit;
9. one position is allowed at a time.

Base research assumptions remain 4 bps fee per side, 2 bps slippage per side, 1% realized-equity risk, and 3x maximum notional leverage.

## Development

```text
BTCUSDT H1
2019-01-01T00:00Z .. 2023-01-01T00:00Z
```

Exactly 144 configurations:

```text
entry lookback        24 / 48 / 96
breakout buffer       0 / 10 bps
rising EMA-200 regime off / on
initial stop          1.5 / 2.5 ATR
trailing distance     2.0 / 3.0 / 4.0 ATR
maximum hold          72 / 168 H1 bars
```

DEV requires >=100 trades, PF >=1.30, positive expectancy after costs, and max drawdown <=20%.

## Fresh holdout A

If and only if DEV passes, the exact frozen candidate is evaluated once on:

```text
ETHUSDT H1
2019-01-01T00:00Z .. 2025-01-01T00:00Z
```

ETH is not an optimization surface. It requires >=100 trades, PF >=1.15, positive expectancy, and max drawdown <=20%.

## Fresh holdout B

If and only if ETH passes, the same exact candidate is evaluated once on:

```text
BNBUSDT H1
2025-01-01T00:00Z .. 2026-08-01T00:00Z
```

BNB is not an optimization surface. It requires >=50 trades, PF >=1.15, positive expectancy, and max drawdown <=20%.

A BNB pass yields `MULTI_MARKET_HISTORICAL_PASS`, not paper/live authorization. The next gate would be execution-cost stress and robustness.

## Governance

V4 execution does not read BTC 2023+ at any stage. V3 is not retuned using its failed CONFIRM result. ETH and BNB access are separate conditional jobs so a failed earlier gate prevents later holdout access.
