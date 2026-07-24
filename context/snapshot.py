"""
Context Layer — Context Snapshot Standard (Phase A16).

ContextSnapshotSchema is a standard, flat, JSON-serializable summary
of market context -- for a future AI provider, Analytics, Replay, or
Education consumer, not for the live pipeline. It does NOT detect
anything itself; every field is either a direct copy of an
already-computed value (from context.context_orchestrator.ContextSnapshot
and its detector modules) or an explicit None/False placeholder for
something no detector computes yet (premium_discount -- see
context/context_config.py's own "future detector" note). See
docs/CONTEXT_SNAPSHOT.md for the full contract and this module's
from_context_snapshot() for how the existing ContextSnapshot becomes
one.

NAMING NOTE -- read before using this module: context.context_orchestrator
already defines a class named ContextSnapshot -- the real, internal,
fully-detailed structure every detector/strategy/signal-quality/
explainability/feature-engineering module already consumes (12
fields: candles, structure, bos_events, ... market_regime). This
module's class is deliberately named ContextSnapshotSchema, not
ContextSnapshot, to avoid a same-name collision between two entirely
different types in the same top-level package -- mirroring
signals/schema.py's SignalSchema (Phase A15), which is similarly
named -Schema to distinguish it from signals/models.py's
SignalCandidate. context.context_orchestrator.ContextSnapshot is
untouched by this phase, and nothing about it changes.
"""

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from context.context_orchestrator import ContextSnapshot
from context.market_structure import most_recent_bias

# The real vocabulary context.market_regime.MarketRegime already
# defines (TRENDING/RANGE/ACCUMULATION/DISTRIBUTION/HIGH_VOLATILITY/
# LOW_VOLATILITY/UNKNOWN) -- reused as plain literals (like
# signals.schema.ALLOWED_DIRECTIONS reuses SignalType's values) rather
# than the roadmap's own illustrative 5-value list
# (TREND/RANGE/REVERSAL/VOLATILITY/UNKNOWN), which would require a
# lossy, invented mapping (e.g. deciding ACCUMULATION means
# "REVERSAL") -- seededocs/CONTEXT_SNAPSHOT.md's "A deliberate
# deviation" section.
ALLOWED_REGIMES = (
    "TRENDING", "RANGE", "ACCUMULATION", "DISTRIBUTION",
    "HIGH_VOLATILITY", "LOW_VOLATILITY", "UNKNOWN",
)


@dataclass(frozen=True)
class StructureInfo:
    """
    trend: "BULLISH"/"BEARISH"/None -- context.market_structure.most_recent_bias()'s
        exact return value, not a new calculation.
    bos: True if context.bos_events is non-empty -- presence only, not
        which direction or how many.
    choch: True if context.choch_events is non-empty -- same rationale.
    swing_state: the most recent StructurePoint's StructureType value
        (e.g. "HH", "HL", "LH", "LL") -- a single already-classified
        label, not a combined "last-high + last-low" pair (that would
        require a new backward-walk this phase doesn't add -- see
        docs/CONTEXT_SNAPSHOT.md).
    """
    trend: Optional[str] = None
    bos: bool = False
    choch: bool = False
    swing_state: Optional[str] = None


@dataclass(frozen=True)
class LiquidityInfo:
    """
    sweep_detected: True if context.liquidity_sweeps is non-empty.
    liquidity_type: the most recent sweep's LiquidityType.value (the
        real value, e.g. "SELL_SIDE_LIQUIDITY"/"BUY_SIDE_LIQUIDITY" --
        not the roadmap's shortened illustrative "SELL_SIDE" label).
        None if no sweep exists.
    """
    sweep_detected: bool = False
    liquidity_type: Optional[str] = None


@dataclass(frozen=True)
class ZonesInfo:
    """
    order_block: True if context.order_blocks is non-empty.
    fvg: True if context.fair_value_gaps is non-empty.
    premium_discount: always None -- no detector for this exists
        anywhere in this codebase today (context/context_config.py's
        own docstring names it as a future detector). Never fabricated.
    """
    order_block: bool = False
    fvg: bool = False
    premium_discount: Optional[str] = None


@dataclass(frozen=True)
class SessionInfo:
    """current_session: the latest SessionEvent's Session.value (e.g. "LONDON"). None if no session data."""
    current_session: Optional[str] = None


@dataclass(frozen=True)
class SnapshotMetadata:
    """
    source: "ContextEngine" -- the real logger name
        context/context_orchestrator.py already uses
        (setup_logger("ContextEngine")), not an invented label.
    engine_version: always None -- no versioning scheme exists for the
        context detection engine itself today. An honest hook.
    """
    source: str = "ContextEngine"
    engine_version: Optional[str] = None


