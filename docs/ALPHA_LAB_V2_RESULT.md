# Alpha Lab V2 — DEV Result

## Disposition

`REJECT_V2_NEAR_MISS_RETURN_TO_DEV_NEW_HYPOTHESIS`

V2 materially improved on V1, but it did not satisfy the preregistered DEV promotion gate. The protected OOS period remains unopened.

## Reproducible run

```text
GitHub Actions run    32636932571
symbol                BTCUSDT
bar interval          H1
DEV                    2019-01-01T00:00Z .. 2023-01-01T00:00Z
DEV dataset SHA-256   16932863ee4ba3b60e4094abdf27834ff71414cd056c784a465d30f5f2dc7e0a
configurations        1,296
candidate id          v2-e61f1d2940199f5fd333
```

## Best V2 DEV configuration

```text
range lookback         48 H1 bars
breakout buffer        5 bps
EMA regime             none
side                   long only
ATR period             14
stop                   2.0 ATR
target                 3.0R
maximum hold           48 H1 bars
risk                   1% realized equity
fee                    4 bps / side
slippage               2 bps / side
max notional leverage  3x
```

## DEV metrics

| Metric | Result | DEV gate |
|---|---:|---:|
| Closed trades | 346 | >= 100 |
| Win rate | 38.73% | — |
| Profit factor | **1.281** | **>= 1.30** |
| Expectancy | **+0.1962R** | > 0R |
| Return | **+89.05%** | — |
| Max drawdown | **7.94%** | <= 20% |
| Final equity | 189,054.64 | — |

V2 passed activity, expectancy, and drawdown requirements. It missed only the profit-factor gate by approximately 0.019.

## Protected data state

```text
DEV_GATE_PASS               = false
OOS_ACCESS_AUTHORIZED       = false
OOS_ACCESSED                = false
CONFIRM_ACCESS_AUTHORIZED   = false
CONFIRM_ACCESSED            = false
```

The workflow skipped the OOS job automatically. No 2023–2024 OOS result was consulted, and 2025+ CONFIRM remains untouched.

## Interpretation

The DEV evidence supports continued investigation of long-side H1 breakout continuation: unlike V1, the V2 family produced positive expectancy, strong cumulative return, and controlled drawdown after the research cost model. However, the fixed promotion threshold is part of the experiment contract. A 1.281 profit factor is not rounded up or treated as equivalent to 1.30.

The next candidate must therefore be a new preregistered DEV hypothesis that attempts to improve trade quality structurally—for example by conditioning V2-style long breakouts on volatility expansion and/or higher-timeframe trend/location—rather than reducing the gate or tuning from OOS.
