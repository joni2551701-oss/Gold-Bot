"""
Backtesting Layer — Backtest Engine (Phase 60.2: Backtesting Engine,
TASK 3).

The full chain the Director asked for, built entirely by composing
already-existing, unmodified functions -- no trading logic (Strategy/
Signal/Decision/Risk) is reimplemented or altered anywhere in this
file:

    ReplayEngine (Phase 60.1)              -- candle source, via ReplayDataFeed/IDataFeed (TASK 2)
    context.context_orchestrator.build_context_snapshot()  -- unmodified
    context.market_phase.compute_market_phase()             -- unmodified
    signals.signal_engine.SignalEngine().generate_signals()  -- unmodified (runs strategies/ internally)
    signals.signal_quality.compute_signal_quality()          -- unmodified
    ai.ai_analyzer.AIAnalyzer().analyze()                    -- unmodified
    decision.decision_engine.DecisionEngine().evaluate()      -- unmodified
    risk.risk_manager.RiskManager().evaluate()                 -- unmodified
    signals.adapter.from_signal_candidate()                    -- unmodified
    lifecycle.paper_trade.create_paper_trade()/open_paper_trade()  -- unmodified
    lifecycle.paper_trade_monitor.check_paper_trade_against_candles()  -- unmodified
    analytics.signal_performance.compute_signal_performance()  -- unmodified
    backtesting.backtest_result.build_backtest_result()          -- Phase 60.2, TASK 4
    learning.trade_event_bridge.bridge_closed_trade()             -- Phase 60.8, TASK 3

Phase 60.8 (Safe Integration Layer, TASK 3): every candidate whose
paper trade reaches `TradeState.CLOSED` in `_process_candidate()` is
now bridged into `LearningRepository.record()` via
`bridge_closed_trade()` -- the first real caller of the bridge Phase
60.7 built and left unwired. This is deliberately the ONLY place this
phase wires it: `core/pipeline.py` never constructs a `PaperTrade`
(confirmed by TASK 1's own audit, `docs/ADAPTIVE_INTELLIGENCE_AUDIT.md`),
so live trading still records nothing to Learning -- live learning
integration is deferred until a real MT5/broker execution lifecycle
exists to produce a real CLOSED trade to observe. A `bridge_closed_trade()`
failure (e.g. a database error) is caught and logged, never allowed to
fail the backtest itself -- Learning stays a pure, non-critical
observer, same posture the whole `learning/` package already commits
to.

Reused call sequence and gate condition (`decision.action == APPROVE
and risk_result.approved`) copied verbatim from `core/pipeline.py`'s
own `run()` -- read directly this phase (TASK 1) to guarantee this
engine reaches the same APPROVE/REJECT/NO_TRADE outcome a live cycle
would for the same inputs.

Deliberate difference from live (documented, not a trading-logic
change): `core/pipeline.py` sends at most one Telegram message per
cycle (the single highest-confidence approved candidate); this engine
opens a `PaperTrade` for *every* approved+risk-approved candidate at
each step, since a backtest's purpose is measuring every strategy's
own performance, not simulating "what would have been sent to a
user." Neither `DecisionEngine` nor `RiskManager` themselves are
altered -- only what a caller does with their already-unchanged output
differs.

Scope boundary (documented, not silently skipped): HTF Bias needs a
real multi-timeframe (Daily/H4/H1) historical replay, which this phase
does not build (a single-timeframe `ReplayConfig` only). This engine
defaults every step's HTF bias to the same neutral fallback
`core/pipeline.py` itself already falls back to on a live HTF fetch
failure (`compute_htf_bias(MarketSnapshot(symbol=...))` ->
`HTFBias.UNKNOWN`) -- reusing an existing degrade path, not inventing
a new one. A caller may override this via `htf_bias_provider` for a
future phase that replays multiple timeframes together.

**A genuine Phase 60.2 bug found and fixed during Phase 60.7's own
TASK 1 reuse audit**: `_process_candidate()` originally called
`open_paper_trade(paper_trade)` and
`check_paper_trade_against_candles(paper_trade, forward_candles)`
without capturing either call's returned `.trade` -- both functions
are pure (return a *new* frozen `PaperTrade`, never mutate their
argument), so the local `paper_trade` variable silently stayed at
`TradeState.CREATED` forever, `check_paper_trade_against_candles()`
immediately no-opped on every call (its own status guard: "Cannot
monitor a trade that is not OPEN"), and every `SignalPerformance`
built downstream had `result=None` regardless of what the candle
window actually showed -- a backtest could open trades but never
actually resolve a single one to TP/SL/EXPIRED. Fixed by reassigning
`paper_trade` to each call's `.trade` (both never raise, so `.trade`
is always safe to read). See `docs/LEARNING_LOOP.md`'s Phase 60.7
section for the regression test.
"""

