from typing import List
from context.context_orchestrator import ContextSnapshot
from signals.models import SignalCandidate
from strategies.liquidity_strategy import LiquidityStrategy
from strategies.fvg_strategy import FVGStrategy
from strategies.amd_strategy import AMDStrategy


class StrategyManager:
    """
    Orchestrates the execution of all registered trading strategies.
    Aggregates candidates from disparate SMC methodologies into a
    unified list for the Signal Engine.
    """

    def __init__(self):
        self.strategies = [
            LiquidityStrategy(),
            FVGStrategy(),
            AMDStrategy(),
        ]

    def run_all_strategies(self, context: ContextSnapshot) -> List[SignalCandidate]:
        """
        Executes all registered strategies against the provided ContextSnapshot.
        Aggregation is performed linearly.
        """
        all_candidates: List[SignalCandidate] = []

        for strategy in self.strategies:
            candidates = strategy.analyze(context)
            all_candidates.extend(candidates)

        return all_candidates
