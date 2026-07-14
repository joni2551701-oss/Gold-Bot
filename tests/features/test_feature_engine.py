"""
Phase A10 -- Feature Engineering foundation tests (features/feature_engine.py).

No mocking -- real ContextSnapshot/MarketRegimeResult/SessionEvent/
LiquidityZone/HTFBiasResult objects, same convention as
tests/context/test_market_regime.py and tests/signals/test_explainability.py.
"""

import dataclasses
from datetime import datetime, timezone

from features.feature_engine import compute_market_features
from features.feature_model import MarketFeatures
from context.context_orchestrator import ContextSnapshot
from context.market_regime import MarketRegimeResult, MarketRegime, RegimeDirection
from context.session import Session, SessionEvent
from context.liquidity import LiquidityZone, LiquidityType
from context.htf_bias import HTFBias, HTFBiasResult
from data.twelve_data_client import Candle

TS = datetime(2024, 1, 2, 9, 0, tzinfo=timezone.utc)  # 09:00 UTC -- LONDON per context/session.py


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


def test_feature_creation_from_full_context():
    candles = [_candle(9, high=110.0, low=100.0, close=105.0)]  # single candle -- avoids averaging across the LONDON session
    context = _empty_context(
        candles=candles,
        liquidity_zones=(LiquidityZone(price=120.0, type=LiquidityType.BSL, start_index=0, end_index=1, strength=2),),
        session_events=(SessionEvent(index=1, timestamp=TS, session=Session.LONDON),),
        market_regime=MarketRegimeResult(
            regime=MarketRegime.TRENDING, direction=RegimeDirection.BULLISH, confidence=85.0, reasons=[],
        ),
    )

    features = compute_market_features(context, _htf(HTFBias.BULLISH))

    assert isinstance(features, MarketFeatures)
    assert features.session == "LONDON"
    assert features.regime == "TRENDING"
    assert features.htf_bias == "BULLISH"
    assert features.trend_strength == 0.85
    assert features.volatility == "NORMAL"
    assert features.atr == 10.0  # high(110) - low(100) for the one candle in the LONDON session
    assert features.liquidity_distance == 15.0  # |105 - 120|


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

    assert compute_market_features(high_vol, None).volatility == "HIGH"
    assert compute_market_features(low_vol, None).volatility == "LOW"


def test_trend_strength_is_zero_when_not_trending():
    ranging = _empty_context(
        market_regime=MarketRegimeResult(
            regime=MarketRegime.RANGE, direction=RegimeDirection.NEUTRAL, confidence=50.0, reasons=[],
        ),
    )

    assert compute_market_features(ranging, None).trend_strength == 0.0


def test_missing_context_degrades_gracefully():
    """No session events, no liquidity zones, no htf_bias -- must not raise, must report UNKNOWN/None."""
    candles = [_candle(9)]
    context = _empty_context(candles=candles)  # no session_events, no liquidity_zones

    features = compute_market_features(context, htf_bias=None)

    assert features.session == "UNKNOWN"
    assert features.liquidity_distance is None
    assert features.htf_bias == "UNKNOWN"
    assert features.regime == "UNKNOWN"  # default market_regime in _empty_context()


def test_empty_data_produces_no_crash_and_none_fields():
    context = _empty_context()  # zero candles at all

    features = compute_market_features(context, htf_bias=None)

    assert features.atr is None
    assert features.liquidity_distance is None
    assert features.session == "UNKNOWN"
    assert isinstance(features, MarketFeatures)


def test_no_fake_volume_ever():
    """volume must always be None -- across every scenario, never a fabricated number."""
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
        features = compute_market_features(context, _htf(HTFBias.BULLISH))
        assert features.volume is None


def test_future_compatibility_field_shape_is_stable():
    """MarketFeatures is a plain, introspectable dataclass -- a future consumer can rely on its field set."""
    field_names = {f.name for f in dataclasses.fields(MarketFeatures)}
    assert field_names == {
        "atr", "volatility", "trend_strength", "session", "regime", "htf_bias", "liquidity_distance", "volume",
    }

    # Direct construction via keyword args (e.g. a future backtester replaying historical
    # features) must work without going through compute_market_features() at all.
    manual = MarketFeatures(
        atr=12.5, volatility="NORMAL", trend_strength=0.5, session="ASIA",
        regime="RANGE", htf_bias="NEUTRAL", liquidity_distance=3.2,
    )
    assert manual.volume is None  # default applies even without passing it explicitly


def test_never_raises_across_extreme_inputs():
    extreme_contexts = [
        _empty_context(),
        _empty_context(candles=[_candle(h) for h in range(24)]),
        _empty_context(liquidity_zones=(LiquidityZone(price=0.0, type=LiquidityType.SSL, start_index=0, end_index=0, strength=1),)),
    ]
    for context in extreme_contexts:
        for htf in (None, _htf(HTFBias.BULLISH), _htf(HTFBias.UNKNOWN)):
            result = compute_market_features(context, htf)
            assert isinstance(result, MarketFeatures)
