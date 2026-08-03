"""
Phase 60.7: Adaptive Intelligence Layer Foundation, TASK 2 --
ai_layer/knowledge_ai/learning_loop/trade_event_bridge.py tests. Real PaperTrade/SignalPerformance/
LearningRepository objects, no mocks -- same convention as every
other learning/ test.
"""

from ai_layer.knowledge_ai.learning_loop.trade_event_bridge import bridge_closed_trade, build_learning_record_from_trade
from trade_monitoring_layer.paper_trading.paper_trade import PaperTrade, close_paper_trade, open_paper_trade
from trade_monitoring_layer.paper_trading.trade_state import TradeState
from backtesting_layer.statistics.signal_performance import SignalPerformance
from context_layer.context_engine.context_orchestrator import ContextSnapshot
from context_layer.fundamental.fundamental_context import compute_fundamental_context, merge_fundamental_score
from context_layer.fundamental.fundamental_scoring import compute_fundamental_score
from context_layer.trend.htf_bias import HTFBias, HTFBiasResult
from context_layer.trend.market_regime import MarketRegime, MarketRegimeResult, RegimeDirection
from database_layer.journal_repository.learning_repository import LearningRepository


def _htf_bias(bias) -> HTFBiasResult:
    return HTFBiasResult(bias=bias, confidence=80.0, timeframes=["H4"], quality_score=1.0)


def _empty_context(regime=MarketRegime.UNKNOWN, **overrides) -> ContextSnapshot:
    base = dict(
        candles=(), structure=(), bos_events=(), choch_events=(),
        liquidity_zones=(), liquidity_sweeps=(), order_blocks=(), fair_value_gaps=(),
        amd_events=(), wyckoff_events=(), session_events=(),
        market_regime=MarketRegimeResult(regime=regime, direction=RegimeDirection.NEUTRAL, confidence=0.0, reasons=[]),
    )
    base.update(overrides)
    return ContextSnapshot(**base)


def _open_trade(direction="BUY", trade_id="t1", signal_id="s1") -> PaperTrade:
    trade = PaperTrade(
        trade_id=trade_id, signal_id=signal_id, symbol="XAUUSD", direction=direction,
        entry=2000.0, stop_loss=1990.0, take_profit=2020.0, status=TradeState.CREATED,
    )
    return open_paper_trade(trade).trade


def _closed_trade(result="SL", **kwargs) -> PaperTrade:
    trade = _open_trade(**kwargs)
    return close_paper_trade(trade, result).trade


def _performance(strategy_id="Liquidity Sweep", session="London", market_phase="DISTRIBUTION", r_multiple=-1.0):
    return SignalPerformance(
        performance_id="p1", signal_id="s1", strategy_id=strategy_id,
        session=session, market_phase=market_phase, r_multiple=r_multiple,
    )


def test_build_learning_record_returns_none_for_a_non_closed_trade():
    trade = _open_trade()

    record = build_learning_record_from_trade(trade)

    assert record is None


def test_build_learning_record_relays_trade_and_performance_fields():
    trade = _closed_trade(result="SL")
    performance = _performance()

    record = build_learning_record_from_trade(trade, performance=performance)

    assert record.trade_id == trade.trade_id
    assert record.signal_id == trade.signal_id
    assert record.strategy_name == "Liquidity Sweep"
    assert record.session == "London"
    assert record.market_phase == "DISTRIBUTION"
    assert record.result == "SL"
    assert record.r_multiple == -1.0


def test_loss_populates_failure_type_not_success_pattern():
    trade = _closed_trade(result="SL", direction="BUY")
    performance = _performance()

    record = build_learning_record_from_trade(trade, performance=performance, htf_bias=_htf_bias(HTFBias.BEARISH))

    assert record.failure_type is not None
    assert record.success_pattern is None


