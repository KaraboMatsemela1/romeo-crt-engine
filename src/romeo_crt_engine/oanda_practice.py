"""Practice-only OANDA boundary with execution disabled by default."""

from dataclasses import dataclass
from enum import StrEnum

PRACTICE_URL = "https://api-fxpractice.oanda.com"
LIVE_URL = "https://api-fxtrade.oanda.com"


class Environment(StrEnum):
    PRACTICE = "practice"
    LIVE = "live"


@dataclass(frozen=True)
class OandaConfig:
    environment: Environment
    base_url: str
    account_id: str
    token: str
    execution_enabled: bool = False

    def validate(self) -> None:
        if self.environment is not Environment.PRACTICE:
            raise ValueError("only the OANDA practice environment is permitted")
        if self.base_url.rstrip("/") != PRACTICE_URL:
            raise ValueError("base_url must be the OANDA practice endpoint")
        if self.execution_enabled:
            raise ValueError("strategy execution is disabled by this adapter")


@dataclass(frozen=True)
class InstrumentMetadata:
    instrument: str
    display_precision: int
    trade_units_precision: int
    minimum_trade_size: int


@dataclass(frozen=True)
class HealthResult:
    environment: Environment
    account_id: str
    read_only: bool


@dataclass(frozen=True)
class OrderIntent:
    client_order_id: str
    instrument: str
    units: int


class PracticeAdapter:
    def __init__(self, config: OandaConfig) -> None:
        config.validate()
        self._config = config

    def health_check(self) -> HealthResult:
        return HealthResult(
            environment=self._config.environment,
            account_id=self._config.account_id,
            read_only=True,
        )

    def execute(self, intent: OrderIntent) -> None:
        raise PermissionError(
            f"practice order execution is disabled for client order {intent.client_order_id}"
        )

    def normalize_instrument(
        self,
        instrument: str,
        display_precision: int,
        trade_units_precision: int,
        minimum_trade_size: int,
    ) -> InstrumentMetadata:
        if not instrument or display_precision < 0 or trade_units_precision < 0:
            raise ValueError("invalid instrument metadata")
        if minimum_trade_size <= 0:
            raise ValueError("minimum trade size must be positive")
        return InstrumentMetadata(
            instrument,
            display_precision,
            trade_units_precision,
            minimum_trade_size,
        )
