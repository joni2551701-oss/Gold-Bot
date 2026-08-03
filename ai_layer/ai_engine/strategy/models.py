"""
AI Layer — Strategy Model (Phase 66.6: AI Strategy Intelligence
Foundation, TASK 2).

`StrategyRecord`/`StrategyType`/`StrategyStatus`/`StrategyConfidence`
follow the same Article 3 resolution `ai/trade_journal/models.py`,
`ai/ai_layer/knowledge_ai/learning_loop/models.py`, `ai/coaching/models.py`, and
`ai/performance/models.py` all already established: every field is a
primitive (`str`/`bool`) or an enum defined in this same file -- never
a `decision_layer.decision_engine.models.TradeDecision`, `risk_layer.risk_engine.risk_manager.RiskResult`, or
any other Trading Core object reference. `ai/strategy/` never imports
`decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, `monitoring/`, `telegram/`, `database/`, `voice/`,
`assistant/`, `media/`, `broadcast/`, `academy/`, `portfolio/`,
`research/`, `core.`, or `ai_layer.knowledge_ai.memory_manager`.

**Naming note** (documented, not a defect -- see
`docs/PHASE66_6_AUDIT.md`'s "Question 1" section): a *different*,
Trading-Core `StrategyStatus` enum already exists at
`strategy_layer.strategy_manager.lifecycle.strategy_status.StrategyStatus`
(`TESTING`/`ACTIVE`/`DISABLED`/`DEPRECATED`) alongside its own
`StrategyDefinition`/`StrategyRegistry`. Unlike every prior `66.x`
naming collision (where reuse was merely a field-shape mismatch), this
one is architecturally forbidden outright -- this brief's own Rule 1
bans `ai/` from importing `strategies/` at all, so this module's
`StrategyStatus` (`ACTIVE`/`TESTING`/`DISABLED`/`ARCHIVED`, a
different value set) is a distinct, non-colliding fully-qualified path,
never imported alongside the Trading Core one.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import uuid4


class StrategyType(Enum):
    """TASK 2's own exact vocabulary -- caller-supplied, never inferred by this package."""

    LIQUIDITY_SWEEP = "LIQUIDITY_SWEEP"
    FVG = "FVG"
    AMD = "AMD"
    TREND_BREAKOUT = "TREND_BREAKOUT"
    ORDER_BLOCK = "ORDER_BLOCK"
    WYCKOFF = "WYCKOFF"
    SMC = "SMC"
    CUSTOM = "CUSTOM"


class StrategyStatus(Enum):
    """
    TASK 2's own exact vocabulary. Metadata only -- this package never
    controls whether any real strategy in `strategies/*.py` runs; see
    the module docstring's "Naming note" for why this is a distinct
    enum from `strategy_layer.strategy_manager.lifecycle.strategy_status.StrategyStatus`.
    """

    ACTIVE = "ACTIVE"
    TESTING = "TESTING"
    DISABLED = "DISABLED"
    ARCHIVED = "ARCHIVED"


class StrategyConfidence(Enum):
    """TASK 2's own exact vocabulary -- a caller-supplied qualitative label, distinct from `StrategyRecord.confidence`'s own free-form numeric-or-text field."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass(frozen=True)
class StrategyRecord:
    """
    TASK 2's own exact field list: `strategy_id`, `strategy_name`,
    `strategy_type`, `strategy_version`, `confidence`, `notes`,
    `status`, `created_at`.

    strategy_id: this record's own generated identity
        (`generate_strategy_id()`).
    strategy_name: free-text display name (e.g. "Liquidity Sweep") --
        caller-supplied, never inferred.
    strategy_type: `StrategyType` -- caller-supplied classification.
    strategy_version: a plain string (e.g. "v1", "v2") -- no versioning
        history is computed here (Director Note 1 for a future,
        separately-briefed phase); this field only relays whatever the
        caller supplies.
    confidence: caller-supplied free-text confidence label (e.g. a
        `StrategyConfidence` value's own `.value` string, or any other
        caller-chosen text) -- this module never computes or grades a
        confidence score itself (Rule 5: CRUD only).
    notes: a short free-text note.
    status: `StrategyStatus`, mutated only via `StrategyRuntime.archive()`/
        `update()`.
    created_at: ISO-8601 timestamp string, stamped by
        `StrategyRuntime.create()`.
    """

    strategy_id: str
    strategy_name: str
    strategy_type: StrategyType
    strategy_version: Optional[str] = None
    confidence: Optional[str] = None
    notes: Optional[str] = None
    status: StrategyStatus = StrategyStatus.TESTING
    created_at: str = ""


def generate_strategy_id() -> str:
    """Same stateless uuid4 convention as every other generate_X_id() in this codebase (e.g. ai.performance.models.generate_performance_id())."""
    return str(uuid4())
