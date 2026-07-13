"""
Phase 52 — command argument / input validation tests.

telegram/handlers.py validates every settings-change argument
(/risk, /language, /timeframe, /strategy) against a fixed allowlist
before calling the service layer -- but no test previously drove that
validation branch through route_command(); tests/test_user.py only
exercised the service methods directly (UserService.change_risk(),
etc.), bypassing the handler's argument parsing entirely. This file
closes that gap, plus a couple of missing-argument / empty-input
checks for admin commands and feedback.
"""

import asyncio

from telegram.command_router import route_command

USER_ID = "8201"


def _run(coro):
    return asyncio.run(coro)


def test_risk_command_rejects_out_of_range_value():
    result = _run(route_command("/risk 99", telegram_id=USER_ID))
    assert result.text == "Invalid risk percent. Choose one of: 1, 2, 3, 5."


def test_risk_command_accepts_valid_value():
    _run(route_command("/start", telegram_id=USER_ID))
    result = _run(route_command("/risk 3", telegram_id=USER_ID))
    assert result.text == "Risk updated to 3%."


def test_language_command_rejects_unknown_language():
    result = _run(route_command("/language XX", telegram_id=USER_ID))
    assert result.text == "Invalid language. Choose one of: UZ, RU, EN."


def test_language_command_accepts_valid_language():
    _run(route_command("/start", telegram_id=USER_ID))
    result = _run(route_command("/language RU", telegram_id=USER_ID))
    assert result.text == "Language updated to RU."


def test_timeframe_command_rejects_unknown_timeframe():
    result = _run(route_command("/timeframe M99", telegram_id=USER_ID))
    assert result.text == "Invalid timeframe. Choose one of: M15, H1, H4."


def test_strategy_command_rejects_unknown_strategy():
    result = _run(route_command("/strategy Not A Real Strategy", telegram_id=USER_ID))
    assert result.text == "Invalid strategy. Choose one of: Liquidity Sweep, FVG, AMD, Order Block."


def test_addadmin_command_requires_an_argument():
    from telegram.command_router import PERMISSION_DENIED_TEXT

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
    assert result.text == "Send your feedback:\n\nUse /feedback <your message>."


def test_feedback_command_with_only_whitespace_prompts_instead_of_submitting():
    result = _run(route_command("/feedback    ", telegram_id=USER_ID))
    assert result.text == "Send your feedback:\n\nUse /feedback <your message>."
