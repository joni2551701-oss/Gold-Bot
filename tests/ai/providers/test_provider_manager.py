"""Phase 61.0 TASK 3 — Provider Manager Preferred -> Fallback -> Disabled selection."""

from ai.providers.provider_manager import ProviderManager, ProviderStatus
from ai.providers.provider_registry import build_provider_registry


def test_registry_lists_the_five_named_placeholder_providers():
    names = {d.name for d in build_provider_registry()}
    assert names == {"openai", "gemini", "claude", "grok", "local_llm"}


def test_manager_defaults_every_provider_to_fallback():
    manager = ProviderManager()
    for name in manager.list_providers():
        assert manager.status_of(name) == ProviderStatus.FALLBACK


def test_select_provider_without_a_preferred_returns_first_fallback_in_registry_order():
    manager = ProviderManager()
    selected = manager.select_provider()
    assert selected is not None
    assert selected.name == manager.list_providers()[0]


def test_select_provider_prefers_the_explicitly_preferred_provider():
    manager = ProviderManager()
    manager.set_status("claude", ProviderStatus.PREFERRED)
    selected = manager.select_provider()
    assert selected.name == "claude"


def test_select_provider_skips_disabled_providers():
    manager = ProviderManager()
    for name in manager.list_providers():
        manager.set_status(name, ProviderStatus.DISABLED)
    manager.set_status("grok", ProviderStatus.FALLBACK)
    selected = manager.select_provider()
    assert selected.name == "grok"


def test_select_provider_returns_none_when_everything_disabled():
    manager = ProviderManager()
    for name in manager.list_providers():
        manager.set_status(name, ProviderStatus.DISABLED)
    assert manager.select_provider() is None


def test_set_status_on_unregistered_provider_is_ignored():
    manager = ProviderManager()
    manager.set_status("unknown_provider", ProviderStatus.PREFERRED)
    assert manager.status_of("unknown_provider") is None


def test_get_provider_returns_none_for_unregistered_name():
    manager = ProviderManager()
    assert manager.get_provider("unknown_provider") is None
