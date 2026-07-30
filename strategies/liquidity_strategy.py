from typing import List
from context.context_orchestrator import ContextSnapshot
from context.bos import BosDirection
from signals.models import SignalCandidate, SignalType


class LiquidityStrategy:
    """
    Analyzes Liquidity Sweeps in relation to structural BOS and Order Blocks.
    Stateless and read-only.
    """

    def analyze(self, context: ContextSnapshot) -> List[SignalCandidate]:
        candidates: List[SignalCandidate] = []

        if not context.liquidity_sweeps or not context.bos_events:
            return candidates

        latest_sweep = context.liquidity_sweeps[-1]

        for bos in context.bos_events:
            if bos.index > latest_sweep.index:
                relevant_ob = None
                for ob in context.order_blocks:
                    if abs(ob.index - latest_sweep.index) <= 5:
                        relevant_ob = ob
                        break

                if relevant_ob:
                    s_type = (
                        SignalType.BUY
                        if bos.direction == BosDirection.BULLISH
                        else SignalType.SELL
                    )

                    entry = (relevant_ob.high + relevant_ob.low) / 2
                    stop_loss = latest_sweep.sweep_price
                    take_profit = bos.broken_structure.swing.price

                    candidates.append(SignalCandidate(
                        signal_type=s_type,
                        entry=entry,
                        stop_loss=stop_loss,
                        take_profit=take_profit,
                        strategy_name="LIQUIDITY_SWEEP_STRATEGY",
                        confidence=0.75,
                        reasons=[f"Sweep at {latest_sweep.index} confirmed by BOS at {bos.index}"]
                    ))
                    break

        return candidates


# --- Setup layer (TASK-CORE-007) --------------------------------------------
# Additive: reuses the frozen LiquidityStrategy.analyze() detection above.
from strategies.base import SetupStrategy  # noqa: E402
from strategies.result import StrategyResult  # noqa: E402


class LiquiditySetupStrategy(SetupStrategy):
    """Setup-layer view over the frozen LiquidityStrategy."""

    def __init__(self) -> None:
        self._inner = LiquidityStrategy()

    def name(self) -> str:
        return "LIQUIDITY_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard
        try:
            candidates = self._inner.analyze(context)
        except AttributeError:
            return StrategyResult.none(self.name(), "context missing fields for liquidity")
        if not candidates:
            return StrategyResult.none(self.name(), "no liquidity sweep setup")
        return StrategyResult.from_signal_candidate(candidates[0], strategy_name=self.name())
