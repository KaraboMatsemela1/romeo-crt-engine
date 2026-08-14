# Risk engine and kill switch foundation

This module is a broker-independent, fail-closed safety boundary. It rejects orders when the persistent kill switch is engaged, risk or session-loss limits are exceeded, positions are already at the configured maximum, data is stale, spreads are too wide, the session is ineligible, or sizing inputs are invalid.

The kill switch defaults to engaged. The module only evaluates synthetic order requests and calculates conservative rounded-down units. It does not connect to OANDA, place orders, authorize paper trading, or alter strategy signals.
