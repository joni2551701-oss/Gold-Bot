"""PLATFORM-001 -- Universal Menu Registry foundation tests (platforms/)."""

import pytest

from platforms.menu_registry import MenuDefinition, MenuRegistry, DuplicateMenuIdError
from platforms.platform_model import PlatformName


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
