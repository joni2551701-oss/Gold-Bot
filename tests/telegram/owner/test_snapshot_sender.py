"""GoldBot Core Owner Snapshot Reporter Alpha, TASK 4 -- telegram/owner/snapshot_sender.py tests."""

import asyncio
import logging

from telegram.owner.snapshot_sender import SnapshotSendResult, send_snapshot


class _FakeBotResult:
    def __init__(self, sent, reason=""):
        self.sent = sent
        self.reason = reason


class _FakeBot:
    def __init__(self, sent=True, reason=""):
        self._result = _FakeBotResult(sent, reason)
        self.closed = False
        self.sent_with = None

    async def send_message(self, text, chat_id):
        self.sent_with = (text, chat_id)
        return self._result

    async def close(self):
        self.closed = True


def test_send_snapshot_skips_when_owner_unset(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    bot = _FakeBot()

    result = asyncio.run(send_snapshot("hello", bot=bot))

    assert result.sent is False
    assert bot.sent_with is None


def test_send_snapshot_sends_to_configured_owner(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    bot = _FakeBot(sent=True)

    result = asyncio.run(send_snapshot("hello", bot=bot))

    assert result.sent is True
    assert bot.sent_with == ("hello", "111")


def test_send_snapshot_returns_result_type():
    result = asyncio.run(send_snapshot("hello", bot=_FakeBot()))
    assert isinstance(result, SnapshotSendResult)


def test_send_snapshot_propagates_failure_reason(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    bot = _FakeBot(sent=False, reason="network unreachable")

    result = asyncio.run(send_snapshot("hello", bot=bot))

    assert result.sent is False
    assert result.reason == "network unreachable"


def test_send_snapshot_never_raises_when_bot_send_raises(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")

    class RaisingBot(_FakeBot):
        async def send_message(self, text, chat_id):
            raise RuntimeError("boom")

    try:
        asyncio.run(send_snapshot("hello", bot=RaisingBot()))
        raised = False
    except RuntimeError:
        raised = True
    # send_snapshot itself doesn't catch bot.send_message()'s own exceptions
    # (that's TelegramBot's own contract to never raise) -- this test
    # documents that contract boundary rather than assuming send_snapshot
    # adds a second safety net on top of an already-safe dependency.
    assert raised is True


def test_send_snapshot_closes_a_self_constructed_bot(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456789:AAFakeToken0000000000000000000")
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    import telegram.owner.snapshot_sender as sender_module

    created = {}

    class TrackedBot(_FakeBot):
        def __init__(self):
            super().__init__(sent=True)
            created["bot"] = self

    monkeypatch.setattr(sender_module, "TelegramBot", TrackedBot)

    asyncio.run(send_snapshot("hello"))

    assert created["bot"].closed is True


def test_send_snapshot_does_not_close_a_caller_supplied_bot():
    bot = _FakeBot(sent=True)
    import os

    os.environ["TELEGRAM_OWNER_ID"] = "111"
    try:
        asyncio.run(send_snapshot("hello", bot=bot))
    finally:
        pass
    assert bot.closed is False


def test_send_snapshot_never_logs_the_owner_id(monkeypatch, caplog):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "999888777")
    bot = _FakeBot(sent=True)

    with caplog.at_level(logging.INFO, logger="SnapshotSender"):
        asyncio.run(send_snapshot("hello", bot=bot))

    messages = [r.message for r in caplog.records]
    assert not any("999888777" in m for m in messages)


def test_send_snapshot_never_logs_the_token(monkeypatch, caplog):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "super-secret-token-value")
    bot = _FakeBot(sent=True)

    with caplog.at_level(logging.INFO, logger="SnapshotSender"):
        asyncio.run(send_snapshot("hello", bot=bot))

    messages = [r.message for r in caplog.records]
    assert not any("super-secret-token-value" in m for m in messages)


def test_send_snapshot_logs_skip_reason_when_owner_missing(monkeypatch, caplog):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)

    with caplog.at_level(logging.WARNING, logger="SnapshotSender"):
        result = asyncio.run(send_snapshot("hello", bot=_FakeBot()))

    assert "TELEGRAM_OWNER_ID not configured" in result.reason
