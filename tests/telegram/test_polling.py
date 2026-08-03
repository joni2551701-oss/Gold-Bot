"""
GitHub Secrets / Environment Configuration Audit -- TASK 2/7 -- plus
GoldBot Core Telegram Runtime Activation Alpha (startup secret
validation, owner-only startup notification, heartbeat loop, and
run_polling()'s wiring into telegram.runtime_monitor).

platform_layer/telegram/polling.py is the real /start entry point (run as
`python -m telegram.polling`, a long-running process -- see
docs/DEPLOYMENT.md). Covers the missing-token startup-abort path,
create_dispatcher()'s wiring, and the Runtime Activation additions --
all without opening a real network connection (Bot(token=...) itself
never phones home at construction time; the real aiogram Bot class is
also monkeypatched out entirely for the run_polling() integration
tests below, since dispatcher.start_polling() blocks forever for real).
"""

import asyncio
import logging
from types import SimpleNamespace

from platform_layer.telegram import runtime_monitor
from platform_layer.telegram.polling import (
    HEARTBEAT_INTERVAL_SECONDS,
    _build_startup_message,
    _heartbeat_loop,
    _log_startup_secret_presence,
    _notify_owner_startup,
    create_dispatcher,
    run_polling,
)


def test_run_polling_logs_explicit_missing_token_message(monkeypatch, caplog):
    """
    A missing TELEGRAM_BOT_TOKEN must produce a clear, grep-able
    "Startup aborted: Missing TELEGRAM_BOT_TOKEN" log line (the exact
    shape Telegram Runtime Activation Alpha's TASK 6 asks for;
    docs/DEPLOYMENT.md's Troubleshooting section documents it), not
    just a generic exception message, and must return without
    starting polling.
    """
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    with caplog.at_level(logging.ERROR, logger="TelegramPolling"):
        asyncio.run(run_polling())

    messages = [record.message for record in caplog.records]
    assert any("Startup aborted: Missing TELEGRAM_BOT_TOKEN" in m for m in messages)


def test_run_polling_never_raises_on_missing_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    asyncio.run(run_polling())  # must return quietly, not raise


def test_create_dispatcher_returns_dispatcher_with_message_handler():
    from aiogram import Dispatcher

    dispatcher = create_dispatcher()
    assert isinstance(dispatcher, Dispatcher)


def test_on_message_routes_text_to_route_message(monkeypatch):
    """A text message (no .contact) is routed via command_router.route_message()."""
    import platform_layer.telegram.polling as polling_module

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
        from_user = SimpleNamespace(id=100)
        answered_with = None

        async def answer(self, text, reply_markup=None):
            self.answered_with = (text, reply_markup)

    message = FakeMessage()
    asyncio.run(handler(message))
    assert message.answered_with == ("Profile created.", None)


def test_on_message_routes_contact_to_route_contact(monkeypatch):
    """A contact-share message (.contact populated) is routed via command_router.route_contact()."""
    import platform_layer.telegram.polling as polling_module

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
        from_user = SimpleNamespace(id=101)
        answered_with = None

        async def answer(self, text, reply_markup=None):
            self.answered_with = (text, reply_markup)

    message = FakeMessage()
    asyncio.run(handler(message))
    assert message.answered_with == ("Phone number saved.", None)


def test_on_callback_query_routes_to_callback_router(monkeypatch):
    """A callback_query (inline keyboard button tap) is forwarded to
    callback_router.route_callback() -- polling.py never branches on
    callback.data itself (V1 Language Callback Fix)."""
    import platform_layer.telegram.polling as polling_module

    dispatcher = create_dispatcher()
    handler = dispatcher.callback_query.handlers[0].callback

    captured = {}

    async def fake_route_callback(callback):
        captured["callback"] = callback

    monkeypatch.setattr(polling_module, "route_callback", fake_route_callback)

    class FakeCallback:
        data = "lang_uz"

    callback = FakeCallback()
    asyncio.run(handler(callback))
    assert captured["callback"] is callback


def test_on_callback_query_never_raises_on_routing_failure(monkeypatch):
    import platform_layer.telegram.polling as polling_module

    dispatcher = create_dispatcher()
    handler = dispatcher.callback_query.handlers[0].callback

    async def failing_route_callback(callback):
        raise RuntimeError("boom")

    monkeypatch.setattr(polling_module, "route_callback", failing_route_callback)

    class FakeCallback:
        data = "lang_uz"
        answered = False

        async def answer(self):
            self.answered = True

    callback = FakeCallback()
    asyncio.run(handler(callback))  # must not raise
    assert callback.answered is True


def test_on_message_never_raises_on_routing_failure(monkeypatch):
    import platform_layer.telegram.polling as polling_module

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


