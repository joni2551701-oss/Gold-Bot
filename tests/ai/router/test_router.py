"""Phase 61.0 TASK 4 — AI Router: Capability -> Provider -> Return. No real API call anywhere."""

from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.providers.provider_manager import ProviderManager, ProviderStatus
from ai.router.router import AIRouter
from ai.router.routing_rules import ROUTING_RULES, get_candidate_providers


def test_every_capability_has_a_routing_rule():
    assert set(ROUTING_RULES.keys()) == set(Capability)


def test_get_candidate_providers_returns_declared_order():
    assert get_candidate_providers(Capability.IMAGE) == ("openai",)


def test_get_candidate_providers_returns_empty_tuple_for_undeclared_capability():
    class _FakeCapability:
        pass

    assert get_candidate_providers(_FakeCapability()) == ()


def test_router_routes_explanation_to_first_available_candidate():
    router = AIRouter(ProviderManager())
    result = router.route(Capability.EXPLANATION)
    assert result.provider_name == "gemini"


def test_router_routes_image_to_openai_per_worked_example():
    router = AIRouter(ProviderManager())
    result = router.route(Capability.IMAGE)
    assert result.provider_name == "openai"


def test_router_skips_disabled_providers_and_falls_back():
    provider_manager = ProviderManager()
    provider_manager.set_status("gemini", ProviderStatus.DISABLED)
    router = AIRouter(provider_manager)
    result = router.route(Capability.EXPLANATION)
    assert result.provider_name == "openai"


def test_router_returns_none_when_capability_manager_disables_it():
    capability_manager = CapabilityManager()
    capability_manager.disable(Capability.CHAT)
    router = AIRouter(ProviderManager(), capability_manager=capability_manager)
    result = router.route(Capability.CHAT)
    assert result.provider_name is None
    assert "disabled" in result.reason


def test_router_without_capability_manager_ignores_capability_state():
    router = AIRouter(ProviderManager())
    result = router.route(Capability.CHAT)
    assert result.provider_name is not None


def test_router_returns_none_when_every_candidate_disabled():
    provider_manager = ProviderManager()
    for name in provider_manager.list_providers():
        provider_manager.set_status(name, ProviderStatus.DISABLED)
    router = AIRouter(provider_manager)
    result = router.route(Capability.IMAGE)
    assert result.provider_name is None
