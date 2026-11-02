# CodePulse AI — Consolidated Test Execution Report
**Project:** CodePulse AI – Machine Learning Based Phishing Website Detection System  
**Location:** `E:\PROJECT`  
**Execution Date:** November 2026  
**Test Harness:** Python `unittest`, AST Compilation Engine, Flask WSGI Client  

---

## 1. Test Summary

| Test Category | Suite Location | Executed | Passed | Failed | Pass Rate |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **AST Compilation** | All Python Source Files | 46 | 46 | 0 | **100%** |
| **Unit Tests** | `tests/unit/` | 9 | 9 | 0 | **100%** |
| **Integration Tests** | `tests/integration/` | 6 | 6 | 0 | **100%** |
| **Modular E2E Test** | `tests/e2e/` | 1 | 1 | 0 | **100%** |
| **System Test Suite** | `test_system.py` | 59 | 59 | 0 | **100%** |
| **WSGI Route Verification**| Live HTTP Endpoints | 18 | 18 | 0 | **100%** |
| **OVERALL TOTAL** | | **139** | **139** | **0** | **100%** |

---

## 2. Test Coverage by Subsystem

### 2.1 Machine Learning & 17 Feature Vector Tests
- Verified 17-dimensional feature vector extraction order matching `FEATURE_NAMES`:
  `url_length`, `domain_length`, `num_dots`, `num_hyphens`, `num_digits`, `has_ip_address`, `is_https`, `has_at_symbol`, `num_suspicious_symbols`, `num_subdomains`, `is_shortened`, `path_length`, `num_query_params`, `has_sensitive_keywords`, `has_double_slash_redirect`, `prefix_suffix_hyphen`, `has_tld_in_subdomain`.
- Verified IPv4 and IPv6 detection, including bracketed literals and port stripping.
- Verified URL shortener domain mapping against 60+ known services.

### 2.2 Defensive Validation Tests
- Verified length constraint enforcement ($\le 2048$ characters).
- Verified protocol whitelist (`http://`, `https://`) and blocking of `javascript:`, `data:`, `file:`.
- Verified RFC DNS label character regex matching.

### 2.3 Persistence & Database Operations
- Verified parameterized insertion into `scans` table and lastrowid retrieval.
- Verified KPI telemetry aggregation (total scans, legitimate/phishing counts, detection rate).
- Verified history pagination, search filtering, and RFC 4180 CSV export.

### 2.4 HTTP Routes & Presentation Layer
- Verified HTTP 200 responses on all pages: `/`, `/scanner`, `/history`, `/analytics`, `/model-performance`, `/security-insights`, `/settings`, `/about`.
- Verified JSON responses on `/api/analyze`, `/api/scan`, and `/api/stats`.
- Verified session flash messaging and HTTP 302 redirects.

