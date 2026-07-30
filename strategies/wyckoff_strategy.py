"""
Strategies — Wyckoff setup strategy (TASK-CORE-007, setup layer).

Reads the frozen context/ Wyckoff events (context.wyckoff.
detect_wyckoff_events output). A SPRING (Accumulation) is a bullish
setup, an UPTHRUST (Distribution) a bearish one. Returns a
StrategyResult; recomputes no structure, emits no signal.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus
from context.wyckoff import WyckoffEventType


class WyckoffStrategy(SetupStrategy):
    def name(self) -> str:
        return "WYCKOFF_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        events = list(getattr(context, "wyckoff_events", ()) or ())
        if not events:
            return StrategyResult.none(self.name(), "no Wyckoff Spring/Upthrust")

        event = max(events, key=lambda e: e.index)
        is_spring = event.type == WyckoffEventType.SPRING
        direction = StrategyDirection.LONG if is_spring else StrategyDirection.SHORT
        phase = getattr(getattr(event, "phase", None), "value", None)
        sweep_price = getattr(getattr(event, "sweep", None), "sweep_price", None)

        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=0.7,
            entry_zone=(sweep_price, sweep_price) if sweep_price is not None else None,
            invalidation=sweep_price,
            reasons=[f"{event.type.value} ({phase}) confirmed at index {event.index}"],
            status=SetupStatus.SETUP_FOUND,
            metadata={"wyckoff_type": event.type.value, "phase": phase, "index": event.index},
        )
