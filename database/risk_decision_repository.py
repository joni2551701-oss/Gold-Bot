"""
Database Layer — Risk Decision repository (Phase V1.0.1: Risk
Management Hardening Patch, TASK 8). Mirrors
database/emergency_repository.py's own structure (append-only, no
update/delete, idempotent schema init in __init__).
"""

from typing import List, Optional
from datetime import datetime, timezone, timedelta

from database.database import Database
from database.models import init_risk_schema
from database.risk_decision_models import RiskDecisionEntry, create_risk_decision_entry
from core_layer.logger.logger import setup_logger

logger = setup_logger("RiskDecisionRepository")

_RISK_DECISION_SELECT_COLUMNS = (
    "SELECT symbol, strategy_name, direction, risk_percent, risk_reward, drawdown_percent, "
    "decision, reason, reject_category, created_at"
)


def _row_to_entry(row) -> RiskDecisionEntry:
    return RiskDecisionEntry(
        symbol=row["symbol"],
        strategy_name=row["strategy_name"],
        direction=row["direction"],
        risk_percent=row["risk_percent"],
        risk_reward=row["risk_reward"],
        drawdown_percent=row["drawdown_percent"],
        decision=row["decision"],
        reason=row["reason"],
        reject_category=row["reject_category"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


class RiskDecisionRepository:
    """Append-only persistence for RiskDecisionEntry -- database access only, no risk-calculation logic (that's risk_layer/risk_engine/risk_manager.py's job, same phase)."""

    def __init__(self):
        self.db = Database()
        with self.db as conn:
            init_risk_schema(conn)

    def record(
        self,
        symbol: str,
        decision: str,
        reason: str,
        strategy_name: Optional[str] = None,
        direction: Optional[str] = None,
        risk_percent: Optional[float] = None,
        risk_reward: Optional[float] = None,
        drawdown_percent: Optional[float] = None,
        reject_category: Optional[str] = None,
    ) -> RiskDecisionEntry:
        """Builds (via create_risk_decision_entry()) and inserts one new row -- never an UPDATE, every RiskManager.evaluate() call is a genuinely new history entry."""
        entry = create_risk_decision_entry(
            symbol=symbol, decision=decision, reason=reason, strategy_name=strategy_name,
            direction=direction, risk_percent=risk_percent, risk_reward=risk_reward,
            drawdown_percent=drawdown_percent, reject_category=reject_category,
        )
        query = (
            "INSERT INTO risk_decisions "
            "(symbol, strategy_name, direction, risk_percent, risk_reward, drawdown_percent, "
            "decision, reason, reject_category, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        params = (
            entry.symbol, entry.strategy_name, entry.direction, entry.risk_percent,
            entry.risk_reward, entry.drawdown_percent, entry.decision, entry.reason,
            entry.reject_category, entry.created_at.isoformat(),
        )
        with self.db as conn:
            conn.execute(query, params)
        return entry

    def get_recent(self, limit: int = 50) -> List[RiskDecisionEntry]:
        """Most recent `limit` risk decisions, newest first."""
        with self.db as conn:
            cursor = conn.execute(
                _RISK_DECISION_SELECT_COLUMNS + " FROM risk_decisions ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            return [_row_to_entry(row) for row in cursor.fetchall()]

    def get_recent_approved(
        self,
        symbol: str,
        direction: str,
        strategy_name: Optional[str],
        within_seconds: float,
    ) -> List[RiskDecisionEntry]:
        """
        APPROVE decisions for this exact (symbol, direction,
        strategy_name) within the last `within_seconds` -- the lookup
        risk.duplicate_checker.DuplicateTradeChecker uses (TASK 6).
        strategy_name=None matches any strategy_name for this
        symbol/direction pair (a looser check for callers that don't
        know the strategy).
        """
        since = (datetime.now(timezone.utc) - timedelta(seconds=within_seconds)).isoformat()
        with self.db as conn:
            if strategy_name is None:
                cursor = conn.execute(
                    _RISK_DECISION_SELECT_COLUMNS + " FROM risk_decisions "
                    "WHERE symbol = ? AND direction = ? AND decision = 'APPROVE' AND created_at >= ? "
                    "ORDER BY id DESC",
                    (symbol, direction, since),
                )
            else:
                cursor = conn.execute(
                    _RISK_DECISION_SELECT_COLUMNS + " FROM risk_decisions "
                    "WHERE symbol = ? AND direction = ? AND strategy_name = ? "
                    "AND decision = 'APPROVE' AND created_at >= ? "
                    "ORDER BY id DESC",
                    (symbol, direction, strategy_name, since),
                )
            return [_row_to_entry(row) for row in cursor.fetchall()]

    def count_all(self) -> int:
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) AS count FROM risk_decisions")
            return cursor.fetchone()["count"]

    def count_by_decision(self, decision: str) -> int:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) AS count FROM risk_decisions WHERE decision = ?", (decision,)
            )
            return cursor.fetchone()["count"]

    def count_by_reject_category(self, reject_category: str) -> int:
        with self.db as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) AS count FROM risk_decisions WHERE reject_category = ?",
                (reject_category,),
            )
            return cursor.fetchone()["count"]
