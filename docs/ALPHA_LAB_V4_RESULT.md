# Alpha Lab V4 — Fresh-Holdout Result

## Final disposition

`HOLDOUT_A_FAIL_REJECT_V4`

V4 passed the fixed BTCUSDT DEV gate and remained profitable on the first fresh ETHUSDT holdout, but failed the preregistered risk gate because maximum drawdown reached 28.29% versus the 20% ceiling. BNBUSDT was therefore not accessed.

## Frozen V4 candidate

```text
candidate id            v4-a6627eb176a7e497b1ab
entry Donchian lookback 24 H1 bars
breakout buffer         10 bps
rising EMA-200 regime   off
ATR period              14
initial stop            1.5 ATR
trailing stop           4.0 ATR
maximum hold            168 H1 bars
risk                    1% realized equity
fee                     4 bps / side
slippage                2 bps / side
max notional leverage   3x
fixed profit target     none
```

## BTCUSDT DEV — PASS

Authoritative staged workflow run: `32638095351`.

```text
window              2019-01-01T00:00Z .. 2023-01-01T00:00Z
dataset SHA-256     16932863ee4ba3b60e4094abdf27834ff71414cd056c784a465d30f5f2dc7e0a
searched configs    144
BTC 2023+ accessed  false
```

| Metric | Result | DEV gate |
|---|---:|---:|
| Closed trades | 422 | >= 100 |
| Win rate | 31.99% | — |
| Profit factor | **1.403** | >= 1.30 |
| Expectancy | **+0.3736R** | > 0R |
| Return | **+306.61%** | — |
| Max drawdown | **18.21%** | <= 20% |
| Final equity | 406,612.72 | — |

The return is compounded simulator equity from 1% realized-equity risk sizing and is not an expected annual return forecast.

## Fresh ETHUSDT holdout A — FAIL

The exact frozen BTC DEV candidate was then evaluated once on preregistered ETH history with no search or parameter changes.

```text
window              2019-01-01T00:00Z .. 2025-01-01T00:00Z
dataset SHA-256     75b2ee802b2b6cef8f837fc2ab0cdda984543a669aac2e80a574c19b27f983e3
```

| Metric | Result | Holdout-A gate |
|---|---:|---:|
| Closed trades | 680 | >= 100 |
| Win rate | 31.32% | — |
| Profit factor | **1.196** | >= 1.15 |
| Expectancy | **+0.2021R** | > 0R |
| Return | **+235.62%** | — |
| Max drawdown | **28.29%** | **<= 20%** |
| Final equity | 335,617.88 | — |

ETH preserved positive profitability, but maximum drawdown exceeded the fixed limit by 8.29 percentage points. This is a risk-robustness failure, not a profitability failure.

## Fresh BNBUSDT holdout B

```text
access authorized = false
accessed           = false
```

The workflow skipped BNB automatically after ETH failed. BNB 2025–July 2026 remains unconsumed by Alpha Lab V4 and can remain an independent holdout for a future strategy protocol.

## Interpretation

V4 provides evidence that a simple long-only Donchian/Chandelier trend-following architecture can retain positive expectancy across BTC and a fresh ETH market under the stated bar-level cost model. However, the ETH drawdown failure means the strategy is not sufficiently risk-stable for promotion at 1% risk per trade.

The correct response is **not** to change V4's stop, trail, risk limit, or gate after seeing ETH. V4 is terminally rejected. A future version may define a materially new risk architecture before accessing another independent holdout, but ETH outcome feedback must not be presented as untouched validation for that new version.

```text
V4_DEV_GATE_PASS               = true
V4_ETH_HOLDOUT_GATE_PASS       = false
V4_BNB_HOLDOUT_ACCESSED        = false
V4_PARAMETER_RETUNING          = unauthorized
PAPER_TRADING_AUTHORIZED       = false
LIVE_TRADING_AUTHORIZED        = false
```
