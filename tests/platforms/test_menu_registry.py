"""PLATFORM-001 -- Universal Menu Registry foundation tests (platforms/). TASK-002C adds target_bindings/DEFAULT_MENUS/build_default_menu_registry() tests."""

import pytest

from platform_layer.platform_service.menu_registry import (
    MenuDefinition,
    MenuRegistry,
    DuplicateMenuIdError,
    DEFAULT_MENUS,
    build_default_menu_registry,
)
from platform_layer.platform_service.navigation_model import is_valid_screen_id
from platform_layer.platform_service.platform_model import PlatformName


def _definition(menu_id="settings", platforms=None):
    return MenuDefinition(id=menu_id, permission="USER", platforms=platforms or [PlatformName.TELEGRAM_BOT])


def test_register_get_list():
    registry = MenuRegistry()
    a = _definition(menu_id="settings")
    b = _definition(menu_id="profile")

    registry.register(a)
    registry.register(b)

    assert registry.get("settings") is a
    assert registry.get("profile") is b
    assert len(registry.list()) == 2


def test_get_returns_none_for_unregistered_id():
    registry = MenuRegistry()
    assert registry.get("does_not_exist") is None


def test_duplicate_id_raises():
    registry = MenuRegistry()
    registry.register(_definition(menu_id="settings"))

    with pytest.raises(DuplicateMenuIdError):
        registry.register(_definition(menu_id="settings"))


def test_by_platform_filters_correctly():
    registry = MenuRegistry()
    registry.register(_definition(menu_id="settings", platforms=[PlatformName.TELEGRAM_BOT]))
    registry.register(_definition(menu_id="future_chart", platforms=[PlatformName.ANDROID, PlatformName.IOS]))

    telegram_menus = {d.id for d in registry.by_platform(PlatformName.TELEGRAM_BOT)}
    assert telegram_menus == {"settings"}
    android_menus = {d.id for d in registry.by_platform(PlatformName.ANDROID)}
    assert android_menus == {"future_chart"}
    assert registry.by_platform(PlatformName.DESKTOP) == []


def test_menu_definition_defaults():
    definition = MenuDefinition(id="bare", permission="USER")
    assert definition.platforms == []
    assert definition.version == "0.1"
    assert definition.dependencies == []
    assert definition.target_bindings == {}


def test_menu_definition_target_bindings():
    definition = MenuDefinition(
        id="settings.language",
        permission="USER",
        platforms=[PlatformName.TELEGRAM_BOT],
        target_bindings={PlatformName.TELEGRAM_BOT: "/language"},
    )
    assert definition.target_bindings[PlatformName.TELEGRAM_BOT] == "/language"


def test_default_menus_all_ids_follow_adr002_universal_screen_identity():
    """Every DEFAULT_MENUS entry must use the dotted Universal Screen ID convention (ADR-002)."""
    for definition in DEFAULT_MENUS:
        assert is_valid_screen_id(definition.id), f"{definition.id} is not a valid Universal Screen ID"


def test_default_menus_no_duplicate_ids():
    ids = [d.id for d in DEFAULT_MENUS]
    assert len(ids) == len(set(ids))


def test_default_menus_every_entry_has_a_telegram_target_binding():
    """DEFAULT_MENUS mirrors GoldBot's real, live Telegram screens only -- every entry must bind to a real "/command" string."""
    for definition in DEFAULT_MENUS:
        assert PlatformName.TELEGRAM_BOT in definition.target_bindings
        binding = definition.target_bindings[PlatformName.TELEGRAM_BOT]
        assert binding.startswith("/")


def test_default_menus_permissions_match_real_tiers():
    valid_tiers = {"USER", "ADMIN", "OWNER"}
    for definition in DEFAULT_MENUS:
        assert definition.permission in valid_tiers


def test_build_default_menu_registry_contains_every_default_menu():
    registry = build_default_menu_registry()
    assert len(registry.list()) == len(DEFAULT_MENUS)
    for definition in DEFAULT_MENUS:
        assert registry.get(definition.id) is definition


def test_build_default_menu_registry_returns_independent_instances():
    first = build_default_menu_registry()
    second = build_default_menu_registry()
    assert first is not second
    assert first.list() is not second.list()


def test_admin_management_reopens_admin_panel():
    """Matches platform_layer/telegram/reply_keyboard_manager.py's Director Review correction 1 -- Admin Management is not a direct action."""
    registry = build_default_menu_registry()
    admin_management = registry.get("admin.management")
    assert admin_management.target_bindings[PlatformName.TELEGRAM_BOT] == "/admin"
