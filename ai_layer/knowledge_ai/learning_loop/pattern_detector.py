"""
Learning Layer — Failure/Success Pattern Detector (Phase 60.6:
Learning Loop Foundation, TASK 4).

Groups already-built `ai_layer.knowledge_ai.learning_loop.models.LearningRecord`s by their three
real, structured condition dimensions (`strategy_name`, `session`,
`market_phase` -- the same three fields `backtesting_layer/statistics/context_report.py`
already groups `SignalPerformance` by) and reports each combination's
historical win rate, using `backtesting_layer.statistics.strategy_report.compute_win_rate()`
directly -- reused, not reimplemented, the same convention every prior
phase's grouping module has followed.

Deliberately does not attempt to parse `failure_type`/`success_pattern`
free text into structured sub-conditions (e.g. splitting "Against HTF
bias" into a boolean flag) -- both fields are disclosed, untyped free
text (see `ai_layer/knowledge_ai/learning_loop/models.py`'s own docstring, mirroring
`ai_layer.knowledge_ai.knowledge_base.journal.failure_analysis.FailureAnalysisEntry.reason`), and
building a text classifier for them would be new inference logic this
phase's own boundary does not ask for. Instead, the single most common
`failure_type`/`success_pattern` string in a group is surfaced as a
supporting example, never as a parsed, generalized rule.

Per this whole phase's hard boundary: `detect_patterns()` returns data
only. Nothing reads a `PatternInsight` back into `strategies/`,
`decision/`, or `risk/` to change behavior.

Phase 60.7 (Adaptive Intelligence Layer Foundation, TASK 4) extends
the grouping key with the two new condition dimensions
`ai_layer.knowledge_ai.learning_loop.models.LearningRecord` gained in TASK 3 (`htf_bias`/
`volatility_state`) — purely additive: every Phase 60.6 record has
both fields `None`, so grouping by the extended 5-tuple key produces
the exact same groups as before for any pre-existing record set, and
every existing test/caller keeps working unmodified.

`MIN_PATTERN_SAMPLE = 20` is a new named constant for the Director's
own worked example ("Samples: 5 -> Confidence: LOW, Samples: 100 ->
Confidence: HIGH"). That example is about a *confidence label*, not an
exclusion threshold, so `detect_patterns()`'s own `min_occurrences`
gate (still defaulting to 3 -- unchanged, to avoid a silent behavior
change for every existing caller) is left as-is; `MIN_PATTERN_SAMPLE`
is exported here for `ai_layer.knowledge_ai.learning_loop.confidence` (TASK 5) to import and use
for its own sample-size scoring, not consumed by this module itself.
"""

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from backtesting_layer.statistics.strategy_report import compute_win_rate
from ai_layer.knowledge_ai.learning_loop.models import LearningRecord

HIGH_SUCCESS = "HIGH_SUCCESS"
HIGH_FAILURE = "HIGH_FAILURE"
MIXED = "MIXED"

MIN_PATTERN_SAMPLE = 20

# (strategy_name, session, market_phase, htf_bias, volatility_state)
PatternKey = Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]


@dataclass(frozen=True)
class PatternInsight:
    """
    strategy_name/session/market_phase/htf_bias/volatility_state: the
        condition combination this insight describes -- every field
        but `strategy_name` may be None (no condition on that
        dimension among the grouped records).
    occurrences: total records in this group, regardless of result.
    win_count/loss_count: "TP"/"SL" counts specifically -- same
        vocabulary `strategy_report.StrategyPerformanceReport` uses.
    win_rate: `compute_win_rate(win_count, loss_count)`, reused
        directly.
    classification: HIGH_SUCCESS (win_rate >= high_threshold),
        HIGH_FAILURE (win_rate <= 1 - high_threshold), else MIXED.
    example_failure_type/example_success_pattern: the single most
        common non-None value of each field among this group's
        records -- an illustrative example, not a generalized rule.
        None if no record in the group set that field.
    """
    strategy_name: str
    session: Optional[str]
    market_phase: Optional[str]
    occurrences: int
    win_count: int
    loss_count: int
    win_rate: float
    classification: str
    htf_bias: Optional[str] = None
    volatility_state: Optional[str] = None
    example_failure_type: Optional[str] = None
    example_success_pattern: Optional[str] = None


def _most_common(values: Sequence[Optional[str]]) -> Optional[str]:
    present = [v for v in values if v is not None]
    if not present:
        return None
    return Counter(present).most_common(1)[0][0]


