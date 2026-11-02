"""
Threat Analytics & Telemetry Blueprint
Provides interactive charts, historical distribution metrics, and API endpoints.
"""

from flask import Blueprint, render_template, jsonify

from app.services.analytics_service import get_telemetry_report, get_dashboard_kpis
from app.ml.model_loader import get_metrics

analytics_bp = Blueprint("analytics_bp", __name__)


@analytics_bp.route("/analytics")
def analytics():
    """Interactive Threat Analytics view with real scan history distributions."""
    analytics_data = get_telemetry_report()
    stats = get_dashboard_kpis()
    metrics = get_metrics()
    return render_template(
        "analytics.html",
        analytics=analytics_data,
        stats=stats,
        metrics=metrics
    )


@analytics_bp.route("/api/stats")
def api_stats():
    """Return live system statistics in JSON format."""
    stats = get_dashboard_kpis()
    return jsonify({"success": True, "stats": stats})


@analytics_bp.route("/api/analytics")
def api_analytics():
    """Return comprehensive aggregated scan analytics in JSON format for charts."""
    summary = get_telemetry_report()
    return jsonify({"success": True, "analytics": summary})

