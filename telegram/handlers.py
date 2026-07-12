"""
Telegram Layer — command handler skeletons.

Future shape:

    Telegram Message -> Handler -> Service -> Database/Core

Each handler below is an empty async stub, one per entry in
commands.py. No business logic, no aiogram Dispatcher registration,
no service calls yet -- wiring to user_service.py / admin_service.py /
result_handler.py belongs to a later phase.

Note for that later phase: Notifier.send_message() runs its own
asyncio.run() internally, so it must not be called directly from
inside these (already-async) handlers once real logic is added --
the same nested-event-loop crash found and fixed in main.py (Phase
31.1) would reoccur. Handlers should talk to TelegramBot directly
(await bot.send_message(...)) or to a future async-native service.
"""


async def start_handler():
    pass


async def help_handler():
    pass


async def profile_handler():
    pass


async def signal_handler():
    pass


async def history_handler():
    pass


async def admin_handler():
    pass
