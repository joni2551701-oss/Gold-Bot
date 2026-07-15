"""
Context Layer — Fundamental Context (Phase 59.3, TASK 6: Fundamental
Context Contract).

Architecture this closes, per this task's own brief:

    FRED
     |
     v
    Fundamental Context   <- this module
     |
     v
    AI Analyzer

FRED exists (data/providers/fred_provider.py, Phase 59.2) but was
never connected to Context. This module is that connection point --
a pure, read-only adapter, same posture as context/market_phase.py's
own compute_market_phase(): computes a classification from
already-supplied data, generates no signal, makes no decision.
"Signal yaratmaydi. Faqat Context." (does not generate a signal, only
context) is this task's own explicit boundary.

Does NOT call FredProvider itself: FredProvider.get_interest_rate()/
get_inflation_data() always raise NotImplementedError today (Phase
59.2's own honest stub) -- this function takes already-fetched
FundamentalDataPoint values as input, the same "adapter over
already-computed data" pattern signals/adapter.py and
context/snapshot.py already established. A future, real FredProvider
implementation is the one that would supply real values here; this
module does not change when that happens.

NAMING NOTE -- read before using this module: data.providers.fundamental_base.FundamentalSnapshot
(Phase 59.2) already exists -- a generic Dict[str, FundamentalDataPoint]
bundle, keyed by logical name, at the provider layer. This module's
own FundamentalContextSnapshot is a DIFFERENT, Context-layer-shaped
type (fixed fields: fed_rate, inflation, dollar_strength, risk_level --
exactly this task's own brief), not a rename or a duplicate --
deliberately not named FundamentalSnapshot to avoid a same-name
collision between two different types, the same disambiguation
discipline ContextSnapshotSchema (vs. ContextSnapshot) and
SignalLifecycleState (vs. execution.signal_lifecycle.SignalState)
already established.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from data.providers.fundamental_base import FundamentalDataPoint


@dataclass(frozen=True)
class FundamentalContextSnapshot:
    """
    Identity: snapshot_id (generate_fundamental_snapshot_id()), created_at.
    fed_rate/inflation: the raw value off an already-supplied
        FundamentalDataPoint (FEDFUNDS/CPIAUCSL, see
        data/providers/fred_provider.py) -- relayed directly, never
        recomputed. None if that indicator wasn't supplied.
    dollar_strength/risk_level: always None in this phase -- an
        honest hook, same "never fabricate" convention as
        context/snapshot.py's ZonesInfo.premium_discount. A real
        classification would need a historical baseline/threshold
        model this codebase has no real data to calibrate today
        (FredProvider has no live connection yet, Phase 59.2). Not
        invented here.
    """
    snapshot_id: str
    created_at: datetime
    fed_rate: Optional[float] = None
    inflation: Optional[float] = None
    dollar_strength: Optional[str] = None
    risk_level: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at.isoformat(),
            "fed_rate": self.fed_rate,
            "inflation": self.inflation,
            "dollar_strength": self.dollar_strength,
            "risk_level": self.risk_level,
        }


def generate_fundamental_snapshot_id() -> str:
    """Same generation convention as every other Phase A/AC/Phase-59 identity field (str(uuid.uuid4())) -- not a new scheme."""
    return str(uuid.uuid4())


def compute_fundamental_context(
    interest_rate: Optional['FundamentalDataPoint'] = None,
    inflation: Optional['FundamentalDataPoint'] = None,
) -> FundamentalContextSnapshot:
    """
    Builds a FundamentalContextSnapshot from already-fetched
    FundamentalDataPoints. Never raises: missing inputs (the common
    case today, since FredProvider is still a stub) produce a snapshot
    with fed_rate/inflation/dollar_strength/risk_level all None, not
    an exception -- the same fail-safe posture every other foundation
    module in this codebase uses.
    """
    return FundamentalContextSnapshot(
        snapshot_id=generate_fundamental_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        fed_rate=interest_rate.value if interest_rate is not None else None,
        inflation=inflation.value if inflation is not None else None,
        dollar_strength=None,
        risk_level=None,
    )
