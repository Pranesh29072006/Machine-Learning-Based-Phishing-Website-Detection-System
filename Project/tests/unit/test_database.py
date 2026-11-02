"""
Unit Tests for Database Operations (Isolated Test Environment).
"""

import os
import unittest
import tempfile

from app.database import (
    set_db_path,
    init_db,
    save_scan,
    get_scan_by_id,
    get_scan_stats,
    clear_history
)


class TestDatabaseOperations(unittest.TestCase):
    """Test suite for SQLite operations in isolated database file."""

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        set_db_path(self.temp_db.name)
        init_db()

    def tearDown(self):
        set_db_path(None)
        if os.path.exists(self.temp_db.name):
            try:
                os.remove(self.temp_db.name)
            except OSError:
                pass

    def test_save_and_retrieve_scan(self):
        scan_id = save_scan(
            url="https://unit-test.com",
            prediction="Legitimate",
            confidence=95.5,
            risk_level="Low Risk",
            processing_time_ms=25.0
        )
        self.assertGreater(scan_id, 0)

        record = get_scan_by_id(scan_id)
        self.assertIsNotNone(record)
        self.assertEqual(record["url"], "https://unit-test.com")
        self.assertEqual(record["prediction"], "Legitimate")
        self.assertEqual(record["confidence"], 95.5)

    def test_stats_computation(self):
        save_scan("https://safe.com", "Legitimate", 95.0, "Low Risk", 10.0)
        save_scan("https://phish.com", "Phishing", 90.0, "High Risk", 12.0)

        stats = get_scan_stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["legitimate"], 1)
        self.assertEqual(stats["phishing"], 1)
        self.assertEqual(stats["detection_rate"], 50.0)

    def test_clear_history(self):
        save_scan("https://test.com", "Legitimate", 90.0, "Low Risk", 5.0)
        clear_history()
        stats = get_scan_stats()
        self.assertEqual(stats["total"], 0)


if __name__ == "__main__":
    unittest.main()

