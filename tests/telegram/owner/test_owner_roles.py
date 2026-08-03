"""
Phase 59.6, TASK 3 -- telegram/owner/owner_roles.py tests. Real
AdminRepository (SQLite, tests/conftest.py's autouse fresh_database
fixture) -- no mocks. TELEGRAM_OWNER_ID is set to "111" by conftest.py.
"""

from database_layer.user_repository.admin_repository import AdminRepository
from telegram.owner.owner_roles import OwnerRole, resolve_owner_role


def test_resolve_owner_role_owner_id_is_owner():
    assert resolve_owner_role("111") == OwnerRole.OWNER


def test_resolve_owner_role_unregistered_user_is_viewer():
    assert resolve_owner_role("999999") == OwnerRole.VIEWER


def test_resolve_owner_role_admin_row_defaults_to_admin():
    repo = AdminRepository()
    repo.add_admin("8004")  # default role="ADMIN"

    assert resolve_owner_role("8004", admin_repository=repo) == OwnerRole.ADMIN


def test_resolve_owner_role_super_admin_row_resolves_correctly():
    repo = AdminRepository()
    repo.add_admin("8005", role="SUPER_ADMIN")

    assert resolve_owner_role("8005", admin_repository=repo) == OwnerRole.SUPER_ADMIN


def test_resolve_owner_role_owner_takes_precedence_over_admin_row():
    repo = AdminRepository()
    repo.add_admin("111", role="SUPER_ADMIN")  # even if also an admin row

    assert resolve_owner_role("111", admin_repository=repo) == OwnerRole.OWNER


def test_resolve_owner_role_unrecognized_role_string_defaults_to_admin():
    repo = AdminRepository()
    repo.add_admin("8006", role="CUSTOM_TIER")

    assert resolve_owner_role("8006", admin_repository=repo) == OwnerRole.ADMIN


def test_resolve_owner_role_never_raises_without_explicit_repository():
    # Constructs a real AdminRepository internally -- must not raise.
    result = resolve_owner_role("999999")
    assert result == OwnerRole.VIEWER


def test_owner_role_has_exactly_four_values():
    assert {r.value for r in OwnerRole} == {"OWNER", "SUPER_ADMIN", "ADMIN", "VIEWER"}
