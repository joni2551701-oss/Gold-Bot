"""
Telegram Layer — live polling entry point (Phase 36).

Responsibility: create the aiogram Bot used to RECEIVE updates, wire
an aiogram Dispatcher to it, and start long-polling. Every incoming
message is handed to telegram.command_router.route_message(), which
does the actual command -> handler -> service -> database work. No
business logic lives here -- this module only starts the listener and
forwards updates.

    Telegram User -> Aiogram Dispatcher -> polling.py
        -> command_router.route_message() -> handlers.py -> services -> database

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
"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from core.secrets import Secrets
from core.logger import setup_logger
from telegram.command_router import route_message

logger = setup_logger("TelegramPolling")


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
            result = await route_message(message)
        except Exception as e:
            # Defense in depth: route_message() already catches handler
            # errors internally, but a malformed update (e.g. missing
            # from_user) must not crash the polling loop either.
            logger.warning(f"route_message failed: {e}")
            await message.answer("Service temporarily unavailable.")
            return

        await message.answer(result.text, reply_markup=result.keyboard)

    return dispatcher


async def run_polling() -> None:
    """
    Creates the inbound Bot, wires the Dispatcher, and starts
    long-polling. Blocks until stopped. A per-update failure is caught
    inside _on_message above, so one bad update cannot kill the loop.
    """
    try:
        token = Secrets().TELEGRAM_BOT_TOKEN
    except Exception as e:
        logger.error(f"Cannot start polling: {e}")
        return

    bot = Bot(token=token)
    dispatcher = create_dispatcher()

    logger.info("Telegram polling started.")
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Telegram polling stopped.")


def main() -> None:
    asyncio.run(run_polling())


if __name__ == "__main__":
    main()
