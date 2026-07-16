"""AI Layer — Analytics Tool (Phase 61.0, TASK 8). Interface only -- does not call analytics/ or database/."""

from ai.tools.tool_registry import BaseAITool, ToolResult


class AnalyticsTool(BaseAITool):
    @property
    def name(self) -> str:
        return "analytics_tool"

    @property
    def description(self) -> str:
        return "Would answer performance/analytics questions for the AI layer. Placeholder -- no real analytics/ call yet."

    def run(self, **kwargs) -> ToolResult:
        return ToolResult(content="[analytics_tool] placeholder -- no real analytics call yet.", metadata={"tool": self.name})
