"""
Data Layer — MT5 Provider stub (Phase 59.1, TASK 1).

MT5 integration itself is explicitly out of scope for this phase (the
Director's own brief: "MT5 uchun vaqt sarflash kerak emas" -- no time
should be spent on MT5 right now). This file exists only so the
provider abstraction (base_provider.py's MarketDataProvider) has a
second, real implementation to prove the interface generalizes beyond
TwelveData -- every method here is an honest, disclosed placeholder,
never a fabricated result.

get_market_status() is the one method that must always be safe to
call, even with no MT5 terminal, no MetaTrader5 package installed, and
no connection -- this is what "MT5 yo'q bo'lsa tizim yiqilmaydi" (the
system does not crash if MT5 is absent) means in practice: a caller
checks get_market_status().available before ever calling
get_candles()/get_latest_price(), and that check itself never raises.
get_candles()/get_latest_price() raise NotImplementedError if called
directly -- a genuine "this doesn't exist yet" signal for a caller
that skips the status check, not a silently wrong empty result.
"""

from typing import List, Optional, Tuple

from data.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus


class MT5Provider(MarketDataProvider):
    """
    A deliberate, inert stub -- no MetaTrader5 package dependency, no
    terminal connection attempt, no order/execution code (that
    would be execution/'s job in a future, separately-approved phase,
    not this data-only provider). See docs/MARKET_PROVIDER.md's "MT5
    Future Integration" section for what a real implementation would
    need to add.
    """

    UNAVAILABLE_REASON = "MT5 integration is not implemented yet (Phase 59.1 is TwelveData-only)"

    def get_provider_name(self) -> str:
        return "mt5"

    def get_supported_timeframes(self) -> Tuple[str, ...]:
        """Empty -- an honest "not implemented yet" answer, never raises (see base_provider.py's own docstring on why this must be safe to call on every registered provider)."""
        return ()

    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        raise NotImplementedError(self.UNAVAILABLE_REASON)

    def get_latest_price(self, symbol: str) -> Optional[float]:
        raise NotImplementedError(self.UNAVAILABLE_REASON)

    def get_market_status(self) -> ProviderStatus:
        """Always available=False. Never raises -- this is the one safe way to detect MT5 is absent."""
        return ProviderStatus(available=False, reason=self.UNAVAILABLE_REASON)
