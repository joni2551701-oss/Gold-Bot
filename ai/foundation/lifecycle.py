"""
AI Foundation — Lifecycle State (TASK-AI-001: AI Foundation Activation).

A transition-validated lifecycle state machine every Foundation
component and the `AIManager` itself move through:

    CREATED -> INITIALIZED -> STARTED <-> STOPPED -> SHUTDOWN
                    |             |          |
                    +-------------+----------+--> FAILED --> SHUTDOWN

Reuse-First note: this reuses, *by pattern*, the transition-validated
state model already proven in `ai/runtime/runtime_state.py`
(`RuntimeState` + `is_valid_transition`). It is deliberately not an
import of that module: TASK-AI-001's dependency rule confines the
Foundation to depending only on other `ai/foundation/` modules and
stdlib, and `ai/runtime/` transitively imports `core.logger`, which
the Foundation->Core prohibition forbids. So the Foundation owns its
own, dependency-free lifecycle vocabulary. No business logic here.
"""

from enum import Enum
from typing import Dict, Set


class LifecycleState(Enum):
    CREATED = "CREATED"
    INITIALIZED = "INITIALIZED"
    STARTED = "STARTED"
    STOPPED = "STOPPED"
    SHUTDOWN = "SHUTDOWN"
    FAILED = "FAILED"


_VALID_TRANSITIONS: Dict[LifecycleState, Set[LifecycleState]] = {
    LifecycleState.CREATED: {LifecycleState.INITIALIZED, LifecycleState.FAILED},
    LifecycleState.INITIALIZED: {
        LifecycleState.STARTED,
        LifecycleState.SHUTDOWN,
        LifecycleState.FAILED,
    },
    LifecycleState.STARTED: {
        LifecycleState.STOPPED,
        LifecycleState.SHUTDOWN,
        LifecycleState.FAILED,
    },
    LifecycleState.STOPPED: {
        LifecycleState.STARTED,
        LifecycleState.SHUTDOWN,
        LifecycleState.FAILED,
    },
    LifecycleState.SHUTDOWN: set(),
    LifecycleState.FAILED: {LifecycleState.SHUTDOWN},
}


def is_valid_transition(current: LifecycleState, target: LifecycleState) -> bool:
    """Never raises: an unknown/terminal current state simply reports no valid transition."""
    return target in _VALID_TRANSITIONS.get(current, set())
