"""Contract specs and trading costs for B3 instruments.

FEES ARE APPROXIMATE. B3 changes its fee tables and they depend on volume
tiers. Calibrate them with a real brokerage note (nota de corretagem) from
your Clear account: divide the total fees by the number of contracts/value.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Instrument:
    kind: Literal["stock", "future"]
    tick_size: float
    # R$ gained per 1.0 move in price, per contract. Stocks are sized by capital instead.
    point_value: float = 1.0
    # Futures: R$ per contract per side (B3 emolumentos + registro). Clear charges no brokerage.
    fee_per_contract_daytrade: float = 0.0
    fee_per_contract_swing: float = 0.0
    # Stocks: share of traded value per side (negociação + liquidação).
    fee_rate_daytrade: float = 0.0
    fee_rate_swing: float = 0.0
    # Ticks lost per side between the price the strategy sees and the fill.
    slippage_ticks: float = 1.0

    def fee_per_unit(self, daytrade: bool) -> float:
        if self.kind == "future":
            return self.fee_per_contract_daytrade if daytrade else self.fee_per_contract_swing
        return self.fee_rate_daytrade if daytrade else self.fee_rate_swing


# Mini Ibovespa futures: 1 point = R$ 0.20, tick = 5 points.
WIN = Instrument(kind="future", tick_size=5, point_value=0.20,
                 fee_per_contract_daytrade=0.25, fee_per_contract_swing=0.45)
# Mini dollar futures: 1 point = R$ 10.00, tick = 0.5 point.
WDO = Instrument(kind="future", tick_size=0.5, point_value=10.0,
                 fee_per_contract_daytrade=1.20, fee_per_contract_swing=2.00)
STOCK = Instrument(kind="stock", tick_size=0.01,
                   fee_rate_daytrade=0.00023, fee_rate_swing=0.00030)


def for_symbol(symbol: str) -> Instrument:
    if symbol.startswith("WIN"):
        return WIN
    if symbol.startswith("WDO"):
        return WDO
    return STOCK
