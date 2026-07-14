import time
from typing import List

from data.market_data import MarketDataNormalizer, MarketSnapshot
from data.data_quality import assess_data_quality, DataQualityResult
from context.context_orchestrator import build_context_snapshot
from context.htf_bias import compute_htf_bias, HTFBiasResult, SUPPORTED_HTF_TIMEFRAMES
from features.feature_engine import compute_market_features
from features.feature_model import MarketFeatures
from signals.signal_engine import SignalEngine
from signals.signal_quality import compute_signal_quality, SignalQualityResult
from signals.explainability import explain_signal, SignalExplanation
from ai.ai_analyzer import AIAnalyzer, AIAnalysisResult
from decision.decision_engine import DecisionEngine
from decision.models import TradeDecision, DecisionAction
from risk.risk_manager import RiskManager, RiskResult
from telegram.signal_formatter import SignalFormatter
from telegram.notifier import Notifier
from database.signal_repository import SignalRepository
from database.signal_record import SignalRecord, create_signal_record
from core.logger import setup_logger

logger = setup_logger("TradingPipeline")

# Phase 53 performance monitoring: any single stage taking longer than
# this is logged as a WARNING (monitoring only -- never blocks, never
# retries, never changes behavior). 2s comfortably covers this
# pipeline's own compute (sub-millisecond per stage, benchmarked in
# docs/PERFORMANCE.md) while still catching a slow network call
# (Market Data fetch, Telegram delivery) worth knowing about.
SLOW_OPERATION_THRESHOLD_SECONDS = 2.0


