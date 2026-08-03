"""
Learning Layer — Trade Event Bridge (Phase 60.7: Adaptive
Intelligence Layer Foundation, TASK 2).

The one missing connection Phase 60.6's own docs disclosed ("no
observation point yet calls LearningRepository.record()"): bridges an
already-CLOSED `trade_monitoring_layer.paper_trading.paper_trade.PaperTrade` into a persisted
`learning.models.LearningRecord`, via
`learning.outcome_analyzer.analyze_trade_result()` (reused directly,
not reimplemented) for the `failure_type`/`success_pattern` text.

TASK 1's audit (`docs/ADAPTIVE_INTELLIGENCE_AUDIT.md`) found the only
real CLOSED `PaperTrade` producer in this codebase today is
`backtesting_layer/backtest_engine/backtest_engine.py` — a genuine Phase 60.2 bug (the
engine never actually captured a trade's CLOSED transition) was found
and fixed there as part of that same audit, since without that fix
this bridge would have had nothing but permanently-`CREATED` trades to
observe.

The one disclosed exception to this package's own "does not persist
anything itself" rule (see `learning/README.md`):
`bridge_closed_trade()` accepts an already-constructed
`database_layer.journal_repository.learning_repository.LearningRepository` and calls its
`record()` method — the same dependency-injection posture
`telegram/*_service.py` already uses for its own repository calls, not
a new "`learning/` always imports `database/`" precedent (every other
file in this package still imports nothing from `database/`).

Per this whole phase's hard boundary: this bridge only OBSERVES an
already-closed trade and RECORDS what happened — it never calls
`strategies/`, `decision/`, or `risk/`, and nothing about a trade's own
result/lifecycle is altered by bridging it. Still not wired into
`core/pipeline.py` or `backtesting_layer/backtest_engine/backtest_engine.py` — a caller must
invoke this explicitly.
"""

from typing import Optional, TYPE_CHECKING

from context_layer.trend.market_regime import MarketRegime
from trade_monitoring_layer.paper_trading.trade_state import TradeState
from learning.models import LearningRecord, create_learning_record
from learning.outcome_analyzer import analyze_trade_result

if TYPE_CHECKING:
    from context_layer.context_engine.context_orchestrator import ContextSnapshot
    from context_layer.fundamental.fundamental_context import FundamentalContextSnapshot
    from context_layer.trend.htf_bias import HTFBiasResult
    from analytics.signal_performance import SignalPerformance
    from trade_monitoring_layer.paper_trading.paper_trade import PaperTrade
    from database_layer.journal_repository.learning_repository import LearningRepository
    from database_layer.journal_repository.learning_models import LearningRecordRow

_VOLATILITY_REGIMES = (MarketRegime.HIGH_VOLATILITY, MarketRegime.LOW_VOLATILITY)


def _volatility_state(context: Optional['ContextSnapshot']) -> Optional[str]:
    """
    Relays `context.market_regime.regime.value` ONLY when it is one of
    the two volatility-shaped regimes -- every other regime
    (TRENDING/RANGE/etc.) says nothing about volatility specifically,
    so this stays None rather than reporting a misleading label. See
    `learning.models.LearningRecord.volatility_state`'s own docstring.
    """
    if context is None:
        return None
    if context.market_regime.regime in _VOLATILITY_REGIMES:
        return context.market_regime.regime.value
    return None


def build_learning_record_from_trade(
    paper_trade: 'PaperTrade',
    context: Optional['ContextSnapshot'] = None,
    performance: Optional['SignalPerformance'] = None,
    htf_bias: Optional['HTFBiasResult'] = None,
    fundamental: Optional['FundamentalContextSnapshot'] = None,
) -> Optional[LearningRecord]:
    """
    None (not an exception) when `paper_trade.status` is not `CLOSED`
    — same "nothing to report yet" posture every
    `PaperTradeTransitionResult` producer already uses. Reuses
    `analyze_trade_result()` directly for `reasons`/`lesson`;
    `failure_type`/`success_pattern` are the joined `reasons` list
    (`" + "`-separated, matching `learning.pattern_detector`'s own
    condition-formatting convention), attributed to whichever side the
    trade actually resolved to (`"SL"` -> `failure_type`, `"TP"` ->
    `success_pattern`; `"BE"`/`"EXPIRED"`/`"CANCELLED"` get neither,
    since `analyze_trade_result()` itself only classifies win/loss
    structural reasons).

    `htf_bias`/`volatility_state`/`fundamental_bias`/`confidence_score`
    (Phase 60.7, TASK 3) are all relayed from the supplied `htf_bias`/
    `context`/`fundamental` inputs -- never recomputed here.
    `confidence_score` relays `fundamental.confidence` (the
    `context.fundamental_scoring.FundamentalScoreResult` confidence
    that was merged into it, if any) when `fundamental` is supplied,
    since that is the one confidence value already available at this
    call site; a caller wanting a different confidence source builds
    its own `LearningRecord` directly. `sample_size` stays the honest
    `None` default -- see `LearningRecord`'s own docstring.
    """
    if paper_trade.status != TradeState.CLOSED:
        return None

    analysis = analyze_trade_result(paper_trade, context=context, performance=performance, htf_bias=htf_bias)
    reason_text = " + ".join(analysis.reasons) if analysis.reasons else None

    return create_learning_record(
        trade_id=paper_trade.trade_id,
        signal_id=paper_trade.signal_id,
        strategy_name=performance.strategy_id if performance is not None else None,
        market_phase=performance.market_phase if performance is not None else None,
        session=performance.session if performance is not None else None,
        timeframe=performance.timeframe if performance is not None else None,
        result=paper_trade.result,
        r_multiple=performance.r_multiple if performance is not None else None,
        failure_type=reason_text if analysis.result == "SL" else None,
        success_pattern=reason_text if analysis.result == "TP" else None,
        htf_bias=htf_bias.bias.value if htf_bias is not None else None,
        volatility_state=_volatility_state(context),
        fundamental_bias=fundamental.gold_bias if fundamental is not None else None,
        confidence_score=fundamental.confidence if fundamental is not None else None,
    )


def bridge_closed_trade(
    paper_trade: 'PaperTrade',
    repository: 'LearningRepository',
    context: Optional['ContextSnapshot'] = None,
    performance: Optional['SignalPerformance'] = None,
    htf_bias: Optional['HTFBiasResult'] = None,
    fundamental: Optional['FundamentalContextSnapshot'] = None,
) -> Optional['LearningRecordRow']:
    """
    Builds (via `build_learning_record_from_trade()`) and persists one
    `LearningRecord` through the supplied repository. `None` when the
    trade is not yet `CLOSED` — same as `build_learning_record_from_trade()`,
    and nothing is persisted in that case.
    """
    record = build_learning_record_from_trade(
        paper_trade, context=context, performance=performance, htf_bias=htf_bias, fundamental=fundamental,
    )
    if record is None:
        return None

    return repository.record(
        record.record_id, record.trade_id, record.signal_id,
        strategy_name=record.strategy_name, market_phase=record.market_phase,
        session=record.session, timeframe=record.timeframe, result=record.result,
        r_multiple=record.r_multiple, failure_type=record.failure_type, success_pattern=record.success_pattern,
        htf_bias=record.htf_bias, volatility_state=record.volatility_state,
        fundamental_bias=record.fundamental_bias, confidence_score=record.confidence_score,
        engine_version=record.engine_version, sample_size=record.sample_size,
    )
