"""
Phase 52 — Telegram command-routing integration tests.

Exercises the full Telegram Update -> route_command() -> permission
check -> handler -> service -> database chain for commands that had no
direct route_command()-level test before this phase: /profile,
/settings, /history, /subscription, /notifications, /users. (/start,
/addadmin, /removeadmin, /stats, /feedback were already covered in
tests/test_admin.py and tests/test_feedback.py -- not duplicated here.)
"""

import asyncio

from telegram.command_router import route_command, PERMISSION_DENIED_TEXT

USER_ID = "8101"
ADMIN_ID = "8102"


def _run(coro):
    return asyncio.run(coro)


def test_profile_command_after_start():
    _run(route_command("/start", telegram_id=USER_ID, username="tester"))
    result = _run(route_command("/profile", telegram_id=USER_ID))
    assert result.text.startswith("GoldBot Profili")
    assert "tester" in result.text


def test_profile_command_without_start_shows_not_found():
    result = _run(route_command("/profile", telegram_id="8199-never-started"))
    assert result.text == "Profil topilmadi.\nAvval /start buyrug'ini bosing."


def test_settings_command_shows_menu():
    result = _run(route_command("/settings", telegram_id=USER_ID))
    assert result.text.startswith("Sozlamalar")
    assert "/language" in result.text


def test_history_command_empty_then_populated():
    empty = _run(route_command("/history", telegram_id=USER_ID))
    assert empty.text == "Signal tarixi mavjud emas."

    from database_layer.trade_repository.signal_repository import SignalRepository
    SignalRepository().create_signal({
        "signal_id": "hist-1", "symbol": "XAUUSD", "direction": "BUY",
        "entry_zone_min": 2000.0, "entry_zone_max": 2000.0, "stop_loss": 1990.0,
        "take_profit_1": 2030.0, "take_profit_2": 0.0, "risk_percent": 0.0,
        "lot_size": 0.0, "strategy_name": "Liquidity Sweep", "confidence_score": 0.8,
        "ai_explanation": "test",
    })
    populated = _run(route_command("/history", telegram_id=USER_ID))
    assert populated.text.startswith("Signal History")


def test_subscription_command_shows_free_by_default():
    _run(route_command("/start", telegram_id=USER_ID))
    result = _run(route_command("/subscription", telegram_id=USER_ID))
    assert result.text.startswith("Obuna Holati")
    assert "FREE" in result.text


def test_notifications_command_status_and_toggle():
    _run(route_command("/start", telegram_id=USER_ID))
    status = _run(route_command("/notifications", telegram_id=USER_ID))
    assert "Bildirishnomalar" in status.text

    off = _run(route_command("/notifications off", telegram_id=USER_ID))
    assert off.text == "Bildirishnomalar o'chirildi."

    on = _run(route_command("/notifications on", telegram_id=USER_ID))
    assert on.text == "Bildirishnomalar yoqildi."


def test_notifications_command_rejects_invalid_argument():
    result = _run(route_command("/notifications maybe", telegram_id=USER_ID))
    assert result.text == "Noto'g'ri tanlov. /notifications on yoki /notifications off dan foydalaning."


def test_users_command_requires_admin_and_reports_counts():
    from database_layer.user_repository.admin_repository import AdminRepository

    _run(route_command("/start", telegram_id=USER_ID))
    _run(route_command("/start", telegram_id=ADMIN_ID))
    AdminRepository().add_admin(ADMIN_ID)

    denied = _run(route_command("/users", telegram_id=USER_ID))
    assert denied.text == PERMISSION_DENIED_TEXT

    allowed = _run(route_command("/users", telegram_id=ADMIN_ID))
    assert allowed.text.startswith("GoldBot Users")
    assert "Total:\n2" in allowed.text


def test_broadcast_command_denied_for_plain_user():
    result = _run(route_command("/broadcast hello", telegram_id=USER_ID))
    assert result.text == PERMISSION_DENIED_TEXT


def test_unknown_command_returns_safe_text():
    from telegram.command_router import UNKNOWN_COMMAND_TEXT

    result = _run(route_command("/this_is_not_a_real_command", telegram_id=USER_ID))
    assert result.text == UNKNOWN_COMMAND_TEXT
