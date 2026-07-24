"""
StreamManager -- supervises one PriceStream per asset (v1.1 Phase 1,
module 4; DD-030 multi-asset).

Each asset has its own PriceStream + provider + CandleBuilder sink +
MarketMemory, so instruments run independently (single-writer per asset
preserved). The manager registers streams and advances them; a real
deployment drives `tick_all(now)` in a loop (one worker per asset in a
threaded deployment), but the manager keeps the coordination logic
clock-injected and testable.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Any

from data.stream.price_stream import PriceStream
from data.stream.stream_event import StreamState


class StreamManager:
    """Registry-aligned supervisor of per-asset PriceStreams."""

    def __init__(self):
        self._streams: Dict[str, PriceStream] = {}

    def add(self, stream: PriceStream) -> PriceStream:
        if stream.asset in self._streams:
            raise ValueError(f"stream for {stream.asset!r} already registered")
        self._streams[stream.asset] = stream
        return stream

    def get(self, asset: str) -> PriceStream:
        return self._streams[asset]

    def assets(self) -> List[str]:
        return list(self._streams.keys())

    def tick_all(self, now: datetime) -> Dict[str, StreamState]:
        """Advance every stream one step; returns each asset's new state."""
        return {asset: s.tick(now) for asset, s in self._streams.items()}

    def shutdown_all(self, now: datetime = None) -> Dict[str, Any]:
        """Graceful shutdown of every stream (DD-050)."""
        return {asset: s.shutdown(now) for asset, s in self._streams.items()}

    def health(self) -> Dict[str, Any]:
        return {asset: s.health() for asset, s in self._streams.items()}
