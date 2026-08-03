from typing import List
from context_layer.context_engine.context_orchestrator import ContextSnapshot
from signal_layer.signal_builder.models import SignalCandidate
from strategy_layer.strategy_manager.strategy_manager import StrategyManager


class SignalEngine:
    """
    High-level router for signal generation.
    Orchestrates the strategy execution pipeline by consuming
    an immutable ContextSnapshot and aggregating strategy results.
    """

    def __init__(self):
        self.strategy_manager = StrategyManager()

    def generate_signals(self, context: ContextSnapshot) -> List[SignalCandidate]:
        """
        Consumes context snapshot and routes to strategy manager.
        Purely functional/stateless regarding market data.
        """
        # The engine acts as the interface for downstream AI/Decision layers
        return self.strategy_manager.run_all_strategies(context)
