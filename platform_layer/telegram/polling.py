"""
Telegram Layer — live polling entry point (Phase 36; startup
notification, heartbeat, and secret validation added by GoldBot Core
Telegram Runtime Activation Alpha).

Responsibility: create the aiogram Bot used to RECEIVE updates, wire
an aiogram Dispatcher to it, and start long-polling. Every incoming
text message is handed to telegram.command_router.route_message(),
which does the actual command -> handler -> service -> database work.
No business logic lives here -- this module only starts the listener
and forwards updates.

A contact-share message (Phase 61.5: AI Production Integration
Foundation, TASK 4 -- the Phone Share Button reply) is structurally
different: `message.contact` is populated and `message.text is None`,
so `route_message()` (which only reads `.text`) would silently
resolve it to "Unknown command." `_on_message` below checks
`message.contact` first and routes it to the new, separate
`command_router.route_contact()` instead -- the one new conditional
this phase adds to this file.

A callback_query (an inline keyboard button tap, e.g.
telegram.keyboards.language_keyboard()'s buttons) is a third,
structurally distinct update type -- neither `.text` nor `.contact`,
so it needs its own Dispatcher registration. `_on_callback_query`
below forwards it, unexamined, to `platform_layer.telegram.callback_router.
route_callback()` (V1 Language Callback Fix) -- this file still
never branches on `callback.data` itself; that translation lives in
callback_router.py, the same separation of concerns route_message()/
route_contact() already keep for text/contact updates.

    Telegram User -> Aiogram Dispatcher -> polling.py
        -> command_router.route_message() -> handlers.py -> services -> database
        -> command_router.route_contact() -> handlers.py -> services -> database (contact messages)
        -> callback_router.route_callback() -> handlers.py -> services -> database (button taps)

This is a separate, standalone entry point from main.py. main.py
(GoldBot) is a scheduled, one-shot pipeline run (Data -> ... ->
Telegram notification) that exits after a single cycle; polling.py is
a long-running process that blocks forever inside dispatcher.start_
polling(). They are two different deployment concerns and are not
wired together -- running both means running two separate processes.

Uses its own aiogram Bot instance, independent of
telegram.bot.TelegramBot / telegram.notifier.Notifier's outbound
notification bot. Inbound polling and outbound signal delivery each
own their own Bot/session and event loop lifecycle, so this module
cannot interfere with the asyncio.run()-per-batch fix from Phase 33.1
(Notifier.send_messages()), and vice versa.

Telegram Runtime Activation Alpha additions (all best-effort, never
able to block/abort the actual polling loop):
- TASK 6: `_log_startup_secret_presence()` logs presence/absence
  (never the value) of every secret named in the brief. Only
  TELEGRAM_BOT_TOKEN actually gates startup -- see
  docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md's #2 for why
  TELEGRAM_OWNER_ID/TWELVE_DATA_API_KEY/GEMINI_API_KEY are visibility-
  only here.
- TASK 2: `_notify_owner_startup()` sends a one-time "GoldBot Online"
  status message to TELEGRAM_OWNER_ID only, once polling actually
  starts. Skipped (not an error) if no owner is configured.
- TASK 5: `_heartbeat_loop()` runs alongside `dispatcher.start_polling()`,
  logging an internal `BOT_HEARTBEAT` line (never sent to the owner)
  every `HEARTBEAT_INTERVAL_SECONDS`.
- TASK 4: all three record into `platform_layer.telegram.runtime_monitor`, this
  phase's own new Telegram-connection-specific status tracker (see
  that module's docstring for why it's separate from
  `core_layer.health_monitor.system_monitor.SystemMonitor`).

V2 Phase 4 (Persistent Menu) addition: `register_all_menus()`
(`platform_layer/telegram/menu_commands.py`) registers Telegram's native Menu Button
command lists once, at startup, before polling begins -- same
one-shot, best-effort, never-blocks-polling posture as every step
above. See that module's own docstring for the USER/ADMIN/OWNER scope
strategy.

V2 Phase 6.1 (Director Approved Navigation Controller) addition,
RETIRED by V2 Phase 6.3 (Director Approved: Dynamic Reply Keyboard
Navigation): `_deliver()` used to edit the chat's last bot message in
place for six "editable" pages. Director's Phase 6.3 decision retires
that mechanism outright -- "Eski xabarlar tahrir qilinmaydi. Yangi
javob yuboriladi" (old messages are never edited; every reply is a new
message) -- so `_deliver()` now always sends a new message, same as
every other reply here, and lets the Reply Keyboard attached to it
(platform_layer/telegram/reply_keyboard_manager.py) carry the navigation instead.
`RouterResult.followup`, if set, is still sent as a second message.
"""