@dataclass(frozen=True)
class ContextSnapshotSchema:
    """
    Identity: snapshot_id (generate_snapshot_id()), created_at (when
        this schema object was built), version (schema version,
        "1.0" today).
    Market: symbol/timeframe/timestamp -- all Optional: a snapshot
        built from an empty-candle context has no real timestamp to
        report, and validate_snapshot() is the one place that gets to
        say so is invalid, not the dataclass constructor (never
        raises at construction -- same posture as signals/schema.py).
    structure/liquidity/zones/session: nested, already-documented
        Info groups -- each defaults to its own all-empty instance.
    regime: one of ALLOWED_REGIMES, defaults "UNKNOWN".
    metadata: SnapshotMetadata.
    """
    snapshot_id: str
    created_at: datetime
    version: str = "1.0"
    symbol: Optional[str] = None
    timeframe: Optional[str] = None
    timestamp: Optional[datetime] = None
    structure: StructureInfo = field(default_factory=StructureInfo)
    liquidity: LiquidityInfo = field(default_factory=LiquidityInfo)
    zones: ZonesInfo = field(default_factory=ZonesInfo)
    session: SessionInfo = field(default_factory=SessionInfo)
    regime: str = "UNKNOWN"
    metadata: SnapshotMetadata = field(default_factory=SnapshotMetadata)

    def to_dict(self) -> dict:
        """JSON-safe nested dict -- created_at/timestamp rendered as ISO-8601 strings, everything else already a primitive."""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["timestamp"] = self.timestamp.isoformat() if self.timestamp is not None else None
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data: dict) -> 'ContextSnapshotSchema':
        """The exact inverse of to_dict() -- reconstructs nested Info groups and parses ISO-8601 strings back into datetime."""
        return ContextSnapshotSchema(
            snapshot_id=data["snapshot_id"],
            created_at=datetime.fromisoformat(data["created_at"]),
            version=data.get("version", "1.0"),
            symbol=data.get("symbol"),
            timeframe=data.get("timeframe"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
            structure=StructureInfo(**data.get("structure") or {}),
            liquidity=LiquidityInfo(**data.get("liquidity") or {}),
            zones=ZonesInfo(**data.get("zones") or {}),
            session=SessionInfo(**data.get("session") or {}),
            regime=data.get("regime", "UNKNOWN"),
            metadata=SnapshotMetadata(**data.get("metadata") or {}),
        )

    @staticmethod
    def from_json(payload: str) -> 'ContextSnapshotSchema':
        return ContextSnapshotSchema.from_dict(json.loads(payload))


def generate_snapshot_id() -> str:
    """Same generation convention as signals/schema.py's generate_signal_id() (str(uuid.uuid4())) -- not a new scheme."""
    return str(uuid.uuid4())


@dataclass(frozen=True)
class ValidationResult:
    """
    A separate, tiny definition from signals.schema.ValidationResult
    -- not imported from there. context/ must never depend on
    signals/ (see docs/ARCHITECTURE_RULES.md's Context Engine rule:
    context does not generate a signal, so it must not import from
    the signal layer either). Same two-field shape by convention, not
    by shared code.
    """
    valid: bool
    errors: List[str] = field(default_factory=list)


def validate_snapshot(snapshot: ContextSnapshotSchema) -> ValidationResult:
    """
    Never raises: an invalid ContextSnapshotSchema (missing symbol/
    timeframe/timestamp/version, or an unrecognized regime) produces
    ValidationResult(valid=False, errors=[...]), not an exception --
    the same fail-safe posture every other Phase A foundation module
    uses.
    """
    errors: List[str] = []

    if not snapshot.symbol:
        errors.append("symbol is required")
    if not snapshot.timeframe:
        errors.append("timeframe is required")
    if not snapshot.timestamp:
        errors.append("timestamp is required")
    if not snapshot.version:
        errors.append("version is required")

    if snapshot.regime and snapshot.regime not in ALLOWED_REGIMES:
        errors.append(f"regime must be one of {ALLOWED_REGIMES}, got {snapshot.regime!r}")

    return ValidationResult(valid=len(errors) == 0, errors=errors)


def from_context_snapshot(
    context: ContextSnapshot,
    *,
    symbol: str = "XAUUSD",
    timeframe: str = "M15",
    engine_version: Optional[str] = None,
) -> ContextSnapshotSchema:
    """
    Builds a ContextSnapshotSchema from an existing, already-computed
    context.context_orchestrator.ContextSnapshot -- the minimum
    required input. Every field below is either a direct read/presence
    check of an already-detected sequence or an honest None/False for
    something no detector computes (premium_discount). Never raises:
    an empty-candle ContextSnapshot produces a schema with
    symbol/timeframe filled in (the caller's own real values) but
    timestamp=None and every structure/liquidity/zones/session field
    at its default -- see validate_snapshot() for how that gets
    flagged, not this function.
    """
    trend = most_recent_bias(context.structure)
    swing_state = context.structure[-1].structure.value if context.structure else None

    liquidity_type = context.liquidity_sweeps[-1].type.value if context.liquidity_sweeps else None

    current_session = (
        context.session_events[-1].session.value if context.session_events else None
    )

    timestamp = context.candles[-1].timestamp if context.candles else None

    return ContextSnapshotSchema(
        snapshot_id=generate_snapshot_id(),
        created_at=datetime.now(timezone.utc),
        symbol=symbol,
        timeframe=timeframe,
        timestamp=timestamp,
        structure=StructureInfo(
            trend=trend,
            bos=bool(context.bos_events),
            choch=bool(context.choch_events),
            swing_state=swing_state,
        ),
        liquidity=LiquidityInfo(
            sweep_detected=bool(context.liquidity_sweeps),
            liquidity_type=liquidity_type,
        ),
        zones=ZonesInfo(
            order_block=bool(context.order_blocks),
            fvg=bool(context.fair_value_gaps),
            premium_discount=None,
        ),
        session=SessionInfo(current_session=current_session),
        regime=context.market_regime.regime.value,
        metadata=SnapshotMetadata(source="ContextEngine", engine_version=engine_version),
    )
