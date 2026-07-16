"""
AI Layer — AI Tool Registry (Phase 61.0: AI Infrastructure
Foundation, TASK 8; real logic Phase 61.3: AI Intelligence Layer,
TASK 4).

`BaseAITool` is the shared contract every tool in this package
implements. Every concrete tool's `run()` now performs real,
read-only formatting logic over an already-built input object passed
in via `**kwargs` (a `MarketContext`, a `FundamentalContextSnapshot`,
a `Sequence[SignalPerformance]`, a `LearningContext`, or a
`knowledge/` lookup) -- none fetches its own data. `ai/` still holds
no runtime dependency on `database/`, `context/`, or `core.pipeline`
(see `ai/context/context_adapter.py`'s docstring for why `ai/` never
reaches `context/` directly); the caller that already legitimately
built the input object is responsible for supplying it. A future
integration phase decides which caller wires a real input source in
(never a write -- tools are advisory, same boundary as every other
`ai/` module).
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
    """Registers this package's five named tools -- imported lazily inside the function body to avoid a module-level import cycle with the tool modules themselves (each of which does not import this function)."""
    from ai.tools.analytics_tool import AnalyticsTool
    from ai.tools.education_tool import EducationTool
    from ai.tools.learning_tool import LearningTool
    from ai.tools.market_tool import MarketTool
    from ai.tools.news_tool import NewsTool

    registry = ToolRegistry()
    for tool in (MarketTool(), NewsTool(), AnalyticsTool(), EducationTool(), LearningTool()):
        registry.register(tool)
    return registry
