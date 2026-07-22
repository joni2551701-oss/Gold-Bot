"""
Telegram Layer — callback_query router (V1 Language Callback Fix).

telegram/polling.py only forwards `callback_query` updates here; it
never branches on `callback.data` itself, keeping polling.py a thin
transport layer with no business logic -- the same shape
command_router.py already gives text-command dispatch.

route_callback() is the single entry point. It translates a
callback_data string into a call to the *same* handlers.*_handler()
function (or, for language, the richer handlers.language_status()) the
equivalent text command already uses -- e.g. "lang_uz" resolves to
what "/language UZ" resolves to. No new business logic exists in this
file, only that translation, matching the "one backend, two entry
points" principle already used for text-command vs future-Menu-Button
dispatch (both funnel into command_router.route_command()).

Scope (V1 Language Callback Fix; UX polished in V1.1 Language UX
Polish): only the lang_uz/lang_ru/lang_en callbacks from
telegram.keyboards.language_keyboard() are implemented. Every other
keyboard's callback_data (risk_*, timeframe_*, strategy_*,
notifications_*, settings_*, admin_*) is recognized here as a category
ready for a future phase, but not yet handled -- callback.answer() is
still called for them (so the Telegram client's loading spinner
clears), matching every not-yet-implemented command elsewhere in this
codebase staying honestly inert rather than fabricating behavior.
"""

from aiogram.types import CallbackQuery

from telegram import handlers
from telegram.keyboards import language_keyboard
from core.logger import setup_logger

logger = setup_logger("CallbackRouter")

_LANGUAGE_CALLBACKS = {
    "lang_uz": "UZ",
    "lang_ru": "RU",
    "lang_en": "EN",
}

# Recognized-but-not-yet-implemented callback_data prefixes (future
# phases add a branch here, same shape as _handle_language below --
# never a second dispatch mechanism).
_RECOGNIZED_PREFIXES = (
    "lang_",
    "risk_",
    "strategy_",
    "timeframe_",
    "notifications_",
    "settings_",
    "admin_",
)


async def route_callback(callback: CallbackQuery) -> None:
    """
    Routes an incoming callback_query to the same handler its
    equivalent text command already uses. Never raises: an
    unrecognized, not-yet-implemented, or failing callback is answered
    (clears the Telegram client's spinner) and otherwise produces no
    visible error, the same "never raises" contract every
    telegram/handlers.py function already keeps.
    """
    data = callback.data or ""

    try:
        if data in _LANGUAGE_CALLBACKS:
            await _handle_language(callback, _LANGUAGE_CALLBACKS[data])
            return

        # Recognized category, not yet implemented -- clear the
        # spinner, do nothing else.
        await callback.answer()
    except Exception as e:
        logger.warning(f"route_callback failed for data={data!r}: {e}")
        try:
            await callback.answer()
        except Exception:
            pass


async def _handle_language(callback: CallbackQuery, language: str) -> None:
    """
    lang_uz/lang_ru/lang_en -> handlers.language_status() (V1.1
    Language UX Polish), then edit the prompt message in place rather
    than sending a new one: the language-choice keyboard's only job
    was choosing a language, so once chosen its message is stale --
    editing it to show the result leaves one clean confirmation
    instead of a dead keyboard plus a separate new message. Falls back
    to a new message if edit_text fails (e.g. the prompt message is
    too old for Telegram to allow editing, or was deleted) -- same
    never-raises posture as every other handler here.

    The picker keyboard is removed once a language change actually
    took effect (result.show_keyboard is False) -- its job is done, so
    leaving tappable buttons under a "language updated" confirmation
    would invite an accidental re-tap. It stays attached for every
    other outcome (invalid input, re-picking the current language, an
    update failure) since those are all still-open states the caller
    may reasonably want to act on again.
    """
    telegram_id = callback.from_user.id
    result = await handlers.language_status(telegram_id, args=language)
    await callback.answer()
    reply_markup = language_keyboard(language) if result.show_keyboard else None
    try:
        await callback.message.edit_text(result.text, reply_markup=reply_markup)
    except Exception as e:
        logger.warning(f"route_callback: edit_text failed, sending new message instead: {e}")
        await callback.message.answer(result.text, reply_markup=reply_markup)
