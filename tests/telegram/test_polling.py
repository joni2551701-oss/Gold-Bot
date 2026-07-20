"""
GitHub Secrets / Environment Configuration Audit -- TASK 2/7.

telegram/polling.py is the real /start entry point (run as
`python -m telegram.polling`, a long-running process -- see
docs/DEPLOYMENT.md). No test file existed for it before this audit.
Covers the missing-token startup-abort path this audit's TASK 2 fix
touched, and create_dispatcher()'s wiring, without opening a real
network connection (Bot(token=...) itself never phones home at
construction time -- aiogram only calls the network on the first API
request).
"""

import asyncio
import logging

from telegram.polling import create_dispatcher, run_polling


def test_run_polling_logs_explicit_missing_token_message(monkeypatch, caplog):
    """
    TASK 2's fix: a missing TELEGRAM_BOT_TOKEN must produce a clear,
    grep-able "TELEGRAM_BOT_TOKEN missing" / "Bot startup aborted"
    pair of log lines (docs/DEPLOYMENT.md's new Troubleshooting
    section documents these exact strings), not just a generic
    exception message, and must return without starting polling.
    """
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    with caplog.at_level(logging.ERROR, logger="TelegramPolling"):
        asyncio.run(run_polling())

    messages = [record.message for record in caplog.records]
    assert any("TELEGRAM_BOT_TOKEN missing" in m for m in messages)
    assert any("Bot startup aborted" in m for m in messages)


def test_run_polling_never_raises_on_missing_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    asyncio.run(run_polling())  # must return quietly, not raise


def test_create_dispatcher_returns_dispatcher_with_message_handler():
    from aiogram import Dispatcher

    dispatcher = create_dispatcher()
    assert isinstance(dispatcher, Dispatcher)


def test_on_message_routes_text_to_route_message(monkeypatch):
    """A text message (no .contact) is routed via command_router.route_message()."""
    import telegram.polling as polling_module

    dispatcher = create_dispatcher()
    handler = dispatcher.message.handlers[0].callback

    class FakeResult:
        text = "Profile created."
        keyboard = None

    async def fake_route_message(message):
        return FakeResult()

    monkeypatch.setattr(polling_module, "route_message", fake_route_message)

    class FakeMessage:
        contact = None
        text = "/start"
        answered_with = None

        async def answer(self, text, reply_markup=None):
            self.answered_with = (text, reply_markup)

    message = FakeMessage()
    asyncio.run(handler(message))
    assert message.answered_with == ("Profile created.", None)


def test_on_message_routes_contact_to_route_contact(monkeypatch):
    """A contact-share message (.contact populated) is routed via command_router.route_contact()."""
    import telegram.polling as polling_module

    dispatcher = create_dispatcher()
    handler = dispatcher.message.handlers[0].callback

    class FakeResult:
        text = "Phone number saved."
        keyboard = None

    async def fake_route_contact(message):
        return FakeResult()

    monkeypatch.setattr(polling_module, "route_contact", fake_route_contact)

    class FakeContact:
        phone_number = "+1234567890"

    class FakeMessage:
        contact = FakeContact()
        text = None
        answered_with = None

        async def answer(self, text, reply_markup=None):
            self.answered_with = (text, reply_markup)

    message = FakeMessage()
    asyncio.run(handler(message))
    assert message.answered_with == ("Phone number saved.", None)


def test_on_message_never_raises_on_routing_failure(monkeypatch):
    import telegram.polling as polling_module

    dispatcher = create_dispatcher()
    handler = dispatcher.message.handlers[0].callback

    async def failing_route_message(message):
        raise RuntimeError("boom")

    monkeypatch.setattr(polling_module, "route_message", failing_route_message)

    class FakeMessage:
        contact = None
        text = "/start"
        answered_with = None

        async def answer(self, text, reply_markup=None):
            self.answered_with = (text, reply_markup)

    message = FakeMessage()
    asyncio.run(handler(message))  # must not raise
    assert message.answered_with[0] == "Service temporarily unavailable."
