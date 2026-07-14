"""
Phase A7 -- Market Regime Engine foundation tests (context/market_regime.py).

No mocking -- real StructurePoint/WyckoffEvent/HTFBiasResult/Candle
objects, same convention as tests/context/test_htf_bias.py,
tests/context/test_wyckoff.py, and tests/context/test_session.py.
"""

from datetime import datetime, timezone

from context.market_regime import (
    compute_market_regime,
    MarketRegime,
    RegimeDirection,
    TRENDING_CONFIRMED_CONFIDENCE,
    TRENDING_UNCONFIRMED_CONFIDENCE,
    WYCKOFF_REGIME_CONFIDENCE,
    RANGE_CONFIDENCE,
    UNKNOWN_CONFIDENCE,
)
from context.market_structure import SwingPoint, SwingType, StructurePoint, StructureType
from context.wyckoff import WyckoffEvent, WyckoffEventType, WyckoffPhase
from context.liquidity import LiquidityZone, LiquiditySweepEvent, LiquidityType
from context.htf_bias import HTFBias, HTFBiasResult
from context.context_orchestrator import build_context_snapshot
from data.twelve_data_client import Candle

TS = datetime(2024, 1, 1, tzinfo=timezone.utc)


def _bullish_structure():
    low = SwingPoint(index=0, price=100.0, timestamp=TS, type=SwingType.LOW)
    high = SwingPoint(index=1, price=110.0, timestamp=TS, type=SwingType.HIGH)
    return (
        StructurePoint(swing=low, structure=StructureType.HIGHER_LOW),
        StructurePoint(swing=high, structure=StructureType.HIGHER_HIGH),
    )


def _bearish_structure():
    high = SwingPoint(index=0, price=110.0, timestamp=TS, type=SwingType.HIGH)
    low = SwingPoint(index=1, price=100.0, timestamp=TS, type=SwingType.LOW)
    return (
        StructurePoint(swing=high, structure=StructureType.LOWER_HIGH),
        StructurePoint(swing=low, structure=StructureType.LOWER_LOW),
    )


def _htf(bias):
    return HTFBiasResult(bias=bias, confidence=100.0, timeframes=("Daily", "H4", "H1"), quality_score=1.0)


def _spring_event():
    zone = LiquidityZone(price=99.0, type=LiquidityType.SSL, start_index=0, end_index=1, strength=2)
    sweep = LiquiditySweepEvent(index=2, timestamp=TS, type=LiquidityType.SSL, sweep_price=98.5, zone=zone)
    return WyckoffEvent(
        type=WyckoffEventType.SPRING, phase=WyckoffPhase.ACCUMULATION, index=5, timestamp=TS,
        sweep=sweep, confirming_break_index=5, volume_confirmed=None,
    )


def _upthrust_event():
    zone = LiquidityZone(price=111.0, type=LiquidityType.BSL, start_index=0, end_index=1, strength=2)
    sweep = LiquiditySweepEvent(index=2, timestamp=TS, type=LiquidityType.BSL, sweep_price=111.5, zone=zone)
    return WyckoffEvent(
        type=WyckoffEventType.UPTHRUST, phase=WyckoffPhase.DISTRIBUTION, index=5, timestamp=TS,
        sweep=sweep, confirming_break_index=5, volume_confirmed=None,
    )


def _candle(hour, high=101.0, low=99.0):
    return Candle(timestamp=datetime(2024, 1, 2, hour, tzinfo=timezone.utc), open=100.0, high=high, low=low, close=100.0)


def test_bullish_trend_confirmed_by_htf():
    result = compute_market_regime(candles=[], structure=_bullish_structure(), wyckoff_events=[], htf_bias=_htf(HTFBias.BULLISH))

    assert result.regime == MarketRegime.TRENDING
    assert result.direction == RegimeDirection.BULLISH
    assert result.confidence == TRENDING_CONFIRMED_CONFIDENCE
    assert "HTF bullish bias" in result.reasons
    assert "HH/HL structure" in result.reasons


def test_bearish_trend_confirmed_by_htf():
    result = compute_market_regime(candles=[], structure=_bearish_structure(), wyckoff_events=[], htf_bias=_htf(HTFBias.BEARISH))

    assert result.regime == MarketRegime.TRENDING
    assert result.direction == RegimeDirection.BEARISH
    assert result.confidence == TRENDING_CONFIRMED_CONFIDENCE


def test_trend_unconfirmed_without_htf_bias():
    result = compute_market_regime(candles=[], structure=_bullish_structure(), wyckoff_events=[], htf_bias=None)

    assert result.regime == MarketRegime.TRENDING
    assert result.direction == RegimeDirection.BULLISH
    assert result.confidence == TRENDING_UNCONFIRMED_CONFIDENCE
    assert result.confidence < TRENDING_CONFIRMED_CONFIDENCE


def test_conflicting_structure_and_htf_produces_range():
    result = compute_market_regime(candles=[], structure=_bullish_structure(), wyckoff_events=[], htf_bias=_htf(HTFBias.BEARISH))

    assert result.regime == MarketRegime.RANGE
    assert result.direction == RegimeDirection.NEUTRAL
    assert "conflicting" in result.reasons[0].lower()


