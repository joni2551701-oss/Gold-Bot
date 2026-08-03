"""
AI Layer — AI Access Roles (Phase 61.0: AI Infrastructure Foundation,
TASK 6).

`AIRole` is named distinctly from `platform_layer/telegram/owner/owner_roles.py`'s
`OwnerRole` (OWNER/SUPER_ADMIN/ADMIN/VIEWER, an admin-console
hierarchy) and `platform_layer/telegram/permissions.py`'s `PermissionLevel`
(OWNER/ADMIN/USER, the live Telegram command gate) --
`docs/PHASE61_AI_FOUNDATION_AUDIT.md` TASK 1 found neither already
carries VIP/PREMIUM/FREE (subscription tiers), so this is a genuinely
distinct, AI-capability-entitlement-scoped enum, not a duplicate.
Reusing either existing enum's name here would conflate two different
concerns the codebase already keeps apart (admin-console access vs.
subscription-tier AI entitlement).

Not wired to any real user lookup this phase -- `database_layer/user_repository/user_repository.py`,
`database_layer/user_repository/admin_repository.py`, and `database_layer/user_repository/subscription_repository.py`
are read, not called, by this file (foundation only, per TASK 1's
audit).
"""

from enum import Enum


class AIRole(Enum):
    """
    Ordered highest-to-lowest privilege, matching the brief's own
    listed order. OWNER/ADMIN mirror the existing admin-console
    concept by name only (not by import) for readability; VIP/PREMIUM/
    FREE mirror `database_layer/database_manager/models.py`'s free-text subscription `plan`
    column values by name only, same reasoning.
    """
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    VIP = "VIP"
    PREMIUM = "PREMIUM"
    FREE = "FREE"
