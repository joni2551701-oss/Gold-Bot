"""
Phase 59.8, Owner Control Center -- platform_layer/telegram/owner/security.py tests.
Real AdminRepository/AuditLogRepository (SQLite, tests/conftest.py's
autouse fresh_database fixture) -- no mocks. TELEGRAM_OWNER_ID is "111"
per conftest.py.
"""

from database_layer.user_repository.admin_repository import AdminRepository
from database_layer.audit_log.audit_log_repository import AuditLogRepository
from platform_layer.telegram.owner.owner_roles import OwnerRole
from platform_layer.telegram.owner.security import SecurityCheckResult, log_owner_action, require_role


def test_owner_meets_any_minimum_role():
    result = require_role("111", OwnerRole.OWNER)

    assert isinstance(result, SecurityCheckResult)
    assert result.allowed is True
    assert result.role == OwnerRole.OWNER


def test_viewer_does_not_meet_admin_minimum():
    result = require_role("999999", OwnerRole.ADMIN)

    assert result.allowed is False
    assert result.role == OwnerRole.VIEWER
    assert "requires ADMIN" in result.reason


def test_admin_meets_admin_minimum():
    repo = AdminRepository()
    repo.add_admin("8004")

    result = require_role("8004", OwnerRole.ADMIN, admin_repository=repo)

    assert result.allowed is True


def test_admin_does_not_meet_super_admin_minimum():
    repo = AdminRepository()
    repo.add_admin("8004")

    result = require_role("8004", OwnerRole.SUPER_ADMIN, admin_repository=repo)

    assert result.allowed is False


def test_super_admin_meets_admin_minimum():
    repo = AdminRepository()
    repo.add_admin("8005", role="SUPER_ADMIN")

    result = require_role("8005", OwnerRole.ADMIN, admin_repository=repo)

    assert result.allowed is True


def test_viewer_meets_viewer_minimum():
    result = require_role("999999", OwnerRole.VIEWER)
    assert result.allowed is True


# --- log_owner_action ---

def test_log_owner_action_persists_an_entry():
    entry = log_owner_action("owner", "FEATURE_ENABLED", target="ENABLE_AI")

    assert entry.actor == "owner"
    assert entry.action == "FEATURE_ENABLED"
    assert entry.target == "ENABLE_AI"

    persisted = AuditLogRepository().get_recent()
    assert len(persisted) == 1


def test_log_owner_action_uses_injected_repository():
    repo = AuditLogRepository()
    log_owner_action("owner", "PANIC", audit_log_repository=repo)

    assert repo.count() == 1
