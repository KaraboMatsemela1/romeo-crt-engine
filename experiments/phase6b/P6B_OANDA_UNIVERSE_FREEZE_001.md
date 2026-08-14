# Phase 6B OANDA Universe Freeze 001

**Candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Underlying alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.2-MULTI-MARKET`  
**Provider:** OANDA v20 practice  
**Source qualification:** `P6B_OANDA_RUNTIME_QUALIFICATION_002`

## Frozen universe

The qualification returned all four market families that were named before runtime discovery. The exact research universe is therefore frozen as:

| Family | OANDA symbol | Instrument type |
|---|---|---|
| EUR/USD | `EUR_USD` | CURRENCY |
| Gold/USD | `XAU_USD` | METAL |
| US NAS 100 / NQ proxy | `NAS100_USD` | CFD |
| US SPX 500 / ES proxy | `SPX500_USD` | CFD |

```text
accepted instruments = 4
minimum required      = 2
selection rule        = all precommitted aliases that matched
```

No additional instrument from the 123-account-instrument universe may be added to this candidate based on later detector counts or performance. None of the four frozen instruments may be removed based on later detector counts or performance. Any future universe change requires a separately versioned candidate and a new evidence-backed precommitment.

Source identities:

```text
GitHub Actions run                 31696424928
run attempt                       2
raw instrument response SHA-256   e9ea9a83b2b0f66605f79a94e9c5ca6f21549dd1f1cbbe739077165fe604ea64
available names SHA-256           2e77a962f559c51d37120ebe842ba62cd0c42e07f50fe845ced04df7ad0755d2
```

## What this freeze does not authorize

The universe freeze does not open detector activity counts or any performance outcome. Before detector activity access, each instrument still requires an explicit price quantum, evidenced session/holiday policy, sealed MID M1 DEV retrieval, deterministic H1/New-York-midnight D1 construction and a trusted provider-neutral dataset identity.

The backtester remains outside this gate.
