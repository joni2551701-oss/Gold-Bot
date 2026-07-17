"""Phase 61.5 TASK 5 — AI Content Adapter. ContentEngine wraps AIService.ask() unmodified, same pattern as ExplanationEngine. Foundation only: no AIService dispatch mapping exists yet for any content capability, so generate() is always cleanly rejected today -- never fabricates content, never touches database/telegram, never produces a trading signal."""

from ai.access.permissions import AIRole
from ai.capabilities.capability import Capability
from ai.content.content_adapter import ContentEngine
from ai.content.content_schema import ContentRequest
from ai.context.context_builder import build_ai_context
from ai.interfaces import MarketContext
from ai.runtime.ai_service import AIService


def _context():
    return build_ai_context(market_context=MarketContext(symbol="XAUUSD", timeframe="M15", summary="uptrend"))


def test_generate_market_report_is_cleanly_rejected_today_never_fabricates_content():
    engine = ContentEngine(ai_service=AIService())
    request = ContentRequest(capability=Capability.AI_MARKET_REPORT, ai_context=_context(), role=AIRole.OWNER)

    result = engine.generate(request)

    assert result.accepted is False
    assert result.body is None
    assert result.content_type == "AI_MARKET_REPORT"
    assert result.title == "Market Report"
    assert result.generated_at is not None


def test_generate_rejects_a_non_content_capability_before_calling_ai_service():
    engine = ContentEngine(ai_service=AIService())
    request = ContentRequest(capability=Capability.CHAT, ai_context=_context(), role=AIRole.OWNER)

    result = engine.generate(request)

    assert result.accepted is False
    assert "not a content-generation capability" in result.reason


def test_generate_never_raises_for_every_content_capability():
    engine = ContentEngine(ai_service=AIService())
    for capability in (
        Capability.AI_MARKET_REPORT, Capability.AI_WEEKLY_OUTLOOK,
        Capability.AI_NEWS_ANALYSIS, Capability.AI_SCRIPT_GENERATION,
    ):
        request = ContentRequest(capability=capability, ai_context=_context(), role=AIRole.OWNER)
        result = engine.generate(request)
        assert result.accepted is False
        assert result.content_type == capability.value


def test_content_result_to_dict_is_json_serializable_shape():
    engine = ContentEngine(ai_service=AIService())
    request = ContentRequest(capability=Capability.AI_NEWS_ANALYSIS, ai_context=_context(), role=AIRole.OWNER, topic="Fed rate decision")

    result = engine.generate(request).to_dict()

    assert result["content_type"] == "AI_NEWS_ANALYSIS"
    assert result["accepted"] is False
    assert result["body"] is None
    assert "generated_at" in result


def test_generate_with_a_topic_never_raises():
    engine = ContentEngine(ai_service=AIService())
    request = ContentRequest(
        capability=Capability.AI_SCRIPT_GENERATION, ai_context=_context(), role=AIRole.OWNER,
        topic="XAUUSD breakout setup", telegram_id="111",
    )
    result = engine.generate(request)
    assert result.accepted is False
