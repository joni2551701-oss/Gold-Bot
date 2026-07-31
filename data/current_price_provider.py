"""
Current Price Provider (TASK‑CORE‑004 Phase 1, Director Decision 1;
TASK‑DATA‑001 Phase 3: default backend swapped to `PriceStreamService`).

The single abstraction between the Telegram layer and live price data
for the "Current Price" feature:

    Telegram → CurrentPriceProvider → PriceStreamService.get_price()
    (legacy)  Telegram → CurrentPriceProvider → SmartDataCache

Telegram never reads a cache/service directly (Director order). Swapping
the backend is a change **inside this module only** — no Telegram code
changes when the backend changes (that is the whole point of this seam).
As of Phase 3, `PriceStreamLastPriceSource` (wrapping the Price Stream
Foundation's `PriceStreamService.get_price()`, itself a single-tick,
read-only cache lookup — see `data/stream/price_stream_service.py`) is
the default; `SmartCacheLastPriceSource` remains available (and tested)
as the pre‑Phase‑3 backend but is no longer constructed by
`build_default_current_price_provider()`.

**Read‑only and fail‑safe.** It reads already‑cached data and **never
triggers a provider fetch / network request / API call** — a button
press must not spend API quota. Returns ``None`` (→ empty state) when no
price is cached yet.

This module never imports from any layer above `data/`; it is pure
read access over the existing cache/service.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Protocol, runtime_checkable

from core.logger import setup_logger

logger = setup_logger("CurrentPriceProvider")


@dataclass(frozen=True)
class CurrentPrice:
    """One asset's last known price. `price` is the last **closed**
    candle's close; `timestamp` is when that candle closed (tz‑aware UTC)
    — the same value a signal for that candle would have used."""
    asset: str
    price: float
    timestamp: datetime


@runtime_checkable
class LastPriceSource(Protocol):
    """A backend returning the last `CurrentPrice` for a symbol, reading
    only already‑available data (never fetching). `PriceStreamLastPriceSource`
    is the production backend as of Phase 3; `SmartCacheLastPriceSource` is
    the pre‑Phase‑3 backend, still available and tested."""

    def get_current_price(self, symbol: str) -> Optional[CurrentPrice]:
        ...


class SmartCacheLastPriceSource:
    """
    Reads the last cached candle from the production `SmartDataCache`
    **without** triggering a fetch. It inspects the cache's already‑loaded
    per‑(symbol, interval) store (populated by the live pipeline and
    persisted to disk, loaded in `SmartDataCache.__init__`) and returns the
    freshest closed candle's close. It never calls `get_cached_snapshot()`,
    which would fetch (an API call) on a cache miss.
    """

    def __init__(self, cache=None):
        # Lazily construct the SmartDataCache so importing this module is
        # side‑effect free (SmartDataCache.__init__ loads state from disk).
        self._cache = cache

    def _get_cache(self):
        if self._cache is None:
            from data.data_cache import SmartDataCache
            self._cache = SmartDataCache()
        return self._cache

    def get_current_price(self, symbol: str) -> Optional[CurrentPrice]:
        try:
            cache = self._get_cache()
            per_interval = getattr(cache, "cache", {}).get(symbol) or {}
            best = None  # (timestamp, close)
            for _interval, info in per_interval.items():
                candles = (info or {}).get("data") or []
                if not candles:
                    continue
                last = candles[-1]
                ts = getattr(last, "timestamp", None)
                close = getattr(last, "close", None)
                if ts is None or close is None:
                    continue
                if best is None or ts > best[0]:
                    best = (ts, float(close))
            if best is None:
                return None
            return CurrentPrice(asset=symbol, price=best[1], timestamp=best[0])
        except Exception as e:  # noqa: BLE001 -- absolutely fail‑safe read
            logger.warning(
                "SmartCache last‑price read failed for %s: %s: %s",
                symbol, type(e).__name__, str(e)[:200],
            )
            return None


class PriceStreamLastPriceSource:
    """
    Reads the last tick from the Price Stream Foundation's
    `PriceStreamService` (TASK‑DATA‑001 Phase 3) **without** triggering a
    fetch. `PriceStreamService.get_price()` is itself already a pure
    `PriceCache` read (see its own docstring) — this class only adapts
    its `PriceTick` result into this module's `CurrentPrice` shape.
    """

    def __init__(self, service=None):
        # Lazily construct the default PriceStreamService so importing
        # this module stays side‑effect free (mirrors
        # SmartCacheLastPriceSource's lazy SmartDataCache construction).
        self._service = service

    def _get_service(self):
        if self._service is None:
            from data.stream.price_stream_service import build_default_price_stream_service
            self._service = build_default_price_stream_service()
        return self._service

    def get_current_price(self, symbol: str) -> Optional[CurrentPrice]:
        try:
            service = self._get_service()
            tick = service.get_price(symbol)
            if tick is None:
                return None
            return CurrentPrice(asset=tick.symbol, price=tick.price, timestamp=tick.timestamp)
        except Exception as e:  # noqa: BLE001 -- absolutely fail‑safe read
            logger.warning(
                "PriceStream last‑price read failed for %s: %s: %s",
                symbol, type(e).__name__, str(e)[:200],
            )
            return None


class CurrentPriceProvider:
    """
    The stable interface the Telegram layer depends on. Delegates to a
    swappable `LastPriceSource` (default as of Phase 3:
    `PriceStreamService`). Fail‑safe: never raises, never fetches. Symbol
    is normalised to the canonical upper‑case form the cache/pipeline use
    (e.g. ``"XAUUSD"``).
    """

    def __init__(self, source: Optional[LastPriceSource] = None):
        self._source = source or PriceStreamLastPriceSource()

    def get_current_price(self, symbol: str) -> Optional[CurrentPrice]:
        try:
            return self._source.get_current_price((symbol or "").strip().upper())
        except Exception as e:  # noqa: BLE001
            logger.warning(
                "CurrentPriceProvider failed for %s: %s: %s",
                symbol, type(e).__name__, str(e)[:200],
            )
            return None


def build_default_current_price_provider() -> CurrentPriceProvider:
    """Production wiring (Phase 3): reads the `PriceStreamService` (no
    fetch). Later, swap the source for a `MemoryReader`‑backed one —
    Telegram is unaffected."""
    return CurrentPriceProvider(source=PriceStreamLastPriceSource())
