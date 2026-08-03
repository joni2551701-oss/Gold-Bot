"""
AI Layer — Analytics Tool (Phase 61.0, TASK 8; real logic Phase 61.3,
TASK 4).

Builds a real strategy performance report via
`backtesting_layer.statistics.strategy_report.build_strategy_report()` over an
already-fetched `Sequence[SignalPerformance]` -- the same
already-established `ai/` -> `analytics/` import
`ai_layer/knowledge_ai/learning_context.py` uses for `backtesting_layer.statistics.strategy_report.compute_win_rate`
(Phase 60.6). This tool never reads `database/` itself; a caller that
already legitimately has performance records passes them in.
"""

from typing import Optional, Sequence

from backtesting_layer.statistics.signal_performance import SignalPerformance
from backtesting_layer.statistics.strategy_report import build_strategy_report
from ai_layer.ai_service.tools.tool_registry import BaseAITool, ToolResult


class AnalyticsTool(BaseAITool):
    @property
    def name(self) -> str:
        return "analytics_tool"

    @property
    def description(self) -> str:
        return "Answers performance/analytics questions from an already-fetched sequence of SignalPerformance records."

    def run(self, performances: Optional[Sequence[SignalPerformance]] = None, **kwargs) -> ToolResult:
        if not performances:
            return ToolResult(
                content="No performance records were supplied to this tool call.",
                metadata={"tool": self.name, "strategy_count": 0},
            )

        report = build_strategy_report(performances)
        if not report:
            return ToolResult(
                content="Supplied records carry no strategy_id -- nothing to report per-strategy.",
                metadata={"tool": self.name, "strategy_count": 0},
            )

        lines = [
            f"{strategy_id}: {stats.win_count}W/{stats.loss_count}L, "
            f"win_rate={stats.win_rate:.2%}, total={stats.total_signals}"
            for strategy_id, stats in sorted(report.items())
        ]
        return ToolResult(
            content="\n".join(lines),
            metadata={"tool": self.name, "strategy_count": len(report)},
        )
