# Phase 5 Simulator Provenance Contract

`CRT-BACKTEST-v0.1` run identity must bind the simulator implementation and execution quantity contract, not only the observed outcomes.

For every Phase-5 result preserve:

```text
strategy_version
detector_version
detector_run_sha256
dataset_version
dataset_manifest_sha256
simulator_version
simulator_code_sha256
quantity_step
backtest_config_sha256
backtest_run_sha256
```

`simulator_code_sha256` is derived from the Python source files in `src/romeo_crt_engine/backtest/`.

`quantity_step` is an explicit run input because changing permitted quantity granularity can change risk sizing and P&L even when the same detector TradePlan and market data are used.

The deterministic regression suite requires identical source/data/config/quantity inputs to reproduce the same run SHA and requires quantity-step drift to create a different run SHA.

This provenance contract is an integrity property only. It is not a profitability claim.
