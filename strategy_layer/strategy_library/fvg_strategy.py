from typing import List
from context_layer.context_engine.context_orchestrator import ContextSnapshot
from context_layer.fair_value_gap.fvg import FvgType
from signal_layer.signal_builder.models import SignalCandidate, SignalType


class StrategyConfig:
    FVG_BOS_WINDOW = 15


class FVGStrategy:
    """
    Analyzes FVG formations confirmed by structural delivery (BOS/CHoCH).
    Stateless and read-only.
    """

    def analyze(self, context: ContextSnapshot) -> List[SignalCandidate]:
        candidates: List[SignalCandidate] = []

        if not context.fair_value_gaps:
            return candidates

        latest_fvg = context.fair_value_gaps[-1]
        if latest_fvg.filled:
            return candidates

        is_bullish = latest_fvg.type == FvgType.BULLISH

        structural_events = list(context.bos_events) + list(context.choch_events)

        for structural_event in structural_events:
            if abs(structural_event.index - latest_fvg.index) <= StrategyConfig.FVG_BOS_WINDOW:

                s_type = SignalType.BUY if is_bullish else SignalType.SELL

                entry = (latest_fvg.top + latest_fvg.bottom) / 2
                stop_loss = latest_fvg.bottom if is_bullish else latest_fvg.top
                take_profit = structural_event.broken_structure.swing.price

                candidates.append(SignalCandidate(
                    signal_type=s_type,
                    entry=entry,
                    stop_loss=stop_loss,
                    take_profit=take_profit,
                    strategy_name="FVG_STRATEGY",
                    confidence=0.70,
                    reasons=[f"FVG at {latest_fvg.index} confirmed by structure at {structural_event.index}"]
                ))
                break

        return candidates


# --- Setup layer (TASK-CORE-007) --------------------------------------------
# Additive: reuses the frozen FVGStrategy.analyze() detection above.
from strategy_layer.strategy_engine.base import SetupStrategy  # noqa: E402
from strategy_layer.strategy_engine.result import StrategyResult  # noqa: E402


class FVGSetupStrategy(SetupStrategy):
    """Setup-layer view over the frozen FVGStrategy."""

    def __init__(self) -> None:
        self._inner = FVGStrategy()

    def name(self) -> str:
        return "FVG_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard
        try:
            candidates = self._inner.analyze(context)
        except AttributeError:
            return StrategyResult.none(self.name(), "context missing fields for FVG")
        if not candidates:
            return StrategyResult.none(self.name(), "no FVG setup")
        return StrategyResult.from_signal_candidate(candidates[0], strategy_name=self.name())
