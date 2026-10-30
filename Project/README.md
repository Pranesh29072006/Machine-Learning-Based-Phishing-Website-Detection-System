# Machine Learning Based Phishing Website Detection System

An end-to-end, production-grade cybersecurity web application that inspects Uniform Resource Locators (URLs) and predicts whether a website is **Legitimate / Safe** or **Phishing / Suspicious** using an empirically trained Machine Learning classifier.

---

## 1. Project Overview & Objective

Phishing attacks remain the most prevalent initial access vector for credential theft, session hijacking, and ransomware distribution. Cyber adversaries frequently construct deceptive domain structures, deep nested subdomains, and obfuscated URLs that trick standard users and evade basic keyword filters.

This system provides a proactive defense layer that analyzes URLs **before** a user navigates to them. By converting raw URLs into a standardized **17-dimensional lexical and structural feature vector**, the trained Machine Learning model predicts fraud likelihood, outputs a calibrated confidence score, and provides a security breakdown—all without making destructive outbound HTTP connections to the malicious host.

---

## 2. Technology Stack

- **Backend:** Python 3.11, Flask
- **Machine Learning:** Scikit-learn (Random Forest, Gradient Boosting, Decision Trees, Logistic Regression)
- **Data Engineering:** Pandas, NumPy
- **Model Serialization:** Joblib, JSON
- **Database:** SQLite3 (parameterized queries with auto-indexing)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3
- **Data Visualization:** Chart.js 4.4
- **Icons & Fonts:** Bootstrap Icons, Inter & JetBrains Mono

---

## 3. Key Features

### A. Modern Cybersecurity Dashboard
- Dark charcoal / navy operations-center interface inspired by SOC dashboards.
- URL input field with real-time validation and one-click **Test Sample Pills** (Safe domains, IP address phishing, Subdomain spoofing, Shortened links).
- Four live KPI cards: **Total URLs Analyzed**, **Safe Websites Verified**, **Phishing Threats Flagged**, and **Model Validation Accuracy**.
- Recent scan history preview with one-click direct report inspection.

### B. Intelligent URL Detection Engine
- Extracts 17 lexical, structural, and heuristic features.
- Evaluates targets via the trained ensemble classifier.
- Computes continuous probability and assigns a risk category:
  - **High Risk** (Phishing probability $\ge 85\%$)
  - **Moderate-High Risk** (Phishing probability $50\% - 84\%$)
  - **Low-to-Moderate Risk** (Legitimate probability $50\% - 79\%$)
  - **Low Risk** (Legitimate probability $\ge 80\%$)
- Zero external network requests: non-destructive inspection prevents browser infection.

### C. Comprehensive Machine Learning Pipeline (`train_model.py`)
- Trains on an authentic, balanced dataset of **7,000 real-world URLs**:
  - **Legitimate:** Cisco OpenDNS top domains and University of New Brunswick (UNB) CIC benign dataset.
  - **Phishing:** Verified active phishing URLs from PhishTank and OpenPhish feeds.
- Stratified 80/20 train-test split evaluated on 1,400 unseen URLs.
- Multi-algorithm comparative benchmark:
  - **Random Forest Classifier:** 95.93% Accuracy | 97.49% Precision | 95.86% F1-Score
  - **Gradient Boosting:** 95.79% Accuracy | 97.48% Precision | 95.71% F1-Score
  - **Decision Tree:** 94.71% Accuracy | 97.57% Precision | 94.55% F1-Score
  - **Logistic Regression:** 83.71% Accuracy | 84.91% Precision | 83.43% F1-Score
- **Academic Generalization Verification (GroupShuffleSplit by domain):**
  - **Domain-Disjoint Held-Out Accuracy:** 97.21% | **F1-Score:** 97.55% (tested on 100% disjoint domain names to verify zero domain-level memorization).
- Serializes champion model to `models/phishing_model.joblib` and metrics to `models/model_metrics.json`.

### D. Detailed Scan Result Page (`result.html`)
- High-visibility status indicator (Emerald for Safe, Crimson for Phishing).
- Continuous confidence meter with calibrated certainty percentage.
- Full 17-feature diagnostic inspection table with status badges and threat explanations.
- Prominent cybersecurity advisory and probabilistic modeling disclaimer.

### E. Persistent Scan History (`history.html`)
- SQLite database (`database/scan_history.db`) storing scan records, confidence, risk levels, and timestamps.
- Safe plain-text URL rendering with copy buttons (no automatic redirection or browser opening).
- Full-text search and filtering by domain or prediction status.
- Modal-confirmed **Clear History** functionality.

