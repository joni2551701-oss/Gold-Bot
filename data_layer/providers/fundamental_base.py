"""
Data Layer — Fundamental Data Provider Interface (Phase 59.2, TASK 4).

FundamentalDataProvider is the abstract contract a macro/economic data
source (FRED today) implements -- distinct from MarketDataProvider
(base_provider.py), since a macro indicator (an interest rate, a CPI
reading) is not a candle: it has no open/high/low/close, and often
updates monthly or quarterly, not per-minute. Both share the same
DataProvider root (get_provider_name(), get_market_status()) so
registry.py/monitoring/provider_health.py (TASK 5/6) can hold both
kinds of provider uniformly -- see base_provider.py's own module
docstring for the full split rationale.

Architecture this feeds (per this task's own brief):

    FRED
     |
     v
    Fundamental Context
     |
     v
    AI Analyzer

Not built in this phase: no `Fundamental Context` consumer exists yet,
and `ai/ai_analyzer.py` (a heuristic stub, per every prior phase's own
audit) reads nothing from this module. This is upstream foundation
only, same "zero pipeline wiring" posture as every other Phase A/AC/
Phase-59 module.
"""

from abc import abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Dict, Optional

from data_layer.providers.base_provider import DataProvider


@dataclass(frozen=True)
class FundamentalDataPoint:
    """
    One macro/economic observation.
    series_id: the source's own identifier (e.g. FRED's "FEDFUNDS",
        "CPIAUCSL", "DTWEXBGS" -- see fred_provider.py for the exact
        series this foundation targets).
    value: the raw reported number -- never transformed/interpreted
        here (no "bullish for gold" style judgment; that belongs to a
        future Fundamental Context/AI layer, not this data-only
        provider).
    unit: a short label (e.g. "percent", "index"), as reported by the
        source -- never invented.
    as_of: the date/period this observation covers (FRED reports are
        often monthly/quarterly, not real-time).
    source: the provider name this point came from (matches
        get_provider_name()).
    """
    series_id: str
    value: float
    unit: str
    as_of: datetime
    source: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["as_of"] = self.as_of.isoformat()
        return data


@dataclass(frozen=True)
class FundamentalSnapshot:
    """
    A standard bundle of already-fetched FundamentalDataPoints, keyed
    by a short logical name (e.g. "dxy", "interest_rate", "cpi") --
    not by the source's own series_id, so a future consumer can read
    `snapshot.indicators["interest_rate"]` without knowing FRED's own
    naming convention. Mirrors context/snapshot.py's
    ContextSnapshotSchema identity/timestamp shape (snapshot_id,
    created_at) -- the same standardization pattern, not shared code
    (data_layer/providers/ must not import context/, see registry.py's own
    dependency notes).
    """
    snapshot_id: str
    created_at: datetime
    indicators: Dict[str, FundamentalDataPoint] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at.isoformat(),
            "indicators": {name: point.to_dict() for name, point in self.indicators.items()},
        }


class FundamentalDataProvider(DataProvider):
    """
    Abstract contract every macro/fundamental data provider
    implements. Like MarketDataProvider, this is data-only: never
    generates a signal, never knows about a strategy or a decision,
    never itself judges what a reading "means" for gold.
    """

    @abstractmethod
    def get_macro_indicator(self, series_id: str) -> Optional[FundamentalDataPoint]:
        """
        Returns the latest known observation for `series_id`, or None
        if unavailable -- never raises for a data-driven "no data"
        condition (same fail-safe posture as
        MarketDataProvider.get_latest_price()).
        """
        raise NotImplementedError

    @abstractmethod
    def get_interest_rate(self) -> Optional[FundamentalDataPoint]:
        """A convenience wrapper over get_macro_indicator() for the provider's own designated interest-rate series."""
        raise NotImplementedError

    @abstractmethod
    def get_inflation_data(self) -> Optional[FundamentalDataPoint]:
        """A convenience wrapper over get_macro_indicator() for the provider's own designated inflation series."""
        raise NotImplementedError
