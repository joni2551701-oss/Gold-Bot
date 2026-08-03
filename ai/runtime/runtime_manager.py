"""
AI Layer — AI Runtime Manager (Phase 61.6: AI Operations & Reliability
Foundation, TASK 2).

`RuntimeManager` is the one holder of `AIService`'s own operational
state -- same "transition-validating state machine over an enum,
in-memory history" shape `core_layer.emergency.emergency_manager.
EmergencyManager` already established for a different domain. Every
transition is checked against `runtime_state.VALID_TRANSITIONS`
before it is applied; an invalid transition is rejected (returns
`None`, logs a warning) rather than silently corrupting the state.

Defaults to `RuntimeState.READY` on construction -- same "works out of
the box" convention `ai.providers.provider_manager.ProviderManager`/
`ai.providers.provider_health.ProviderHealthTracker` already use, so a
fresh `RuntimeManager()` (e.g. inside an Owner `/runtime` command,
which always constructs fresh -- see `platform_layer/telegram/owner/dashboard.py`)
reports a sensible default rather than a permanently-stuck
`INITIALIZING`. A caller that wants to model an explicit startup
sequence constructs with `initial_state=RuntimeState.INITIALIZING`
and calls `transition(RuntimeState.READY, ...)` itself.

`event_bus` is optional and injectable (same convention as every other
Phase 61.x manager's dependencies) -- when provided, a transition INTO
`READY` (from any other state) publishes `EventType.RUNTIME_STARTED`,
a transition into `SHUTDOWN` publishes `EventType.RUNTIME_STOPPED`,
and a transition into `FAILED` publishes `EventType.RUNTIME_FAILED`
(Phase 61.6 TASK 7 -- the Runtime Notification Layer's "Runtime
FAILED" alert reads this). Never wired into `core/pipeline.py`/
`decision/`/`risk/`/`execution/` (Rule 1) -- this is `ai/runtime/`'s
own operational self-awareness, nothing else reads or drives it this
phase.

Phase 61.7 TASK 7 (continuation session): every valid transition,
regardless of target state, additionally publishes the generic
`EventType.RUNTIME_STATE_CHANGED` -- for a subscriber that only cares
"did the state change at all," not which specific transition it was.
Published unconditionally, before the specific STARTED/STOPPED/FAILED
branches below (which still fire exactly as before, unchanged) -- not
a replacement for them.
"""

from typing import List, Optional

from ai.event_bus import EventBus, EventType, RuntimeEvent
from ai.runtime.runtime_events import RuntimeLifecycleEvent, create_lifecycle_event
from ai.runtime.runtime_state import RuntimeState, is_valid_transition
from core_layer.logger.logger import setup_logger

logger = setup_logger("RuntimeManager")


class RuntimeManager:
    def __init__(self, initial_state: RuntimeState = RuntimeState.READY, event_bus: Optional[EventBus] = None) -> None:
        self._state = initial_state
        self._event_bus = event_bus
        self._history: List[RuntimeLifecycleEvent] = [create_lifecycle_event(None, initial_state, reason="constructed")]

    def current_state(self) -> RuntimeState:
        return self._state

    def is_healthy(self) -> bool:
        """READY/BUSY/DEGRADED can all still serve requests -- FAILED/SHUTDOWN/INITIALIZING cannot."""
        return self._state in (RuntimeState.READY, RuntimeState.BUSY, RuntimeState.DEGRADED)

    def transition(self, to_state: RuntimeState, reason: Optional[str] = None) -> Optional[RuntimeLifecycleEvent]:
        """Never raises: an invalid transition is rejected (returns None, logs a warning) rather than applied."""
        if not is_valid_transition(self._state, to_state):
            logger.warning(f"Invalid runtime transition rejected: {self._state.value} -> {to_state.value}")
            return None

        previous_state = self._state
        event = create_lifecycle_event(previous_state, to_state, reason)
        self._history.append(event)
        self._state = to_state
        logger.info(f"Runtime transitioned: {previous_state.value} -> {to_state.value} (reason={reason})")

        if self._event_bus is not None:
            self._event_bus.publish(RuntimeEvent(
                event_type=EventType.RUNTIME_STATE_CHANGED,
                payload={"from_state": previous_state.value, "to_state": to_state.value, "reason": reason},
            ))
            if to_state == RuntimeState.READY and previous_state != RuntimeState.READY:
                self._event_bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STARTED, payload={"reason": reason}))
            elif to_state == RuntimeState.SHUTDOWN:
                self._event_bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_STOPPED, payload={"reason": reason}))
            elif to_state == RuntimeState.FAILED:
                self._event_bus.publish(RuntimeEvent(event_type=EventType.RUNTIME_FAILED, payload={"reason": reason, "from_state": previous_state.value}))

        return event

    def history(self) -> List[RuntimeLifecycleEvent]:
        return list(self._history)
