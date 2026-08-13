# ADR-010 — OANDA provider price quantum for Phase 6B

- **Status:** ACCEPTED — FROZEN PRE-ACTIVITY
- **Date:** 2026-08-13
- **Candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`
- **Applies to:** OANDA v20 MID signal datasets only

## Context

The frozen v0.1 alpha uses a one-unit stop buffer through the legacy `tick_size` detector input. OANDA v20 exposes `pipLocation` and `displayPrecision`, but does not label `displayPrecision` as an exchange/market tick size.

OANDA's v20 `Instrument` contract defines `displayPrecision` as the decimal places used to display instrument prices. OANDA's v20 error contract separately documents `PRICE_PRECISION_EXCEEDED` / stop-price precision rejection when a submitted price contains more precision than the instrument allows.

Primary sources:

- https://developer.oanda.com/rest-live-v20/primitives-df/
- https://developer.oanda.com/rest-live-v20/troubleshooting-errors/

## Decision

For Phase 6B, define **provider price quantum** as the smallest decimal price unit allowed by OANDA's instrument precision policy:

```text
price_quantum = 10 ^ (-displayPrecision)
source        = PROVIDER_PRICE_PRECISION_POLICY
```

This value is **not** asserted to be an exchange tick size, economic minimum price movement, or pip. `pipLocation` remains separate metadata.

The legacy v0.1 evaluator's `tick_size` argument receives this frozen provider price quantum through `CRT-DETECTOR-v0.2-MULTI-MARKET`. This is a provider-compatibility definition made before detector activity counts and before any P&L outcome.

## Frozen accepted-instrument values

| OANDA symbol | displayPrecision | provider price quantum | pipLocation |
|---|---:|---:|---:|
| `EUR_USD` | 5 | `0.00001` | -4 |
| `XAU_USD` | 3 | `0.001` | -2 |
| `NAS100_USD` | 1 | `0.1` | 0 |
| `SPX500_USD` | 1 | `0.1` | 0 |

## Guardrails

- Do not rename this value to `exchange_tick_size` or claim it is a pip.
- Do not estimate a different value from historical strategy outcomes.
- Do not alter the value after detector counts are opened for this candidate.
- A provider contract change requires a new data identity and explicit amendment before further outcome access.
- Quantity precision remains governed separately by `tradeUnitsPrecision` / `provider_unit_precision_step`.

## Consequence

`PriceDatasetIdentityV2.price_quantum_source` must be `PROVIDER_PRICE_PRECISION_POLICY` for all four frozen OANDA Phase-6B signal datasets.
