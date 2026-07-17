"""
AI Layer — Runtime Event Bus (Phase 61.6: AI Operations & Reliability
Foundation, TASK 5).

Genuinely new (Module Reuse Principle steps 1/2 both "no" — no
pub/sub mechanism exists anywhere in `ai/` today). Its entire purpose
is decoupling: `ai/runtime/ai_service.py`, `ai/providers/
circuit_breaker.py`, and `ai/runtime/runtime_manager.py` each publish
events about their own state without knowing who (if anyone) is
listening -- "Hech kim bir-birini to'g'ridan-to'g'ri chaqirmaydi" (no
module calls another directly) per the Director's own brief.

The eight event types are exactly the Director's own list -- no extra
event type invented, no event type omitted.

Phase 61.6 TASK 7: one additional event type, `RUNTIME_FAILED`, added
in place (extending this same enum, not a new bus/module) -- the
Runtime Notification Layer's own "Runtime FAILED" alert needs a signal
distinct from `RUNTIME_STOPPED` (a clean, intentional SHUTDOWN, not an
alarming condition). `ai.runtime.runtime_manager.RuntimeManager.
transition()` publishes it the same way it already publishes
`RUNTIME_STARTED`/`RUNTIME_STOPPED` -- one more branch on the same
existing `if/elif` block, no new orchestration logic.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from core.logger import setup_logger

logger = setup_logger("EventBus")


class EventType(Enum):
    PROVIDER_CHANGED = "ProviderChanged"
    PROVIDER_FAILED = "ProviderFailed"
    PROVIDER_RECOVERED = "ProviderRecovered"
    CACHE_HIT = "CacheHit"
    CACHE_MISS = "CacheMiss"
    VALIDATION_FAILED = "ValidationFailed"
    RUNTIME_STARTED = "RuntimeStarted"
    RUNTIME_STOPPED = "RuntimeStopped"
    RUNTIME_FAILED = "RuntimeFailed"


@dataclass(frozen=True)
class RuntimeEvent:
    """payload: free-form, event-type-specific detail (e.g. {"provider_name": "gemini"}) -- never trading data, never a signal/decision object."""
    event_type: EventType
    payload: Dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    """
    In-memory publish/subscribe, same "foundation, no persistence, no
    background thread" posture as every other Phase 61.x manager
    (`ai.session.session_manager.SessionManager`,
    `ai.providers.provider_health.ProviderHealthTracker`). `publish()`
    never raises, even if a subscribed handler does -- one bad
    subscriber must never break the publisher or any other subscriber.
    `history()` keeps every published event in-memory for inspection/
    testing (e.g. `/runtime_events`), same convention
    `core.emergency.emergency_manager.EmergencyManager`'s own
    transition history already uses.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[EventType, List[Callable[[RuntimeEvent], None]]] = {}
        self._history: List[RuntimeEvent] = []

    def subscribe(self, event_type: EventType, handler: Callable[[RuntimeEvent], None]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: RuntimeEvent) -> None:
        self._history.append(event)
        for handler in self._subscribers.get(event.event_type, []):
            try:
                handler(event)
            except Exception as e:
                logger.warning(f"EventBus subscriber failed for {event.event_type.value}: {e}")

    def history(self, event_type: Optional[EventType] = None) -> List[RuntimeEvent]:
        """All published events, oldest first -- optionally filtered to one event_type."""
        if event_type is None:
            return list(self._history)
        return [e for e in self._history if e.event_type == event_type]
