"""
AI Layer — AI Runtime Lifecycle Events (Phase 61.6: AI Operations &
Reliability Foundation, TASK 2).

`RuntimeLifecycleEvent` is the record `runtime_manager.py`'s
`RuntimeManager` appends to its own in-memory history on every state
transition -- distinct from `ai_layer/ai_service/event_bus.py`'s
`RuntimeEvent`/`EventType` (TASK 5), which is a general-purpose
cross-cutting pub/sub carrying `RuntimeStarted`/`RuntimeStopped` (among
six other event types) to any subscriber. `RuntimeManager` is the one
place both concepts meet: every transition is recorded here (for
`/runtime_events`-style inspection of "how did the runtime get to this
state"), and a transition into `READY` for the first time / into
`SHUTDOWN` additionally publishes onto the `EventBus` via an
injectable, optional dependency -- see `runtime_manager.py`.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from ai_layer.ai_engine.runtime.runtime_state import RuntimeState


@dataclass(frozen=True)
class RuntimeLifecycleEvent:
    from_state: Optional[RuntimeState]
    to_state: RuntimeState
    reason: Optional[str]
    occurred_at: datetime


def create_lifecycle_event(
    from_state: Optional[RuntimeState], to_state: RuntimeState, reason: Optional[str] = None,
) -> RuntimeLifecycleEvent:
    """Pure, deterministic factory -- stamps occurred_at to now, same convention as core_layer.emergency.emergency_state.create_emergency_state_record()."""
    return RuntimeLifecycleEvent(
        from_state=from_state, to_state=to_state, reason=reason, occurred_at=datetime.now(timezone.utc),
    )
