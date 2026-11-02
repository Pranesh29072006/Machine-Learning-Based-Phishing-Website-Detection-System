"""
Unit Tests for URL Defensive Validation.
"""

import unittest
from app.utils.validators import validate_url


class TestValidators(unittest.TestCase):
    """Test suite for URL input validation."""

    def test_valid_urls(self):
        valid_samples = [
            "https://www.google.com",
            "http://github.com/torvalds/linux",
            "https://sub.domain.co.uk/path?q=1&b=2",
            "http://192.168.1.1/admin",
            "http://localhost:5000"
        ]
        for url in valid_samples:
            is_valid, sanitized, err = validate_url(url)
            self.assertTrue(is_valid, f"Expected valid: {url}, got error: {err}")

    def test_invalid_urls(self):
        invalid_samples = [
            "",
            "   ",
            None,
            "ftp://files.example.com",
            "javascript:alert(1)",
            "data:text/html,malicious",
            "not_a_url",
            "https://" + "a" * 2050
        ]
        for url in invalid_samples:
            is_valid, sanitized, err = validate_url(url)
            self.assertFalse(is_valid, f"Expected invalid: {url}")


if __name__ == "__main__":
    unittest.main()

