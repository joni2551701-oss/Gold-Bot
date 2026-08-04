"""
Market Layer — Order Book read model (TASK-CORE-005).

Optional order-book view for the market façade. No provider in this
codebase supplies order-book depth yet (TwelveData is candle-only; the
crypto providers are inert stubs), so this stays a normalisation target
only: `from_levels()` turns a provider's raw bid/ask lists into a clean
internal model. It computes NO signal and makes NO trade decision --
just holds normalised depth. An absent order book is the empty model,
not an error.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class OrderBookLevel:
    """One price level: a price and the size resting at it."""
    price: float
    size: float


@dataclass(frozen=True)
class OrderBook:
    """
    Normalised order book: bids (descending price) and asks (ascending
    price). Both default empty -- the honest "no depth available" state.
    Holds data only; no imbalance/signal computation here.
    """
    symbol: str
    bids: List[OrderBookLevel] = field(default_factory=list)
    asks: List[OrderBookLevel] = field(default_factory=list)
    timestamp: Optional[datetime] = None
    provider: Optional[str] = None

    @property
    def best_bid(self) -> Optional[OrderBookLevel]:
        return self.bids[0] if self.bids else None

    @property
    def best_ask(self) -> Optional[OrderBookLevel]:
        return self.asks[0] if self.asks else None

    @property
    def is_empty(self) -> bool:
        return not self.bids and not self.asks

    @classmethod
    def from_levels(
        cls,
        symbol: str,
        bids: Sequence[Tuple[float, float]],
        asks: Sequence[Tuple[float, float]],
        timestamp: Optional[datetime] = None,
        provider: Optional[str] = None,
    ) -> "OrderBook":
        """
        Build an OrderBook from raw (price, size) tuple sequences (a
        common provider shape). Never raises -- malformed/empty inputs
        yield an empty side. No sorting/ranking logic beyond wrapping
        each level.
        """
        def _levels(rows: Sequence[Tuple[float, float]]) -> List[OrderBookLevel]:
            out: List[OrderBookLevel] = []
            for row in rows or []:
                try:
                    price, size = float(row[0]), float(row[1])
                except (TypeError, ValueError, IndexError):
                    continue
                out.append(OrderBookLevel(price=price, size=size))
            return out

        return cls(symbol=symbol, bids=_levels(bids), asks=_levels(asks),
                   timestamp=timestamp, provider=provider)
