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
  - `data.stream.price_stream.PriceStream` / `stream_manager.StreamManager`
    -- per-asset lifecycle state machine (v1.1 Phase 1, module 4).
  - `data.stream.twelve_data_provider.TwelveDataProvider` /
    `data.stream.bitget_price_source.BitgetPriceSource` -- vendor
    adapters (DD-048 provider abstraction).
  - `data.price_cache.PriceCache` -- last-tick-per-symbol store.
  - `data.events.event_bus.EventBus` -- publishes `PRICE.UPDATED`
    (`EventType.PRICE_UPDATED`) whenever a tick lands.

`PriceStream` normally forwards `StreamEvent`s to the CandleBuilder
sink (module 3, candle aggregation) -- this service does NOT replace
that consumer; it registers as an independent sink that only cares
about the latest price, not candle building. `tick(now)` must be
driven by a caller (a scheduler loop) exactly like `StreamManager`
already requires; this service does not start a background thread of
its own.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from core.logger import setup_logger
from data.events.event_bus import EventBus
from data.events.event_model import Event, EventType
from data.price_cache import PriceCache
from data.stream.price_stream import PriceStream
from data.stream.price_tick import PriceTick
from data.stream.provider import PriceProvider
from data.stream.stream_event import AssetClass, StreamEvent
from data.stream.stream_manager import StreamManager

logger = setup_logger("PriceStreamService")


class _PriceTickSink:
    """`PriceStream` sink adapter: converts each forwarded `StreamEvent`
    into a `PriceTick`, stores it in `PriceCache`, and publishes
    `PRICE.UPDATED` on the event bus. Isolated from `PriceStream`'s own
    error handling -- it only ever receives already-validated events."""

    def __init__(self, provider_name: str, cache: PriceCache,
                 event_bus: Optional[EventBus]):
        self._provider_name = provider_name
        self._cache = cache
        self._event_bus = event_bus

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


class PriceStreamService:
    """The one Data Layer price-stream API every consumer reads through."""

    def __init__(self, cache: Optional[PriceCache] = None,
                 event_bus: Optional[EventBus] = None):
        self._cache = cache or PriceCache()
        self._event_bus = event_bus
        self._manager = StreamManager()

    def register_source(self, symbol: str, provider: PriceProvider,
                         provider_name: str,
                         asset_class: AssetClass = AssetClass.METAL) -> PriceStream:
        """Register one asset's `PriceProvider` with the stream. Call once
        per symbol at startup (e.g. XAUUSD/TwelveDataProvider,
        BTCUSDT/BitgetPriceSource)."""
        sink = _PriceTickSink(provider_name, self._cache, self._event_bus)
        stream = PriceStream(asset=symbol, provider=provider, sink=sink,
                              asset_class=asset_class)
        return self._manager.add(stream)

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


def build_default_price_stream_service() -> PriceStreamService:
    """Production wiring: XAUUSD via TwelveData, BTCUSDT via Bitget
    (currently an honest stub -- see `bitget_price_source.py`)."""
    from data.stream.bitget_price_source import BitgetPriceSource
    from data.stream.twelve_data_provider import TwelveDataProvider

    service = PriceStreamService()
    service.register_source("XAUUSD", TwelveDataProvider(asset="XAUUSD"),
                             provider_name="twelvedata",
                             asset_class=AssetClass.METAL)
    service.register_source("BTCUSDT", BitgetPriceSource(asset="BTCUSDT"),
                             provider_name="bitget",
                             asset_class=AssetClass.CRYPTO)
    return service
