"""
Market Layer — Current Price read point (TASK-CORE-005).

The market layer's fast "what is the latest price?" accessor. It does
NOT keep history and does NOT compute a signal (Director constraint).

Reuse (CLAUDE.md Module Reuse / Director "duplicate logic qat'iyan
taqiqlanadi"): the live price store already exists as
stream.current_price.CurrentPrice. This module does NOT reimplement it
-- it provides a thin market-facing value object (MarketPrice) and a
helper that READS from an existing stream CurrentPrice, so a market
consumer has one façade to read from without importing stream/. No
secret is read or logged here.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class MarketPrice:
    """The market layer's latest-price value. Mirrors stream.PricePoint but is the market façade's own read type."""
    symbol: str
    price: float
    timestamp: Optional[datetime] = None
    provider: Optional[str] = None

    @classmethod
    def from_price_point(cls, point) -> Optional["MarketPrice"]:
        """Adapt a stream.PricePoint (public attributes only) into a MarketPrice. None-safe: returns None for a None point."""
        if point is None:
            return None
        return cls(symbol=point.symbol, price=point.price,
                   timestamp=getattr(point, "timestamp", None),
                   provider=getattr(point, "provider", None))


def read_current_price(stream_current_price, symbol: str) -> Optional[MarketPrice]:
    """
    Read `symbol`'s latest price from an existing
    stream.current_price.CurrentPrice and return it as a MarketPrice, or
    None if unknown. Pure read -- never writes, never computes, never
    raises for a missing symbol.
    """
    if stream_current_price is None:
        return None
    point = stream_current_price.get(symbol)
    return MarketPrice.from_price_point(point)
