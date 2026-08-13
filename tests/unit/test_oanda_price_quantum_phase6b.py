from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.oanda_price_quantum import (
    oanda_price_quantum_source,
    price_quantum_from_display_precision,
)
from romeo_crt_engine.market_data.price_data_v2 import PriceQuantumSource


def test_price_quantum_matches_frozen_oanda_instrument_precision() -> None:
    assert price_quantum_from_display_precision(5) == Decimal("0.00001")
    assert price_quantum_from_display_precision(3) == Decimal("0.001")
    assert price_quantum_from_display_precision(1) == Decimal("0.1")


def test_price_quantum_source_is_provider_precision_policy() -> None:
    assert oanda_price_quantum_source() is PriceQuantumSource.PROVIDER_PRICE_PRECISION_POLICY


@pytest.mark.parametrize("value", [-1, -5])
def test_negative_display_precision_fails_closed(value: int) -> None:
    with pytest.raises(ValueError, match="display_precision"):
        price_quantum_from_display_precision(value)
