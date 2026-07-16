"""
AI Layer — AI Tool Registry (Phase 61.0: AI Infrastructure
Foundation, TASK 8).

`BaseAITool` is the shared contract every tool in this package
implements. "Tool faqat interface. Hech biri database yoki pipeline'ni
chaqirmaydi" (a tool is interface only -- none call database or
pipeline) -- every concrete tool's `run()` returns a fixed stub
`ToolResult`, never a real `database.*_repository` or
`core.pipeline` call. A future integration phase decides which tool
gets wired to a real read (never a write -- tools are advisory, same
boundary as every other `ai/` module).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class ToolResult:
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAITool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        raise NotImplementedError


class ToolRegistry:
    """In-memory registry, same register/list/get shape as `ai/providers/provider_registry.py`'s catalog, sized for a handful of tools."""

    def __init__(self) -> None:
        self._tools: Dict[str, BaseAITool] = {}

    def register(self, tool: BaseAITool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseAITool:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())


def build_default_tool_registry() -> ToolRegistry:
    """Registers this package's four named tools -- imported lazily inside the function body to avoid a module-level import cycle with the tool modules themselves (each of which does not import this function)."""
    from ai.tools.analytics_tool import AnalyticsTool
    from ai.tools.education_tool import EducationTool
    from ai.tools.market_tool import MarketTool
    from ai.tools.news_tool import NewsTool

    registry = ToolRegistry()
    for tool in (MarketTool(), NewsTool(), AnalyticsTool(), EducationTool()):
        registry.register(tool)
    return registry
