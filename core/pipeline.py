import time
from typing import List

from data.market_data import MarketDataNormalizer
from context.context_orchestrator import build_context_snapshot
from signals.signal_engine import SignalEngine
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
# docs/performance_report.md) while still catching a slow network call
# (Market Data fetch, Telegram delivery) worth knowing about.
SLOW_OPERATION_THRESHOLD_SECONDS = 2.0


class TradingPipeline:
    """
    Wires Data -> Context -> Signal -> AI -> Decision -> Risk ->
    Signal Formatter -> Telegram Delivery -> Persistence into a
    single, runnable flow.

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

        t0 = time.perf_counter()
        context = build_context_snapshot(candles)
        self._log_stage("context", time.perf_counter() - t0)

        # NOTE: SignalEngine.generate_signals() already runs StrategyManager
        # internally. StrategyManager must not be called separately here,
        # or every strategy would execute twice against the same context.
        t0 = time.perf_counter()
        signal_candidates = self.signal_engine.generate_signals(context)
        self._log_stage("signal", time.perf_counter() - t0)
        logger.info(f"[{self.symbol}|{self.interval}] Generated {len(signal_candidates)} signal candidate(s).")

        t0 = time.perf_counter()
        ai_results: List[AIAnalysisResult] = [
            self.ai_analyzer.analyze(candidate, context)
            for candidate in signal_candidates
        ]
        self._log_stage("ai", time.perf_counter() - t0)

        t0 = time.perf_counter()
        decisions: List[TradeDecision] = [
            self.decision_engine.evaluate(candidate, ai_result)
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
            "signals": signal_candidates,
            "ai_results": ai_results,
            "decisions": decisions,
            "risk_results": risk_results,
            "telegram_messages": telegram_messages,
            "notification_results": notification_results,
            "signal_records": signal_records,
        }
