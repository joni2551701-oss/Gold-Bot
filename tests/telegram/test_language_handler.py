"""
Telegram Layer -- Language module handler tests (V1.1 Language UX
Polish). telegram.handlers.language_status()/language_handler() are
exercised against the real UserService/UserRepository (same pattern
tests/telegram/test_phone_registration.py already uses) rather than
mocks, since telegram.user_service.UserService owns no branching this
phase needs to fake around.
"""

import asyncio

from telegram.handlers import language_handler, language_status
from telegram.user_service import UserService


def _run(coro):
    return asyncio.run(coro)


def test_language_status_no_args_shows_current_language_default_uz():
    UserService().register_user("601", username="a")
    result = _run(language_status("601", args=None))

    assert "🇺🇿 Uzbek" in result.text
    assert result.show_keyboard is True


def test_language_status_no_args_reflects_a_previously_changed_language():
    UserService().register_user("602", username="b")
    UserService().change_language("602", "RU")

    result = _run(language_status("602", args=None))
    assert "🇷🇺 Русский" in result.text


def test_language_status_invalid_choice_keeps_keyboard_and_does_not_change_language():
    UserService().register_user("603", username="c")
    result = _run(language_status("603", args="XX"))

    assert "Invalid language" in result.text
    assert result.show_keyboard is True
    assert UserService().get_profile("603").profile.language == "UZ"


def test_language_status_successful_update_removes_keyboard_and_persists():
    UserService().register_user("604", username="d")
    result = _run(language_status("604", args="RU"))

    assert result.show_keyboard is False
    assert "✅ Language updated" in result.text
    assert "🇷🇺 Русский" in result.text
    assert UserService().get_profile("604").profile.language == "RU"


def test_language_status_reselecting_current_language_is_a_no_op():
    UserService().register_user("605", username="e")
    UserService().change_language("605", "EN")

    result = _run(language_status("605", args="EN"))

    assert "Already selected" in result.text
    assert "🇬🇧 English" in result.text
    assert result.show_keyboard is True
    # still EN -- update_settings was never called a second time
    assert UserService().get_profile("605").profile.language == "EN"


def test_language_status_unknown_telegram_id_reports_a_friendly_error():
    result = _run(language_status("999999999", args="RU"))

    assert result.text == "Unable to update language.\nPlease try again."
    assert result.show_keyboard is True


def test_language_handler_returns_plain_text_wrapper():
    UserService().register_user("606", username="f")
    text = _run(language_handler("606", args="UZ"))

    assert isinstance(text, str)
    assert "Already selected" in text  # UZ is the DB default


def test_language_handler_lowercase_argument_is_normalized():
    UserService().register_user("607", username="g")
    text = _run(language_handler("607", args="ru"))

    assert "✅ Language updated" in text
    assert UserService().get_profile("607").profile.language == "RU"
