"""
Feature Layer — feature calculator foundation (Phase A10, corrected).

Builds a MarketFeatures snapshot entirely from results already
computed elsewhere in the pipeline -- no new indicator, no ML model,
no fabricated value, no strategy/signal-scoring change. This is a
standardization layer, not an analysis layer: it runs at the END of
the per-candidate analysis chain (after Signal Quality Score and
Explainability), turning their already-computed results into one
standard object per candidate for a future AI Analyzer, backtester, or
ML dataset exporter -- see docs/FEATURE_ENGINEERING.md for the full
contract.

Reuses existing detection output rather than duplicating it:
- context.market_regime.MarketRegimeResult (Phase A7) supplies
  volatility classification and trend_strength directly -- neither is
  a new trend/volatility calculation, both are direct reads of
  Market Regime's own already-computed regime/confidence.
- context.session.SessionEvent (Phase A6) supplies the current
  session name -- no new session classification.
- context.htf_bias.HTFBiasResult (Phase A2, passed in externally,
  same as Decision Engine v2/Market Regime) supplies htf_bias.
- ContextSnapshot.liquidity_zones (context/liquidity.py) supplies the
  nearest-zone distance calculation -- no new liquidity detection.
- signals.explainability.SignalExplanation (Phase A9) supplies
  signal_quality and confidence -- both already computed by Signal
  Quality Score/Explainability, relayed here, never recomputed.

Deliberately does NOT compute atr: a textbook Average True Range would
be a new indicator, out of scope for this standardization-only phase
-- atr is always None, an explicit hook for a future phase.
"""

from typing import Optional, TYPE_CHECKING

from context.market_regime import MarketRegime
from features.feature_model import MarketFeatures

if TYPE_CHECKING:
    from context.context_orchestrator import ContextSnapshot
    from context.htf_bias import HTFBiasResult
    from signals.explainability import SignalExplanation


def compute_market_features(
    context: 'ContextSnapshot',
    explanation: 'SignalExplanation',
    asset: str,
    timeframe: str,
    htf_bias: Optional['HTFBiasResult'] = None,
) -> MarketFeatures:
    """
    Never raises: an empty/minimal context (no candles, no session/
    liquidity data, htf_bias=None) produces a MarketFeatures with
    None/"UNKNOWN" fields, not an error. signal_quality/confidence are
    always populated -- explanation is a required, already-computed
    result, never optional.
    """
    regime_result = context.market_regime

    if regime_result.regime == MarketRegime.HIGH_VOLATILITY:
        volatility = "HIGH"
    elif regime_result.regime == MarketRegime.LOW_VOLATILITY:
        volatility = "LOW"
    elif regime_result.regime == MarketRegime.UNKNOWN:
        volatility = "UNKNOWN"
    else:
        volatility = "NORMAL"

    trend_strength = 0.0
    if regime_result.regime == MarketRegime.TRENDING:
        trend_strength = round(regime_result.confidence / 100.0, 4)

    session = context.session_events[-1].session.value if context.session_events else "UNKNOWN"
    market_regime = regime_result.regime.value
    htf_bias_label = htf_bias.bias.value if htf_bias is not None else "UNKNOWN"

    liquidity_distance = None
    if context.candles and context.liquidity_zones:
        current_price = context.candles[-1].close
        liquidity_distance = round(
            min(abs(current_price - zone.price) for zone in context.liquidity_zones), 5
        )

    return MarketFeatures(
        asset=asset,
        timeframe=timeframe,
        htf_bias=htf_bias_label,
        market_regime=market_regime,
        session=session,
        signal_quality=explanation.quality,
        confidence=explanation.confidence,
        volatility=volatility,
        trend_strength=trend_strength,
        liquidity_distance=liquidity_distance,
        volume=None,
        atr=None,
    )
