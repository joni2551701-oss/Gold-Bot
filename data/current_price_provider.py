"""
Current Price Provider (TASK‑CORE‑004 Phase 1, Director Decision 1).

The single abstraction between the Telegram layer and the market‑data
cache for the "Current Price" feature:

    Telegram → CurrentPriceProvider → current production cache
    (future)  Telegram → CurrentPriceProvider → MemoryReader (v1.1)

Telegram never reads the cache directly (Director order). Swapping the
backend from the production `SmartDataCache` to the v1.1 `MemoryReader`
is a change **inside this module only** — no Telegram code changes during
the future v1.1 migration (that is the whole point of this seam).

**Read‑only and fail‑safe.** It reads the *already‑cached* last candle and
**never triggers a provider fetch / network request / API call** — a
button press must not spend API quota. Returns ``None`` (→ empty state)
when no price is cached yet.

This module never imports from any layer above `data/`; it is pure
read access over the existing cache.
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
    only already‑available data (never fetching). `SmartCacheLastPriceSource`
    is the production backend; a future `MemoryReader`‑backed source
    implements the same one method."""

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


class CurrentPriceProvider:
    """
    The stable interface the Telegram layer depends on. Delegates to a
    swappable `LastPriceSource` (default: the production `SmartDataCache`).
    Fail‑safe: never raises, never fetches. Symbol is normalised to the
    canonical upper‑case form the cache/pipeline use (e.g. ``"XAUUSD"``).
    """

    def __init__(self, source: Optional[LastPriceSource] = None):
        self._source = source or SmartCacheLastPriceSource()

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
    """Production wiring: reads the existing `SmartDataCache` (no fetch).
    Later, swap the source for a `MemoryReader`‑backed one — Telegram is
    unaffected."""
    return CurrentPriceProvider(source=SmartCacheLastPriceSource())
