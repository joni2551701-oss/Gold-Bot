"""
Telegram Layer -- Navigation Controller tests (V2 Phase 6.1, Director
Approved). Covers the Back/Home inline row builder, the
with_back_home() composition helper, and the process-local Message
Lifecycle Tracker telegram/navigation.py owns.
"""

from telegram.navigation import (
    EDITABLE_COMMANDS,
    back_home_row,
    last_message_id,
    record_message,
    with_back_home,
)
from telegram.keyboards import settings_keyboard


def _labels(row):
    return [button.text for button in row]


def test_editable_commands_matches_director_decision_3():
    assert EDITABLE_COMMANDS == {"profile", "subscription", "settings", "help", "about", "history"}


def test_back_home_row_localized_labels():
    en = _labels(back_home_row("EN"))
    uz = _labels(back_home_row("UZ"))
    ru = _labels(back_home_row("RU"))

    assert en == ["⬅️ Back", "🏠 Home"]
    assert uz == ["⬅️ Orqaga", "🏠 Bosh sahifa"]
    assert ru == ["⬅️ Назад", "🏠 Главная"]


def test_back_home_row_callback_data_is_stable_across_languages():
    assert [b.callback_data for b in back_home_row("EN")] == ["nav_back", "nav_home"]
    assert [b.callback_data for b in back_home_row("RU")] == ["nav_back", "nav_home"]


def test_with_back_home_builds_a_keyboard_when_none_existed():
    markup = with_back_home(None, "UZ")
    assert len(markup.inline_keyboard) == 1
    assert _labels(markup.inline_keyboard[0]) == ["⬅️ Orqaga", "🏠 Bosh sahifa"]


def test_with_back_home_appends_to_an_existing_keyboard():
    base = settings_keyboard("UZ")
    markup = with_back_home(base, "UZ")

    assert len(markup.inline_keyboard) == len(base.inline_keyboard) + 1
    assert _labels(markup.inline_keyboard[-1]) == ["⬅️ Orqaga", "🏠 Bosh sahifa"]
    # existing rows/callback_data untouched
    assert markup.inline_keyboard[0][0].callback_data == base.inline_keyboard[0][0].callback_data


def test_message_lifecycle_tracker_round_trip():
    record_message("9001", 4242)
    assert last_message_id("9001") == 4242


def test_message_lifecycle_tracker_defaults_to_none_for_unknown_chat():
    assert last_message_id("no-such-chat-ever") is None
