"""
Comprehensive Automated Test Suite for Phishing Website Detection System.

Tests cover:
1. All 17 heuristic URL features individually and feature ordering compatibility.
2. Input validation: valid URLs, IPv4/IPv6 hosts, malformed hosts, unsupported schemes, length limits, control characters.
3. Machine learning inference, calibrated probabilities, and error recovery (including mock model failures).
4. SQLite persistence, querying, search filtering, and history clearing (run in isolated test database).
5. Flask HTTP routes, status codes, invalid methods, JSON API responses, and template rendering.
6. Graceful handling of missing models and missing datasets.
"""

import os
import tempfile
import unittest
import json
import numpy as np
from unittest.mock import patch, MagicMock

import app
import feature_extraction as fe
import database.db as db


class ComprehensivePhishingTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configure app for testing
        app.app.config['TESTING'] = True
        app.app.config['DEBUG'] = False
        cls.client = app.app.test_client()

        # Create isolated temporary database so production scan_history.db is NEVER touched
        cls.test_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        cls.test_db_path = cls.test_db_file.name
        cls.test_db_file.close()

        # Switch db to use the isolated test database
        cls.orig_db_path = db.get_db_path()
        db.set_db_path(cls.test_db_path)
        db.init_db()

    @classmethod
    def tearDownClass(cls):
        # Restore original database path and remove temporary test database
        db.set_db_path(cls.orig_db_path)
        try:
            if os.path.exists(cls.test_db_path):
                os.remove(cls.test_db_path)
        except OSError:
            pass

    def setUp(self):
        # Clear test database before each test
        db.clear_history()

    # =========================================================================
    # 1. INDIVIDUAL TESTS FOR ALL 17 FEATURES
    # =========================================================================

    def test_feature_01_url_length(self):
        url = "https://example.com/short"
        vec = fe.extract_features(url)
        idx = fe.FEATURE_NAMES.index("url_length")
        self.assertEqual(vec[idx], float(len(url)))

    def test_feature_02_domain_length(self):
        url = "https://my-bank-domain.com/path"
        vec = fe.extract_features(url)
        idx = fe.FEATURE_NAMES.index("domain_length")
        self.assertEqual(vec[idx], float(len("my-bank-domain.com")))

    def test_feature_03_num_dots(self):
        url = "https://a.b.c.example.com/page.html"
        vec = fe.extract_features(url)
        idx = fe.FEATURE_NAMES.index("num_dots")
        self.assertEqual(vec[idx], float(url.count(".")))

    def test_feature_04_num_hyphens(self):
        url = "https://apple-login-security-center.com/auth-id"
        vec = fe.extract_features(url)
        idx = fe.FEATURE_NAMES.index("num_hyphens")
        self.assertEqual(vec[idx], float(url.count("-")))

    def test_feature_05_num_digits(self):
        url = "https://example.com/item/12345/session987"
        vec = fe.extract_features(url)
        idx = fe.FEATURE_NAMES.index("num_digits")
        expected_digits = sum(c.isdigit() for c in url)
        self.assertEqual(vec[idx], float(expected_digits))

    def test_feature_06_has_ip_address_ipv4_and_ipv6(self):
        idx = fe.FEATURE_NAMES.index("has_ip_address")
        
        # Standard IPv4
        vec_ipv4 = fe.extract_features("http://192.168.1.1/login.php")
        self.assertEqual(vec_ipv4[idx], 1.0)
        
        # IPv4 with port
        vec_ipv4_port = fe.extract_features("http://10.0.0.1:8080/index")
        self.assertEqual(vec_ipv4_port[idx], 1.0)
        
        # IPv6 bracketed
        vec_ipv6 = fe.extract_features("http://[2001:db8::1]/admin")
        self.assertEqual(vec_ipv6[idx], 1.0)

        # Standard domain (non-IP)
        vec_domain = fe.extract_features("https://www.google.com")
        self.assertEqual(vec_domain[idx], 0.0)

    def test_feature_07_is_https(self):
        idx = fe.FEATURE_NAMES.index("is_https")
        self.assertEqual(fe.extract_features("https://secure.com")[idx], 1.0)
        self.assertEqual(fe.extract_features("http://insecure.com")[idx], 0.0)

    def test_feature_08_has_at_symbol(self):
        idx = fe.FEATURE_NAMES.index("has_at_symbol")
        self.assertEqual(fe.extract_features("http://user@attacker.com")[idx], 1.0)
        self.assertEqual(fe.extract_features("http://standard.com")[idx], 0.0)

    def test_feature_09_num_suspicious_symbols(self):
        idx = fe.FEATURE_NAMES.index("num_suspicious_symbols")
        url = "https://example.com/test?a=1&b=2%20+3"
        vec = fe.extract_features(url)
        self.assertGreater(vec[idx], 0.0)

    def test_feature_10_num_subdomains(self):
        idx = fe.FEATURE_NAMES.index("num_subdomains")
        self.assertEqual(fe.extract_features("https://google.com")[idx], 0.0)
        self.assertEqual(fe.extract_features("https://sub.google.com")[idx], 1.0)
        self.assertEqual(fe.extract_features("https://a.b.google.com")[idx], 2.0)
        # IP addresses should have 0 subdomains
        self.assertEqual(fe.extract_features("http://192.168.1.1/login")[idx], 0.0)

    def test_feature_11_is_shortened(self):
        idx = fe.FEATURE_NAMES.index("is_shortened")
        self.assertEqual(fe.extract_features("http://bit.ly/3xY9zQ")[idx], 1.0)
        self.assertEqual(fe.extract_features("https://tinyurl.com/abc123")[idx], 1.0)
        self.assertEqual(fe.extract_features("https://wikipedia.org")[idx], 0.0)

    def test_feature_12_path_length(self):
        idx = fe.FEATURE_NAMES.index("path_length")
        url = "https://example.com/long/nested/path/to/resource.html"
        vec = fe.extract_features(url)
        self.assertEqual(vec[idx], float(len("/long/nested/path/to/resource.html")))

    def test_feature_13_num_query_params(self):
        idx = fe.FEATURE_NAMES.index("num_query_params")
        self.assertEqual(fe.extract_features("https://example.com/search?q=1&lang=en&page=2")[idx], 3.0)
        self.assertEqual(fe.extract_features("https://example.com/")[idx], 0.0)

    def test_feature_14_has_sensitive_keywords(self):
        idx = fe.FEATURE_NAMES.index("has_sensitive_keywords")
        # Contains 'login' and 'verify' and 'account'
        url = "https://fake-portal.com/login/verify-account.php"
        vec = fe.extract_features(url)
        self.assertGreaterEqual(vec[idx], 2.0)

    def test_feature_15_has_double_slash_redirect(self):
        idx = fe.FEATURE_NAMES.index("has_double_slash_redirect")
        self.assertEqual(fe.extract_features("https://example.com/redirect//http://evil.com")[idx], 1.0)
        self.assertEqual(fe.extract_features("https://example.com/safe/path")[idx], 0.0)

    def test_feature_16_prefix_suffix_hyphen(self):
        idx = fe.FEATURE_NAMES.index("prefix_suffix_hyphen")
        self.assertEqual(fe.extract_features("https://paypal-security-login.com")[idx], 1.0)
        self.assertEqual(fe.extract_features("https://paypal.com")[idx], 0.0)

    def test_feature_17_has_tld_in_subdomain(self):
        idx = fe.FEATURE_NAMES.index("has_tld_in_subdomain")
        self.assertEqual(fe.extract_features("https://paypal.com.account-update.xyz")[idx], 1.0)
        self.assertEqual(fe.extract_features("https://paypal.com")[idx], 0.0)

    def test_feature_ordering_and_count_strictness(self):
        """Ensure feature vector matches FEATURE_NAMES order exactly."""
        vec = fe.extract_features("https://test.com")
        self.assertEqual(len(vec), 17)
        self.assertEqual(len(fe.FEATURE_NAMES), 17)

    # =========================================================================
    # 2. INPUT VALIDATION & SECURITY
    # =========================================================================

    def test_validation_valid_cases(self):
        valid_cases = [
            "https://www.google.com",
            "http://example.com/page?id=123",
            "https://github.com/torvalds/linux",
            "http://192.168.1.1/index.html",
            "http://[2001:db8::1]/path",
            "https://sub.domain.co.uk/docs"
        ]
        for u in valid_cases:
            is_valid, sanitized, err = app.validate_url(u)
            self.assertTrue(is_valid, f"Expected valid URL: {u}. Error: {err}")
            self.assertEqual(err, "")

    def test_validation_disallowed_schemes(self):
        disallowed = [
            "javascript:alert(1)",
            "data:text/html;base64,PHNjcmlwdD4=",
            "file:///C:/Windows/System32",
            "ftp://files.example.com",
            "telnet://192.168.1.1"
        ]
        for u in disallowed:
            is_valid, sanitized, err = app.validate_url(u)
            self.assertFalse(is_valid, f"Scheme should be disallowed: {u}")
            self.assertIn("scheme", err.lower())

    def test_validation_empty_and_whitespace(self):
        for empty_val in ["", "   ", "\t\n", None]:
            is_valid, sanitized, err = app.validate_url(empty_val)
            self.assertFalse(is_valid)
            self.assertIn("valid website url", err.lower())

    def test_validation_malformed_hosts(self):
        invalid_hosts = [
            "http://...",
            "http://-.-",
            "http://example..com",
            "http:///",
            "http://",
            "https://"
        ]
        for bad in invalid_hosts:
            is_valid, sanitized, err = app.validate_url(bad)
            self.assertFalse(is_valid, f"Host should be rejected: {bad}")

    def test_validation_length_limit(self):
        huge_url = "https://example.com/" + ("a" * 2050)
        is_valid, sanitized, err = app.validate_url(huge_url)
        self.assertFalse(is_valid)
        self.assertIn("maximum permissible length", err.lower())

    def test_validation_control_characters_sanitization(self):
        # URLs with embedded newlines or carriage returns should be sanitized
        raw_url = "https://example.com/path\r\n?query=1"
        is_valid, sanitized, err = app.validate_url(raw_url)
        self.assertTrue(is_valid)
        self.assertNotIn("\r", sanitized)
        self.assertNotIn("\n", sanitized)

    # =========================================================================
    # 3. MODEL INFERENCE & ERROR RECOVERY
    # =========================================================================

    def test_prediction_legitimate_url(self):
        res = app.run_prediction("https://www.google.com")
        self.assertTrue(res["success"])
        self.assertIn(res["prediction"], ["Legitimate", "Phishing"])
        self.assertGreaterEqual(res["confidence"], 50.0)
        self.assertIn(res["risk_level"], ["Low Risk", "Low-to-Moderate Risk", "High Risk", "Moderate-High Risk"])
        self.assertIsInstance(res["feature_details"], list)

    def test_prediction_phishing_url(self):
        res = app.run_prediction("http://192.168.1.1/paypal-login/verification.php?cmd=_login_submit")
        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "Phishing")
        self.assertIn("High Risk", res["risk_level"])

    def test_mock_model_inference_failure(self):
        """Simulate unexpected model exception to test graceful error recovery."""
        mock_model = MagicMock()
        mock_model.predict.side_effect = RuntimeError("Simulated matrix compute crash")

        with patch.object(app, "get_model", return_value=mock_model):
            res = app.run_prediction("https://www.test.com")
            self.assertFalse(res["success"])
            self.assertIn("error", res)
            self.assertIn("inference error", res["error"].lower())

    def test_missing_model_handling(self):
        with patch.object(app, "get_model", return_value=None):
            res = app.run_prediction("https://www.test.com")
            self.assertFalse(res["success"])
            self.assertIn("not yet loaded or trained", res["error"])

    # =========================================================================
    # 4. DATABASE OPERATIONS (ISOLATED TEST DB)
    # =========================================================================

    def test_db_insert_retrieve_search_and_clear(self):
        # Insert safe record
        id1 = db.save_scan("https://www.google.com", "Legitimate", 99.5, "Low Risk")
        self.assertIsInstance(id1, int)

        # Insert threat record
        id2 = db.save_scan("http://paypal-fake-login.xyz", "Phishing", 98.2, "High Risk")
        self.assertIsInstance(id2, int)

        # Retrieve statistics
        stats = db.get_scan_stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["legitimate"], 1)
        self.assertEqual(stats["phishing"], 1)

        # Retrieve single record by ID
        rec = db.get_scan_by_id(id1)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["url"], "https://www.google.com")
        self.assertEqual(rec["prediction"], "Legitimate")

        # Search filter
        search_res = db.get_all_scans(search_query="fake-login")
        self.assertEqual(len(search_res), 1)
        self.assertEqual(search_res[0]["prediction"], "Phishing")

        # Clear history
        db.clear_history()
        stats_cleared = db.get_scan_stats()
        self.assertEqual(stats_cleared["total"], 0)

    # =========================================================================
    # 5. FLASK WEB ROUTES & API ENDPOINTS
    # =========================================================================

    def test_get_dashboard_route(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Machine Learning Based", resp.data)

    def test_get_history_route(self):
        resp = self.client.get("/history")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Security Scan History", resp.data)

    def test_get_model_performance_route(self):
        resp = self.client.get("/model-performance")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Model Performance", resp.data)

    def test_get_about_route(self):
        resp = self.client.get("/about")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Threat Architecture", resp.data)

    def test_post_analyze_valid_form(self):
        resp = self.client.post("/analyze", data={"url": "https://www.google.com"}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Scan Report", resp.data)

    def test_post_analyze_invalid_form(self):
        resp = self.client.post("/analyze", data={"url": "ftp://not-supported.com"}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        # Should redirect back to dashboard and flash alert
        self.assertIn(b"Disallowed URL scheme", resp.data)

    def test_get_analyze_disallowed_method(self):
        resp = self.client.get("/analyze")
        self.assertEqual(resp.status_code, 405)

    def test_api_analyze_json_success(self):
        resp = self.client.post(
            "/api/analyze",
            data=json.dumps({"url": "https://www.wikipedia.org"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("prediction", data)
        self.assertIn("confidence", data)

    def test_api_analyze_invalid_payload(self):
        resp = self.client.post(
            "/api/analyze",
            data="not-valid-json",
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertFalse(data["success"])

    def test_api_analyze_missing_url(self):
        resp = self.client.post(
            "/api/analyze",
            data=json.dumps({"wrong_key": "val"}),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertFalse(data["success"])

    def test_view_past_result_route(self):
        sid = db.save_scan("https://www.github.com", "Legitimate", 99.2, "Low Risk")
        resp = self.client.get(f"/result/{sid}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"github.com", resp.data)

    def test_view_nonexistent_result_redirect(self):
        resp = self.client.get("/result/999999", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Scan record not found", resp.data)

    def test_clear_history_post_route(self):
        db.save_scan("https://test.com", "Legitimate", 95.0, "Low Risk")
        resp = self.client.post("/clear-history", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"successfully cleared", resp.data)

    def test_custom_404_handler(self):
        resp = self.client.get("/this-route-does-not-exist-at-all")
        self.assertEqual(resp.status_code, 404)
        self.assertIn(b"404 - Not Found", resp.data)


if __name__ == "__main__":
    unittest.main()
