import time
import uuid
from typing import List, Optional

from data_layer.live_data.market_data import MarketSnapshot
from data_layer.live_data.market_data_service import MarketDataService
from data_layer.data_validation.data_quality import assess_data_quality, DataQualityResult
from context_layer.context_engine.context_orchestrator import build_context_snapshot
from context_layer.trend.htf_bias import compute_htf_bias, HTFBiasResult, SUPPORTED_HTF_TIMEFRAMES
from context_layer.trend.market_phase import compute_market_phase, MarketPhaseResult
from context_layer.context_engine.snapshot import from_context_snapshot, ContextSnapshotSchema
from features.feature_engine import compute_market_features
from features.feature_model import MarketFeatures
from signal_layer.signal_engine.signal_engine import SignalEngine
from signal_layer.signal_scoring.signal_quality import compute_signal_quality, SignalQualityResult
from signal_layer.signal_scoring.explainability import explain_signal, SignalExplanation
from signal_layer.signal_builder.adapter import from_signal_candidate
from signal_layer.signal_builder.schema import SignalSchema
from ai.ai_analyzer import AIAnalyzer, AIAnalysisResult
from decision_layer.decision_engine.decision_engine import DecisionEngine
from decision_layer.decision_engine.models import TradeDecision, DecisionAction
from risk_layer.risk_engine.risk_manager import RiskManager, RiskResult
from telegram.signal_formatter import SignalFormatter
from telegram.notifier import Notifier
from database.signal_repository import SignalRepository
from database.signal_record import SignalRecord, create_signal_record
from core_layer.pipeline.pipeline_guard import PipelineGuard
from core_layer.logger.logger import setup_logger

logger = setup_logger("TradingPipeline")

# Phase 53 performance monitoring: any single stage taking longer than
# this is logged as a WARNING (monitoring only -- never blocks, never
# retries, never changes behavior). 2s comfortably covers this
# pipeline's own compute (sub-millisecond per stage, benchmarked in
# docs/PERFORMANCE.md) while still catching a slow network call
# (Market Data fetch, Telegram delivery) worth knowing about.
SLOW_OPERATION_THRESHOLD_SECONDS = 2.0


def _neutral_ai_result(reason: str) -> AIAnalysisResult:
    """
    Phase 60.8 (Safe Integration Layer, TASK 2): the substitute
    AIAnalysisResult used when PipelineGuard.before_ai() says the `ai`
    stage should be skipped (ENABLE_AI=False). Neutral, never
    blocking -- approved=True, confidence/risk_score at the exact
    midpoint -- so DecisionEngine.evaluate() still runs its normal
    weighted formula unobstructed, matching this codebase's own
    "AI optional" architecture (AI absence must never be worse than
    AI's own heuristic-stub verdict, and must never itself force a
    reject). The same "degrade to a documented neutral value, never
    raise, never block" posture already established for a missing HTF
    read (`context.htf_bias.compute_htf_bias`'s own UNKNOWN fallback)
    and `backtesting/backtest_engine.py`'s `_neutral_htf_bias()`.
    """
    return AIAnalysisResult(
        approved=True, confidence=0.5, risk_score=0.5,
        explanation=f"AI stage skipped: {reason}",
    )


