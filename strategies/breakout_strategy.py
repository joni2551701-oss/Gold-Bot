"""
Strategies — Breakout / failed-breakout setup strategy (TASK-CORE-007, setup layer).

Reads the frozen context/ liquidity sweeps and structural breaks.
- Range breakout: a liquidity sweep followed by a same-direction BOS
  (the break holds) -> continuation.
- Failed breakout: a liquidity sweep with no confirming break (price
  swept a level and closed back) -> reversal against the swept side.
Returns a StrategyResult; recomputes no structure, emits no signal.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus
from context_layer.liquidity.liquidity import LiquidityType
from context_layer.market_structure.bos import BosDirection


class BreakoutStrategy(SetupStrategy):
    def name(self) -> str:
        return "BREAKOUT_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        sweeps = list(getattr(context, "liquidity_sweeps", ()) or ())
        if not sweeps:
            return StrategyResult.none(self.name(), "no liquidity sweep to break/fail")

        sweep = max(sweeps, key=lambda s: s.index)
        bos_events = list(getattr(context, "bos_events", ()) or ())

        # A sell-side (SSL) sweep breaking up wants a bullish BOS after it.
        wanted = BosDirection.BULLISH if sweep.type == LiquidityType.SSL else BosDirection.BEARISH
        confirming = next((b for b in bos_events if b.direction == wanted and b.index > sweep.index), None)

        if confirming:
            direction = StrategyDirection.LONG if wanted == BosDirection.BULLISH else StrategyDirection.SHORT
            return StrategyResult(
                strategy_name=self.name(),
                direction=direction,
                confidence=0.72,
                entry_zone=(sweep.sweep_price, sweep.sweep_price),
                invalidation=sweep.sweep_price,
                reasons=[f"range breakout: {sweep.type.value} sweep @ {sweep.index} held by BOS @ {confirming.index}"],
                status=SetupStatus.SETUP_FOUND,
                metadata={"sweep_index": sweep.index, "kind": "breakout"},
            )

        # No confirming break -> failed breakout, reverse against the swept side.
        direction = StrategyDirection.LONG if sweep.type == LiquidityType.SSL else StrategyDirection.SHORT
        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=0.6,
            entry_zone=(sweep.sweep_price, sweep.sweep_price),
            invalidation=sweep.sweep_price,
            reasons=[f"failed breakout: {sweep.type.value} sweep @ {sweep.index} with no confirming break"],
            status=SetupStatus.SETUP_FOUND,
            metadata={"sweep_index": sweep.index, "kind": "failed_breakout"},
        )
