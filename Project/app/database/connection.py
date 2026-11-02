"""
Database Connection & Schema Initialization Module
Handles SQLite connection pooling, WAL mode, pragmas, and schema creation.
"""

import os
import sqlite3
from pathlib import Path
from config import Config

DEFAULT_DB_PATH = Config.DATABASE_PATH
_active_db_path = os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH)


def set_db_path(path: str = None) -> None:
    """Set the active SQLite database path (useful for testing isolation)."""
    global _active_db_path
    _active_db_path = str(path) if path else DEFAULT_DB_PATH


def get_db_path() -> str:
    """Return the active SQLite database path."""
    return _active_db_path


def get_connection() -> sqlite3.Connection:
    """Create and return a database connection with row factory enabled and concurrency timeout."""
    conn = sqlite3.connect(_active_db_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the SQLite database schema with auto-indexing and WAL mode."""
    db_dir = os.path.dirname(_active_db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = get_connection()
    try:
        with conn:
            # Enable WAL mode for high-throughput concurrency and prevent database locking
            try:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA busy_timeout=5000;")
            except sqlite3.OperationalError:
                pass
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    prediction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    risk_level TEXT NOT NULL,
                    processing_time_ms REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_scans_created ON scans(created_at DESC);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_scans_url ON scans(url);")
    finally:
        conn.close()

