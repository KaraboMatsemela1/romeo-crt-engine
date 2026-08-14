# Leakage and implementation-spec audit

The audit consumes only candidate metadata and synthetic audit fixtures. It checks future D1/H1 information, unfinished Candle-3/final OHLC use, retrospective parent selection, date-window and cost immutability, detector/simulator/data hash binding, same-bar and gap policies, quarantined-window exclusion, and spec/code agreement.

It emits one machine-readable PASS or FAIL status with a finding and evidence reference for every check. A PASS report is necessary but not sufficient for paper promotion. The audit does not load market data, inspect P&L, or access hidden OOS/CONFIRM outcomes.
