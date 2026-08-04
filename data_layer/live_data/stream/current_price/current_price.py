"""
Stream Layer — Current Price (TASK-CORE-004).

CurrentPrice is the fast, single-value read point for "what is the
latest price right now?" -- the anchor every later layer (Telegram,
future chart, market, context, monitoring, platform) reads from
instead of re-fetching a provider.

Strict scope (TASK-CORE-004): current value ONLY.
    - It stores the latest price per symbol, nothing else.
    - It keeps NO history (that is data/'s job, not the stream layer's).
    - It computes NO signal, indicator, or decision.
No secret is read or logged here.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass(frozen=True)
class PricePoint:
    """One latest-price reading -- price plus the timestamp/provider it came from. Immutable snapshot value."""
    symbol: str
    price: float
    timestamp: Optional[datetime] = None
    provider: Optional[str] = None


class CurrentPrice:
    """
    Holds the latest PricePoint per symbol. `set()` overwrites (last
    write wins -- there is no history); `get()`/`price_of()` read;
    `all()` snapshots every known symbol. Never raises for a missing
    symbol (returns None), matching the codebase's structured-absence
    convention.
    """

    def __init__(self) -> None:
        self._prices: Dict[str, PricePoint] = {}

    def set(self, symbol: str, price: float, timestamp: Optional[datetime] = None,
            provider: Optional[str] = None) -> None:
        """Record the latest price for `symbol`. Overwrites any previous value -- no history is kept."""
        self._prices[symbol] = PricePoint(
            symbol=symbol, price=price, timestamp=timestamp, provider=provider
        )

    def update_from_event(self, event) -> None:
        """Convenience: take the close of a StreamEvent as the latest price. Reads only public attributes."""
        self.set(event.symbol, event.close, getattr(event, "timestamp", None),
                 getattr(event, "provider", None))

    def get(self, symbol: str) -> Optional[PricePoint]:
        """The latest PricePoint for `symbol`, or None if none recorded yet. Never raises."""
        return self._prices.get(symbol)

    def price_of(self, symbol: str) -> Optional[float]:
        """Just the latest float price for `symbol`, or None. Never raises."""
        point = self._prices.get(symbol)
        return point.price if point else None

    def all(self) -> Dict[str, PricePoint]:
        """A shallow copy of every known symbol's latest PricePoint (safe to iterate/serialize)."""
        return dict(self._prices)

    def clear(self) -> None:
        """Drop all recorded prices (e.g. on a stream reset). Never raises."""
        self._prices.clear()
