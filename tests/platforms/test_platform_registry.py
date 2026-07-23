"""
PLATFORM-001 -- Platform Registry foundation tests (platforms/).

No mocking -- real PlatformDefinition/PlatformRegistry objects, same
convention as tests/assets/test_asset_intelligence.py.

Platform Registry stores metadata only: it does not run, install, or
ship any client.
"""

import dataclasses

import pytest

from platforms.platform_model import PlatformDefinition, PlatformName, PlatformStatus
from platforms.platform_registry import (
    PlatformRegistry,
    DuplicatePlatformError,
    DEFAULT_PLATFORMS,
    build_default_registry,
)


def _definition(name=PlatformName.ANDROID, status=PlatformStatus.NOT_STARTED):
    return PlatformDefinition(name=name, status=status, version="0.0")


def test_platform_definition_is_immutable():
    definition = _definition()
    with pytest.raises(dataclasses.FrozenInstanceError):
        definition.version = "1.0"


def test_registry_register_get_list():
    registry = PlatformRegistry()
    a = _definition(name=PlatformName.ANDROID)
    b = _definition(name=PlatformName.IOS)

    registry.register(a)
    registry.register(b)

    assert registry.get(PlatformName.ANDROID) is a
    assert registry.get(PlatformName.IOS) is b
    listed = registry.list()
    assert len(listed) == 2
    assert a in listed
    assert b in listed


def test_get_returns_none_for_unregistered_platform():
    registry = PlatformRegistry()
    assert registry.get(PlatformName.DESKTOP) is None


def test_duplicate_platform_raises():
    registry = PlatformRegistry()
    registry.register(_definition(name=PlatformName.ANDROID))

    with pytest.raises(DuplicatePlatformError):
        registry.register(_definition(name=PlatformName.ANDROID))


def test_by_status_filters_correctly():
    registry = PlatformRegistry()
    registry.register(_definition(name=PlatformName.TELEGRAM_BOT, status=PlatformStatus.LIVE))
    registry.register(_definition(name=PlatformName.ANDROID, status=PlatformStatus.NOT_STARTED))
    registry.register(_definition(name=PlatformName.IOS, status=PlatformStatus.NOT_STARTED))

    not_started = {d.name for d in registry.by_status(PlatformStatus.NOT_STARTED)}
    assert not_started == {PlatformName.ANDROID, PlatformName.IOS}
    assert [d.name for d in registry.by_status(PlatformStatus.LIVE)] == [PlatformName.TELEGRAM_BOT]
    assert registry.by_status(PlatformStatus.PLANNED) == []


def test_default_registry_reflects_honest_current_state():
    """
    Only Telegram Bot is LIVE today -- every other platform is
    NOT_STARTED, matching this codebase's real, current state (no
    fabricated "in progress" status for a platform with zero code).
    """
    registry = build_default_registry()

    assert len(DEFAULT_PLATFORMS) == 5
    live = registry.by_status(PlatformStatus.LIVE)
    assert [d.name for d in live] == [PlatformName.TELEGRAM_BOT]

    not_started = {d.name for d in registry.by_status(PlatformStatus.NOT_STARTED)}
    assert not_started == {
        PlatformName.TELEGRAM_MINI_APP,
        PlatformName.ANDROID,
        PlatformName.IOS,
        PlatformName.DESKTOP,
    }


def test_build_default_registry_returns_independent_instances():
    """
    Each call returns its own registry object, not a shared singleton.
    Unlike AssetRegistry's default (only Gold registered, room to add
    an extra symbol), PlatformRegistry's default already covers every
    PlatformName value -- so independence is checked via object
    identity rather than an extra register() call.
    """
    first = build_default_registry()
    second = build_default_registry()

    assert first is not second
    assert first.list() is not second.list()


def test_platform_definition_field_shape_is_stable():
    field_names = {f.name for f in dataclasses.fields(PlatformDefinition)}
    assert field_names == {"name", "status", "version", "features", "compatibility"}

    minimal = PlatformDefinition(name=PlatformName.DESKTOP, status=PlatformStatus.NOT_STARTED, version="0.0")
    assert minimal.features == []
    assert minimal.compatibility is None
