"""
Telegram Layer — inline keyboard foundation.

language_keyboard(), risk_keyboard(), timeframe_keyboard(),
strategy_keyboard(), and settings_keyboard() (Phase 40) are real: each
renders the options telegram/handlers.py documents in its command's
"no argument" prompt text. Their callback_data carries the value the
user would need to pass as a command argument (e.g. "risk_5" ->
"/risk 5"), but no aiogram callback_query handler consumes it yet --
these are display hints, same precedent as language_keyboard() since
Phase 34. Real settings changes happen via command arguments (e.g.
"/risk 5"), handled by telegram.handlers / telegram.user_service; see
telegram/handlers.py's module docstring for why. admin_panel_keyboard()
stays a placeholder -- no admin panel UI exists yet, only text (Phase
37's /admin).
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
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1%", callback_data="risk_1"),
                InlineKeyboardButton(text="2%", callback_data="risk_2"),
                InlineKeyboardButton(text="3%", callback_data="risk_3"),
                InlineKeyboardButton(text="5%", callback_data="risk_5"),
            ]
        ]
    )


def timeframe_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="M15", callback_data="timeframe_m15"),
                InlineKeyboardButton(text="H1", callback_data="timeframe_h1"),
                InlineKeyboardButton(text="H4", callback_data="timeframe_h4"),
            ]
        ]
    )


def strategy_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Liquidity Sweep", callback_data="strategy_liquidity_sweep")],
            [InlineKeyboardButton(text="FVG", callback_data="strategy_fvg")],
            [InlineKeyboardButton(text="AMD", callback_data="strategy_amd")],
            [InlineKeyboardButton(text="Order Block", callback_data="strategy_order_block")],
        ]
    )


def settings_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Language", callback_data="settings_language")],
            [InlineKeyboardButton(text="Risk", callback_data="settings_risk")],
            [InlineKeyboardButton(text="Strategy", callback_data="settings_strategy")],
            [InlineKeyboardButton(text="Timeframe", callback_data="settings_timeframe")],
            [InlineKeyboardButton(text="Notifications", callback_data="settings_notifications")],
        ]
    )


def admin_panel_keyboard():
    pass
