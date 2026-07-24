"""
Telegram Layer -- callback_query router tests (V1 Language Callback
Fix; UX behavior extended in V1.1 Language UX Polish).
telegram/callback_router.py translates a callback_data string into the
same handlers.*_handler() call (or, for language, handlers.
language_status()) its equivalent text command already uses -- these
tests verify that translation, the always-call-answer() contract, the
edit-then-fallback UX, the keyboard-removal-on-success behavior, and
that a recognized-but-not-yet-implemented or entirely unrecognized
callback_data never raises and never fabricates behavior.
"""

import asyncio

from telegram.callback_router import route_callback
from telegram.handlers import LanguageUpdateResult
from database.user_repository import UserRepository
from telegram.registration_service import RegistrationStep


class FakeUser:
    def __init__(self, telegram_id, username=None):
        self.id = telegram_id
        self.username = username


class FakeMessage:
    def __init__(self):
        self.edited_with = None
        self.edited_with_markup = "NOT_SET"
        self.answered_with = None
        self.answered_with_markup = "NOT_SET"
        self.edit_should_fail = False

    async def edit_text(self, text, reply_markup=None):
        if self.edit_should_fail:
            raise RuntimeError("message too old to edit")
        self.edited_with = text
        self.edited_with_markup = reply_markup

    async def answer(self, text, reply_markup=None):
        self.answered_with = text
        self.answered_with_markup = reply_markup


class FakeCallback:
    def __init__(self, data, telegram_id=2031615956):
        self.data = data
        self.from_user = FakeUser(telegram_id)
        self.message = FakeMessage()
        self.answered = False
        self.answer_should_fail = False

    async def answer(self):
        if self.answer_should_fail:
            raise RuntimeError("network error")
        self.answered = True


def _patch_language_status(monkeypatch, fake):
    import telegram.callback_router as router_module

    monkeypatch.setattr(router_module.handlers, "language_status", fake)


def test_route_callback_lang_uz_calls_language_status_with_UZ(monkeypatch):
    captured = {}

    async def fake_language_status(telegram_id=None, args=None):
        captured["telegram_id"] = telegram_id
        captured["args"] = args
        return LanguageUpdateResult(text="✅ Language updated\nCurrent language:\n🇺🇿 Uzbek", show_keyboard=False)

    _patch_language_status(monkeypatch, fake_language_status)

    callback = FakeCallback("lang_uz", telegram_id=2031615956)
    asyncio.run(route_callback(callback))

    assert captured["telegram_id"] == 2031615956
    assert captured["args"] == "UZ"


def test_route_callback_lang_ru_calls_language_status_with_RU(monkeypatch):
    captured = {}

    async def fake_language_status(telegram_id=None, args=None):
        captured["args"] = args
        return LanguageUpdateResult(text="✅ Language updated\nCurrent language:\n🇷🇺 Русский", show_keyboard=False)

    _patch_language_status(monkeypatch, fake_language_status)

    asyncio.run(route_callback(FakeCallback("lang_ru")))
    assert captured["args"] == "RU"


def test_route_callback_lang_en_calls_language_status_with_EN(monkeypatch):
    captured = {}

    async def fake_language_status(telegram_id=None, args=None):
        captured["args"] = args
        return LanguageUpdateResult(text="✅ Language updated\nCurrent language:\n🇬🇧 English", show_keyboard=False)

    _patch_language_status(monkeypatch, fake_language_status)

    asyncio.run(route_callback(FakeCallback("lang_en")))
    assert captured["args"] == "EN"


def test_route_callback_language_edits_the_prompt_message_in_place(monkeypatch):
    async def fake_language_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="✅ Language updated\nCurrent language:\n🇺🇿 Uzbek", show_keyboard=False)

    _patch_language_status(monkeypatch, fake_language_status)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))

    assert callback.message.edited_with == "✅ Language updated\nCurrent language:\n🇺🇿 Uzbek"
    assert callback.message.answered_with is None  # no separate new message sent


