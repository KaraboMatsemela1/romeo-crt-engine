# Phase 6B Trusted Dataset Freeze 001

**Machine-readable freeze:** `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.json`  
**Protocol:** `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`  
**Candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Frozen alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.2-MULTI-MARKET`  
**Signal component:** `MID`

## Decision

The preregistered OANDA source-family universe is accepted **4/4** for the detector-only Phase 6B activity gate.

This freeze was committed before any trusted multi-market detector activity count was opened. Instrument inclusion is based only on provider/data facts and does not use detector frequency, P&L, win rate, chart appearance, or any other strategy outcome.

## Authoritative trusted-data build

OANDA Trusted Dataset Build run #3 (`31799895592`) completed successfully at trusted-build head:

```text
91627194e374dd604a2cf0a58052a8d81ec44196
```

All four instruments independently reconstructed their full frozen provider history, matched the sealed provider values/gap coordinates, completed the New-York boundary, derived canonical H1 and New-York-midnight D1 bars, and emitted `P6B_CANONICAL_PRICE_DATASET_V2` identities with `quality_status = TRUSTED`.

The canonical DEV coverage is:

```text
2019-01-01T05:00:00Z
through
2023-01-01T05:00:00Z exclusive
```

The shared account/division instrument-discovery response digest is:

```text
393a037b5eaba52286a8e43c38183699e41cc6c5d96a9a44862cf9254f0fa63b
```

## Frozen accepted instruments

| Source family | Exact OANDA symbol | H1 | NY-D1 | Price quantum | Normalized H1/D1 SHA-256 |
|---|---:|---:|---:|---:|---|
| US NAS 100 / NQ proxy | `NAS100_USD` | 23,604 | 1,245 | `0.1` | `4c46987b424f6616116299132664ea298dab55697d240f089fe0867c5cf19181` |
| US SPX 500 / ES proxy | `SPX500_USD` | 23,605 | 1,245 | `0.1` | `dae1825b057fdc1acf87278a2163b570d9f2ae3fa870484c775eec78de37c19f` |
| EUR/USD | `EUR_USD` | 24,902 | 1,249 | `0.00001` | `b141c402fc4a69456fa56ab074b7bf37c75465b2e1e92a4c98c8516a08f96dd8` |
| Gold/USD | `XAU_USD` | 23,660 | 1,244 | `0.001` | `ec349ca0f77c3827666519bb234466ff1ff3e0ba2a30e46795c597a1df79fcdd` |

Each price quantum is frozen as `PROVIDER_PRICE_PRECISION_POLICY`; it is a provider price-representation precision decision and is not claimed to be an exchange tick-size contract.

## Reproducibility evidence

Before the authoritative run completed, an earlier non-authoritative provider reconstruction produced the same normalized H1/D1 digest for every instrument. The authoritative green-head build independently reproduced those exact values 4/4.

The detector-facing artifacts are bound by exact GitHub artifact IDs and ZIP SHA-256 digests in the machine-readable freeze. The H1/D1 file SHA-256 values are also frozen there.

Raw M1 provider price files were not persisted in the trusted artifacts.

## Authorization after this freeze

Only the preregistered detector **activity counts** may now be opened:

```text
complete D1 bars
rolling C1/C2/C3 candidate count
NO_SIGNAL count
TRADE_PLAN count
ReasonCode counts
```

Pooled output is restricted to the metrics permitted by `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`.

The following remain prohibited:

```text
BACKTESTER                         false
MULTI_MARKET_PNL_OUTCOME_ACCESS   false
PAPER_TRADING                      false
SHADOW_TRADING                     false
LIVE_TRADING                       false
```

No instrument may now be removed or added because of its forthcoming detector activity result.
