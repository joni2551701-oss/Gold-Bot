"""
Analytics Layer — Learning Report (Phase 60.6: Learning Loop
Foundation, TASK 6).

Reuses `learning.pattern_detector.detect_patterns()` directly, not
reimplemented -- picks the single highest- and lowest-win-rate
condition combination among the patterns it already found, matching
the Director's own worked example shape:

    Last 100 trades
    Best condition:
    London
    Liquidity Sweep
    Win rate 72%
    Worst condition:
    NY news
    Counter trend
    Win rate 31%

The brief's own illustrative example additionally names "H4 bullish"
under Best Condition -- an HTF-alignment detail `learning.models.LearningRecord`
does not carry as a structured field (only `strategy_name`/`session`/
`market_phase` are real grouping dimensions, same three
`learning.pattern_detector.detect_patterns()` already groups by). This
report reproduces the shape with the three real dimensions, not a
fabricated fourth one -- the same disclosed, deliberate substitution
`context_layer.fundamental.fundamental_scoring`'s own worked-example handling already
established this session.
"""

from dataclasses import dataclass
from typing import Optional, Sequence

from learning.models import LearningRecord
from learning.pattern_detector import PatternInsight, detect_patterns


@dataclass(frozen=True)
class LearningReport:
    """
    total_records: every `LearningRecord` passed in, regardless of
        whether it belonged to a large-enough group to become a
        pattern.
    best_condition/worst_condition: the highest-/lowest-win-rate
        `PatternInsight` among `detect_patterns()`'s own output; both
        `None` when no group met `min_occurrences` (too little data to
        call anything a "condition" yet).
    """
    total_records: int
    best_condition: Optional[PatternInsight] = None
    worst_condition: Optional[PatternInsight] = None


def build_learning_report(records: Sequence[LearningRecord], min_occurrences: int = 3) -> LearningReport:
    """Never raises: an empty or all-below-threshold input produces a report with total_records set and both conditions None."""
    insights = detect_patterns(records, min_occurrences=min_occurrences)
    if not insights:
        return LearningReport(total_records=len(records))

    best = max(insights, key=lambda insight: insight.win_rate)
    worst = min(insights, key=lambda insight: insight.win_rate)

    return LearningReport(total_records=len(records), best_condition=best, worst_condition=worst)


def _format_condition(insight: PatternInsight) -> str:
    lines = [part for part in (insight.session, insight.strategy_name, insight.market_phase) if part is not None]
    lines.append(f"Win rate {insight.win_rate * 100:.0f}%")
    return "\n".join(lines)


def format_learning_report(report: LearningReport) -> str:
    """Matches the Director's own worked example shape exactly. Pure formatting, no computation."""
    lines = [f"Last {report.total_records} trades"]

    if report.best_condition is not None:
        lines.append("Best condition:")
        lines.append(_format_condition(report.best_condition))
    if report.worst_condition is not None:
        lines.append("Worst condition:")
        lines.append(_format_condition(report.worst_condition))
    if report.best_condition is None and report.worst_condition is None:
        lines.append("Not enough data yet for a condition breakdown.")

    return "\n".join(lines)
