"""
signal_layer/signal_engine/lifecycle/ — canonical signal build/publish lifecycle (STEP-08).

See signal_layer/signal_engine/lifecycle/state.py for the CanonicalSignalStatus state machine
and how it differs from lifecycle/signal_state.py and
execution_layer/execution_monitor/signal_lifecycle.py.
"""

from signal_layer.signal_engine.lifecycle.state import (
    CanonicalSignalStatus,
    SignalStatusTransitionResult,
    transition,
    is_terminal,
    ALLOWED_TRANSITIONS,
)

__all__ = [
    "CanonicalSignalStatus",
    "SignalStatusTransitionResult",
    "transition",
    "is_terminal",
    "ALLOWED_TRANSITIONS",
]
