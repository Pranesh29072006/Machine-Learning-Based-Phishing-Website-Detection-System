"""
Unit Tests for 17-Dimensional Feature Extraction Engine.
"""

import unittest
import numpy as np

from app.ml.feature_extraction import (
    extract_features,
    get_feature_dict,
    get_feature_details,
    is_ip,
    FEATURE_NAMES
)


class TestFeatureExtraction(unittest.TestCase):
    """Test suite for URL feature extraction."""

    def test_feature_vector_dimension(self):
        """Verify vector shape is exactly (17,) and matches FEATURE_NAMES."""
        features = extract_features("https://www.example.com")
        self.assertIsInstance(features, np.ndarray)
        self.assertEqual(features.shape, (17,))
        self.assertEqual(len(FEATURE_NAMES), 17)

    def test_ip_detection(self):
        """Test IPv4 and IPv6 detection."""
        self.assertEqual(is_ip("192.168.1.1"), 1)
        self.assertEqual(is_ip("10.0.0.1:8080"), 1)
        self.assertEqual(is_ip("[2001:db8::1]"), 1)
        self.assertEqual(is_ip("google.com"), 0)

    def test_https_feature(self):
        """Test is_https feature identification."""
        vec_https = extract_features("https://secure.bank.com")
        idx = FEATURE_NAMES.index("is_https")
        self.assertEqual(vec_https[idx], 1.0)

        vec_http = extract_features("http://insecure.bank.com")
        self.assertEqual(vec_http[idx], 0.0)

    def test_feature_details_count(self):
        """Verify get_feature_details returns 17 diagnostic items."""
        details = get_feature_details("https://www.google.com")
        self.assertEqual(len(details), 17)
        for item in details:
            self.assertIn("name", item)
            self.assertIn("value", item)
            self.assertIn("status", item)
            self.assertIn("description", item)


if __name__ == "__main__":
    unittest.main()

