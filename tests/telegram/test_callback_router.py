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


class FakeUser:
    def __init__(self, telegram_id):
        self.id = telegram_id


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
    """risk_1/strategy_.../timeframe_.../notifications_.../settings_.../admin_...
    are recognized categories for future phases -- not implemented yet,
    but the spinner must still clear."""
    for data in ("risk_1", "strategy_fvg", "timeframe_h1", "notifications_on", "settings_open", "admin_users"):
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
