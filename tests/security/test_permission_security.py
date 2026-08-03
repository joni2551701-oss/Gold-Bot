"""
Phase 54 — permission / privilege-escalation security tests.

Consolidates the exact USER-denied / ADMIN-allowed / OWNER-full-access
matrix this phase's spec named, for every admin-tier command, through
the real route_command() -> permission check -> handler chain. Some of
this overlaps intentionally with tests/test_admin.py (Phase 47) and
tests/integration/test_telegram_flow.py (Phase 52) as a consolidated
regression net specifically for privilege escalation, but /admin and
/system's full ADMIN/OWNER-allowed paths (not just USER-denied) had no
direct test before this phase.
"""

import asyncio

from platform_layer.telegram.command_router import route_command, PERMISSION_DENIED_TEXT

OWNER_ID = "111"  # matches conftest's TELEGRAM_OWNER_ID
ADMIN_ID = "9302"
USER_ID = "9303"


def _run(coro):
    return asyncio.run(coro)


def _bootstrap():
    from database_layer.user_repository.admin_repository import AdminRepository

    async def register_all():
        await route_command("/start", telegram_id=OWNER_ID)
        await route_command("/start", telegram_id=ADMIN_ID)
        await route_command("/start", telegram_id=USER_ID)

    _run(register_all())
    AdminRepository().add_admin(ADMIN_ID)


def test_user_denied_every_admin_tier_command():
    """The exact command list this phase's spec named for USER."""
    _bootstrap()
    for command in ("/admin", "/stats", "/users", "/system", "/broadcast hi"):
        result = _run(route_command(command, telegram_id=USER_ID))
        assert result.text == PERMISSION_DENIED_TEXT, f"{command} was not denied for USER"


def test_admin_allowed_every_admin_tier_command():
    _bootstrap()

    admin_panel = _run(route_command("/admin", telegram_id=ADMIN_ID))
    assert admin_panel.text.startswith("GoldBot Admin Panel")
    assert "Broadcast" not in admin_panel.text  # reduced panel -- OWNER-only actions hidden

    stats = _run(route_command("/stats", telegram_id=ADMIN_ID))
    assert stats.text.startswith("GoldBot Statistics")

    users = _run(route_command("/users", telegram_id=ADMIN_ID))
    assert users.text.startswith("GoldBot Users")

    system = _run(route_command("/system", telegram_id=ADMIN_ID))
    assert system.text.startswith("GoldBot System Status")

    broadcast = _run(route_command("/broadcast security test", telegram_id=ADMIN_ID))
    assert not broadcast.text.startswith("Permission denied")


def test_owner_has_full_access_including_owner_only_commands():
    _bootstrap()

    admin_panel = _run(route_command("/admin", telegram_id=OWNER_ID))
    assert admin_panel.text.startswith("GoldBot Owner Panel")
    assert "Broadcast" in admin_panel.text  # full panel

    # OWNER-only commands (not in ADMIN_COMMANDS at all): /addadmin, /removeadmin
    add_result = _run(route_command("/addadmin 555555", telegram_id=OWNER_ID))
    assert add_result.text == "Admin added."

    remove_result = _run(route_command("/removeadmin 555555", telegram_id=OWNER_ID))
    assert remove_result.text == "Admin removed."


def test_admin_denied_owner_only_commands():
    """ADMIN is not OWNER -- /addadmin and /removeadmin must stay OWNER-exclusive."""
    _bootstrap()

    add_result = _run(route_command("/addadmin 555555", telegram_id=ADMIN_ID))
    assert add_result.text == PERMISSION_DENIED_TEXT

    remove_result = _run(route_command("/removeadmin 555555", telegram_id=ADMIN_ID))
    assert remove_result.text == PERMISSION_DENIED_TEXT


def test_revoked_admin_immediately_loses_access():
    """No caching/stale-permission window -- revocation takes effect on the very next call."""
    from database_layer.user_repository.admin_repository import AdminRepository

    _bootstrap()
    before = _run(route_command("/stats", telegram_id=ADMIN_ID))
    assert before.text != PERMISSION_DENIED_TEXT

    AdminRepository().remove_admin(ADMIN_ID)

    after = _run(route_command("/stats", telegram_id=ADMIN_ID))
    assert after.text == PERMISSION_DENIED_TEXT


def test_command_allowlist_blocks_attribute_injection_attempts():
    """
    _parse_command()'s output is checked against the closed _ALL_COMMANDS
    registry BEFORE it is ever used in getattr(handlers, f"{command}_handler").
    A command name that isn't a real registered command must resolve to
    UNKNOWN_COMMAND_TEXT, never reach getattr with attacker-controlled input.
    """
    from platform_layer.telegram.command_router import UNKNOWN_COMMAND_TEXT

    for malicious in ("/__class__", "/__init__", "/os.system", "/../etc/passwd", "/eval"):
        result = _run(route_command(malicious, telegram_id=USER_ID))
        assert result.text == UNKNOWN_COMMAND_TEXT


def test_owner_status_is_config_only_never_a_database_row():
    """
    OWNER comes exclusively from TELEGRAM_OWNER_ID (core/secrets.py) --
    adding a database row for a telegram_id must never grant OWNER,
    only ADMIN.
    """
    from database_layer.user_repository.admin_repository import AdminRepository
    from platform_layer.telegram.permissions import is_owner

    AdminRepository().add_admin(USER_ID)
    assert is_owner(USER_ID) is False
