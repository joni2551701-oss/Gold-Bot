"""
PriceStreamService -- the single Price Stream API for GoldBot
(TASK-DATA-001, Price Stream Foundation).

    price_stream.get_price("XAUUSD")
    price_stream.get_price("BTCUSDT")

is the ONLY sanctioned way any consumer (TradingPipeline,
CurrentPriceProvider, Telegram, Chart, Dashboard, future AI) reads a
live price -- calling a `PriceProvider`/vendor API directly is not
permitted (task requirement). Adding a new provider (Binance,
CoinGecko, OANDA, Polygon, ...) means registering one more
`PriceProvider` adapter here; nothing above this service changes.

Reuse (Module Reuse Principle): this module is pure orchestration. It
wires already-existing building blocks together rather than
reimplementing any of them:
  - `data_layer.live_data.price_stream.PriceStream` / `stream_manager.StreamManager`
    -- per-asset lifecycle state machine (v1.1 Phase 1, module 4).
  - `data_layer.live_data.twelve_data_provider.TwelveDataProvider` /
    `data_layer.live_data.bitget_price_source.BitgetPriceSource` -- vendor
    adapters (DD-048 provider abstraction).
  - `data_layer.live_data.price_cache.PriceCache` -- last-tick-per-symbol store.
  - `data_layer.event_system.event_bus.EventBus` -- publishes `PRICE.UPDATED`
    (`EventType.PRICE_UPDATED`) whenever a tick lands.

`PriceStream` normally forwards `StreamEvent`s to the CandleBuilder
sink (module 3, candle aggregation). `tick(now)` must be driven by a
caller (a scheduler loop) exactly like `StreamManager` already
requires; this service does not start a background thread of its own.

Market Memory write path (TASK-DATA-004, opt-in): when a
`MarketMemoryRegistry` is supplied, `register_source()` also builds one
`data_layer.live_data.candle_builder.CandleBuilder` per asset over that asset's
`data_layer.market_memory.MarketMemory`, and the sink forwards every `StreamEvent`
to it -- so live ticks fold into the existing, Director-accepted
MarketMemory (MA-001) via its documented SINGLE WRITER (CandleBuilder),
not by a second, parallel write path. This reuses the frozen memory
core rather than duplicating it. The `PriceCache` + `PRICE.UPDATED`
behavior is unchanged and runs alongside it; the memory write is
absolutely fail-safe (a CandleBuilder error never reaches the stream or
the cache). With no registry supplied (the default, and what
`build_default_price_stream_service()` still produces for the Phase 3
`CurrentPriceProvider` path), behavior is byte-for-byte as before --
no memory objects are constructed. Foundation only: no consumer reads
the memory yet, and nothing drives `tick()` in production, so this
changes no existing runtime behavior.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from core_layer.logger.logger import setup_logger
from data_layer.event_system.event_bus import EventBus
from data_layer.event_system.event_model import Event, EventType
from data_layer.live_data.price_cache import PriceCache
from data_layer.live_data.price_stream import PriceStream
from data_layer.live_data.price_tick import PriceTick
from data_layer.live_data.provider import PriceProvider
from data_layer.live_data.stream_event import AssetClass, StreamEvent
from data_layer.live_data.stream_manager import StreamManager

logger = setup_logger("PriceStreamService")


class _PriceTickSink:
    """`PriceStream` sink adapter: converts each forwarded `StreamEvent`
    into a `PriceTick`, stores it in `PriceCache`, publishes
    `PRICE.UPDATED` on the event bus, and (when a `candle_builder` is
    supplied) folds the tick into MarketMemory via that single writer.
    Isolated from `PriceStream`'s own error handling -- it only ever
    receives already-validated events."""

    def __init__(self, provider_name: str, cache: PriceCache,
                 event_bus: Optional[EventBus], candle_builder: Any = None):
        self._provider_name = provider_name
        self._cache = cache
        self._event_bus = event_bus
        self._candle_builder = candle_builder

    def on_event(self, event: StreamEvent) -> None:
        tick = PriceTick(
            symbol=event.asset,
            price=event.price,
            timestamp=event.timestamp,
            provider=self._provider_name,
            volume=event.volume,
        )
        self._cache.update(tick)
        if self._event_bus is not None:
            self._event_bus.publish(Event(
                type=EventType.PRICE_UPDATED,
                payload=tick,
                asset=tick.symbol,
                event_id=f"price-{tick.symbol}-{tick.timestamp.timestamp()}",
                timestamp=datetime.now(timezone.utc),
                source="PriceStreamService",
            ))
        # TASK-DATA-004: fold the tick into MarketMemory via the single
        # writer (CandleBuilder). Absolutely fail-safe -- a memory write
        # failure must never disturb the cache/event path above, exactly
        # like PriceStream isolates provider errors (DD-051).
        if self._candle_builder is not None:
            try:
                self._candle_builder.on_event(event)
            except Exception as e:  # noqa: BLE001 -- fail-safe memory write
                logger.warning(
                    "PriceStreamService memory write failed for %s: %s: %s",
                    tick.symbol, type(e).__name__, str(e)[:200])


class PriceStreamService:
    """The one Data Layer price-stream API every consumer reads through."""

    def __init__(self, cache: Optional[PriceCache] = None,
                 event_bus: Optional[EventBus] = None,
                 memory_registry: Any = None):
        # memory_registry: an optional data_layer.market_memory.MarketMemoryRegistry.
        # When supplied, register_source() builds a per-asset
        # CandleBuilder over that registry's MarketMemory so live ticks
        # fold into the existing MarketMemory (MA-001) via its single
        # writer. Default None -> no memory writes, behavior unchanged.
        self._cache = cache or PriceCache()
        self._event_bus = event_bus
        self._memory_registry = memory_registry
        self._manager = StreamManager()

    def register_source(self, symbol: str, provider: PriceProvider,
                         provider_name: str,
                         asset_class: AssetClass = AssetClass.METAL,
                         calendar: Any = None,
                         validator: Any = None) -> PriceStream:
        """Register one asset's `PriceProvider` with the stream. Call once
        per symbol at startup (e.g. XAUUSD/TwelveDataProvider,
        BTCUSDT/BitgetPriceSource).

        `calendar` (TASK-ARCH-101): an optional `MarketCalendar` (e.g.
        `data_layer.live_data.market_calendar.ForexMarketCalendar`) driving
        weekend/market-closed waiting mode. Default None -> the
        `PriceStream` default (AlwaysOpenCalendar), behavior unchanged.
        `validator` (TASK-ARCH-101): an optional
        `data_layer.live_data.stream_validator.StreamValidator`; when supplied,
        invalid ticks are dropped before forwarding. Default None ->
        no validation, behavior unchanged."""
        candle_builder = self._build_candle_builder(symbol)
        sink = _PriceTickSink(provider_name, self._cache, self._event_bus,
                              candle_builder=candle_builder)
        stream = PriceStream(asset=symbol, provider=provider, sink=sink,
                              asset_class=asset_class,
                              calendar=calendar, validator=validator)
        return self._manager.add(stream)

    def _build_candle_builder(self, symbol: str):
        """Construct one CandleBuilder (the MarketMemory single writer)
        for `symbol` over the injected registry's MarketMemory, or return
        None when no registry was supplied. Fail-safe: any construction
        problem degrades to None (no memory writes) rather than blocking
        stream registration."""
        if self._memory_registry is None:
            return None
        try:
            from data_layer.live_data.candle_builder import CandleBuilder
            memory = self._memory_registry.get_or_create(symbol)
            return CandleBuilder(symbol, memory)
        except Exception as e:  # noqa: BLE001 -- fail-safe wiring
            logger.warning(
                "PriceStreamService could not wire MarketMemory for %s: %s: %s",
                symbol, type(e).__name__, str(e)[:200])
            return None

    def tick(self, now: Optional[datetime] = None) -> Dict[str, Any]:
        """Advance every registered stream by one step. A caller (a
        scheduler loop) drives this; the service starts no thread itself."""
        now = now or datetime.now(timezone.utc)
        return self._manager.tick_all(now)

    def get_price(self, symbol: str) -> Optional[PriceTick]:
        """The sanctioned read API: the latest cached `PriceTick` for
        `symbol`, or `None` if no tick has arrived yet. Never fetches --
        purely a cache read, same fail-safe posture as
        `CurrentPriceProvider`."""
        try:
            return self._cache.get((symbol or "").strip().upper())
        except Exception as e:  # noqa: BLE001 -- fail-safe read
            logger.warning("PriceStreamService.get_price failed for %s: %s: %s",
                            symbol, type(e).__name__, str(e)[:200])
            return None

    def health(self) -> Dict[str, Any]:
        return self._manager.health()

    def shutdown(self, now: Optional[datetime] = None) -> Dict[str, Any]:
        return self._manager.shutdown_all(now or datetime.now(timezone.utc))


def build_default_price_stream_service(memory_registry: Any = None
                                        ) -> PriceStreamService:
    """Production wiring: XAUUSD via TwelveData, BTCUSDT via Bitget
    (currently an honest stub -- see `bitget_price_source.py`).

    `memory_registry` (TASK-DATA-004): pass a shared
    `data_layer.market_memory.MarketMemoryRegistry` to also fold ticks into
    MarketMemory (share the same instance with
    `build_default_market_data_service()` for one source of truth).
    Omitted by default so the Phase 3 `CurrentPriceProvider` path that
    lazily builds this service is completely unchanged (no memory
    objects constructed, no behavior change).

    GFL-001 FLOW-001 (Current Price, Data Validation module): every
    registered source is wired with the canonical
    `data_layer.live_data.stream_validator.StreamValidator` (TASK-ARCH-101),
    dropping empty/non-finite/non-positive-price/future-timestamp/
    duplicate/out-of-order ticks before they ever reach the cache or
    MarketMemory -- reusing the validator that already existed for this
    exact purpose rather than adding a second one."""
    from data_layer.live_data.bitget_price_source import BitgetPriceSource
    from data_layer.live_data.stream_validator import StreamValidator
    from data_layer.live_data.twelve_data_provider import TwelveDataProvider

    validator = StreamValidator()
    service = PriceStreamService(memory_registry=memory_registry)
    service.register_source("XAUUSD", TwelveDataProvider(asset="XAUUSD"),
                             provider_name="twelvedata",
                             asset_class=AssetClass.METAL,
                             validator=validator)
    service.register_source("BTCUSDT", BitgetPriceSource(asset="BTCUSDT"),
                             provider_name="bitget",
                             asset_class=AssetClass.CRYPTO,
                             validator=validator)
    return service


_shared_service: Optional[PriceStreamService] = None


def get_shared_price_stream_service(memory_registry: Any = None
                                     ) -> PriceStreamService:
    """GFL-001 FLOW-001 (Current Price, Price Stream + Market Memory
    modules): the ONE process-wide `PriceStreamService` every default
    `CurrentPriceProvider` reads through (see
    `data_layer.live_data.current_price_provider.PriceStreamLastPriceSource`)
    AND the one a driver's `tick(now)` loop (e.g.
    `platform_layer.telegram.polling._price_stream_tick_loop`) advances --
    the same object, so ticking it is what a Telegram `/price` reader
    actually observes. Without this, each `CurrentPriceProvider()`
    default-constructed its own private, never-ticked service (see
    `build_default_price_stream_service()`'s own docstring history), so
    a driver ticking one instance could never be seen by a reader
    holding a different one.

    Built once, lazily, on first call; `memory_registry` only matters
    for that first build (a `MarketMemoryRegistry()` is constructed by
    default so live ticks also fold into the canonical, Director-
    accepted MarketMemory SSOT -- MA-001/DD-030/DD-031 -- satisfying
    FLOW-001's documented Consumer without a second write path).
    Subsequent calls return the same instance regardless of arguments.
    `reset_shared_price_stream_service()` clears it (test isolation)."""
    global _shared_service
    if _shared_service is None:
        from data_layer.market_memory import MarketMemoryRegistry
        _shared_service = build_default_price_stream_service(
            memory_registry=memory_registry or MarketMemoryRegistry())
    return _shared_service


def reset_shared_price_stream_service() -> None:
    """Test-isolation helper: clears the process-wide singleton so the
    next `get_shared_price_stream_service()` call builds a fresh one."""
    global _shared_service
    _shared_service = None
