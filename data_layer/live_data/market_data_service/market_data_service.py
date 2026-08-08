"""
MarketDataService -- the Data Layer facade for candle-shaped market
data: get_candles(), get_snapshot(), and historical series
(TASK-DATA-001, Phase 2).

Deliberately a separate service from `data_layer.live_data.price_stream_service
.PriceStreamService`, per the Phase 1 review split:

    TradingPipeline  -> MarketDataService   (candles/snapshot/history)
    CurrentPriceProvider, Telegram,            (live single-tick price)
    Dashboard, future UI -> PriceStreamService

Both services may share the same underlying providers (TwelveData,
Bitget) and caches -- they answer different questions (a multi-candle
OHLC series vs. the single latest tick) and neither depends on the
other.

Reuse (Module Reuse Principle): pure orchestration over already-
existing modules, none of which are modified by this file:
  - `data_layer.live_data.market_data.MarketDataNormalizer` -- get_candles()/
    get_snapshot() fetch + validate + quality logic.
  - `data_layer.historical_data.historical_data_collector.collect_historical_candles()` --
    historical range collection + persistence (Phase 59.5).
  - `data_layer.providers.get_provider()` -- the configured
    `MarketDataProvider` historical collection reads from.

Conservative in this phase: `get_candles()`/`get_snapshot()` delegate
directly to `MarketDataNormalizer`, uncached -- byte-for-byte the same
data, on the same timing, `TradingPipeline` already relied on before
this facade existed. The HTF Bias snapshot this feeds is one of
`DecisionEngine`'s four weighted inputs (Trading Safety), so this
phase does not change its freshness semantics. Wiring
`data_layer.market_memory.data_cache.SmartDataCache`'s already-built cache-hit/miss logic
in behind this same interface is a natural, isolated follow-up --
nothing above this service would need to change when that happens.

Market Memory write path (TASK-DATA-004, opt-in): when a
`MarketMemoryRegistry` is supplied, `get_candles()`/`get_snapshot()`
also HYDRATE the matching `data_layer.market_memory.TimeframeMemory` with the closed
candles they fetched, so the existing MarketMemory (MA-001) becomes the
single source of truth without a duplicate store. This reuses the
frozen memory core's own `hydrate()`; it is absolutely fail-safe (a
hydrate failure never changes what the method returns) and only ever
writes into a timeframe the memory already holds (`has_timeframe`),
so the "Daily" vs "D1" naming difference is skipped rather than
force-mapped in this foundation phase. The default (no registry) writes
nothing -- so the `TradingPipeline` instance, constructed as bare
`MarketDataService()` in `core/pipeline.py`, is byte-for-byte unchanged
and keeps working exactly the old way (no consumer reads memory yet).

This module never imports from any layer above data/.
"""

from __future__ import annotations

from typing import Any, List, Optional

from core_layer.logger.logger import setup_logger
from data_layer.live_data.market_data import MarketDataNormalizer, MarketSnapshot
from data_layer.providers.twelve_data_client import Candle

logger = setup_logger("MarketDataService")


