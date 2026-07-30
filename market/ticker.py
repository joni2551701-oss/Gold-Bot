"""
Market Layer — Ticker read model (TASK-CORE-005).

A fast, current price/ticker snapshot for the market façade's
consumers. Optional bid/ask are carried but never fabricated (no
provider supplies them today). No history, no signal, no logic --
purely a read value adapted from the latest price or stream event.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Ticker:
    """Latest price for a symbol, plus optional bid/ask. bid/ask default None and are never invented."""
    symbol: str
    price: float
    timestamp: Optional[datetime] = None
    provider: Optional[str] = None
    bid: Optional[float] = None
    ask: Optional[float] = None

    @classmethod
    def from_market_price(cls, market_price) -> Optional["Ticker"]:
        """Adapt a market.current_price.MarketPrice into a Ticker. None-safe."""
        if market_price is None:
            return None
        return cls(symbol=market_price.symbol, price=market_price.price,
                   timestamp=market_price.timestamp, provider=market_price.provider)

    @classmethod
    def from_stream_event(cls, event) -> "Ticker":
        """Adapt a stream.StreamEvent's close price into a Ticker (public attributes only)."""
        return cls(symbol=event.symbol, price=event.close,
                   timestamp=getattr(event, "timestamp", None),
                   provider=getattr(event, "provider", None))
