"""
Telegram Layer -- Settings module handler tests (V2 Phase 6.2: Settings
Callback Completion). telegram.handlers.risk_status()/strategy_status()/
timeframe_status()/notifications_status() and settings_handler()'s
current-value display are exercised against the real UserService/
UserRepository (same pattern tests/telegram/test_language_handler.py
already uses), since the point is verifying real DB persistence, not
just dispatch shape.
"""

import asyncio

from telegram.handlers import (
    risk_status,
    risk_handler,
    strategy_status,
    strategy_handler,
    timeframe_status,
    timeframe_handler,
    notifications_status,
    notifications_handler,
    settings_handler,
)
from telegram.user_service import UserService


def _run(coro):
    return asyncio.run(coro)


# ---------------------------------------------------------------------------
# Risk
# ---------------------------------------------------------------------------


def test_risk_status_no_args_shows_current_value_and_keeps_keyboard():
    UserService().register_user("901", username="risk_a")
    result = _run(risk_status("901", args=None))
    assert result.show_keyboard is True


def test_risk_status_valid_choice_updates_db_and_removes_keyboard():
    UserService().register_user("902", username="risk_b")
    result = _run(risk_status("902", args="3"))

    assert result.show_keyboard is False
    assert "3%" in result.text
    assert UserService().get_profile("902").profile.risk_percent == 3.0


def test_risk_status_invalid_choice_keeps_keyboard_and_does_not_change_db():
    UserService().register_user("903", username="risk_c")
    result = _run(risk_status("903", args="99"))

    assert result.show_keyboard is True
    assert UserService().get_profile("903").profile.risk_percent == 2.0  # unchanged default


def test_risk_handler_is_a_thin_wrapper_returning_just_the_text():
    UserService().register_user("904", username="risk_d")
    text = _run(risk_handler("904", args="5"))
    assert "5%" in text
    assert isinstance(text, str)


# ---------------------------------------------------------------------------
# Strategy
# ---------------------------------------------------------------------------


def test_strategy_status_valid_choice_updates_db():
    UserService().register_user("905", username="strategy_a")
    result = _run(strategy_status("905", args="fvg"))

    assert result.show_keyboard is False
    assert UserService().get_profile("905").profile.strategy == "FVG"


def test_strategy_status_invalid_choice_keeps_keyboard_and_does_not_change_db():
    UserService().register_user("906", username="strategy_b")
    result = _run(strategy_status("906", args="Not A Real Strategy"))

    assert result.show_keyboard is True
    assert UserService().get_profile("906").profile.strategy == "Liquidity Sweep"  # unchanged default


def test_strategy_handler_is_a_thin_wrapper_returning_just_the_text():
    UserService().register_user("907", username="strategy_c")
    text = _run(strategy_handler("907", args="amd"))
    assert isinstance(text, str)
    assert UserService().get_profile("907").profile.strategy == "AMD"


# ---------------------------------------------------------------------------
# Timeframe
# ---------------------------------------------------------------------------


def test_timeframe_status_valid_choice_updates_db():
    UserService().register_user("908", username="timeframe_a")
    result = _run(timeframe_status("908", args="h4"))

    assert result.show_keyboard is False
    assert UserService().get_profile("908").profile.timeframe == "H4"


def test_timeframe_status_invalid_choice_keeps_keyboard_and_does_not_change_db():
    UserService().register_user("909", username="timeframe_b")
    result = _run(timeframe_status("909", args="M99"))

    assert result.show_keyboard is True
    assert UserService().get_profile("909").profile.timeframe == "M15"  # unchanged default


def test_timeframe_handler_is_a_thin_wrapper_returning_just_the_text():
    UserService().register_user("910", username="timeframe_c")
    text = _run(timeframe_handler("910", args="h1"))
    assert isinstance(text, str)
    assert UserService().get_profile("910").profile.timeframe == "H1"


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------


def test_notifications_status_no_args_shows_current_status_and_keeps_keyboard():
    UserService().register_user("911", username="notif_a")
    result = _run(notifications_status("911", args=None))
    assert result.show_keyboard is True


def test_notifications_status_off_updates_db():
    UserService().register_user("912", username="notif_b")
    result = _run(notifications_status("912", args="off"))

    assert result.show_keyboard is False
    assert UserService().get_profile("912").profile.notifications_enabled is False


def test_notifications_status_invalid_choice_keeps_keyboard_and_does_not_change_db():
    UserService().register_user("913", username="notif_c")
    result = _run(notifications_status("913", args="maybe"))

    assert result.show_keyboard is True
    assert UserService().get_profile("913").profile.notifications_enabled is True  # unchanged default


def test_notifications_handler_is_a_thin_wrapper_returning_just_the_text():
    UserService().register_user("914", username="notif_d")
    text = _run(notifications_handler("914", args="on"))
    assert isinstance(text, str)


# ---------------------------------------------------------------------------
# Translation -- UZ/RU/EN all render risk.updated without a raw {percent}
# placeholder leaking through (Stage 8: no hardcoded strings, all three
# languages covered).
# ---------------------------------------------------------------------------


def test_risk_updated_message_is_localized_in_all_three_languages():
    UserService().register_user("915", username="risk_uz")
    UserService().register_user("916", username="risk_ru")
    UserService().register_user("917", username="risk_en")
    UserService().change_language("916", "RU")
    UserService().change_language("917", "EN")

    uz = _run(risk_status("915", args="2")).text
    ru = _run(risk_status("916", args="2")).text
    en = _run(risk_status("917", args="2")).text

    assert "{percent}" not in uz and "{percent}" not in ru and "{percent}" not in en
    assert "o'zgartirildi" in uz
    assert "обновлён" in ru
    assert "updated" in en


# ---------------------------------------------------------------------------
# settings_handler() -- Stage 5 (Current Value): shows the caller's real
# stored values, never hardcoded placeholders.
# ---------------------------------------------------------------------------


def test_settings_handler_shows_actual_current_values_not_hardcoded():
    UserService().register_user("918", username="settings_a")
    UserService().change_risk("918", 5.0)
    UserService().change_strategy("918", "AMD")
    UserService().change_timeframe("918", "H1")

    text = _run(settings_handler("918"))

    assert "5%" in text
    assert "AMD" in text
    assert "H1" in text


def test_settings_handler_falls_back_to_na_for_unregistered_caller():
    text = _run(settings_handler("999999999999"))
    assert "N/A" in text


# ---------------------------------------------------------------------------
# Regression -- existing text-command shape (str, not a result object)
# stays intact for every *_handler(), matching the CLAUDE.md "no breaking
# changes" restriction.
# ---------------------------------------------------------------------------


def test_all_setting_handlers_still_return_plain_strings():
    UserService().register_user("919", username="regression")
    assert isinstance(_run(risk_handler("919", args=None)), str)
    assert isinstance(_run(strategy_handler("919", args=None)), str)
    assert isinstance(_run(timeframe_handler("919", args=None)), str)
    assert isinstance(_run(notifications_handler("919", args=None)), str)
