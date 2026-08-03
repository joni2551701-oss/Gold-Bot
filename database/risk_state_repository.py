"""
Database Layer — Risk Account State repository (Phase V1.0.1: Risk
Management Hardening Patch, TASK 4/5/10). Mirrors
database/runtime_feature_repository.py's own structure (upsert via
check-then-branch UPDATE/INSERT, idempotent schema init in __init__,
one row per key -- here `symbol` instead of `feature`).
"""

from typing import Optional
from datetime import datetime, timezone

from database.database import Database
from database.models import init_risk_schema
from database.risk_state_models import RiskAccountStateEntry
from core_layer.logger.logger import setup_logger

logger = setup_logger("RiskStateRepository")

_RISK_STATE_SELECT_COLUMNS = (
    "SELECT symbol, starting_equity, current_equity, drawdown_status, "
    "daily_start_balance, daily_date, created_at, updated_at"
)


def _row_to_entry(row) -> RiskAccountStateEntry:
    return RiskAccountStateEntry(
        symbol=row["symbol"],
        starting_equity=row["starting_equity"],
        current_equity=row["current_equity"],
        drawdown_status=row["drawdown_status"],
        daily_start_balance=row["daily_start_balance"],
        daily_date=row["daily_date"],
        created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
        updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
    )


class RiskStateRepository:
    """Handles CRUD operations for the 'risk_account_state' table. Database access only -- no drawdown/daily-loss calculation logic (that's risk/account_state_tracker.py's job, same phase)."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_risk_schema(conn)

    def get_state(self, symbol: str) -> Optional[RiskAccountStateEntry]:
        """Returns None when no persisted row exists yet for this symbol -- never raises for a lookup miss."""
        with self.db as conn:
            cursor = conn.execute(
                _RISK_STATE_SELECT_COLUMNS + " FROM risk_account_state WHERE symbol = ?", (symbol,)
            )
            row = cursor.fetchone()
            return _row_to_entry(row) if row else None

    def upsert_state(
        self,
        symbol: str,
        starting_equity: Optional[float] = None,
        current_equity: Optional[float] = None,
        drawdown_status: str = "NORMAL",
        daily_start_balance: Optional[float] = None,
        daily_date: Optional[str] = None,
    ) -> RiskAccountStateEntry:
        """
        Upserts the row for `symbol`: UPDATE if it already exists
        (`created_at` is never touched by an UPDATE), otherwise INSERT
        (stamps `created_at` for the first and only time). Re-reads
        and returns the row as actually written, same "canonical
        DB-truth" idiom as RuntimeFeatureRepository.set_feature().
        """
        now = datetime.now(timezone.utc).isoformat()
        with self.db as conn:
            cursor = conn.execute(
                "UPDATE risk_account_state SET starting_equity = ?, current_equity = ?, "
                "drawdown_status = ?, daily_start_balance = ?, daily_date = ?, updated_at = ? "
                "WHERE symbol = ?",
                (starting_equity, current_equity, drawdown_status, daily_start_balance, daily_date, now, symbol),
            )
            if cursor.rowcount == 0:
                conn.execute(
                    "INSERT INTO risk_account_state "
                    "(symbol, starting_equity, current_equity, drawdown_status, "
                    "daily_start_balance, daily_date, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (symbol, starting_equity, current_equity, drawdown_status,
                     daily_start_balance, daily_date, now, now),
                )
        return self.get_state(symbol)
