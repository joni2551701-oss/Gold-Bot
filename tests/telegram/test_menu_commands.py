"""V2 Phase 4 (Persistent Menu, Stage 1) -- telegram/menu_commands.py."""

import asyncio

from aiogram.types import BotCommandScopeChat, BotCommandScopeDefault

from telegram.menu_commands import (
    _admin_menu,
    _owner_menu,
    _user_menu,
    register_all_menus,
)
from database.admin_repository import AdminRepository
from database.user_repository import UserRepository


def _run(coro):
    return asyncio.run(coro)


class FakeBot:
    def __init__(self, fail=False):
        self.fail = fail
        self.calls = []

    async def set_my_commands(self, commands, scope=None, language_code=None):
        if self.fail:
            raise RuntimeError("Telegram API unreachable")
        self.calls.append({"commands": commands, "scope": scope, "language_code": language_code})


# ---------------------------------------------------------------------------
# Menu content
# ---------------------------------------------------------------------------


def test_user_menu_has_six_entries_in_director_order():
    commands = [c.command for c in _user_menu("EN")]
    assert commands == ["start", "profile", "signal", "subscription", "settings", "help"]


def test_user_menu_is_localized_per_language():
    en_home = _user_menu("EN")[0].description
    uz_home = _user_menu("UZ")[0].description
    ru_home = _user_menu("RU")[0].description

    assert en_home == "🏠 Home"
    assert uz_home == "🏠 Bosh sahifa"
    assert ru_home == "🏠 Главная"


def test_admin_menu_is_user_menu_plus_admin_entry():
    admin_commands = [c.command for c in _admin_menu("EN")]
    assert admin_commands == ["start", "profile", "signal", "subscription", "settings", "help", "admin"]
    assert _admin_menu("EN")[-1].description == "🛠 Admin"


def test_owner_menu_is_admin_menu_plus_owner_entry():
    owner_commands = [c.command for c in _owner_menu("EN")]
    assert owner_commands == [
        "start", "profile", "signal", "subscription", "settings", "help", "admin", "owner",
    ]
    assert _owner_menu("EN")[-1].description == "👑 Owner"


def test_admin_owner_extra_labels_are_language_invariant():
    assert _admin_menu("UZ")[-1].description == _admin_menu("RU")[-1].description == "🛠 Admin"
    assert _owner_menu("UZ")[-1].description == _owner_menu("RU")[-1].description == "👑 Owner"


# ---------------------------------------------------------------------------
# register_all_menus() -- default (USER) scope
# ---------------------------------------------------------------------------


def test_register_all_menus_sets_the_default_scope_once_plus_one_per_language(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    bot = FakeBot()

    _run(register_all_menus(bot))

    default_calls = [c for c in bot.calls if isinstance(c["scope"], BotCommandScopeDefault)]
    assert len(default_calls) == 4  # 1 catch-all + uz/ru/en


def test_register_all_menus_default_scope_uses_user_menu(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    bot = FakeBot()

    _run(register_all_menus(bot))

    default_calls = [c for c in bot.calls if isinstance(c["scope"], BotCommandScopeDefault)]
    for call in default_calls:
        assert [c.command for c in call["commands"]] == [
            "start", "profile", "signal", "subscription", "settings", "help",
        ]


def test_register_all_menus_never_raises_when_set_my_commands_fails(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    bot = FakeBot(fail=True)

    _run(register_all_menus(bot))  # must not raise


# ---------------------------------------------------------------------------
# register_all_menus() -- privileged (ADMIN/OWNER) scope
# ---------------------------------------------------------------------------


def test_register_all_menus_registers_owner_chat_scope(monkeypatch):
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "9001")
    UserRepository().create_user("9001", username="owner_user", language="EN")
    bot = FakeBot()

    _run(register_all_menus(bot))

    owner_calls = [
        c for c in bot.calls
        if isinstance(c["scope"], BotCommandScopeChat) and c["scope"].chat_id == 9001
    ]
    assert len(owner_calls) == 1
    assert [c.command for c in owner_calls[0]["commands"]][-1] == "owner"


def test_register_all_menus_registers_admin_chat_scope(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    UserRepository().create_user("9002", username="admin_user", language="RU")
    AdminRepository().add_admin("9002")
    bot = FakeBot()

    _run(register_all_menus(bot))

    admin_calls = [
        c for c in bot.calls
        if isinstance(c["scope"], BotCommandScopeChat) and c["scope"].chat_id == 9002
    ]
    assert len(admin_calls) == 1
    commands = [c.command for c in admin_calls[0]["commands"]]
    assert commands[-1] == "admin"
    assert "owner" not in commands
    assert admin_calls[0]["commands"][0].description == "🏠 Главная"  # RU label


def test_register_all_menus_gives_owner_the_owner_menu_not_the_admin_menu(monkeypatch):
    """A telegram_id that is both a registered admin AND the configured owner gets exactly one, richer menu."""
    monkeypatch.setenv("TELEGRAM_OWNER_ID", "9003")
    UserRepository().create_user("9003", username="both", language="EN")
    AdminRepository().add_admin("9003")
    bot = FakeBot()

    _run(register_all_menus(bot))

    scoped_calls = [
        c for c in bot.calls
        if isinstance(c["scope"], BotCommandScopeChat) and c["scope"].chat_id == 9003
    ]
    assert len(scoped_calls) == 1
    assert [c.command for c in scoped_calls[0]["commands"]][-1] == "owner"


def test_register_all_menus_unset_owner_registers_no_owner_scope(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    bot = FakeBot()

    _run(register_all_menus(bot))

    assert not [c for c in bot.calls if isinstance(c["scope"], BotCommandScopeChat)]


def test_register_all_menus_skips_a_non_numeric_admin_id_without_raising(monkeypatch):
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    AdminRepository().add_admin("not-a-number")
    bot = FakeBot()

    _run(register_all_menus(bot))  # must not raise

    assert not [c for c in bot.calls if isinstance(c["scope"], BotCommandScopeChat)]


def test_register_all_menus_admin_language_defaults_to_uz_for_unknown_user(monkeypatch):
    """An admin telegram_id with no matching users row still gets a menu (schema default language)."""
    monkeypatch.delenv("TELEGRAM_OWNER_ID", raising=False)
    AdminRepository().add_admin("9004")
    bot = FakeBot()

    _run(register_all_menus(bot))

    admin_calls = [
        c for c in bot.calls
        if isinstance(c["scope"], BotCommandScopeChat) and c["scope"].chat_id == 9004
    ]
    assert len(admin_calls) == 1
    assert admin_calls[0]["commands"][0].description == "🏠 Bosh sahifa"  # UZ default
