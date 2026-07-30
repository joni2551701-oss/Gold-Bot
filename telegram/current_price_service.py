"""
Telegram Layer — Current Price service (TASK‑CORE‑004 Phase 1).

Renders the informational "Current Price" message for a user. It calls
`data.current_price_provider.CurrentPriceProvider` (never the cache
directly — Director Decision 1) and formats a localized message.

**Read‑only / informational only.** No signal generation, trade
execution, risk, AI, or strategy path (Director Decision 2 scope limit).
Fail‑safe: never raises into the Telegram event loop; a missing price
degrades to the localized empty‑state string.

Handler → this service → `CurrentPriceProvider` (the `CLAUDE.md`
handler→service pattern; the provider plays the read‑only data‑access
role here, replacing "repository" for market data).
"""

from dataclasses import dataclass
from typing import Dict, Optional

from core.logger import setup_logger
from data.current_price_provider import CurrentPrice, CurrentPriceProvider
from translation.ui_catalog import t

logger = setup_logger("CurrentPriceService")


@dataclass(frozen=True)
class AssetMeta:
    display: str
    icon: str
    precision: int = 2


# Production trades XAUUSD (Gold) today (`assets/asset_type.py`). Extensible:
# add a symbol here and the feature supports it — no other code change.
# (BTCUSDT was an MVP‑only source and is NOT tracked by the production
# pipeline, so it is deliberately not listed — no fabricated data.)
ASSET_META: Dict[str, AssetMeta] = {
    "XAUUSD": AssetMeta(display="XAU/USD", icon="🥇", precision=2),
}
DEFAULT_ASSET = "XAUUSD"


class CurrentPriceService:
    """Serves the localized Current Price message. Holds only a
    `CurrentPriceProvider` reference; never fetches or mutates anything."""

    def __init__(self, provider: Optional[CurrentPriceProvider] = None):
        self._provider = provider or CurrentPriceProvider()

    def render(self, language: str = "EN", symbol: str = DEFAULT_ASSET) -> str:
        """
        The Current Price block, exactly:

            📊 Current Price
            🥇 XAU/USD
            Price:
            3368.42
            Updated:
            14:52:08 UTC

        (labels localized). An unknown asset or a not‑yet‑available price
        both render the localized empty‑state. Never raises.
        """
        sym = (symbol or "").strip().upper()
        meta = ASSET_META.get(sym)
        cp: Optional[CurrentPrice] = None
        try:
            cp = self._provider.get_current_price(sym)
        except Exception as e:  # noqa: BLE001 -- fail‑safe
            logger.warning("current price read failed for %s: %s", sym, e)
            cp = None

        if meta is None or cp is None:
            return t("price.empty", language)
        try:
            price = f"{float(cp.price):.{meta.precision}f}"
            updated = cp.timestamp.strftime("%H:%M:%S")
        except Exception:  # noqa: BLE001 -- malformed value never crashes a button
            return t("price.empty", language)

        return (
            f"{t('price.title', language)}\n"
            f"{meta.icon} {meta.display}\n"
            f"{t('price.price_label', language)}:\n"
            f"{price}\n"
            f"{t('price.updated_label', language)}:\n"
            f"{updated} UTC"
        )


def build_default_current_price_service() -> CurrentPriceService:
    """Production wiring — reads the existing production cache via the
    provider, no fetch, no secret exposed."""
    return CurrentPriceService(provider=CurrentPriceProvider())
