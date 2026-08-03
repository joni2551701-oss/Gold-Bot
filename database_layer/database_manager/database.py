import sqlite3
import os
from core_layer.logger.logger import setup_logger
from config import Config
from database_layer.database_manager.models import init_schema

logger = setup_logger("DatabaseManager")

class Database:
    """
    Handles SQLite connection lifecycle and schema initialization.
    """
    def __init__(self):
        self.db_path = Config.DB_PATH
        self.connection = None

    def _ensure_directory(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def init_db(self):
        """Initializes the database directory and tables."""
        self._ensure_directory()
        with self as conn:
            init_schema(conn)

    def __enter__(self):
        try:
            self._ensure_directory()
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
