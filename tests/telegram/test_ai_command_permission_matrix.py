"""Phase 61.5 Addendum (per Director review) — explicit permission-tier tests for the AI dashboard commands, /owner, and /doctor: FREE denied, ADMIN allow (read-only commands), OWNER allow (including the OWNER-only /doctor), and an unknown command."""

import asyncio

from platform_layer.telegram.command_router import route_command, PERMISSION_DENIED_TEXT, UNKNOWN_COMMAND_TEXT

OWNER_ID = "111"  # matches conftest's TELEGRAM_OWNER_ID
ADMIN_ID = "222"
FREE_USER_ID = "333"


def _run(coro):
    return asyncio.run(coro)


def _bootstrap_admin():
    from database_layer.user_repository.admin_repository import AdminRepository

    async def register_all():
        await route_command("/start", telegram_id=OWNER_ID)
        await route_command("/start", telegram_id=ADMIN_ID)
        await route_command("/start", telegram_id=FREE_USER_ID)

    _run(register_all())
    AdminRepository().add_admin(ADMIN_ID)


def test_free_user_is_denied_ai_status():
    _bootstrap_admin()
    result = _run(route_command("/ai_status", telegram_id=FREE_USER_ID))
    assert result.text == PERMISSION_DENIED_TEXT


def test_admin_is_allowed_ai_provider():
    _bootstrap_admin()
    result = _run(route_command("/ai_provider analysis", telegram_id=ADMIN_ID))
    assert result.text != PERMISSION_DENIED_TEXT
    assert "Current Provider" in result.text or "No available provider" in result.text


def test_admin_is_allowed_ai_status_ai_cost_ai_usage_ai_health_and_owner():
    _bootstrap_admin()
    for command in ("/ai_status", "/ai_cost", "/ai_usage 1", "/ai_health", "/owner"):
        result = _run(route_command(command, telegram_id=ADMIN_ID))
        assert result.text != PERMISSION_DENIED_TEXT, f"{command} unexpectedly denied for ADMIN"


def test_admin_is_denied_doctor_owner_only():
    """/doctor is deliberately OWNER-only (exposes internal subsystem reachability) -- ADMIN does not inherit it, unlike the read-only AI dashboard commands."""
    _bootstrap_admin()
    result = _run(route_command("/doctor", telegram_id=ADMIN_ID))
    assert result.text == PERMISSION_DENIED_TEXT


def test_owner_is_allowed_doctor():
    _bootstrap_admin()
    result = _run(route_command("/doctor", telegram_id=OWNER_ID))
    assert result.text != PERMISSION_DENIED_TEXT
    assert "Status" in result.text


def test_owner_is_allowed_every_ai_command_and_owner_and_doctor():
    _bootstrap_admin()
    for command in ("/ai_status", "/ai_provider analysis", "/ai_cost", "/ai_usage 1", "/ai_health", "/owner", "/doctor"):
        result = _run(route_command(command, telegram_id=OWNER_ID))
        assert result.text != PERMISSION_DENIED_TEXT, f"{command} unexpectedly denied for OWNER"


def test_unknown_ai_command_reports_invalid_command():
    _bootstrap_admin()
    result = _run(route_command("/ai_abc", telegram_id=OWNER_ID))
    assert result.text == UNKNOWN_COMMAND_TEXT
