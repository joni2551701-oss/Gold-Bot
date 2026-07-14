"""
Data Layer — TwelveData Provider (Phase 59.1, TASK 2).

Audit finding this module acts on: the real Twelve Data client is
data/twelve_data_client.py's TwelveDataClient (not "data/twelve_data.py",
the brief's own shorthand filename) -- read in full before writing
this module. It already has retry/backoff (3 attempts, exponential
backoff on HTTP 429), symbol formatting ("XAUUSD" -> "XAU/USD", a
generic 6-character 3+3 split that already, correctly, handles every
symbol this task's brief names: XAU/USD, EUR/USD, GBP/USD, BTC/USD,
ETH/USD -- no new format-adapter logic was needed), and raises
ValueError/ConnectionError for its own error conditions. **Moving it
into this package was not necessary and was not done**: this task's
own brief says so conditionally ("agar ko'chirish kerak bo'lsa" -- "if
it needs to be moved"), and data/twelve_data_client.py is imported
directly by data/market_data.py (the live pipeline's data source) and
referenced by type in multiple existing tests -- moving/renaming it
would be a non-additive refactor this phase's "No unnecessary
refactor" rule forbids. TwelveDataProvider instead wraps the existing,
completely untouched TwelveDataClient.
"""

from typing import List, Optional, Tuple

from data.api_error_classifier import classify_api_error, classify_empty_response
from data.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus
from data.twelve_data_client import TwelveDataClient
from core.logger import setup_logger

logger = setup_logger("TwelveDataProvider")

# The five symbols this task's brief names. Documentation/validation
# only -- data/twelve_data_client.py's own _format_symbol() already
# generically supports any 6-character symbol (a 3+3 split), so no new
# per-symbol formatting logic was needed; this tuple exists so
# get_market_status()/callers can see which symbols this provider is
# actually tested against. Not enforced as a hard whitelist:
# strategies/assets/ only trade "XAUUSD" today (assets/profiles/gold.py,
# Phase A12) -- this list does not change what GoldBot actually trades.
SUPPORTED_SYMBOLS = ("XAUUSD", "EURUSD", "GBPUSD", "BTCUSD", "ETHUSD")


class TwelveDataProvider(MarketDataProvider):
    """
    Wraps TwelveDataClient behind the MarketDataProvider interface.
    Never generates a signal, never knows about a strategy or a
    decision -- only adapts TwelveDataClient's existing Candle output
    into the standard MarketCandle shape (adding symbol/timeframe,
    volume always None -- see base_provider.py's own docstring on why
    no fake volume is ever fabricated).
    """

    def __init__(self, client: Optional[TwelveDataClient] = None):
        # Injectable for tests, same pattern as
        # monitoring/performance.py's PerformanceTracker taking an
        # optional SignalRepository.
        self.client = client or TwelveDataClient()

    def get_provider_name(self) -> str:
        return "twelvedata"

    def get_supported_timeframes(self) -> Tuple[str, ...]:
        """The real, live set -- TwelveDataClient.INTERVAL_MAP's own keys, not a separately maintained duplicate list."""
        return tuple(self.client.INTERVAL_MAP.keys())

    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        """
        Delegates entirely to TwelveDataClient.fetch_candles() -- no
        retry/backoff/error-handling logic is reimplemented here. An
        empty result is logged via classify_empty_response() (TASK 5,
        API_004) -- a precise, known condition, not guessed from an
        exception. A raised exception (ValueError/ConnectionError from
        fetch_candles()) is logged via classify_api_error() and then
        re-raised -- unlike data/market_data.py's get_candles(), this
        method does NOT swallow the exception into an empty list; it
        is a thinner adapter, and the caller (a future pipeline wiring
        step, not this phase) decides how to degrade.
        """
        try:
            raw_candles = self.client.fetch_candles(symbol, timeframe, limit)
        except Exception as e:
            logger.error(classify_api_error(e, module="TwelveDataProvider").to_dict())
            raise

        if not raw_candles:
            logger.warning(classify_empty_response(symbol, timeframe).to_dict())
            return []

        return [
            MarketCandle(
                symbol=symbol,
                timeframe=timeframe,
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                timestamp=candle.timestamp,
                volume=None,
            )
            for candle in raw_candles
        ]

    def get_latest_price(self, symbol: str) -> Optional[float]:
        """
        An honest, disclosed simplification: Twelve Data's time_series
        endpoint (the only endpoint TwelveDataClient calls) is
        candle-based, not a live tick/quote stream, so "latest price"
        here means the most recent M5 candle's close -- not a live
        bid/ask. Returns None (never raises) if no candle is
        available, e.g. no API key configured, the market is closed,
        or the underlying fetch fails -- unlike get_candles() (which
        re-raises), get_latest_price() catches and swallows any
        exception itself, matching base_provider.py's own contract
        that this method must never raise.
        """
        try:
            candles = self.get_candles(symbol, "M5", 1)
        except Exception:
            return None
        return candles[-1].close if candles else None

    def get_market_status(self) -> ProviderStatus:
        """
        Never raises. available=True only if an API key is configured
        -- the same check TwelveDataClient.fetch_candles() itself
        performs (self.api_key is None -> ValueError), surfaced here
        without needing to attempt a real network call.
        """
        if self.client.api_key is None:
            return ProviderStatus(available=False, reason="TWELVE_DATA_API_KEY not configured")
        return ProviderStatus(available=True, reason="")
