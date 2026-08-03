"""
Strategies — Session setup strategy (TASK-CORE-007, setup layer).

Reads the frozen context/ session events (context.session.Session). A
"killzone" session (London / New York / their overlap) is where SMC
setups are conventionally sought; the setup gains confluence when a
structural break (BOS/CHoCH) coincides with the killzone. Direction is
taken from that structural break, else NEUTRAL. Returns a StrategyResult;
recomputes no structure, emits no signal.
"""

from strategy_layer.strategy_engine.base import SetupStrategy
from strategy_layer.strategy_engine.result import StrategyResult, StrategyDirection, SetupStatus

_KILLZONES = {"LONDON", "NEW_YORK", "LONDON_NEW_YORK_OVERLAP"}


class SessionStrategy(SetupStrategy):
    def name(self) -> str:
        return "SESSION_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        session_events = list(getattr(context, "session_events", ()) or ())
        if not session_events:
            return StrategyResult.none(self.name(), "no session data")

        current = session_events[-1]
        session_name = getattr(getattr(current, "session", None), "value", None)
        if session_name not in _KILLZONES:
            return StrategyResult.none(self.name(), f"outside killzone (session {session_name})",
                                       session=session_name)

        # Confluence: a structural break lends the killzone a direction.
        bos_events = list(getattr(context, "bos_events", ()) or ())
        choch_events = list(getattr(context, "choch_events", ()) or ())
        events = bos_events + choch_events
        direction = StrategyDirection.NEUTRAL
        confidence = 0.5
        reasons = [f"killzone session: {session_name}"]
        if events:
            latest = max(events, key=lambda e: e.index)
            dir_val = getattr(getattr(latest, "direction", None), "value", None)
            if dir_val == "BULLISH":
                direction = StrategyDirection.LONG
            elif dir_val == "BEARISH":
                direction = StrategyDirection.SHORT
            confidence = 0.65
            reasons.append(f"confluence with structural break @ index {latest.index}")

        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=confidence,
            reasons=reasons,
            status=SetupStatus.SETUP_FOUND,
            metadata={"session": session_name},
        )
