"""
Telegram Layer — inline keyboard foundation.

Each function is a placeholder for a future aiogram
InlineKeyboardMarkup builder. No keyboard objects are constructed
yet -- only the call sites future handlers will use.

language_keyboard() is the one exception (Phase 34, Part 9): a
foundation-level language hint attached to /start only. The buttons
carry callback_data but nothing consumes it yet -- no language
switching logic is wired to these buttons.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 Uzbek", callback_data="lang_uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        ]
    )


def trading_style_keyboard():
    pass


def risk_keyboard():
    pass


def settings_keyboard():
    pass


def admin_panel_keyboard():
    pass
