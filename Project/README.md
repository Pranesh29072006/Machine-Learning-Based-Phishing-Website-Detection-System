# CodePulse AI – Intelligent Phishing Website Detection Platform

[![Python Version](https://img.shields.io/badge/Python-3.11.15-blue.svg)](https://python.org)
[![Flask Framework](https://img.shields.io/badge/Flask-3.1.3-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.1-orange.svg)](https://scikit-learn.org/)
[![Test Suite Status](https://img.shields.io/badge/Tests-104%2F104%20PASS-brightgreen.svg)]()
[![Inference Mode](https://img.shields.io/badge/Network%20Mode-100%25%20Offline-cyan.svg)]()

**CodePulse AI** is an enterprise-grade cybersecurity web application and Security Operations Center (SOC) dashboard designed to inspect, analyze, and detect deceptive Uniform Resource Locators (URLs) prior to user navigation. 

Utilizing an empirical 17-dimensional lexical and structural feature engineering pipeline paired with an ensemble Random Forest classifier, the system calculates fraud probability and outputs diagnostic security telemetry—operating in non-destructive local inference with **zero outbound network connections**.

---

## 1. Enterprise Cybersecurity SaaS Architecture

The platform provides a modern Security Operations interface with dark navy styling, electric blue accents, responsive collapsible navigation, and real-time Chart.js visual telemetry across 8 dedicated operational modules:

```
+-----------------------------------------------------------------------------------+
|                           CODEPULSE AI - SAAS PLATFORM                            |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Sidebar Navigation]        [Top Navigation Bar: Search, Status, Notifications]  |
|  - 1. Overview               +-------------------------------------------------+  |
|  - 2. URL Scanner            | Active Route View                               |  |
|  - 3. Scan History           |                                                 |  |
|  - 4. Threat Analytics       | - Real-time Database KPIs (Total, Safe, Phish)  |  |
|  - 5. Model Performance      | - Interactive URL Feature Extraction (17 Dims)  |  |
|  - 6. Security Insights      | - Continuous Probability & Risk Stratification  |  |
|  - 7. System Settings        | - SQLite Persistence with Latency Tracking (ms) |  |
|  - 8. Platform Docs          | - CSV Export & RESTful JSON API Integrations    |  |
|                              +-------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Module Breakdown

| Route | Module Name | Core Responsibility |
|---|---|---|
| `/` or `/overview` | **Operations Overview** | 6 live KPI cards, daily scan volume chart, detection ratio doughnut, recent audits table, and quick scanner console. |
| `/scanner` | **URL Scanner Console** | Dedicated inspection console with clearing button, real-time client-side validation, 6 test pills, and animated radar overlay. |
| `/analyze` & `/result/<id>` | **Diagnostic Telemetry Report** | High-visibility verdict banner, calibrated certainty meter, latency telemetry, and granular 17-vector feature table. |
| `/history` | **Scan Audit Log** | Paginated persistent SQLite audit trail with keyword search, sorting, classification filtering, and modal clear confirmation. |
| `/history/export` | **CSV Export Engine** | Generates dynamic, streaming RFC-compliant CSV files containing full scan audit logs. |
| `/analytics` | **Threat Analytics Center** | Daily scan timeline chart, classification distribution, risk severity breakdown, and confidence histogram. |
| `/model-performance` | **Model Performance Center** | Empirical benchmarks (95.93% accuracy, 99.47% ROC-AUC), $2\times2$ confusion matrix, algorithm comparison, and feature importance charts. |
| `/security-insights` | **Security Insights & Tactics** | Knowledge base breaking down adversarial phishing tactics, detection heuristics, and defensive mitigations. |
| `/settings` | **Platform Settings & Diagnostics**| Theme preference toggles (Dark, High Contrast, Light), latency toggles, engine health monitor, and SQLite storage stats. |
| `/about` | **System Architecture & Docs** | Comprehensive system workflow, 5-stage pipeline, and complete academic documentation. |

---

## 2. Technology Stack

- **Backend:** Python 3.11.15, Flask 3.1.3 (WSGI / Werkzeug)
- **Machine Learning:** Scikit-Learn 1.9.1 (Random Forest, Gradient Boosting, Decision Tree, Logistic Regression)
- **Data Engineering:** Pandas 2.2.3, NumPy 2.2.3
- **Model Serialization:** Joblib 1.4.2, JSON
- **Database:** SQLite 3 with WAL-mode connection management, parameterized queries, and automatic migrations
- **Frontend:** Semantic HTML5, Bootstrap 5.3.3, Vanilla ES6+ JavaScript, CSS3 Custom Properties (Design System)
- **Visualization:** Chart.js 4.4.2 (Responsive canvas-based bar, doughnut, and timeline charts)
- **Icons & Typography:** Bootstrap Icons 1.11.3, Google Fonts (`Inter` & `JetBrains Mono`)

---

## 3. Machine Learning Pipeline & Empirical Verification

### Dataset & Training Configuration
- **Dataset Size:** 7,000 balanced real-world URLs (`data/phishing_dataset.csv`):
  - **3,500 Benign URLs:** Cisco OpenDNS Top Million and University of New Brunswick (UNB) CIC benign datasets.
  - **3,500 Phishing URLs:** Verified active fraud feeds from PhishTank and OpenPhish.
- **Evaluation Split:** Stratified 80/20 train/test split evaluated on 1,400 completely unseen URLs.

### Champion Model Evaluation Metrics

| Metric | Random Forest (Champion) | Gradient Boosting | Decision Tree | Logistic Regression |
|---|---|---|---|---|
| **Accuracy** | **95.93%** | 95.79% | 94.71% | 83.71% |
| **Precision** | **97.49%** | 97.48% | 97.57% | 84.91% |
| **Recall** | **94.29%** | 94.00% | 91.71% | 82.00% |
| **F1-Score** | **95.86%** | 95.71% | 94.55% | 83.43% |
| **ROC-AUC** | **99.47%** | 99.19% | 94.71% | 92.40% |

### Domain Generalization Check (`GroupShuffleSplit`)
To verify the model learns structural lexical anomalies rather than memorizing domain names, a domain-disjoint split evaluated on 100% disjoint domain names achieved:
- **Disjoint Test Accuracy:** **97.21%**
- **Disjoint Test F1-Score:** **97.55%**

---

## 4. The 17 Extracted Heuristic Feature Vectors

| # | Feature Key | Data Type | Threat Significance & Heuristic Analysis |
|---|---|---|---|
| 1 | `url_length` | Numeric | Phishing links often exceed 75 characters to hide complex redirection parameters. |
| 2 | `domain_length` | Numeric | Hostnames exceeding 30 characters frequently pad brand names with spoof suffixes. |
| 3 | `num_dots` | Numeric | High dot frequency ($\ge 3$) indicates nested spoof subdomains. |
| 4 | `num_hyphens` | Numeric | Hyphenated domain names (e.g. `apple-id-verify.com`) indicate trademark spoofing. |
| 5 | `num_digits` | Numeric | High numeric digit density represents randomized token paths or IP port camouflage. |
| 6 | `has_ip_address` | Binary (0/1) | Direct IPv4/IPv6 address hosts bypass DNS registration records (WHOIS). |
| 7 | `is_https` | Binary (0/1) | Encrypted protocol check (note: modern phishing kits may also provision free SSL certs). |
| 8 | `has_at_symbol` | Binary (0/1) | User-info delimiter character `@` redirects browsers to whatever follows it. |
| 9 | `num_suspicious_symbols` | Numeric | Delimiters (`?`, `=`, `&`, `%`, `~`, `+`, `$`) transmitting encoded stolen data. |
| 10 | `num_subdomains` | Numeric | Deep subdomain structures (e.g. `bank.secure.login.attacker.xyz`). |
| 11 | `is_shortened` | Binary (0/1) | Masked destination via shortening providers (`bit.ly`, `tinyurl`, `t.co`). |
| 12 | `path_length` | Numeric | Excessive directory path depth concealing credential harvesting assets. |
| 13 | `num_query_params` | Numeric | Frequency of query parameters transmitting exfiltrated data. |
| 14 | `has_sensitive_keywords` | Numeric | Trigger keywords: `login`, `verify`, `account`, `banking`, `secure`, `update`, `signin`. |
| 15 | `has_double_slash_redirect` | Binary (0/1) | Double slashes `//` within resource paths to trigger open redirects. |
| 16 | `prefix_suffix_hyphen` | Binary (0/1) | Hyphens placed directly in the domain portion to deceive human readers. |
| 17 | `has_tld_in_subdomain` | Binary (0/1) | Deceptive TLD camouflage (e.g. `paypal.com.attacker.net`). |

---

## 5. RESTful JSON API Documentation

Third-party platforms, security incident response tools, and SIEM pipelines can query CodePulse AI programmatically:

### `POST /api/analyze` or `POST /api/scan`
Evaluates a target URL and records the telemetry in SQLite.

**Request:**
```http
POST /api/analyze HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{
  "url": "https://secure-banking-portal.com/login"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "scan_id": 182,
  "url": "https://secure-banking-portal.com/login",
  "prediction": "Phishing",
  "confidence": 98.3,
  "risk_level": "High Risk",
  "processing_time_ms": 14.8,
  "feature_details": [...],
  "analyzed_at": "2026-11-02 11:55:00"
}
```

### `GET /api/stats`
Fetches aggregate scan statistics and detection rates.

**Response (200 OK):**
```json
{
  "success": true,
  "stats": {
    "total": 135,
    "legitimate": 72,
    "phishing": 63,
    "safe_percentage": 53.3,
    "phishing_percentage": 46.7,
    "detection_rate": 46.7,
    "avg_processing_time_ms": 15.6
  }
}
```

### `GET /api/analytics`
Fetches structured telemetry for dashboard visualizations.

---

## 6. Project Directory Structure

```
E:\PROJECT\
│
├── app.py                                       # Flask application with routes, context processors & API
├── feature_extraction.py                        # 17-vector heuristic feature extraction engine
├── train_model.py                               # ML training, cross-validation & benchmark exporter
├── test_system.py                               # Automated system unit test suite (55 test cases)
├── run_comprehensive_e2e_tests.py               # Complete end-to-end automated test runner (49 test cases)
├── requirements.txt                             # Python dependencies
├── README.md                                    # Comprehensive system documentation
│
├── data/
│   ├── download_dataset.py                      # Dataset fetcher script
│   └── phishing_dataset.csv                     # Balanced dataset (7,000 labeled URLs)
│
├── models/
│   ├── phishing_model.joblib                    # Serialized Random Forest classifier
│   └── model_metrics.json                       # Evaluated metrics, confusion matrix & feature weights
│
├── database/
│   ├── db.py                                    # SQLite persistence module with migrations & analytics
│   └── scan_history.db                          # SQLite audit repository
│
├── templates/
│   ├── base.html                                # Global layout, sidebar, navbar, notifications & themes
│   ├── index.html                               # Overview dashboard with real KPIs, charts & quick scan
│   ├── scanner.html                             # Dedicated URL Scanner Console with samples & radar overlay
│   ├── result.html                              # Diagnostic report with verdict banner & 17 vectors table
│   ├── history.html                             # Paginated audit log with search, filters & CSV download
│   ├── analytics.html                           # Threat Analytics Center with 4 Chart.js telemetry charts
│   ├── model_performance.html                   # Benchmark comparisons, confusion matrix & charts
│   ├── security_insights.html                   # Adversarial tactics and heuristic analysis guide
│   ├── settings.html                            # System settings, UI preferences & engine diagnostics
│   ├── about.html                               # Architecture documentation and attack anatomy
│   ├── 404.html                                 # Custom cybersecurity 404 Not Found error page
│   └── 500.html                                 # Custom cybersecurity 500 Internal Error page
│
└── static/
    ├── css/
    │   └── style.css                            # Enterprise cybersecurity SaaS design system
    ├── js/
    │   └── script.js                            # Sidebar controls, theme toggler, Chart.js & scan overlay
    └── images/
        └── logo.svg                             # Custom vector cyber shield logo
```

---

## 7. Installation, Setup & Execution

### Prerequisites
- Python 3.10+ (Verified on Python 3.11.15)
- Git (optional)

### Step 1: Clone or Navigate to Project
```bash
cd E:\PROJECT
```

### Step 2: Initialize Virtual Environment & Dependencies
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt
```

### Step 3: Train / Verify Model Artifacts (Optional)
```bash
python train_model.py
```

### Step 4: Start the Web Application
```bash
python app.py
```
The server will bind to:
**`http://127.0.0.1:5000`**

Open `http://127.0.0.1:5000` in any modern web browser to access the CodePulse AI Operations Center.

---

## 8. Automated Test Suite Execution

The application comes with two comprehensive automated test suites covering 104 distinct assertions across frontend, backend, machine learning, database, API, and security domains:

### 1. System Unit Tests (`test_system.py`)
```bash
.\.venv\Scripts\python.exe test_system.py
```
- **Total Tests:** 55
- **Result:** **55 / 55 PASSED (100%)**
- **Coverage:** Feature extraction safety, model loading, continuous probability calibration, database persistence, search filtering, route rendering, RESTful API payloads, and error handlers.

### 2. End-to-End Test Suite (`run_comprehensive_e2e_tests.py`)
```bash
.\.venv\Scripts\python.exe run_comprehensive_e2e_tests.py
```
- **Total Tests:** 49
- **Result:** **49 / 49 PASSED (100%)**
- **Summary Breakdown:**
  - Frontend: 8 / 8 PASS
  - Backend: 16 / 16 PASS
  - Machine Learning: 6 / 6 PASS
  - Database: 6 / 6 PASS
  - API: 5 / 5 PASS
  - Security: 7 / 7 PASS
  - End-to-End Simulation: 1 / 1 PASS

---

## 9. Security & Responsible Disclosure Notice

CodePulse AI evaluates Uniform Resource Locators based entirely on mathematical lexical patterns and structural heuristics. 

- **Offline Inference Safety:** The system never initiates socket connections, DNS resolutions, or HTTP requests to the target domain, eliminating drive-by download risks.
- **Probabilistic Modeling Disclaimer:** Machine learning classifications reflect statistical likelihoods rather than infallible guarantees. Users must remain vigilant, verify digital certificates, and adhere to organizational zero-trust policies.