from datetime import datetime, timezone
from typing import Callable, Optional
from uuid import uuid4

from ai.ai_analyzer import AIAnalyzer
from analytics.signal_performance import compute_signal_performance
from backtesting.backtest_result import BacktestResult, build_backtest_result
from backtesting.data_feed import ReplayDataFeed
from backtesting.replay_engine import ReplayEngine
from backtesting.replay_models import ReplayConfig
from context_layer.context_engine.context_orchestrator import build_context_snapshot
from context_layer.trend.htf_bias import HTFBiasResult, compute_htf_bias
from context_layer.trend.market_phase import compute_market_phase
from context_layer.context_engine.snapshot import from_context_snapshot
from data_layer.live_data.market_data import MarketSnapshot
from decision_layer.decision_engine.decision_engine import DecisionEngine
from decision_layer.decision_engine.models import DecisionAction
from lifecycle.paper_trade import create_paper_trade, open_paper_trade
from lifecycle.paper_trade_monitor import check_paper_trade_against_candles
from lifecycle.trade_state import TradeState
from learning.trade_event_bridge import bridge_closed_trade
from risk_layer.risk_engine.risk_manager import RiskManager
from signal_layer.signal_builder.adapter import from_signal_candidate
from signal_layer.signal_engine.signal_engine import SignalEngine
from signal_layer.signal_scoring.signal_quality import compute_signal_quality
from database.learning_repository import LearningRepository
from database.raw_candle_repository import RawCandleRepository
from core_layer.logger.logger import setup_logger

logger = setup_logger("BacktestEngine")

_DEFAULT_CONTEXT_WINDOW = 200
_MIN_CANDLES_FOR_CONTEXT = 20


def _neutral_htf_bias(symbol: str) -> HTFBiasResult:
    """The same graceful-degradation fallback core/pipeline.py's own live run() uses on an HTF fetch failure -- reused, not reinvented."""
    return compute_htf_bias(MarketSnapshot(symbol=symbol))


