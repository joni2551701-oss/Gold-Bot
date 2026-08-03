"""
Phase 52 — command argument / input validation tests.

platform_layer/telegram/handlers.py validates every settings-change argument
(/risk, /language, /timeframe, /strategy) against a fixed allowlist
before calling the service layer -- but no test previously drove that
validation branch through route_command(); tests/test_user.py only
exercised the service methods directly (UserService.change_risk(),
etc.), bypassing the handler's argument parsing entirely. This file
closes that gap, plus a couple of missing-argument / empty-input
checks for admin commands and feedback.
"""

import asyncio

from platform_layer.telegram.command_router import route_command

USER_ID = "8201"


def _run(coro):
    return asyncio.run(coro)


def test_risk_command_rejects_out_of_range_value():
    result = _run(route_command("/risk 99", telegram_id=USER_ID))
    assert result.text == "Noto'g'ri risk foizi. Quyidagilardan birini tanlang: 1, 2, 3, 5."


def test_risk_command_accepts_valid_value():
    _run(route_command("/start", telegram_id=USER_ID))
    result = _run(route_command("/risk 3", telegram_id=USER_ID))
    assert result.text == "Risk 3% ga o'zgartirildi."


def test_language_command_rejects_unknown_language():
    result = _run(route_command("/language XX", telegram_id=USER_ID))
    assert result.text == "⚠️ Noto'g'ri til. Quyidagilardan birini tanlang: UZ, RU, EN."


def test_language_command_accepts_valid_language():
    _run(route_command("/start", telegram_id=USER_ID))
    result = _run(route_command("/language RU", telegram_id=USER_ID))
    assert result.text == "✅ Язык обновлён\nТекущий язык:\n🇷🇺 Русский"


def test_timeframe_command_rejects_unknown_timeframe():
    result = _run(route_command("/timeframe M99", telegram_id=USER_ID))
    assert result.text == "Noto'g'ri vaqt oralig'i. Quyidagilardan birini tanlang: M15, H1, H4."


def test_strategy_command_rejects_unknown_strategy():
    result = _run(route_command("/strategy Not A Real Strategy", telegram_id=USER_ID))
    assert result.text == "Noto'g'ri strategiya. Quyidagilardan birini tanlang: Liquidity Sweep, FVG, AMD, Order Block."


def test_addadmin_command_requires_an_argument():
    from platform_layer.telegram.command_router import PERMISSION_DENIED_TEXT

    # A plain user is denied before argument validation even runs --
    # confirms permission is checked first, not argument shape.
    result = _run(route_command("/addadmin", telegram_id=USER_ID))
    assert result.text == PERMISSION_DENIED_TEXT


def test_addadmin_command_requires_an_argument_for_owner():
    result = _run(route_command("/addadmin", telegram_id="111"))  # OWNER
    assert result.text == "Usage: /addadmin USER_ID"


def test_userinfo_command_requires_an_argument_for_admin(admin_user):
    result = _run(route_command("/userinfo", telegram_id=admin_user))
    assert result.text == "Usage: /userinfo USER_ID"


def test_feedback_command_with_no_argument_prompts_instead_of_submitting():
    result = _run(route_command("/feedback", telegram_id=USER_ID))
    assert result.text == "Fikr-mulohazangizni yuboring:\n\n/feedback <xabaringiz> dan foydalaning."


def test_feedback_command_with_only_whitespace_prompts_instead_of_submitting():
    result = _run(route_command("/feedback    ", telegram_id=USER_ID))
    assert result.text == "Fikr-mulohazangizni yuboring:\n\n/feedback <xabaringiz> dan foydalaning."


# ---------------------------------------------------------------------------
# Phase 54 — crash-safety additions: non-numeric input, very long text, and
# special/unicode characters must never raise, only ever produce a safe text
# response (this phase's spec's exact example: "/risk abc" must not crash).
# ---------------------------------------------------------------------------

def test_risk_command_with_non_numeric_value_does_not_crash():
    """The exact scenario this phase's spec named: /risk abc must not crash."""
    result = _run(route_command("/risk abc", telegram_id=USER_ID))
    assert result.text == "Noto'g'ri risk foizi. Quyidagilardan birini tanlang: 1, 2, 3, 5."


def test_risk_command_with_negative_and_float_values_does_not_crash():
    for bad_value in ("-5", "1.5", "999999999999999999999", "0", "٥"):
        result = _run(route_command(f"/risk {bad_value}", telegram_id=USER_ID))
        assert result.text == "Noto'g'ri risk foizi. Quyidagilardan birini tanlang: 1, 2, 3, 5."


def test_feedback_command_with_very_long_message_does_not_crash():
    """Telegram's own message cap is 4096 chars; well past it must still not crash."""
    long_message = "A" * 10000
    result = _run(route_command(f"/feedback {long_message}", telegram_id=USER_ID))
    assert result.text.startswith("✅ Fikr-mulohaza qabul qilindi.")


def test_feedback_command_with_special_and_unicode_characters_does_not_crash():
    payloads = [
        "😀🚀💰 emoji feedback",
        "Ω≈ç√∫˜µ≤≥÷ unicode symbols",
        "\x00\x01\x02 control characters",
        "line1\nline2\ttabbed",
        "<script>alert('xss')</script>",
        "'; DROP TABLE feedback; --",
        "بازخورد به زبان فارسی",  # right-to-left script
        "𝕿𝖊𝖘𝖙 𝖚𝖓𝖎𝖈𝖔𝖉𝖊 𝖇𝖑𝖔𝖈𝖐𝖘",  # astral-plane unicode
    ]
    for payload in payloads:
        result = _run(route_command(f"/feedback {payload}", telegram_id=USER_ID))
        assert result.text.startswith("✅ Fikr-mulohaza qabul qilindi."), f"crashed or rejected on: {payload!r}"


def test_broadcast_command_with_very_long_message_does_not_crash(owner_user):
    long_message = "B" * 10000
    result = _run(route_command(f"/broadcast {long_message}", telegram_id=owner_user))
    assert not result.text.startswith("Permission denied")


def test_userinfo_command_with_special_character_target_id_does_not_crash(admin_user):
    for payload in ("' OR '1'='1", "../../etc/passwd", "\x00", "🚀"):
        result = _run(route_command(f"/userinfo {payload}", telegram_id=admin_user))
        assert result.text == "User not found."  # safe, well-formed response, no crash


def test_strategy_command_with_very_long_argument_does_not_crash():
    result = _run(route_command(f"/strategy {'X' * 5000}", telegram_id=USER_ID))
    assert result.text == "Noto'g'ri strategiya. Quyidagilardan birini tanlang: Liquidity Sweep, FVG, AMD, Order Block."


def test_addadmin_command_with_special_character_argument_does_not_crash(owner_user):
    """
    A non-numeric/malicious-looking target_id must still be handled
    safely (stored literally, not executed). addadmin_handler's
    _first_arg() only takes the first whitespace-separated token from
    args -- matching that real, existing (and correct) behavior, not
    a bug this test should force-work-around.
    """
    result = _run(route_command("/addadmin ';DROP_TABLE_admins;--", telegram_id=owner_user))
    assert result.text == "Admin added."

    from database_layer.user_repository.admin_repository import AdminRepository
    assert AdminRepository().is_admin("';DROP_TABLE_admins;--") is True
