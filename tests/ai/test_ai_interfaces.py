"""
Phase 55 — AI interface foundation tests.

No real AI/LLM call anywhere in ai/interfaces.py -- these tests only
confirm the data contracts construct correctly and the abstract
interface enforces its contract, matching this phase's explicit
"real AI test kerak emas" scope.
"""

import pytest

from ai.interfaces import AIAnalyzerInterface, MarketContext, UserContext, AIResponse


def test_market_context_constructs_with_required_fields():
    ctx = MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend")
    assert ctx.symbol == "XAUUSD"
    assert ctx.timeframe == "M15"
    assert ctx.summary == "uptrend"
    assert ctx.metadata == {}


def test_market_context_is_immutable():
    ctx = MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend")
    with pytest.raises(Exception):
        ctx.symbol = "EURUSD"


def test_user_context_is_fully_optional():
    ctx = UserContext()
    assert ctx.telegram_id is None
    assert ctx.experience_level is None
    assert ctx.preferred_strategy is None
    assert ctx.risk_style is None
    assert ctx.language is None


def test_user_context_accepts_all_fields():
    ctx = UserContext(
        telegram_id="123", experience_level="beginner",
        preferred_strategy="FVG", risk_style="conservative", language="EN",
    )
    assert ctx.telegram_id == "123"
    assert ctx.experience_level == "beginner"


def test_ai_response_constructs_with_expected_shape():
    response = AIResponse(decision="HOLD", confidence=0.5, explanation="foundation test")
    assert response.decision == "HOLD"
    assert response.confidence == 0.5
    assert response.explanation == "foundation test"
    assert response.metadata == {}


def test_ai_response_is_immutable():
    response = AIResponse(decision="HOLD", confidence=0.5, explanation="x")
    with pytest.raises(Exception):
        response.confidence = 0.9


def test_ai_analyzer_interface_cannot_be_instantiated_directly():
    """It's an ABC -- a concrete implementation must provide evaluate()."""
    with pytest.raises(TypeError):
        AIAnalyzerInterface()


def test_ai_analyzer_interface_requires_evaluate_implementation():
    class IncompleteProvider(AIAnalyzerInterface):
        pass

    with pytest.raises(TypeError):
        IncompleteProvider()


def test_ai_analyzer_interface_can_be_implemented():
    """A minimal, real implementation satisfies the contract -- no LLM call, just shape."""

    class StubProvider(AIAnalyzerInterface):
        def evaluate(self, market_context, user_context=None):
            return AIResponse(decision="HOLD", confidence=0.0, explanation="stub, no real AI")

    provider = StubProvider()
    result = provider.evaluate(MarketContext(symbol="XAUUSD", timeframe="M15", summary="test"))
    assert isinstance(result, AIResponse)
    assert result.decision == "HOLD"


def test_production_analyzer_does_not_implement_the_new_interface_yet():
    """
    Documents the current, deliberate state (docs/AI_ARCHITECTURE.md):
    retrofitting the production AIAnalyzer onto this interface is out
    of scope this phase. This test exists so that decision is visible
    and explicit in the test suite, not just in a doc.
    """
    from ai.ai_analyzer import AIAnalyzer

    assert not issubclass(AIAnalyzer, AIAnalyzerInterface)
