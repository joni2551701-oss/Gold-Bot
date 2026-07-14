"""
Data Layer — Market Provider Interface (Phase 59.1: Market Data
Provider Abstraction & TwelveData Integration Foundation, TASK 1).

MarketDataProvider is the abstract contract every market data source
(TwelveData today, MT5 in a future, separately-approved phase) must
implement. A provider is data-only:

    A provider NEVER generates a signal.
    A provider NEVER knows about a strategy.
    A provider NEVER knows about a decision.
    A provider only returns data.

No implementation lives in this file -- see twelve_data_provider.py
and mt5_provider.py (same package).

NAMING NOTE -- read before using this module: data/twelve_data_client.py
already defines Candle (timestamp, open, high, low, close -- no
symbol/timeframe/volume of its own, the real type
data/market_data.py's MarketDataNormalizer and the entire live
pipeline already use). MarketCandle (this module) is a distinct,
richer, standardized shape for the NEW provider abstraction layer
only -- it carries its own symbol/timeframe/volume, matching this
phase's own brief's exact output shape. MarketCandle does not replace
Candle, and data/twelve_data_client.py is untouched by this phase; a
TwelveDataProvider (twelve_data_provider.py) adapts one Candle into
one MarketCandle per candle, it does not change what
TwelveDataClient.fetch_candles() itself returns.
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class MarketCandle:
    """
    The provider layer's standard candle shape -- exactly this
    phase's own brief:

        MarketCandle(symbol="XAUUSD", timeframe="M15", open=, high=,
                     low=, close=, volume=None, timestamp=)

    volume is always None from every provider in this phase -- no
    fake/synthetic volume is ever fabricated. TwelveData's time_series
    endpoint does not return volume for XAU/USD-style pairs, and MT5
    is not implemented yet (mt5_provider.py); a future MT5 provider
    that has a real tick-volume source may populate this field, but
    nothing in this codebase does today.
    """
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    timestamp: datetime
    volume: Optional[float] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass(frozen=True)
class ProviderStatus:
    """
    available: whether this provider can currently serve data (e.g.
        an API key is configured). Checking this is always safe --
        never raises, even for a provider with no real implementation
        (mt5_provider.py's MT5Provider.get_market_status() always
        returns available=False, never raises).
    reason: a short, human-readable explanation. Empty string when
        available is True.
    """
    available: bool
    reason: str = ""


class MarketDataProvider(ABC):
    """
    Abstract contract every market data provider implements. A
    provider is data-only -- see this module's own docstring for the
    three things a provider must never do.
    """

    @abstractmethod
    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        """
        Returns candles for `symbol` at `timeframe`, most recent
        `limit` at most, chronologically ascending (oldest first) --
        matching data/twelve_data_client.py's own fetch_candles()
        ordering convention. Never returns None; an empty list is the
        "no data" case, not an exception, matching this codebase's
        established fail-safe posture for data-driven conditions.
        """
        raise NotImplementedError

    @abstractmethod
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """
        The most recent known close price for `symbol`, or None if
        unavailable. Never raises for a data-driven "no price yet"
        condition.
        """
        raise NotImplementedError

    @abstractmethod
    def get_market_status(self) -> ProviderStatus:
        """
        Whether this provider can currently serve data. Must never
        raise -- this is the one method a caller can always call
        safely to check availability before calling get_candles()/
        get_latest_price(), even for a provider with no real
        implementation.
        """
        raise NotImplementedError