import asyncio
import contextlib
from datetime import datetime, timezone

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, Message

from core_layer.secrets import Secrets
from core_layer.logger.logger import setup_logger
from platform_layer.telegram import runtime_monitor
from platform_layer.telegram.callback_router import route_callback
from platform_layer.telegram.command_router import route_contact, route_message
from platform_layer.telegram.menu_commands import register_all_menus
from core_layer.health_monitor.system_monitor import get_health as _get_core_health

logger = setup_logger("TelegramPolling")

# TASK 5: "Har 5-10 minut" -- 5 minutes, the low end of the brief's
# own stated range.
HEARTBEAT_INTERVAL_SECONDS = 300.0

# TASK 6: every secret name the brief asks to validate at startup.
_STARTUP_SECRET_NAMES = (
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_OWNER_ID",
    "TWELVE_DATA_API_KEY",
    "GEMINI_API_KEY",
)


def create_dispatcher() -> Dispatcher:
    """
    Builds a Dispatcher with a single catch-all message handler that
    delegates everything to command_router.route_message(). Which
    command exists and which handler it maps to is command_router's
    job (backed by telegram.commands.COMMANDS) -- this function does
    not hardcode a command list of its own.
    """
    dispatcher = Dispatcher()

    @dispatcher.message()
    async def _on_message(message: Message) -> None:
        try:
            if message.contact is not None:
                result = await route_contact(message)
            else:
                result = await route_message(message)
        except Exception as e:
            # Defense in depth: route_message()/route_contact() already
            # catch handler errors internally, but a malformed update
            # (e.g. missing from_user) must not crash the polling loop.
            logger.warning(f"message routing failed: {e}")
            await message.answer("Service temporarily unavailable.")
            return

        await _deliver(message, result)

    @dispatcher.callback_query()
    async def _on_callback_query(callback: CallbackQuery) -> None:
        try:
            await route_callback(callback)
        except Exception as e:
            # Defense in depth: route_callback() already catches its own
            # failures internally, but this must never crash the polling
            # loop (same posture as _on_message above).
            logger.warning(f"callback routing failed: {e}")
            try:
                await callback.answer()
            except Exception:
                pass

    return dispatcher


async def _send_new(message: Message, result) -> None:
    """Sends `result` as a brand-new message. Never edits an existing one (V2 Phase 6.3)."""
    await message.answer(result.text, reply_markup=result.keyboard)


async def _deliver(message: Message, result) -> None:
    """
    V2 Phase 6.3 (Director Approved: Dynamic Reply Keyboard Navigation)
    -- every reply is a brand-new message; Phase 6.1's edit-in-place
    delivery is retired outright ("Eski xabarlar tahrir qilinmaydi.
    Yangi javob yuboriladi"). Navigation now happens through the Reply
    Keyboard attached to each reply (platform_layer/telegram/reply_keyboard_manager.py
    decides which one), not through editing a previous message.

    If `result.followup` is set (V2 Phase 6.1 Director Decision 7 --
    only route_contact()'s registration-completion reply sets it
    today: ReplyKeyboardRemove() -> Persistent Reply Keyboard), it is
    always sent as a second, brand-new message after the primary one.
    Each send is wrapped independently so a failure in one never
    silently drops the other (e.g. a transient network error on the
    primary message must not skip the followup, since that would leave
    the chat with no Reply Keyboard at all). `_deliver()` itself never
    raises, matching the never-raises posture _on_message's caller
    already relies on for every other delivery path.
    """
    try:
        await _send_new(message, result)
    except Exception as e:
        logger.warning(f"_deliver: primary send failed for telegram_id={message.from_user.id}: {e}")

    followup = getattr(result, "followup", None)
    if followup is not None:
        try:
            await _send_new(message, followup)
        except Exception as e:
            logger.warning(f"_deliver: followup send failed for telegram_id={message.from_user.id}: {e}")


