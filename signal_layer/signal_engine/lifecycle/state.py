"""
Signals — Canonical Signal build/publish lifecycle (TASK-CORE-008 / STEP-08).

Names the stages a canonical signal passes through *inside the signals/
layer* while it is being assembled and made ready for consumers:

    CREATED -> VALIDATED -> ENRICHED -> READY -> PUBLISHED
                                          └-> EXPIRED / CANCELLED

NAMING NOTE — read before using: this is deliberately a DIFFERENT concept
from lifecycle/signal_state.py's SignalLifecycleState (Phase 59), which
tracks a signal's *analysis/decision* journey (CREATED -> QUALITY_CHECKED ->
EXPLAINED -> APPROVED/REJECTED -> PAPER_OPEN -> CLOSED), and from
execution_layer/execution_monitor/signal_lifecycle.py's SignalState (Telegram message delivery).
CanonicalSignalStatus tracks only the signals/-layer *build-and-publish*
progress of the canonical payload — validated? enriched? ready to hand to a
consumer? published? — never the decision or the trade outcome. The three
concepts live in three packages under three distinct names on purpose, the
same disambiguation discipline the codebase already applies elsewhere.

This module is a pure, standalone transition validator. It holds no state,
persists nothing, and is not auto-wired into core/pipeline.py.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple


class CanonicalSignalStatus(Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    ENRICHED = "ENRICHED"
    READY = "READY"
    PUBLISHED = "PUBLISHED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


# PUBLISHED/EXPIRED/CANCELLED are terminal. A signal can be CANCELLED from any
# pre-terminal stage; EXPIRED applies once it is READY/PUBLISHED but no longer
# actionable. The happy path is CREATED->VALIDATED->ENRICHED->READY->PUBLISHED.
ALLOWED_TRANSITIONS: Dict[CanonicalSignalStatus, Tuple[CanonicalSignalStatus, ...]] = {
    CanonicalSignalStatus.CREATED: (
        CanonicalSignalStatus.VALIDATED,
        CanonicalSignalStatus.CANCELLED,
    ),
    CanonicalSignalStatus.VALIDATED: (
        CanonicalSignalStatus.ENRICHED,
        CanonicalSignalStatus.CANCELLED,
    ),
    CanonicalSignalStatus.ENRICHED: (
        CanonicalSignalStatus.READY,
        CanonicalSignalStatus.CANCELLED,
    ),
    CanonicalSignalStatus.READY: (
        CanonicalSignalStatus.PUBLISHED,
        CanonicalSignalStatus.EXPIRED,
        CanonicalSignalStatus.CANCELLED,
    ),
    CanonicalSignalStatus.PUBLISHED: (
        CanonicalSignalStatus.EXPIRED,
    ),
    CanonicalSignalStatus.EXPIRED: (),
    CanonicalSignalStatus.CANCELLED: (),
}


@dataclass(frozen=True)
class SignalStatusTransitionResult:
    """Never raises — an invalid transition returns success=False + reason."""
    success: bool
    reason: str


def transition(
    current: CanonicalSignalStatus,
    next_state: CanonicalSignalStatus,
) -> SignalStatusTransitionResult:
    """Validate one step of ALLOWED_TRANSITIONS. Pure — mutates nothing."""
    if next_state in ALLOWED_TRANSITIONS.get(current, ()):
        return SignalStatusTransitionResult(success=True, reason="")
    return SignalStatusTransitionResult(
        success=False,
        reason=f"{current.value} -> {next_state.value} is not an allowed transition",
    )


def is_terminal(state: CanonicalSignalStatus) -> bool:
    """True when no further transition is possible."""
    return len(ALLOWED_TRANSITIONS.get(state, ())) == 0
