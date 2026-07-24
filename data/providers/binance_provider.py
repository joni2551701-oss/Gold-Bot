"""
Data Layer — Binance Provider stub (Phase 59.2, TASK 3).

Foundation only, for a future v0.9 Multi Asset phase — **no real
Binance API connection exists in this file**. No `python-binance`/
`ccxt` dependency, no HTTP calls, no websocket. Every data-fetch
method raises NotImplementedError, the same honest-stub pattern
mt5_provider.py's MT5Provider already established.

Unlike MT5Provider, this stub DOES validate the requested symbol
before raising "not implemented" — a real, testable distinction (see
"Symbol validation" below) between "this symbol isn't one Binance even
lists" (a genuine input error, ValueError) and "this symbol is a real
Binance pair, but GoldBot's BinanceProvider doesn't fetch real data
yet" (NotImplementedError). MT5 has no defined symbol universe of its
own to validate against yet, so it does not make this distinction.
"""

from typing import List, Optional, Tuple

from data.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus

# Binance's own symbol format (no separator, quote asset suffixed --
# "BTCUSDT", not "BTC/USDT" or "BTCUSD") -- deliberately different
# from TwelveDataProvider's SUPPORTED_SYMBOLS ("BTCUSD", TwelveData's
# own convention). This is real, disclosed provider-to-provider format
# divergence, not a bug -- a future real BinanceProvider implementation
# would need its own symbol-mapping step, not a shared one with
# TwelveData. Only the two symbols this task's brief names.
SUPPORTED_SYMBOLS = ("BTCUSDT", "ETHUSDT")

# Binance's own kline (candlestick) interval vocabulary is a superset
# of GoldBot's -- this tuple lists only the subset a future
# implementation would map onto GoldBot's existing timeframe
# vocabulary (M5/M15/H1/H4/Daily), not Binance's full interval list.
SUPPORTED_TIMEFRAMES: Tuple[str, ...] = ("M5", "M15", "H1", "H4", "Daily")


class BinanceProvider(MarketDataProvider):
    """
    A deliberate, inert stub -- no exchange connection of any kind.
    See docs/PROVIDER_CONTRACTS.md for what a real implementation
    would need to add (API key/secret, rate-limit handling, a real
    kline-interval mapping).
    """

    UNIMPLEMENTED_REASON = "Binance integration is not implemented yet (v0.9 Multi Asset foundation only)"

    def get_provider_name(self) -> str:
        return "binance"

    def get_supported_timeframes(self) -> Tuple[str, ...]:
        """Non-empty, unlike MT5Provider's stub -- this is documented, intended future capability, not a live guarantee. Never raises."""
        return SUPPORTED_TIMEFRAMES

    def _validate_symbol(self, symbol: str) -> None:
        """Raises ValueError for a symbol outside SUPPORTED_SYMBOLS -- a genuine input error, checked before the "not implemented" signal."""
        if symbol not in SUPPORTED_SYMBOLS:
            raise ValueError(
                f"Unsupported Binance symbol {symbol!r}. Supported: {', '.join(SUPPORTED_SYMBOLS)}"
            )

    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        self._validate_symbol(symbol)
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_latest_price(self, symbol: str) -> Optional[float]:
        self._validate_symbol(symbol)
        raise NotImplementedError(self.UNIMPLEMENTED_REASON)

    def get_market_status(self) -> ProviderStatus:
        """Always available=False. Never raises -- same safe-status-check pattern as MT5Provider."""
        return ProviderStatus(available=False, reason=self.UNIMPLEMENTED_REASON)
