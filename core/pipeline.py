from typing import List

from data.market_data import MarketDataNormalizer
from context.context_orchestrator import build_context_snapshot
from signals.signal_engine import SignalEngine
from ai.ai_analyzer import AIAnalyzer, AIAnalysisResult
from decision.decision_engine import DecisionEngine
from decision.models import TradeDecision
from risk.risk_manager import RiskManager, RiskResult
from telegram.signal_formatter import SignalFormatter
from core.logger import setup_logger

logger = setup_logger("TradingPipeline")


class TradingPipeline:
    """
    Wires Data -> Context -> Signal -> AI -> Decision -> Risk ->
    Telegram Output into a single, runnable flow.

    Execution and Monitoring are intentionally not part of this
    pipeline (Phase 25.1+). Risk Layer output is a sizing suggestion
    only -- no MT5/broker connection, no order execution. The
    Telegram step only formats text -- no bot, no aiogram, no sending.
    """

    def __init__(self, symbol: str, interval: str, outputsize: int):
        self.symbol = symbol
        self.interval = interval
        self.outputsize = outputsize

        self.data_normalizer = MarketDataNormalizer()
        self.signal_engine = SignalEngine()
        self.ai_analyzer = AIAnalyzer()
        self.decision_engine = DecisionEngine()
        self.risk_manager = RiskManager()
        self.signal_formatter = SignalFormatter()

    def run(self) -> dict:
        """
        Runs one full pipeline cycle: fetch candles, build context,
        generate signal candidates, evaluate each with the AI Analyzer,
        produce a TradeDecision per candidate, pass each decision
        through the Risk Layer, and format a Telegram message per
        candidate.
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

        return {
            "context": context,
            "signals": signal_candidates,
            "ai_results": ai_results,
            "decisions": decisions,
            "risk_results": risk_results,
            "telegram_messages": telegram_messages,
        }
