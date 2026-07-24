"""
AI Layer — Learning Tool (Phase 61.3, TASK 4, new).

Formats an already-built `ai.learning_context.LearningContext` --
never fetches `learning.models.LearningRecord` itself. `ai/` already
legitimately builds `LearningContext` internally
(`ai/learning_context.py`, Phase 60.6/60.7) from a caller-supplied
`Sequence[LearningRecord]`; this tool is a thin formatter over that
existing type, the same "accept already-computed data" convention
`market_tool.py` and `news_tool.py` use. No new import of `database/`
or `learning/` beyond what `ai/learning_context.py` already has.
"""

from typing import Optional

from ai.learning_context import LearningContext
from ai.tools.tool_registry import BaseAITool, ToolResult


class LearningTool(BaseAITool):
    @property
    def name(self) -> str:
        return "learning_tool"

    @property
    def description(self) -> str:
        return "Answers learning/trade-history questions from an already-built LearningContext."

    def run(self, learning_context: Optional[LearningContext] = None, **kwargs) -> ToolResult:
        if learning_context is None:
            return ToolResult(
                content="No learning context was supplied to this tool call.",
                metadata={"tool": self.name, "has_context": False},
            )

        parts = []
        if learning_context.strategy_stats:
            parts.append("Strategy stats: " + "; ".join(learning_context.strategy_stats))
        if learning_context.successful_patterns:
            parts.append("Successful patterns: " + "; ".join(learning_context.successful_patterns))
        if learning_context.recent_failures:
            parts.append("Recent failures: " + "; ".join(learning_context.recent_failures))

        content = " | ".join(parts) if parts else "Learning context carries no data yet."
        return ToolResult(
            content=content,
            metadata={
                "tool": self.name,
                "has_context": True,
                "strategy_count": len(learning_context.strategy_stats),
                "failure_count": len(learning_context.recent_failures),
            },
        )
