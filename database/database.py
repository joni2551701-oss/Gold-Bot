import sqlite3
import os
from core.logger import setup_logger
from config import Config

logger = setup_logger("DatabaseManager")

class Database:
    """
    Handles SQLite connection lifecycle using centralized configuration.
    Designed with abstraction to facilitate future migration to PostgreSQL.
    """
    def __init__(self):
        self.db_path = Config.DB_PATH
        self.connection = None

    def _ensure_directory(self):
        """Ensures the database directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def init_db(self):
        """Placeholder for schema initialization in database/models.py."""
        self._ensure_directory()
        logger.info(f"Initializing database at {self.db_path}")

    def __enter__(self):
        """Context manager entry."""
        try:
            self._ensure_directory()
            self.connection = sqlite3.connect(self.db_path)
            # Row factory allows column access by name
            self.connection.row_factory = sqlite3.Row
            return self.connection
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit: ensures connection is closed."""
        if self.connection:
            if exc_type:
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
