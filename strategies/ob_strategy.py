"""
Strategies — Order Block setup strategy (TASK-CORE-007, setup layer).

Reads the frozen context/ order blocks (context.order_block.
detect_order_blocks output). An OB retest/rejection setup: the latest
order block defines a zone and a direction; if the latest price is at or
inside that zone it is a retest. Returns a StrategyResult; recomputes no
structure, emits no signal.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus
from context_layer.order_block.order_block import OrderBlockType


class OBStrategy(SetupStrategy):
    def name(self) -> str:
        return "ORDER_BLOCK_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        order_blocks = list(getattr(context, "order_blocks", ()) or ())
        if not order_blocks:
            return StrategyResult.none(self.name(), "no order blocks")

        ob = max(order_blocks, key=lambda o: o.index)
        bullish = ob.type == OrderBlockType.BULLISH
        direction = StrategyDirection.LONG if bullish else StrategyDirection.SHORT

        price = self._last_price(context)
        at_zone = price is not None and ob.low <= price <= ob.high
        confidence = 0.68 if at_zone else 0.55
        state = "retest (price at OB)" if at_zone else "pending retest"

        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=confidence,
            entry_zone=(ob.low, ob.high),
            invalidation=ob.low if bullish else ob.high,
            reasons=[f"{'bullish' if bullish else 'bearish'} order block @ index {ob.index}, {state}"],
            status=SetupStatus.SETUP_FOUND,
            metadata={"ob_index": ob.index, "at_zone": at_zone},
        )
