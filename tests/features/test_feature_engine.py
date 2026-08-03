"""
Phase A10 (corrected) -- Feature Engineering foundation tests
(features/feature_engine.py).

No mocking -- real ContextSnapshot/MarketRegimeResult/SessionEvent/
LiquidityZone/HTFBiasResult/SignalExplanation objects, same convention
as tests/context/test_market_regime.py and
tests/signals/test_explainability.py.

Feature Engineering is a standardization layer, not an analysis
layer: it runs at the end of the per-candidate analysis chain, after
Signal Quality Score and Explainability -- signal_quality/confidence
are relayed directly from a SignalExplanation, never recomputed here.
"""

import dataclasses
from datetime import datetime, timezone

from features.feature_engine import compute_market_features
from features.feature_model import MarketFeatures
from context_layer.context_engine.context_orchestrator import ContextSnapshot
from context_layer.trend.market_regime import MarketRegimeResult, MarketRegime, RegimeDirection
from context_layer.session.session import Session, SessionEvent
from context_layer.liquidity.liquidity import LiquidityZone, LiquidityType
from context_layer.trend.htf_bias import HTFBias, HTFBiasResult
from signals.explainability import SignalExplanation
from data_layer.providers.twelve_data_client import Candle

TS = datetime(2024, 1, 2, 9, 0, tzinfo=timezone.utc)  # 09:00 UTC -- LONDON per context_layer/session/session.py


def _empty_context(**overrides) -> ContextSnapshot:
    base = dict(
        candles=(),
        structure=(),
        bos_events=(),
        choch_events=(),
        liquidity_zones=(),
        liquidity_sweeps=(),
        order_blocks=(),
        fair_value_gaps=(),
        amd_events=(),
        wyckoff_events=(),
        session_events=(),
        market_regime=MarketRegimeResult(
            regime=MarketRegime.UNKNOWN, direction=RegimeDirection.NEUTRAL, confidence=0.0, reasons=[],
        ),
    )
    base.update(overrides)
    return ContextSnapshot(**base)


def _candle(hour, high=105.0, low=100.0, close=102.0):
    return Candle(timestamp=datetime(2024, 1, 2, hour, tzinfo=timezone.utc), open=101.0, high=high, low=low, close=close)


def _htf(bias):
    return HTFBiasResult(bias=bias, confidence=100.0, timeframes=("Daily", "H4", "H1"), quality_score=1.0)


def _explanation(quality="A+", confidence=86.0, direction="BUY", reasons=()):
    return SignalExplanation(direction=direction, reasons=tuple(reasons), quality=quality, confidence=confidence)


def test_feature_creation_from_full_context():
    candles = [_candle(9, high=110.0, low=100.0, close=105.0)]
    context = _empty_context(
        candles=candles,
        liquidity_zones=(LiquidityZone(price=120.0, type=LiquidityType.BSL, start_index=0, end_index=1, strength=2),),
        session_events=(SessionEvent(index=1, timestamp=TS, session=Session.LONDON),),
        market_regime=MarketRegimeResult(
            regime=MarketRegime.TRENDING, direction=RegimeDirection.BULLISH, confidence=85.0, reasons=[],
        ),
    )
    explanation = _explanation(quality="A+", confidence=86.0)

    features = compute_market_features(context, explanation, "XAUUSD", "M15", _htf(HTFBias.BULLISH))

    assert isinstance(features, MarketFeatures)
    assert features.asset == "XAUUSD"
    assert features.timeframe == "M15"
    assert features.session == "LONDON"
    assert features.market_regime == "TRENDING"
    assert features.htf_bias == "BULLISH"
    assert features.signal_quality == "A+"
    assert features.confidence == 86.0
    assert features.trend_strength == 0.85
    assert features.volatility == "NORMAL"
    assert features.liquidity_distance == 15.0  # |105 - 120|
    assert features.volume is None
    assert features.atr is None  # atr is always a hook, never computed in this phase


def test_signal_quality_and_confidence_are_relayed_not_recomputed():
    """signal_quality/confidence must come straight from the already-computed SignalExplanation, never re-derived."""
    context = _empty_context()

    for quality, confidence in [("A+", 95.0), ("C", 12.5)]:
        features = compute_market_features(context, _explanation(quality=quality, confidence=confidence), "XAUUSD", "M15", None)
        assert features.signal_quality == quality
        assert features.confidence == confidence


