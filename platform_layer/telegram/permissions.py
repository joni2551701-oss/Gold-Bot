"""
Telegram Layer — permission tier foundation.

Classifies a Telegram user_id into OWNER / ADMIN / USER. No business
logic beyond tier classification -- what each tier is allowed to do
is command_router.py's decision (Phase 37: per-command permission
check against telegram.commands.OWNER_COMMANDS / ADMIN_COMMANDS).

OWNER_ID is sourced from core_layer.secrets.Secrets (env var
TELEGRAM_OWNER_ID), never hardcoded. ADMIN membership is sourced from
the 'admins' table via telegram.admin_service.AdminService, never
hardcoded.
"""

from enum import Enum

from core_layer.secrets import Secrets
from core_layer.logger.logger import setup_logger

logger = setup_logger("Permissions")


class PermissionLevel(Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    USER = "USER"


def _get_owner_id() -> str:
    """Reads the configured owner's Telegram user_id. "" if unset."""
    try:
        return Secrets().TELEGRAM_OWNER_ID
    except Exception:
        return ""


def is_owner(user_id) -> bool:
    owner_id = _get_owner_id()
    return bool(owner_id) and str(user_id) == owner_id


def is_admin(user_id) -> bool:
    """
    OWNER always counts as ADMIN. Otherwise checks the 'admins' table
    via AdminService. Never raises: a database failure or an
    unresolvable user_id resolves to False (fail-closed -- an unknown
    user stays USER, never silently promoted).
    """
    if is_owner(user_id):
        return True
    try:
        from platform_layer.telegram.admin_service import AdminService
        return AdminService().is_admin(user_id)
    except Exception as e:
        logger.warning(f"is_admin check failed for user_id={user_id}: {e}")
        return False


def is_user(user_id) -> bool:
    """Any resolvable Telegram user_id is at least a USER."""
    return user_id is not None


def get_permission_level(user_id) -> PermissionLevel:
    if is_owner(user_id):
        return PermissionLevel.OWNER
    if is_admin(user_id):
        return PermissionLevel.ADMIN
    return PermissionLevel.USER
