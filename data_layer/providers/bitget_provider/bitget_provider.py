"""
Data Layer — Bitget Provider stub (TASK-CORE-003).

Foundation only for a future crypto/fallback phase — **no real Bitget
API connection exists in this file**. No `ccxt`/`bitget` SDK, no HTTP
call, no websocket. Every data-fetch method raises NotImplementedError,
the same honest-stub pattern binance_provider.py / mt5_provider.py
already established.

Two intentional differences from the older MT5/Binance stubs, both
aligned with TASK-CORE-003's requirements:

1. It reads its API key through config only (config.get_settings().
   providers.bitget_api_key, a MaskedSecret) -- proving the
   config -> provider secret hand-off works and that the secret is
   masked. `.env` is NEVER read here (only config.py reads .env). The
   key is never logged, printed, or placed in an error message; even
   its repr renders `***`.
2. Like BinanceProvider, it validates the requested symbol against a
   crypto symbol set before signalling "not implemented", separating a
   genuine bad-symbol input error (ValueError) from "this real pair
   isn't wired to live data yet" (NotImplementedError).

Bitget spot uses the no-separator, quote-suffixed format ("BTCUSDT"),
same surface convention as Binance -- a real implementation would still
need its own symbol-mapping step, not a shared one.
"""

from typing import List, Optional, Tuple

import config
from data_layer.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus

SUPPORTED_SYMBOLS = ("BTCUSDT", "ETHUSDT")
SUPPORTED_TIMEFRAMES: Tuple[str, ...] = ("M5", "M15", "H1", "H4", "Daily")


class BitgetProvider(MarketDataProvider):
    """
    A deliberate, inert stub -- no exchange connection of any kind. The
    API key is obtained from config (masked) purely to exercise the
    config->provider settings path; it is never used for a live call in
    this phase.
    """

    UNIMPLEMENTED_REASON = "Bitget integration is not implemented yet (crypto/fallback foundation only)"

    def __init__(self, settings=None) -> None:
        # settings is injectable for tests; defaults to the central
        # config singleton. The key is a MaskedSecret -- never a raw str.
        self._settings = settings or config.get_settings()

    @property
    def _api_key(self):
        """The MaskedSecret for BITGET_API_KEY -- render/log-safe (repr is `***`). Read from config only."""
        return self._settings.providers.bitget_api_key

    def get_provider_name(self) -> str:
        return "bitget"

    def get_supported_timeframes(self) -> Tuple[str, ...]:
        """Documented, intended future capability -- never a live guarantee. Never raises."""
        return SUPPORTED_TIMEFRAMES

    def _validate_symbol(self, symbol: str) -> None:
        """Raises ValueError for a symbol outside SUPPORTED_SYMBOLS -- a genuine input error, checked before the 'not implemented' signal."""
        if symbol not in SUPPORTED_SYMBOLS:
            raise ValueError(
                f"Unsupported Bitget symbol {symbol!r}. Supported: {', '.join(SUPPORTED_SYMBOLS)}"
            )

    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        self._validate_symbol(symbol)
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_latest_price(self, symbol: str) -> Optional[float]:
        self._validate_symbol(symbol)
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_market_status(self) -> ProviderStatus:
        """Always available=False. Never raises -- same safe-status-check pattern as the other stubs."""
        return ProviderStatus(available=False, reason=self.UNIMPLEMENTED_REASON)
