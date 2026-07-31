"""
MarketDataService -- the Data Layer facade for candle-shaped market
data: get_candles(), get_snapshot(), and historical series
(TASK-DATA-001, Phase 2).

Deliberately a separate service from `data.stream.price_stream_service
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
  - `data.market_data.MarketDataNormalizer` -- get_candles()/
    get_snapshot() fetch + validate + quality logic.
  - `data.historical_data_collector.collect_historical_candles()` --
    historical range collection + persistence (Phase 59.5).
  - `data.providers.get_provider()` -- the configured
    `MarketDataProvider` historical collection reads from.

Conservative in this phase: `get_candles()`/`get_snapshot()` delegate
directly to `MarketDataNormalizer`, uncached -- byte-for-byte the same
data, on the same timing, `TradingPipeline` already relied on before
this facade existed. The HTF Bias snapshot this feeds is one of
`DecisionEngine`'s four weighted inputs (Trading Safety), so this
phase does not change its freshness semantics. Wiring
`data.data_cache.SmartDataCache`'s already-built cache-hit/miss logic
in behind this same interface is a natural, isolated follow-up --
nothing above this service would need to change when that happens.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from typing import List, Optional

from data.market_data import MarketDataNormalizer, MarketSnapshot
from data.twelve_data_client import Candle


class MarketDataService:
    """Facade for candle/snapshot/historical market data. See module
    docstring for the Price Stream Service vs Market Data Service split."""

    def __init__(self, normalizer: Optional[MarketDataNormalizer] = None):
        self._normalizer = normalizer or MarketDataNormalizer()

    def get_candles(self, symbol: str, interval: str, outputsize: int) -> List[Candle]:
        """Same contract as `MarketDataNormalizer.get_candles()` --
        fetch, validate, and clean one timeframe's candles. Never
        raises; an empty list is the "no data" case, not an exception."""
        return self._normalizer.get_candles(symbol, interval, outputsize)

    def get_snapshot(self, symbol: str, intervals: List[str]) -> MarketSnapshot:
        """Same contract as `MarketDataNormalizer.get_snapshot()` -- a
        multi-timeframe `MarketSnapshot` with per-interval quality flags."""
        return self._normalizer.get_snapshot(symbol, intervals)

    def get_historical_candles(self, symbol: str, timeframe: str, start, end,
                                provider=None):
        """Delegates to the existing `historical_data_collector`
        (Phase 59.5) -- fetches and persists a `[start, end)` historical
        range via `provider` (defaults to `data.providers.get_provider()`,
        the single configured `MarketDataProvider`). Not reimplemented
        here; returns the same `CollectionResult` that function returns."""
        from data.historical_data_collector import collect_historical_candles
        from data.providers import get_provider

        return collect_historical_candles(
            provider or get_provider(), symbol, timeframe, start, end,
        )


def build_default_market_data_service() -> MarketDataService:
    """Production wiring: the existing `MarketDataNormalizer` (TwelveData)."""
    return MarketDataService(normalizer=MarketDataNormalizer())
