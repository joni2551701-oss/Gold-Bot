"""
Telegram Layer — Navigation Controller (V2 Phase 6.1, Director
Approved; see docs/PHASE6_NAVIGATION_AUDIT.md's "Director Decision —
Phase 6" section).

Two responsibilities, both explicitly scoped to Phase 6.1 (Navigation
Controller / Unified Message Lifecycle / Reply + Inline Navigation
Integration — Phase 6.2's Settings Callback Completion is out of scope
here):

1. Back/Home inline row (Director Decision 4) — every one of the six
   "editable" pages (Director Decision 3) carries a mandatory
   "⬅️ Orqaga" / "🏠 Bosh sahifa" inline row. Structurally, this is the
   one exception to Director Decision 8's "inline = in-page action,
   Reply Keyboard = between-page navigation" rule — the Reply Keyboard
   is fixed (Director Decision 7: always visible, same buttons
   everywhere), so it cannot carry a page-specific "go back to X"
   action; only an inline row on that specific page's own message can.
   In Phase 6.1, with no sub-screens deeper than one level yet, Back
   and Home are functionally identical (both resolve to /start) —
   Director Decision 4 combined with Decision 6 (fully stateless, no
   history stack) means Back always resolves to a page's one fixed,
   hardcoded parent rather than a dynamic "previous screen"; for these
   six flat pages, that fixed parent is Home. Phase 6.2's Settings
   sub-screens will be the first place Back and Home actually differ.

2. Message Lifecycle Tracker (Director Decision 3/6) — a process-local
   (never database-persisted, per Decision 6) `telegram_id -> last bot
   message_id` pointer, consulted by telegram/polling.py to decide
   whether a reply to one of the six editable commands should edit
   that message in place instead of sending a new one. This is not a
   history/screen stack — it holds exactly one id per chat, overwritten
   on every send, and fails safe to "send a new message" if the id is
   missing or stale (e.g. after a process restart).
"""

from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from translation.ui_catalog import t

# Director Decision 3 -- these six top-level pages edit their existing
# message in place instead of creating a new one on every navigation tap.
EDITABLE_COMMANDS = frozenset({"profile", "subscription", "settings", "help", "about", "history"})


def back_home_row(language=None):
    """The mandatory ⬅️ Orqaga / 🏠 Bosh sahifa inline row (Director Decision 4)."""
    return [
        InlineKeyboardButton(text=t("nav.back", language), callback_data="nav_back"),
        InlineKeyboardButton(text=t("nav.home", language), callback_data="nav_home"),
    ]


def with_back_home(keyboard: Optional[InlineKeyboardMarkup], language=None) -> InlineKeyboardMarkup:
    """
    Appends the Back/Home row to an existing InlineKeyboardMarkup (e.g.
    settings_keyboard()'s five category buttons), or builds a keyboard
    containing just that row if the page had none (Profile/Subscription/
    Help/About/History). Never touches callback_data any existing row
    already carries.
    """
    rows = list(keyboard.inline_keyboard) if keyboard is not None else []
    rows.append(back_home_row(language))
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ---------------------------------------------------------------------------
# Message Lifecycle Tracker -- process-local only (Director Decision 6:
# "Database'da navigation state saqlanmaydi" -- never written to the
# database, and not a history/screen stack: exactly one message id per
# chat, overwritten on every send).
# ---------------------------------------------------------------------------

_LAST_MESSAGE_ID: dict = {}


def record_message(telegram_id, message_id) -> None:
    _LAST_MESSAGE_ID[str(telegram_id)] = message_id


def last_message_id(telegram_id):
    return _LAST_MESSAGE_ID.get(str(telegram_id))
