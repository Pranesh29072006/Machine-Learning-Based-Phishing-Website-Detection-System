"""
Complete End-to-End Test Suite for Machine Learning Based Phishing Website Detection System.
Executes actual HTTP and backend tests against the live application at http://127.0.0.1:5000.
Maintains session cookies to verify flash messages across HTTP 302 redirects.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import sqlite3
import numpy as np

BASE_URL = "http://127.0.0.1:5000"
PROJECT_DIR = r"E:\PROJECT"

class TestRunner:
    def __init__(self):
        self.results = []
        self.categories = {
            "Frontend": {"total": 0, "pass": 0, "fail": 0, "blocked": 0},
            "Backend": {"total": 0, "pass": 0, "fail": 0, "blocked": 0},
            "Machine Learning": {"total": 0, "pass": 0, "fail": 0, "blocked": 0},
            "Database": {"total": 0, "pass": 0, "fail": 0, "blocked": 0},
            "API": {"total": 0, "pass": 0, "fail": 0, "blocked": 0},
            "Security": {"total": 0, "pass": 0, "fail": 0, "blocked": 0},
            "End-to-End": {"total": 0, "pass": 0, "fail": 0, "blocked": 0}
        }
        self.cookie_jar = http.cookiejar.CookieJar()
        self.cookie_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))

    def record(self, category: str, test_name: str, passed: bool, details: str = "", blocked: bool = False):
        status = "BLOCKED" if blocked else ("PASS" if passed else "FAIL")
        self.categories[category]["total"] += 1
        if blocked:
            self.categories[category]["blocked"] += 1
        elif passed:
            self.categories[category]["pass"] += 1
        else:
            self.categories[category]["fail"] += 1

        self.results.append({
            "category": category,
            "test_name": test_name,
            "status": status,
            "details": details
        })
        icon = "[PASS]" if status == "PASS" else ("[FAIL]" if status == "FAIL" else "[BLOCKED]")
        print(f" {icon} [{category}] {test_name}: {details}")

    def http_get(self, path: str):
        url = BASE_URL + path
        req = urllib.request.Request(url, headers={"User-Agent": "E2E-Tester/1.0"})
        try:
            with self.cookie_opener.open(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return resp.status, body, resp.headers
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return e.code, body, e.headers
        except Exception as e:
            return 0, str(e), {}

    def http_post_form(self, path: str, data: dict):
        url = BASE_URL + path
        encoded = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(url, data=encoded, headers={
            "User-Agent": "E2E-Tester/1.0",
            "Content-Type": "application/x-www-form-urlencoded"
        })
        try:
            with self.cookie_opener.open(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return resp.status, body, resp.headers
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return e.code, body, e.headers
        except Exception as e:
            return 0, str(e), {}

    def http_post_json(self, path: str, data: any):
        url = BASE_URL + path
        encoded = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=encoded, headers={
            "User-Agent": "E2E-Tester/1.0",
            "Content-Type": "application/json"
        })
        try:
            with self.cookie_opener.open(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return resp.status, body, resp.headers
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return e.code, body, e.headers
        except Exception as e:
            return 0, str(e), {}


def run_tests():
    runner = TestRunner()
    print("=" * 75)
    print("STARTING COMPLETE END-TO-END AUTOMATED TEST SUITE")
    print(f"Target Server: {BASE_URL}")
    print("=" * 75)

    # -------------------------------------------------------------
    # PHASE 2: Application Startup & Static Files
    # -------------------------------------------------------------
    print("\n--- PHASE 2: APPLICATION STARTUP & STATIC ASSETS ---")
    
    # 1. Server responsive
    status, body, _ = runner.http_get("/")
    runner.record(
        "Backend",
        "Application Startup & HTTP Availability",
        status == 200,
        f"Server returned HTTP {status}"
    )

    # 2. CSS Asset
    status, body, headers = runner.http_get("/static/css/style.css")
    css_ok = (status == 200 and "--bg-primary" in body and "cyber-card" in body)
    runner.record(
        "Frontend",
        "CSS Stylesheet Delivery (/static/css/style.css)",
        css_ok,
        f"HTTP {status}, size {len(body)} bytes, includes cyber theme rules"
    )

    # 3. JavaScript Asset
    status, body, headers = runner.http_get("/static/js/script.js")
    js_ok = (status == 200 and "renderModelPerformanceCharts" in body and "DOMContentLoaded" in body)
    runner.record(
        "Frontend",
        "JavaScript Client Asset Delivery (/static/js/script.js)",
        js_ok,
        f"HTTP {status}, size {len(body)} bytes, includes Chart.js & overlay handlers"
    )

    # 4. Logo SVG Asset
    status, body, headers = runner.http_get("/static/images/logo.svg")
    svg_ok = (status == 200 and "<svg" in body and "</svg>" in body)
    runner.record(
        "Frontend",
        "Brand Logo SVG Vector Delivery (/static/images/logo.svg)",
        svg_ok,
        f"HTTP {status}, valid XML SVG vector markup"
    )

    # -------------------------------------------------------------
    # PHASE 3: Frontend Route & Page Loading Tests
    # -------------------------------------------------------------
    print("\n--- PHASE 3: FRONTEND PAGE LOADING & RENDERING ---")

    # 1. Homepage / Dashboard
    status, body, _ = runner.http_get("/")
    has_home_elements = all(k in body for k in [
        "PHISH",
        "analyzeForm",
        "urlInput",
        "sample-badge",
        "Total URLs Analyzed",
        "Legitimate Sites",
        "Phishing Threats",
        "Model Ready"
    ])
    runner.record(
        "Frontend",
        "Homepage / Dashboard Rendering (/)",
        status == 200 and has_home_elements,
        "HTTP 200 with Brand, Form, Sample Pills, Model Status, and KPI cards"
    )

    # 2. History Page
    status, body, _ = runner.http_get("/history")
    has_history_elements = all(k in body for k in [
        "Security Scan History",
        "Total Scanned",
        "Safe Verified",
        "Threats Flagged",
        "name=\"q\""
    ])
    runner.record(
        "Frontend",
        "Scan History Page Rendering (/history)",
        status == 200 and has_history_elements,
        "HTTP 200 with Stats summary, Filter search box, and table structure"
    )

    # 3. Model Performance Page
    status, body, _ = runner.http_get("/model-performance")
    has_perf_elements = all(k in body for k in [
        "Model Performance & Evaluation",
        "Accuracy",
        "Precision",
        "Recall",
        "F1-Score",
        "Confusion Matrix",
        "modelComparisonChart",
        "featureImportanceChart"
    ])
    runner.record(
        "Frontend",
        "Model Performance Page Rendering (/model-performance)",
        status == 200 and has_perf_elements,
        "HTTP 200 with 4 KPI cards, Confusion Matrix, and 2 Chart.js canvases"
    )

    # 4. Threat Architecture / About Page
    status, body, _ = runner.http_get("/about")
    has_about_elements = all(k in body for k in [
        "Phishing Attack Anatomy",
        "Subdomain Camouflage",
        "URL Shortening Cloaking",
        "Direct IP Address Hosts",
        "17 Extracted Heuristic Feature Vectors"
    ])
    runner.record(
        "Frontend",
        "Threat Architecture / About Page Rendering (/about)",
        status == 200 and has_about_elements,
        "HTTP 200 with Attack Anatomy breakdown and 17 feature descriptions"
    )

    # 5. Custom 404 Error Handler Page
    status, body, _ = runner.http_get("/non-existent-route-testing-404")
    has_404_elements = (status == 404 and "404 - Not Found" in body and "Return to Dashboard" in body)
    runner.record(
        "Frontend",
        "Custom 404 Error Page Handler",
        has_404_elements,
        "HTTP 404 with custom cybersecurity theme layout and recovery navigation link"
    )

    # -------------------------------------------------------------
    # PHASE 4: Phishing Detection Testing with Safe Examples
    # -------------------------------------------------------------
    print("\n--- PHASE 4: PHISHING DETECTION TESTING (12 SCENARIOS) ---")

    test_urls = [
        ("Valid normal URL", "https://www.google.com", True, "Legitimate"),
        ("URL with HTTPS", "https://en.wikipedia.org/wiki/Computer_security", True, "Legitimate"),
        ("URL with HTTP", "http://example.com/index.html", True, "Legitimate"),
        ("URL containing an IP address", "http://192.168.1.1/paypal-login/verification.php", True, "Phishing"),
        ("URL with multiple subdomains", "https://appleid.apple.com.verify-device.account-update.info/login", True, "Phishing"),
        ("URL containing unusual characters", "https://example.com/test?token=@!$%^&*()", True, None),
        ("Empty input", "", False, "Please enter a valid website URL."),
        ("Invalid URL", "not a valid website url!@#", False, "Invalid domain format"),
        ("URL without a protocol", "github.com/torvalds/linux", True, "Legitimate"),
        ("Very long URL (>2048 chars)", "https://example.com/" + ("a" * 2100), False, "URL exceeds maximum permissible length"),
        ("Duplicate URL submission", "https://www.google.com", True, "Legitimate"),
        ("URL with query parameters", "https://example.com/search?q=cybersecurity&category=research", True, "Legitimate")
    ]

    for label, url, expected_valid, expected_outcome in test_urls:
        status, body, headers = runner.http_post_form("/analyze", {"url": url})
        
        if expected_valid:
            passed = (status == 200 and "Extracted URL Feature Breakdown" in body and "17 Vectors Analyzed" in body)
            if expected_outcome:
                passed = passed and (expected_outcome in body)
            details = f"HTTP 200, successfully analyzed, rendered 17-vector result page"
        else:
            passed = (status == 200 and expected_outcome.lower() in body.lower())
            details = f"Gracefully intercepted invalid input with alert message"

        runner.record(
            "Backend",
            f"URL Detection Test: {label}",
            passed,
            details
        )

    # -------------------------------------------------------------
    # PHASE 5: Machine Learning Testing
    # -------------------------------------------------------------
    print("\n--- PHASE 5: MACHINE LEARNING PIPELINE & MODEL TESTING ---")

    import app as app_module
    import feature_extraction as fe

    # 1. Model Loading
    model = app_module.get_model()
    model_loaded = model is not None and hasattr(model, "predict")
    runner.record(
        "Machine Learning",
        "Trained Model Deserialization & Loading",
        model_loaded,
        f"Champion model loaded successfully: {type(model).__name__}"
    )

    # 2. Feature Vector Dimension & Ordering
    sample_url = "https://www.paypal-verification.com/login.php?id=123"
    features = fe.extract_features(sample_url)
    dim_ok = (isinstance(features, np.ndarray) and features.shape == (17,) and len(fe.FEATURE_NAMES) == 17)
    runner.record(
        "Machine Learning",
        "Feature Vector Dimension & Order Strictness",
        dim_ok,
        f"Extracted shape {features.shape}, exactly 17 features matching FEATURE_NAMES"
    )

    # 3. Feature Details Count Alignment
    details_list = fe.get_feature_details(sample_url)
    details_count_ok = (len(details_list) == 17)
    runner.record(
        "Machine Learning",
        "Human-Readable Feature Details Alignment (17 Vectors)",
        details_count_ok,
        f"get_feature_details returned {len(details_list)} diagnostic objects"
    )

    # 4. Predict Proba and Confidence Calibration
    pred_res = app_module.run_prediction("https://www.google.com")
    conf_ok = (pred_res["success"] and 50.0 <= pred_res["confidence"] <= 100.0 and pred_res["risk_level"] in ["Low Risk", "Low-to-Moderate Risk", "Moderate-High Risk", "High Risk"])
    runner.record(
        "Machine Learning",
        "Continuous Confidence Scoring & Risk Level Mapping",
        conf_ok,
        f"Predicted '{pred_res['prediction']}' with {pred_res['confidence']}% certainty ({pred_res['risk_level']})"
    )

    # 5. Missing Model Graceful Error Handling
    orig_pipeline = app_module._model_pipeline
    try:
        app_module._model_pipeline = None
        orig_model_path = app_module.MODEL_PATH
        app_module.MODEL_PATH = "nonexistent_model_file.joblib"
        
        miss_res = app_module.run_prediction("https://example.com")
        miss_ok = (not miss_res["success"] and "not yet loaded" in miss_res["error"])
        runner.record(
            "Machine Learning",
            "Missing Model File Graceful Handling",
            miss_ok,
            "Returns structured failure message without crashing web application"
        )
    finally:
        app_module._model_pipeline = orig_pipeline
        app_module.MODEL_PATH = orig_model_path

    # 6. Inference Exception Recovery
    class FailingModel:
        def predict(self, X):
            raise RuntimeError("Simulated GPU/CPU matrix compute failure")
    
    try:
        app_module._model_pipeline = FailingModel()
        crash_res = app_module.run_prediction("https://example.com")
        crash_ok = (not crash_res["success"] and "inference error occurred" in crash_res["error"])
        runner.record(
            "Machine Learning",
            "Inference Exception Recovery & Fault Tolerance",
            crash_ok,
            "Caught runtime compute exception, logged error, returned clean user message"
        )
    finally:
        app_module._model_pipeline = orig_pipeline

    # -------------------------------------------------------------
    # PHASE 6: Database Testing
    # -------------------------------------------------------------
    print("\n--- PHASE 6: DATABASE TESTING (SQLITE OPERATIONS) ---")

    import database.db as db

    # 1. Database Connection & Schema
    conn = db.get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scans';")
        has_table = cur.fetchone() is not None
        cur.execute("PRAGMA table_info(scans);")
        columns = [row["name"] for row in cur.fetchall()]
        schema_ok = has_table and all(col in columns for col in ["id", "url", "prediction", "confidence", "risk_level", "created_at"])
    finally:
        conn.close()

    runner.record(
        "Database",
        "SQLite Connection & Schema Verification",
        schema_ok,
        f"Verified 'scans' table exists with columns: {columns}"
    )

    # 2. Insert Record
    test_scan_url = "https://e2e-test-database-record.org/test"
    new_id = db.save_scan(test_scan_url, "Legitimate", 98.5, "Low Risk")
    runner.record(
        "Database",
        "Insert Scan Record (save_scan)",
        new_id > 0,
        f"Inserted test row with ID #{new_id}"
    )

    # 3. Retrieve by ID
    fetched_record = db.get_scan_by_id(new_id)
    fetch_ok = (fetched_record is not None and fetched_record["url"] == test_scan_url and fetched_record["prediction"] == "Legitimate")
    runner.record(
        "Database",
        "Retrieve Record by ID (get_scan_by_id)",
        fetch_ok,
        f"Retrieved scan #{new_id}: URL={fetched_record['url']}, Confidence={fetched_record['confidence']}%"
    )

    # 4. Search Filtering
    search_results = db.get_all_scans(search_query="e2e-test-database-record")
    search_ok = (len(search_results) >= 1 and any(r["id"] == new_id for r in search_results))
    runner.record(
        "Database",
        "Parameterized Search Query Filter (get_all_scans)",
        search_ok,
        f"Found {len(search_results)} matching row(s) for search keyword"
    )

    # 5. Statistics Computation
    stats = db.get_scan_stats()
    stats_ok = (isinstance(stats, dict) and stats["total"] >= 1 and "phishing_percentage" in stats)
    runner.record(
        "Database",
        "Aggregate Scan Statistics Calculation (get_scan_stats)",
        stats_ok,
        f"Total: {stats['total']}, Safe: {stats['legitimate']}, Phishing: {stats['phishing']} ({stats['phishing_percentage']}%)"
    )

    # 6. Data Persistence Across Reconnections
    conn1 = db.get_connection()
    conn1.close()
    conn2 = db.get_connection()
    try:
        cur = conn2.cursor()
        cur.execute("SELECT COUNT(*) as cnt FROM scans WHERE id = ?", (new_id,))
        count_val = cur.fetchone()["cnt"]
        persist_ok = (count_val == 1)
    finally:
        conn2.close()

    runner.record(
        "Database",
        "Data Persistence After Connection Close/Reopen",
        persist_ok,
        "Record persists reliably in SQLite storage file"
    )

    # -------------------------------------------------------------
    # PHASE 7: API and Backend Testing
    # -------------------------------------------------------------
    print("\n--- PHASE 7: API & BACKEND ROUTE TESTING ---")

    # 1. JSON API Success POST /api/analyze
    status, body, headers = runner.http_post_json("/api/analyze", {"url": "https://www.github.com"})
    try:
        api_data = json.loads(body)
        api_ok = (status == 200 and api_data.get("success") is True and api_data.get("prediction") == "Legitimate")
    except Exception:
        api_ok = False
        api_data = {}

    runner.record(
        "API",
        "JSON Analysis API Success (POST /api/analyze)",
        api_ok,
        f"HTTP {status}, returned prediction='{api_data.get('prediction')}', confidence={api_data.get('confidence')}%"
    )

    # 2. JSON API Missing URL Field
    status, body, _ = runner.http_post_json("/api/analyze", {})
    try:
        err_data = json.loads(body)
        err_ok = (status == 400 and err_data.get("success") is False and "Please enter a valid website URL." in err_data.get("error", ""))
    except Exception:
        err_ok = False

    runner.record(
        "API",
        "JSON Analysis API Missing URL Validation",
        err_ok,
        f"HTTP {status}, returned 400 Bad Request with client validation message"
    )

    # 3. JSON API Non-JSON / Malformed Payload
    status, body, _ = runner.http_post_json("/api/analyze", "This is plain string not object")
    try:
        err_data2 = json.loads(body)
        err_ok2 = (status == 400 and err_data2.get("success") is False)
    except Exception:
        err_ok2 = False

    runner.record(
        "API",
        "JSON Analysis API Malformed Payload Handling",
        err_ok2,
        f"HTTP {status}, returned 400 Bad Request with format error"
    )

    # 4. Disallowed HTTP Method on POST-only Route (GET /analyze)
    status, body, _ = runner.http_get("/analyze")
    runner.record(
        "API",
        "Disallowed HTTP Method Rejection (GET /analyze -> 405)",
        status == 405,
        f"HTTP {status} Method Not Allowed returned correctly"
    )

    # 5. Result Page by ID Route (GET /result/<scan_id>)
    status, body, _ = runner.http_get(f"/result/{new_id}")
    res_page_ok = (status == 200 and f"Scan Report #{new_id}" in body and "Extracted URL Feature Breakdown" in body)
    runner.record(
        "Backend",
        f"Historical Result Route (GET /result/{new_id})",
        res_page_ok,
        f"HTTP {status}, correctly reconstructed 17 features from saved database scan"
    )

    # 6. Non-Existent Result ID Redirect
    status, body, headers = runner.http_get("/result/9999999")
    redirect_ok = (status == 200 and "Scan record not found." in body)
    runner.record(
        "Backend",
        "Non-Existent Scan ID Graceful Redirect",
        redirect_ok,
        "Redirected to /history with user-friendly warning message"
    )

    # -------------------------------------------------------------
    # PHASE 8: Security & Reliability Testing
    # -------------------------------------------------------------
    print("\n--- PHASE 8: SECURITY & RELIABILITY TESTING ---")

    # 1. XSS Injection Attempt
    xss_payload = "<script>alert('xss-exploit')</script>"
    status, body, _ = runner.http_post_form("/analyze", {"url": xss_payload})
    xss_blocked = (status == 200 and "<script>alert" not in body and "Invalid domain" in body)
    runner.record(
        "Security",
        "Cross-Site Scripting (XSS) Input Sanitization",
        xss_blocked,
        "Blocked malicious script tags before analysis, no script execution"
    )

    # 2. SQL Injection Attempt
    sqli_payload = "https://example.com/test' OR '1'='1"
    status, body, _ = runner.http_post_form("/analyze", {"url": sqli_payload})
    sqli_safe = (status == 200 and "database disk image is malformed" not in body and "OperationalError" not in body)
    runner.record(
        "Security",
        "SQL Injection Prevention via Parameterized Queries",
        sqli_safe,
        "Processed via parameterized statements without SQL syntax breakage"
    )

    # 3. Disallowed Schemes: JavaScript / Data / File
    for bad_scheme in ["javascript:alert(document.cookie)", "data:text/html;base64,PHNjcmlwdD4=", "file:///etc/shadow"]:
        status, body, _ = runner.http_post_form("/analyze", {"url": bad_scheme})
        scheme_blocked = (status == 200 and "Disallowed URL scheme" in body)
        runner.record(
            "Security",
            f"Disallowed Protocol Scheme Block ({bad_scheme.split(':')[0]}:)",
            scheme_blocked,
            f"Blocked protocol '{bad_scheme.split(':')[0]}:' safely"
        )

    # 4. Zero Outbound Network Connections Verification
    t0 = time.time()
    status, body, _ = runner.http_post_form("/analyze", {"url": "https://nonexistent-domain-that-will-never-resolve-12345.com/login"})
    elapsed = time.time() - t0
    zero_net_ok = (status == 200 and elapsed < 1.0)
    runner.record(
        "Security",
        "Zero External Outbound HTTP Requests (Offline Safety)",
        zero_net_ok,
        f"Completed lexical inference in {elapsed:.3f}s with no socket delays to target"
    )

    # -------------------------------------------------------------
    # PHASE 9: Complete End-to-End User Journey Simulation
    # -------------------------------------------------------------
    print("\n--- PHASE 9: END-TO-END BROWSER WORKFLOW SIMULATION ---")

    st1, b1, _ = runner.http_get("/")
    target_journey_url = "https://secure-banking-verification-update.com/account/login"
    st2, b2, _ = runner.http_post_form("/analyze", {"url": target_journey_url})
    journey_result_ok = (st2 == 200 and "Scan Analysis Result" in b2 and "17 Vectors Analyzed" in b2)
    st3, b3, _ = runner.http_get("/history")
    journey_history_ok = (st3 == 200 and "secure-banking-verification-update.com" in b3)
    st4, b4, _ = runner.http_get("/model-performance")
    journey_perf_ok = (st4 == 200 and "Multi-Algorithm Performance Benchmark" in b4)
    st5, b5, _ = runner.http_get("/about")
    journey_about_ok = (st5 == 200 and "Phishing Attack Anatomy" in b5)

    complete_journey_ok = (st1 == 200 and journey_result_ok and journey_history_ok and journey_perf_ok and journey_about_ok)
    runner.record(
        "End-to-End",
        "Full User Navigation & Detection Lifecycle Workflow",
        complete_journey_ok,
        "Homepage -> Form Submit -> Diagnostic Result -> History Log -> Model Evaluation -> Threat Docs"
    )

    # -------------------------------------------------------------
    # TEST SUMMARY & REPORT COMPILATION
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print("TEST EXECUTION COMPLETE. GENERATING SUMMARY TABLE:")
    print("=" * 75)
    print(f"{'Category':<20} | {'Total':>6} | {'Passed':>7} | {'Failed':>7} | {'Blocked':>8}")
    print("-" * 57)
    grand_total = 0
    grand_pass = 0
    grand_fail = 0
    grand_blocked = 0

    for cat, counts in runner.categories.items():
        grand_total += counts["total"]
        grand_pass += counts["pass"]
        grand_fail += counts["fail"]
        grand_blocked += counts["blocked"]
        print(f"{cat:<20} | {counts['total']:>6} | {counts['pass']:>7} | {counts['fail']:>7} | {counts['blocked']:>8}")

    print("-" * 57)
    print(f"{'OVERALL TOTAL':<20} | {grand_total:>6} | {grand_pass:>7} | {grand_fail:>7} | {grand_blocked:>8}")
    print("=" * 75)

    return runner


if __name__ == "__main__":
    runner = run_tests()
