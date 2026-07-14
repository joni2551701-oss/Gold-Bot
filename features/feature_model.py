"""
Feature Layer — data model (Phase A10, corrected).

MarketFeatures is the standard, per-candidate feature snapshot a
future AI Analyzer, backtester, or ML dataset exporter would consume
-- one flat, documented shape instead of each future consumer
re-deriving its own subset from raw ContextSnapshot/SignalCandidate/
SignalQualityResult fields. It is a standardization layer, not an
analysis layer: every field is either a direct read of an
already-computed result or an explicit, honest None placeholder --
never a new calculation, never a fabricated value. See
docs/FEATURE_ENGINEERING.md for the full contract and
feature_engine.py for how each field is computed.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MarketFeatures:
    """
    asset: the symbol this cycle analyzed (e.g. "XAUUSD").
    timeframe: the execution interval this cycle analyzed (e.g. "M15").
    htf_bias: context.htf_bias.HTFBiasResult.bias.value, reused
        directly (e.g. "BULLISH"). "UNKNOWN" if no HTFBiasResult was
        supplied.
    market_regime: context.market_regime.MarketRegimeResult.regime.value,
        reused directly (e.g. "TRENDING", "RANGE").
    session: the current session's name (e.g. "LONDON"), reused from
        the most recent context.session.SessionEvent. "UNKNOWN" if no
        session data was available.
    signal_quality: signals.explainability.SignalExplanation.quality
        (the letter grade already produced by Signal Quality Score),
        relayed as-is -- not recomputed here.
    confidence: signals.explainability.SignalExplanation.confidence
        (SignalCandidate.confidence * 100, already relayed by
        Explainability), relayed as-is -- not recomputed here.
    volatility: "HIGH"/"LOW"/"NORMAL"/"UNKNOWN", reused directly from
        context.market_regime.MarketRegimeResult.regime.
    trend_strength: 0.0-1.0. context.market_regime.MarketRegimeResult
        .confidence / 100.0 when the regime is TRENDING, else 0.0 --
        not a new trend calculation.
    liquidity_distance: absolute distance from the most recent
        candle's close to the nearest detected LiquidityZone's price
        -- None if no candles or no liquidity zones exist.
    volume: always None. This codebase has no volume data source at
        all (Twelve Data's Candle payload is OHLC-only, confirmed
        repeatedly since Phase A1's audit) -- an explicit, honest
        hook, never a fabricated value.
    atr: always None in this phase. A textbook Average True Range
        would be a new indicator, out of scope for a foundation/
        standardization phase -- an explicit hook for a future,
        separately-approved phase (Advanced Risk/Quant Research/ML),
        never a fabricated value. See docs/FEATURE_ENGINEERING.md's
        "ATR hook" section.
    """
    asset: str
    timeframe: str
    htf_bias: str
    market_regime: str
    session: str
    signal_quality: str
    confidence: float
    volatility: str
    trend_strength: float
    liquidity_distance: Optional[float]
    volume: Optional[float] = None
    atr: Optional[float] = None