class TradingPipeline:
    """
    Wires Data -> Data Quality -> HTF Bias -> Context -> Market Phase ->
    Signal -> Signal Quality -> Explainability -> Feature Engineering ->
    AI -> Decision -> Risk -> Signal History -> Signal Formatter ->
    Telegram Delivery -> Persistence into a single, runnable flow.

    Market Phase (Pre-Phase 59 Architecture Readiness Review, AC-02,
    context_layer/trend/market_phase.py) classifies the market into one of six
    states (ACCUMULATION/MANIPULATION/DISTRIBUTION/MARKUP/MARKDOWN/
    UNKNOWN) once per cycle, entirely from data already on
    ContextSnapshot (wyckoff_events, amd_events, market_regime) -- no
    new detection logic, context_layer/wyckoff/wyckoff.py and context_layer/amd/amd.py are
    unmodified. Purely advisory: not consumed by any strategy,
    AIAnalyzer, DecisionEngine, or RiskManager. Returned in run()'s
    result dict ("market_phase") for a future AI explanation or
    Education consumer.

    Signal History (Pre-Phase 59 Architecture Readiness Review, AC-03,
    signal_layer/signal_builder/adapter.py + context_layer/context_engine/snapshot.py) builds one
    ContextSnapshotSchema per cycle and one SignalSchema per candidate,
    with a real context_id (the cycle's ContextSnapshotSchema.snapshot_id)
    and a real decision_id (freshly generated per TradeDecision) --
    closing the "Signal + Context Historical Link" gap Phase A15/A16
    deliberately left as an unwired hook. strategy_name already carries
    the real strategy identifier (Phase A11's StrategyDefinition.id),
    so no separate strategy_id field was added. Computes nothing new:
    signal_quality/decision are relayed from the already-computed
    SignalQualityResult/TradeDecision; as of Phase 59 Real Market
    Validation Foundation (TASK 2), each SignalSchema also carries
    market_phase, relayed from the same cycle's already-computed
    MarketPhaseResult (the market_phase stage above) -- still no new
    computation. Not written to the database in this phase -- returned
    in run()'s result dict ("context_snapshot", "signal_history") for
    a future, separately-approved persistence phase to consume.

    Feature Engineering (Phase A10, features/feature_engine.py) is a
    standardization layer, not an analysis layer -- it does not
    analyze the market itself, it turns results already produced by
    Context/Signal Quality/Explainability into one standard
    MarketFeatures object per candidate (asset, timeframe, htf_bias,
    market_regime, session, signal_quality, confidence, volatility,
    trend_strength, liquidity_distance, volume, atr) for a future AI
    Analyzer, backtester, or ML dataset exporter. Runs at the END of
    the per-candidate analysis chain -- after Signal Quality Score and
    Explainability, since signal_quality/confidence are relayed
    directly from SignalExplanation, not recomputed. volume and atr
    are always None: this codebase has no volume data source, and a
    real ATR would be a new indicator, out of scope for a
    standardization-only phase -- both are explicit, honest hooks
    rather than fabricated values. Purely advisory: not passed into
    SignalEngine/AIAnalyzer/DecisionEngine/RiskManager in this phase.
    Returned in run()'s result dict ("features", one per candidate,
    same order as "signals") for a future consumer to use.

    Explainability (Phase A9, signal_layer/signal_scoring/explainability.py) turns each
    signal candidate's already-computed context into human-readable
    reasons -- reusing Signal Quality's criteria_met plus Wyckoff/
    Session/Market Regime, no new detection logic, no new confidence
    computation (SignalCandidate.confidence is relayed, not
    recomputed). Purely advisory: not passed into AIAnalyzer,
    DecisionEngine, or RiskManager in this phase, and never blocks or
    alters any existing stage. Returned in run()'s result dict
    ("explanations", one per candidate, same order as "signals") for
    a future consumer (e.g. Telegram message enrichment) to use.

    Data Quality (Phase A8, data_layer/data_validation/data_quality.py) assesses the candle
    list get_candles() already returned -- missing candles, duplicate
    timestamps, invalid OHLC, timeframe consistency -- into a scored,
    structured DataQualityResult. Purely observational: it never
    filters, blocks, or alters the candles the rest of the cycle uses,
    even when data_quality.valid is False. Returned in run()'s result
    dict ("data_quality") for a future, separately-approved phase to
    consume (e.g. skipping a cycle below some quality threshold -- not
    implemented here).

    Signal Quality Score (Phase A4, signal_layer/signal_scoring/signal_quality.py) grades
    each signal candidate's alignment with HTF Bias and existing
    context (Structure, Liquidity, Order Blocks, FVG) into a letter
    grade (A+/A/B/C). Purely advisory, like HTF Bias was before Phase
    A3 -- it is not passed into AIAnalyzer, DecisionEngine, or
    RiskManager in this phase, and never blocks or alters any existing
    stage. It is returned in run()'s result dict ("quality_results",
    one per candidate, same order as "signals") for a future,
    separately-approved phase to consume.

    Market Regime (Phase A7, context_layer/trend/market_regime.py) classifies
    overall market character (TRENDING/RANGE/ACCUMULATION/
    DISTRIBUTION/HIGH_VOLATILITY/LOW_VOLATILITY/UNKNOWN) from
    already-computed Structure, Wyckoff events, session/volatility
    data, and (if available) HTF Bias -- htf_bias is passed into
    build_context_snapshot() specifically so Market Regime can read it
    (the only reason ContextSnapshot construction now takes htf_bias
    at all; every other detector still only reads candles). Purely
    advisory: `context_layer.trend.market_regime` is part of ContextSnapshot, not
    consumed by any strategy, AIAnalyzer, DecisionEngine, or
    RiskManager in this phase.

    HTF Bias (Phase A2, context_layer/trend/htf_bias.py) describes the higher-
    timeframe (Daily/H4/H1) market state only -- it is never passed
    into Strategies or the AI Analyzer, and it never blocks or alters
    any existing stage. As of Phase A3 (Decision Engine v2), it is
    passed into DecisionEngine.evaluate() as one of four weighted
    inputs to the final confidence score (see
    docs/ARCHITECTURE.md's Decision Engine v2 section) -- it still
    never itself approves/rejects a trade; it only contributes a
    bounded component to a score the existing threshold logic then
    evaluates, same as before. It is also returned in run()'s result
    dict ("htf_bias") in full. A failure fetching HTF data degrades to
    HTFBias.UNKNOWN (logged), never raises, and never affects the rest
    of the cycle -- the Decision Engine treats a missing/UNKNOWN HTF
    read as a neutral (non-penalizing, non-rewarding) contribution.

    Execution and TP/SL Monitoring are intentionally not part of this
    pipeline (Phase 27.2+). Risk Layer output is a sizing suggestion
    only -- no MT5/broker connection, no order execution.

    Telegram messages are only ever generated for the single best
    candidate that both the Decision Engine APPROVEd and the Risk
    Manager approved (action == APPROVE and risk_result.approved is
    True) -- REJECT, NO_TRADE, and risk-blocked candidates (including
    invalid SL/TP geometry, caught by RiskManager.validate_geometry())
    are never formatted or sent. When multiple candidates qualify in
    one cycle, only the highest-confidence one is sent -- at most one
    Telegram message per pipeline run. Delivery only happens if
    send_notifications=True is passed explicitly. Signal records are
    always built for every candidate regardless of approval (so
    rejected/blocked signals remain available for analytics), but
    only written to the database if persist_signals=True is passed
    explicitly. This keeps backtesting/testing runs free of side
    effects by default.
    """

    def __init__(
        self,
        symbol: str,
        interval: str,
        outputsize: int,
        send_notifications: bool = False,
        persist_signals: bool = False,
        pipeline_guard: Optional[PipelineGuard] = None,
    ):
        self.symbol = symbol
        self.interval = interval
        self.outputsize = outputsize
        self.send_notifications = send_notifications
        self.persist_signals = persist_signals

        # TASK-DATA-001 Phase 2: depends on MarketDataService (a thin,
        # uncached facade over MarketDataNormalizer -- see
        # data_layer/live_data/market_data_service.py's docstring for why it is uncached
        # in this phase and the Price Stream Service split). Attribute
        # name kept as `data_normalizer` -- existing tests monkeypatch
        # `pipeline.data_normalizer.get_candles`/`.get_snapshot` directly
        # on this instance to avoid real API calls; MarketDataService
        # exposes the identical two methods, so those patches still work
        # unchanged.
        self.data_normalizer = MarketDataService()
        self.signal_engine = SignalEngine()
        self.ai_analyzer = AIAnalyzer()
        self.decision_engine = DecisionEngine()
        self.risk_manager = RiskManager()
        self.signal_formatter = SignalFormatter()
        self.notifier = Notifier()
        # Only constructed when needed: SignalRepository.__init__() touches
        # disk (creates the DB file/schema), which must not happen for a
        # default/backtesting run.
        self.signal_repository = SignalRepository() if persist_signals else None
        # Phase 60.8 (Safe Integration Layer, TASK 2): eagerly
        # constructed like every other dependency above -- unlike
        # signal_repository, PipelineGuard's checks run on every cycle
        # regardless of persist_signals, so there is no flag to make it
        # conditional on. Injectable for tests (same convention as
        # every other manager in this codebase).
        self.pipeline_guard = pipeline_guard or PipelineGuard()

    def _log_stage(self, stage: str, duration: float) -> None:
        """
        Phase 53 performance monitoring: one consistent log line per
        stage, plus a WARNING if it crossed SLOW_OPERATION_THRESHOLD_SECONDS.
        Monitoring only -- never raises, never alters the stage's result.
        """
        logger.info(f"[{self.symbol}|{self.interval}] stage={stage} duration={duration:.3f}s")
        if duration > SLOW_OPERATION_THRESHOLD_SECONDS:
            logger.warning(
                f"slow_operation module=TradingPipeline stage={stage} "
                f"duration={duration:.3f}s threshold={SLOW_OPERATION_THRESHOLD_SECONDS}s"
            )

    def _aborted_result(
        self,
        context,
        data_quality: DataQualityResult,
        htf_bias: HTFBiasResult,
        market_phase: MarketPhaseResult,
    ) -> dict:
        """
        Phase 60.8 (Safe Integration Layer, TASK 2/3): the early-return
        shape used when PipelineGuard reports EmergencyState.KILLED.
        Same key set as run()'s own normal return -- every downstream
        consumer that already handles an empty-list stage (a
        pre-existing, ordinary outcome whenever no strategy triggers)
        handles this the same way. context_snapshot stays None (it is
        normally built later, alongside signal_history, from data this
        early-return path never reaches) rather than duplicating that
        construction here.
        """
        return {
            "context": context,
            "data_quality": data_quality,
            "htf_bias": htf_bias,
            "market_phase": market_phase,
            "signals": [],
            "quality_results": [],
            "explanations": [],
            "features": [],
            "context_snapshot": None,
            "signal_history": [],
            "ai_results": [],
            "decisions": [],
            "risk_results": [],
            "telegram_messages": [],
            "notification_results": [],
            "signal_records": [],
        }

    def run(self) -> dict:
        """
        Runs one full pipeline cycle: fetch candles, build context,
        generate signal candidates, evaluate each with the AI Analyzer,
        produce a TradeDecision per candidate, pass each decision
        through the Risk Layer, select the single best APPROVE+approved
        candidate (if any) and format one Telegram message for it,
        (only if send_notifications=True) deliver that message via the
        Notifier, and (only if persist_signals=True) persist a
        SignalRecord for every candidate via the SignalRepository.
        """
        pipeline_start = time.perf_counter()
        logger.info(f"[{self.symbol}|{self.interval}] pipeline_started")

        t0 = time.perf_counter()
        candles = self.data_normalizer.get_candles(
            self.symbol,
            self.interval,
            self.outputsize,
        )
        self._log_stage("market_data", time.perf_counter() - t0)
        logger.info(f"[{self.symbol}|{self.interval}] Fetched {len(candles)} candles.")

        # Data Quality (Phase A8): assesses the candle list
        # get_candles() already returned -- reports (never filters
        # further) missing candles, duplicates, invalid OHLC, and
        # timeframe consistency. Purely observational: never blocks or
        # alters the candles the rest of the cycle uses, even when
        # data_quality.valid is False.
        t0 = time.perf_counter()
        data_quality: DataQualityResult = assess_data_quality(candles, self.interval)
        self._log_stage("data_quality", time.perf_counter() - t0)
        logger.info(
            f"[{self.symbol}|{self.interval}] Data quality: valid={data_quality.valid} "
            f"score={data_quality.score:.2f} issues={list(data_quality.issues)}"
        )

        # HTF Bias (Phase A2): a separate, best-effort fetch of the
        # Daily/H4/H1 snapshot, independent of the execution-timeframe
        # candles fetched above. Never raises -- any fetch/compute
        # failure here degrades to HTFBias.UNKNOWN rather than
        # affecting the rest of the cycle, since HTF Bias is
        # context-only and nothing downstream depends on it yet.
        t0 = time.perf_counter()
        try:
            htf_snapshot = self.data_normalizer.get_snapshot(
                self.symbol, list(SUPPORTED_HTF_TIMEFRAMES)
            )
            htf_bias: HTFBiasResult = compute_htf_bias(htf_snapshot)
        except Exception as e:
            logger.warning(f"[{self.symbol}|{self.interval}] HTF bias computation failed: {e}")
            htf_bias = compute_htf_bias(MarketSnapshot(symbol=self.symbol))
        self._log_stage("htf_bias", time.perf_counter() - t0)
        logger.info(
            f"[{self.symbol}|{self.interval}] HTF bias: {htf_bias.bias.value} "
            f"confidence={htf_bias.confidence:.2f} quality_score={htf_bias.quality_score:.2f}"
        )

        t0 = time.perf_counter()
        context = build_context_snapshot(candles, htf_bias)
        self._log_stage("context", time.perf_counter() - t0)

        # Market Phase (Pre-Phase 59 Architecture Readiness Review,
        # AC-02): a 5-state (+ UNKNOWN) classification of where the
        # market sits in the Accumulation-Manipulation-Distribution-
        # Markup-Markdown cycle, computed entirely from data already on
        # `context` (wyckoff_events, amd_events, market_regime) -- no
        # new detection logic, context_layer/wyckoff/wyckoff.py and context_layer/amd/amd.py
        # are unmodified. Purely advisory: not consumed by any
        # strategy, AIAnalyzer, DecisionEngine, or RiskManager.
        t0 = time.perf_counter()
        market_phase: MarketPhaseResult = compute_market_phase(context)
        self._log_stage("market_phase", time.perf_counter() - t0)
        logger.info(
            f"[{self.symbol}|{self.interval}] Market phase: {market_phase.phase.value} "
            f"({market_phase.reason})"
        )

        # Phase 60.8 (Safe Integration Layer, TASK 2/3): the earliest of
        # PipelineGuard's four hooks -- an abort here (EmergencyState.
        # KILLED) stops the run before any signal is generated, any
        # decision made, anything sent, or anything persisted. Nothing
        # above this line (market_data/data_quality/htf_bias/context/
        # market_phase) is gated -- see pipeline_guard.py's own
        # "Disclosed Findings" for why.
        signal_decision = self.pipeline_guard.before_signal()
        if signal_decision.abort:
            logger.warning(f"[{self.symbol}|{self.interval}] pipeline_aborted stage=signal reason={signal_decision.reason}")
            return self._aborted_result(context, data_quality, htf_bias, market_phase)

        # NOTE: SignalEngine.generate_signals() already runs StrategyManager
        # internally. StrategyManager must not be called separately here,
        # or every strategy would execute twice against the same context.
        t0 = time.perf_counter()
        if signal_decision.proceed:
            signal_candidates = self.signal_engine.generate_signals(context)
        else:
            signal_candidates = []
            logger.info(f"[{self.symbol}|{self.interval}] signal_stage_skipped reason={signal_decision.reason}")
        self._log_stage("signal", time.perf_counter() - t0)
        logger.info(f"[{self.symbol}|{self.interval}] Generated {len(signal_candidates)} signal candidate(s).")

        # Signal Quality Score (Phase A4): per-candidate, independent of
        # AI/Decision -- grades each candidate's alignment with HTF Bias
        # and existing context (Structure, Liquidity, Order Blocks, FVG)
        # into a letter grade. Advisory only: not consumed by
        # AIAnalyzer/DecisionEngine/RiskManager in this phase, same
        # "compute now, wire into Decision Engine in a later,
        # separately-approved phase" posture Phase A2's HTF Bias used
        # before Phase A3 connected it.
        t0 = time.perf_counter()
        quality_results: List[SignalQualityResult] = [
            compute_signal_quality(candidate, context, htf_bias)
            for candidate in signal_candidates
        ]
        self._log_stage("signal_quality", time.perf_counter() - t0)
        if quality_results:
            logger.info(
                f"[{self.symbol}|{self.interval}] Signal quality grades: "
                f"{[q.grade.value for q in quality_results]}"
            )

        # Explainability (Phase A9): per-candidate human-readable
        # reasons, reusing Signal Quality's already-computed
        # criteria_met plus Wyckoff/Session/Market Regime context --
        # no new detection logic, no new confidence computation.
        # Advisory only: not consumed by AIAnalyzer/DecisionEngine/
        # RiskManager in this phase.
        t0 = time.perf_counter()
        explanations: List[SignalExplanation] = [
            explain_signal(candidate, context, quality)
            for candidate, quality in zip(signal_candidates, quality_results)
        ]
        self._log_stage("explainability", time.perf_counter() - t0)

        # Feature Engineering (Phase A10, corrected): a standardization
        # layer, not an analysis layer -- runs at the end of the
        # per-candidate analysis chain (after Signal Quality Score and
        # Explainability), turning their already-computed results into
        # one MarketFeatures snapshot per candidate. atr/volume stay
        # explicit None hooks -- no new indicator, no fabricated value.
        t0 = time.perf_counter()
        features: List[MarketFeatures] = [
            compute_market_features(context, explanation, self.symbol, self.interval, htf_bias)
            for explanation in explanations
        ]
        self._log_stage("features", time.perf_counter() - t0)
        if features:
            logger.info(
                f"[{self.symbol}|{self.interval}] Features: "
                f"{[(f.market_regime, f.session, f.signal_quality) for f in features]}"
            )

        # Phase 60.8 (Safe Integration Layer, TASK 2/3): AI stage guard.
        # A skip substitutes a neutral AIAnalysisResult per candidate
        # (_neutral_ai_result()) rather than an empty list -- Decision
        # Engine must still evaluate every candidate normally, matching
        # this codebase's "AI optional" architecture (AI's absence must
        # never itself force a reject).
        ai_decision = self.pipeline_guard.before_ai()
        if ai_decision.abort:
            logger.warning(f"[{self.symbol}|{self.interval}] pipeline_aborted stage=ai reason={ai_decision.reason}")
            return self._aborted_result(context, data_quality, htf_bias, market_phase)

        t0 = time.perf_counter()
        if ai_decision.proceed:
            ai_results: List[AIAnalysisResult] = [
                self.ai_analyzer.analyze(candidate, context)
                for candidate in signal_candidates
            ]
        else:
            ai_results = [_neutral_ai_result(ai_decision.reason) for _ in signal_candidates]
            logger.info(f"[{self.symbol}|{self.interval}] ai_stage_skipped reason={ai_decision.reason}")
        self._log_stage("ai", time.perf_counter() - t0)

        t0 = time.perf_counter()
        decisions: List[TradeDecision] = [
            self.decision_engine.evaluate(candidate, ai_result, htf_bias)
            for candidate, ai_result in zip(signal_candidates, ai_results)
        ]
        self._log_stage("decision", time.perf_counter() - t0)
        logger.info(f"[{self.symbol}|{self.interval}] Produced {len(decisions)} trade decision(s).")

        t0 = time.perf_counter()
        risk_results: List[RiskResult] = [
            self.risk_manager.evaluate(decision)
            for decision in decisions
        ]
        self._log_stage("risk", time.perf_counter() - t0)
        logger.info(f"[{self.symbol}|{self.interval}] Produced {len(risk_results)} risk result(s).")

        # Signal <-> Context Historical Link (Pre-Phase 59 Architecture
        # Readiness Review, AC-03): builds one standard, portable
        # SignalSchema per candidate (Phase A15), referencing the real
        # ContextSnapshotSchema this cycle produced (Phase A16) via
        # context_id, plus a freshly-generated decision_id for the real
        # TradeDecision each candidate received. Computes nothing new --
        # signal_quality/decision are relayed from the already-computed
        # SignalQualityResult/TradeDecision, never recomputed.
        # strategy_name already carries the real strategy identifier
        # (matching strategy_layer.strategy_manager.lifecycle.strategy_registry.StrategyDefinition.id),
        # so no separate "strategy_id" field was needed. Not written to
        # the database in this phase -- the link now exists and is
        # returned in run()'s result dict, ready for a future,
        # separately-approved persistence phase.
        t0 = time.perf_counter()
        context_snapshot: ContextSnapshotSchema = from_context_snapshot(
            context, symbol=self.symbol, timeframe=self.interval
        )
        signal_history: List[SignalSchema] = [
            from_signal_candidate(
                candidate,
                symbol=self.symbol,
                timeframe=self.interval,
                session=context_snapshot.session.current_session,
                market_phase=market_phase.phase.value,
                context_id=context_snapshot.snapshot_id,
                quality=quality,
                decision=decision,
                decision_id=str(uuid.uuid4()),
            )
            for candidate, quality, decision in zip(signal_candidates, quality_results, decisions)
        ]
        self._log_stage("signal_history", time.perf_counter() - t0)
        if signal_history:
            logger.info(
                f"[{self.symbol}|{self.interval}] Signal history: {len(signal_history)} "
                f"record(s) linked to context snapshot {context_snapshot.snapshot_id}."
            )

        # Only a candidate the Decision Engine APPROVEd AND the Risk
        # Manager approved (valid geometry, valid stop-loss distance)
        # is eligible for Telegram. REJECT/NO_TRADE decisions and
        # risk-blocked candidates are still returned in "decisions"/
        # "risk_results" and still persisted below, but must never be
        # formatted or sent -- this is the fix for rejected/blocked
        # signals reaching production users.
        approved_indices = [
            i
            for i, (decision, risk_result) in enumerate(zip(decisions, risk_results))
            if decision.action == DecisionAction.APPROVE and risk_result.approved
        ]

        # A single pipeline cycle can produce several independently
        # APPROVEd candidates (one per strategy). At most one
        # notification may ever be sent per cycle, so the
        # highest-confidence approved candidate is selected as the
        # winner and the rest are dropped from the Telegram path.
        best_index = (
            max(approved_indices, key=lambda i: decisions[i].confidence)
            if approved_indices
            else None
        )

        t0 = time.perf_counter()
        telegram_messages: List[str] = []
        if best_index is not None:
            telegram_messages = [
                self.signal_formatter.format_signal(
                    signal_candidates[best_index],
                    ai_results[best_index],
                    decisions[best_index],
                    risk_results[best_index],
                )
            ]
        self._log_stage("telegram_format", time.perf_counter() - t0)
        logger.info(f"[{self.symbol}|{self.interval}] Produced {len(telegram_messages)} telegram message(s).")

        # Phase 60.8 (Safe Integration Layer, TASK 2/3): before_execution()
        # gates only the actual delivery call below -- telegram_format
        # above stays unconditional, so result["telegram_messages"]
        # still shows what would have been sent even when delivery
        # itself is skipped (EmergencyState.PAUSED, or ENABLE_EXECUTION
        # disabled). See pipeline_guard.py's own "Disclosed Findings"
        # for why "execution" maps to Telegram delivery here, not to
        # execution_layer/execution_engine/execution_engine.py (untouched, still inert).
        execution_decision = self.pipeline_guard.before_execution()
        if execution_decision.abort:
            logger.warning(f"[{self.symbol}|{self.interval}] pipeline_aborted stage=execution reason={execution_decision.reason}")
            return self._aborted_result(context, data_quality, htf_bias, market_phase)

        t0 = time.perf_counter()
        notification_results: List[bool] = []
        if self.send_notifications and execution_decision.proceed:
            # send_messages() delivers the whole batch through one
            # event loop / one aiohttp session (Phase 33.1) -- calling
            # send_message() once per message here previously opened a
            # fresh event loop per call while reusing the same bot,
            # which broke after the first successful send.
            notification_results = self.notifier.send_messages(telegram_messages)
            logger.info(
                f"[{self.symbol}|{self.interval}] Sent {sum(notification_results)}/"
                f"{len(notification_results)} telegram notification(s)."
            )
        elif self.send_notifications and not execution_decision.proceed:
            logger.info(f"[{self.symbol}|{self.interval}] execution_stage_skipped reason={execution_decision.reason}")
        self._log_stage("telegram_delivery", time.perf_counter() - t0)

        # Phase 60.8 (Safe Integration Layer, TASK 2/3): before_database()
        # gates the persistence write only -- signal_records still ends
        # up empty (same shape as any ordinary zero-candidate cycle)
        # when skipped, never a partial/inconsistent write.
        database_decision = self.pipeline_guard.before_database()
        if database_decision.abort:
            logger.warning(f"[{self.symbol}|{self.interval}] pipeline_aborted stage=database reason={database_decision.reason}")
            return self._aborted_result(context, data_quality, htf_bias, market_phase)

        t0 = time.perf_counter()
        signal_records: List[SignalRecord] = []
        if self.persist_signals and database_decision.proceed:
            for candidate, decision, risk_result in zip(signal_candidates, decisions, risk_results):
                # timeframe has no source on SignalCandidate/TradeDecision/
                # RiskResult -- the pipeline is the only thing that knows
                # which interval it queried (Phase 39 display field).
                record = create_signal_record(candidate, decision, risk_result, timeframe=self.interval)
                self.signal_repository.save_signal_record(record)
                signal_records.append(record)
            logger.info(f"[{self.symbol}|{self.interval}] Persisted {len(signal_records)} signal record(s).")
        elif self.persist_signals and not database_decision.proceed:
            logger.info(f"[{self.symbol}|{self.interval}] database_stage_skipped reason={database_decision.reason}")
        self._log_stage("database", time.perf_counter() - t0)

        total_duration = time.perf_counter() - pipeline_start
        logger.info(f"[{self.symbol}|{self.interval}] pipeline_finished duration={total_duration:.3f}s")

        return {
            "context": context,
            "data_quality": data_quality,
            "htf_bias": htf_bias,
            "market_phase": market_phase,
            "signals": signal_candidates,
            "quality_results": quality_results,
            "explanations": explanations,
            "features": features,
            "context_snapshot": context_snapshot,
            "signal_history": signal_history,
            "ai_results": ai_results,
            "decisions": decisions,
            "risk_results": risk_results,
            "telegram_messages": telegram_messages,
            "notification_results": notification_results,
            "signal_records": signal_records,
        }
