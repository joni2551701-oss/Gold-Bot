"""
Phase 61.0 TASK 8 — AI Tool Registry (interface only, no database/
pipeline call). Extended Phase 61.3 TASK 4 — real, read-only tool
logic over already-built input objects.
"""

import pytest

from ai.tools.analytics_tool import AnalyticsTool
from ai.tools.education_tool import EducationTool
from ai.tools.learning_tool import LearningTool
from ai.tools.market_tool import MarketTool
from ai.tools.news_tool import NewsTool
from ai.tools.tool_registry import BaseAITool, ToolRegistry, build_default_tool_registry

ALL_TOOLS = [MarketTool, NewsTool, AnalyticsTool, EducationTool, LearningTool]


def test_base_tool_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        BaseAITool()


@pytest.mark.parametrize("tool_cls", ALL_TOOLS)
def test_tool_run_with_no_input_returns_a_graceful_result_tagged_with_its_own_name(tool_cls):
    tool = tool_cls()
    result = tool.run()
    assert result.metadata["tool"] == tool.name
    assert "no" in result.content.lower() or "none" in result.content.lower()


def test_registry_registers_and_retrieves_a_tool():
    registry = ToolRegistry()
    tool = MarketTool()
    registry.register(tool)
    assert registry.get("market_tool") is tool


def test_registry_get_returns_none_for_unknown_tool():
    registry = ToolRegistry()
    assert registry.get("unknown") is None


def test_build_default_tool_registry_registers_all_five_named_tools():
    registry = build_default_tool_registry()
    assert set(registry.list_tools()) == {
        "market_tool", "news_tool", "analytics_tool", "education_tool", "learning_tool",
    }


def test_market_tool_formats_a_supplied_market_context():
    from ai.interfaces import MarketContext

    tool = MarketTool()
    context = MarketContext(symbol="XAUUSD", timeframe="M15", summary="Regime: TRENDING, Trend: BULLISH")
    result = tool.run(market_context=context)
    assert result.metadata["has_context"] is True
    assert "XAUUSD" in result.content
    assert "TRENDING" in result.content


def test_news_tool_formats_a_supplied_fundamental_snapshot():
    from datetime import datetime, timezone

    from context_layer.fundamental.fundamental_context import FundamentalContextSnapshot

    tool = NewsTool()
    snapshot = FundamentalContextSnapshot(
        snapshot_id="fs-1",
        created_at=datetime.now(timezone.utc),
        dxy_bias="STRONG",
        gold_bias="BULLISH",
    )
    result = tool.run(fundamental=snapshot)
    assert result.metadata["has_context"] is True
    assert "DXY bias: STRONG" in result.content
    assert "Gold bias: BULLISH" in result.content


def test_analytics_tool_builds_a_real_strategy_report():
    from analytics.signal_performance import SignalPerformance, generate_performance_id

    tool = AnalyticsTool()
    performances = [
        SignalPerformance(performance_id=generate_performance_id(), signal_id="s1", strategy_id="amd_strategy", result="TP"),
        SignalPerformance(performance_id=generate_performance_id(), signal_id="s2", strategy_id="amd_strategy", result="SL"),
    ]
    result = tool.run(performances=performances)
    assert result.metadata["strategy_count"] == 1
    assert "amd_strategy" in result.content
    assert "1W/1L" in result.content


def test_education_tool_looks_up_a_known_key():
    tool = EducationTool()
    result = tool.run(key="smc.bos")
    assert result.metadata["match_count"] == 1
    assert "Break of Structure" in result.content


def test_education_tool_searches_by_query():
    tool = EducationTool()
    result = tool.run(query="fomo")
    assert result.metadata["match_count"] >= 1
    assert "FOMO" in result.content


def test_learning_tool_formats_a_supplied_learning_context():
    from ai.learning_context import LearningContext

    tool = LearningTool()
    context = LearningContext(strategy_stats=["amd_strategy: 60.0%"], recent_failures=["SL_TOO_TIGHT"])
    result = tool.run(learning_context=context)
    assert result.metadata["has_context"] is True
    assert "amd_strategy: 60.0%" in result.content
    assert "SL_TOO_TIGHT" in result.content
