# Execution-disabled paper infrastructure harness

`romeo_crt_engine.paper_harness` is a deterministic integration harness for the
paper-infrastructure contracts. It is explicitly not a paper-trading authorization,
candidate selection mechanism, backtest, P&L calculation, or OANDA client.

## Component boundary

```text
synthetic/frozen TradePlan
  -> independent check_order + kill switch
  -> disabled authorization gate
  -> OrderIntent contract -> FakeBroker only
  -> OrderRecord/PositionRecord persistent lifecycle
  -> reconcile -> structured AuditEvent + compact JSON report
```

The harness imports the existing public `TradePlan`, `check_order`, `OrderIntent`,
order-state/reconciliation, and observability contracts. `PracticeAdapter.execute`
is never constructed or called; the report always records
`"execution_disabled": true` and `"oanda_order_endpoint_called": false`.

`PersistentLifecycle` uses a local deterministic JSON journal only for synthetic
fixture runs. It permits restart/reload and duplicate-intent detection; it is not a
production database or a broker ledger.

## Invocation

Run the synthetic positive and negative fixture suite:

```bash
python scripts/run_paper_infrastructure_harness.py
```

It prints one compact machine-readable JSON report. The focused tests cover the
accepted lifecycle plus risk/stale rejection, absent execution authorization,
duplicate intent, broker error, and reconciliation mismatch. A reconciliation
mismatch engages the in-memory harness kill switch for subsequent requests.

This infrastructure preserves the Phase 6/6B evidence and does not read market
history, select a candidate, calculate P&L, access OOS/CONFIRM, use credentials, or
connect to practice/live OANDA endpoints.
