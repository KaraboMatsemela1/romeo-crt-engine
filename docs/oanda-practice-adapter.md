# OANDA practice adapter

This boundary is deliberately practice-only and read-only. Configuration must use
the OANDA practice endpoint, a practice account identifier, and an externally supplied
token. The adapter validates instrument metadata and can expose a read-only health
contract, but its order method always raises and no HTTP request is made by CI.

Execution is disabled by default and explicit enablement is rejected. Live endpoints,
live environment mode, credentials in source, and strategy-driven paper orders are not
permitted by this issue. A future execution implementation must be introduced behind
the later #38/#39 authorization gates.

## Manual GitHub Actions connectivity smoke

`.github/workflows/oanda-practice-readonly-smoke.yml` is an opt-in
`workflow_dispatch` check. Before dispatching it, repository administrators must add
these GitHub Actions secrets for a **practice** account only:

- `OANDA_API_TOKEN`
- `OANDA_ACCOUNT_ID`

The workflow fixes `OANDA_ENV=practice`; it does not accept an endpoint override.
From the Actions tab, select **OANDA Practice Read-Only Smoke** and use **Run
workflow**. It makes only these GET requests after validating the exact HTTPS practice
origin and verifying the configured account is present in the token-authorized account
list in memory:

- `/v3/accounts`
- `/v3/accounts/{accountID}/summary`
- `/v3/accounts/{accountID}/instruments`

It never calls pricing, history, transaction, position, trade, or order endpoints.
The retained seven-day artifact is a small PASS/FAIL JSON report. It excludes the
token, authorization header, and full account identifiers; failed transport details
are intentionally not written to the artifact or logs. A FAIL result is fail-closed:
correct the practice-secret or configuration problem and manually dispatch a new run.
This connectivity check does not authorize strategy, paper, shadow, or live execution.
