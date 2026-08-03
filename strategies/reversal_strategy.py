"""
Strategies — Reversal setup strategy (TASK-CORE-007, setup layer).

Reads the frozen context/ CHoCH events (counter-trend structural breaks)
and liquidity sweeps. A reversal setup is a CHoCH, strengthened when a
liquidity sweep of the opposite side preceded it (sweep-then-reverse).
Returns a StrategyResult; recomputes no structure, emits no signal.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus
from context_layer.market_structure.choch import ChochDirection
from context_layer.liquidity.liquidity import LiquidityType


class ReversalStrategy(SetupStrategy):
    def name(self) -> str:
        return "REVERSAL_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        choch_events = list(getattr(context, "choch_events", ()) or ())
        if not choch_events:
            return StrategyResult.none(self.name(), "no CHoCH (no character change)")

        event = max(choch_events, key=lambda e: e.index)
        bullish = event.direction == ChochDirection.BULLISH
        direction = StrategyDirection.LONG if bullish else StrategyDirection.SHORT

        # A confirming opposite-side sweep before the CHoCH strengthens it:
        # a bullish reversal wants a sell-side (SSL) sweep taken first.
        wanted_sweep = LiquidityType.SSL if bullish else LiquidityType.BSL
        sweeps = list(getattr(context, "liquidity_sweeps", ()) or ())
        confirming = next(
            (s for s in sweeps if s.type == wanted_sweep and s.index <= event.index),
            None,
        )
        confidence = 0.8 if confirming else 0.65
        level = event.broken_structure.swing.price

        reasons = [f"CHoCH {'bullish' if bullish else 'bearish'} at index {event.index}"]
        if confirming:
            reasons.append(f"preceded by {wanted_sweep.value} sweep at index {confirming.index}")

        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=confidence,
            entry_zone=(level, level),
            invalidation=confirming.sweep_price if confirming else level,
            reasons=reasons,
            status=SetupStatus.SETUP_FOUND,
            metadata={"choch_index": event.index, "sweep_confirmed": confirming is not None},
        )
