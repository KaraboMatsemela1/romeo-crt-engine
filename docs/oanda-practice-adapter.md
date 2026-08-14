# OANDA practice adapter

This boundary is deliberately practice-only and read-only. Configuration must use
the OANDA practice endpoint, a practice account identifier, and an externally supplied
token. The adapter validates instrument metadata and can expose a read-only health
contract, but its order method always raises and no HTTP request is made by CI.

Execution is disabled by default and explicit enablement is rejected. Live endpoints,
live environment mode, credentials in source, and strategy-driven paper orders are not
permitted by this issue. A future execution implementation must be introduced behind
the later #38/#39 authorization gates.
