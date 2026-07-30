"""
decision/ — GoldBot's Decision Layer.

Live/FROZEN path (unchanged): decision.decision_engine.DecisionEngine.evaluate()
takes a SignalCandidate + AIAnalysisResult and returns a TradeDecision with a
DecisionAction (APPROVE / REJECT / NO_TRADE) — the confidence-blend the live
pipeline runs; do not modify without explicit approval (CLAUDE.md Trading
Safety).

STEP-09 business-decision layer (TASK-CORE-009, additive parallel, reuse-first):
decision.decision_manager.DecisionManager takes a canonical signal
(signals.schema.SignalSchema) and produces a DecisionOutcome with a
DecisionStatus (APPROVE / REJECT / HOLD / EXPIRE). It REUSES the frozen
engine's verdict (mapping NO_TRADE -> HOLD) and adds HOLD/EXPIRE via its own
business rules. It sizes no risk, sends no order, and touches no platform.
"""

from decision.decision_status import (
    DecisionStatus,
    from_decision_action,
    from_signal_decision,
)
from decision.decision_model import DecisionOutcome
from decision.decision_manager import DecisionManager
from decision.decision_router import DecisionConsumer, route as route_decision

__all__ = [
    "DecisionStatus",
    "from_decision_action",
    "from_signal_decision",
    "DecisionOutcome",
    "DecisionManager",
    "DecisionConsumer",
    "route_decision",
]
