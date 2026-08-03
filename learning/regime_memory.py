"""
Learning Layer — Market Regime Memory (Phase 60.7: Adaptive
Intelligence Layer Foundation, TASK 7).

An in-memory, append-only observation log of which of the Director's
own five named regimes ("Trending, Range, High volatility, Low
volatility, News event") was seen and when. Four of the five map
directly onto `context.market_regime.MarketRegime`'s own real enum
values (`record_from_context()` relays `.value` directly, never
recomputing a regime classification itself); `"NEWS_EVENT"` is the one
category with no existing detector behind it in this codebase
(`context_layer/fundamental/economic_events.py`'s own docstring already discloses "no
economic-calendar provider exists" — an `EconomicEvent` cannot be
auto-detected from a `ContextSnapshot` today) — a caller records it
explicitly via `record()` when it has that information some other way,
never fabricated here.

Not persisted -- same "does not persist anything itself" rule every
other `learning/` module (besides `trade_event_bridge.py`'s own
disclosed exception) follows; a `database/regime_memory_repository.py`
would be a separate, future, explicitly-approvable step. `RegimeMemory`
lives only as long as the process holding it.

Per this whole phase's hard boundary: this module returns data only.
Nothing reads a `RegimeObservation` back into `strategies/`,
`decision/`, or `risk/` to change behavior.
"""

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, TYPE_CHECKING

from context_layer.trend.market_regime import MarketRegime

if TYPE_CHECKING:
    from context_layer.context_engine.context_orchestrator import ContextSnapshot

REGIME_TRENDING = "TRENDING"
REGIME_RANGE = "RANGE"
REGIME_HIGH_VOLATILITY = "HIGH_VOLATILITY"
REGIME_LOW_VOLATILITY = "LOW_VOLATILITY"
REGIME_NEWS_EVENT = "NEWS_EVENT"

KNOWN_REGIMES = (REGIME_TRENDING, REGIME_RANGE, REGIME_HIGH_VOLATILITY, REGIME_LOW_VOLATILITY, REGIME_NEWS_EVENT)

_MARKET_REGIME_TO_LABEL = {
    MarketRegime.TRENDING: REGIME_TRENDING,
    MarketRegime.RANGE: REGIME_RANGE,
    MarketRegime.HIGH_VOLATILITY: REGIME_HIGH_VOLATILITY,
    MarketRegime.LOW_VOLATILITY: REGIME_LOW_VOLATILITY,
}


@dataclass(frozen=True)
class RegimeObservation:
    """
    regime: one of `KNOWN_REGIMES` by convention -- not enforced as an
        enum, since `record()` accepts any string (same "free text, no
        fixed taxonomy yet" posture `ai.journal.failure_analysis.FailureAnalysisEntry.reason`
        already established, for a caller with a regime this module's
        own five categories don't name).
    session: optional, e.g. "LONDON"/"NY_NEWS" -- relayed, not
        recomputed.
    notes: optional free text.
    observed_at: when this observation was recorded.
    """
    regime: str
    observed_at: datetime
    session: Optional[str] = None
    notes: Optional[str] = None


class RegimeMemory:
    """In-memory observation log -- no database, no file, cleared when the process holding it ends."""

    def __init__(self):
        self._observations: List[RegimeObservation] = []

    def record(
        self,
        regime: str,
        session: Optional[str] = None,
        notes: Optional[str] = None,
        observed_at: Optional[datetime] = None,
    ) -> RegimeObservation:
        """Appends and returns one RegimeObservation. Never raises: any non-empty string is accepted as `regime`, not validated against KNOWN_REGIMES."""
        observation = RegimeObservation(
            regime=regime,
            observed_at=observed_at or datetime.now(timezone.utc),
            session=session,
            notes=notes,
        )
        self._observations.append(observation)
        return observation

    def all(self) -> List[RegimeObservation]:
        return list(self._observations)

    def count_by_regime(self) -> Dict[str, int]:
        return dict(Counter(observation.regime for observation in self._observations))

    def most_recent(self, limit: int = 5) -> List[RegimeObservation]:
        """Newest first."""
        return sorted(self._observations, key=lambda observation: observation.observed_at, reverse=True)[:limit]


def record_from_context(
    memory: RegimeMemory,
    context: 'ContextSnapshot',
    session: Optional[str] = None,
) -> Optional[RegimeObservation]:
    """
    Relays `context.market_regime.regime.value` directly for the four
    regimes this module's vocabulary covers
    (TRENDING/RANGE/HIGH_VOLATILITY/LOW_VOLATILITY). Returns `None`
    (records nothing) for `ACCUMULATION`/`DISTRIBUTION`/`UNKNOWN` --
    this module's own five-category vocabulary doesn't name them, and
    inventing a mapping would misclassify a real regime rather than
    honestly saying "not tracked here." Never raises.
    """
    label = _MARKET_REGIME_TO_LABEL.get(context.market_regime.regime)
    if label is None:
        return None
    return memory.record(label, session=session)


def format_regime_summary(memory: RegimeMemory) -> List[str]:
    """
    One `"<REGIME>: <N> observation(s)"` line per distinct regime seen,
    most-observed first -- the exact `Sequence[str]` shape
    `ai.learning_context.build_learning_context()`'s own `regimes=`
    parameter expects. Never raises: an empty memory produces an empty
    list.
    """
    counts = memory.count_by_regime()
    ordered = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [f"{regime}: {count} observation(s)" for regime, count in ordered]
