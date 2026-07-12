"""
Telegram Layer — permission tier foundation.

Classifies a Telegram user_id into OWNER / ADMIN / USER. No business
logic beyond tier classification -- what each tier is allowed to do
is a decision for handlers.py / user_service.py / admin_service.py in
a later phase.

OWNER_ID is sourced from core.secrets.Secrets (env var
TELEGRAM_OWNER_ID), never hardcoded.
"""

from enum import Enum

from core.secrets import Secrets


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
    Foundation only: no admin list source exists yet (no database
    schema change in this phase). Only the owner currently qualifies
    as admin; a real admin list will be wired in a future phase.
    """
    return is_owner(user_id)


def is_user(user_id) -> bool:
    """Any resolvable Telegram user_id is at least a USER."""
    return user_id is not None


def get_permission_level(user_id) -> PermissionLevel:
    if is_owner(user_id):
        return PermissionLevel.OWNER
    if is_admin(user_id):
        return PermissionLevel.ADMIN
    return PermissionLevel.USER
