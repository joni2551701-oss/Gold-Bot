"""
Context Layer — Economic Event Model (Phase 60.5: Fundamental
Intelligence Foundation, TASK 4).

A calendar entry for a scheduled macro release (NFP, CPI, FOMC, ISM,
PMI, etc.) -- distinct from context/fundamental_context.py's
FundamentalContextSnapshot (a point-in-time indicator reading) and
context/fundamental_scoring.py's FundamentalScoreResult (an aggregate
bias/score): this module answers "what economic release is this, and
what did it say," not "what does it mean for gold" -- that
interpretation belongs to a future caller, same "data, not judgment"
boundary every provider-layer type in this codebase already holds
(see data/providers/fundamental_base.py's own docstring).

No fetch/schedule logic here -- this is a data model only, same
"standardization layer" posture as every other context/ dataclass.
Nothing in this codebase populates one yet (no economic-calendar
provider exists); a future data/ source would construct these.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class EventImpact(Enum):
    """Standard three-tier economic-calendar convention (widely used by e.g. Forex Factory/Investing.com), not invented here."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class EconomicEvent:
    """
    name: the release's own name (e.g. "NFP", "CPI", "FOMC Statement").
    date: the scheduled/actual release timestamp.
    impact: EventImpact -- the calendar's own stated importance, not
        computed here.
    currency: the release's currency (e.g. "USD" for every example
        this task's own brief names).
    expected/actual: the consensus forecast and the reported outcome,
        both None until the release happens (a future event has no
        actual yet; a past event may still have no expected if the
        source didn't report a consensus).
    """
    name: str
    date: datetime
    impact: EventImpact
    currency: str
    expected: Optional[float] = None
    actual: Optional[float] = None

    @property
    def surprise(self) -> Optional[float]:
        """actual - expected, the standard "beat/miss" figure -- None unless both are known. Never fabricated."""
        if self.expected is None or self.actual is None:
            return None
        return self.actual - self.expected

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "date": self.date.isoformat(),
            "impact": self.impact.value,
            "currency": self.currency,
            "expected": self.expected,
            "actual": self.actual,
            "surprise": self.surprise,
        }
