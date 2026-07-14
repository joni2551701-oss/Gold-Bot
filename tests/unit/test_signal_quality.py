"""
Phase A4 -- Signal Quality Score unit tests (signals/signal_quality.py).

Builds minimal, real ContextSnapshot/HTFBiasResult objects directly
(no mocking) to control exactly which of the 5 criteria are met, and
verifies the resulting grade/score/criteria_met against real code --
same no-mocking convention as tests/unit/test_decision_engine.py and
tests/unit/test_risk_manager.py.
"""

from datetime import datetime, timezone

from signals.signal_quality import compute_signal_quality, QualityGrade
from signals.models import SignalType
from context.context_orchestrator import ContextSnapshot
from context.market_structure import SwingPoint, SwingType, StructurePoint, StructureType
from context.liquidity import LiquidityZone, LiquiditySweepEvent, LiquidityType
from context.order_block import OrderBlock, OrderBlockType
from context.fvg import FairValueGap, FvgType
from context.htf_bias import HTFBias, HTFBiasResult


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
    )
    base.update(overrides)
    return ContextSnapshot(**base)


def _bullish_structure():
    swing_low = SwingPoint(index=0, price=100.0, timestamp=TS, type=SwingType.LOW)
    swing_high = SwingPoint(index=1, price=110.0, timestamp=TS, type=SwingType.HIGH)
    return (
        StructurePoint(swing=swing_low, structure=StructureType.HIGHER_LOW),
        StructurePoint(swing=swing_high, structure=StructureType.HIGHER_HIGH),
    )


def _bearish_structure():
    swing_high = SwingPoint(index=0, price=110.0, timestamp=TS, type=SwingType.HIGH)
    swing_low = SwingPoint(index=1, price=100.0, timestamp=TS, type=SwingType.LOW)
    return (
        StructurePoint(swing=swing_high, structure=StructureType.LOWER_HIGH),
        StructurePoint(swing=swing_low, structure=StructureType.LOWER_LOW),
    )


def _ssl_sweep():
    zone = LiquidityZone(price=99.0, type=LiquidityType.SSL, start_index=0, end_index=1, strength=2)
    return LiquiditySweepEvent(index=2, timestamp=TS, type=LiquidityType.SSL, sweep_price=98.5, zone=zone)


def _bsl_sweep():
    zone = LiquidityZone(price=111.0, type=LiquidityType.BSL, start_index=0, end_index=1, strength=2)
    return LiquiditySweepEvent(index=2, timestamp=TS, type=LiquidityType.BSL, sweep_price=111.5, zone=zone)


def _bullish_ob(entry: float):
    return OrderBlock(high=entry + 1.0, low=entry - 1.0, index=3, timestamp=TS, type=OrderBlockType.BULLISH, strength=1)


def _bearish_ob(entry: float):
    return OrderBlock(high=entry + 1.0, low=entry - 1.0, index=3, timestamp=TS, type=OrderBlockType.BEARISH, strength=1)


def _bullish_fvg(entry: float):
    return FairValueGap(top=entry + 1.0, bottom=entry - 1.0, index=4, timestamp=TS, type=FvgType.BULLISH)


def _bearish_fvg(entry: float):
    return FairValueGap(top=entry + 1.0, bottom=entry - 1.0, index=4, timestamp=TS, type=FvgType.BEARISH)


def _htf(bias):
    return HTFBiasResult(bias=bias, confidence=100.0, timeframes=("Daily", "H4", "H1"), quality_score=1.0)


