"""
Assistant Layer — Owner Mode Gate (Phase 65.3: Personal AI Assistant
Foundation, TASK 7).

Deliberately NOT `ai/access/access_control.py`'s `AccessControl`
matrix -- that matrix grants `AIRole.OWNER` and `AIRole.ADMIN` the same
`frozenset(Capability)` automatically, which would silently pass
`ADMIN` too. TASK 7 is explicit: "Admin: BLOCK. Premium: BLOCK. VIP:
BLOCK." -- only `AIRole.OWNER` may ever pass. See
`docs/PHASE65_3_AUDIT.md`'s own "Owner Mode" section for the full
resolution.

`AIRole` (the enum) is read from `ai_layer.ai_service.access.permissions` -- an
access-control *type*, orthogonal to the Knowledge->...->Broadcast
content chain the Intelligence Dependency Principle governs, the same
class every `platform_layer/telegram/owner/ai_commands.py` function already imports.
"""

from ai_layer.ai_service.access.permissions import AIRole
from core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def is_personal_ai_enabled_for(role: AIRole, flags: FeatureFlags = DEFAULT_FLAGS) -> bool:
    """
    True only when BOTH the global `enable_personal_ai` flag is on AND
    `role` is exactly `AIRole.OWNER`. Never raises: an unrecognized
    role value simply fails the equality check, no exception.
    """
    if not flags.enable_personal_ai:
        return False
    return role == AIRole.OWNER
