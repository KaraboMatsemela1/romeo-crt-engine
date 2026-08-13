# Phase 6 Checklist

Protocol: `experiments/phase6/P6_VALIDATION_PROTOCOL_V1.md`

## Protocol freeze

- [x] Frozen strategy/detector/simulator baseline declared
- [x] DEV window preregistered
- [x] OOS window preregistered
- [x] September 2025 engineering window quarantined
- [x] Final CONFIRM window reserved untouched
- [x] Fixed cost scenarios declared
- [x] Sample-size / insufficient-evidence gates declared
- [x] Promotion robustness gates declared
- [x] Diagnostic sensitivity grid declared
- [x] Monte Carlo seed/iterations declared
- [x] Sequential access rule declared
- [x] Paper/live authorization remains false

## DEV — P6-DEV-001

- [x] Trusted DEV dataset built and versioned
- [x] Data-quality gate passed
- [x] Frozen detector run completed
- [x] Frozen simulator scenarios completed
- [x] DEV activity gate evaluated
- [x] DEV report sealed before any OOS access

DEV result:

```text
rolling detector candidates  1,416
valid TradePlans                 4
BASE closed trades               4
required minimum                30
result          INSUFFICIENT_DEV_SAMPLE
```

## OOS — P6-OOS-001

- [x] OOS remained unobserved through DEV decision
- [x] OOS access decision recorded: **DO NOT OPEN — DEV SAMPLE GATE FAILED**
- [ ] Trusted OOS dataset built and versioned — **NOT PERMITTED / NOT REQUIRED**
- [ ] Frozen detector/simulator OOS runs — **NOT PERMITTED / NOT REQUIRED**
- [ ] OOS robustness gates — **NOT REACHED**

## CONFIRM — P6-CONFIRM-001

- [x] CONFIRM remained untouched
- [x] Decision recorded: **PRESERVE CONFIRM UNUSED**
- [ ] Trusted CONFIRM dataset — **NOT PERMITTED / NOT REQUIRED**
- [ ] Confirmatory run — **NOT PERMITTED / NOT REQUIRED**

## Robustness analysis

- [x] Cost scenario matrix reported descriptively
- [x] Sensitivity diagnostics correctly skipped because DEV sample gate failed
- [x] Rolling stability correctly skipped because sample size is insufficient
- [x] Monte Carlo correctly skipped because sample size is insufficient
- [x] Regime/session inference correctly skipped because sample size is insufficient
- [x] Independent leakage/overfit/gate review completed
- [x] Negative/low-activity results preserved

## Final decision

- [x] Final disposition written: `INSUFFICIENT_EVIDENCE`
- [x] OOS remains unopened
- [x] CONFIRM remains untouched
- [x] Paper trading remains disabled
- [x] Shadow trading remains disabled
- [x] Live trading remains disabled
- [x] Phase-6 completion report written
- [x] Project status/governance synchronization required before merge

## Exit

Phase 6 is complete for v0.1 when the governance synchronization and final CI/PR review pass.

The next legitimate project track is a **new evidence-backed strategy candidate/version**, not Phase 7 paper trading.
