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

FRED exists (data_layer/providers/fred_provider.py, Phase 59.2) but was
never connected to Context. This module is that connection point --
a pure, read-only adapter, same posture as context_layer/trend/market_phase.py's
own compute_market_phase(): computes a classification from
already-supplied data, generates no signal, makes no decision.
"Signal yaratmaydi. Faqat Context." (does not generate a signal, only
context) is this task's own explicit boundary.

Does NOT call FredProvider itself: FredProvider.get_interest_rate()/
get_inflation_data() always raise NotImplementedError today (Phase
59.2's own honest stub) -- this function takes already-fetched
FundamentalDataPoint values as input, the same "adapter over
already-computed data" pattern signal_layer/signal_builder/adapter.py and
context_layer/context_engine/snapshot.py already established. A future, real FredProvider
implementation is the one that would supply real values here; this
module does not change when that happens.

NAMING NOTE -- read before using this module: data_layer.providers.fundamental_base.FundamentalSnapshot
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

Phase 60.5 (Fundamental Intelligence Foundation, TASK 2) extends this
same FundamentalContextSnapshot with eight additional Optional fields
(dxy_bias/rates_bias/inflation_bias/fed_expectation/risk_sentiment/
gold_bias/confidence/macro_score) rather than creating a second,
competing model -- the Director's own brief lists these as a
"FundamentalSnapshot" shape, but that name is already taken at the
provider layer (see the naming note above), and TASK 1's reuse audit
found this module is the correct, already-existing Context-layer home
for them. All eight default to None and compute_fundamental_context()
does not set any of them -- same honest-hook posture dollar_strength/
risk_level already established; a real value only appears once a
caller merges in a context.fundamental_scoring.FundamentalScoreResult
via merge_fundamental_score() (this module, below), which
context.fundamental_scoring.py (TASK 5) produces.
"""

import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from data_layer.providers.fundamental_base import FundamentalDataPoint
    from context_layer.fundamental.fundamental_scoring import FundamentalScoreResult
    from context_layer.context_engine.context_orchestrator import ContextSnapshot


@dataclass(frozen=True)
class FundamentalContextSnapshot:
    """
    Identity: snapshot_id (generate_fundamental_snapshot_id()), created_at.
    fed_rate/inflation: the raw value off an already-supplied
        FundamentalDataPoint (FEDFUNDS/CPIAUCSL, see
        data_layer/providers/fred_provider.py) -- relayed directly, never
        recomputed. None if that indicator wasn't supplied.
    dollar_strength/risk_level: always None in this phase -- an
        honest hook, same "never fabricate" convention as
        context_layer/context_engine/snapshot.py's ZonesInfo.premium_discount. A real
        classification would need a historical baseline/threshold
        model this codebase has no real data to calibrate today
        (FredProvider has no live connection yet, Phase 59.2). Not
        invented here.
    dxy_bias/rates_bias/inflation_bias/fed_expectation/risk_sentiment
        (Phase 60.5, TASK 2): per-indicator biases FOR GOLD
        ("BULLISH"/"BEARISH"/"NEUTRAL"), each already classified by
        the caller (a future analyst/AI layer) -- this dataclass only
        carries them, it does not classify them (same "no threshold
        model exists" gap dollar_strength/risk_level already
        disclose). fed_expectation is informational only ("HAWKISH"/
        "DOVISH"/"NEUTRAL"), not part of the numeric score.
    gold_bias/confidence/macro_score (Phase 60.5, TASK 2): the
        aggregate output of context.fundamental_scoring.compute_fundamental_score()
        (TASK 5), carried here once merged via merge_fundamental_score()
        (below). All three None until a caller does that merge.
    """
    snapshot_id: str
    created_at: datetime
    fed_rate: Optional[float] = None
    inflation: Optional[float] = None
    dollar_strength: Optional[str] = None
    risk_level: Optional[str] = None
    dxy_bias: Optional[str] = None
    rates_bias: Optional[str] = None
    inflation_bias: Optional[str] = None
    fed_expectation: Optional[str] = None
    risk_sentiment: Optional[str] = None
    gold_bias: Optional[str] = None
    confidence: Optional[float] = None
    macro_score: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at.isoformat(),
            "fed_rate": self.fed_rate,
            "inflation": self.inflation,
            "dollar_strength": self.dollar_strength,
            "risk_level": self.risk_level,
            "dxy_bias": self.dxy_bias,
            "rates_bias": self.rates_bias,
            "inflation_bias": self.inflation_bias,
            "fed_expectation": self.fed_expectation,
            "risk_sentiment": self.risk_sentiment,
            "gold_bias": self.gold_bias,
            "confidence": self.confidence,
            "macro_score": self.macro_score,
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


def merge_fundamental_score(
    snapshot: FundamentalContextSnapshot, score: 'FundamentalScoreResult'
) -> FundamentalContextSnapshot:
    """
    Phase 60.5, TASK 2/5 glue: returns a new FundamentalContextSnapshot
    (this dataclass is frozen -- dataclasses.replace(), never mutation)
    with dxy_bias/rates_bias/inflation_bias/fed_expectation/
    risk_sentiment/gold_bias/confidence/macro_score filled in from an
    already-computed context.fundamental_scoring.FundamentalScoreResult
    (TASK 5). Every other field (snapshot_id, created_at, fed_rate,
    inflation, dollar_strength, risk_level) is carried over unchanged.
    Never raises.
    """
    return replace(
        snapshot,
        dxy_bias=score.dxy_bias,
        rates_bias=score.rates_bias,
        inflation_bias=score.inflation_bias,
        fed_expectation=score.fed_expectation,
        risk_sentiment=score.risk_sentiment,
        gold_bias=score.gold_bias,
        confidence=score.confidence,
        macro_score=score.macro_score,
    )


@dataclass(frozen=True)
class EnrichedContextSnapshot:
    """
    Phase 60.5, TASK 6 (Context Integration). Pairs an already-built
    context.context_orchestrator.ContextSnapshot with an already-built
    FundamentalContextSnapshot -- composition, not modification.

    ContextSnapshot's own docstring states its field set is a stable
    contract with "no defaults by design," so every caller supplies
    every field explicitly -- adding a fundamental field directly onto
    it would force every existing construction site (core/pipeline.py,
    backtesting/backtest_engine.py, and every test that builds one) to
    change, a real breaking change this task's own boundary ("Decision
    hali o'zgarmaydi", decision does not change) does not ask for and
    CLAUDE.md's "No breaking changes" restriction forbids without
    explicit approval. This wrapper achieves the same practical result
    -- one object carrying both technical and fundamental context --
    without touching ContextSnapshot at all.

    Not constructed anywhere in core/pipeline.py or any live path this
    phase -- a foundation type only, same posture as every other
    module in this phase.
    """
    context: 'ContextSnapshot'
    fundamental: FundamentalContextSnapshot


def attach_fundamental_context(
    context: 'ContextSnapshot', fundamental: FundamentalContextSnapshot
) -> EnrichedContextSnapshot:
    """Pure composition -- wraps both already-built snapshots, computes nothing, never raises."""
    return EnrichedContextSnapshot(context=context, fundamental=fundamental)
