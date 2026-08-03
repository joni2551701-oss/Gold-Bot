"""
Phase 47 — Admin Layer tests: OWNER/ADMIN/USER permission matrix,
admin CRUD, statistics, and the async broadcast() fix (Phase 47 audit).
"""

import asyncio
from unittest.mock import patch

from telegram.command_router import route_command, PERMISSION_DENIED_TEXT

OWNER_ID = "111"  # matches conftest's TELEGRAM_OWNER_ID
ADMIN_ID = "222"
USER_ID = "333"


def _bootstrap():
    from database_layer.user_repository.admin_repository import AdminRepository

    async def register_all():
        await route_command("/start", telegram_id=OWNER_ID)
        await route_command("/start", telegram_id=ADMIN_ID)
        await route_command("/start", telegram_id=USER_ID)

    asyncio.run(register_all())
    AdminRepository().add_admin(ADMIN_ID)


def test_owner_admin_user_permission_matrix_for_stats():
    _bootstrap()

    async def scenario():
        owner = await route_command("/stats", telegram_id=OWNER_ID)
        admin = await route_command("/stats", telegram_id=ADMIN_ID)
        user = await route_command("/stats", telegram_id=USER_ID)
        return owner, admin, user

    owner, admin, user = asyncio.run(scenario())
    assert owner.text.startswith("GoldBot Statistics")
    assert admin.text.startswith("GoldBot Statistics")
    assert user.text == PERMISSION_DENIED_TEXT


def test_addadmin_removeadmin_restricted_to_owner():
    _bootstrap()

    async def scenario():
        admin_tries = await route_command("/addadmin 999", telegram_id=ADMIN_ID)
        user_tries = await route_command("/addadmin 999", telegram_id=USER_ID)
        owner_tries = await route_command("/addadmin 999", telegram_id=OWNER_ID)
        return admin_tries, user_tries, owner_tries

    admin_tries, user_tries, owner_tries = asyncio.run(scenario())
    assert admin_tries.text == PERMISSION_DENIED_TEXT
    assert user_tries.text == PERMISSION_DENIED_TEXT
    assert owner_tries.text == "Admin added."


def test_add_admin_duplicate_reports_already_admin():
    from telegram.admin_service import AdminService

    service = AdminService()
    service.add_admin("400")
    result = service.add_admin("400")
    assert result.success is False
    assert result.reason == "Already an admin"


def test_remove_admin_revokes_admin_tier_access():
    _bootstrap()

    async def scenario():
        before = await route_command("/stats", telegram_id=ADMIN_ID)
        await route_command(f"/removeadmin {ADMIN_ID}", telegram_id=OWNER_ID)
        after = await route_command("/stats", telegram_id=ADMIN_ID)
        return before, after

    before, after = asyncio.run(scenario())
    assert before.text != PERMISSION_DENIED_TEXT
    assert after.text == PERMISSION_DENIED_TEXT


def test_get_user_summary_counts_by_status():
    _bootstrap()
    from telegram.admin_service import AdminService

    result = AdminService().get_user_summary()
    assert result.success is True
    assert result.user_summary.total == 3


def test_broadcast_is_async_and_safe_inside_a_running_event_loop():
    """
    Phase 47 audit fix: AdminService.broadcast() used to wrap its own
    asyncio.run() call and crashed with "asyncio.run() cannot be called
    from a running event loop" whenever invoked from an already-async
    caller (exactly how telegram/polling.py's Dispatcher calls
    broadcast_handler). It must now be awaited cleanly with no crash.
    """
    from aiogram.client.session.aiohttp import AiohttpSession
    from database_layer.user_repository.user_repository import UserRepository
    from telegram.admin_service import AdminService

    for i in range(4):
        UserRepository().create_user(telegram_id=f"{9000 + i}", notifications_enabled=(i % 2 == 0))

    async def fake_make_request(self, bot, method, timeout=None):
        await self.create_session()
        return None

    async def scenario():
        with patch.object(AiohttpSession, "make_request", new=fake_make_request):
            return await AdminService().broadcast("hello")

    result = asyncio.run(scenario())
    assert result.success is True
    assert result.broadcast.sent == 2  # only the notifications-enabled half
    assert result.broadcast.failed == 0


def test_permissions_owner_is_also_admin():
    from telegram.permissions import is_owner, is_admin, get_permission_level, PermissionLevel

    assert is_owner(OWNER_ID) is True
    assert is_admin(OWNER_ID) is True  # OWNER always counts as ADMIN
    assert get_permission_level(OWNER_ID) == PermissionLevel.OWNER


def test_permissions_unknown_user_is_plain_user():
    from telegram.permissions import get_permission_level, PermissionLevel

    assert get_permission_level("some-random-id-999999") == PermissionLevel.USER
