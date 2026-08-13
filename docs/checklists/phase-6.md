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

- [ ] Trusted DEV dataset built and versioned
- [ ] Data-quality gate passed
- [ ] Frozen detector run completed
- [ ] Frozen simulator scenarios completed
- [ ] DEV activity gate evaluated
- [ ] DEV report sealed before OOS access

## OOS — P6-OOS-001

- [ ] OOS remains unobserved until DEV report sealed
- [ ] Trusted OOS dataset built and versioned
- [ ] Data-quality gate passed
- [ ] Frozen detector/simulator runs completed
- [ ] OOS activity and robustness gates evaluated
- [ ] OOS report sealed before CONFIRM decision

## CONFIRM — P6-CONFIRM-001

- [ ] CONFIRM remains untouched until protocol permits access
- [ ] Decision recorded whether to consume or preserve CONFIRM
- [ ] If consumed, trusted dataset built/versioned once
- [ ] Frozen confirmatory run completed once
- [ ] Confirmatory report sealed

## Robustness analysis

- [ ] Cost scenario matrix reported
- [ ] Sensitivity diagnostics run only if DEV sample gate permits
- [ ] Rolling stability reported if sample size permits
- [ ] Monte Carlo run only if sample size permits
- [ ] Regime/session diagnostics run only if predefined and sample permits
- [ ] Independent leakage/overfit review completed
- [ ] Negative/zero-activity results preserved

## Final decision

- [ ] Final disposition written: `REJECT`, `REVISE_AS_NEW_VERSION`, `INSUFFICIENT_EVIDENCE`, or `PROMOTE_TO_PAPER_CANDIDATE`
- [ ] Project Bible / STATUS updated
- [ ] Paper trading remains disabled unless explicitly promoted
- [ ] Live trading remains disabled