def test_route_callback_language_removes_keyboard_on_successful_update(monkeypatch):
    async def fake_language_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="✅ Language updated\nCurrent language:\n🇷🇺 Русский", show_keyboard=False)

    _patch_language_status(monkeypatch, fake_language_status)

    callback = FakeCallback("lang_ru")
    asyncio.run(route_callback(callback))

    assert callback.message.edited_with_markup is None


def test_route_callback_language_keeps_keyboard_when_already_selected(monkeypatch):
    async def fake_language_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="Already selected\n🇺🇿 Uzbek", show_keyboard=True)

    _patch_language_status(monkeypatch, fake_language_status)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))

    assert callback.message.edited_with == "Already selected\n🇺🇿 Uzbek"
    assert callback.message.edited_with_markup is not None


def test_route_callback_language_keeps_keyboard_on_update_error(monkeypatch):
    async def fake_language_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="Unable to update language.\nPlease try again.", show_keyboard=True)

    _patch_language_status(monkeypatch, fake_language_status)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))

    assert callback.message.edited_with_markup is not None


def test_route_callback_language_falls_back_to_new_message_if_edit_fails(monkeypatch):
    async def fake_language_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="✅ Language updated\nCurrent language:\n🇺🇿 Uzbek", show_keyboard=False)

    _patch_language_status(monkeypatch, fake_language_status)

    callback = FakeCallback("lang_uz")
    callback.message.edit_should_fail = True
    asyncio.run(route_callback(callback))

    assert callback.message.answered_with == "✅ Language updated\nCurrent language:\n🇺🇿 Uzbek"
    assert callback.message.answered_with_markup is None


def test_route_callback_language_always_calls_answer(monkeypatch):
    async def fake_language_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="✅ Language updated\nCurrent language:\n🇺🇿 Uzbek", show_keyboard=False)

    _patch_language_status(monkeypatch, fake_language_status)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))
    assert callback.answered is True


def test_route_callback_never_raises_when_language_status_fails(monkeypatch):
    async def failing_language_status(telegram_id=None, args=None):
        raise RuntimeError("database error")

    _patch_language_status(monkeypatch, failing_language_status)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))  # must not raise
    assert callback.answered is True  # spinner still cleared


def test_route_callback_never_raises_when_answer_itself_fails(monkeypatch):
    async def failing_language_status(telegram_id=None, args=None):
        raise RuntimeError("database error")

    _patch_language_status(monkeypatch, failing_language_status)

    callback = FakeCallback("lang_uz")
    callback.answer_should_fail = True
    asyncio.run(route_callback(callback))  # must not raise


def test_route_callback_recognized_but_unimplemented_prefix_just_answers():
    """settings_.../admin_... are recognized categories for future
    phases -- not implemented yet, but the spinner must still clear.
    risk_*/strategy_*/timeframe_*/notifications_* were moved out of
    this list by V2 Phase 6.2 (Settings Callback Completion) -- they
    are wired now, see the section below."""
    for data in ("settings_open", "admin_users"):
        callback = FakeCallback(data)
        asyncio.run(route_callback(callback))
        assert callback.answered is True, f"{data} must still call answer()"
        assert callback.message.edited_with is None
        assert callback.message.answered_with is None


def test_route_callback_unrecognized_data_just_answers():
    callback = FakeCallback("totally_unknown_callback")
    asyncio.run(route_callback(callback))
    assert callback.answered is True
    assert callback.message.edited_with is None


def test_route_callback_handles_none_data_without_raising():
    callback = FakeCallback(None)
    asyncio.run(route_callback(callback))  # must not raise
    assert callback.answered is True


# ---------------------------------------------------------------------------
# V2 Phase 3 -- a language choice mid-Wizard advances registration_step and
# prompts the now-mandatory Phone Share step. Uses the real handlers.
# language_status()/UserService (not mocked) since the point is to verify
# real cross-module wiring, not just callback_router's own dispatch shape.
# ---------------------------------------------------------------------------