class BacktestEngine:
    """
    One engine per backtest run. Every dependency is injectable (same
    optional-dependency convention as every Phase 59.x/60.x manager in
    this codebase) and defaults to the real, unmodified class --
    running with all defaults reproduces exactly what a live cycle
    would decide for the same candle window.
    """

    def __init__(
        self,
        config: ReplayConfig,
        raw_candle_repository: Optional[RawCandleRepository] = None,
        ai_analyzer: Optional[AIAnalyzer] = None,
        decision_engine: Optional[DecisionEngine] = None,
        risk_manager: Optional[RiskManager] = None,
        context_window: int = _DEFAULT_CONTEXT_WINDOW,
        htf_bias_provider: Optional[Callable[[str], HTFBiasResult]] = None,
        learning_repository: Optional[LearningRepository] = None,
    ):
        self.config = config
        self.replay_engine = ReplayEngine(config, raw_candle_repository)
        self.data_feed = ReplayDataFeed(self.replay_engine.feed)
        self.ai_analyzer = ai_analyzer or AIAnalyzer()
        self.decision_engine = decision_engine or DecisionEngine()
        self.risk_manager = risk_manager or RiskManager()
        self.signal_engine = SignalEngine()
        self.context_window = context_window
        self.htf_bias_provider = htf_bias_provider or _neutral_htf_bias
        # Phase 60.8 (Safe Integration Layer, TASK 3): the injected
        # repository bridge_closed_trade() persists through. Eager,
        # same posture as every other dependency above.
        self.learning_repository = learning_repository or LearningRepository()

        self.signals_generated = 0
        self.trades_opened = 0
        self.performances = []

    def run(self) -> BacktestResult:
        """Replays the full configured window step by step, running the real chain at every step that has enough candles for context."""
        started_at = datetime.now(timezone.utc)
        self.replay_engine.clock.play()

        while not self.replay_engine.is_finished:
            self.replay_engine.step()
            self._process_step()

        finished_at = datetime.now(timezone.utc)
        return build_backtest_result(
            symbol=self.config.symbol,
            timeframe=self.config.timeframe,
            candles_processed=self.replay_engine.candles_replayed,
            signals_generated=self.signals_generated,
            trades_opened=self.trades_opened,
            performances=self.performances,
            started_at=started_at,
            finished_at=finished_at,
        )

    def _process_step(self) -> None:
        candles = self.data_feed.get_candles(self.context_window)
        if len(candles) < _MIN_CANDLES_FOR_CONTEXT:
            return

        htf_bias = self.htf_bias_provider(self.config.symbol)
        context = build_context_snapshot(candles, htf_bias)
        market_phase = compute_market_phase(context)
        candidates = self.signal_engine.generate_signals(context)
        self.signals_generated += len(candidates)
        if not candidates:
            return

        context_snapshot_schema = from_context_snapshot(context, symbol=self.config.symbol, timeframe=self.config.timeframe)
        forward_candles = self.replay_engine.feed.candles[self.replay_engine.feed.cursor + 1:]

        for candidate in candidates:
            self._process_candidate(candidate, context, market_phase, htf_bias, context_snapshot_schema, forward_candles)

    def _process_candidate(self, candidate, context, market_phase, htf_bias, context_snapshot_schema, forward_candles) -> None:
        quality = compute_signal_quality(candidate, context, htf_bias)
        ai_result = self.ai_analyzer.analyze(candidate, context)
        decision = self.decision_engine.evaluate(candidate, ai_result, htf_bias)
        risk_result = self.risk_manager.evaluate(decision)

        signal_schema = from_signal_candidate(
            candidate,
            symbol=self.config.symbol,
            timeframe=self.config.timeframe,
            session=context_snapshot_schema.session.current_session,
            market_phase=market_phase.phase.value,
            context_id=context_snapshot_schema.snapshot_id,
            quality=quality,
            decision=decision,
            decision_id=str(uuid4()),
        )

        paper_trade = None
        # Same eligibility gate core/pipeline.py's own run() uses for Telegram delivery.
        if decision.action == DecisionAction.APPROVE and risk_result.approved:
            paper_trade = create_paper_trade(signal_schema)
            paper_trade = open_paper_trade(paper_trade).trade
            paper_trade = check_paper_trade_against_candles(paper_trade, forward_candles).trade
            self.trades_opened += 1

        performance = compute_signal_performance(
            signal_schema, paper_trade=paper_trade,
            session=context_snapshot_schema.session.current_session,
            market_phase=market_phase.phase.value,
        )
        self.performances.append(performance)

        # Phase 60.8 (Safe Integration Layer, TASK 3): the one real
        # observation point for Learning today -- see this module's own
        # docstring. Never allowed to fail the backtest: a persistence
        # error here is a Learning-layer concern, not a trading-logic
        # one, and must not abort a run that has already correctly
        # decided/priced/resolved this candidate.
        if paper_trade is not None and paper_trade.status == TradeState.CLOSED:
            try:
                bridge_closed_trade(
                    paper_trade, self.learning_repository,
                    context=context, performance=performance, htf_bias=htf_bias,
                )
            except Exception as e:
                logger.warning(f"bridge_closed_trade failed for trade_id={paper_trade.trade_id}: {e}")
