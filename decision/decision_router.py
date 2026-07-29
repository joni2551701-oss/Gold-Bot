"""
Decision — STEP-09 router (TASK-CORE-009).

Decides which downstream consumers a decision outcome is relevant to and
returns that as route metadata. It sends nothing and calls no layer — a
consumer (risk/, database/, telegram/, ai/, monitoring/) reads the route list
and pulls the outcome itself. decision/ never reaches down into risk or
execution.

Routing is a pure function of the outcome's status: only an APPROVE flows on
to risk/ (the next trading step); every outcome is still routed to
database/ai/monitoring for the record.
"""

from enum import Enum
from typing import List

from decision.decision_status import DecisionStatus


class DecisionConsumer(str, Enum):
    """Layers that can consume a decision outcome."""
    RISK = "RISK"
    DATABASE = "DATABASE"
    TELEGRAM = "TELEGRAM"
    AI = "AI"
    MONITORING = "MONITORING"


# Always recorded/observed, regardless of verdict.
_ALWAYS = (
    DecisionConsumer.DATABASE,
    DecisionConsumer.AI,
    DecisionConsumer.MONITORING,
    DecisionConsumer.TELEGRAM,
)


def route(outcome) -> List[DecisionConsumer]:
    """
    Consumers for this outcome. RISK is included only for an APPROVE
    (HOLD/REJECT/EXPIRE never reach risk sizing); database/ai/monitoring/
    telegram always get it for the record. Pure metadata — dispatches nothing.
    """
    consumers: List[DecisionConsumer] = list(_ALWAYS)
    if getattr(outcome, "status", None) == DecisionStatus.APPROVE:
        consumers.insert(0, DecisionConsumer.RISK)
    return consumers


def route_values(outcome) -> List[str]:
    """route() as plain strings, for serialization."""
    return [c.value for c in route(outcome)]
