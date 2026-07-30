"""
Decision — STEP-09 status vocabulary (TASK-CORE-009).

DecisionStatus is the STEP-09 business-decision verdict over a canonical
signal: APPROVE / REJECT / HOLD / EXPIRE.

Additive-parallel + reuse-first (Director decision): the live, FROZEN
decision.models.DecisionAction (APPROVE / REJECT / NO_TRADE) produced by
decision.decision_engine.DecisionEngine.evaluate() is untouched. STEP-09
does NOT re-derive the confidence-blend; it REUSES that verdict and maps it
into this richer vocabulary — NO_TRADE becomes HOLD (both mean "no trade now,
but not a hard reject"), and EXPIRE is a new, time-based status STEP-09's own
rules add (a stale canonical signal), which the frozen engine has no concept
of. See docs/PHASE_DECISION.md for the full mapping table.

No risk sizing, no order, no analysis here — only the verdict vocabulary and
the mappings onto it.
"""

from enum import Enum
from typing import Optional

from decision.models import DecisionAction


class DecisionStatus(str, Enum):
    """STEP-09 business verdict over a canonical signal."""
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    HOLD = "HOLD"
    EXPIRE = "EXPIRE"


# Frozen DecisionAction.value -> STEP-09 status. NO_TRADE -> HOLD: the frozen
# engine's "no trade this cycle" is a hold, not a hard reject.
_ACTION_TO_STATUS = {
    "APPROVE": DecisionStatus.APPROVE,
    "REJECT": DecisionStatus.REJECT,
    "NO_TRADE": DecisionStatus.HOLD,
}

# signals.schema.SignalSchema.decision vocabulary (APPROVED/REJECTED/PENDING)
# -> STEP-09 status. PENDING -> HOLD (decision hasn't concluded yet).
_SIGNAL_DECISION_TO_STATUS = {
    "APPROVED": DecisionStatus.APPROVE,
    "REJECTED": DecisionStatus.REJECT,
    "PENDING": DecisionStatus.HOLD,
}


def from_decision_action(action) -> DecisionStatus:
    """
    Map the FROZEN DecisionAction (or its .value) onto DecisionStatus — the
    reuse point that lets STEP-09 build on the engine's verdict instead of
    recomputing it. Unknown -> HOLD. Never raises.
    """
    value = getattr(action, "value", action)
    if isinstance(action, DecisionAction):
        value = action.value
    return _ACTION_TO_STATUS.get(value, DecisionStatus.HOLD)


def from_signal_decision(decision: Optional[str]) -> DecisionStatus:
    """Map a canonical signal's own decision string (APPROVED/REJECTED/PENDING) onto DecisionStatus. Unknown/None -> HOLD."""
    if not decision:
        return DecisionStatus.HOLD
    return _SIGNAL_DECISION_TO_STATUS.get(decision.upper(), DecisionStatus.HOLD)
