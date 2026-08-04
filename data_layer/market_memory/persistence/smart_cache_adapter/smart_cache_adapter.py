"""
SmartCacheAdapter -- a durable BootstrapCache (module-5 contract) over the
persistent storage backend, completing the cache wiring the bootstrap
deferred to module 6. v1.1 Phase 1, module 6.

Freshness reuses the SmartDataCache lineage (candle-close-boundary
freshness, `_get_next_candle_time`) generalized to all six timeframes via
CachePolicy/candle_clock. Candle lists are stored per (asset, timeframe)
in a StorageBackend, so warm restart is now genuinely durable across
process restarts (File backend) rather than RAM-only.

This module never imports from any layer above data/.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Tuple

from data_layer.providers.twelve_data_client import Candle
from data_layer.live_data.candle_clock import CandleClock
from data_layer.market_memory.persistence.persistent_store import (
    StorageBackend, InMemoryStorageBackend,
)
from data_layer.market_memory.persistence.cache_policy import CachePolicy


class SmartCacheAdapter:
    """Durable BootstrapCache (get/put/is_fresh/last_time)."""

    def __init__(self, backend: Optional[StorageBackend] = None,
                 clock: Optional[CandleClock] = None,
                 policy: Optional[CachePolicy] = None):
        self._backend = backend or InMemoryStorageBackend()
        self._clock = clock or CandleClock()
        self._policy = policy or CachePolicy(clock=self._clock)
        self._written_at: Dict[Tuple[str, str], datetime] = {}

    @staticmethod
    def _key(asset: str, timeframe: str) -> str:
        return f"cache/{asset}/{timeframe}"

    def get(self, asset: str, timeframe: str) -> Optional[List[Candle]]:
        data = self._backend.get(self._key(asset, timeframe))
        if data is None:
            return None
        rows = json.loads(data.decode("utf-8"))
        return [self._row_to_candle(r) for r in rows]

    def put(self, asset: str, timeframe: str,
            candles: List[Candle], when: datetime) -> None:
        rows = [self._candle_to_row(c) for c in candles]
        self._backend.put(self._key(asset, timeframe),
                          json.dumps(rows, separators=(",", ":")).encode("utf-8"))
        self._written_at[(asset, timeframe)] = when

    def is_fresh(self, asset: str, timeframe: str, now: datetime) -> bool:
        written = self._written_at.get((asset, timeframe))
        if written is None:
            return False
        return self._policy.is_fresh(timeframe, written, now)

    def last_time(self, asset: str, timeframe: str) -> Optional[datetime]:
        candles = self.get(asset, timeframe)
        if not candles:
            return None
        return max(c.timestamp for c in candles)

    @staticmethod
    def _candle_to_row(c: Candle) -> list:
        return [c.timestamp.isoformat(), c.open, c.high, c.low, c.close]

    @staticmethod
    def _row_to_candle(r: list) -> Candle:
        ts = datetime.fromisoformat(r[0])
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return Candle(timestamp=ts, open=r[1], high=r[2], low=r[3], close=r[4])
