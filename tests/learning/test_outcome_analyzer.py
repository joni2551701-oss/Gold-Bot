"""
Phase 60.6: Learning Loop Foundation, TASK 3 --
learning/outcome_analyzer.py tests. Real ContextSnapshot/PaperTrade/
HTFBiasResult/SignalPerformance objects, no mocks -- same convention
as tests/context/test_market_phase.py.
"""

from datetime import datetime, timezone

from context_layer.market_structure.bos import BosDirection, BosEvent
from context_layer.context_engine.context_orchestrator import ContextSnapshot
from context_layer.fair_value_gap.fvg import FairValueGap, FvgType
from context_layer.trend.htf_bias import HTFBias, HTFBiasResult
from context_layer.liquidity.liquidity import LiquiditySweepEvent, LiquidityType, LiquidityZone
from context_layer.trend.market_regime import MarketRegime, MarketRegimeResult, RegimeDirection
from context_layer.market_structure.market_structure import StructurePoint, StructureType, SwingPoint, SwingType
from context_layer.order_block.order_block import OrderBlock, OrderBlockType
from learning.outcome_analyzer import TradeAnalysis, analyze_trade_result
from trade_monitoring_layer.paper_trading.paper_trade import PaperTrade
from trade_monitoring_layer.paper_trading.trade_state import TradeState
from analytics.signal_performance import SignalPerformance

TS = datetime(2024, 1, 2, 9, 0, tzinfo=timezone.utc)


def _empty_context(**overrides) -> ContextSnapshot:
    base = dict(
        candles=(), structure=(), bos_events=(), choch_events=(),
        liquidity_zones=(), liquidity_sweeps=(), order_blocks=(), fair_value_gaps=(),
        amd_events=(), wyckoff_events=(), session_events=(),
        market_regime=MarketRegimeResult(regime=MarketRegime.UNKNOWN, direction=RegimeDirection.NEUTRAL, confidence=0.0, reasons=[]),
    )
    base.update(overrides)
    return ContextSnapshot(**base)


def _trade(direction="BUY", result="SL") -> PaperTrade:
    return PaperTrade(
        trade_id="t1", signal_id="s1", symbol="XAUUSD", direction=direction,
        entry=2000.0, stop_loss=1990.0, take_profit=2020.0,
        status=TradeState.CLOSED, result=result,
    )


def _htf_bias(bias) -> HTFBiasResult:
    return HTFBiasResult(bias=bias, confidence=80.0, timeframes=["H4"], quality_score=1.0)


def _bos_event() -> BosEvent:
    swing = SwingPoint(index=0, price=2000.0, timestamp=TS, type=SwingType.HIGH)
    structure = StructurePoint(swing=swing, structure=StructureType.HIGHER_HIGH)
    return BosEvent(index=1, timestamp=TS, direction=BosDirection.BULLISH, broken_structure=structure)


def _liquidity_sweep() -> LiquiditySweepEvent:
    zone = LiquidityZone(price=2000.0, type=LiquidityType.SSL, start_index=0, end_index=1, strength=2)
    return LiquiditySweepEvent(index=1, timestamp=TS, type=LiquidityType.SSL, sweep_price=1999.0, zone=zone)


def _order_block() -> OrderBlock:
    return OrderBlock(high=2001.0, low=1999.0, index=1, timestamp=TS, type=OrderBlockType.BULLISH, strength=2)


def _fvg() -> FairValueGap:
    return FairValueGap(top=2005.0, bottom=2002.0, index=2, timestamp=TS, type=FvgType.BULLISH)


def _performance(session=None) -> SignalPerformance:
    return SignalPerformance(performance_id="p1", signal_id="s1", session=session)


def test_analyze_trade_result_never_raises_on_bare_paper_trade():
    analysis = analyze_trade_result(_trade())

    assert isinstance(analysis, TradeAnalysis)
    assert analysis.trade_id == "t1"
    assert analysis.result == "SL"
    assert analysis.reasons == []
    assert analysis.lesson == "No specific lesson available."


def test_htf_alignment_reason_for_a_buy_against_bearish_bias():
    analysis = analyze_trade_result(_trade(direction="BUY", result="SL"), htf_bias=_htf_bias(HTFBias.BEARISH))

    assert "Against HTF bias" in analysis.reasons


def test_htf_alignment_reason_for_a_buy_with_bullish_bias():
    analysis = analyze_trade_result(_trade(direction="BUY", result="TP"), htf_bias=_htf_bias(HTFBias.BULLISH))

    assert "HTF bias aligned" in analysis.reasons


def test_neutral_htf_bias_produces_no_alignment_reason():
    analysis = analyze_trade_result(_trade(), htf_bias=_htf_bias(HTFBias.NEUTRAL))

    assert "Against HTF bias" not in analysis.reasons
    assert "HTF bias aligned" not in analysis.reasons


def test_loss_with_no_structural_break_or_sweep_reports_both():
    analysis = analyze_trade_result(_trade(result="SL"), context=_empty_context())

    assert "No confirmed structural break" in analysis.reasons
    assert "No liquidity sweep observed" in analysis.reasons


def test_loss_with_bos_and_sweep_present_reports_neither_missing_reason():
    context = _empty_context(bos_events=(_bos_event(),), liquidity_sweeps=(_liquidity_sweep(),))

    analysis = analyze_trade_result(_trade(result="SL"), context=context)

    assert "No confirmed structural break" not in analysis.reasons
    assert "No liquidity sweep observed" not in analysis.reasons


def test_win_with_ob_and_fvg_present_reports_both():
    context = _empty_context(order_blocks=(_order_block(),), fair_value_gaps=(_fvg(),))

    analysis = analyze_trade_result(_trade(result="TP"), context=context)

    assert "OB reaction present" in analysis.reasons
    assert "FVG fill" in analysis.reasons


def test_matches_the_directors_own_worked_example_lesson():
    """A loss, against HTF bias, no confirmed structural break, known session -> 'Avoid {session} reversal without BOS'."""
    analysis = analyze_trade_result(
        _trade(direction="SELL", result="SL"),
        context=_empty_context(),
        performance=_performance(session="London"),
        htf_bias=_htf_bias(HTFBias.BULLISH),
    )

    assert analysis.lesson == "Avoid London reversal without BOS"


def test_loss_without_the_full_pattern_gets_a_generic_review_lesson():
    analysis = analyze_trade_result(_trade(result="SL"), context=_empty_context())

    assert analysis.lesson.startswith("Review:")


def test_win_with_reasons_gets_a_generic_repeat_lesson():
    context = _empty_context(order_blocks=(_order_block(),))

    analysis = analyze_trade_result(_trade(result="TP"), context=context)

    assert analysis.lesson.startswith("Repeat:")


def test_breakeven_trade_produces_no_win_or_loss_structural_reasons():
    context = _empty_context(order_blocks=(_order_block(),))

    analysis = analyze_trade_result(_trade(result="BE"), context=context)

    assert analysis.reasons == []
    assert analysis.lesson == "No specific lesson available."
