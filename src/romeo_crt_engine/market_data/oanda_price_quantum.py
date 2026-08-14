from __future__ import annotations

from decimal import Decimal

from romeo_crt_engine.market_data.price_data_v2 import PriceQuantumSource


def price_quantum_from_display_precision(display_precision: int) -> Decimal:
    """Return OANDA's provider price quantum from its allowed price precision policy.

    This is the smallest representable/allowed decimal price unit implied by
    `displayPrecision`. It is deliberately not named or treated as an exchange
    tick size or pip.
    """

    if isinstance(display_precision, bool) or display_precision < 0:
        raise ValueError("display_precision must be a non-negative integer")
    return Decimal(1).scaleb(-display_precision)


def oanda_price_quantum_source() -> PriceQuantumSource:
    return PriceQuantumSource.PROVIDER_PRICE_PRECISION_POLICY
