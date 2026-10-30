"""
Machine Learning Based Phishing Website Detection System
Flask Web Application Backend
"""

import os
import re
import json
from datetime import datetime
from urllib.parse import urlparse

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    abort
)
import joblib
import numpy as np

import feature_extraction as fe
import database.db as db

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-cybersecurity-phishing-detector-key-2026")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_model.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "models", "model_metrics.json")

# Cached model and metrics
_model_pipeline = None
_model_metrics = None


def get_model():
    """Load and cache the trained ML model pipeline."""
    global _model_pipeline
    if _model_pipeline is None:
        if os.path.exists(MODEL_PATH):
            try:
                _model_pipeline = joblib.load(MODEL_PATH)
                app.logger.info(f"Loaded trained ML model from {MODEL_PATH}")
            except Exception as e:
                app.logger.error(f"Error loading model from {MODEL_PATH}: {e}")
                _model_pipeline = None
        else:
            app.logger.warning(f"Model file not found at {MODEL_PATH}")
    return _model_pipeline


def get_metrics():
    """Load cached model evaluation metrics."""
    global _model_metrics
    if _model_metrics is None:
        if os.path.exists(METRICS_PATH):
            try:
                with open(METRICS_PATH, "r") as f:
                    _model_metrics = json.load(f)
            except Exception as e:
                app.logger.error(f"Error loading metrics from {METRICS_PATH}: {e}")
                _model_metrics = None
    return _model_metrics


def validate_url(url_string: str) -> tuple[bool, str, str]:
    """
    Validate user submitted URL.
    Enforces HTTP/HTTPS protocol and basic hostname structure.
    Does NOT make any network connection.
    Returns: (is_valid, sanitized_url, error_message)
    """
    if not url_string or not isinstance(url_string, str):
        return False, "", "Please enter a valid website URL."
    
    # Strip whitespace and dangerous control characters
    sanitized = "".join(ch for ch in url_string.strip() if ch not in "\r\n\t\0")
    if not sanitized:
        return False, "", "Please enter a valid website URL."

    if len(sanitized) > 2048:
        return False, "", "URL exceeds maximum permissible length of 2048 characters."

    # Check for disallowed schemes early (ensuring host:port patterns like 192.168.1.1:8080 are not mistaken for schemes)
    scheme_match = re.match(r"^([a-zA-Z][a-zA-Z0-9\+\.\-]*):", sanitized)
    if scheme_match:
        remainder = sanitized[len(scheme_match.group(0)):]
        if re.match(r"^\d+(/|$)", remainder) and not sanitized.lower().startswith(("http://", "https://")):
            pass  # Host:port pattern without explicit scheme
        else:
            scheme_prefix = scheme_match.group(1).lower()
            if scheme_prefix not in ("http", "https"):
                return False, "", f"Disallowed URL scheme '{scheme_prefix}:'. Only HTTP and HTTPS protocols are supported."

    # Prepend http:// if protocol is omitted to parse correctly
    if not (sanitized.startswith("http://") or sanitized.startswith("https://")):
        sanitized = "http://" + sanitized

    try:
        parsed = urlparse(sanitized)
    except Exception:
        return False, "", "Malformed URL structure."

    if parsed.scheme.lower() not in ("http", "https"):
        return False, "", f"Unsupported protocol '{parsed.scheme}'. Only HTTP and HTTPS are permitted."

    hostname = (parsed.hostname or "").strip()
    if not hostname:
        # Check netloc fallback for malformed patterns
        netloc = (parsed.netloc or "").strip()
        if netloc and not netloc.startswith("/"):
            hostname = netloc.split(":")[0]

    if not hostname:
        return False, "", "URL must contain a valid domain name or IP host address."

    # Check if host is an IPv4 or IPv6 address
    if fe.is_ip(hostname):
        return True, sanitized, ""

    # If domain with port, strip port
    clean_host = hostname.split(":")[0] if ":" in hostname else hostname

    # Domain syntax validation: at least 2 labels, valid DNS characters
    labels = clean_host.split(".")
    if len(labels) < 2:
        return False, "", "Invalid domain format. Domain must contain a valid domain name and TLD."

    for label in labels:
        if not label:
            return False, "", "Invalid domain format: domain labels cannot be empty."
        if not re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$", label):
            return False, "", f"Invalid domain label '{label}'. Domains must contain alphanumeric characters."

    return True, sanitized, ""


