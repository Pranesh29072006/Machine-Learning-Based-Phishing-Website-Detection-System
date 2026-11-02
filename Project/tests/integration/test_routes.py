"""
Integration Tests for Flask Blueprints and UI Routes.
"""

import unittest
from app import create_app
from config import TestingConfig


class TestRoutes(unittest.TestCase):
    """Test suite for HTTP page delivery and response codes."""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def test_page_routes(self):
        routes = [
            ("/", 200),
            ("/overview", 200),
            ("/dashboard", 200),
            ("/scanner", 200),
            ("/history", 200),
            ("/analytics", 200),
            ("/model-performance", 200),
            ("/security-insights", 200),
            ("/settings", 200),
            ("/about", 200),
            ("/nonexistent-route-for-404", 404)
        ]
        for path, code in routes:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, code, f"Route {path} failed: {resp.status_code}")

    def test_security_headers(self):
        resp = self.client.get("/")
        self.assertEqual(resp.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(resp.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertIn("1; mode=block", resp.headers.get("X-XSS-Protection", ""))


if __name__ == "__main__":
    unittest.main()

