"""
Integration Tests for JSON API Endpoints.
"""

import json
import unittest
from app import create_app
from config import TestingConfig


class TestAPI(unittest.TestCase):
    """Test suite for JSON threat inspection endpoints."""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def test_api_analyze_success(self):
        payload = {"url": "https://www.google.com"}
        resp = self.client.post(
            "/api/analyze",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("prediction", data)
        self.assertIn("confidence", data)
        self.assertIn("processing_time_ms", data)

    def test_api_analyze_validation_error(self):
        payload = {"url": "javascript:alert(1)"}
        resp = self.client.post(
            "/api/analyze",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Disallowed URL scheme", data["error"])

    def test_api_stats_endpoint(self):
        resp = self.client.get("/api/stats")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("stats", data)

    def test_api_analytics_endpoint(self):
        resp = self.client.get("/api/analytics")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("analytics", data)


if __name__ == "__main__":
    unittest.main()

