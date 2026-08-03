"""Phase 61.3 TASK 8 — Runtime Trace: RuntimeResponse.request_id + trace_request() join over RequestLog/ResponseLog."""

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_service.audit.request_log import RequestLog
from ai_layer.ai_service.audit.response_log import ResponseLog
from ai_layer.ai_service.audit.trace import trace_request
from ai_layer.ai_engine.capabilities.capability import Capability
from ai_layer.ai_engine.context.context_builder import build_ai_context
from ai_layer.ai_service.interfaces import MarketContext
from ai_layer.ai_engine.providers.base_provider import ProviderResult
from ai_layer.ai_engine.providers.provider_manager import ProviderStatus
from ai_layer.ai_engine.runtime.ai_service import AIService
from ai_layer.ai_engine.runtime.runtime_request import RuntimeRequest


class _FakeProvider:
    def __init__(self, name: str, behavior=None):
        self._name = name
        self._behavior = behavior or (lambda prompt: ProviderResult(content=f"[{name}] ok"))

    @property
    def name(self) -> str:
        return self._name

    def analyze(self, prompt):
        return self._behavior(prompt)

    def chat(self, prompt):
        return self._behavior(prompt)


class _FakeProviderManager:
    def __init__(self, providers: dict):
        self._providers = providers
        self._statuses = {name: ProviderStatus.FALLBACK for name in providers}

    def list_providers(self):
        return list(self._providers.keys())

    def get_provider(self, name):
        return self._providers.get(name)

    def status_of(self, name):
        return self._statuses.get(name)


def _context():
    return build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))


def test_successful_response_carries_a_request_id():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager)
    response = service.ask(RuntimeRequest(capability=Capability.ANALYSIS, ai_context=_context(), role=AIRole.OWNER))

    assert response.accepted is True
    assert response.request_id is not None


def test_access_denied_response_has_no_request_id():
    service = AIService()
    response = service.ask(RuntimeRequest(capability=Capability.VISION, ai_context=_context(), role=AIRole.FREE))
    assert response.accepted is False
    assert response.request_id is None


def test_cache_hit_response_has_no_request_id_since_no_provider_was_called():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager)
    request = RuntimeRequest(capability=Capability.ANALYSIS, ai_context=_context(), role=AIRole.OWNER)

    first = service.ask(request)
    second = service.ask(request)

    assert first.request_id is not None
    assert second.from_cache is True
    assert second.request_id is None


def test_trace_request_finds_the_matching_request_and_response_entries():
    request_log = RequestLog()
    response_log = ResponseLog()
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    service = AIService(provider_manager=provider_manager, request_log=request_log, response_log=response_log)

    response = service.ask(RuntimeRequest(capability=Capability.ANALYSIS, ai_context=_context(), role=AIRole.OWNER))

    trace = trace_request(request_log, response_log, response.request_id)

    assert trace.request_id == response.request_id
    assert trace.request is not None
    assert trace.request.capability == Capability.ANALYSIS
    assert len(trace.responses) == 1
    assert trace.responses[0].status == "SUCCESS"


def test_trace_request_with_unknown_id_returns_empty_not_an_error():
    trace = trace_request(RequestLog(), ResponseLog(), "does-not-exist")
    assert trace.request is None
    assert trace.responses == []