def test_conflicting_bearish_structure_and_bullish_htf_also_produces_range():
    """Mirror of the bullish-vs-bearish conflict -- both directions of disagreement must resolve to RANGE."""
    result = compute_market_regime(candles=[], structure=_bearish_structure(), wyckoff_events=[], htf_bias=_htf(HTFBias.BULLISH))

    assert result.regime == MarketRegime.RANGE
    assert result.direction == RegimeDirection.NEUTRAL
    assert "conflicting" in result.reasons[0].lower()


def test_accumulation_from_spring_event():
    result = compute_market_regime(candles=[], structure=[], wyckoff_events=[_spring_event()], htf_bias=None)

    assert result.regime == MarketRegime.ACCUMULATION
    assert result.direction == RegimeDirection.BULLISH
    assert result.confidence == WYCKOFF_REGIME_CONFIDENCE


def test_distribution_from_upthrust_event():
    result = compute_market_regime(candles=[], structure=[], wyckoff_events=[_upthrust_event()], htf_bias=None)

    assert result.regime == MarketRegime.DISTRIBUTION
    assert result.direction == RegimeDirection.BEARISH
    assert result.confidence == WYCKOFF_REGIME_CONFIDENCE


def test_wyckoff_takes_priority_over_trend():
    """A recent Spring wins over an also-present bullish structure/HTF trend -- regime is a single label."""
    result = compute_market_regime(
        candles=[], structure=_bullish_structure(), wyckoff_events=[_spring_event()], htf_bias=_htf(HTFBias.BULLISH),
    )

    assert result.regime == MarketRegime.ACCUMULATION


def test_high_volatility_from_session_range_ratio():
    """One candle with a huge range dominates the window average -- current session should read as HIGH_VOLATILITY."""
    candles = [_candle(1, high=100.5, low=99.5), _candle(2, high=100.5, low=99.5), _candle(9, high=130.0, low=70.0)]

    result = compute_market_regime(candles=candles, structure=[], wyckoff_events=[], htf_bias=None)

    assert result.regime == MarketRegime.HIGH_VOLATILITY
    assert result.direction == RegimeDirection.NEUTRAL


def test_low_volatility_from_session_range_ratio():
    """The most recent candle has a tiny range relative to the window average -- current session should read as LOW_VOLATILITY."""
    candles = [_candle(1, high=130.0, low=70.0), _candle(2, high=130.0, low=70.0), _candle(9, high=100.1, low=99.9)]

    result = compute_market_regime(candles=candles, structure=[], wyckoff_events=[], htf_bias=None)

    assert result.regime == MarketRegime.LOW_VOLATILITY


def test_range_when_no_trend_wyckoff_or_volatility_extreme():
    candles = [_candle(1), _candle(2), _candle(3)]  # uniform ranges -- ratio == 1.0, no extreme

    result = compute_market_regime(candles=candles, structure=[], wyckoff_events=[], htf_bias=None)

    assert result.regime == MarketRegime.RANGE
    assert result.confidence == RANGE_CONFIDENCE


def test_unknown_when_no_data_at_all():
    result = compute_market_regime(candles=[], structure=[], wyckoff_events=[], htf_bias=None)

    assert result.regime == MarketRegime.UNKNOWN
    assert result.direction == RegimeDirection.NEUTRAL
    assert result.confidence == UNKNOWN_CONFIDENCE


def test_malformed_input_never_raises():
    """Empty/missing everything simultaneously -- must degrade to UNKNOWN, never crash."""
    result = compute_market_regime(candles=[], structure=[], wyckoff_events=[], htf_bias=None)
    assert result.regime == MarketRegime.UNKNOWN

    # Also confirm a mismatched-but-well-typed combination (structure present, but
    # completely unclassifiable -- all UNKNOWN structure points) never raises.
    only_unknown = (StructurePoint(swing=SwingPoint(0, 100.0, TS, SwingType.HIGH), structure=StructureType.UNKNOWN),)
    result2 = compute_market_regime(candles=[], structure=only_unknown, wyckoff_events=[], htf_bias=None)
    assert result2.regime == MarketRegime.UNKNOWN


def test_confidence_always_within_0_and_100():
    scenarios = [
        compute_market_regime([], _bullish_structure(), [], _htf(HTFBias.BULLISH)),
        compute_market_regime([], _bearish_structure(), [], None),
        compute_market_regime([], [], [_spring_event()], None),
        compute_market_regime([], [], [_upthrust_event()], None),
        compute_market_regime([_candle(1), _candle(9, high=150.0, low=50.0)], [], [], None),
        compute_market_regime([], [], [], None),
    ]
    for result in scenarios:
        assert 0.0 <= result.confidence <= 100.0


def test_market_regime_is_wired_through_context_orchestrator():
    """Confirms build_context_snapshot() populates ContextSnapshot.market_regime and forwards htf_bias to it."""
    candles = [_candle(1), _candle(2)]

    snapshot_no_htf = build_context_snapshot(candles)
    assert hasattr(snapshot_no_htf, "market_regime")
    assert snapshot_no_htf.market_regime.regime in set(MarketRegime)

    snapshot_with_htf = build_context_snapshot(candles, _htf(HTFBias.BULLISH))
    assert snapshot_with_htf.market_regime.regime in set(MarketRegime)
