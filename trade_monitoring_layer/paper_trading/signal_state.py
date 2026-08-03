"""
Lifecycle Layer — Signal Lifecycle State (Phase 59 Preparation, TASK 4:
Signal Lifecycle Audit).

After Phase A15 (Signal Schema) and A16 (Context Snapshot), a signal's
own shape is standard, but its *life* -- which stages it has passed
through -- was never written down as an explicit state machine. This
module names the flow and validates transitions between its states; it
does not change how a signal is generated, graded, explained, or
decided -- see "What this module does NOT do" below.

    CREATED -> QUALITY_CHECKED -> EXPLAINED -> APPROVED / REJECTED -> PAPER_OPEN -> CLOSED

NAMING NOTE -- read before using this module: execution_layer/execution_monitor/signal_lifecycle.py
already defines a class named SignalState (CREATED/SENT/ACKNOWLEDGED/
CLOSED) -- a Telegram message-delivery state machine, inert, unrelated
to a signal's own analysis-pipeline progress (SENT/ACKNOWLEDGED both
describe what happened to the *Telegram message*, not the signal's
quality/explanation/decision journey). This module's enum is
deliberately named SignalLifecycleState, not SignalState, to avoid a
same-name collision between two different concepts in two different
packages -- the same disambiguation discipline
context_layer/context_engine/snapshot.py's ContextSnapshotSchema (vs. the real
ContextSnapshot) and trade_monitoring_layer/paper_trading/paper_trade.py (vs.
execution_layer/execution_monitor/signal_lifecycle.py's own SignalState) already established.
execution_layer/execution_monitor/signal_lifecycle.py is untouched by this phase.

What this module does NOT do:
- Does not change signal_layer/signal_scoring/signal_quality.py, signal_layer/signal_scoring/explainability.py,
  or decision_layer/decision_engine/decision_engine.py -- their outputs are only *read* by
  derive_signal_lifecycle_state() below, never recomputed.
- Does not add a new field to signals.schema.SignalSchema, and does
  not persist anything -- no database change.
- Does not enforce transitions automatically anywhere in
  core/pipeline.py -- this is a standalone validator, not wired into
  the live pipeline in this phase.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple, TYPE_CHECKING

from trade_monitoring_layer.paper_trading.trade_state import TradeState

if TYPE_CHECKING:
    from trade_monitoring_layer.paper_trading.paper_trade import PaperTrade
    from signal_layer.signal_builder.schema import SignalSchema


class SignalLifecycleState(Enum):
    CREATED = "CREATED"
    QUALITY_CHECKED = "QUALITY_CHECKED"
    EXPLAINED = "EXPLAINED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PAPER_OPEN = "PAPER_OPEN"
    CLOSED = "CLOSED"


# REJECTED and CLOSED are terminal -- an empty tuple means "no further
# transition is valid." APPROVED branches to PAPER_OPEN only (a
# REJECTED signal never opens a paper trade); EXPLAINED branches to
# either APPROVED or REJECTED, mirroring Decision Engine's own
# real APPROVE/REJECT/NO_TRADE outcomes collapsed onto SignalSchema's
# APPROVED/REJECTED vocabulary (see docs/SIGNAL_SCHEMA.md's "Decision
# status mapping").
ALLOWED_TRANSITIONS: Dict[SignalLifecycleState, Tuple[SignalLifecycleState, ...]] = {
    SignalLifecycleState.CREATED: (SignalLifecycleState.QUALITY_CHECKED,),
    SignalLifecycleState.QUALITY_CHECKED: (SignalLifecycleState.EXPLAINED,),
    SignalLifecycleState.EXPLAINED: (SignalLifecycleState.APPROVED, SignalLifecycleState.REJECTED),
    SignalLifecycleState.APPROVED: (SignalLifecycleState.PAPER_OPEN,),
    SignalLifecycleState.REJECTED: (),
    SignalLifecycleState.PAPER_OPEN: (SignalLifecycleState.CLOSED,),
    SignalLifecycleState.CLOSED: (),
}


@dataclass(frozen=True)
class SignalStateTransitionResult:
    """Never raises -- an invalid transition produces success=False with a reason, the same convention as PaperTradeTransitionResult."""
    success: bool
    reason: str


def transition_signal_state(
    current: SignalLifecycleState,
    next_state: SignalLifecycleState,
) -> SignalStateTransitionResult:
    """Validates one step of ALLOWED_TRANSITIONS. Pure -- does not hold or mutate any state itself."""
    if next_state in ALLOWED_TRANSITIONS.get(current, ()):
        return SignalStateTransitionResult(success=True, reason="")
    return SignalStateTransitionResult(
        success=False,
        reason=f"{current.value} -> {next_state.value} is not an allowed transition",
    )


def derive_signal_lifecycle_state(
    signal: 'SignalSchema',
    paper_trade: Optional['PaperTrade'] = None,
) -> SignalLifecycleState:
    """
    Observational only -- classifies a SignalSchema's current lifecycle
    state from fields it (and an optional linked PaperTrade) already
    carry, the same read-only, priority-ordered classification pattern
    context_layer/trend/market_phase.py's compute_market_phase() already
    established. No new decision or quality logic: every input here
    was computed elsewhere (Signal Quality Score, Decision Engine,
    Paper Trade transitions).

    Known limitation, disclosed rather than faked: SignalSchema.
    explanation_id is always None in this codebase today (Explainability,
    Phase A9, has never been wired to it -- see docs/SIGNAL_SCHEMA.md).
    EXPLAINED therefore cannot be reliably derived from SignalSchema
    alone; a signal with quality_grade set is reported as
    QUALITY_CHECKED even if Explainability has, in fact, already run
    upstream in core/pipeline.py (it always has, by pipeline order --
    this function just cannot see that from the SignalSchema object
    itself).
    """
    if paper_trade is not None and paper_trade.status == TradeState.CLOSED:
        return SignalLifecycleState.CLOSED
    if paper_trade is not None and paper_trade.status == TradeState.OPEN:
        return SignalLifecycleState.PAPER_OPEN

    if signal.decision == "REJECTED":
        return SignalLifecycleState.REJECTED
    if signal.decision == "APPROVED":
        return SignalLifecycleState.APPROVED

    if signal.quality_grade is not None:
        return SignalLifecycleState.QUALITY_CHECKED

    return SignalLifecycleState.CREATED
