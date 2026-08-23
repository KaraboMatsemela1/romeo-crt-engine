# Alpha Lab V3 — DEV and OOS Result

## Disposition

`PROMOTE_V3_TO_CONFIRM_CANDIDATE`

V3 is the first Alpha Lab candidate to clear both the preregistered DEV gate and the untouched OOS gate after the research cost model. The candidate is frozen. No V3 parameters may be changed in response to OOS.

## Frozen candidate

```text
candidate id            v3-47f727727bbd433e5b22
symbol                  BTCUSDT
bar interval            H1
range lookback          24 H1 bars
breakout buffer         10 bps
EMA-200 regime          required: close > EMA-200
ATR period              14
ATR expansion           current ATR / median prior 48 ATR >= 1.0
close-location minimum  0.50
stop                    1.5 ATR
target                  3.0R
maximum hold            24 H1 bars
risk                    1% realized equity
fee                     4 bps / side
slippage                2 bps / side
max notional leverage   3x
```

## DEV — optimization window

Authoritative workflow run: `32637405603`.

```text
window                 2019-01-01T00:00Z .. 2023-01-01T00:00Z
DEV dataset SHA-256    16932863ee4ba3b60e4094abdf27834ff71414cd056c784a465d30f5f2dc7e0a
searched configs       576
```

| Metric | Result | DEV gate |
|---|---:|---:|
| Closed trades | 283 | >= 100 |
| Win rate | 46.29% | — |
| Profit factor | **1.596** | >= 1.30 |
| Expectancy | **+0.3523R** | > 0R |
| Return | **+161.49%** | — |
| Max drawdown | **8.67%** | <= 20% |
| Final equity | 261,485.69 | — |

**DEV gate: PASS.** The candidate was frozen before OOS access.

## OOS — untouched one-shot evaluation

The workflow restored the exact frozen DEV candidate and then opened the previously protected 2023–2024 window once.

```text
window                 2023-01-01T00:00Z .. 2025-01-01T00:00Z
OOS dataset SHA-256    41731710ca984804b2bfb2b7215274c59c74ceb58bcbb54f17566c50fb438d07
```

| Metric | Result | OOS gate |
|---|---:|---:|
| Closed trades | 171 | >= 50 |
| Win rate | 41.52% | — |
| Profit factor | **1.328** | >= 1.15 |
| Expectancy | **+0.2138R** | > 0R |
| Return | **+41.24%** | — |
| Max drawdown | **8.61%** | — |
| Final equity | 141,239.41 | — |

**OOS gate: PASS.**

## Interpretation

This is meaningful evidence of an edge, but it is not proof of guaranteed profitability and it is not live-trading authorization. DEV return is compounded through the simulator's 1% realized-equity risk sizing, so it should not be read as an expected annual return. OOS is the more important result because its parameter values were frozen before that period was exposed.

The OOS result is weaker than DEV, as should generally be expected, but it remains positive with PF 1.328 and +0.214R expectancy across 171 trades after the stated fee/slippage model.

## Protected data state

```text
DEV_GATE_PASS               = true
OOS_ACCESS_AUTHORIZED       = true
OOS_ACCESSED                = true
OOS_GATE_PASS               = true
CONFIRM_ACCESS_AUTHORIZED   = true
CONFIRM_ACCESSED            = false
PAPER_TRADING_AUTHORIZED    = false
LIVE_TRADING_AUTHORIZED     = false
```

Issue #133 deliberately stops here. The 2025+ CONFIRM period remains unopened. A separate preregistered confirmation task must define an exact confirmation window and final gate before any CONFIRM data is downloaded/read.
