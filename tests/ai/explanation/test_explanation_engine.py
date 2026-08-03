"""Phase 61.3 TASK 7 — Explanation Engine: thin wrapper over AIService (unmodified) for EXPLANATION/SUMMARY/EDUCATION/ANALYSIS."""

from ai_layer.ai_service.access.permissions import AIRole
from ai_layer.ai_engine.context.context_builder import build_ai_context
from ai_layer.explanation_ai.explanation_engine import ExplanationEngine
from ai_layer.ai_service.interfaces import MarketContext
from ai_layer.ai_engine.providers.base_provider import ProviderResult
from ai_layer.ai_engine.providers.provider_manager import ProviderStatus
from ai_layer.ai_engine.runtime.ai_service import AIService
from signal_layer.signal_scoring.explainability import SignalExplanation


class _FakeProvider:
    def __init__(self, name: str, behavior=None):
        self._name = name
        self._behavior = behavior or (lambda prompt: ProviderResult(content=f"[{name}] {prompt[:20]}"))

    @property
    def name(self) -> str:
        return self._name

    def explain(self, prompt):
        return self._behavior(prompt)

    def chat(self, prompt):
        return self._behavior(prompt)

    def analyze(self, prompt):
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


def _engine():
    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini")})
    return ExplanationEngine(ai_service=AIService(provider_manager=provider_manager))


def _context():
    return build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))


def _signal_explanation():
    return SignalExplanation(
        direction="BUY",
        reasons=("HTF bullish bias", "HH/HL structure", "London session"),
        quality="A+",
        confidence=85.0,
    )


def test_explain_signal_accepts_and_returns_content():
    engine = _engine()
    response = engine.explain_signal(_signal_explanation(), _context(), AIRole.OWNER)
    assert response.accepted is True
    assert response.content is not None


def test_explain_signal_prompt_carries_reasons_quality_confidence():
    captured = []

    def _capture(prompt):
        captured.append(prompt)
        return ProviderResult(content="ok")

    provider_manager = _FakeProviderManager({"gemini": _FakeProvider("gemini", behavior=_capture)})
    engine = ExplanationEngine(ai_service=AIService(provider_manager=provider_manager))

    engine.explain_signal(_signal_explanation(), _context(), AIRole.OWNER)

    prompt = captured[0]
    assert "HTF bullish bias" in prompt
    assert "A+" in prompt
    assert "85.0" in prompt
    assert "BUY" in prompt


def test_explain_signal_with_no_reasons_does_not_crash():
    engine = _engine()
    empty_explanation = SignalExplanation(direction="NONE", reasons=(), quality="C", confidence=0.0)
    response = engine.explain_signal(empty_explanation, _context(), AIRole.OWNER)
    assert response.accepted is True


def test_summarize_report_is_cleanly_rejected_no_provider_mapping_yet():
    engine = _engine()
    response = engine.summarize_report("Strategy X: 60% win rate", _context(), AIRole.OWNER)
    assert response.accepted is False
    assert "no runtime method mapping" in response.reason


def test_explain_topic_looks_up_a_known_knowledge_entry_then_is_cleanly_rejected():
    engine = _engine()
    response = engine.explain_topic("smc.bos", _context(), AIRole.OWNER)
    assert response.accepted is False
    assert "no runtime method mapping" in response.reason


def test_explain_topic_with_unknown_key_is_rejected_before_calling_ai_service():
    engine = _engine()
    response = engine.explain_topic("does.not.exist", _context(), AIRole.OWNER)
    assert response.accepted is False
    assert "no knowledge entry found" in response.reason


def test_analyze_market_delegates_to_ai_service_analysis_capability():
    engine = _engine()
    response = engine.analyze_market(_context(), AIRole.OWNER)
    assert response.accepted is True
