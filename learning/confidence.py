"""
Learning Layer — Confidence Engine (Phase 60.7: Adaptive Intelligence
Layer Foundation, TASK 5).

Classifies a `learning.pattern_detector.PatternInsight` into
LOW/MEDIUM/HIGH confidence, per the Director's own formula:

    Confidence = Sample Size + Consistency + Recency + Performance

The Director's own worked example ("Samples: 5 -> Confidence: LOW,
Samples: 100 -> Confidence: HIGH") ties sample size to the *outcome*
even when nothing else is said about the other three factors — a
5-sample pattern must stay LOW no matter how clean its win rate looks,
the standard small-sample-overfitting caution. A plain four-way
average does not reproduce that: even a perfect 5-sample track record
would otherwise score HIGH. So sample size is a **multiplicative
gate**, not a fourth additive term:

    overall_score = sample_size_score * mean(consistency_score, recency_score, performance_score)

This module makes four disclosed, deterministic 0.0-1.0 sub-scores,
the same "reproduce the shape, not invent literal arithmetic"
precedent `context.fundamental_scoring`'s own worked-example handling
already established this session:

- **Sample Size**: `min(occurrences / MIN_PATTERN_SAMPLE, 1.0)` —
  reuses `learning.pattern_detector.MIN_PATTERN_SAMPLE` (20) directly
  as the "full confidence" reference point, not a second constant.
- **Consistency**: `abs(win_rate - 0.5) * 2.0` — how decisively
  one-sided the pattern's win rate already is (0.0 at a coin-flip
  50%, 1.0 at a clean 0% or 100%). Reuses `PatternInsight.win_rate`
  directly.
- **Recency**: linear decay of the most recent record's `created_at`
  over a disclosed 30-day window (1.0 today, 0.0 at 30+ days old) —
  no other "how stale is this pattern" concept exists anywhere in this
  codebase to reuse instead.
- **Performance**: the group's average `r_multiple`, mapped
  `clamp(avg_r / 2.0 + 0.5, 0.0, 1.0)` (0R -> 0.5 neutral, +1R -> 1.0,
  -1R -> 0.0) — reuses each record's already-real `r_multiple`, never
  a new PnL/profit computation.

Per this whole phase's hard boundary: `compute_pattern_confidence()`
returns data only — a `PatternConfidence` is never read back into
`strategies/`, `decision/`, or `risk/` to change behavior, and this
module calls none of them.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence

from learning.models import LearningRecord
from learning.pattern_detector import MIN_PATTERN_SAMPLE, PatternInsight

LOW = "LOW"
MEDIUM = "MEDIUM"
HIGH = "HIGH"

_RECENCY_WINDOW_DAYS = 30.0
_NEUTRAL_PERFORMANCE_SCORE = 0.5


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _sample_size_score(insight: PatternInsight) -> float:
    return _clamp(insight.occurrences / MIN_PATTERN_SAMPLE)


def _consistency_score(insight: PatternInsight) -> float:
    return _clamp(abs(insight.win_rate - 0.5) * 2.0)


def _recency_score(records: Sequence[LearningRecord], now: Optional[datetime] = None) -> float:
    """1.0 for a record created right now, 0.0 for one 30+ days old. None if no record carries a created_at at all."""
    timestamps = [r.created_at for r in records if r.created_at is not None]
    if not timestamps:
        return 0.0

    reference = now or datetime.now(timezone.utc)
    most_recent = max(timestamps)
    age_days = max((reference - most_recent).total_seconds() / 86400.0, 0.0)
    return _clamp(1.0 - (age_days / _RECENCY_WINDOW_DAYS))


def _performance_score(records: Sequence[LearningRecord]) -> float:
    """Neutral 0.5 (not 0.0) when no record carries an r_multiple -- an unknown average is not the same as a bad one."""
    r_multiples = [r.r_multiple for r in records if r.r_multiple is not None]
    if not r_multiples:
        return _NEUTRAL_PERFORMANCE_SCORE

    average_r = sum(r_multiples) / len(r_multiples)
    return _clamp(average_r / 2.0 + 0.5)


@dataclass(frozen=True)
class PatternConfidence:
    """
    sample_size_score/consistency_score/recency_score/performance_score:
        each 0.0-1.0, see module docstring for each formula.
    overall_score: `sample_size_score * mean(consistency_score,
        recency_score, performance_score)` — sample size gates the
        other three rather than averaging alongside them, see module
        docstring for why.
    level: LOW (overall_score < 0.33), MEDIUM (< 0.66), else HIGH.
    """
    sample_size_score: float
    consistency_score: float
    recency_score: float
    performance_score: float
    overall_score: float
    level: str


def compute_pattern_confidence(
    insight: PatternInsight,
    records: Sequence[LearningRecord],
    now: Optional[datetime] = None,
) -> PatternConfidence:
    """
    `records` should be the same group `insight` was built from
    (`learning.pattern_detector.detect_patterns()`'s own grouping) --
    this function does not re-filter or re-group them itself. `now`
    lets a caller pin recency scoring to a fixed instant (tests); a
    live caller omits it and gets `datetime.now(timezone.utc)`. Never
    raises: an empty `records` sequence produces recency=0.0 and
    performance=0.5 (neutral), not an exception.
    """
    sample_size_score = _sample_size_score(insight)
    consistency_score = _consistency_score(insight)
    recency_score = _recency_score(records, now)
    performance_score = _performance_score(records)

    overall_score = sample_size_score * ((consistency_score + recency_score + performance_score) / 3.0)

    if overall_score >= 0.66:
        level = HIGH
    elif overall_score >= 0.33:
        level = MEDIUM
    else:
        level = LOW

    return PatternConfidence(
        sample_size_score=sample_size_score,
        consistency_score=consistency_score,
        recency_score=recency_score,
        performance_score=performance_score,
        overall_score=overall_score,
        level=level,
    )
