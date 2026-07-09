import sqlite3
from typing import List, Optional, Dict
from datetime import datetime, timezone
from database.database import Database
from core.logger import setup_logger

logger = setup_logger("SignalRepository")

class SignalRepository:
    """
    Handles CRUD operations for the 'signals' table.
    Uses Database context manager for connection safety.
    """
    def __init__(self):
        self.db = Database()

    def create_signal(self, data: Dict) -> str:
        """Inserts a new signal into the database."""
        query = """
        INSERT INTO signals (
            signal_id, symbol, direction, entry_zone_min, entry_zone_max, 
            stop_loss, take_profit_1, take_profit_2, risk_percent, 
            lot_size, strategy_name, confidence_score, ai_explanation, 
            status, result, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'OPEN', 'OPEN', ?)
        """
        created_at = datetime.now(timezone.utc).isoformat()
        params = (
            data['signal_id'], data['symbol'], data['direction'], 
            data['entry_zone_min'], data['entry_zone_max'], data['stop_loss'],
            data['take_profit_1'], data['take_profit_2'], data['risk_percent'],
            data['lot_size'], data['strategy_name'], data['confidence_score'],
            data['ai_explanation'], created_at
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
