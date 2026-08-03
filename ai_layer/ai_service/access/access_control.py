"""
AI Layer — AI Access Control (Phase 61.0: AI Infrastructure
Foundation, TASK 6).

A Role x Capability permission matrix -- "AI yoqish/o'chirish emas.
Capability permission" (this is capability-level entitlement, not a
global AI on/off switch; that is `ai/capabilities/capability_manager.py`'s
separate, orthogonal concern). `is_allowed()` answers "may this role
use this capability at all" -- it says nothing about whether the
capability itself is currently enabled system-wide (a caller checks
both, independently).
"""

from typing import Dict, FrozenSet

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.capabilities.capability import Capability

# Default entitlement matrix. OWNER/ADMIN: every capability (console
# operators, not subject to a subscription tier). VIP: everything
# except the heaviest/least-built capabilities (TOOL_CALLING/VIDEO/
# DOCUMENT stay OWNER/ADMIN-only until a real cost/safety review).
# PREMIUM: the core advisory set. FREE: read-only, low-cost
# capabilities only. This is a foundation default, not a business
# decision about pricing -- a future phase may make this configurable
# per the same Module Reuse Principle this phase itself follows.
_DEFAULT_MATRIX: Dict[AIRole, FrozenSet[Capability]] = {
    AIRole.OWNER: frozenset(Capability),
    AIRole.ADMIN: frozenset(Capability),
    AIRole.VIP: frozenset({
        Capability.CHAT, Capability.ANALYSIS, Capability.EXPLANATION,
        Capability.SUMMARY, Capability.MEMORY, Capability.EDUCATION,
        Capability.VISION, Capability.IMAGE, Capability.VOICE,
    }),
    AIRole.PREMIUM: frozenset({
        Capability.CHAT, Capability.ANALYSIS, Capability.EXPLANATION,
        Capability.SUMMARY, Capability.EDUCATION,
    }),
    AIRole.FREE: frozenset({
        Capability.CHAT, Capability.EXPLANATION,
    }),
}


class AccessControl:
    """Wraps `_DEFAULT_MATRIX` behind a class so a future caller can construct a customized matrix (e.g. for a test) without editing the module-level default."""

    def __init__(self, matrix: Dict[AIRole, FrozenSet[Capability]] = None) -> None:
        self._matrix = matrix if matrix is not None else _DEFAULT_MATRIX

    def is_allowed(self, role: AIRole, capability: Capability) -> bool:
        """Never raises: an AIRole missing from the matrix (impossible with the default, possible with a custom one) is treated as no entitlement, not an error."""
        return capability in self._matrix.get(role, frozenset())

    def allowed_capabilities(self, role: AIRole) -> FrozenSet[Capability]:
        return self._matrix.get(role, frozenset())
