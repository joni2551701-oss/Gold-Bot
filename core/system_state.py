"""
Core Layer — System State Manager (Phase 59.6: Audit & Observability
Foundation, TASK 1).

SystemState is the top-level operating-mode vocabulary a future Owner
Mode / Emergency Layer (Phase 59.9, per the Director's own roadmap)
will read and write. This phase builds only the model -- the enum, an
immutable record of one state change, and a factory. Nothing in
core/pipeline.py, decision/, risk/, or execution/ reads this module;
constructing a SystemStateRecord changes no runtime behavior anywhere.
A future, separately-approved phase would add the actual holder/store
(in-memory singleton or persisted "current state" row) and wire
core/pipeline.py's stages to check it before running -- that wiring is
explicitly out of scope here, same "foundation, not full wiring"
posture as lifecycle/trade_state.py's own TradeState before
core/pipeline.py ever called into lifecycle/paper_trade_monitor.py.

Distinct from lifecycle.trade_state.TradeState (a single PaperTrade's
own CREATED/OPEN/CLOSED/CANCELLED lifecycle) and from
lifecycle.signal_lifecycle... no such collision exists, but the naming
follows the same discipline: SystemState is a new, never-before-used
name, describing the whole bot's operating mode, not one trade's or
one signal's state.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class SystemState(Enum):
    """
    RUNNING: normal operation -- the default, and the only state any
        of this codebase's real components run in today.
    VALIDATION: Phase 59 Real Market Validation Foundation's own
        observation-only posture (see config.Config.VALIDATION_MODE) --
        named here for the future Owner Mode to report against, not a
        new behavior.
    MAINTENANCE: reserved for a future Phase 59.9 Maintenance Mode
        (signal/execution paused, owner commands still available).
    PANIC: reserved for a future Phase 59.9 Emergency Kill Switch.
    READ_ONLY: reserved for a future state where owner commands can
        observe but not mutate anything (e.g. during a config rollback).
    """
    RUNNING = "RUNNING"
    VALIDATION = "VALIDATION"
    MAINTENANCE = "MAINTENANCE"
    PANIC = "PANIC"
    READ_ONLY = "READ_ONLY"


@dataclass(frozen=True)
class SystemStateRecord:
    """
    An immutable record of one state transition -- not a mutable
    "current state" holder (no such singleton exists in this phase;
    see module docstring). `changed_by`/`reason` are optional free
    text, same convention as
    ai.journal.failure_analysis.FailureAnalysisEntry's own
    reason/context fields -- no fixed taxonomy exists yet.
    """
    state: SystemState
    changed_at: datetime
    changed_by: Optional[str] = None
    reason: Optional[str] = None


def create_system_state_record(
    state: SystemState,
    changed_by: Optional[str] = None,
    reason: Optional[str] = None,
) -> SystemStateRecord:
    """Pure, deterministic factory -- stamps changed_at, same convention as every other create_X() factory in this codebase (e.g. analytics.signal_performance.generate_performance_id()'s caller)."""
    return SystemStateRecord(
        state=state,
        changed_at=datetime.now(timezone.utc),
        changed_by=changed_by,
        reason=reason,
    )
