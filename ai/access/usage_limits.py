"""
AI Layer — AI Usage Limits (Phase 61.0: AI Infrastructure Foundation,
TASK 6).

In-memory, per-(telegram_id, capability) call counter with a
role-based daily ceiling -- foundation only, no persistence, no timer/
scheduler (a caller/test resets or inspects state directly; nothing
here runs a background job).
"""

from dataclasses import dataclass
from typing import Dict, Tuple

from ai.access.permissions import AIRole
from ai.capabilities.capability import Capability

# Foundation defaults -- same "not a business decision, a placeholder
# default" posture as access_control.py's _DEFAULT_MATRIX. 0 means
# "no fixed daily ceiling recorded for this role" (OWNER/ADMIN today).
_DEFAULT_DAILY_LIMITS: Dict[AIRole, int] = {
    AIRole.OWNER: 0,
    AIRole.ADMIN: 0,
    AIRole.VIP: 200,
    AIRole.PREMIUM: 50,
    AIRole.FREE: 10,
}


@dataclass(frozen=True)
class UsageCheckResult:
    allowed: bool
    used: int
    limit: int
    reason: str = ""


class UsageLimiter:
    """`limit=0` means unlimited (OWNER/ADMIN's default) -- never counted against."""

    def __init__(self, daily_limits: Dict[AIRole, int] = None) -> None:
        self._limits = daily_limits if daily_limits is not None else _DEFAULT_DAILY_LIMITS
        self._counts: Dict[Tuple[str, Capability], int] = {}

    def _limit_for(self, role: AIRole) -> int:
        return self._limits.get(role, 0)

    def check(self, telegram_id: str, role: AIRole, capability: Capability) -> UsageCheckResult:
        """Read-only check -- does not increment. A caller calls record() separately after a successful call, so a rejected/failed call is never counted."""
        limit = self._limit_for(role)
        used = self._counts.get((telegram_id, capability), 0)
        if limit == 0:
            return UsageCheckResult(allowed=True, used=used, limit=limit, reason="unlimited")
        if used >= limit:
            return UsageCheckResult(allowed=False, used=used, limit=limit, reason="daily limit reached")
        return UsageCheckResult(allowed=True, used=used, limit=limit, reason="within limit")

    def record(self, telegram_id: str, capability: Capability) -> None:
        key = (telegram_id, capability)
        self._counts[key] = self._counts.get(key, 0) + 1

    def reset(self, telegram_id: str = None) -> None:
        """Clears one user's counters, or every counter if `telegram_id` is omitted -- same shape as ai/memory/context_memory.py's ContextMemory.clear()."""
        if telegram_id is None:
            self._counts.clear()
        else:
            for key in [k for k in self._counts if k[0] == telegram_id]:
                del self._counts[key]
