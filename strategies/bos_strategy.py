"""
Strategies — BOS / CHoCH setup strategy (TASK-CORE-007, setup layer).

Reads the frozen context/ BOS and CHoCH events (context.bos.detect_bos /
context.choch.detect_choch output). A BOS is a trend-continuation break;
a CHoCH is a counter-trend reversal break. Returns a StrategyResult;
computes no structure, emits no signal.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus
from context.bos import BosDirection
from context.choch import ChochDirection


class BOSStrategy(SetupStrategy):
    def name(self) -> str:
        return "BOS_CHOCH_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        bos_events = list(getattr(context, "bos_events", ()) or ())
        choch_events = list(getattr(context, "choch_events", ()) or ())
        if not bos_events and not choch_events:
            return StrategyResult.none(self.name(), "no BOS/CHoCH events")

        latest_bos = max(bos_events, key=lambda e: e.index) if bos_events else None
        latest_choch = max(choch_events, key=lambda e: e.index) if choch_events else None

        # The most recent structural break decides the setup type.
        use_choch = latest_choch is not None and (
            latest_bos is None or latest_choch.index >= latest_bos.index
        )
        event = latest_choch if use_choch else latest_bos
        kind = "reversal (CHoCH)" if use_choch else "continuation (BOS)"

        if use_choch:
            direction = StrategyDirection.LONG if event.direction == ChochDirection.BULLISH else StrategyDirection.SHORT
        else:
            direction = StrategyDirection.LONG if event.direction == BosDirection.BULLISH else StrategyDirection.SHORT

        level = event.broken_structure.swing.price
        confidence = 0.7 if use_choch else 0.75

        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=confidence,
            entry_zone=(level, level),
            invalidation=level,
            reasons=[f"{kind} at index {event.index}, broken structure @ {level}"],
            status=SetupStatus.SETUP_FOUND,
            metadata={"break_index": event.index, "kind": "choch" if use_choch else "bos"},
        )
