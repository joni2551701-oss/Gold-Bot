"""Phase 61.2 TASK 6/7/8/9 — AI Runtime Service Layer. No real network call anywhere -- every provider is faked or the real (keyless) GeminiProvider, which never reaches the network without a key."""

from ai.access.permissions import AIRole
from ai.capabilities.capability import Capability
from ai.capabilities.capability_manager import CapabilityManager
from ai.context.context_builder import build_ai_context
from ai.interfaces import MarketContext
from ai.providers.base_provider import ProviderResult
from ai.providers.provider_health import ProviderHealthTracker
from ai.providers.provider_manager import ProviderStatus
from ai.providers.runtime_errors import ProviderTimeoutError
from ai.runtime.ai_service import AIService
from ai.runtime.runtime_request import RuntimeRequest


class _FakeProvider:
    """Impersonates a registered provider name (e.g. "gemini") so ai/providers/provider_capabilities.py's matrix and ai/router/routing_rules.py's candidate lists both recognize it -- the router doesn't care what class backs a name."""

    def __init__(self, name: str, behavior=None):
        self._name = name
        self._behavior = behavior or (lambda prompt: ProviderResult(content=f"[{name}] answer", metadata={"provider": name}))

    @property
    def name(self) -> str:
        return self._name

    def chat(self, prompt):
        return self._behavior(prompt)

    def analyze(self, prompt):
        return self._behavior(prompt)

    def explain(self, prompt):
        return self._behavior(prompt)

    def vision(self, prompt, image_ref=None):
        return self._behavior(prompt)

    def image(self, prompt):
        return self._behavior(prompt)

    def voice(self, prompt):
        return self._behavior(prompt)


class _FakeProviderManager:
    """Duck-typed ProviderManager double -- only implements what AIRouter/AIService actually call (list_providers/get_provider/status_of), so a test never needs the real registry's five hardcoded providers."""

    def __init__(self, providers: dict, statuses: dict = None):
        self._providers = providers
        self._statuses = statuses or {name: ProviderStatus.FALLBACK for name in providers}

    def list_providers(self):
        return list(self._providers.keys())

    def get_provider(self, name):
        return self._providers.get(name)

    def status_of(self, name):
        return self._statuses.get(name)


def _context():
    return build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))


def test_access_denied_for_role_without_capability_entitlement():
    service = AIService()
    request = RuntimeRequest(capability=Capability.VISION, ai_context=_context(), role=AIRole.FREE)
    response = service.ask(request)
    assert response.accepted is False
    assert "access denied" in response.reason


def test_capability_disabled_is_rejected():
    capability_manager = CapabilityManager()
    capability_manager.disable(Capability.CHAT)
    service = AIService(capability_manager=capability_manager)
    request = RuntimeRequest(capability=Capability.CHAT, ai_context=_context(), role=AIRole.OWNER, prompt="hi")
    response = service.ask(request)
    assert response.accepted is False
    assert "disabled" in response.reason


def test_capability_with_no_runtime_method_mapping_is_rejected():
    service = AIService()
    request = RuntimeRequest(capability=Capability.SUMMARY, ai_context=_context(), role=AIRole.OWNER, prompt="summarize")
    response = service.ask(request)
    assert response.accepted is False
    assert "no runtime method mapping" in response.reason


def test_no_prompt_and_no_market_context_is_rejected():
    empty_context = build_ai_context()
    service = AIService()
    request = RuntimeRequest(capability=Capability.CHAT, ai_context=empty_context, role=AIRole.OWNER)
    response = service.ask(request)
    assert response.accepted is False
    assert "no prompt available" in response.reason


def test_successful_call_returns_provider_content():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager)
    request = RuntimeRequest(capability=Capability.ANALYSIS, ai_context=_context(), role=AIRole.OWNER)
    response = service.ask(request)
    assert response.accepted is True
    assert response.provider_name == "gemini"
    assert "gemini" in response.content


def test_second_identical_call_is_served_from_cache():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager)
    request = RuntimeRequest(capability=Capability.ANALYSIS, ai_context=_context(), role=AIRole.OWNER)

    first = service.ask(request)
    second = service.ask(request)

    assert first.from_cache is False
    assert second.from_cache is True
    assert second.content == first.content


def test_unsafe_content_is_rejected_by_the_validator():
    unsafe_provider = _FakeProvider("gemini", behavior=lambda prompt: ProviderResult(content="You should BUY NOW."))
    provider_manager = _FakeProviderManager({"gemini": unsafe_provider})
    service = AIService(provider_manager=provider_manager)
    request = RuntimeRequest(capability=Capability.ANALYSIS, ai_context=_context(), role=AIRole.OWNER)

    response = service.ask(request)

    assert response.accepted is False
    assert "validation" in response.reason
    assert any("trade-directive" in e for e in response.errors)


def test_provider_runtime_error_falls_back_to_next_candidate():
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai"),
    })
    service = AIService(provider_manager=provider_manager)
    request = RuntimeRequest(capability=Capability.CHAT, ai_context=_context(), role=AIRole.OWNER, prompt="hi")

    response = service.ask(request)

    assert response.accepted is True
    assert response.provider_name == "openai"


def test_provider_failure_is_recorded_in_health_tracker():
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    health_tracker = ProviderHealthTracker()
    provider_manager = _FakeProviderManager({
        "gemini": _FakeProvider("gemini", behavior=_fail),
        "openai": _FakeProvider("openai"),
    })
    service = AIService(provider_manager=provider_manager, health_tracker=health_tracker)
    request = RuntimeRequest(capability=Capability.CHAT, ai_context=_context(), role=AIRole.OWNER, prompt="hi")

    service.ask(request)

    assert health_tracker.is_available("gemini") is False


def test_every_candidate_failing_is_a_clean_rejection_not_a_crash():
    def _fail(prompt):
        raise ProviderTimeoutError("gemini", "timed out")

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini", behavior=_fail)})
    service = AIService(provider_manager=provider_manager)
    request = RuntimeRequest(capability=Capability.CHAT, ai_context=_context(), role=AIRole.OWNER, prompt="hi")

    response = service.ask(request)

    assert response.accepted is False
    assert response.content is None


def test_not_implemented_method_falls_back_to_next_provider():
    class _NoVisionProvider(_FakeProvider):
        def vision(self, prompt, image_ref=None):
            raise NotImplementedError("no real vision yet")

    provider_manager = _FakeProviderManager({
        "gemini": _NoVisionProvider("gemini"),
        "openai": _FakeProvider("openai"),
    })
    capability_manager = CapabilityManager()
    capability_manager.enable(Capability.VISION)
    service = AIService(provider_manager=provider_manager, capability_manager=capability_manager)
    request = RuntimeRequest(capability=Capability.VISION, ai_context=_context(), role=AIRole.OWNER, prompt="what's in this image?")

    response = service.ask(request)

    assert response.accepted is True
    assert response.provider_name == "openai"


def test_real_provider_manager_default_never_crashes_without_any_api_key():
    """Integration-shaped: the real ProviderManager (real GeminiProvider, no key in this sandbox) must fail over cleanly to a placeholder, never raise."""
    service = AIService()
    request = RuntimeRequest(capability=Capability.EXPLANATION, ai_context=_context(), role=AIRole.OWNER)
    response = service.ask(request)
    assert response.accepted is True
    assert response.provider_name != "gemini"
