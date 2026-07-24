"""
AI Layer — AI Runtime State Model (Phase 61.6: AI Operations &
Reliability Foundation, TASK 2).

A dedicated vocabulary for `AIService`'s own operational lifecycle --
distinct from `ai.providers.provider_status.HealthStatus` (one
provider's observed health) and `ai.providers.provider_manager.
ProviderStatus` (one provider's owner-set intent). This enum describes
the AI runtime as a whole, the same "process-wide state, not a single
component's state" role `core.emergency.emergency_state.EmergencyState`
plays for the emergency layer.

Foundation only: nothing in `core/pipeline.py`, `decision/`, `risk/`,
or `execution/` reads this module (Rule 1) -- constructing a
`RuntimeStateRecord` changes no trading behavior anywhere.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class RuntimeState(Enum):
    """
    INITIALIZING: the runtime has been constructed but has not yet
        confirmed it is ready to serve requests.
    READY: normal operating state -- able to serve requests.
    BUSY: actively serving a request right now (a transient state a
        caller may set around a single ask() call; optional to use).
    DEGRADED: still able to serve requests, but under a known-reduced
        posture (e.g. a provider circuit is OPEN, cache disabled).
    FAILED: unable to serve requests -- every provider unavailable, or
        an unrecoverable internal error. Recoverable back to READY.
    SHUTDOWN: terminal -- the runtime has been deliberately stopped.
        No further transition is valid out of this state.
    """
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    BUSY = "BUSY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    SHUTDOWN = "SHUTDOWN"


# The valid transition graph -- same "enforce the rule in data, not
# just the docstring" posture ai/cache/cache_policy.py's CacheKey
# already uses. SHUTDOWN has no outgoing edges (terminal).
VALID_TRANSITIONS = {
    RuntimeState.INITIALIZING: frozenset({RuntimeState.READY, RuntimeState.FAILED}),
    RuntimeState.READY: frozenset({RuntimeState.BUSY, RuntimeState.DEGRADED, RuntimeState.FAILED, RuntimeState.SHUTDOWN}),
    RuntimeState.BUSY: frozenset({RuntimeState.READY, RuntimeState.DEGRADED, RuntimeState.FAILED}),
    RuntimeState.DEGRADED: frozenset({RuntimeState.READY, RuntimeState.FAILED, RuntimeState.SHUTDOWN}),
    RuntimeState.FAILED: frozenset({RuntimeState.READY, RuntimeState.SHUTDOWN}),
    RuntimeState.SHUTDOWN: frozenset(),
}


def is_valid_transition(from_state: RuntimeState, to_state: RuntimeState) -> bool:
    """Never raises: an unknown from_state (impossible with the enum, defensive anyway) has no valid transitions."""
    return to_state in VALID_TRANSITIONS.get(from_state, frozenset())


@dataclass(frozen=True)
class RuntimeStateRecord:
    """An immutable snapshot of the runtime's current state -- not a mutable holder (runtime_manager.py's RuntimeManager is the holder), same convention as core.emergency.emergency_state.EmergencyStateRecord."""
    state: RuntimeState
    reason: Optional[str] = None
    changed_at: Optional[datetime] = None
