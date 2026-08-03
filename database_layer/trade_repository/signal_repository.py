import sqlite3
from typing import List, Optional, Dict
from datetime import datetime, timezone
from database_layer.database_manager.database import Database
from database_layer.trade_repository.signal_record import SignalRecord
from core_layer.logger.logger import setup_logger

logger = setup_logger("SignalRepository")

class SignalRepository:
    """
    Handles CRUD operations for the 'signals' table.
    Uses Database context manager for connection safety.
    """
    def __init__(self):
        self.db = Database()
        # Idempotent (CREATE TABLE IF NOT EXISTS): safe to call on every
        # construction, never crashes if the schema already exists.
        self.db.init_db()

    def save_signal_record(self, record: SignalRecord) -> str:
        """
        Maps a SignalRecord (signal + decision + risk_result, wrapped
        with a signal_id) onto the existing 'signals' table row shape
        and persists it via create_signal(). The original schema is
        not redesigned: fields with no direct source on the wrapped
        objects (symbol, a second take-profit, risk_percent) are left
        empty rather than invented. strategy/timeframe/rr_ratio/
        ai_decision/risk_status/risk_amount/signal_status (Phase 39)
        are read straight off the record -- create_signal_record()
        already computed/collected them.
        """
        signal = record.signal
        decision = record.decision
        risk_result = record.risk_result

        data = {
            "signal_id": record.signal_id,
            "symbol": "",
            "direction": getattr(getattr(signal, "signal_type", None), "value", ""),
            "entry_zone_min": signal.entry,
            "entry_zone_max": signal.entry,
            "stop_loss": signal.stop_loss,
            "take_profit_1": signal.take_profit,
            "take_profit_2": 0.0,
            "risk_percent": 0.0,
            "lot_size": risk_result.lot_size,
            "strategy_name": signal.strategy_name,
            "confidence_score": decision.confidence,
            "ai_explanation": decision.ai_analysis.explanation,
            "strategy": record.strategy,
            "timeframe": record.timeframe,
            "rr_ratio": record.rr_ratio,
            "ai_decision": record.ai_decision,
            "risk_status": record.risk_status,
            "risk_amount": record.risk_amount,
            "signal_status": record.signal_status,
        }
        return self.create_signal(data)

    def create_signal(self, data: Dict) -> str:
        """
        Inserts a new signal into the database. The Phase 39 display
        columns (strategy, timeframe, rr_ratio, ai_decision,
        risk_status, risk_amount, signal_status) default when an
        old-style caller doesn't supply them, so this method's
        existing callers/contract are unaffected.
        """
        query = """
        INSERT INTO signals (
            signal_id, symbol, direction, entry_zone_min, entry_zone_max,
            stop_loss, take_profit_1, take_profit_2, risk_percent,
            lot_size, strategy_name, confidence_score, ai_explanation,
            status, result, created_at,
            strategy, timeframe, rr_ratio, ai_decision, risk_status,
            risk_amount, signal_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'OPEN', 'OPEN', ?, ?, ?, ?, ?, ?, ?, ?)
        """
        created_at = datetime.now(timezone.utc).isoformat()
        params = (
            data['signal_id'], data['symbol'], data['direction'],
            data['entry_zone_min'], data['entry_zone_max'], data['stop_loss'],
            data['take_profit_1'], data['take_profit_2'], data['risk_percent'],
            data['lot_size'], data['strategy_name'], data['confidence_score'],
            data['ai_explanation'], created_at,
            data.get('strategy', 'UNKNOWN'),
            data.get('timeframe', 'M15'),
            data.get('rr_ratio', 0.0),
            data.get('ai_decision', 'N/A'),
            data.get('risk_status', 'N/A'),
            data.get('risk_amount', 0.0),
            data.get('signal_status', 'NEW'),
        )

        with self.db as conn:
            try:
                conn.execute(query, params)
                return data['signal_id']
            except sqlite3.IntegrityError as e:
                logger.error(f"Failed to create signal {data.get('signal_id')}: {e}")
                raise

    def get_signal(self, signal_id: str) -> Optional[Dict]:
        """Retrieves a single signal by its ID."""
        with self.db as conn:
            cursor = conn.execute("SELECT * FROM signals WHERE signal_id = ?", (signal_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_open_signals(self) -> List[Dict]:
        """Retrieves all signals with status 'OPEN'."""
        with self.db as conn:
            cursor = conn.execute("SELECT * FROM signals WHERE status = 'OPEN'")
            return [dict(row) for row in cursor.fetchall()]

    def get_closed_signals(self) -> List[Dict]:
        """Retrieves all signals with status 'CLOSED'. Empty list if none."""
        with self.db as conn:
            cursor = conn.execute("SELECT * FROM signals WHERE status = 'CLOSED'")
            return [dict(row) for row in cursor.fetchall()]

    def count_signals_today(self) -> int:
        """Signals created today (UTC) -- same date('now') convention as UserRepository.count_users_created_today(). Used by platform_layer/telegram/owner/dashboard.py's /owner summary (Phase 61.5)."""
        with self.db as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM signals WHERE date(created_at) = date('now')")
            row = cursor.fetchone()
            return row["count"] if row else 0

    def get_closed_signals_today(self) -> List[Dict]:
        """Signals with status 'CLOSED' created today (UTC). Empty list if none. Used to compute today's win rate (Phase 61.5)."""
        with self.db as conn:
            cursor = conn.execute(
                "SELECT * FROM signals WHERE status = 'CLOSED' AND date(created_at) = date('now')"
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_signals_today(self) -> List[Dict]:
        """All signals created today (UTC), any status -- unlike count_signals_today() (a count) and get_closed_signals_today() (closed only), this returns the full rows so a caller can aggregate by direction/confidence. Used by core_layer/health_monitor/signal_monitor.py's get_signal_health() (GoldBot Core Owner Monitoring Alpha)."""
        with self.db as conn:
            cursor = conn.execute("SELECT * FROM signals WHERE date(created_at) = date('now')")
            return [dict(row) for row in cursor.fetchall()]

    def get_latest_signal(self) -> Optional[Dict]:
        """Most recently created signal, or None if the table is empty."""
        with self.db as conn:
            cursor = conn.execute(
                "SELECT * FROM signals ORDER BY created_at DESC, id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_recent_signals(self, limit: int = 5) -> List[Dict]:
        """Most recent `limit` signals, newest first. Empty list if none."""
        with self.db as conn:
            cursor = conn.execute(
                "SELECT * FROM signals ORDER BY created_at DESC, id DESC LIMIT ?", (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def update_signal_status(self, signal_id: str, status: str) -> bool:
        """Updates the status and updates closed_at if status is changed to CLOSED."""
        query = "UPDATE signals SET status = ?, closed_at = ? WHERE signal_id = ?"
        closed_at = datetime.now(timezone.utc).isoformat() if status == 'CLOSED' else None
        
        with self.db as conn:
            cursor = conn.execute(query, (status, closed_at, signal_id))
            return cursor.rowcount > 0

    def update_signal_result(self, signal_id: str, result: str) -> bool:
        """
        Finalizes a signal by setting the result, closing status, 
        and recording the completion timestamp.
        """
        ALLOWED_RESULTS = {"WIN", "LOSS", "BE", "CANCELLED"}
        
        if result not in ALLOWED_RESULTS:
            raise ValueError(f"Invalid result '{result}'. Must be one of {ALLOWED_RESULTS}")
        
        query = """
        UPDATE signals 
        SET result = ?, status = 'CLOSED', closed_at = ? 
        WHERE signal_id = ?
        """
        closed_at = datetime.now(timezone.utc).isoformat()
        
        with self.db as conn:
            cursor = conn.execute(query, (result, closed_at, signal_id))
            if cursor.rowcount > 0:
                logger.info(f"Signal {signal_id} closed with result: {result}")
                return True
            logger.warning(f"Attempted to update result for non-existent signal: {signal_id}")
            return False