def test_all_five_criteria_met_grades_a_plus(mock_signal_candidate):
    entry = 105.0
    signal = mock_signal_candidate(signal_type=SignalType.BUY, entry=entry, stop_loss=100.0, take_profit=120.0)
    context = _empty_context(
        structure=_bullish_structure(),
        liquidity_sweeps=(_ssl_sweep(),),
        order_blocks=(_bullish_ob(entry),),
        fair_value_gaps=(_bullish_fvg(entry),),
    )

    result = compute_signal_quality(signal, context, _htf(HTFBias.BULLISH))

    assert result.grade == QualityGrade.A_PLUS
    assert result.score == 100.0
    assert result.criteria_total == 5
    assert set(result.criteria_met) == {
        "HTF_ALIGNED", "STRUCTURE_ALIGNED", "LIQUIDITY_SWEPT", "ORDER_BLOCK_ALIGNED", "FVG_ALIGNED",
    }


def test_zero_criteria_met_grades_c(mock_signal_candidate):
    signal = mock_signal_candidate(signal_type=SignalType.BUY, entry=105.0)
    context = _empty_context()  # no structure, no liquidity, no OB, no FVG

    result = compute_signal_quality(signal, context, htf_bias=None)

    assert result.grade == QualityGrade.C
    assert result.score == 0.0
    assert result.criteria_met == ()


def test_three_criteria_met_grades_a(mock_signal_candidate):
    entry = 105.0
    signal = mock_signal_candidate(signal_type=SignalType.BUY, entry=entry)
    context = _empty_context(
        structure=_bullish_structure(),
        liquidity_sweeps=(_ssl_sweep(),),
        order_blocks=(_bullish_ob(entry),),
    )

    result = compute_signal_quality(signal, context, htf_bias=None)  # HTF and FVG both unmet

    assert result.grade == QualityGrade.A
    assert result.score == 60.0
    assert len(result.criteria_met) == 3


def test_two_criteria_met_grades_b(mock_signal_candidate):
    entry = 105.0
    signal = mock_signal_candidate(signal_type=SignalType.BUY, entry=entry)
    context = _empty_context(structure=_bullish_structure(), liquidity_sweeps=(_ssl_sweep(),))

    result = compute_signal_quality(signal, context, htf_bias=None)

    assert result.grade == QualityGrade.B
    assert result.score == 40.0


def test_one_criterion_met_grades_c(mock_signal_candidate):
    entry = 105.0
    signal = mock_signal_candidate(signal_type=SignalType.BUY, entry=entry)
    context = _empty_context(liquidity_sweeps=(_ssl_sweep(),))

    result = compute_signal_quality(signal, context, htf_bias=None)

    assert result.grade == QualityGrade.C
    assert result.score == 20.0


def test_htf_alignment_is_direction_specific(mock_signal_candidate):
    buy = mock_signal_candidate(signal_type=SignalType.BUY, entry=105.0)
    sell = mock_signal_candidate(signal_type=SignalType.SELL, entry=105.0)
    context = _empty_context()

    assert "HTF_ALIGNED" in compute_signal_quality(buy, context, _htf(HTFBias.BULLISH)).criteria_met
    assert "HTF_ALIGNED" not in compute_signal_quality(buy, context, _htf(HTFBias.BEARISH)).criteria_met
    assert "HTF_ALIGNED" in compute_signal_quality(sell, context, _htf(HTFBias.BEARISH)).criteria_met
    assert "HTF_ALIGNED" not in compute_signal_quality(sell, context, _htf(HTFBias.BULLISH)).criteria_met
    assert "HTF_ALIGNED" not in compute_signal_quality(buy, context, None).criteria_met
    assert "HTF_ALIGNED" not in compute_signal_quality(buy, context, _htf(HTFBias.NEUTRAL)).criteria_met


def test_structure_alignment_is_direction_specific(mock_signal_candidate):
    buy = mock_signal_candidate(signal_type=SignalType.BUY, entry=105.0)
    sell = mock_signal_candidate(signal_type=SignalType.SELL, entry=105.0)

    bullish_ctx = _empty_context(structure=_bullish_structure())
    bearish_ctx = _empty_context(structure=_bearish_structure())

    assert "STRUCTURE_ALIGNED" in compute_signal_quality(buy, bullish_ctx, None).criteria_met
    assert "STRUCTURE_ALIGNED" not in compute_signal_quality(buy, bearish_ctx, None).criteria_met
    assert "STRUCTURE_ALIGNED" in compute_signal_quality(sell, bearish_ctx, None).criteria_met
    assert "STRUCTURE_ALIGNED" not in compute_signal_quality(sell, bullish_ctx, None).criteria_met


