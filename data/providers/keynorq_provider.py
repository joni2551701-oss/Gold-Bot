"""
Data Layer — Keynorq Provider stub (TASK-CORE-003).

Foundation only for a future custom-source phase — **no real Keynorq
API connection exists in this file**. No SDK, no HTTP call. Every
data-fetch method raises NotImplementedError, the same honest-stub
pattern mt5_provider.py / binance_provider.py / bitget_provider.py
already established.

Keynorq is a *custom* data source with no publicly-defined symbol or
timeframe universe yet, so -- unlike BinanceProvider/BitgetProvider --
this stub does NOT pretend to validate symbols or declare timeframes
it cannot actually serve. It follows MT5Provider's most-conservative
honest posture: get_supported_timeframes() returns () and the
data-fetch methods raise NotImplementedError for any input. That is
the truthful answer for "not implemented yet, universe unknown", not a
fabricated capability.

Like BitgetProvider, it reads its API key through config only
(config.get_settings().providers.keynorq_api_key, a MaskedSecret) --
proving the config -> provider secret hand-off and that the secret is
masked. `.env` is NEVER read here. The key is never logged, printed, or
placed in an error message.
"""

from typing import List, Optional, Tuple

import config
from data.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus


class KeynorqProvider(MarketDataProvider):
    """
    A deliberate, inert stub for a custom source -- no connection of any
    kind, no assumed symbol/timeframe universe. The API key is obtained
    from config (masked) purely to exercise the config->provider
    settings path; it is never used for a live call in this phase.
    """

    UNIMPLEMENTED_REASON = "Keynorq integration is not implemented yet (custom-source foundation only)"

    def __init__(self, settings=None) -> None:
        self._settings = settings or config.get_settings()

    @property
    def _api_key(self):
        """The MaskedSecret for KEYNORQ_API_KEY -- render/log-safe (repr is `***`). Read from config only."""
        return self._settings.providers.keynorq_api_key

    def get_provider_name(self) -> str:
        return "keynorq"

    def get_supported_timeframes(self) -> Tuple[str, ...]:
        """Empty -- an honest 'not implemented yet, universe unknown' answer. Never raises."""
        return ()

    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_latest_price(self, symbol: str) -> Optional[float]:
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_market_status(self) -> ProviderStatus:
        """Always available=False. Never raises -- the one safe way to detect Keynorq is absent."""
        return ProviderStatus(available=False, reason=self.UNIMPLEMENTED_REASON)
