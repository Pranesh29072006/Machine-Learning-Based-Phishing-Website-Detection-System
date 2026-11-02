"""
End-to-End Workflow Simulation Test.
"""

import unittest
from app import create_app
from config import TestingConfig


class TestE2EWorkflow(unittest.TestCase):
    """Simulates full user lifecycle across all major application features."""

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def test_complete_user_lifecycle(self):
        # 1. Access Dashboard
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

        # 2. Navigate to Scanner Console
        resp = self.client.get("/scanner")
        self.assertEqual(resp.status_code, 200)

        # 3. Submit Scan Request
        resp = self.client.post("/analyze", data={"url": "https://www.wikipedia.org"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Scan Report", resp.text)
        self.assertIn("17 Vectors Analyzed", resp.text)

        # 4. View Scan History
        resp = self.client.get("/history")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("wikipedia.org", resp.text)

        # 5. Export CSV
        resp = self.client.get("/history/export")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, "text/csv; charset=utf-8")
        self.assertIn("Scan ID", resp.text)

        # 6. Check Threat Analytics
        resp = self.client.get("/analytics")
        self.assertEqual(resp.status_code, 200)

        # 7. Check Model Benchmarks
        resp = self.client.get("/model-performance")
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()

