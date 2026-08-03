"""
MemoryReader -- the read-only platform contract over MarketMemory
(DD-031). Phase 1 module 2.

Every future client (Telegram, Mini App, Android, iOS, Desktop, Web, AI,
Chart, Signal/Risk) reads market data through this one interface and
never touches a data provider (Memory-First). MemoryReader is
constructed over a MarketMemoryRegistry and exposes ONLY reads -- it has
no write method, so a consumer can never mutate memory.

Incremental delivery (architecture §25 / DD-038):
- This module delivers the READ facade: get_last_candle, get_last_closed,
  get_forming, get_series, revision, mode, health, timeframes, assets.
- `subscribe` / `unsubscribe` are the DD-028 event-bus surface and are
  delivered in module 7 (Event Bus); `snapshot` is delivered in module 9
  (Snapshot API). Their signatures are declared here so the DD-031
  contract is visible now; the bodies raise NotImplementedError until
  their modules land (a backward-compatible fill-in, not a signature
  change).

All returned candles are copies (copy-on-read is enforced by the
underlying TimeframeMemory), so readers never alias internal state.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any

from data_layer.market_memory.market_memory_registry import MarketMemoryRegistry
from data_layer.market_memory.market_memory import MarketMemory
from data_layer.market_memory.timeframe_memory import TimeframeMemory
from data_layer.market_memory.candle_record import CandleRecord, MemoryMode


class MemoryReader:
    """Read-only facade over a MarketMemoryRegistry (DD-031)."""

    def __init__(self, registry: MarketMemoryRegistry):
        if registry is None:
            raise ValueError("registry must not be None")
        self._registry = registry

    # -- resolution helpers --------------------------------------------
    def _asset(self, asset: str) -> MarketMemory:
        return self._registry.get(asset)

    def _tf(self, asset: str, timeframe: str) -> TimeframeMemory:
        return self._registry.get(asset).timeframe(timeframe)

    # -- discovery ------------------------------------------------------
    def assets(self) -> List[str]:
        return self._registry.assets()

    def timeframes(self, asset: str) -> List[str]:
        return self._asset(asset).timeframes()

    def mode(self, asset: str) -> MemoryMode:
        """LIVE or REPLAY for the asset (DD-033)."""
        return self._asset(asset).mode

    # -- candle reads (copy-on-read) -----------------------------------
    def get_last_candle(self, asset: str, timeframe: str
                        ) -> Optional[CandleRecord]:
        """Forming candle if present, else the last closed candle."""
        return self._tf(asset, timeframe).get_last()

    def get_last_closed(self, asset: str, timeframe: str
                        ) -> Optional[CandleRecord]:
        return self._tf(asset, timeframe).get_last_closed()

    def get_forming(self, asset: str, timeframe: str
                    ) -> Optional[CandleRecord]:
        return self._tf(asset, timeframe).get_forming()

    def get_series(self, asset: str, timeframe: str,
                   n: Optional[int] = None,
                   include_forming: bool = False) -> List[CandleRecord]:
        """Up to the last `n` candles (oldest -> newest), as copies."""
        return self._tf(asset, timeframe).get_series(
            n=n, include_forming=include_forming)

    # -- versioning / health -------------------------------------------
    def revision(self, asset: str, timeframe: str) -> int:
        """O(1) change signal for the (asset, timeframe) (DD-029)."""
        return self._tf(asset, timeframe).revision()

    def health(self, asset: str) -> Dict[str, Any]:
        return self._asset(asset).health()

    # -- deferred surface (declared for the DD-031 contract) -----------
    def subscribe(self, asset: str, timeframe: str, handler: Any) -> Any:
        """Delivered in module 7 (Event Bus, DD-028)."""
        raise NotImplementedError(
            "subscribe() is delivered in Phase 1 module 7 (Event Bus)")

    def unsubscribe(self, handle: Any) -> None:
        """Delivered in module 7 (Event Bus, DD-028)."""
        raise NotImplementedError(
            "unsubscribe() is delivered in Phase 1 module 7 (Event Bus)")

    def snapshot(self, asset: str,
                 timeframes: Optional[List[str]] = None) -> Any:
        """Delivered in module 9 (Snapshot API, DD-034)."""
        raise NotImplementedError(
            "snapshot() is delivered in Phase 1 module 9 (Snapshot API)")