def test_liquidity_sweep_is_direction_specific(mock_signal_candidate):
    buy = mock_signal_candidate(signal_type=SignalType.BUY, entry=105.0)
    sell = mock_signal_candidate(signal_type=SignalType.SELL, entry=105.0)

    ssl_ctx = _empty_context(liquidity_sweeps=(_ssl_sweep(),))
    bsl_ctx = _empty_context(liquidity_sweeps=(_bsl_sweep(),))

    assert "LIQUIDITY_SWEPT" in compute_signal_quality(buy, ssl_ctx, None).criteria_met
    assert "LIQUIDITY_SWEPT" not in compute_signal_quality(buy, bsl_ctx, None).criteria_met
    assert "LIQUIDITY_SWEPT" in compute_signal_quality(sell, bsl_ctx, None).criteria_met
    assert "LIQUIDITY_SWEPT" not in compute_signal_quality(sell, ssl_ctx, None).criteria_met


def test_order_block_requires_matching_type_and_price_zone(mock_signal_candidate):
    entry = 105.0
    buy = mock_signal_candidate(signal_type=SignalType.BUY, entry=entry)

    inside_bullish = _empty_context(order_blocks=(_bullish_ob(entry),))
    inside_bearish = _empty_context(order_blocks=(_bearish_ob(entry),))
    outside_zone = _empty_context(order_blocks=(_bullish_ob(entry + 1000.0),))

    assert "ORDER_BLOCK_ALIGNED" in compute_signal_quality(buy, inside_bullish, None).criteria_met
    assert "ORDER_BLOCK_ALIGNED" not in compute_signal_quality(buy, inside_bearish, None).criteria_met
    assert "ORDER_BLOCK_ALIGNED" not in compute_signal_quality(buy, outside_zone, None).criteria_met


def test_fvg_requires_matching_type_and_price_zone(mock_signal_candidate):
    entry = 105.0
    sell = mock_signal_candidate(signal_type=SignalType.SELL, entry=entry)

    inside_bearish = _empty_context(fair_value_gaps=(_bearish_fvg(entry),))
    inside_bullish = _empty_context(fair_value_gaps=(_bullish_fvg(entry),))
    outside_zone = _empty_context(fair_value_gaps=(_bearish_fvg(entry + 1000.0),))

    assert "FVG_ALIGNED" in compute_signal_quality(sell, inside_bearish, None).criteria_met
    assert "FVG_ALIGNED" not in compute_signal_quality(sell, inside_bullish, None).criteria_met
    assert "FVG_ALIGNED" not in compute_signal_quality(sell, outside_zone, None).criteria_met


def test_never_raises_with_signal_type_none(mock_signal_candidate):
    none_signal = mock_signal_candidate(signal_type=SignalType.NONE, entry=105.0)
    context = _empty_context(
        structure=_bullish_structure(),
        liquidity_sweeps=(_ssl_sweep(),),
        order_blocks=(_bullish_ob(105.0),),
        fair_value_gaps=(_bullish_fvg(105.0),),
    )

    result = compute_signal_quality(none_signal, context, _htf(HTFBias.BULLISH))

    assert result.grade == QualityGrade.C
    assert result.score == 0.0


def test_score_and_criteria_total_stay_consistent(mock_signal_candidate):
    signal = mock_signal_candidate(signal_type=SignalType.BUY, entry=105.0)
    context = _empty_context(structure=_bullish_structure())

    result = compute_signal_quality(signal, context, None)

    assert result.criteria_total == 5
    assert result.score == round(len(result.criteria_met) / result.criteria_total * 100, 2)
    assert 0.0 <= result.score <= 100.0
