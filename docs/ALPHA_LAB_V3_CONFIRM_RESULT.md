# Alpha Lab V3 — CONFIRM Result

## Final V3 disposition

`CONFIRM_FAIL_REJECT_V3`

V3 passed both DEV and the untouched 2023–2024 OOS window, but failed the separately preregistered 2025-01-01 through 2026-07-31 CONFIRM period. Under the research contract, that failure is terminal for V3. Its parameters must not be changed in response to CONFIRM.

## Frozen candidate

`v3-47f727727bbd433e5b22`

The candidate configuration and cost assumptions are identical to the sealed DEV/OOS candidate. No parameter search occurred in CONFIRM.

## CONFIRM protocol

```text
workflow run          32637754408
window                2025-01-01T00:00Z .. 2026-08-01T00:00Z
CONFIRM dataset SHA   cc5dd26b182d3f3cc75c77d55fe6a918a62c76f6cf48d7f070d254657616cac3
candidate             v3-47f727727bbd433e5b22
optimizer/search      none
```

Preregistered gate:

```text
closed trades       >= 100
profit factor       >= 1.15
expectancy          > 0R after costs
max drawdown        <= 20%
```

## CONFIRM metrics

| Metric | Result | Gate |
|---|---:|---:|
| Closed trades | 127 | >= 100 |
| Win rate | 33.86% | — |
| Profit factor | **0.835** | >= 1.15 |
| Expectancy | **-0.0987R** | > 0R |
| Return | **-12.77%** | — |
| Max drawdown | 17.61% | <= 20% |
| Final equity | 87,226.76 | — |

Activity and drawdown remained within limits, but profitability failed materially. This is not a borderline result.

## Full V3 historical sequence

| Stage | Trades | PF | Expectancy | Return | Max DD | Outcome |
|---|---:|---:|---:|---:|---:|---|
| DEV 2019–2022 | 283 | 1.596 | +0.352R | +161.49% | 8.67% | PASS |
| OOS 2023–2024 | 171 | 1.328 | +0.214R | +41.24% | 8.61% | PASS |
| CONFIRM 2025–Jul 2026 | 127 | **0.835** | **-0.099R** | **-12.77%** | 17.61% | **FAIL** |

The deterioration in the latest independent window means the apparent edge is not sufficiently stable across time for promotion.

## What this means for further research

The project must not reinterpret the failed period as optimization data for V3, relax the CONFIRM gate, or test alternate V3 parameter combinations on the consumed CONFIRM window.

Because BTCUSDT 2019–July 2026 has now been exposed across DEV/OOS/CONFIRM, future candidate promotion must establish a **new independent validation boundary**. A sound next research phase should therefore use fresh holdouts such as previously untouched markets and/or future forward data rather than pretending the consumed BTC windows are still pristine OOS evidence.

```text
V3_PARAMETER_RETUNING_AUTHORIZED = false
V3_PAPER_TRADING_AUTHORIZED      = false
V3_LIVE_TRADING_AUTHORIZED       = false
```
