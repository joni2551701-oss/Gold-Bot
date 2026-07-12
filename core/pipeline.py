from typing import List

from data.market_data import MarketDataNormalizer
from context.context_orchestrator import build_context_snapshot
from signals.signal_engine import SignalEngine
from ai.ai_analyzer import AIAnalyzer, AIAnalysisResult
from core.logger import setup_logger

logger = setup_logger("TradingPipeline")


class TradingPipeline:
    """
    Wires Data -> Context -> Signal -> AI into a single, runnable flow.

    Decision, Risk, Execution, Telegram, and Monitoring are intentionally
    not part of this pipeline (Phase 23+).
    """

    def __init__(self, symbol: str, interval: str, outputsize: int):
        self.symbol = symbol
        self.interval = interval
        self.outputsize = outputsize

        self.data_normalizer = MarketDataNormalizer()
        self.signal_engine = SignalEngine()
        self.ai_analyzer = AIAnalyzer()

    def run(self) -> dict:
        """
        Runs one full pipeline cycle: fetch candles, build context,
        generate signal candidates, and evaluate each with the AI Analyzer.
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

        return {
            "context": context,
            "signals": signal_candidates,
            "ai_results": ai_results,
        }
