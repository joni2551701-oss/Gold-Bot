"""
Telegram Layer — Owner Permission System foundation (Phase 59.6: Audit
& Observability Foundation, TASK 3).

OwnerRole is a finer-grained hierarchy for the future Owner Mode
dashboard (Phase 59.8, per the Director's own roadmap) -- NOT a
replacement for telegram.permissions.PermissionLevel (OWNER/ADMIN/
USER), which is live-wired into telegram/command_router.py's real,
already-running permission gating today (_PERMISSION_RANK,
_required_level()). This module never imports or modifies that enum
or its ranking; it exists alongside it, foundation only -- "Hozir
faqat foundation" per this task's own brief. No owner command in
telegram/owner/ checks OwnerRole yet; wiring a real per-command
minimum-role check is a future, separately-approved step.
"""

from enum import Enum
from typing import Optional, TYPE_CHECKING

from telegram.permissions import is_owner
from core_layer.logger.logger import setup_logger

if TYPE_CHECKING:
    from database.admin_repository import AdminRepository

logger = setup_logger("OwnerRoles")


class OwnerRole(Enum):
    """
    OWNER: the single configured owner (telegram.permissions.is_owner()) --
        always the highest tier, same source of truth as PermissionLevel.OWNER.
    SUPER_ADMIN/ADMIN: read from the existing 'admins' table's free-text
        `role` column (database/admin_models.py's AdminRecord.role,
        already there since Phase 37/45, previously only used as a
        label -- resolve_owner_role() below is the first place its
        value is actually classified into a tier). "ADMIN" is the
        table's own existing default; "SUPER_ADMIN" is a new value a
        caller may set via AdminRepository.add_admin(role="SUPER_ADMIN"),
        not yet done anywhere in this codebase.
    VIEWER: the safe default for any resolvable Telegram user_id that
        is neither the owner nor a row in `admins` -- read-only intent
        by name, though nothing in this codebase enforces that
        restriction yet (foundation only).
    """
    OWNER = "OWNER"
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    VIEWER = "VIEWER"


def resolve_owner_role(telegram_id, admin_repository: Optional['AdminRepository'] = None) -> OwnerRole:
    """
    Never raises: mirrors telegram.permissions.is_admin()'s own
    fail-closed posture -- an AdminRepository lookup failure resolves
    to VIEWER, never silently promoted. `admin_repository` is
    injectable (same optional-dependency convention as
    TwelveDataProvider's own `client` parameter) so a caller/test never
    needs to construct a real AdminRepository just to check OWNER.
    """
    if is_owner(telegram_id):
        return OwnerRole.OWNER

    try:
        if admin_repository is None:
            from database.admin_repository import AdminRepository as _AdminRepository
            admin_repository = _AdminRepository()
        record = admin_repository.get_admin(telegram_id)
    except Exception as e:
        logger.warning(f"resolve_owner_role admin lookup failed for telegram_id={telegram_id}: {e}")
        return OwnerRole.VIEWER

    if record is None:
        return OwnerRole.VIEWER

    if record.role == OwnerRole.SUPER_ADMIN.value:
        return OwnerRole.SUPER_ADMIN

    return OwnerRole.ADMIN