def test_volatility_reuses_market_regime_classification():
    high_vol = _empty_context(
        market_regime=MarketRegimeResult(
            regime=MarketRegime.HIGH_VOLATILITY, direction=RegimeDirection.NEUTRAL, confidence=65.0, reasons=[],
        ),
    )
    low_vol = _empty_context(
        market_regime=MarketRegimeResult(
            regime=MarketRegime.LOW_VOLATILITY, direction=RegimeDirection.NEUTRAL, confidence=65.0, reasons=[],
        ),
    )

    assert compute_market_features(high_vol, _explanation(), "XAUUSD", "M15", None).volatility == "HIGH"
    assert compute_market_features(low_vol, _explanation(), "XAUUSD", "M15", None).volatility == "LOW"


def test_trend_strength_is_zero_when_not_trending():
    ranging = _empty_context(
        market_regime=MarketRegimeResult(
            regime=MarketRegime.RANGE, direction=RegimeDirection.NEUTRAL, confidence=50.0, reasons=[],
        ),
    )

    assert compute_market_features(ranging, _explanation(), "XAUUSD", "M15", None).trend_strength == 0.0


def test_missing_context_degrades_gracefully():
    """No session events, no liquidity zones, no htf_bias -- must not raise, must report UNKNOWN/None."""
    candles = [_candle(9)]
    context = _empty_context(candles=candles)  # no session_events, no liquidity_zones

    features = compute_market_features(context, _explanation(), "XAUUSD", "M15", htf_bias=None)

    assert features.session == "UNKNOWN"
    assert features.liquidity_distance is None
    assert features.htf_bias == "UNKNOWN"
    assert features.market_regime == "UNKNOWN"  # default market_regime in _empty_context()


def test_empty_data_produces_no_crash_and_none_fields():
    context = _empty_context()  # zero candles at all

    features = compute_market_features(context, _explanation(), "XAUUSD", "M15", htf_bias=None)

    assert features.liquidity_distance is None
    assert features.session == "UNKNOWN"
    assert isinstance(features, MarketFeatures)


def test_no_fake_volume_or_atr_ever():
    """volume and atr must always be None -- across every scenario, never a fabricated number."""
    scenarios = [
        _empty_context(),
        _empty_context(candles=[_candle(9)]),
        _empty_context(
            candles=[_candle(9)],
            market_regime=MarketRegimeResult(
                regime=MarketRegime.TRENDING, direction=RegimeDirection.BULLISH, confidence=85.0, reasons=[],
            ),
        ),
    ]
    for context in scenarios:
        features = compute_market_features(context, _explanation(), "XAUUSD", "M15", _htf(HTFBias.BULLISH))
        assert features.volume is None
        assert features.atr is None


def test_future_compatibility_field_shape_is_stable():
    """MarketFeatures is a plain, introspectable dataclass -- a future consumer can rely on its field set."""
    field_names = {f.name for f in dataclasses.fields(MarketFeatures)}
    assert field_names == {
        "asset", "timeframe", "htf_bias", "market_regime", "session", "signal_quality",
        "confidence", "volatility", "trend_strength", "liquidity_distance", "volume", "atr",
    }

    # Direct construction via keyword args (e.g. a future backtester replaying historical
    # features) must work without going through compute_market_features() at all.
    manual = MarketFeatures(
        asset="XAUUSD", timeframe="M15", htf_bias="NEUTRAL", market_regime="RANGE", session="ASIA",
        signal_quality="B", confidence=55.0, volatility="NORMAL", trend_strength=0.5, liquidity_distance=3.2,
    )
    assert manual.volume is None  # default applies even without passing it explicitly
    assert manual.atr is None  # default applies even without passing it explicitly


def test_never_raises_across_extreme_inputs():
    extreme_contexts = [
        _empty_context(),
        _empty_context(candles=[_candle(h) for h in range(24)]),
        _empty_context(liquidity_zones=(LiquidityZone(price=0.0, type=LiquidityType.SSL, start_index=0, end_index=0, strength=1),)),
    ]
    for context in extreme_contexts:
        for htf in (None, _htf(HTFBias.BULLISH), _htf(HTFBias.UNKNOWN)):
            result = compute_market_features(context, _explanation(), "XAUUSD", "M15", htf)
            assert isinstance(result, MarketFeatures)