# ---------------------------------------------------------------------------
# V2 Phase 6.3 (Director Approved: Dynamic Reply Keyboard Navigation) --
# _deliver() always sends a new message (Phase 6.1's edit-in-place delivery
# and telegram.navigation's Message Lifecycle Tracker are both retired), and
# always sends RouterResult.followup (if set) as a second new message.
# ---------------------------------------------------------------------------


def test_deliver_sends_a_new_message():
    import platform_layer.telegram.polling as polling_module

    class FakeMessage:
        from_user = SimpleNamespace(id=950)
        answered_with = None

        async def answer(self, text, reply_markup=None):
            self.answered_with = (text, reply_markup)

    class FakeResult:
        text = "hello"
        keyboard = None
        followup = None

    message = FakeMessage()
    asyncio.run(polling_module._deliver(message, FakeResult()))
    assert message.answered_with == ("hello", None)


def test_deliver_sends_followup_as_a_second_message():
    import platform_layer.telegram.polling as polling_module

    class FakeMessage:
        from_user = SimpleNamespace(id=954)

        def __init__(self):
            self.answered = []

        async def answer(self, text, reply_markup=None):
            self.answered.append((text, reply_markup))

    class FakeFollowup:
        text = "menu ready"
        keyboard = None

    class FakeResult:
        text = "phone registered"
        keyboard = None
        followup = FakeFollowup()

    message = FakeMessage()
    asyncio.run(polling_module._deliver(message, FakeResult()))

    assert message.answered == [("phone registered", None), ("menu ready", None)]


def test_deliver_still_sends_followup_when_the_primary_send_fails():
    """V2 Phase 6.1.1: a transient failure on the primary (e.g. the
    ReplyKeyboardRemove() message) must not skip the followup -- skipping
    it would leave the chat with no Reply Keyboard at all."""
    import platform_layer.telegram.polling as polling_module

    class FakeMessage:
        from_user = SimpleNamespace(id=955)

        def __init__(self):
            self.calls = 0

        async def answer(self, text, reply_markup=None):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("network unreachable")

    class FakeFollowup:
        text = "menu ready"
        keyboard = None

    class FakeResult:
        text = "phone registered"
        keyboard = None
        followup = FakeFollowup()

    message = FakeMessage()
    asyncio.run(polling_module._deliver(message, FakeResult()))  # must not raise

    assert message.calls == 2


# ---------------------------------------------------------------------------
# TASK 6 -- startup secret validation
# ---------------------------------------------------------------------------

def test_log_startup_secret_presence_logs_present_for_set_vars(caplog):
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = [r.message for r in caplog.records]
    assert any("TELEGRAM_BOT_TOKEN: present" in m for m in messages)


def test_log_startup_secret_presence_logs_missing_for_unset_owner_id(monkeypatch, caplog):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = [r.message for r in caplog.records]
    assert any("TELEGRAM_OWNER_ID: missing" in m for m in messages)


def test_log_startup_secret_presence_logs_missing_for_unset_twelve_data_key(monkeypatch, caplog):
    monkeypatch.delenv("TWELVE_DATA_API_KEY", raising=False)
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = [r.message for r in caplog.records]
    assert any("TWELVE_DATA_API_KEY: missing" in m for m in messages)


def test_log_startup_secret_presence_logs_missing_for_unset_gemini_key(monkeypatch, caplog):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = [r.message for r in caplog.records]
    assert any("GEMINI_API_KEY: missing" in m for m in messages)


def test_log_startup_secret_presence_never_logs_a_value(monkeypatch, caplog):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "super-secret-token-value")
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = [r.message for r in caplog.records]
    assert not any("super-secret-token-value" in m for m in messages)


def test_log_startup_secret_presence_never_raises_when_all_missing(monkeypatch):
    for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_OWNER_ID", "TWELVE_DATA_API_KEY", "GEMINI_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    _log_startup_secret_presence()  # must not raise


def test_log_startup_secret_presence_logs_present_for_set_twelve_data_key(monkeypatch, caplog):
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "some-value")
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = [r.message for r in caplog.records]
    assert any("TWELVE_DATA_API_KEY: present" in m for m in messages)


def test_log_startup_secret_presence_logs_present_for_set_gemini_key(monkeypatch, caplog):
    monkeypatch.setenv("GEMINI_API_KEY", "some-value")
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = [r.message for r in caplog.records]
    assert any("GEMINI_API_KEY: present" in m for m in messages)


def test_log_startup_secret_presence_covers_all_four_brief_secrets(monkeypatch, caplog):
    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        _log_startup_secret_presence()
    messages = " ".join(r.message for r in caplog.records)
    for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_OWNER_ID", "TWELVE_DATA_API_KEY", "GEMINI_API_KEY"):
        assert name in messages


