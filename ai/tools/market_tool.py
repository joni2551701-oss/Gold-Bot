"""
AI Layer — Market Tool (Phase 61.0, TASK 8; real logic Phase 61.3,
TASK 4).

Formats an already-built `MarketContext` -- never fetches one.
`ai/` deliberately holds no runtime dependency on `context/` or
`data/` (see `ai/context/context_adapter.py`'s own docstring for the
established boundary this reuses); the (future, unwired) caller that
already legitimately builds a `MarketContext` -- e.g. via
`ai.context.context_adapter.market_context_from_snapshot()` -- is
responsible for passing it in as `run(market_context=...)`.
"""

from typing import Optional

from ai.interfaces import MarketContext
from ai.tools.tool_registry import BaseAITool, ToolResult


class MarketTool(BaseAITool):
    @property
    def name(self) -> str:
        return "market_tool"

    @property
    def description(self) -> str:
        return "Answers market-context questions from an already-built MarketContext."

    def run(self, market_context: Optional[MarketContext] = None, **kwargs) -> ToolResult:
        if market_context is None:
            return ToolResult(
                content="No market context was supplied to this tool call.",
                metadata={"tool": self.name, "has_context": False},
            )
        return ToolResult(
            content=(
                f"{market_context.symbol} ({market_context.timeframe}): "
                f"{market_context.summary}"
            ),
            metadata={
                "tool": self.name,
                "has_context": True,
                "symbol": market_context.symbol,
                "timeframe": market_context.timeframe,
            },
        )
