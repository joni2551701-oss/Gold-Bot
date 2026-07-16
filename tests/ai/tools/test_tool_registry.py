"""Phase 61.0 TASK 8 — AI Tool Registry: interface only, no database/pipeline call."""

import pytest

from ai.tools.analytics_tool import AnalyticsTool
from ai.tools.education_tool import EducationTool
from ai.tools.market_tool import MarketTool
from ai.tools.news_tool import NewsTool
from ai.tools.tool_registry import BaseAITool, ToolRegistry, build_default_tool_registry

ALL_TOOLS = [MarketTool, NewsTool, AnalyticsTool, EducationTool]


def test_base_tool_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        BaseAITool()


@pytest.mark.parametrize("tool_cls", ALL_TOOLS)
def test_tool_run_returns_a_placeholder_result_tagged_with_its_own_name(tool_cls):
    tool = tool_cls()
    result = tool.run()
    assert result.metadata["tool"] == tool.name
    assert tool.name in result.content


def test_registry_registers_and_retrieves_a_tool():
    registry = ToolRegistry()
    tool = MarketTool()
    registry.register(tool)
    assert registry.get("market_tool") is tool


def test_registry_get_returns_none_for_unknown_tool():
    registry = ToolRegistry()
    assert registry.get("unknown") is None


def test_build_default_tool_registry_registers_all_four_named_tools():
    registry = build_default_tool_registry()
    assert set(registry.list_tools()) == {"market_tool", "news_tool", "analytics_tool", "education_tool"}
