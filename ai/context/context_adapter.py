"""
AI Layer — AI Context Adapter (Phase 61.0: AI Infrastructure
Foundation, TASK 5).

A defensive boundary, not a data source: `sanitize_market_context()`
exists so "AI hech qachon raw market data olmaydi" (AI never receives
raw market data) is enforced structurally, not just by convention --
it rejects a `MarketContext` whose `metadata` carries the kind of
bulk/raw keys a candle-series dump would use, rather than trusting
every future caller to remember not to pass one.
"""

from typing import Optional

from ai.interfaces import MarketContext

# Metadata keys that would indicate a caller accidentally attached raw
# market data (a candle series, a full OHLCV dump) instead of the
# already-summarized text MarketContext.summary is meant to carry.
_FORBIDDEN_METADATA_KEYS = frozenset({"candles", "raw_candles", "ohlcv", "raw_data"})


def sanitize_market_context(market_context: Optional[MarketContext]) -> Optional[MarketContext]:
    """
    Returns `market_context` unchanged if it carries no forbidden raw
    key, or a copy with those keys stripped from `metadata` otherwise.
    Never raises -- a violation is corrected, not fatal, matching this
    codebase's fail-safe posture for foundation modules.
    """
    if market_context is None:
        return None

    offending = _FORBIDDEN_METADATA_KEYS.intersection(market_context.metadata.keys())
    if not offending:
        return market_context

    cleaned_metadata = {
        key: value for key, value in market_context.metadata.items()
        if key not in _FORBIDDEN_METADATA_KEYS
    }
    return MarketContext(
        symbol=market_context.symbol,
        timeframe=market_context.timeframe,
        summary=market_context.summary,
        metadata=cleaned_metadata,
    )
