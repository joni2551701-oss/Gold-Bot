"""
signals/lifecycle/ — canonical signal build/publish lifecycle (STEP-08).

See signals/lifecycle/state.py for the CanonicalSignalStatus state machine
and how it differs from lifecycle/signal_state.py and
execution/signal_lifecycle.py.
"""

from signals.lifecycle.state import (
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