def test_win_populates_success_pattern_not_failure_type():
    trade = _closed_trade(result="TP", direction="BUY")
    performance = _performance(r_multiple=2.0)

    record = build_learning_record_from_trade(trade, performance=performance, htf_bias=_htf_bias(HTFBias.BULLISH))

    assert record.success_pattern is not None
    assert record.failure_type is None


def test_breakeven_populates_neither():
    trade = _closed_trade(result="BE")
    performance = _performance(r_multiple=0.0)

    record = build_learning_record_from_trade(trade, performance=performance)

    assert record.failure_type is None
    assert record.success_pattern is None


def test_never_raises_with_no_performance_supplied():
    trade = _closed_trade(result="TP")

    record = build_learning_record_from_trade(trade)  # must not raise

    assert record.trade_id == trade.trade_id
    assert record.strategy_name is None


def test_bridge_closed_trade_returns_none_for_a_non_closed_trade():
    trade = _open_trade()
    repo = LearningRepository()

    result = bridge_closed_trade(trade, repo)

    assert result is None
    assert repo.count() == 0


def test_bridge_closed_trade_persists_a_row():
    trade = _closed_trade(result="SL")
    performance = _performance()
    repo = LearningRepository()

    row = bridge_closed_trade(trade, repo, performance=performance)

    assert row is not None
    assert row.trade_id == trade.trade_id
    assert repo.count() == 1


def test_bridge_closed_trade_round_trips_through_get_recent():
    trade = _closed_trade(result="TP")
    performance = _performance(r_multiple=2.0)
    repo = LearningRepository()

    bridge_closed_trade(trade, repo, performance=performance)
    recent = repo.get_recent()

    assert len(recent) == 1
    assert recent[0].trade_id == trade.trade_id
    assert recent[0].result == "TP"


# --- Phase 60.7 TASK 3: Enhanced Learning Schema fields on the bridge ---

def test_htf_bias_is_relayed_as_a_plain_string():
    trade = _closed_trade(result="TP", direction="BUY")

    record = build_learning_record_from_trade(trade, htf_bias=_htf_bias(HTFBias.BULLISH))

    assert record.htf_bias == "BULLISH"


def test_volatility_state_relayed_only_for_volatility_regimes():
    trade = _closed_trade(result="TP")
    high_vol_context = _empty_context(regime=MarketRegime.HIGH_VOLATILITY)
    trending_context = _empty_context(regime=MarketRegime.TRENDING)

    high_vol_record = build_learning_record_from_trade(trade, context=high_vol_context)
    trending_record = build_learning_record_from_trade(trade, context=trending_context)

    assert high_vol_record.volatility_state == "HIGH_VOLATILITY"
    assert trending_record.volatility_state is None


def test_fundamental_bias_and_confidence_score_are_relayed():
    trade = _closed_trade(result="TP")
    score = compute_fundamental_score(dxy_bias="BULLISH", rates_bias="BULLISH")
    fundamental = merge_fundamental_score(compute_fundamental_context(), score)

    record = build_learning_record_from_trade(trade, fundamental=fundamental)

    assert record.fundamental_bias == fundamental.gold_bias
    assert record.confidence_score == fundamental.confidence


def test_engine_version_is_stamped_by_default():
    trade = _closed_trade(result="TP")

    record = build_learning_record_from_trade(trade)

    from ai_layer.knowledge_ai.learning_loop.models import LEARNING_ENGINE_VERSION
    assert record.engine_version == LEARNING_ENGINE_VERSION


def test_bridge_closed_trade_persists_the_new_phase_607_fields():
    trade = _closed_trade(result="TP", direction="BUY")
    context = _empty_context(regime=MarketRegime.LOW_VOLATILITY)
    repo = LearningRepository()

    bridge_closed_trade(trade, repo, context=context, htf_bias=_htf_bias(HTFBias.BULLISH))
    recent = repo.get_recent()

    assert recent[0].htf_bias == "BULLISH"
    assert recent[0].volatility_state == "LOW_VOLATILITY"
