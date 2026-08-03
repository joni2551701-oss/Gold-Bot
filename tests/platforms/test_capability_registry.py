"""PLATFORM-001 -- Module Capability Registry foundation tests (platforms/)."""

import pytest

from platform_layer.platform_service.capability_model import PlatformCapability, SupportStatus
from platform_layer.platform_service.platform_model import PlatformName
from platform_layer.platform_service.capability_registry import (
    ModuleCapabilityRegistry,
    DuplicateModuleCapabilityError,
)


def _all_supported():
    return {p: PlatformCapability(platform=p, status=SupportStatus.SUPPORTED) for p in PlatformName}


def test_register_get_list():
    registry = ModuleCapabilityRegistry()
    registry.register("moduleA", _all_supported())

    assert registry.get("moduleA") is not None
    assert registry.get("moduleA")[PlatformName.ANDROID].status == SupportStatus.SUPPORTED
    assert registry.list() == ["moduleA"]


def test_get_returns_none_for_unregistered_module():
    registry = ModuleCapabilityRegistry()
    assert registry.get("does_not_exist") is None


def test_duplicate_module_name_raises():
    registry = ModuleCapabilityRegistry()
    registry.register("moduleA", _all_supported())

    with pytest.raises(DuplicateModuleCapabilityError):
        registry.register("moduleA", _all_supported())


def test_capability_not_supported_carries_reason():
    capability = PlatformCapability(
        platform=PlatformName.ANDROID,
        status=SupportStatus.NOT_SUPPORTED,
        reason="No Android client exists yet.",
        future_plan="Planned once the Android client foundation is built.",
    )
    assert capability.status == SupportStatus.NOT_SUPPORTED
    assert capability.reason == "No Android client exists yet."
    assert capability.future_plan is not None
