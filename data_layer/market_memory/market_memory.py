"""
MarketMemory -- one asset's multi-timeframe memory (DD-030 non-singleton,
DD-033 LIVE/REPLAY).

Owns an independent TimeframeMemory per configured timeframe. This class
is deliberately NOT a singleton: a MarketMemoryRegistry holds one
MarketMemory per asset (XAUUSD, BTCUSD, ...), so multiple instruments run
concurrently without an architecture change.

This module never imports from any layer above data/.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Any, Mapping

from data_layer.market_memory.candle_record import MemoryMode
from data_layer.market_memory.timeframe_memory import TimeframeMemory


class MarketMemory:
    """Per-asset container of TimeframeMemory objects."""

    def __init__(self, asset: str, timeframe_capacities: Mapping[str, int],
                 mode: MemoryMode = MemoryMode.LIVE):
        if not asset:
            raise ValueError("asset must be a non-empty string")
        if not timeframe_capacities:
            raise ValueError("timeframe_capacities must not be empty")
        self._asset = asset
        self._lock = threading.RLock()
        self._mode = mode
        self._timeframes: Dict[str, TimeframeMemory] = {
            tf: TimeframeMemory(asset, tf, cap)
            for tf, cap in timeframe_capacities.items()
        }

    @property
    def asset(self) -> str:
        return self._asset

    @property
    def mode(self) -> MemoryMode:
        with self._lock:
            return self._mode

    def set_mode(self, mode: MemoryMode) -> None:
        """Switch LIVE <-> REPLAY (DD-033)."""
        if not isinstance(mode, MemoryMode):
            raise TypeError(f"mode must be a MemoryMode, got {mode!r}")
        with self._lock:
            self._mode = mode

    def timeframes(self) -> List[str]:
        with self._lock:
            return list(self._timeframes.keys())

    def has_timeframe(self, timeframe: str) -> bool:
        with self._lock:
            return timeframe in self._timeframes

    def timeframe(self, timeframe: str) -> TimeframeMemory:
        """Return the TimeframeMemory for `timeframe` (raises if unknown)."""
        with self._lock:
            try:
                return self._timeframes[timeframe]
            except KeyError:
                raise KeyError(
                    f"{self._asset} has no timeframe {timeframe!r}; "
                    f"known: {sorted(self._timeframes)}")

    def health(self) -> Dict[str, Any]:
        """Aggregate per-timeframe health for the monitor / snapshot."""
        with self._lock:
            return {
                "asset": self._asset,
                "mode": self._mode.value,
                "timeframes": {
                    tf: mem.health() for tf, mem in self._timeframes.items()
                },
            }
