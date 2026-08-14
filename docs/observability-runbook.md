# Paper observability and incident runbook

The observability boundary emits structured audit events for decisions, orders, broker responses, positions, risk rejections, kill-switch actions, and reconciliation. Events may carry candidate, detector, and data hashes so an operational review can reproduce a decision without changing strategy rules.

Synthetic alert evaluation covers:

- stale market data;
- reconciliation failure;
- repeated broker order errors; and
- risk-limit rejection thresholds.

Operational response:

1. Stale data: stop new order submission, preserve the event stream, and verify provider freshness.
2. Reconciliation failure: fail closed, stop new orders, compare persisted and broker state, and escalate before resuming.
3. Repeated order errors: stop retries, classify the broker error, and investigate connectivity or contract mismatches.
4. Risk-limit alert: keep the kill switch engaged and review the risk ledger.
5. Any restart: replay the immutable audit events and reconcile before enabling any future paper execution.

This issue adds telemetry and runbook artifacts only. It does not connect to a broker, place orders, enable paper trading, or authorize live trading.
