"""AI Layer — News Tool (Phase 61.0, TASK 8). Interface only -- does not call any fundamental/news provider."""

from ai.tools.tool_registry import BaseAITool, ToolResult


class NewsTool(BaseAITool):
    @property
    def name(self) -> str:
        return "news_tool"

    @property
    def description(self) -> str:
        return "Would answer economic-news/fundamental questions for the AI layer. Placeholder -- no real provider call yet."

    def run(self, **kwargs) -> ToolResult:
        return ToolResult(content="[news_tool] placeholder -- no real news/fundamental call yet.", metadata={"tool": self.name})
