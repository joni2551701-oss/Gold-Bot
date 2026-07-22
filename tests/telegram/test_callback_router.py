"""
Telegram Layer -- callback_query router tests (V1 Language Callback
Fix). telegram/callback_router.py translates a callback_data string
into the same handlers.*_handler() call its equivalent text command
already uses -- these tests verify that translation, the
always-call-answer() contract, the edit-then-fallback UX, and that a
recognized-but-not-yet-implemented or entirely unrecognized
callback_data never raises and never fabricates behavior.
"""

import asyncio

from telegram.callback_router import route_callback


class FakeUser:
    def __init__(self, telegram_id):
        self.id = telegram_id


class FakeMessage:
    def __init__(self):
        self.edited_with = None
        self.answered_with = None
        self.edit_should_fail = False

    async def edit_text(self, text):
        if self.edit_should_fail:
            raise RuntimeError("message too old to edit")
        self.edited_with = text

    async def answer(self, text, reply_markup=None):
        self.answered_with = text


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


def test_route_callback_lang_uz_calls_language_handler_with_UZ(monkeypatch):
    import telegram.callback_router as router_module

    captured = {}

    async def fake_language_handler(telegram_id=None, args=None):
        captured["telegram_id"] = telegram_id
        captured["args"] = args
        return "Language updated to UZ."

    monkeypatch.setattr(router_module.handlers, "language_handler", fake_language_handler)

    callback = FakeCallback("lang_uz", telegram_id=2031615956)
    asyncio.run(route_callback(callback))

    assert captured["telegram_id"] == 2031615956
    assert captured["args"] == "UZ"


def test_route_callback_lang_ru_calls_language_handler_with_RU(monkeypatch):
    import telegram.callback_router as router_module

    captured = {}

    async def fake_language_handler(telegram_id=None, args=None):
        captured["args"] = args
        return "Language updated to RU."

    monkeypatch.setattr(router_module.handlers, "language_handler", fake_language_handler)

    asyncio.run(route_callback(FakeCallback("lang_ru")))
    assert captured["args"] == "RU"


def test_route_callback_lang_en_calls_language_handler_with_EN(monkeypatch):
    import telegram.callback_router as router_module

    captured = {}

    async def fake_language_handler(telegram_id=None, args=None):
        captured["args"] = args
        return "Language updated to EN."

    monkeypatch.setattr(router_module.handlers, "language_handler", fake_language_handler)

    asyncio.run(route_callback(FakeCallback("lang_en")))
    assert captured["args"] == "EN"


def test_route_callback_language_edits_the_prompt_message_in_place(monkeypatch):
    import telegram.callback_router as router_module

    async def fake_language_handler(telegram_id=None, args=None):
        return "Language updated to UZ."

    monkeypatch.setattr(router_module.handlers, "language_handler", fake_language_handler)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))

    assert callback.message.edited_with == "Language updated to UZ."
    assert callback.message.answered_with is None  # no separate new message sent


def test_route_callback_language_falls_back_to_new_message_if_edit_fails(monkeypatch):
    import telegram.callback_router as router_module

    async def fake_language_handler(telegram_id=None, args=None):
        return "Language updated to UZ."

    monkeypatch.setattr(router_module.handlers, "language_handler", fake_language_handler)

    callback = FakeCallback("lang_uz")
    callback.message.edit_should_fail = True
    asyncio.run(route_callback(callback))

    assert callback.message.answered_with == "Language updated to UZ."


def test_route_callback_language_always_calls_answer(monkeypatch):
    import telegram.callback_router as router_module

    async def fake_language_handler(telegram_id=None, args=None):
        return "Language updated to UZ."

    monkeypatch.setattr(router_module.handlers, "language_handler", fake_language_handler)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))
    assert callback.answered is True


def test_route_callback_never_raises_when_language_handler_fails(monkeypatch):
    import telegram.callback_router as router_module

    async def failing_language_handler(telegram_id=None, args=None):
        raise RuntimeError("database error")

    monkeypatch.setattr(router_module.handlers, "language_handler", failing_language_handler)

    callback = FakeCallback("lang_uz")
    asyncio.run(route_callback(callback))  # must not raise
    assert callback.answered is True  # spinner still cleared


def test_route_callback_never_raises_when_answer_itself_fails(monkeypatch):
    import telegram.callback_router as router_module

    async def failing_language_handler(telegram_id=None, args=None):
        raise RuntimeError("database error")

    monkeypatch.setattr(router_module.handlers, "language_handler", failing_language_handler)

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
