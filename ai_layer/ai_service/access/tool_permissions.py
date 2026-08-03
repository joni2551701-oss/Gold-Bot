"""
AI Layer — AI Tool Permission Matrix (Phase 61.1: AI Provider
Reliability Foundation, TASK 6; corrected Phase 61.4: AI Product &
Control Layer, TASK 2).

Extends `ai/access/` with a second, independent entitlement axis --
Role x Tool (`ai/tools/*`'s plain string names), alongside
`access_control.py`'s existing Role x Capability matrix. A new file in
the same package rather than a new package, matching this package's
own existing internal split (`permissions.py` for the enum,
`access_control.py` for capability entitlement, `usage_limits.py` for
rate ceilings, now `tool_permissions.py` for tool entitlement).

Tool names are plain strings (`"market_tool"`, `"news_tool"`, ...)
matching `ai_layer.ai_service.tools.tool_registry.BaseAITool.name`'s own values --
deliberately not importing `ai/tools/` classes just for their names,
keeping this module's only dependency the `AIRole` enum it already
needs.

Phase 61.4 TASK 2 correction: `"learning_tool"` (added Phase 61.3
TASK 4, after this matrix was last touched) was missing from every
role's set -- `docs/PHASE61_4_PRODUCT_CONTROL_AUDIT.md` flagged this
as drift, not a new decision. Placed alongside `"analytics_tool"`
(same performance/history-shaped category) in every role that already
grants that tool.
"""

from typing import Dict, FrozenSet

from ai_layer.ai_service.access.permissions import AIRole

# Same "foundation default, not a business decision" posture as
# access_control.py's _DEFAULT_MATRIX. OWNER/ADMIN: every tool. VIP:
# every tool (matches the brief's own worked example: "VIP / News Tool
# / YES"). PREMIUM: everything except news_tool (a heavier, external-
# data-shaped tool). FREE: education_tool only (matches the brief's
# own worked example: "FREE / News Tool / NO").
_DEFAULT_TOOL_MATRIX: Dict[AIRole, FrozenSet[str]] = {
    AIRole.OWNER: frozenset({"market_tool", "news_tool", "analytics_tool", "learning_tool", "education_tool"}),
    AIRole.ADMIN: frozenset({"market_tool", "news_tool", "analytics_tool", "learning_tool", "education_tool"}),
    AIRole.VIP: frozenset({"market_tool", "news_tool", "analytics_tool", "learning_tool", "education_tool"}),
    AIRole.PREMIUM: frozenset({"market_tool", "analytics_tool", "learning_tool", "education_tool"}),
    AIRole.FREE: frozenset({"education_tool"}),
}


class ToolPermissions:
    """Same shape as `access_control.AccessControl` -- a caller can construct a customized matrix (e.g. for a test) without editing the module-level default."""

    def __init__(self, matrix: Dict[AIRole, FrozenSet[str]] = None) -> None:
        self._matrix = matrix if matrix is not None else _DEFAULT_TOOL_MATRIX

    def is_tool_allowed(self, role: AIRole, tool_name: str) -> bool:
        """Never raises: a role missing from the matrix has no entitlement, an unknown tool_name is never in any role's set."""
        return tool_name in self._matrix.get(role, frozenset())

    def allowed_tools(self, role: AIRole) -> FrozenSet[str]:
        return self._matrix.get(role, frozenset())
