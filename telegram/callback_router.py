"""
Telegram Layer — callback_query router (V1 Language Callback Fix).

telegram/polling.py only forwards `callback_query` updates here; it
never branches on `callback.data` itself, keeping polling.py a thin
transport layer with no business logic -- the same shape
command_router.py already gives text-command dispatch.

route_callback() is the single entry point. It translates a
callback_data string into a call to the *same* handlers.*_status()
function the equivalent text command already uses -- e.g. "lang_uz"
resolves to what "/language UZ" resolves to, "risk_3" to "/risk 3".
No new business logic exists in this file, only that translation,
matching the "one backend, two entry points" principle already used
for text-command vs future-Menu-Button dispatch (both funnel into
command_router.route_command()).

Scope (V1 Language Callback Fix; UX polished in V1.1 Language UX
Polish; risk_*/strategy_*/timeframe_*/notifications_* wired in V2
Phase 6.2 Settings Callback Completion): lang_* is handled by
_handle_language(); risk_*/strategy_*/timeframe_*/notifications_* are
handled by _handle_setting() (see _SETTING_CALLBACKS below). Every
other keyboard's callback_data (settings_*, admin_*) is recognized
here as a category ready for a future phase, but not yet handled --
callback.answer() is still called for them (so the Telegram client's
loading spinner clears), matching every not-yet-implemented command
elsewhere in this codebase staying honestly inert rather than
fabricating behavior.
"""

from aiogram.types import CallbackQuery

from telegram import handlers
from telegram.keyboards import (
    language_keyboard,
    risk_keyboard,
    strategy_keyboard,
    timeframe_keyboard,
    notifications_keyboard,
    phone_share_keyboard,
)
from telegram.registration_service import RegistrationService
from translation.ui_catalog import t
from core_layer.logger.logger import setup_logger

logger = setup_logger("CallbackRouter")

_LANGUAGE_CALLBACKS = {
    "lang_uz": "UZ",
    "lang_ru": "RU",
    "lang_en": "EN",
}

# V2 Phase 6.2 (Settings Callback Completion) -- one entry per inline
# value-picker prefix, reusing the exact same handlers.*_status()
# function and telegram.keyboards.*_keyboard() builder the text
# command (/risk, /strategy, /timeframe, /notifications) and
# command_router._KEYBOARD_BY_COMMAND already use. "status_fn"/
# "current_value" are attribute *names* (looked up on handlers at call
# time in _handle_setting below), not direct function references --
# the same live-lookup shape _handle_language already uses when it
# calls handlers.language_status(...), so tests can monkeypatch
# handlers.risk_status etc. the same way they monkeypatch
# handlers.language_status. "parse" turns the callback_data suffix
# (the part after "risk_"/"strategy_"/etc.) into the same args string
# the text command would have received -- strategy is the only one
# that needs translating, since its keyboard callback_data uses
# underscore slugs ("liquidity_sweep") while handlers._STRATEGY_OPTIONS
# keys use spaces ("liquidity sweep").
_SETTING_CALLBACKS = {
    "risk": {
        "status_fn": "risk_status",
        "keyboard_builder": risk_keyboard,
        "current_value": "_current_risk",
        "parse": lambda suffix: suffix,
    },
    "strategy": {
        "status_fn": "strategy_status",
        "keyboard_builder": strategy_keyboard,
        "current_value": "_current_strategy_slug",
        "parse": lambda suffix: suffix.replace("_", " "),
    },
    "timeframe": {
        "status_fn": "timeframe_status",
        "keyboard_builder": timeframe_keyboard,
        "current_value": "_current_timeframe",
        "parse": lambda suffix: suffix,
    },
    "notifications": {
        "status_fn": "notifications_status",
        "keyboard_builder": notifications_keyboard,
        "current_value": "_current_notifications_choice",
        "parse": lambda suffix: suffix,
    },
}

# Recognized-but-not-yet-implemented callback_data prefixes (future
# phases add a branch here, same shape as _handle_language/
# _handle_setting below -- never a second dispatch mechanism). "nav_"
# (Phase 6.1's inline Back/Home row) was retired by V2 Phase 6.3
# (Director Approved: Dynamic Reply Keyboard Navigation) -- navigation
# is Reply-Keyboard-only now, so no nav_* callback_data is ever
# produced anymore; any stray one from a stale client-cached inline
# keyboard still falls through to the harmless "recognized but not
# implemented" answer() below.
_RECOGNIZED_PREFIXES = (
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

        for prefix, entry in _SETTING_CALLBACKS.items():
            if data.startswith(prefix + "_"):
                await _handle_setting(callback, entry, data[len(prefix) + 1:])
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

    # V2 Phase 3: a language choice mid-Wizard (registration_step ==
    # LANGUAGE) advances to the now-mandatory Phone Share step. A
    # no-op (advance_past_language() returns False) for an
    # already-registered user changing language later via /language --
    # this block never fires for them. ReplyKeyboardMarkup (Phone
    # Share) cannot be attached via edit_text() the way the inline
    # language_keyboard above was, so this is deliberately a separate
    # new message, best-effort like every other side effect here.
    try:
        if RegistrationService().advance_past_language(telegram_id):
            await callback.message.answer(
                t("registration.phone_prompt", language), reply_markup=phone_share_keyboard(language)
            )
    except Exception as e:
        logger.warning(f"route_callback: registration advance failed for telegram_id={telegram_id}: {e}")


async def _handle_setting(callback: CallbackQuery, entry: dict, raw_suffix: str) -> None:
    """
    risk_*/strategy_*/timeframe_*/notifications_* -> the matching
    handlers.*_status() (V2 Phase 6.2: Settings Callback Completion),
    then edit the picker message in place to show the result.

    Unlike _handle_language above, the picker keyboard is always
    reattached here (Director's Stage 6 Inline UX requirement) rather
    than removed on success -- Risk/Strategy/Timeframe/Notifications
    are settings the caller may want to keep adjusting, not a one-shot
    wizard step. It is redrawn with `selected` read fresh from the
    caller's *_current_* accessor, not from the tapped button, so it
    reflects the true DB state even if the update itself failed. A
    "✅ Saved" line is appended only when entry["status_fn"] reports
    show_keyboard=False, which every *_status() function above uses to
    mean "the update actually took effect" (the same signal
    _handle_language relies on to decide whether to drop its own
    keyboard).
    """
    telegram_id = callback.from_user.id
    language = handlers._current_language(telegram_id)
    args = entry["parse"](raw_suffix)
    status_fn = getattr(handlers, entry["status_fn"])
    result = await status_fn(telegram_id, args=args)
    await callback.answer()

    text = result.text
    if not result.show_keyboard:
        text = f"{text}\n\n{t('settings.saved', language)}"

    current_value = getattr(handlers, entry["current_value"])
    selected = current_value(telegram_id)
    reply_markup = entry["keyboard_builder"](language, selected=selected)
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except Exception as e:
        logger.warning(f"route_callback: edit_text failed, sending new message instead: {e}")
        await callback.message.answer(text, reply_markup=reply_markup)
