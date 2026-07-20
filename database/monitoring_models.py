"""
Database Layer — Monitoring persistence models (GoldBot Core Owner
Monitoring Alpha, TASK 9). Mirrors `database/emergency_models.py`'s own
shape/naming split: the DB-row model gets its own name distinct from
the domain model (`monitoring.models.ErrorEvent`/
`monitoring.models.DecisionPipelineEntry`), same "two names for two
layers" precedent as `database.emergency_models.EmergencyStateEntry`
vs `core.emergency.emergency_state.EmergencyStateRecord`.

Only these two tables are added -- `SystemHealth`/`MarketHealth`/
`SignalHealth` are computed live, never persisted (see
`docs/PHASE_CORE_MONITORING_AUDIT.md`'s TASK 9 conclusion).
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Sequence


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
    """Mirrors the 'monitoring_decision_pipeline' table row shape. `criteria_met` is stored as a comma-joined string (no fixed criteria vocabulary is enforced at the storage layer, same 'free text, no fixed taxonomy' posture `ai.trade_journal.models.TradeJournalEntry.mistakes` already uses for a similar Sequence[str] field)."""

    symbol: str
    timeframe: str
    criteria_met: Sequence[str]
    criteria_total: int
    decision: str
    reason: str = ""
    created_at: Optional[datetime] = None


def create_decision_pipeline_entry_row(
    symbol: str, timeframe: str, criteria_met: Sequence[str], criteria_total: int,
    decision: str, reason: str = "",
) -> DecisionPipelineEntryRow:
    """Pure, deterministic factory -- stamps created_at to 'now'."""
    return DecisionPipelineEntryRow(
        symbol=symbol, timeframe=timeframe, criteria_met=tuple(criteria_met),
        criteria_total=criteria_total, decision=decision, reason=reason,
        created_at=datetime.now(timezone.utc),
    )
