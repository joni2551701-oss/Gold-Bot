"""
AI Layer — User Capability (Phase 61.4: AI Product & Control Layer,
TASK 2).

A single "can this real user do X right now" answer -- composes the
already-resolved `AIRole` (`ai_layer.ai_service.access.permission_service.resolve_ai_role()`)
with `ai/access/access_control.py`'s Role x Capability matrix,
`ai/access/tool_permissions.py`'s Role x Tool matrix, and
`ai/access/usage_limits.py`'s daily ceiling, so a caller needs one
lookup instead of three. No new entitlement logic -- every check
delegates to the existing, unmodified class.
"""

from dataclasses import dataclass
from typing import Optional

from ai_layer.ai_service.access.access_control import AccessControl
from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_service.access.tool_permissions import ToolPermissions
from ai_layer.ai_service.access.usage_limits import UsageCheckResult, UsageLimiter
from ai_layer.ai_engine.capabilities.capability import Capability


@dataclass(frozen=True)
class UserCapability:
    """The already-resolved identity a caller passes in -- built via ai.access.permission_service.resolve_ai_role(), not by this module."""
    telegram_id: str
    role: AIRole


class UserCapabilityService:
    """Every dependency is injectable, same convention as every other Phase 61.x foundation class."""

    def __init__(
        self,
        access_control: Optional[AccessControl] = None,
        tool_permissions: Optional[ToolPermissions] = None,
        usage_limiter: Optional[UsageLimiter] = None,
    ) -> None:
        self._access_control = access_control or AccessControl()
        self._tool_permissions = tool_permissions or ToolPermissions()
        self._usage_limiter = usage_limiter or UsageLimiter()

    def can_use_capability(self, user: UserCapability, capability: Capability) -> bool:
        return self._access_control.is_allowed(user.role, capability)

    def can_use_tool(self, user: UserCapability, tool_name: str) -> bool:
        return self._tool_permissions.is_tool_allowed(user.role, tool_name)

    def check_usage(self, user: UserCapability, capability: Capability) -> UsageCheckResult:
        return self._usage_limiter.check(user.telegram_id, user.role, capability)

    def record_usage(self, user: UserCapability, capability: Capability) -> None:
        self._usage_limiter.record(user.telegram_id, capability)
