"""
AI Layer — AI Permission Service (Phase 61.4: AI Product & Control
Layer, TASK 2).

Resolves the real `AIRole` for a user from already-resolved identity
facts -- never imports `telegram/` or `database/` itself. `ai/`
deliberately holds no runtime dependency on either layer (the same
boundary `ai/context/context_adapter.py`'s docstring establishes for
`context/`); the caller -- a future `telegram/owner/ai_commands.py`
integration or a Conversation Engine caller -- already legitimately
has `telegram.permissions.is_owner()`/`is_admin()` and
`telegram.subscription_service.SubscriptionService.get_plan()`
available and passes their results in here. `docs/PHASE61_4_PRODUCT_CONTROL_AUDIT.md`'s
own `telegram/` finding names this as the missing resolver, not a
request for a fourth role enum.

Priority: OWNER > ADMIN > subscription-derived role. OWNER/ADMIN are
console operators, not subject to a subscription tier -- matches
`ai/access/access_control.py`'s own `_DEFAULT_MATRIX`, which already
grants OWNER/ADMIN every capability regardless of plan.
"""

from typing import Optional

from ai.access.permissions import AIRole
from ai.access.subscription_policy import plan_to_ai_role


def resolve_ai_role(is_owner: bool, is_admin: bool, plan: Optional[str] = None) -> AIRole:
    """Never raises: neither owner nor admin, with a missing/unrecognized plan, falls back to plan_to_ai_role()'s own FREE default."""
    if is_owner:
        return AIRole.OWNER
    if is_admin:
        return AIRole.ADMIN
    return plan_to_ai_role(plan)
