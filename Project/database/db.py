"""
Database helper module for Phishing Website Detection System.
Provides safe, parameterized SQLite operations for logging and retrieving scan history.
"""

import sqlite3
import os
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_history.db")
_active_db_path = os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH)


def set_db_path(path: str = None):
    """Set the active SQLite database path (useful for testing isolation)."""
    global _active_db_path
    _active_db_path = path if path else DEFAULT_DB_PATH


def get_db_path() -> str:
    """Return the active SQLite database path."""
    return _active_db_path


def get_connection():
    """Create and return a database connection with row factory enabled."""
    conn = sqlite3.connect(_active_db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the SQLite database schema."""
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    prediction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    risk_level TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_scans_created ON scans(created_at DESC);")
    finally:
        conn.close()


def save_scan(url: str, prediction: str, confidence: float, risk_level: str) -> int:
    """
    Save an analyzed URL scan record using parameterized SQL.
    Returns the newly inserted row ID.
    """
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO scans (url, prediction, confidence, risk_level, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (url, prediction, float(confidence), risk_level, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            return cursor.lastrowid
    finally:
        conn.close()


def get_recent_scans(limit: int = 10) -> list:
    """Retrieve the latest scans for dashboard summary."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT id, url, prediction, confidence, risk_level, created_at
            FROM scans
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_all_scans(search_query: str = None, limit: int = 200) -> list:
    """Retrieve all scans with optional search term filtering."""
    conn = get_connection()
    try:
        if search_query and search_query.strip():
            cursor = conn.execute(
                """
                SELECT id, url, prediction, confidence, risk_level, created_at
                FROM scans
                WHERE url LIKE ? OR prediction LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (f"%{search_query.strip()}%", f"%{search_query.strip()}%", limit)
            )
        else:
            cursor = conn.execute(
                """
                SELECT id, url, prediction, confidence, risk_level, created_at
                FROM scans
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_scan_by_id(scan_id: int):
    """Retrieve a single scan record by ID."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT id, url, prediction, confidence, risk_level, created_at
            FROM scans
            WHERE id = ?
            """,
            (scan_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_scan_stats() -> dict:
    """Compute aggregate counts for the dashboard statistics cards."""
    conn = get_connection()
    try:
        cursor = conn.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN prediction = 'Legitimate' THEN 1 ELSE 0 END) as legitimate,
                SUM(CASE WHEN prediction = 'Phishing' THEN 1 ELSE 0 END) as phishing
            FROM scans
        """)
        row = cursor.fetchone()
        total = row['total'] or 0
        legitimate = row['legitimate'] or 0
        phishing = row['phishing'] or 0
        
        return {
            "total": total,
            "legitimate": legitimate,
            "phishing": phishing,
            "phishing_percentage": round((phishing / total * 100), 1) if total > 0 else 0
        }
    finally:
        conn.close()


def clear_history():
    """Clear all records from scan history."""
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM scans;")
    finally:
        conn.close()


# Ensure database is initialized on import
init_db()

