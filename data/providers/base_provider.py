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

Phase 59.2 (Market Data Intelligence Layer, TASK 1: Provider Contract
Audit) split this into two levels, rather than adding new abstract
methods directly onto MarketDataProvider:

    DataProvider (this module)          -- get_provider_name(), get_market_status()
        |
        +-- MarketDataProvider (this module)      -- candle-shaped data (TwelveData, MT5, Binance)
        |       + get_candles(), get_latest_price(), get_supported_timeframes()
        |
        +-- FundamentalDataProvider (fundamental_base.py) -- macro/economic data (FRED)
                + get_macro_indicator(), get_interest_rate(), get_inflation_data()

Why: TASK 4 (FRED) produces macro/economic time series (interest
rates, CPI, DXY), not OHLC candles -- forcing FredProvider to implement
get_candles()/get_latest_price() would mean fabricating a fake
"candle" for a number that isn't priced data at all. Splitting the
truly universal contract (a stable name + a safe status check, needed
by registry.py and monitoring/provider_health.py, TASK 5/6) from the
candle-specific contract lets both TwelveDataProvider-family and
FredProvider-family providers share one registry without either
faking the other's shape. See docs/PROVIDER_CONTRACTS.md for the full
audit.

Audit decision on the brief's own three candidate methods:
- get_provider_name() -- ADDED (new abstract method on DataProvider).
  Needed by registry.py (TASK 5, keys/labels a provider) and
  monitoring/provider_health.py (TASK 6, reports "TwelveData: ONLINE").
- get_supported_timeframes() -- ADDED (new abstract method on
  MarketDataProvider only -- not universal, since FundamentalDataProvider
  has no timeframe concept in the candle sense). Needed by the same
  two consumers, and by BinanceProvider (TASK 3) to declare its
  future timeframe support without a live API to query.
- get_symbol_info() -- NOT ADDED. No concrete consumer needs it in
  this phase (registry.py keys by provider_name; health monitoring
  reads provider_name/get_market_status(); Binance's own symbol-format
  difference is documented in its own module instead of a new
  interface method). Revisit when a real multi-provider symbol-
  translation consumer exists -- "Yangi interface faqat kerak bo'lsa
  qo'shiladi" (a new interface method is added only when needed).
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional, Tuple


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


class DataProvider(ABC):
    """
    The truly universal contract every data source in data/providers/
    implements, regardless of shape (candle-based or macro/fundamental)
    -- see this module's own docstring for why this level exists
    separately from MarketDataProvider.
    """

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        A short, stable, lowercase identifier -- e.g. "twelvedata",
        "mt5", "binance", "fred". Used as the registry key
        (data/providers/registry.py) and the label
        monitoring/provider_health.py reports against. Must never
        raise, and must be a fixed constant, not derived from live
        state.
        """
        raise NotImplementedError

    @abstractmethod
    def get_market_status(self) -> ProviderStatus:
        """
        Whether this provider can currently serve data. Must never
        raise -- this is the one method a caller can always call
        safely to check availability before calling any data-fetch
        method, even for a provider with no real implementation.
        """
        raise NotImplementedError


class MarketDataProvider(DataProvider):
    """
    Abstract contract every candle-shaped market data provider
    implements (TwelveData, MT5, Binance). A provider is data-only --
    see this module's own docstring for the three things a provider
    must never do.
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
    def get_supported_timeframes(self) -> Tuple[str, ...]:
        """
        The timeframe strings this provider can serve (e.g.
        ("M5","M15","H1","H4","Daily")) -- static capability metadata,
        not a live call, so it must never raise, even for a provider
        with no real implementation (an empty tuple is the honest
        answer for "not implemented yet", not an exception -- a
        registry or health check iterating every registered provider
        must be able to call this on all of them without a
        try/except).
        """
        raise NotImplementedError
