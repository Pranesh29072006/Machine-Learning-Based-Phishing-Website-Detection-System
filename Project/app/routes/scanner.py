"""
URL Threat Scanner & Analysis Blueprint
Handles interactive threat scanning, JSON API evaluation, and historical scan inspection.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from app.utils.validators import validate_url
from app.services.prediction_service import process_url_scan, get_historical_scan_report
from app.services.analytics_service import get_dashboard_kpis
from app.ml.model_loader import get_model

scanner_bp = Blueprint("scanner_bp", __name__)


@scanner_bp.route("/scanner")
def scanner():
    """Dedicated interactive URL Scanner console."""
    model = get_model()
    model_ready = model is not None
    stats = get_dashboard_kpis()
    prefill_url = request.args.get("url", "").strip()
    return render_template(
        "scanner.html",
        model_ready=model_ready,
        stats=stats,
        prefill_url=prefill_url
    )


@scanner_bp.route("/analyze", methods=["POST"])
def analyze():
    """Form submission endpoint for interactive URL threat analysis."""
    url_input = request.form.get("url", "")
    is_valid, sanitized_url, error_msg = validate_url(url_input)

    if not is_valid:
        flash(error_msg, "danger")
        return redirect(url_for("scanner", url=url_input))

    result = process_url_scan(sanitized_url)
    if not result.get("success"):
        flash(result.get("error", "An unexpected analysis error occurred."), "danger")
        return redirect(url_for("scanner", url=url_input))

    return render_template("result.html", result=result)


@scanner_bp.route("/api/analyze", methods=["POST"])
@scanner_bp.route("/api/scan", methods=["POST"], endpoint="api_scan")
def api_analyze():
    """JSON API endpoint for AJAX URL threat inspection."""
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

    result = process_url_scan(sanitized_url)
    if not result.get("success"):
        return jsonify({"success": False, "error": result.get("error")}), 500

    return jsonify(result)


@scanner_bp.route("/result/<int:scan_id>")
def view_result(scan_id: int):
    """View an individual historical scan report by ID."""
    result = get_historical_scan_report(scan_id)
    if not result:
        flash("Scan record not found.", "warning")
        return redirect(url_for("history"))

    return render_template("result.html", result=result)

