"""
PriceTick -- the unified, provider-agnostic price observation
(TASK-DATA-001, Price Stream Foundation).

Every `PriceProvider` adapter (TwelveData, Bitget, ...) is read by
`PriceStreamService` and folded into exactly this one shape before it
reaches `PriceCache` or the event bus, so a consumer never needs to know
which vendor produced a given price. `bid`/`ask`/`volume` are optional --
not every provider/asset class has them (XAUUSD may have bid/ask,
BTCUSDT reports volume instead) -- `None` means "not reported", never a
fabricated value.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class PriceTick:
    """One unified price observation, already provider-normalized."""
    symbol: str
    price: float
    timestamp: datetime            # UTC, timezone-aware
    provider: str
    bid: Optional[float] = None
    ask: Optional[float] = None
    volume: Optional[float] = None
