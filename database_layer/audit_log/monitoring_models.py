"""
Database Layer — Monitoring persistence models (GoldBot Core Owner
Monitoring Alpha, TASK 9; extended by Phase B.0 -- `stage_durations_ms`
on `DecisionPipelineEntryRow`, and the new `ProcessStartEntry`, see
`docs/PHASE_B0_AUDIT.md`). Mirrors `database_layer/trade_repository/emergency_models.py`'s own
shape/naming split: the DB-row model gets its own name distinct from
the domain model (`core_layer.health_monitor.models.ErrorEvent`/
`core_layer.health_monitor.models.DecisionPipelineEntry`), same "two names for two
layers" precedent as `database_layer.trade_repository.emergency_models.EmergencyStateEntry`
vs `core_layer.emergency.emergency_state.EmergencyStateRecord`.

Three tables in total -- `SystemHealth`/`MarketHealth`/`SignalHealth`
are computed live, never persisted (see
`docs/PHASE_CORE_MONITORING_AUDIT.md`'s TASK 9 conclusion).
`ProcessStartEntry` is the one fact Phase B.0 adds that genuinely
cannot be computed live -- a restart count only exists across process
lifetimes.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence, Tuple


@dataclass(frozen=True)
class ErrorEventEntry:
    """Mirrors the 'monitoring_error_events' table row shape. `id` is intentionally excluded -- repository-internal detail, same convention as every other Phase 59.x/GoldBot Core Monitoring model."""

    module: str
    error_type: str
    message: str
    severity: str
    created_at: Optional[datetime] = None


def create_error_event_entry(module: str, error_type: str, message: str, severity: str) -> ErrorEventEntry:
    """Pure, deterministic factory -- stamps created_at to 'now'."""
    return ErrorEventEntry(
        module=module, error_type=error_type, message=message, severity=severity,
        created_at=datetime.now(timezone.utc),
    )


@dataclass(frozen=True)
class DecisionPipelineEntryRow:
    """Mirrors the 'monitoring_decision_pipeline' table row shape. `criteria_met` is stored as a comma-joined string (no fixed criteria vocabulary is enforced at the storage layer, same 'free text, no fixed taxonomy' posture `ai.trade_journal.models.TradeJournalEntry.mistakes` already uses for a similar Sequence[str] field). `stage_durations_ms` (Phase B.0) is stored the same way -- a comma-joined `stage:ms` string."""

    symbol: str
    timeframe: str
    criteria_met: Sequence[str]
    criteria_total: int
    decision: str
    reason: str = ""
    stage_durations_ms: Sequence[Tuple[str, float]] = ()
    created_at: Optional[datetime] = None


def create_decision_pipeline_entry_row(
    symbol: str, timeframe: str, criteria_met: Sequence[str], criteria_total: int,
    decision: str, reason: str = "", stage_durations_ms: Sequence[Tuple[str, float]] = (),
) -> DecisionPipelineEntryRow:
    """Pure, deterministic factory -- stamps created_at to 'now'."""
    return DecisionPipelineEntryRow(
        symbol=symbol, timeframe=timeframe, criteria_met=tuple(criteria_met),
        criteria_total=criteria_total, decision=decision, reason=reason,
        stage_durations_ms=tuple(stage_durations_ms),
        created_at=datetime.now(timezone.utc),
    )


@dataclass(frozen=True)
class ProcessStartEntry:
    """Mirrors the 'monitoring_process_starts' table row shape (Phase B.0 TASK 2) -- one append-only row per process start, the only way to count restarts across process lifetimes."""

    created_at: Optional[datetime] = None


def create_process_start_entry() -> ProcessStartEntry:
    """Pure, deterministic factory -- stamps created_at to 'now'."""
    return ProcessStartEntry(created_at=datetime.now(timezone.utc))
