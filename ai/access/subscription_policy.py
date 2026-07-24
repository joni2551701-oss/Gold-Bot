"""
AI Layer — Subscription Policy (Phase 61.4: AI Product & Control
Layer, TASK 2).

Pure `SubscriptionRecord.plan` string -> `AIRole` mapping. No
`telegram/` or `database/` import -- `ai/` never reaches into those
layers directly (see `ai/access/permission_service.py`'s own
docstring for why). `telegram/subscription_service.py`'s
`SIGNAL_ACCESS_PLANS = {"PREMIUM", "VIP"}` and `DEFAULT_PLAN = "FREE"`
(Phase 42, unmodified) already confirm the real plan values this
module maps from.
"""

from typing import Dict, Optional

from ai.access.permissions import AIRole

_PLAN_TO_ROLE: Dict[str, AIRole] = {
    "VIP": AIRole.VIP,
    "PREMIUM": AIRole.PREMIUM,
    "FREE": AIRole.FREE,
}


def plan_to_ai_role(plan: Optional[str]) -> AIRole:
    """Never raises: a missing or unrecognized plan value fails closed to AIRole.FREE, never grants an unearned entitlement."""
    if plan is None:
        return AIRole.FREE
    return _PLAN_TO_ROLE.get(plan.upper(), AIRole.FREE)
