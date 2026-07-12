from typing import List

from data.market_data import MarketDataNormalizer
from context.context_orchestrator import build_context_snapshot
from signals.signal_engine import SignalEngine
from ai.ai_analyzer import AIAnalyzer, AIAnalysisResult
from decision.decision_engine import DecisionEngine
from decision.models import TradeDecision
from core.logger import setup_logger

logger = setup_logger("TradingPipeline")


class TradingPipeline:
    """
    Wires Data -> Context -> Signal -> AI -> Decision into a single,
    runnable flow.

    Risk, Execution, Telegram, and Monitoring are intentionally not
    part of this pipeline (Phase 23.1+).
    """

    def __init__(self, symbol: str, interval: str, outputsize: int):
        self.symbol = symbol
        self.interval = interval
        self.outputsize = outputsize

        self.data_normalizer = MarketDataNormalizer()
        self.signal_engine = SignalEngine()
        self.ai_analyzer = AIAnalyzer()
        self.decision_engine = DecisionEngine()

    def run(self) -> dict:
        """
        Runs one full pipeline cycle: fetch candles, build context,
        generate signal candidates, evaluate each with the AI Analyzer,
        and produce a TradeDecision per candidate.
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

        return {
            "context": context,
            "signals": signal_candidates,
            "ai_results": ai_results,
            "decisions": decisions,
        }
