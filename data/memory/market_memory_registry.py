"""
MarketMemoryRegistry -- asset -> MarketMemory (DD-030).

MarketMemory is not a singleton. The registry is the single point that
owns per-asset memories, so Gold, BTC, EURUSD, NASDAQ, SP500 ... can run
concurrently. The registry itself is instantiated (not a global
singleton) -- a process holds one, higher layers resolve
`registry.get(asset)`.

`DEFAULT_TIMEFRAME_CAPACITY` is the module's own default timeframe set
(all six ON per DD-026). It is intentionally defined here rather than by
mutating the shared `config.TIMEFRAME_HISTORY`: reconciling the fetch-depth
config with the memory set belongs to the later Historical Bootstrap
Integration module (architecture §25), not to the in-memory core. Callers
may pass their own capacities to override.

This module never imports from any layer above data/.
"""

from __future__ import annotations

import threading
from typing import Dict, List, Mapping, Optional

from data.memory.candle_record import MemoryMode
from data.memory.market_memory import MarketMemory


# All six timeframes ON by default (DD-026). Capacities are memory ring
# depths; M1 is deliberately deeper because entry-precision strategies
# (Liquidity Sweep / SMC / ICT) consume it. Reconciled with fetch depths
# in the Historical Bootstrap Integration module.
DEFAULT_TIMEFRAME_CAPACITY: Dict[str, int] = {
    "M1": 500,
    "M5": 300,
    "M15": 200,
    "H1": 200,
    "H4": 100,
    "D1": 100,
}


class DuplicateAssetError(Exception):
    """Raised when registering an asset that already exists."""


class UnknownAssetError(KeyError):
    """Raised when getting an asset that is not registered."""


class MarketMemoryRegistry:
    """Thread-safe registry of per-asset MarketMemory objects."""

    def __init__(self):
        self._lock = threading.RLock()
        self._memories: Dict[str, MarketMemory] = {}

    def register(
        self,
        asset: str,
        timeframe_capacities: Optional[Mapping[str, int]] = None,
        mode: MemoryMode = MemoryMode.LIVE,
    ) -> MarketMemory:
        """
        Create and register a MarketMemory for `asset`. Raises
        DuplicateAssetError if the asset is already registered.
        """
        caps = dict(timeframe_capacities or DEFAULT_TIMEFRAME_CAPACITY)
        with self._lock:
            if asset in self._memories:
                raise DuplicateAssetError(
                    f"asset {asset!r} is already registered")
            memory = MarketMemory(asset, caps, mode=mode)
            self._memories[asset] = memory
            return memory

    def get_or_create(
        self,
        asset: str,
        timeframe_capacities: Optional[Mapping[str, int]] = None,
        mode: MemoryMode = MemoryMode.LIVE,
    ) -> MarketMemory:
        """Return the existing memory for `asset`, or register a new one."""
        with self._lock:
            existing = self._memories.get(asset)
            if existing is not None:
                return existing
            return self.register(asset, timeframe_capacities, mode=mode)

    def get(self, asset: str) -> MarketMemory:
        """Return the memory for `asset` or raise UnknownAssetError."""
        with self._lock:
            try:
                return self._memories[asset]
            except KeyError:
                raise UnknownAssetError(
                    f"asset {asset!r} is not registered; "
                    f"known: {sorted(self._memories)}")

    def has(self, asset: str) -> bool:
        with self._lock:
            return asset in self._memories

    def assets(self) -> List[str]:
        with self._lock:
            return list(self._memories.keys())

    def remove(self, asset: str) -> None:
        """Remove an asset's memory (raises UnknownAssetError if absent)."""
        with self._lock:
            if asset not in self._memories:
                raise UnknownAssetError(
                    f"asset {asset!r} is not registered")
            del self._memories[asset]


def build_default_registry(assets: Optional[List[str]] = None
                           ) -> MarketMemoryRegistry:
    """
    Convenience factory (mirrors the repo's build_default_registry()
    pattern in assets/asset_registry.py). Registers each asset in
    `assets` with the default timeframe capacities. No singleton -- the
    caller owns the returned registry.
    """
    registry = MarketMemoryRegistry()
    for asset in (assets or []):
        registry.register(asset)
    return registry