class MarketDataService:
    """Facade for candle/snapshot/historical market data. See module
    docstring for the Price Stream Service vs Market Data Service split."""

    def __init__(self, normalizer: Optional[MarketDataNormalizer] = None,
                 memory_registry: Any = None):
        # memory_registry: an optional data_layer.market_memory.MarketMemoryRegistry.
        # When supplied, get_candles()/get_snapshot() also hydrate the
        # matching MarketMemory timeframe(s). Default None -> no memory
        # writes, so the pipeline's bare MarketDataService() is unchanged.
        self._normalizer = normalizer or MarketDataNormalizer()
        self._memory_registry = memory_registry

    def get_candles(self, symbol: str, interval: str, outputsize: int) -> List[Candle]:
        """Same contract as `MarketDataNormalizer.get_candles()` --
        fetch, validate, and clean one timeframe's candles. Never
        raises; an empty list is the "no data" case, not an exception."""
        candles = self._normalizer.get_candles(symbol, interval, outputsize)
        self._hydrate_memory(symbol, interval, candles)
        # REAL-DATA-003: Market Memory as SSOT. When a registry is
        # configured, read the just-hydrated candles back OUT of memory so
        # Core consumes the SSOT-stored series rather than the normalizer's
        # direct output. Fail-safe: get_candles_from_memory() returns [] on
        # any miss (unregistered timeframe -- e.g. "Daily" vs "D1" --,
        # empty memory, or read failure), in which case the original
        # validated `candles` are returned unchanged. A bare/no-registry
        # MarketDataService is therefore byte-for-byte unchanged.
        # `candles` guard: when the fetch returned nothing there is
        # nothing hydrated to read back, so skip the memory read entirely
        # (an empty-memory read-back would only log a benign fail-safe
        # UnknownAssetError warning and still return []). Returning the
        # empty `candles` here is byte-for-byte the old behavior.
        if self._memory_registry is not None and candles:
            from_memory = self.get_candles_from_memory(symbol, interval, outputsize)
            if from_memory:
                return from_memory
        return candles

    def get_snapshot(self, symbol: str, intervals: List[str]) -> MarketSnapshot:
        """Same contract as `MarketDataNormalizer.get_snapshot()` -- a
        multi-timeframe `MarketSnapshot` with per-interval quality flags."""
        snapshot = self._normalizer.get_snapshot(symbol, intervals)
        for interval, candles in snapshot.candles.items():
            self._hydrate_memory(symbol, interval, candles)
        return snapshot

    def _hydrate_memory(self, symbol: str, interval: str,
                        candles: List[Candle]) -> None:
        """Fail-safe: load `candles` into the (symbol, interval)
        TimeframeMemory when a registry is configured and that timeframe
        exists. Never raises into the caller and never changes what the
        get_* method returns -- a memory-write failure or a timeframe the
        memory does not hold (e.g. "Daily" vs the memory's "D1") is
        silently skipped."""
        if self._memory_registry is None or not candles:
            return
        try:
            memory = self._memory_registry.get_or_create(symbol)
            if not memory.has_timeframe(interval):
                return
            memory.timeframe(interval).hydrate(candles)
        except Exception as e:  # noqa: BLE001 -- fail-safe memory write
            logger.warning(
                "MarketDataService memory hydrate failed for %s %s: %s: %s",
                symbol, interval, type(e).__name__, str(e)[:200])

    def get_candles_from_memory(self, symbol: str, interval: str,
                                 n: Optional[int] = None) -> List[Candle]:
        """
        GFL-001 FLOW-004 (Market Engine): reads a closed-candle series
        back OUT of Market Memory (the SSOT `get_candles()`/`get_snapshot()`
        already hydrate INTO via `_hydrate_memory()`, TASK-DATA-004)
        through the canonical `data_layer.market_memory.MemoryReader`
        facade -- never reaches into `_memory_registry` directly. Same
        return shape as `get_candles()` (`List[Candle]`, closed bars
        only, oldest -> newest) so this is a drop-in alternative candle
        source for anything that already consumes `get_candles()`'s
        output, ready for
        `context.context_orchestrator.ContextEngine.build()`'s existing,
        frozen `candles` contract. Fail-safe like `get_candles()`: an
        unconfigured registry, an unregistered asset/timeframe, or any
        read failure returns `[]`, never raises.
        """
        if self._memory_registry is None:
            return []
        try:
            from data_layer.market_memory import MemoryReader
            reader = MemoryReader(self._memory_registry)
            records = reader.get_series(symbol, interval, n=n, include_forming=False)
            return [record.to_candle() for record in records]
        except Exception as e:  # noqa: BLE001 -- fail-safe memory read
            logger.warning(
                "MarketDataService memory read failed for %s %s: %s: %s",
                symbol, interval, type(e).__name__, str(e)[:200])
            return []

    def get_historical_candles(self, symbol: str, timeframe: str, start, end,
                                provider=None):
        """Delegates to the existing `historical_data_collector`
        (Phase 59.5) -- fetches and persists a `[start, end)` historical
        range via `provider` (defaults to `data_layer.providers.get_provider()`,
        the single configured `MarketDataProvider`). Not reimplemented
        here; returns the same `CollectionResult` that function returns."""
        from data_layer.historical_data.historical_data_collector import collect_historical_candles
        from data_layer.providers import get_provider

        return collect_historical_candles(
            provider or get_provider(), symbol, timeframe, start, end,
        )


def build_default_market_data_service(memory_registry: Any = None
                                       ) -> MarketDataService:
    """Production wiring: the existing `MarketDataNormalizer` (TwelveData).

    `memory_registry` (TASK-DATA-004): pass a shared
    `data_layer.market_memory.MarketMemoryRegistry` to also hydrate MarketMemory on
    each fetch (share the same instance with
    `build_default_price_stream_service()` for one source of truth).
    Omitted by default -- the `TradingPipeline` continues to construct a
    bare, memory-less `MarketDataService()` and is unaffected."""
    return MarketDataService(normalizer=MarketDataNormalizer(),
                             memory_registry=memory_registry)


_shared_service: Optional[MarketDataService] = None


def get_shared_market_data_service() -> MarketDataService:
    """
    GFL-001 FLOW-004 (Market Engine): the ONE process-wide
    MarketDataService, sharing the SAME `MarketMemoryRegistry` as
    `data_layer.live_data.price_stream_service.get_shared_price_stream_service()`
    -- exactly the pairing `build_default_price_stream_service()`'s own
    docstring already anticipated ("share the same instance with
    `build_default_market_data_service()` for one source of truth",
    TASK-DATA-004), now made real. Built once, lazily, on first call --
    this also lazily builds the shared Price Stream Service if it does
    not exist yet, so whichever of the two callers runs first, both end
    up reading/writing the same registry. Subsequent calls return the
    same instance. `reset_shared_market_data_service()` clears it (test
    isolation).
    """
    global _shared_service
    if _shared_service is None:
        from data_layer.live_data.price_stream_service import get_shared_price_stream_service
        registry = get_shared_price_stream_service().memory_registry
        _shared_service = build_default_market_data_service(memory_registry=registry)
    return _shared_service


def reset_shared_market_data_service() -> None:
    """Test-isolation helper: clears the process-wide singleton so the
    next get_shared_market_data_service() call builds a fresh one."""
    global _shared_service
    _shared_service = None