def _log_startup_secret_presence() -> None:
    """
    TASK 6 -- logs presence/absence of every secret this brief names,
    never the value itself. Only TELEGRAM_BOT_TOKEN gates startup
    (below); the other three are visibility-only, since
    telegram.polling never reads TWELVE_DATA_API_KEY/GEMINI_API_KEY
    directly and TELEGRAM_OWNER_ID already has its own fail-closed
    default in telegram.permissions rather than blocking the listener.
    """
    secrets = Secrets()
    for name in _STARTUP_SECRET_NAMES:
        try:
            present = bool(getattr(secrets, name))
        except Exception:
            present = False
        logger.info(f"{name}: {'present' if present else 'missing'}")


def _build_startup_message() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    return (
        "\U0001F7E2 GoldBot Online\n"
        "Status:\n"
        "Core: Running\n"
        "Telegram: Connected\n"
        "Monitoring: Active\n"
        f"Time:\n{now}"
    )


async def _notify_owner_startup(bot: Bot) -> None:
    """
    TASK 2 -- OWNER-only startup notification. Never raises and never
    blocks polling from starting: a missing owner is a normal skip
    (logged at INFO), a send failure is caught, logged, and relayed
    into telegram.runtime_monitor as a runtime error.
    """
    owner_id = Secrets().TELEGRAM_OWNER_ID  # "" if unset, never raises
    if not owner_id:
        logger.info("Owner startup notification skipped: TELEGRAM_OWNER_ID not set.")
        return

    try:
        await bot.send_message(chat_id=owner_id, text=_build_startup_message())
    except Exception as e:
        logger.warning(f"Owner startup notification failed: {e}")
        runtime_monitor.record_error(f"owner startup notification failed: {e}")


async def _heartbeat_loop(interval_seconds: float = HEARTBEAT_INTERVAL_SECONDS) -> None:
    """
    TASK 5 -- internal-only heartbeat, never sent to the owner as a
    Telegram message. Reuses monitoring.system_monitor.get_health()
    (Core Owner Monitoring Alpha) for the Core/Database checks rather
    than inventing a second health-check writer; a health-check
    failure is recorded as a runtime error, never raised (this loop
    must never crash the polling process).
    """
    while True:
        await asyncio.sleep(interval_seconds)
        try:
            health = _get_core_health()
            core_ok = health.status == "RUNNING"
            database_ok = health.database_status == "OK"
        except Exception as e:
            logger.warning(f"heartbeat health check failed: {e}")
            runtime_monitor.record_error(f"heartbeat health check failed: {e}")
            core_ok = False
            database_ok = False

        runtime_monitor.record_heartbeat()
        logger.info(
            "BOT_HEARTBEAT Telegram=OK "
            f"Core={'OK' if core_ok else 'DOWN'} "
            f"Database={'OK' if database_ok else 'DOWN'}"
        )


async def run_polling() -> None:
    """
    Creates the inbound Bot, wires the Dispatcher, and starts
    long-polling. Blocks until stopped. A per-update failure is caught
    inside _on_message above, so one bad update cannot kill the loop.
    """
    _log_startup_secret_presence()

    try:
        token = Secrets().TELEGRAM_BOT_TOKEN
    except Exception:
        # Deliberately explicit and grep-able: an operator scanning
        # journald/GitHub Actions logs for "why isn't the bot
        # responding" needs the missing variable name and the fact
        # that startup was aborted (not silently degraded), in the
        # exact "Startup aborted: Missing X" shape TASK 6 asks for.
        logger.error("Startup aborted: Missing TELEGRAM_BOT_TOKEN")
        return

    bot = Bot(token=token)
    dispatcher = create_dispatcher()
    runtime_monitor.record_connected()

    logger.info("Telegram polling started.")
    heartbeat_task = asyncio.create_task(_heartbeat_loop())
    try:
        await register_all_menus(bot)
        await _notify_owner_startup(bot)
        await dispatcher.start_polling(bot)
    finally:
        heartbeat_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await heartbeat_task
        await bot.session.close()
        logger.info("Telegram polling stopped.")


def main() -> None:
    asyncio.run(run_polling())


if __name__ == "__main__":
    main()