### F. Model Performance & Evaluation Page (`model_performance.html`)
- Real evaluation metrics: Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
- Full $2 \times 2$ Confusion Matrix visualization with Type I and Type II error explanations.
- Interactive Chart.js comparative multi-algorithm benchmark bar chart.
- Top heuristic feature importance rankings chart.

### G. Threat Architecture & Feature Engineering Guide (`about.html`)
- Educational breakdown of URL phishing attack techniques (subdomain camouflage, shortening cloaking, IP address hosts, `@` redirection).
- Detailed definition and security significance of all 17 extracted features.

---

## 4. The 17 Extracted Heuristic Features

| # | Feature Name | Type | Threat Significance & Adversarial Vector |
|---|--------------|------|------------------------------------------|
| 1 | `url_length` | Numeric | Extremely long URLs (>75 chars) frequently hide malicious redirection tokens or deep directory paths. |
| 2 | `domain_length` | Numeric | Long hostnames (>30 chars) often pad legitimate brand names with descriptive suffixes to mislead users. |
| 3 | `num_dots` | Numeric | Three or more dots in a URL usually indicate multi-level subdomains or disguised hosts. |
| 4 | `num_hyphens` | Numeric | Hyphens in hostnames (e.g. `paypal-security-update.com`) are a trademark spoofing indicator. |
| 5 | `num_digits` | Numeric | High digit counts represent autogenerated hashes, session IDs, or dynamic malware paths. |
| 6 | `has_ip_address` | Binary (0/1) | Direct IPv4/IPv6 hosts (e.g. `http://192.168.1.1/login`) bypass domain registration WHOIS tracking. |
| 7 | `is_https` | Binary (0/1) | Checks protocol encryption. Note: modern phishing pages may also use free TLS certificates. |
| 8 | `has_at_symbol` | Binary (0/1) | RFC standards interpret text before `@` as credentials, routing browsers to the host after the symbol. |
| 9 | `num_suspicious_symbols` | Numeric | Abundance of query delimiters (`?`, `=`, `&`, `%`, `~`, `+`, `$`) used in token transmission. |
| 10 | `num_subdomains` | Numeric | Multiple subdomains (e.g. `login.secure.bank.attacker.com`) conceal the true root domain. |
| 11 | `is_shortened` | Binary (0/1) | Shortening services (`bit.ly`, `tinyurl`, `t.co`) conceal destination domains from human inspection. |
| 12 | `path_length` | Numeric | Deep directory paths indicate embedded credential harvesting landing pages. |
| 13 | `num_query_params` | Numeric | Frequency of query parameters carrying session state or target identification hashes. |
| 14 | `has_sensitive_keywords` | Numeric | Detects high-risk phishing keywords (`login`, `verify`, `account`, `banking`, `secure`, `update`, `signin`). |
| 15 | `has_double_slash_redirect` | Binary (0/1) | Double slashes (`//`) within the URL path component can trigger open-redirect browser behaviors. |
| 16 | `prefix_suffix_hyphen` | Binary (0/1) | Presence of hyphens within the domain portion specifically to mimic legitimate brand names. |
| 17 | `has_tld_in_subdomain` | Binary (0/1) | Deceptive placement of `.com` or `.org` inside subdomains (e.g. `google.com.malicious.net`). |

---

## 5. Project Directory Structure

```
phishing-detection-system/
│
├── app.py                      # Flask backend application with all web & API routes
├── feature_extraction.py       # Standardized 17-feature extraction engine (training & inference)
├── train_model.py              # ML pipeline: data loading, training, evaluation & model persistence
├── test_system.py              # Automated unit and integration test suite
├── requirements.txt            # Python dependencies
├── README.md                   # Complete system documentation and execution guide
├── .gitignore                  # Git ignore rules
│
├── data/
│   ├── download_dataset.py     # Script to fetch Cisco OpenDNS, UNB, PhishTank & OpenPhish datasets
│   └── phishing_dataset.csv    # Balanced labeled dataset (7,000 URLs: 3,500 benign, 3,500 phishing)
│
├── models/
│   ├── phishing_model.joblib   # Trained champion Random Forest classifier artifact
│   └── model_metrics.json      # Empirical evaluation metrics, confusion matrix & feature importances
│
├── database/
│   ├── db.py                   # SQLite helper module (parameterized CRUD operations)
│   └── scan_history.db         # Persistent SQLite scan history database
│
├── templates/
│   ├── base.html               # Master layout with cyber navigation, flash alerts, and footer
│   ├── index.html              # Modern dashboard with scanner input, stats, and quick samples
│   ├── result.html             # Detailed scan verdict, confidence gauge, and 17-feature breakdown
│   ├── history.html            # Scan history table with search filtering and clear history modal
│   ├── model_performance.html  # Model performance metrics, confusion matrix, and comparison charts
│   └── about.html              # Threat architecture and educational feature engineering guide
│
└── static/
    ├── css/
    │   └── style.css           # Custom dark cybersecurity theme styles, glows, and badges
    ├── js/
    │   └── script.js           # Client-side sample auto-fill, loading animation, and Chart.js renderers
    └── images/
        └── logo.svg            # Custom vector cyber shield logo
```