def run_prediction(url: str):
    """
    Run URL through feature extraction and trained ML pipeline.
    Returns: dict with prediction result, probability, risk level, and feature details.
    """
    model = get_model()
    if model is None:
        return {
            "success": False,
            "error": "The machine learning model is not yet loaded or trained. Please run 'python train_model.py'."
        }

    try:
        # Extract 17-dimensional feature vector
        features = fe.extract_features(url)
        X = features.reshape(1, -1)

        # Inference
        prediction_num = int(model.predict(X)[0])  # 0 = Legitimate, 1 = Phishing
        
        # Probability confidence score
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X)[0]
            # probabilities[0] is Legitimate, probabilities[1] is Phishing
            phishing_prob = float(probabilities[1])
            legitimate_prob = float(probabilities[0])
        else:
            phishing_prob = 1.0 if prediction_num == 1 else 0.0
            legitimate_prob = 1.0 - phishing_prob
    except Exception as e:
        app.logger.error(f"Inference exception for URL '{url}': {e}")
        return {
            "success": False,
            "error": "A machine learning inference error occurred while evaluating the URL."
        }

    if prediction_num == 1:
        prediction_label = "Phishing"
        confidence = round(phishing_prob * 100, 2)
        if confidence >= 85:
            risk_level = "High Risk"
            risk_color = "danger"
        else:
            risk_level = "Moderate-High Risk"
            risk_color = "warning"
        summary_verdict = (
            "This URL displays prominent heuristic markers and lexical anomalies "
            "frequently associated with credential harvesting, brand impersonation, or phishing attacks."
        )
    else:
        prediction_label = "Legitimate"
        confidence = round(legitimate_prob * 100, 2)
        if confidence >= 80:
            risk_level = "Low Risk"
            risk_color = "success"
        else:
            risk_level = "Low-to-Moderate Risk"
            risk_color = "info"
        summary_verdict = (
            "This URL matches standard domain structures and lexical patterns of benign websites. "
            "However, always inspect SSL certificates and sender identity before providing sensitive information."
        )

    # Feature details for display
    feature_details = fe.get_feature_details(url)
    
    # Save to SQLite database
    scan_id = db.save_scan(
        url=url,
        prediction=prediction_label,
        confidence=confidence,
        risk_level=risk_level
    )

    return {
        "success": True,
        "scan_id": scan_id,
        "url": url,
        "prediction": prediction_label,
        "confidence": confidence,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "summary": summary_verdict,
        "feature_details": feature_details,
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# =========================================================================
# APPLICATION ROUTES
# =========================================================================

@app.route("/")
def index():
    """Dashboard home view."""
    stats = db.get_scan_stats()
    recent_scans = db.get_recent_scans(limit=8)
    model = get_model()
    metrics = get_metrics()
    model_ready = model is not None
    
    return render_template(
        "index.html",
        stats=stats,
        recent_scans=recent_scans,
        model_ready=model_ready,
        metrics=metrics
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    """Form submission endpoint for URL analysis."""
    url_input = request.form.get("url", "")
    is_valid, sanitized_url, error_msg = validate_url(url_input)
    
    if not is_valid:
        flash(error_msg, "danger")
        return redirect(url_for("index"))

    result = run_prediction(sanitized_url)
    if not result.get("success"):
        flash(result.get("error", "An unexpected analysis error occurred."), "danger")
        return redirect(url_for("index"))

    return render_template("result.html", result=result)


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """JSON API endpoint for AJAX URL analysis with interactive frontend."""
    # Ensure request payload is present and valid
    if request.is_json:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"success": False, "error": "Invalid JSON format. Expected an object with 'url' key."}), 400
        url_input = data.get("url", "")
    elif request.form:
        url_input = request.form.get("url", "")
    else:
        return jsonify({"success": False, "error": "Missing request payload. Please supply 'url'."}), 400
    
    is_valid, sanitized_url, error_msg = validate_url(url_input)
    if not is_valid:
        return jsonify({"success": False, "error": error_msg}), 400

    result = run_prediction(sanitized_url)
    if not result.get("success"):
        return jsonify({"success": False, "error": result.get("error")}), 500

    return jsonify(result)


@app.route("/result/<int:scan_id>")
def view_result(scan_id):
    """View a past scan result by scan ID."""
    scan = db.get_scan_by_id(scan_id)
    if not scan:
        flash("Scan record not found.", "warning")
        return redirect(url_for("history"))
        
    # Reconstruct feature details from URL
    feature_details = fe.get_feature_details(scan["url"])
    is_phish = scan["prediction"] == "Phishing"
    risk_color = "danger" if is_phish else "success"
    
    result = {
        "success": True,
        "scan_id": scan["id"],
        "url": scan["url"],
        "prediction": scan["prediction"],
        "confidence": scan["confidence"],
        "risk_level": scan["risk_level"],
        "risk_color": risk_color,
        "summary": (
            "Analyzed from stored scan record. Note that live site state can change over time."
        ),
        "feature_details": feature_details,
        "analyzed_at": scan["created_at"]
    }
    return render_template("result.html", result=result)


@app.route("/history")
def history():
    """Full scan history log view."""
    search_query = request.args.get("q", "").strip()
    scans = db.get_all_scans(search_query=search_query, limit=200)
    stats = db.get_scan_stats()
    return render_template(
        "history.html",
        scans=scans,
        search_query=search_query,
        stats=stats
    )


@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear all records from SQLite scan history."""
    db.clear_history()
    flash("Scan history has been successfully cleared.", "info")
    return redirect(url_for("history"))


@app.route("/model-performance")
def model_performance():
    """Display real ML metrics, confusion matrix, and feature importances."""
    metrics = get_metrics()
    if not metrics:
        flash("Model metrics are not available. Please train the model using 'python train_model.py'.", "warning")
        return render_template("model_performance.html", metrics=None)

    return render_template("model_performance.html", metrics=metrics)


@app.route("/about")
def about():
    """Educational page detailing phishing techniques and feature engineering."""
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("base.html", error_title="404 - Not Found", error_message="The requested page could not be located."), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("base.html", error_title="500 - Server Error", error_message="An internal server error occurred."), 500


if __name__ == "__main__":
    # Ensure database is set up
    db.init_db()
    # Configure debug mode via environment variable (defaults to False for production safety)
    debug_mode = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true")
    # Run server
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
