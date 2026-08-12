# Observability and Auditability

Track:

- market-data freshness and gaps
- strategy candidate counts/rejections
- reason-code distribution
- risk rejects
- order acknowledgements/rejections/fills
- broker/internal position mismatch
- latency
- slippage
- P&L and drawdown
- strategy/model version
- feature/data version
- service heartbeat

Alerts should prioritize data staleness, broker mismatch, risk-limit breach, unexpected order duplication, and infrastructure failures over ordinary losing trades.
