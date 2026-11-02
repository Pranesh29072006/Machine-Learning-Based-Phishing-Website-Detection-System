"""
Dashboard & Operations Overview Route Blueprint
Provides the main overview console, KPI telemetry summary, and quick scanner entry point.
"""

from flask import Blueprint, render_template

from app.services.analytics_service import get_dashboard_kpis, get_recent_activity, get_telemetry_report
from app.ml.model_loader import get_model, get_metrics

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/overview", endpoint="overview")
@dashboard_bp.route("/dashboard", endpoint="dashboard")
def index():
    """Overview dashboard view with metrics, charts, and activity summary."""
    stats = get_dashboard_kpis()
    recent_scans = get_recent_activity(limit=8)
    analytics = get_telemetry_report()
    model = get_model()
    metrics = get_metrics()
    model_ready = model is not None

    return render_template(
        "index.html",
        stats=stats,
        recent_scans=recent_scans,
        analytics=analytics,
        model_ready=model_ready,
        metrics=metrics
    )