class TradingPipeline:
    """
    Wires Data -> Data Quality -> HTF Bias -> Context -> Feature
    Engineering -> Signal -> Signal Quality -> Explainability -> AI ->
    Decision -> Risk -> Signal Formatter -> Telegram Delivery ->
    Persistence into a single, runnable flow.

    Feature Engineering (Phase A10, features/feature_engine.py) builds
    one MarketFeatures snapshot per cycle (atr, volatility,
    trend_strength, session, regime, htf_bias, liquidity_distance,
    volume) entirely from already-computed data -- no new indicator.
    volume is always None: this codebase has no volume data source,
    and this field is an explicit, honest hook rather than a
    fabricated value. Purely advisory: not passed into
    SignalEngine/AIAnalyzer/DecisionEngine/RiskManager in this phase.
    Returned in run()'s result dict ("features") for a future AI
    Analyzer, backtester, or ML dataset exporter to consume.

    Explainability (Phase A9, signals/explainability.py) turns each
    signal candidate's already-computed context into human-readable
    reasons -- reusing Signal Quality's criteria_met plus Wyckoff/
    Session/Market Regime, no new detection logic, no new confidence
    computation (SignalCandidate.confidence is relayed, not
    recomputed). Purely advisory: not passed into AIAnalyzer,
    DecisionEngine, or RiskManager in this phase, and never blocks or
    alters any existing stage. Returned in run()'s result dict
    ("explanations", one per candidate, same order as "signals") for
    a future consumer (e.g. Telegram message enrichment) to use.

    Data Quality (Phase A8, data/data_quality.py) assesses the candle
    list get_candles() already returned -- missing candles, duplicate
    timestamps, invalid OHLC, timeframe consistency -- into a scored,
    structured DataQualityResult. Purely observational: it never
    filters, blocks, or alters the candles the rest of the cycle uses,
    even when data_quality.valid is False. Returned in run()'s result
    dict ("data_quality") for a future, separately-approved phase to
    consume (e.g. skipping a cycle below some quality threshold -- not
    implemented here).

    Signal Quality Score (Phase A4, signals/signal_quality.py) grades
    each signal candidate's alignment with HTF Bias and existing
    context (Structure, Liquidity, Order Blocks, FVG) into a letter
    grade (A+/A/B/C). Purely advisory, like HTF Bias was before Phase
    A3 -- it is not passed into AIAnalyzer, DecisionEngine, or
    RiskManager in this phase, and never blocks or alters any existing
    stage. It is returned in run()'s result dict ("quality_results",
    one per candidate, same order as "signals") for a future,
    separately-approved phase to consume.

    Market Regime (Phase A7, context/market_regime.py) classifies
    overall market character (TRENDING/RANGE/ACCUMULATION/
    DISTRIBUTION/HIGH_VOLATILITY/LOW_VOLATILITY/UNKNOWN) from
    already-computed Structure, Wyckoff events, session/volatility
    data, and (if available) HTF Bias -- htf_bias is passed into
    build_context_snapshot() specifically so Market Regime can read it
    (the only reason ContextSnapshot construction now takes htf_bias
    at all; every other detector still only reads candles). Purely
    advisory: `context.market_regime` is part of ContextSnapshot, not
    consumed by any strategy, AIAnalyzer, DecisionEngine, or
    RiskManager in this phase.

    HTF Bias (Phase A2, context/htf_bias.py) describes the higher-
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
    ):
        self.symbol = symbol
        self.interval = interval
        self.outputsize = outputsize
        self.send_notifications = send_notifications
        self.persist_signals = persist_signals

        self.data_normalizer = MarketDataNormalizer()
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

        # Feature Engineering (Phase A10): one MarketFeatures snapshot
        # per cycle (not per-candidate, like htf_bias/market_regime --
        # it describes the overall market context at this point, not
        # a specific signal). Built entirely from already-computed
        # data; no new indicator. volume is always None -- no data
        # source exists, never fabricated.
        t0 = time.perf_counter()
        features: MarketFeatures = compute_market_features(context, htf_bias)
        self._log_stage("features", time.perf_counter() - t0)
        logger.info(
            f"[{self.symbol}|{self.interval}] Features: regime={features.regime} "
            f"session={features.session} volatility={features.volatility} "
            f"trend_strength={features.trend_strength:.2f}"
        )

        # NOTE: SignalEngine.generate_signals() already runs StrategyManager
        # internally. StrategyManager must not be called separately here,
        # or every strategy would execute twice against the same context.
        t0 = time.perf_counter()
        signal_candidates = self.signal_engine.generate_signals(context)
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

        t0 = time.perf_counter()
        ai_results: List[AIAnalysisResult] = [
            self.ai_analyzer.analyze(candidate, context)
            for candidate in signal_candidates
        ]
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

        t0 = time.perf_counter()
        notification_results: List[bool] = []
        if self.send_notifications:
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
        self._log_stage("telegram_delivery", time.perf_counter() - t0)

        t0 = time.perf_counter()
        signal_records: List[SignalRecord] = []
        if self.persist_signals:
            for candidate, decision, risk_result in zip(signal_candidates, decisions, risk_results):
                # timeframe has no source on SignalCandidate/TradeDecision/
                # RiskResult -- the pipeline is the only thing that knows
                # which interval it queried (Phase 39 display field).
                record = create_signal_record(candidate, decision, risk_result, timeframe=self.interval)
                self.signal_repository.save_signal_record(record)
                signal_records.append(record)
            logger.info(f"[{self.symbol}|{self.interval}] Persisted {len(signal_records)} signal record(s).")
        self._log_stage("database", time.perf_counter() - t0)

        total_duration = time.perf_counter() - pipeline_start
        logger.info(f"[{self.symbol}|{self.interval}] pipeline_finished duration={total_duration:.3f}s")

        return {
            "context": context,
            "features": features,
            "data_quality": data_quality,
            "htf_bias": htf_bias,
            "signals": signal_candidates,
            "quality_results": quality_results,
            "explanations": explanations,
            "ai_results": ai_results,
            "decisions": decisions,
            "risk_results": risk_results,
            "telegram_messages": telegram_messages,
            "notification_results": notification_results,
            "signal_records": signal_records,
        }
