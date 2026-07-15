"""
Database Layer — Learning Record repository (Phase 60.6: Learning
Loop Foundation, TASK 5). Mirrors `database/audit_log_repository.py`'s
own structure (CRUD-ish only, no business logic, idempotent schema
init in `__init__`) -- this repository also exposes no update/delete:
a learning record is append-only by design, per the Director's own
brief ("append only, tarix o'chirilmaydi, auditga mos").
"""

from typing import List, Optional
from datetime import datetime

from database.database import Database
from database.models import init_learning_schema
from database.learning_models import LearningRecordRow, create_learning_record_row
from core.logger import setup_logger

logger = setup_logger("LearningRepository")

_LEARNING_SELECT_COLUMNS = (
    "SELECT id, record_id, trade_id, signal_id, strategy_name, market_phase, "
    "session, timeframe, result, r_multiple, failure_type, success_pattern, created_at"
)


def _row_to_record(row) -> LearningRecordRow:
    return LearningRecordRow(
        id=row["id"],
        record_id=row["record_id"],
        trade_id=row["trade_id"],
        signal_id=row["signal_id"],
        strategy_name=row["strategy_name"],
        market_phase=row["market_phase"],
        session=row["session"],
        timeframe=row["timeframe"],
        result=row["result"],
        r_multiple=row["r_multiple"],
        failure_type=row["failure_type"],
        success_pattern=row["success_pattern"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


class LearningRepository:
    """Append-only persistence for LearningRecordRow -- database access only, no pattern-detection/analysis logic."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_learning_schema(conn)

    def record(
        self,
        record_id: str,
        trade_id: str,
        signal_id: str,
        strategy_name: Optional[str] = None,
        market_phase: Optional[str] = None,
        session: Optional[str] = None,
        timeframe: Optional[str] = None,
        result: Optional[str] = None,
        r_multiple: Optional[float] = None,
        failure_type: Optional[str] = None,
        success_pattern: Optional[str] = None,
    ) -> LearningRecordRow:
        """Builds (via create_learning_record_row()) and persists one row. Never raises for a normal insert -- record_id is caller-supplied and unique per learning.models.generate_learning_record_id(), no uniqueness collision expected."""
        entry = create_learning_record_row(
            record_id, trade_id, signal_id, strategy_name=strategy_name, market_phase=market_phase,
            session=session, timeframe=timeframe, result=result, r_multiple=r_multiple,
            failure_type=failure_type, success_pattern=success_pattern,
        )
        query = (
            "INSERT INTO learning_records (record_id, trade_id, signal_id, strategy_name, market_phase, "
            "session, timeframe, result, r_multiple, failure_type, success_pattern, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        params = (
            entry.record_id, entry.trade_id, entry.signal_id, entry.strategy_name, entry.market_phase,
            entry.session, entry.timeframe, entry.result, entry.r_multiple, entry.failure_type,
            entry.success_pattern, entry.created_at.isoformat(),
        )

        with self.db as conn:
            conn.execute(query, params)

        return entry

    def get_recent(self, limit: int = 100) -> List[LearningRecordRow]:
        """Most recent `limit` records, newest first -- matches TASK 6's own "Last 100 trades" report shape."""
        with self.db as conn:
            cursor = conn.execute(
                _LEARNING_SELECT_COLUMNS + " FROM learning_records ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            return [_row_to_record(row) for row in cursor.fetchall()]

    def get_by_strategy(self, strategy_name: str, limit: int = 100) -> List[LearningRecordRow]:
        """Every record for one strategy, newest first -- for a future "how has strategy X performed" view."""
        with self.db as conn:
            cursor = conn.execute(
                _LEARNING_SELECT_COLUMNS + " FROM learning_records WHERE strategy_name = ? ORDER BY created_at DESC LIMIT ?",
                (strategy_name, limit),
            )
            return [_row_to_record(row) for row in cursor.fetchall()]

    def count(self) -> int:
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM learning_records")
            row = cursor.fetchone()
            return row["count"] if row else 0
