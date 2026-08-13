# P6 DEV Outcome Access Gate 001

Status: **DEV OUTCOME ACCESS AUTHORIZED**  
Protocol: `P6-VALIDATION-PROTOCOL-v1`  
Window: `P6-DEV-001` only

## Preconditions satisfied before outcome access

The first data-only freeze was created from workflow run `31681313574`, job `94387156400`, while detector/backtest steps were hard-disabled.

A second independent provider retrieval then reproduced the sealed identity exactly in workflow run `31681940715`, job `94389136788`, again while detector/backtest steps were hard-disabled:

```text
sealed_identity_reproduced   true
dataset_version              3e8a39fec1062ef902e8a1ad
manifest_sha256              761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
normalized_sha256            46682c2d793dbdd0a0939862f444d19b4817559c8989a7fde031598d52cb29f5
exclusion_ledger_sha256      fe6ef14eedd4340c0fa6157fb1b44e17684a1bbdfcef7e9c82b3276755fcb5aa
M1 / H1 / D1                 2074680 / 34578 / 1418
excluded UTC archives        20
REST / checksum evidence     48 / 1413
metadata version             6dde8c5617697745
metadata observed_at         2026-08-13T08:16:25.815237+00:00
```

Normal CI and the Phase-5 September regression smoke were also green on the sealed-reproduction head.

## Authorization boundary

The following transition is now permitted:

```text
P6_DEV_OUTCOME_ACCESS_AUTHORIZED = true
```

This authorization is limited to the preregistered DEV window and frozen chain:

```text
P6-DEV-001
  -> dataset 3e8a39fec1062ef902e8a1ad
  -> CRT-C3-D1-H1-M1-BEAR-v0.1
  -> CRT-DETECTOR-v0.1
  -> CRT-BACKTEST-v0.1.1
  -> IDEAL / BASE / STRESSED / SEVERE
```

`CRT-BACKTEST-v0.1.1` is the data-gap compatibility patch governed by `P6-DATA-QUALITY-AMENDMENT-001`; it changes the simulator event-clock continuity check from gapless to ordered/non-overlapping and does not alter entry, stop, target, sizing, transaction-cost, or same-bar semantics.

## Still prohibited

```text
P6_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
P6_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PAPER_TRADING_AUTHORIZED             = false
LIVE_TRADING_AUTHORIZED              = false
```

OOS cannot be opened until the DEV result is captured, its activity gate applied exactly as preregistered, and the DEV report is sealed. CONFIRM remains untouched.

No result observed after this gate may be used to loosen v0.1 in place.
