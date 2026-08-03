"""
CachePolicy -- freshness, TTL and eviction for the persistent cache
(module 6).

Freshness is keyed on the candle-close boundary (a timeframe's cache is
fresh until the next candle after it was written closes) -- the same idea
as the existing SmartDataCache `_get_next_candle_time`, generalized to all
six timeframes via candle_clock. An optional wall-clock TTL and an LRU
size cap bound the durable footprint.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Dict, List

from data_layer.live_data.candle_clock import CandleClock


class CachePolicy:
    def __init__(self, clock: Optional[CandleClock] = None,
                 ttl_seconds: Optional[float] = None,
                 max_entries: Optional[int] = None):
        self._clock = clock or CandleClock()
        self._ttl = ttl_seconds
        self._max_entries = max_entries

    def is_fresh(self, timeframe: str, written_at: datetime,
                 now: datetime) -> bool:
        """
        Fresh until the candle following `written_at` closes (candle-close
        boundary), and within the optional TTL.
        """
        if self._ttl is not None and (now - written_at).total_seconds() >= self._ttl:
            return False
        next_close = self._clock.next_boundary(timeframe, written_at) + timedelta(
            minutes=self._clock.minutes(timeframe))
        return now < next_close

    def evictions(self, last_access: Dict[str, datetime]) -> List[str]:
        """
        Return the keys to evict (LRU) when over `max_entries`. No cap ->
        nothing evicted.
        """
        if self._max_entries is None or len(last_access) <= self._max_entries:
            return []
        ordered = sorted(last_access.items(), key=lambda kv: kv[1])
        overflow = len(last_access) - self._max_entries
        return [k for k, _ in ordered[:overflow]]
