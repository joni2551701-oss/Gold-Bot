from typing import List
from context.context_orchestrator import ContextSnapshot
from context.amd import AmdEventType
from signals.models import SignalCandidate, SignalType


class StrategyConfig:
    AMD_CONFIRMATION_WINDOW = 20


class AMDStrategy:
    """
    Analyzes AMD cycles. Correlates Distribution with structural
    Order Block or FVG footprints.
    """

    def analyze(self, context: ContextSnapshot) -> List[SignalCandidate]:
        candidates: List[SignalCandidate] = []

        if not context.amd_events:
            return candidates

        for amd in reversed(context.amd_events):
            if amd.type == AmdEventType.DISTRIBUTION:

                struct_events = list(context.bos_events) + list(context.choch_events)
                valid_break = next((se for se in struct_events if abs(se.index - amd.index) <= StrategyConfig.AMD_CONFIRMATION_WINDOW), None)

                if not valid_break:
                    continue

                confirming_ob = next((ob for ob in context.order_blocks if abs(ob.index - amd.index) <= StrategyConfig.AMD_CONFIRMATION_WINDOW), None)
                confirming_fvg = next((fvg for fvg in context.fair_value_gaps if abs(fvg.index - amd.index) <= StrategyConfig.AMD_CONFIRMATION_WINDOW), None)

                footprint = confirming_ob or confirming_fvg
                if footprint:
                    s_type = SignalType.BUY if amd.is_bullish else SignalType.SELL

                    if hasattr(footprint, 'high'):
                        entry = (footprint.high + footprint.low) / 2
                        stop_loss = footprint.low if amd.is_bullish else footprint.high
                    else:
                        entry = (footprint.top + footprint.bottom) / 2
                        stop_loss = footprint.bottom if amd.is_bullish else footprint.top

                    candidates.append(SignalCandidate(
                        signal_type=s_type,
                        entry=entry,
                        stop_loss=stop_loss,
                        take_profit=valid_break.broken_structure.swing.price,
                        strategy_name="AMD_STRATEGY",
                        confidence=0.85,
                        reasons=[f"AMD Distribution at {amd.index} confirmed by {type(footprint).__name__} at {footprint.index}"]
                    ))
                    break

        return candidates


# --- Setup layer (TASK-CORE-007) --------------------------------------------
# Additive: reuses the frozen AMDStrategy.analyze() detection above and
# adapts its first SignalCandidate into a StrategyResult. No detection
# logic is duplicated; the live SignalCandidate path is untouched.
from strategies.base import SetupStrategy  # noqa: E402
from strategies.result import StrategyResult  # noqa: E402


class AMDSetupStrategy(SetupStrategy):
    """Setup-layer view over the frozen AMDStrategy."""

    def __init__(self) -> None:
        self._inner = AMDStrategy()

    def name(self) -> str:
        return "AMD_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard
        try:
            candidates = self._inner.analyze(context)
        except AttributeError:
            return StrategyResult.none(self.name(), "context missing fields for AMD")
        if not candidates:
            return StrategyResult.none(self.name(), "no AMD distribution setup")
        return StrategyResult.from_signal_candidate(candidates[0], strategy_name=self.name())
