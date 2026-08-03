"""
Telegram Layer — Owner Control Center Security (Phase 59.8: Owner
Control Center). Foundation only, same "real function, not live-wired"
posture as every other module in this package -- see
provider_commands.py's own docstring. No command in this package calls
require_role() to actually gate itself yet; wiring a real per-command
minimum-role check is a future, separately-approved step, the same
boundary telegram/owner/README.md already documents for
`telegram.owner.owner_roles.OwnerRole` itself.

Two responsibilities, both thin wrappers over already-built Phase 59.6
pieces -- no new role hierarchy, no new audit table:
    require_role()    -- classifies + ranks via owner_roles.resolve_owner_role()
    log_owner_action() -- a convenience call-through to AuditLogRepository.log_action()
"""

from dataclasses import dataclass
from typing import Optional

from database_layer.audit_log.audit_log_repository import AuditLogRepository
from database_layer.audit_log.audit_log_models import AuditLogEntry
from telegram.owner.owner_roles import OwnerRole, resolve_owner_role
from core_layer.logger.logger import setup_logger

logger = setup_logger("OwnerSecurity")

# Same tiering telegram/command_router.py's own _PERMISSION_RANK
# established for PermissionLevel -- a separate ranking here (not a
# shared constant) since OwnerRole and PermissionLevel are
# deliberately distinct hierarchies (see owner_roles.py's own
# docstring); VIEWER is the floor, OWNER the ceiling.
_ROLE_RANK = {
    OwnerRole.VIEWER: 0,
    OwnerRole.ADMIN: 1,
    OwnerRole.SUPER_ADMIN: 2,
    OwnerRole.OWNER: 3,
}


@dataclass(frozen=True)
class SecurityCheckResult:
    """allowed: whether `role` meets or exceeds the required minimum. Never raises to build -- resolve_owner_role() itself already fails closed to VIEWER on any lookup error."""
    allowed: bool
    role: OwnerRole
    reason: str = ""


def require_role(telegram_id, minimum_role: OwnerRole, admin_repository=None) -> SecurityCheckResult:
    """
    Resolves `telegram_id`'s current OwnerRole (via
    telegram.owner.owner_roles.resolve_owner_role(), reused unmodified)
    and checks it against `minimum_role`'s rank. Never raises: an
    unresolvable identity fails closed (VIEWER, the lowest rank), same
    posture as resolve_owner_role() itself.
    """
    role = resolve_owner_role(telegram_id, admin_repository=admin_repository)
    allowed = _ROLE_RANK[role] >= _ROLE_RANK[minimum_role]
    reason = "" if allowed else f"requires {minimum_role.value}, caller is {role.value}"
    return SecurityCheckResult(allowed=allowed, role=role, reason=reason)


def log_owner_action(
    actor: str,
    action: str,
    target: Optional[str] = None,
    result: str = "SUCCESS",
    details: Optional[str] = None,
    audit_log_repository: Optional[AuditLogRepository] = None,
) -> AuditLogEntry:
    """Convenience call-through to AuditLogRepository.log_action() (Phase 59.6, unmodified) -- exists so an Owner Control Center command has one obvious place to log from, without needing to know the repository's own name."""
    repository = audit_log_repository or AuditLogRepository()
    return repository.log_action(actor, action, target=target, result=result, details=details)
