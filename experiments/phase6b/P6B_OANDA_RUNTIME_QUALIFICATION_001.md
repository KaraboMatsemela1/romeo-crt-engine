# Phase 6B OANDA Runtime Qualification 001

**Date:** 2026-08-13  
**Environment:** OANDA practice  
**Research candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Strategy outcome access:** PROHIBITED  
**P&L access:** PROHIBITED

## Purpose

Execute the first credentialed Phase-6B OANDA qualification against runtime-only repository secrets without persisting account identity, bearer credentials, balances, NAV, strategy outcomes, or P&L.

## Safety controls

- `OANDA_ACCOUNT_ID` and `OANDA_API_TOKEN` were supplied only through GitHub Actions secrets.
- GitHub masked both secret values in job logs.
- The qualification code prints only authorization counts/booleans, never authorized account identifiers.
- No provider instrument manifest was produced because the provider rejected the configured account before instrument metadata could be returned.
- No detector activity counts were opened.
- No backtester was invoked.

## Runtime attempts

### Attempt 1

GitHub Actions run: `31695988553`

Observed:

- both required runtime secrets were present;
- OANDA practice account-summary request returned HTTP 403.

This established that repository-secret plumbing worked but did not distinguish token/account mismatch from account/API eligibility.

### Attempt 2 — authorization preflight

GitHub Actions run: `31696221051`

A credential-safe `GET /v3/accounts` preflight was added before account-specific API calls.

Observed:

```text
authorized_account_count=5
configured_account_authorized=true
```

The configured account-summary request still returned HTTP 403.

This proved the token is valid against the practice environment and that the configured account ID is one of the accounts authorized by that token.

### Attempt 3 — instrument-first qualification

GitHub Actions run: `31696424928`

The detector-only gate was relaxed only in one non-alpha respect: account-summary metadata became optional so the qualification could test the instrument-list endpoint first. This did not change strategy rules, market-universe rules, or outcome authorization.

Observed:

```text
authorized_account_count=5
configured_account_authorized=true
instrument discovery HTTP status=403
```

The configured account therefore cannot currently be used for the v20 account-instrument surface required by this Phase-6B route.

## Decision

```text
P6B_OANDA_RUNTIME_QUALIFICATION_001 = ACCOUNT_NOT_V20_ELIGIBLE_FOR_REQUIRED_ENDPOINTS
```

This is **not** a token-secret failure and **not** a strategy result.

The exact OANDA instrument universe remains unopened/unfrozen because `/v3/accounts/{accountID}/instruments` returned no usable response.

## Required remediation

Update the runtime `OANDA_ACCOUNT_ID` secret to an OANDA **practice REST-v20/API-eligible account** authorized by the existing token, or provision such a practice account if none of the token-authorized accounts is v20/API eligible.

Do not place the account ID in repository files, issues, PR comments, or chat transcripts.

After the secret is corrected, rerun the provider qualification and continue the existing precommitted sequence:

1. discover the account-specific instrument universe;
2. freeze exact symbols from the precommitted source families;
3. freeze accepted-instrument session/holiday and price-quantum contracts;
4. retrieve, seal and independently re-fetch MID M1 data;
5. build trusted provider-neutral H1/D1 datasets;
6. only then run the detector-only 2/2/30 activity gate.

## Authorization after this result

```text
V0_1_MUTATION_AUTHORIZED               = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
MULTI_MARKET_ACTIVITY_COUNTS_OPENED    = false
MULTI_MARKET_PNL_OUTCOME_ACCESS        = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
