"""
AI Layer — News Tool (Phase 61.0, TASK 8; real logic Phase 61.3,
TASK 4).

Formats an already-built `context.fundamental_context.FundamentalContextSnapshot`
-- never fetches or computes one. Same `TYPE_CHECKING`-only pattern
`ai/prompts/prompt_manager.py`'s `get_fundamental_analysis_prompt()`
already established (Phase 60.5) for referencing this exact type
without giving `ai/` a runtime dependency on `context/`.
"""

from typing import Optional, TYPE_CHECKING

from ai_layer.ai_service.tools.tool_registry import BaseAITool, ToolResult

if TYPE_CHECKING:
    from context_layer.fundamental.fundamental_context import FundamentalContextSnapshot


class NewsTool(BaseAITool):
    @property
    def name(self) -> str:
        return "news_tool"

    @property
    def description(self) -> str:
        return "Answers economic-news/fundamental questions from an already-built FundamentalContextSnapshot."

    def run(self, fundamental: Optional['FundamentalContextSnapshot'] = None, **kwargs) -> ToolResult:
        if fundamental is None:
            return ToolResult(
                content="No fundamental context was supplied to this tool call.",
                metadata={"tool": self.name, "has_context": False},
            )

        parts = []
        if fundamental.dxy_bias:
            parts.append(f"DXY bias: {fundamental.dxy_bias}")
        if fundamental.rates_bias:
            parts.append(f"Rates bias: {fundamental.rates_bias}")
        if fundamental.inflation_bias:
            parts.append(f"Inflation bias: {fundamental.inflation_bias}")
        if fundamental.fed_expectation:
            parts.append(f"Fed expectation: {fundamental.fed_expectation}")
        if fundamental.risk_sentiment:
            parts.append(f"Risk sentiment: {fundamental.risk_sentiment}")
        if fundamental.gold_bias:
            parts.append(f"Gold bias: {fundamental.gold_bias}")

        content = ", ".join(parts) if parts else "Fundamental context has no scored fields yet."
        return ToolResult(
            content=content,
            metadata={
                "tool": self.name,
                "has_context": True,
                "snapshot_id": fundamental.snapshot_id,
                "macro_score": fundamental.macro_score,
            },
        )
