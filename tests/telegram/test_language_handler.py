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
from telegram.registration_service import RegistrationStep
from database.user_repository import UserRepository


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
    # Rendered in the caller's current (pre-existing) language -- UZ is
    # the DB default for a freshly-registered user.
    UserService().register_user("603", username="c")
    result = _run(language_status("603", args="XX"))

    assert "Noto'g'ri til" in result.text
    assert result.show_keyboard is True
    assert UserService().get_profile("603").profile.language == "UZ"


def test_language_status_successful_update_removes_keyboard_and_persists():
    # Rendered in the newly-selected language (Phase 1.6) -- the
    # confirmation itself proves the switch took effect.
    UserService().register_user("604", username="d")
    result = _run(language_status("604", args="RU"))

    assert result.show_keyboard is False
    assert "✅ Язык обновлён" in result.text
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
    # _current_language() falls back to the DB schema default (UZ) for
    # an unknown telegram_id.
    result = _run(language_status("999999999", args="RU"))

    assert result.text == "Tilni yangilab bo'lmadi.\nQaytadan urinib ko'ring."
    assert result.show_keyboard is True


def test_language_handler_returns_plain_text_wrapper():
    UserService().register_user("606", username="f")
    text = _run(language_handler("606", args="UZ"))

    assert isinstance(text, str)
    assert "Allaqachon tanlangan" in text  # UZ is the DB default


def test_language_handler_lowercase_argument_is_normalized():
    UserService().register_user("607", username="g")
    text = _run(language_handler("607", args="ru"))

    assert "✅ Язык обновлён" in text
    assert UserService().get_profile("607").profile.language == "RU"


# ---------------------------------------------------------------------------
# V2 Phase 3.1 -- /language's text-command path (language_handler) must
# advance the Registration Wizard past LANGUAGE exactly like tapping the
# inline picker button already does (telegram/callback_router.py's
# _handle_language()), so a user who types the command instead of tapping
# is not left stuck being re-shown the Language step by every /start.
# ---------------------------------------------------------------------------


def test_language_handler_valid_choice_advances_a_mid_wizard_user_to_phone():
    repo = UserRepository()
    repo.create_user("608", username="h")
    assert repo.get_user("608").registration_step == RegistrationStep.LANGUAGE

    _run(language_handler("608", args="RU"))

    assert repo.get_user("608").registration_step == RegistrationStep.PHONE


def test_language_handler_reselecting_the_default_language_still_advances():
    """Mirrors the callback path's own unconditional-on-a-real-selection
    behavior -- UZ is the DB default, so this hits the 'already selected'
    branch, yet the Wizard still advances (a real choice was made)."""
    repo = UserRepository()
    repo.create_user("609", username="i")

    _run(language_handler("609", args="UZ"))

    assert repo.get_user("609").registration_step == RegistrationStep.PHONE


def test_language_handler_no_args_does_not_advance_the_wizard():
    repo = UserRepository()
    repo.create_user("610", username="j")

    _run(language_handler("610", args=None))

    assert repo.get_user("610").registration_step == RegistrationStep.LANGUAGE


def test_language_handler_invalid_choice_does_not_advance_the_wizard():
    repo = UserRepository()
    repo.create_user("611", username="k")

    _run(language_handler("611", args="XX"))

    assert repo.get_user("611").registration_step == RegistrationStep.LANGUAGE


def test_language_handler_does_not_reopen_an_already_completed_registration():
    repo = UserRepository()
    repo.create_user("612", username="l")
    repo.complete_registration("612")

    _run(language_handler("612", args="RU"))

    assert repo.get_user("612").registration_step == RegistrationStep.COMPLETE