def group_records_for_patterns(
    records: Sequence[LearningRecord],
    min_occurrences: int = 3,
) -> Dict[PatternKey, List[LearningRecord]]:
    """
    The same grouping `detect_patterns()` itself performs (Phase 60.7,
    TASK 6), exposed directly so a caller (e.g. `ai_layer/knowledge_ai/learning_context.py`)
    can look up the raw records behind one `PatternInsight` -- e.g. for
    `ai_layer.knowledge_ai.learning_loop.confidence.compute_pattern_confidence()`, which needs the
    group's own records, not just the aggregate `PatternInsight` --
    without duplicating this grouping logic. Skips any record with
    `strategy_name is None`, same posture
    `strategy_report.build_strategy_report()` already uses. A group
    with fewer than `min_occurrences` records is dropped, same
    threshold `detect_patterns()` applies.
    """
    grouped: Dict[PatternKey, List[LearningRecord]] = {}
    for record in records:
        if record.strategy_name is None:
            continue
        key: PatternKey = (
            record.strategy_name, record.session, record.market_phase,
            record.htf_bias, record.volatility_state,
        )
        grouped.setdefault(key, []).append(record)

    return {key: group for key, group in grouped.items() if len(group) >= min_occurrences}


def detect_patterns(
    records: Sequence[LearningRecord],
    min_occurrences: int = 3,
    high_threshold: float = 0.65,
) -> List[PatternInsight]:
    """
    Skips any record with `strategy_name is None` (nothing to group it
    under, same posture `strategy_report.build_strategy_report()`
    already uses for its own `strategy_id`). A group with fewer than
    `min_occurrences` records is dropped -- too few data points to call
    a "pattern," not statistically meaningful. Never raises: an empty
    or all-below-threshold input produces an empty list.
    """
    grouped = group_records_for_patterns(records, min_occurrences)

    insights: List[PatternInsight] = []
    for (strategy_name, session, market_phase, htf_bias, volatility_state), group in grouped.items():
        win_count = sum(1 for r in group if r.result == "TP")
        loss_count = sum(1 for r in group if r.result == "SL")
        win_rate = compute_win_rate(win_count, loss_count)

        if win_rate >= high_threshold:
            classification = HIGH_SUCCESS
        elif win_rate <= (1.0 - high_threshold):
            classification = HIGH_FAILURE
        else:
            classification = MIXED

        insights.append(PatternInsight(
            strategy_name=strategy_name,
            session=session,
            market_phase=market_phase,
            occurrences=len(group),
            win_count=win_count,
            loss_count=loss_count,
            win_rate=win_rate,
            classification=classification,
            htf_bias=htf_bias,
            volatility_state=volatility_state,
            example_failure_type=_most_common([r.failure_type for r in group]),
            example_success_pattern=_most_common([r.success_pattern for r in group]),
        ))

    insights.sort(key=lambda insight: (insight.occurrences, abs(insight.win_rate - 0.5)), reverse=True)
    return insights


def filter_high_failure_patterns(insights: Sequence[PatternInsight]) -> List[PatternInsight]:
    return [insight for insight in insights if insight.classification == HIGH_FAILURE]


def filter_high_success_patterns(insights: Sequence[PatternInsight]) -> List[PatternInsight]:
    return [insight for insight in insights if insight.classification == HIGH_SUCCESS]


def format_pattern_insight(insight: PatternInsight) -> str:
    """Matches the Director's own worked example shape: 'Liquidity Sweep + NY session -> High failure probability'."""
    condition = " + ".join(
        part for part in (
            insight.strategy_name, insight.session, insight.market_phase,
            insight.htf_bias, insight.volatility_state,
        ) if part is not None
    )
    label = {
        HIGH_FAILURE: "High failure probability",
        HIGH_SUCCESS: "High success probability",
        MIXED: "Mixed results",
    }[insight.classification]

    lines = [
        f"{condition} -> {label}",
        f"Occurrences: {insight.occurrences} (Win: {insight.win_count}, Loss: {insight.loss_count})",
        f"Win Rate: {insight.win_rate * 100:.0f}%",
    ]
    if insight.example_failure_type:
        lines.append(f"Example failure: {insight.example_failure_type}")
    if insight.example_success_pattern:
        lines.append(f"Example success: {insight.example_success_pattern}")

    return "\n".join(lines)
