from typing import List

from data.market_data import MarketDataNormalizer
from context.context_orchestrator import build_context_snapshot
from signals.signal_engine import SignalEngine
from ai.ai_analyzer import AIAnalyzer, AIAnalysisResult
from decision.decision_engine import DecisionEngine
from decision.models import TradeDecision
from risk.risk_manager import RiskManager, RiskResult
from telegram.signal_formatter import SignalFormatter
from telegram.notifier import Notifier
from database.signal_repository import SignalRepository
from database.signal_record import SignalRecord, create_signal_record
from core.logger import setup_logger

logger = setup_logger("TradingPipeline")


class TradingPipeline:
    """
    Wires Data -> Context -> Signal -> AI -> Decision -> Risk ->
    Signal Formatter -> Telegram Delivery -> Persistence into a
    single, runnable flow.

    Execution and TP/SL Monitoring are intentionally not part of this
    pipeline (Phase 27.2+). Risk Layer output is a sizing suggestion
    only -- no MT5/broker connection, no order execution.

    Telegram messages are always generated, but never sent unless
    send_notifications=True is passed explicitly. Signal records are
    always built in memory, but never written to the database unless
    persist_signals=True is passed explicitly. This keeps
    backtesting/testing runs free of side effects by default.
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

    def run(self) -> dict:
        """
        Runs one full pipeline cycle: fetch candles, build context,
        generate signal candidates, evaluate each with the AI Analyzer,
        produce a TradeDecision per candidate, pass each decision
        through the Risk Layer, format a Telegram message per
        candidate, (only if send_notifications=True) deliver each
        message via the Notifier, and (only if persist_signals=True)
        persist a SignalRecord per candidate via the SignalRepository.
        """
        candles = self.data_normalizer.get_candles(
            self.symbol,
            self.interval,
            self.outputsize,
        )
        logger.info(f"[{self.symbol}|{self.interval}] Fetched {len(candles)} candles.")

        context = build_context_snapshot(candles)

        # NOTE: SignalEngine.generate_signals() already runs StrategyManager
        # internally. StrategyManager must not be called separately here,
        # or every strategy would execute twice against the same context.
        signal_candidates = self.signal_engine.generate_signals(context)
        logger.info(f"[{self.symbol}|{self.interval}] Generated {len(signal_candidates)} signal candidate(s).")

        ai_results: List[AIAnalysisResult] = [
            self.ai_analyzer.analyze(candidate, context)
            for candidate in signal_candidates
        ]

        decisions: List[TradeDecision] = [
            self.decision_engine.evaluate(candidate, ai_result)
            for candidate, ai_result in zip(signal_candidates, ai_results)
        ]
        logger.info(f"[{self.symbol}|{self.interval}] Produced {len(decisions)} trade decision(s).")

        risk_results: List[RiskResult] = [
            self.risk_manager.evaluate(decision)
            for decision in decisions
        ]
        logger.info(f"[{self.symbol}|{self.interval}] Produced {len(risk_results)} risk result(s).")

        telegram_messages: List[str] = [
            self.signal_formatter.format_signal(candidate, ai_result, decision, risk_result)
            for candidate, ai_result, decision, risk_result in zip(
                signal_candidates, ai_results, decisions, risk_results
            )
        ]
        logger.info(f"[{self.symbol}|{self.interval}] Produced {len(telegram_messages)} telegram message(s).")

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

        signal_records: List[SignalRecord] = []
        if self.persist_signals:
            for candidate, decision, risk_result in zip(signal_candidates, decisions, risk_results):
                record = create_signal_record(candidate, decision, risk_result)
                self.signal_repository.save_signal_record(record)
                signal_records.append(record)
            logger.info(f"[{self.symbol}|{self.interval}] Persisted {len(signal_records)} signal record(s).")

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
