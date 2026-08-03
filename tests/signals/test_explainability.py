"""
Phase A9 -- Explainability Layer foundation tests (signal_layer/signal_scoring/explainability.py).

No mocking -- real ContextSnapshot/SignalQualityResult/WyckoffEvent/
SessionEvent/MarketRegimeResult objects, same convention as
tests/unit/test_signal_quality.py and tests/context/test_market_regime.py.
"""

from datetime import datetime, timezone

from signal_layer.signal_scoring.explainability import explain_signal, SignalExplanation
from signal_layer.signal_scoring.signal_quality import SignalQualityResult, QualityGrade
from context_layer.context_engine.context_orchestrator import ContextSnapshot
from context_layer.wyckoff.wyckoff import WyckoffEvent, WyckoffEventType, WyckoffPhase
from context_layer.liquidity.liquidity import LiquidityZone, LiquiditySweepEvent, LiquidityType
from context_layer.session.session import Session, SessionEvent
from context_layer.trend.market_regime import MarketRegimeResult, MarketRegime, RegimeDirection
from signal_layer.signal_builder.models import SignalType

TS = datetime(2024, 1, 1, tzinfo=timezone.utc)


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


def _quality(grade=QualityGrade.A_PLUS, criteria_met=(), score=100.0):
    return SignalQualityResult(grade=grade, score=score, criteria_met=criteria_met, criteria_total=5)


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


def _trending(direction):
    return MarketRegimeResult(regime=MarketRegime.TRENDING, direction=direction, confidence=85.0, reasons=[])


def test_bullish_explanation_includes_all_supporting_reasons(mock_signal_candidate):
    signal = mock_signal_candidate(signal_type=SignalType.BUY, confidence=0.85)
    quality = _quality(
        grade=QualityGrade.A_PLUS,
        criteria_met=("HTF_ALIGNED", "STRUCTURE_ALIGNED", "LIQUIDITY_SWEPT", "FVG_ALIGNED"),
    )
    context = _empty_context(
        wyckoff_events=(_spring_event(),),
        session_events=(SessionEvent(index=0, timestamp=TS, session=Session.LONDON),),
        market_regime=_trending(RegimeDirection.BULLISH),
    )

    explanation = explain_signal(signal, context, quality)

    assert explanation.direction == "BUY"
    assert explanation.quality == "A+"
    assert explanation.confidence == 85.0
    assert "HTF bullish bias" in explanation.reasons
    assert "HH/HL structure" in explanation.reasons
    assert "Liquidity sweep detected" in explanation.reasons
    assert "FVG reaction" in explanation.reasons
    assert "Wyckoff Spring (Accumulation)" in explanation.reasons
    assert "London session" in explanation.reasons
    assert "Market regime: TRENDING (BULLISH)" in explanation.reasons


def test_bearish_explanation_uses_bearish_phrasing(mock_signal_candidate):
    signal = mock_signal_candidate(signal_type=SignalType.SELL, confidence=0.72)
    quality = _quality(grade=QualityGrade.A, criteria_met=("HTF_ALIGNED", "STRUCTURE_ALIGNED"))
    context = _empty_context(
        wyckoff_events=(_upthrust_event(),),
        session_events=(SessionEvent(index=0, timestamp=TS, session=Session.NEW_YORK),),
        market_regime=_trending(RegimeDirection.BEARISH),
    )

    explanation = explain_signal(signal, context, quality)

    assert explanation.direction == "SELL"
    assert explanation.quality == "A"
    assert explanation.confidence == 72.0
    assert "HTF bearish bias" in explanation.reasons
    assert "LH/LL structure" in explanation.reasons
    assert "Wyckoff Upthrust (Distribution)" in explanation.reasons
    assert "New York session" in explanation.reasons
    assert "Market regime: TRENDING (BEARISH)" in explanation.reasons


def test_opposite_direction_wyckoff_and_regime_are_excluded(mock_signal_candidate):
    """A BUY signal must not claim a bearish Upthrust or a bearish TRENDING regime as supporting reasons."""
    signal = mock_signal_candidate(signal_type=SignalType.BUY, confidence=0.6)
    quality = _quality(criteria_met=())
    context = _empty_context(
        wyckoff_events=(_upthrust_event(),),  # bearish -- must not support a BUY
        market_regime=_trending(RegimeDirection.BEARISH),  # must not support a BUY
    )

    explanation = explain_signal(signal, context, quality)

    assert not any("Upthrust" in r for r in explanation.reasons)
    assert not any("Market regime" in r for r in explanation.reasons)


def test_missing_context_degrades_gracefully(mock_signal_candidate):
    """No wyckoff/session events, UNKNOWN market_regime -- must not raise, must simply omit those reasons."""
    signal = mock_signal_candidate(signal_type=SignalType.BUY, confidence=0.5)
    quality = _quality(criteria_met=("HTF_ALIGNED",))
    context = _empty_context()  # no wyckoff, no session, market_regime=UNKNOWN

    explanation = explain_signal(signal, context, quality)

    assert explanation.reasons == ("HTF bullish bias",)


def test_empty_reasons_when_nothing_supports_the_signal(mock_signal_candidate):
    signal = mock_signal_candidate(signal_type=SignalType.BUY, confidence=0.3)
    quality = _quality(criteria_met=())
    context = _empty_context()

    explanation = explain_signal(signal, context, quality)

    assert explanation.reasons == ()
    assert isinstance(explanation, SignalExplanation)


def test_quality_integration_reflects_grade(mock_signal_candidate):
    signal = mock_signal_candidate(signal_type=SignalType.BUY, confidence=0.5)
    context = _empty_context()

    for grade in (QualityGrade.A_PLUS, QualityGrade.A, QualityGrade.B, QualityGrade.C):
        explanation = explain_signal(signal, context, _quality(grade=grade))
        assert explanation.quality == grade.value


def test_confidence_is_relayed_not_recomputed(mock_signal_candidate):
    """Confidence must be exactly signal.confidence * 100 -- never derived from quality.score or anything else."""
    signal = mock_signal_candidate(signal_type=SignalType.BUY, confidence=0.9137)
    quality = _quality(score=10.0)  # deliberately mismatched from signal.confidence
    context = _empty_context()

    explanation = explain_signal(signal, context, quality)

    assert explanation.confidence == 91.37


def test_never_raises_with_signal_type_none(mock_signal_candidate):
    signal = mock_signal_candidate(signal_type=SignalType.NONE, confidence=0.0)
    context = _empty_context(wyckoff_events=(_spring_event(),), market_regime=_trending(RegimeDirection.BULLISH))

    explanation = explain_signal(signal, context, _quality(criteria_met=()))

    assert explanation.direction == "NONE"
