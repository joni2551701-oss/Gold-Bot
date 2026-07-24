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

Phase 60.7 (Adaptive Intelligence Layer Foundation, TASK 6) extends
`LearningContext` with four additional fields the Director's own brief
names (`patterns`/`failures`/`regimes`/`confidence`) -- purely
additive, `recent_failures`/`successful_patterns`/`strategy_stats`
keep their exact Phase 60.6 meaning and default shape:

- `patterns`: every `PatternInsight` `detect_patterns()` found
  (`format_pattern_insight()`'s own text), regardless of
  classification -- `successful_patterns` stays the `HIGH_SUCCESS`-only
  subset it already was.
- `failures`: the `HIGH_FAILURE`-classified patterns, the mirror-image
  of `successful_patterns` -- a pattern-level view, distinct from
  `recent_failures`' per-record `failure_type` strings.
- `confidence`: one `"<condition>: <LEVEL>"` line per pattern, via
  `learning.confidence.compute_pattern_confidence()` (TASK 5) and
  `learning.pattern_detector.group_records_for_patterns()` (the same
  grouping `detect_patterns()` itself performs, reused directly to
  avoid re-deriving which records belong to which pattern).
- `regimes`: caller-supplied, pre-formatted regime observation
  strings (e.g. from `learning.regime_memory`, TASK 7) -- accepted as
  a plain `Sequence[str]` rather than importing `learning.regime_memory`
  directly, so this module's own dependency set does not need to
  change again once that module exists; a caller composes both.

Still context only -- none of these four fields are themselves an
explanation, conclusion, or recommendation; that stays the one thing
a future AI consumer of this context may add.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence

from analytics.strategy_report import compute_win_rate
from learning.confidence import compute_pattern_confidence
from learning.models import LearningRecord
from learning.pattern_detector import (
    PatternInsight,
    detect_patterns,
    filter_high_failure_patterns,
    filter_high_success_patterns,
    format_pattern_insight,
    group_records_for_patterns,
)


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
    patterns (Phase 60.7): every pattern `detect_patterns()` found,
        regardless of classification.
    failures (Phase 60.7): the `HIGH_FAILURE`-classified patterns.
    regimes (Phase 60.7): caller-supplied regime observation strings
        -- empty unless the caller passes `regimes=` to
        `build_learning_context()`.
    confidence (Phase 60.7): one `"<condition>: <LEVEL>"` line per
        pattern in `patterns`, via
        `learning.confidence.compute_pattern_confidence()`.
    """
    recent_failures: List[str] = field(default_factory=list)
    successful_patterns: List[str] = field(default_factory=list)
    strategy_stats: List[str] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    failures: List[str] = field(default_factory=list)
    regimes: List[str] = field(default_factory=list)
    confidence: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "recent_failures": list(self.recent_failures),
            "successful_patterns": list(self.successful_patterns),
            "strategy_stats": list(self.strategy_stats),
            "patterns": list(self.patterns),
            "failures": list(self.failures),
            "regimes": list(self.regimes),
            "confidence": list(self.confidence),
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


def _pattern_condition(insight: PatternInsight) -> str:
    """Same condition-string shape `pattern_detector.format_pattern_insight()` itself builds -- kept in sync deliberately, not imported (that function returns a multi-line report, not a bare condition label)."""
    return " + ".join(
        part for part in (
            insight.strategy_name, insight.session, insight.market_phase,
            insight.htf_bias, insight.volatility_state,
        ) if part is not None
    )


def _confidence_summaries(records: Sequence[LearningRecord], patterns: Sequence[PatternInsight]) -> List[str]:
    """One '<condition>: <LEVEL>' line per pattern, via learning.confidence.compute_pattern_confidence() -- reuses group_records_for_patterns() rather than re-deriving which records belong to which pattern."""
    groups = group_records_for_patterns(records)
    summaries = []
    for insight in patterns:
        key = (insight.strategy_name, insight.session, insight.market_phase, insight.htf_bias, insight.volatility_state)
        group = groups.get(key, [])
        pattern_confidence = compute_pattern_confidence(insight, group)
        summaries.append(f"{_pattern_condition(insight)}: {pattern_confidence.level}")
    return summaries


def build_learning_context(
    records: Sequence[LearningRecord],
    patterns: Optional[Sequence[PatternInsight]] = None,
    limit: int = 5,
    regimes: Optional[Sequence[str]] = None,
) -> LearningContext:
    """
    `patterns`, when omitted, is computed via `detect_patterns(records)`
    with its own default `min_occurrences` -- a caller with an
    already-computed pattern list (e.g. from a prior
    `analytics.learning_report.build_learning_report()` call) can pass
    it directly to avoid recomputing. `regimes` is relayed as-is (an
    already-formatted sequence, e.g. from a future
    `learning.regime_memory` caller) -- this module never fetches or
    computes regime data itself. Never raises: an empty `records`
    produces a `LearningContext` with every list empty.
    """
    if patterns is None:
        patterns = detect_patterns(records)

    successful_patterns = [format_pattern_insight(insight) for insight in filter_high_success_patterns(patterns)]
    all_patterns = [format_pattern_insight(insight) for insight in patterns]
    failures = [format_pattern_insight(insight) for insight in filter_high_failure_patterns(patterns)]

    return LearningContext(
        recent_failures=_recent_failures(records, limit),
        successful_patterns=successful_patterns[:limit],
        strategy_stats=_strategy_stats(records),
        patterns=all_patterns[:limit],
        failures=failures[:limit],
        regimes=list(regimes) if regimes is not None else [],
        confidence=_confidence_summaries(records, patterns)[:limit],
    )