---

## 6. Step-by-Step Installation & Setup (Windows & VS Code)

### Step 1: Open the Project in VS Code
Open VS Code, press `Ctrl + K, Ctrl + O`, and select the project folder (`e:\PROJECT` or your clone directory). Open the integrated PowerShell terminal using `Ctrl + \``.

### Step 2: Create and Activate a Python Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment in PowerShell
.venv\Scripts\Activate.ps1
```
*(If PowerShell displays an Execution Policy restriction, run: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`)*

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Dataset Download (Already Included, Optional Refresh)
The project comes pre-bundled with a verified balanced dataset of 7,000 URLs. To refresh the dataset from live threat feeds:
```powershell
python data/download_dataset.py
```

### Step 5: Train and Evaluate Machine Learning Models
To run feature extraction, train candidate models, evaluate on held-out test data, and serialize the best model:
```powershell
python train_model.py
```
*Output preview:*
```
===========================================================================
MODEL NAME             | ACCURACY   | PRECISION  | RECALL     | F1-SCORE  
===========================================================================
Random Forest          |    96.14% |    97.64% |    94.57% |    96.08%
Logistic Regression    |    83.71% |    84.91% |    82.00% |    83.43%
Decision Tree          |    94.71% |    97.57% |    91.71% |    94.55%
Gradient Boosting      |    95.79% |    97.48% |    94.00% |    95.71%
===========================================================================
[+] Best Performing Model: Random Forest (F1-Score: 96.08%)
[*] Saving best model pipeline to: models/phishing_model.joblib
[+] Evaluation metrics saved to: models/model_metrics.json
```

### Step 6: Run the Automated Test Suite
Verify that all system components, feature extraction, validation, and database operations pass:
```powershell
python test_system.py
```
*(Expected output: `Ran 43 tests in ~1.2s ... OK`)*

### Step 7: Launch the Flask Web Application
```powershell
python app.py
```
Open your web browser and navigate to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 7. Security Best Practices & Defensive Safeguards

1. **Non-Destructive Local Inference:** The system only examines lexical URL strings. It **never** initiates TCP connections, downloads web pages, or renders external scripts from submitted URLs.
2. **Strict Protocol Validation:** Only `http://` and `https://` schemes are processed. Potentially dangerous schemes like `javascript:`, `file:`, `data:`, and `ftp:` are rejected at the input boundary.
3. **Safe Storage & Rendering:** URLs displayed on the Dashboard, Result page, and History log are HTML-escaped by Jinja2 and presented as unlinked text, preventing accidental clicks or stored cross-site scripting (XSS).
4. **Parameterized SQL Queries:** All database interactions with SQLite use parameterized placeholders (`?`) to prevent SQL injection attacks.
5. **Probabilistic Disclaimer:** The interface prominently reminds users that machine learning predictions are probabilistic evaluations, not absolute safety guarantees.

---

## 8. Troubleshooting Guide

- **`ExecutionPolicy` error when activating `.venv`:**  
  Run PowerShell as Administrator or enter:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
- **Port 5000 Already in Use:**  
  In `app.py`, change `app.run(port=5000)` to `app.run(port=5050)` or launch with:
  ```powershell
  flask run --port 5050
  ```
- **"Model not yet loaded or trained" Alert:**  
  Execute `python train_model.py` in your terminal to generate `models/phishing_model.joblib` and `models/model_metrics.json`.

---

## 9. Academic Demonstration Summary

This project was developed as a comprehensive **Computer Science & Engineering (CSE) Capstone / Academic Demonstration**. It showcases the complete lifecycle of an applied Machine Learning cybersecurity solution: threat intelligence collection, lexical feature engineering, model training and comparative benchmarking, SQLite persistence, and a modern, responsive web user interface.