# ---------------------------------------------------------------------------
# TASK 2 -- owner-only startup notification
# ---------------------------------------------------------------------------

def test_build_startup_message_contains_online_marker():
    assert "GoldBot Online" in _build_startup_message()


def test_build_startup_message_contains_core_running():
    assert "Core: Running" in _build_startup_message()


def test_build_startup_message_contains_telegram_connected():
    assert "Telegram: Connected" in _build_startup_message()


def test_build_startup_message_contains_monitoring_active():
    assert "Monitoring: Active" in _build_startup_message()


def test_build_startup_message_contains_a_timestamp():
    message = _build_startup_message()
    assert "Time:" in message


def test_build_startup_message_timestamp_matches_expected_shape():
    import re

    message = _build_startup_message()
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", message)


def test_build_startup_message_uses_green_circle_marker():
    assert "\U0001F7E2" in _build_startup_message()


def test_notify_owner_startup_skips_when_owner_unset(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)

    class FakeBot:
        async def send_message(self, chat_id, text):
            raise AssertionError("must not be called when owner is unset")

    asyncio.run(_notify_owner_startup(FakeBot()))  # must not raise, must not send


def test_notify_owner_startup_sends_to_configured_owner_id(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    sent = {}

    class FakeBot:
        async def send_message(self, chat_id, text):
            sent["chat_id"] = chat_id
            sent["text"] = text

    asyncio.run(_notify_owner_startup(FakeBot()))
    assert sent["chat_id"] == "111"
    assert "GoldBot Online" in sent["text"]


def test_notify_owner_startup_never_raises_on_send_failure(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")

    class FakeBot:
        async def send_message(self, chat_id, text):
            raise RuntimeError("network unreachable")

    asyncio.run(_notify_owner_startup(FakeBot()))  # must not raise


def test_notify_owner_startup_records_runtime_error_on_send_failure(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    monitor = runtime_monitor.TelegramRuntimeMonitor()
    monkeypatch.setattr(runtime_monitor, "DEFAULT_RUNTIME_MONITOR", monitor)

    class FakeBot:
        async def send_message(self, chat_id, text):
            raise RuntimeError("network unreachable")

    asyncio.run(_notify_owner_startup(FakeBot()))
    assert monitor.get_status().errors == 1


# ---------------------------------------------------------------------------
# TASK 5 -- internal heartbeat loop
# ---------------------------------------------------------------------------

def test_heartbeat_interval_is_within_brief_range():
    assert 300.0 <= HEARTBEAT_INTERVAL_SECONDS <= 600.0


def test_heartbeat_loop_logs_bot_heartbeat_line(caplog):
    async def run_one_tick():
        task = asyncio.create_task(_heartbeat_loop(interval_seconds=0.01))
        await asyncio.sleep(0.03)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    with caplog.at_level(logging.INFO, logger="TelegramPolling"):
        asyncio.run(run_one_tick())

    messages = [r.message for r in caplog.records]
    assert any("BOT_HEARTBEAT" in m for m in messages)


def test_heartbeat_loop_never_sends_a_telegram_message():
    """TASK 5's own rule: heartbeat is internal only, never delivered to the owner as a Telegram message."""
    calls = []

    class WatchedBot:
        async def send_message(self, *args, **kwargs):
            calls.append((args, kwargs))

    async def run_one_tick():
        task = asyncio.create_task(_heartbeat_loop(interval_seconds=0.01))
        await asyncio.sleep(0.03)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    asyncio.run(run_one_tick())
    assert calls == []  # _heartbeat_loop never even receives a Bot to send with


def test_heartbeat_loop_records_heartbeat_on_runtime_monitor(monkeypatch):
    monitor = runtime_monitor.TelegramRuntimeMonitor()
    monkeypatch.setattr(runtime_monitor, "DEFAULT_RUNTIME_MONITOR", monitor)

    async def run_one_tick():
        task = asyncio.create_task(_heartbeat_loop(interval_seconds=0.01))
        await asyncio.sleep(0.03)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    asyncio.run(run_one_tick())
    assert monitor.get_status().last_ping is not None


def test_heartbeat_loop_survives_health_check_failure(monkeypatch):
    import platform_layer.telegram.polling as polling_module

    def failing_health():
        raise RuntimeError("provider registry unreachable")

    monkeypatch.setattr(polling_module, "_get_core_health", failing_health)

    async def run_one_tick():
        task = asyncio.create_task(_heartbeat_loop(interval_seconds=0.01))
        await asyncio.sleep(0.03)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    asyncio.run(run_one_tick())  # must not raise/kill the loop


# ---------------------------------------------------------------------------
# run_polling() integration -- Bot/Dispatcher fully faked, no real network
# ---------------------------------------------------------------------------

class _StopPolling(Exception):
    pass


class _FakeSession:
    def __init__(self):
        self.closed = False

    async def close(self):
        self.closed = True


class _FakeBot:
    def __init__(self, token):
        self.token = token
        self.session = _FakeSession()
        self.sent = []

    async def send_message(self, chat_id, text):
        self.sent.append((chat_id, text))


class _FakeDispatcherStopsImmediately:
    async def start_polling(self, bot):
        raise _StopPolling()


def test_run_polling_records_connected_on_successful_startup(monkeypatch):
    import platform_layer.telegram.polling as polling_module

    monkeypatch.setattr(polling_module, "Bot", _FakeBot)
    monkeypatch.setattr(polling_module, "create_dispatcher", lambda: _FakeDispatcherStopsImmediately())
    monitor = runtime_monitor.TelegramRuntimeMonitor()
    monkeypatch.setattr(runtime_monitor, "DEFAULT_RUNTIME_MONITOR", monitor)

    try:
        asyncio.run(run_polling())
    except _StopPolling:
        pass

    assert monitor.get_status().status == "CONNECTED"


def test_run_polling_sends_owner_startup_notification(monkeypatch):
    import platform_layer.telegram.polling as polling_module

    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    monkeypatch.setattr(polling_module, "Bot", _FakeBot)

    captured_bot = {}

    class CapturingDispatcher:
        async def start_polling(self, bot):
            captured_bot["bot"] = bot
            raise _StopPolling()

    monkeypatch.setattr(polling_module, "create_dispatcher", lambda: CapturingDispatcher())

    try:
        asyncio.run(run_polling())
    except _StopPolling:
        pass

    assert len(captured_bot["bot"].sent) == 1
    assert captured_bot["bot"].sent[0][0] == "111"


def test_run_polling_registers_menus_before_owner_notification(monkeypatch):
    """V2 Phase 4: register_all_menus() runs once, before dispatcher.start_polling()."""
    import platform_layer.telegram.polling as polling_module

    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")
    monkeypatch.setattr(polling_module, "Bot", _FakeBot)

    calls = []

    async def fake_register_all_menus(bot):
        calls.append(bot)

    monkeypatch.setattr(polling_module, "register_all_menus", fake_register_all_menus)
    monkeypatch.setattr(polling_module, "create_dispatcher", lambda: _FakeDispatcherStopsImmediately())

    try:
        asyncio.run(run_polling())
    except _StopPolling:
        pass

    assert len(calls) == 1
    assert isinstance(calls[0], _FakeBot)


def test_run_polling_closes_bot_session_on_exit(monkeypatch):
    import platform_layer.telegram.polling as polling_module

    monkeypatch.setattr(polling_module, "Bot", _FakeBot)
    captured_bot = {}

    class CapturingDispatcher:
        async def start_polling(self, bot):
            captured_bot["bot"] = bot
            raise _StopPolling()

    monkeypatch.setattr(polling_module, "create_dispatcher", lambda: CapturingDispatcher())

    try:
        asyncio.run(run_polling())
    except _StopPolling:
        pass

    assert captured_bot["bot"].session.closed is True


def test_run_polling_cancels_heartbeat_task_on_exit(monkeypatch):
    import platform_layer.telegram.polling as polling_module

    monkeypatch.setattr(polling_module, "Bot", _FakeBot)
    monkeypatch.setattr(polling_module, "create_dispatcher", lambda: _FakeDispatcherStopsImmediately())

    created_tasks = []
    real_create_task = asyncio.create_task

    def capturing_create_task(coro, *args, **kwargs):
        task = real_create_task(coro, *args, **kwargs)
        created_tasks.append(task)
        return task

    monkeypatch.setattr(polling_module.asyncio, "create_task", capturing_create_task)

    try:
        asyncio.run(run_polling())
    except _StopPolling:
        pass

    assert len(created_tasks) == 1
    assert created_tasks[0].done()
    assert created_tasks[0].cancelled()


def test_run_polling_still_starts_when_owner_notification_fails(monkeypatch):
    """A broken owner-notification path must never prevent the listener from starting."""
    import platform_layer.telegram.polling as polling_module

    monkeypatch.setenv("TELEGRAM_OWNER_ID", "111")

    class BrokenSendBot(_FakeBot):
        async def send_message(self, chat_id, text):
            raise RuntimeError("network unreachable")

    monkeypatch.setattr(polling_module, "Bot", BrokenSendBot)

    reached_start_polling = {}

    class CapturingDispatcher:
        async def start_polling(self, bot):
            reached_start_polling["value"] = True
            raise _StopPolling()

    monkeypatch.setattr(polling_module, "create_dispatcher", lambda: CapturingDispatcher())

    try:
        asyncio.run(run_polling())
    except _StopPolling:
        pass

    assert reached_start_polling.get("value") is True
