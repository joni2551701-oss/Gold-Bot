"""
AI Layer — Learning Context (Phase 60.6: Learning Loop Foundation,
TASK 7).

Builds the AI-facing input shape the Director's own brief names:

    {
      "recent_failures": [],
      "successful_patterns": [],
      "strategy_stats": []
    }

This module only bundles already-computed data -- it does NOT itself
generate any explanation, conclusion, or recommendation text. Per the
Director's own brief, that is the one thing a future AI consumer of
this context is allowed to produce ("AI: Faqat tushuntirish, xulosa,
tavsiya" -- explanation, conclusion, recommendation only), and even
then strictly advisory: the same `AIAnalyzerInterface` boundary
`ai/interfaces.py` already documents applies here too -- a future AI
that reads a `LearningContext` must never itself approve/reject a
trade, call `risk.risk_manager.RiskManager`, or mutate a strategy
parameter. This module has no LLM call, no network access, and is not
called from `core/pipeline.py`.

Reuses `learning.pattern_detector.detect_patterns()`/
`filter_high_success_patterns()`/`format_pattern_insight()` directly
for the `successful_patterns` list, and
`analytics.strategy_report.compute_win_rate()` directly for
`strategy_stats` -- neither win-rate arithmetic nor pattern grouping
is reimplemented here.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence

from analytics.strategy_report import compute_win_rate
from learning.models import LearningRecord
from learning.pattern_detector import PatternInsight, detect_patterns, filter_high_success_patterns, format_pattern_insight


@dataclass(frozen=True)
class LearningContext:
    """
    recent_failures: the most recent non-None `failure_type` strings,
        newest first -- free text, relayed directly, never
        interpreted.
    successful_patterns: `format_pattern_insight()`'s own text for
        each `HIGH_SUCCESS`-classified pattern `detect_patterns()`
        found -- already-computed, not recomputed here.
    strategy_stats: one short "`strategy_name`: `win_rate`%" line per
        strategy with at least one decided (TP/SL) record.
    """
    recent_failures: List[str] = field(default_factory=list)
    successful_patterns: List[str] = field(default_factory=list)
    strategy_stats: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "recent_failures": list(self.recent_failures),
            "successful_patterns": list(self.successful_patterns),
            "strategy_stats": list(self.strategy_stats),
        }


def _recent_failures(records: Sequence[LearningRecord], limit: int) -> List[str]:
    ordered = sorted(
        (r for r in records if r.failure_type is not None),
        key=lambda r: r.created_at or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return [r.failure_type for r in ordered[:limit]]


def _strategy_stats(records: Sequence[LearningRecord]) -> List[str]:
    grouped: Dict[str, List[LearningRecord]] = defaultdict(list)
    for record in records:
        if record.strategy_name is not None:
            grouped[record.strategy_name].append(record)

    stats = []
    for strategy_name, group in grouped.items():
        win_count = sum(1 for r in group if r.result == "TP")
        loss_count = sum(1 for r in group if r.result == "SL")
        if win_count + loss_count == 0:
            continue
        win_rate = compute_win_rate(win_count, loss_count)
        stats.append(f"{strategy_name}: {win_rate * 100:.0f}%")

    return stats


def build_learning_context(
    records: Sequence[LearningRecord],
    patterns: Optional[Sequence[PatternInsight]] = None,
    limit: int = 5,
) -> LearningContext:
    """
    `patterns`, when omitted, is computed via `detect_patterns(records)`
    with its own default `min_occurrences` -- a caller with an
    already-computed pattern list (e.g. from a prior
    `analytics.learning_report.build_learning_report()` call) can pass
    it directly to avoid recomputing. Never raises: an empty `records`
    produces a `LearningContext` with all three lists empty.
    """
    if patterns is None:
        patterns = detect_patterns(records)

    successful_patterns = [format_pattern_insight(insight) for insight in filter_high_success_patterns(patterns)]

    return LearningContext(
        recent_failures=_recent_failures(records, limit),
        successful_patterns=successful_patterns[:limit],
        strategy_stats=_strategy_stats(records),
    )
