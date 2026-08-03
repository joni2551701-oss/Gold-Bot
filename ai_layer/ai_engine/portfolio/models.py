"""
AI Layer — Portfolio Model (Phase 66.7: AI Portfolio Intelligence
Foundation, TASK 2).

`PortfolioRecord`/`PortfolioStatus`/`PortfolioRiskLevel`/
`PortfolioHealth` follow the same Article 3 resolution
`ai/trade_journal/models.py`, `ai/ai_layer/knowledge_ai/learning_loop/models.py`,
`ai/coaching/models.py`, `ai/performance/models.py`, and
`ai/strategy/models.py` all already established: every field is a
primitive (`str`/`int`) or an enum defined in this same file -- never
a `decision_layer.decision_engine.models.TradeDecision`, `risk_layer.risk_engine.risk_manager.RiskResult`, or
any other Trading Core object reference. `ai/portfolio/` never imports
`decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, `monitoring/`, `telegram/`, `database/`, `voice/`,
`assistant/`, `media/`, `broadcast/`, `academy/`, `research/`, `core.`,
or `ai_layer.knowledge_ai.memory_manager`.

**No naming collision** (documented, see `docs/PHASE66_7_AUDIT.md`'s
"Question 1"): a repository-wide search found no pre-existing
`Portfolio`-shaped model anywhere. `risk_layer/risk_engine/risk_manager.py`'s
`RiskResult`/`RiskManager` are the nearest conceptual neighbor by name
only -- a per-trade sizing contract, not a per-portfolio one, and
Trading Core (`risk/`) -- import forbidden outright by this phase's
own Rule 1, the same absolute-ban posture already established for
`strategies/` in Phase 66.6.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import uuid4


class PortfolioStatus(Enum):
    """TASK 2's own exact vocabulary -- caller-supplied, never inferred by this package."""

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ARCHIVED = "ARCHIVED"


class PortfolioRiskLevel(Enum):
    """TASK 2's own exact vocabulary -- a caller-supplied qualitative label, never computed by this package (Rule 5: CRUD only)."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PortfolioHealth(Enum):
    """TASK 2's own exact vocabulary -- a caller-supplied qualitative label, never graded by this package."""

    GOOD = "GOOD"
    WARNING = "WARNING"
    POOR = "POOR"


@dataclass(frozen=True)
class PortfolioRecord:
    """
    TASK 2's own exact field list: `portfolio_id`, `portfolio_name`,
    `status`, `risk_level`, `health`, `strategy_count`,
    `active_strategy_count`, `notes`, `created_at`.

    portfolio_id: this record's own generated identity
        (`generate_portfolio_id()`).
    portfolio_name: free-text display name -- caller-supplied, never
        inferred.
    status: `PortfolioStatus`, mutated only via `PortfolioRuntime.archive()`/
        `update()`. Defaults to `ACTIVE` -- a portfolio being tracked
        by this Foundation is, by definition, already in use (unlike
        `ai_layer.ai_engine.strategy.models.StrategyRecord.status`'s own `TESTING`
        default, which reflects a strategy not yet proven).
    risk_level: caller-supplied `PortfolioRiskLevel` -- this module
        never computes or grades a risk level itself (Rule 5); `None`
        until a caller explicitly supplies one.
    health: caller-supplied `PortfolioHealth` -- same posture as
        `risk_level`; this module never grades portfolio health.
    strategy_count/active_strategy_count: caller-supplied (or
        adapter-computed via deterministic counting, see
        `strategy_adapter.py`) counts -- this module never infers
        which strategies belong to a portfolio.
    notes: a short free-text note.
    created_at: ISO-8601 timestamp string, stamped by
        `PortfolioRuntime.create()`.
    """

    portfolio_id: str
    portfolio_name: str
    status: PortfolioStatus = PortfolioStatus.ACTIVE
    risk_level: Optional[PortfolioRiskLevel] = None
    health: Optional[PortfolioHealth] = None
    strategy_count: int = 0
    active_strategy_count: int = 0
    notes: Optional[str] = None
    created_at: str = ""


def generate_portfolio_id() -> str:
    """Same stateless uuid4 convention as every other generate_X_id() in this codebase (e.g. ai.strategy.models.generate_strategy_id())."""
    return str(uuid4())
