"""
Feature Layer — data model (Phase A10).

MarketFeatures is the standard feature snapshot a future AI Analyzer,
backtester, or ML dataset exporter would consume -- one flat,
documented shape instead of each future consumer re-deriving its own
subset from raw ContextSnapshot fields. See docs/FEATURE_ENGINEERING.md
for the full contract and feature_engine.py for how each field is
computed.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MarketFeatures:
    """
    atr: real average range for the current session (see
        feature_engine.py's docstring for why this is a
        session-scoped range proxy, not a textbook Wilder ATR) --
        None if no candles were available to compute it.
    volatility: "HIGH"/"LOW"/"NORMAL"/"UNKNOWN", reused directly from
        context.market_regime.MarketRegimeResult.regime.
    trend_strength: 0.0-1.0. context.market_regime.MarketRegimeResult
        .confidence / 100.0 when the regime is TRENDING, else 0.0 --
        not a new trend calculation.
    session: the current session's name (e.g. "LONDON"), reused from
        the most recent context.session.SessionEvent. "UNKNOWN" if no
        session data was available.
    regime: context.market_regime.MarketRegimeResult.regime.value,
        reused directly (e.g. "TRENDING", "RANGE").
    htf_bias: context.htf_bias.HTFBiasResult.bias.value, reused
        directly (e.g. "BULLISH"). "UNKNOWN" if no HTFBiasResult was
        supplied.
    liquidity_distance: absolute distance from the most recent
        candle's close to the nearest detected LiquidityZone's price
        -- None if no candles or no liquidity zones exist.
    volume: always None. This codebase has no volume data source at
        all (Twelve Data's Candle payload is OHLC-only, confirmed
        repeatedly since Phase A1's audit) -- an explicit, honest
        hook, never a fabricated value. See
        docs/FEATURE_ENGINEERING.md's "Volume hook" section.
    """
    atr: Optional[float]
    volatility: str
    trend_strength: float
    session: str
    regime: str
    htf_bias: str
    liquidity_distance: Optional[float]
    volume: Optional[float] = None
