"""AI Layer — Market Tool (Phase 61.0, TASK 8). Interface only -- does not call data/, context/, or the live pipeline."""

from ai.tools.tool_registry import BaseAITool, ToolResult


class MarketTool(BaseAITool):
    @property
    def name(self) -> str:
        return "market_tool"

    @property
    def description(self) -> str:
        return "Would answer market-context questions for the AI layer. Placeholder -- no real data/ call yet."

    def run(self, **kwargs) -> ToolResult:
        return ToolResult(content="[market_tool] placeholder -- no real market data call yet.", metadata={"tool": self.name})
