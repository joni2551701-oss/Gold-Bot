"""
Database Layer — Monitoring repository (GoldBot Core Owner Monitoring
Alpha, TASK 9; extended by Phase B.0 -- `stage_durations_ms` persistence
and `record_process_start()`/`get_restart_count()`, see
`docs/PHASE_B0_AUDIT.md`). Mirrors `database_layer/trade_repository/emergency_repository.py`'s
own structure (append-only, no update/delete, idempotent schema init in
`__init__`) -- an error/decision/process-start history must never be
overwritten, same "Tarix yo'qolmasligi kerak" (history must never be
lost) posture.
"""

from datetime import datetime, timedelta, timezone
from typing import List

from database_layer.database_manager.database import Database
from database_layer.database_manager.models import init_monitoring_schema
from database_layer.audit_log.monitoring_models import (
    DecisionPipelineEntryRow,
    ErrorEventEntry,
    ProcessStartEntry,
    create_decision_pipeline_entry_row,
    create_error_event_entry,
    create_process_start_entry,
)
from core_layer.logger.logger import setup_logger

logger = setup_logger("MonitoringRepository")


def _row_to_error_event(row) -> ErrorEventEntry:
    return ErrorEventEntry(
        module=row["module"],
        error_type=row["error_type"],
        message=row["message"],
        severity=row["severity"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _serialize_stage_durations(stage_durations_ms) -> str:
    return ",".join(f"{stage}:{duration}" for stage, duration in stage_durations_ms)


def _deserialize_stage_durations(raw: str):
    if not raw:
        return ()
    pairs = []
    for entry in raw.split(","):
        if not entry:
            continue
        stage, _, duration = entry.rpartition(":")
        pairs.append((stage, float(duration)))
    return tuple(pairs)


def _row_to_decision_entry(row) -> DecisionPipelineEntryRow:
    criteria_met = tuple(c for c in row["criteria_met"].split(",") if c)
    stage_durations_raw = row["stage_durations_ms"] if "stage_durations_ms" in row.keys() else ""
    return DecisionPipelineEntryRow(
        symbol=row["symbol"],
        timeframe=row["timeframe"],
        criteria_met=criteria_met,
        criteria_total=row["criteria_total"],
        decision=row["decision"],
        reason=row["reason"] or "",
        stage_durations_ms=_deserialize_stage_durations(stage_durations_raw or ""),
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _row_to_process_start(row) -> ProcessStartEntry:
    return ProcessStartEntry(created_at=datetime.fromisoformat(row["created_at"]))


class MonitoringRepository:
    """Append-only persistence for ErrorEventEntry/DecisionPipelineEntryRow -- database access only, no aggregation/formatting logic (that belongs to core_layer/health_monitor/error_monitor.py and decision_layer/decision_logger/decision_logger.py, same phase)."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_monitoring_schema(conn)

    def record_error(self, module: str, error_type: str, message: str, severity: str) -> ErrorEventEntry:
        """Builds (via create_error_event_entry()) and inserts one new row -- never an UPDATE."""
        entry = create_error_event_entry(module, error_type, message, severity)
        with self.db as conn:
            conn.execute(
                "INSERT INTO monitoring_error_events (module, error_type, message, severity, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (entry.module, entry.error_type, entry.message, entry.severity, entry.created_at.isoformat()),
            )
        return entry

    def get_recent_errors(self, hours: int = 24, limit: int = 200) -> List[ErrorEventEntry]:
        """Errors recorded within the last `hours`, newest first. Never raises: an empty table returns an empty list."""
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        with self.db as conn:
            cursor = conn.execute(
                "SELECT module, error_type, message, severity, created_at FROM monitoring_error_events "
                "WHERE created_at >= ? ORDER BY id DESC LIMIT ?",
                (cutoff, limit),
            )
            return [_row_to_error_event(row) for row in cursor.fetchall()]

    def record_decision_entry(
        self, symbol: str, timeframe: str, criteria_met, criteria_total: int, decision: str, reason: str = "",
        stage_durations_ms=(),
    ) -> DecisionPipelineEntryRow:
        """Builds (via create_decision_pipeline_entry_row()) and inserts one new row -- never an UPDATE."""
        entry = create_decision_pipeline_entry_row(
            symbol, timeframe, criteria_met, criteria_total, decision, reason, stage_durations_ms,
        )
        with self.db as conn:
            conn.execute(
                "INSERT INTO monitoring_decision_pipeline "
                "(symbol, timeframe, criteria_met, criteria_total, decision, reason, stage_durations_ms, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    entry.symbol, entry.timeframe, ",".join(entry.criteria_met), entry.criteria_total,
                    entry.decision, entry.reason, _serialize_stage_durations(entry.stage_durations_ms),
                    entry.created_at.isoformat(),
                ),
            )
        return entry

    def get_recent_decision_entries(self, limit: int = 20) -> List[DecisionPipelineEntryRow]:
        """Most recent `limit` decision pipeline entries, newest first."""
        with self.db as conn:
            cursor = conn.execute(
                "SELECT symbol, timeframe, criteria_met, criteria_total, decision, reason, stage_durations_ms, created_at "
                "FROM monitoring_decision_pipeline ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            return [_row_to_decision_entry(row) for row in cursor.fetchall()]

    def record_process_start(self) -> ProcessStartEntry:
        """Phase B.0 TASK 2: builds (via create_process_start_entry()) and inserts one new row -- one call per process start, never an UPDATE."""
        entry = create_process_start_entry()
        with self.db as conn:
            conn.execute(
                "INSERT INTO monitoring_process_starts (created_at) VALUES (?)",
                (entry.created_at.isoformat(),),
            )
        return entry

    def get_restart_count(self) -> int:
        """Phase B.0 TASK 2: total number of recorded process starts. Never raises: relies on the same connection-context posture as every other read here."""
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) AS count FROM monitoring_process_starts")
            row = cursor.fetchone()
            return row["count"] if row else 0