def test_lang_uz_mid_wizard_advances_step_and_prompts_phone_share():
    repo = UserRepository()
    repo.create_user("801", username="wizard_user")
    assert repo.get_user("801").registration_step == RegistrationStep.LANGUAGE

    callback = FakeCallback("lang_uz", telegram_id="801")
    asyncio.run(route_callback(callback))

    assert repo.get_user("801").registration_step == RegistrationStep.PHONE
    assert callback.message.answered_with is not None
    assert callback.message.answered_with_markup is not None


def test_lang_uz_after_registration_complete_does_not_reopen_the_wizard():
    repo = UserRepository()
    repo.create_user("802", username="done_user")
    repo.complete_registration("802")

    callback = FakeCallback("lang_ru", telegram_id="802")
    asyncio.run(route_callback(callback))

    assert repo.get_user("802").registration_step == RegistrationStep.COMPLETE
    # No extra Phone Share prompt sent -- only the edit-in-place from
    # _handle_language() itself, no separate answer() call for the Wizard.
    assert callback.message.answered_with is None


# ---------------------------------------------------------------------------
# V2 Phase 6.2 -- Settings Callback Completion. risk_*/strategy_*/
# timeframe_*/notifications_* are dispatched through _handle_setting(),
# reusing the matching handlers.*_status() the equivalent text command
# already uses -- mirrors the _handle_language() tests above, plus the
# Stage 6 Inline UX contract (keyboard always reattached, "✅ Saved"
# appended only on a real update) that language deliberately does not
# share (its keyboard is removed on success instead).
# ---------------------------------------------------------------------------


def _patch_status(monkeypatch, name, fake):
    import telegram.callback_router as router_module

    monkeypatch.setattr(router_module.handlers, name, fake)


def test_route_callback_risk_calls_risk_status_with_parsed_choice(monkeypatch):
    captured = {}

    async def fake_risk_status(telegram_id=None, args=None):
        captured["telegram_id"] = telegram_id
        captured["args"] = args
        return LanguageUpdateResult(text="Risk updated to 3%.", show_keyboard=False)

    _patch_status(monkeypatch, "risk_status", fake_risk_status)

    asyncio.run(route_callback(FakeCallback("risk_3", telegram_id=2031615956)))

    assert captured["telegram_id"] == 2031615956
    assert captured["args"] == "3"


def test_route_callback_strategy_converts_underscore_slug_to_space_separated_choice(monkeypatch):
    captured = {}

    async def fake_strategy_status(telegram_id=None, args=None):
        captured["args"] = args
        return LanguageUpdateResult(text="Strategy updated to FVG.", show_keyboard=False)

    _patch_status(monkeypatch, "strategy_status", fake_strategy_status)

    asyncio.run(route_callback(FakeCallback("strategy_liquidity_sweep")))
    assert captured["args"] == "liquidity sweep"


def test_route_callback_timeframe_calls_timeframe_status_with_parsed_choice(monkeypatch):
    captured = {}

    async def fake_timeframe_status(telegram_id=None, args=None):
        captured["args"] = args
        return LanguageUpdateResult(text="Timeframe updated to H1.", show_keyboard=False)

    _patch_status(monkeypatch, "timeframe_status", fake_timeframe_status)

    asyncio.run(route_callback(FakeCallback("timeframe_h1")))
    assert captured["args"] == "h1"


def test_route_callback_notifications_calls_notifications_status_with_parsed_choice(monkeypatch):
    captured = {}

    async def fake_notifications_status(telegram_id=None, args=None):
        captured["args"] = args
        return LanguageUpdateResult(text="Notifications enabled.", show_keyboard=False)

    _patch_status(monkeypatch, "notifications_status", fake_notifications_status)

    asyncio.run(route_callback(FakeCallback("notifications_on")))
    assert captured["args"] == "on"


