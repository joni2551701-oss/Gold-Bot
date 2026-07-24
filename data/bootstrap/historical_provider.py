"""
HistoricalProvider -- vendor-agnostic historical data interface (mirrors
the DD-048 provider abstraction for the stream), plus the BootstrapCache
protocol and a simple in-memory cache. v1.1 Phase 1, module 5.

The bootstrap depends only on HistoricalProvider; swapping a vendor means
writing another adapter, nothing above changes. The durable cache
integration (SmartDataCache) is finalized in module 6 (Data Cache
Integration); this module defines the cache contract and an in-memory
default so bootstrap strategies (warm restart / CACHE_ONLY) are complete
and testable now.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Protocol, runtime_checkable, Dict, Tuple

from data.twelve_data_client import Candle
from data.stream.stream_event import ProviderHealth, ProviderCapabilities


class HistoricalProvider(ABC):
    """Abstract historical candle source (vendor-agnostic)."""

    @property
    @abstractmethod
    def capabilities(self) -> ProviderCapabilities:
        """Declared capabilities (supports_historical must be True)."""
        raise NotImplementedError

    @abstractmethod
    def fetch_recent(self, asset: str, timeframe: str, count: int
                     ) -> List[Candle]:
        """The most recent `count` closed candles (cold start)."""
        raise NotImplementedError

    @abstractmethod
    def fetch_range(self, asset: str, timeframe: str,
                    start: datetime, end: datetime) -> List[Candle]:
        """Closed candles with start <= timestamp < end (gap-fill / incremental)."""
        raise NotImplementedError

    @abstractmethod
    def health(self) -> ProviderHealth:
        raise NotImplementedError


@runtime_checkable
class BootstrapCache(Protocol):
    """Durable cache contract (concrete SmartDataCache adapter = module 6)."""
    def get(self, asset: str, timeframe: str) -> Optional[List[Candle]]: ...
    def put(self, asset: str, timeframe: str,
            candles: List[Candle], when: datetime) -> None: ...
    def is_fresh(self, asset: str, timeframe: str, now: datetime) -> bool: ...
    def last_time(self, asset: str, timeframe: str) -> Optional[datetime]: ...


class InMemoryBootstrapCache:
    """
    Minimal in-RAM BootstrapCache for tests and warm-restart logic. A TF
    is 'fresh' until `ttl_seconds` after it was written. Module 6 replaces
    this with a durable SmartDataCache-backed implementation.
    """

    def __init__(self, ttl_seconds: float = 60.0):
        self._ttl = ttl_seconds
        self._store: Dict[Tuple[str, str], Tuple[List[Candle], datetime]] = {}

    def get(self, asset, timeframe):
        entry = self._store.get((asset, timeframe))
        return list(entry[0]) if entry else None

    def put(self, asset, timeframe, candles, when):
        self._store[(asset, timeframe)] = (list(candles), when)

    def is_fresh(self, asset, timeframe, now):
        entry = self._store.get((asset, timeframe))
        if not entry:
            return False
        return (now - entry[1]).total_seconds() < self._ttl

    def last_time(self, asset, timeframe):
        entry = self._store.get((asset, timeframe))
        if not entry or not entry[0]:
            return None
        return max(c.timestamp for c in entry[0])
