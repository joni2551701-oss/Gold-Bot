"""Phase 61.0 TASK 2 — Capability Manager/Registry tests. No real AI call anywhere."""

from ai_layer.ai_engine.capabilities.capability import Capability
from ai_layer.ai_engine.capabilities.capability_manager import CapabilityManager, get_capability_manager
from ai_layer.ai_engine.capabilities.capability_registry import build_capability_registry


def test_registry_declares_every_capability_exactly_once():
    entries = build_capability_registry()
    names = [d.capability for d in entries]
    assert set(names) == set(Capability)
    assert len(names) == len(Capability)


def test_registry_default_enablement_matches_phase_61_0_defaults():
    entries = {d.capability: d.enabled for d in build_capability_registry()}
    assert entries[Capability.CHAT] is True
    assert entries[Capability.ANALYSIS] is True
    assert entries[Capability.VISION] is False
    assert entries[Capability.TOOL_CALLING] is False


def test_manager_seeds_from_registry_defaults():
    manager = CapabilityManager()
    assert manager.is_enabled(Capability.CHAT) is True
    assert manager.is_enabled(Capability.VISION) is False


def test_manager_enable_and_disable_are_independent_per_capability():
    manager = CapabilityManager()
    manager.enable(Capability.VISION)
    manager.disable(Capability.CHAT)
    assert manager.is_enabled(Capability.VISION) is True
    assert manager.is_enabled(Capability.CHAT) is False
    assert manager.is_enabled(Capability.ANALYSIS) is True  # untouched


def test_manager_status_returns_full_descriptor_list():
    manager = CapabilityManager()
    status = manager.status()
    assert len(status) == len(Capability)


def test_manager_enabled_capabilities_lists_only_enabled():
    manager = CapabilityManager()
    manager.disable(Capability.CHAT)
    enabled = manager.enabled_capabilities()
    assert Capability.CHAT not in enabled
    assert Capability.ANALYSIS in enabled


def test_get_capability_manager_returns_a_shared_singleton():
    first = get_capability_manager()
    second = get_capability_manager()
    assert first is second
