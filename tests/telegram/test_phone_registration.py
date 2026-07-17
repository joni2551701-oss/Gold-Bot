"""Phase 61.5 TASK 4 — User Registration Integration: real /start -> Phone Share Button -> Phone Hash -> UserRecord -> Trial Check -> FREE account flow. First live wiring of trial_started_at persistence and contact-message routing."""

import asyncio
from types import SimpleNamespace

from telegram.command_router import route_command, route_contact
from telegram.user_service import UserService
from core.phone_hash import hash_phone_number


def _run(coro):
    return asyncio.run(coro)


def _contact_message(telegram_id, phone_number):
    return SimpleNamespace(
        from_user=SimpleNamespace(id=telegram_id, username="phoneuser"),
        contact=SimpleNamespace(phone_number=phone_number),
        text=None,
    )


def test_register_phone_for_unknown_user_reports_not_found():
    result = UserService().register_phone("999888", "+1 555 000 1111")
    assert result.success is False
    assert "not found" in result.reason.lower()


def test_register_phone_starts_a_trial_for_a_new_user():
    UserService().register_user("501", username="a")
    result = UserService().register_phone("501", "+1 555 111 2222")

    assert result.success is True
    assert result.trial_active is True
    assert result.trial_expires_at is not None


def test_register_phone_persists_only_the_hash_never_the_raw_number():
    UserService().register_user("502", username="b")
    UserService().register_phone("502", "+1 555 333 4444")

    profile = UserService().get_profile("502").profile
    assert profile.phone_hash == hash_phone_number("+1 555 333 4444")
    assert "555" not in profile.phone_hash
    assert "3334444" not in profile.phone_hash


def test_register_phone_persists_trial_started_at():
    UserService().register_user("503", username="c")
    UserService().register_phone("503", "+1 555 555 5555")

    profile = UserService().get_profile("503").profile
    assert profile.trial_started_at is not None


def test_register_phone_a_second_time_never_resets_the_trial_window():
    UserService().register_user("504", username="d")
    UserService().register_phone("504", "+1 555 666 7777")
    first_started_at = UserService().get_profile("504").profile.trial_started_at

    UserService().register_phone("504", "+1 555 666 7777")
    second_started_at = UserService().get_profile("504").profile.trial_started_at

    assert first_started_at == second_started_at


def test_register_phone_reused_by_another_account_blocks_the_trial():
    UserService().register_user("505", username="original")
    UserService().register_phone("505", "+1 555 999 0000")

    UserService().register_user("506", username="second_account")
    result = UserService().register_phone("506", "+1 555 999 0000")

    assert result.success is False
    assert "already registered" in result.reason.lower()


def test_register_phone_reused_still_stores_the_phone_hash_for_audit():
    UserService().register_user("507", username="original")
    UserService().register_phone("507", "+1 555 888 1234")

    UserService().register_user("508", username="reuser")
    UserService().register_phone("508", "+1 555 888 1234")

    profile = UserService().get_profile("508").profile
    assert profile.phone_hash == hash_phone_number("+1 555 888 1234")


def test_route_contact_end_to_end_registers_a_free_account():
    _run(route_command("/start", telegram_id="601"))

    message = _contact_message("601", "+1 555 222 3333")
    result = _run(route_contact(message))

    assert "verified" in result.text.lower()
    assert "trial" in result.text.lower()


def test_start_reply_carries_the_phone_share_keyboard():
    result = _run(route_command("/start", telegram_id="602"))
    assert result.keyboard is not None
