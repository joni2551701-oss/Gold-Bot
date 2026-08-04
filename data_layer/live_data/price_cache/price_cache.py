"""
PriceCache -- per-symbol latest `PriceTick` store (TASK-DATA-001, Price
Stream Foundation).

Deliberately a new, small module rather than extending
`data_layer/market_memory/data_cache.py`'s `SmartDataCache`: `SmartDataCache` stores
multi-candle OHLC series per (symbol, interval) for the pipeline's
Data→Context flow; `PriceCache` stores exactly one thing -- the single
freshest live tick per symbol (no interval, no OHLC, no history) -- for
`PriceStreamService.get_price()`. Bolting a single-tick concept onto a
candle-series cache would mean adding an unrelated shape and access
pattern to an already-documented, pipeline-critical class (Module Reuse
Principle step 2: extending `SmartDataCache` here would break its
current contract, not extend it).

Thread-safe (a real deployment updates it from a stream-tick thread while
consumers read from request/Telegram threads). In-memory only -- no
persistence; a tick is only ever as fresh as the last stream update.

This module never imports from any layer above data/.
"""

from __future__ import annotations

import threading
from typing import Dict, Optional

from data_layer.live_data.price_tick import PriceTick


class PriceCache:
    """Holds the single latest `PriceTick` per symbol."""

    def __init__(self):
        self._lock = threading.RLock()
        self._latest: Dict[str, PriceTick] = {}

    def update(self, tick: PriceTick) -> None:
        with self._lock:
            self._latest[tick.symbol] = tick

    def get(self, symbol: str) -> Optional[PriceTick]:
        with self._lock:
            return self._latest.get(symbol)

    def symbols(self):
        with self._lock:
            return list(self._latest.keys())