def test_route_callback_setting_keeps_keyboard_attached_on_success(monkeypatch):
    """Unlike the language picker, a settings picker keyboard is never
    removed -- Director's Stage 6 Inline UX requirement."""

    async def fake_risk_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="Risk updated to 3%.", show_keyboard=False)

    _patch_status(monkeypatch, "risk_status", fake_risk_status)

    callback = FakeCallback("risk_3")
    asyncio.run(route_callback(callback))

    assert callback.message.edited_with_markup is not None


def test_route_callback_setting_appends_saved_confirmation_on_success(monkeypatch):
    async def fake_risk_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="Risk updated to 3%.", show_keyboard=False)

    _patch_status(monkeypatch, "risk_status", fake_risk_status)

    callback = FakeCallback("risk_3")
    asyncio.run(route_callback(callback))

    assert "Risk updated to 3%." in callback.message.edited_with
    assert "Saved" in callback.message.edited_with or "Saqlandi" in callback.message.edited_with


def test_route_callback_setting_no_saved_confirmation_when_update_did_not_take_effect(monkeypatch):
    async def fake_risk_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="Invalid risk percent.", show_keyboard=True)

    _patch_status(monkeypatch, "risk_status", fake_risk_status)

    callback = FakeCallback("risk_99")
    asyncio.run(route_callback(callback))

    assert callback.message.edited_with == "Invalid risk percent."
    assert callback.message.edited_with_markup is not None


def test_route_callback_setting_falls_back_to_new_message_if_edit_fails(monkeypatch):
    async def fake_risk_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="Risk updated to 3%.", show_keyboard=False)

    _patch_status(monkeypatch, "risk_status", fake_risk_status)

    callback = FakeCallback("risk_3")
    callback.message.edit_should_fail = True
    asyncio.run(route_callback(callback))

    assert callback.message.answered_with is not None
    assert callback.message.answered_with_markup is not None


def test_route_callback_setting_always_calls_answer(monkeypatch):
    async def fake_risk_status(telegram_id=None, args=None):
        return LanguageUpdateResult(text="Risk updated to 3%.", show_keyboard=False)

    _patch_status(monkeypatch, "risk_status", fake_risk_status)

    callback = FakeCallback("risk_3")
    asyncio.run(route_callback(callback))
    assert callback.answered is True


def test_route_callback_never_raises_when_setting_status_fails(monkeypatch):
    async def failing_risk_status(telegram_id=None, args=None):
        raise RuntimeError("database error")

    _patch_status(monkeypatch, "risk_status", failing_risk_status)

    callback = FakeCallback("risk_3")
    asyncio.run(route_callback(callback))  # must not raise
    assert callback.answered is True


# Real DB, not mocked -- same "verify real cross-module wiring" posture
# as test_lang_uz_mid_wizard_advances_step_and_prompts_phone_share above.


def test_risk_callback_persists_to_db_and_reflects_new_current_value():
    repo = UserRepository()
    repo.create_user("803", username="risk_user")

    callback = FakeCallback("risk_2", telegram_id="803")
    asyncio.run(route_callback(callback))

    assert repo.get_user("803").risk_percent == 2.0
    assert callback.message.edited_with_markup is not None


def test_strategy_callback_persists_to_db():
    repo = UserRepository()
    repo.create_user("804", username="strategy_user")

    callback = FakeCallback("strategy_fvg", telegram_id="804")
    asyncio.run(route_callback(callback))

    assert repo.get_user("804").strategy == "FVG"


def test_timeframe_callback_persists_to_db():
    repo = UserRepository()
    repo.create_user("805", username="timeframe_user")

    callback = FakeCallback("timeframe_h4", telegram_id="805")
    asyncio.run(route_callback(callback))

    assert repo.get_user("805").timeframe == "H4"


def test_notifications_callback_persists_to_db():
    repo = UserRepository()
    repo.create_user("806", username="notifications_user")

    callback = FakeCallback("notifications_off", telegram_id="806")
    asyncio.run(route_callback(callback))

    assert repo.get_user("806").notifications_enabled is False
