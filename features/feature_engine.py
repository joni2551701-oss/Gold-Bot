"""
Feature Layer — feature calculator foundation (Phase A10).

Builds a MarketFeatures snapshot entirely from data already computed
elsewhere in the pipeline -- no new indicator, no ML model, no
fabricated value. It does NOT change strategy logic, signal scoring,
or AI behavior -- see docs/FEATURE_ENGINEERING.md for the full
contract.

Reuses existing detection output rather than duplicating it:
- context.session.compute_session_volatility()/classify_session()
  (Phase A6) supply the ATR proxy -- no new range calculation.
- context.market_regime.MarketRegimeResult (Phase A7) supplies
  volatility classification and trend_strength directly -- neither is
  a new trend/volatility calculation, both are direct reads of
  Market Regime's own already-computed regime/confidence.
- context.session.SessionEvent (Phase A6) supplies the current
  session name.
- context.htf_bias.HTFBiasResult (Phase A2, passed in externally,
  same as Decision Engine v2/Market Regime) supplies htf_bias.
- ContextSnapshot.liquidity_zones (context/liquidity.py) supplies the
  nearest-zone distance calculation -- no new liquidity detection.
"""

from typing import Optional, TYPE_CHECKING

from context.market_regime import MarketRegime
from context.session import compute_session_volatility, classify_session
from features.feature_model import MarketFeatures

if TYPE_CHECKING:
    from context.context_orchestrator import ContextSnapshot
    from context.htf_bias import HTFBiasResult


def compute_market_features(
    context: 'ContextSnapshot',
    htf_bias: Optional['HTFBiasResult'] = None,
) -> MarketFeatures:
    """
    Never raises: an empty/minimal context (no candles, no session/
    liquidity data, htf_bias=None) produces a MarketFeatures with
    None/"UNKNOWN" fields, not an error.
    """
    regime_result = context.market_regime

    atr = None
    if context.candles:
        session_ranges = compute_session_volatility(context.candles)
        current_session = classify_session(context.candles[-1].timestamp)
        atr = session_ranges.get(current_session)

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
    regime = regime_result.regime.value
    htf_bias_label = htf_bias.bias.value if htf_bias is not None else "UNKNOWN"

    liquidity_distance = None
    if context.candles and context.liquidity_zones:
        current_price = context.candles[-1].close
        liquidity_distance = round(
            min(abs(current_price - zone.price) for zone in context.liquidity_zones), 5
        )

    return MarketFeatures(
        atr=round(atr, 5) if atr is not None else None,
        volatility=volatility,
        trend_strength=trend_strength,
        session=session,
        regime=regime,
        htf_bias=htf_bias_label,
        liquidity_distance=liquidity_distance,
        volume=None,
    )
