"""
Model Performance & System Documentation Blueprint
Provides empirical ML benchmark evaluation, security attack vector insights,
settings configuration, and system documentation.
"""

from flask import Blueprint, render_template, flash

from app.ml.model_loader import get_metrics, get_model
from app.services.analytics_service import get_system_diagnostics

model_performance_bp = Blueprint("model_performance_bp", __name__)


@model_performance_bp.route("/model-performance")
def model_performance():
    """Display real ML metrics, confusion matrix, ROC curve, and feature importances."""
    metrics = get_metrics()
    if not metrics:
        flash("Model metrics are not available. Please train the model using 'python train_model.py'.", "warning")
        return render_template("model_performance.html", metrics=None)

    return render_template("model_performance.html", metrics=metrics)


@model_performance_bp.route("/security-insights")
def security_insights():
    """Educational knowledge base explaining URL phishing heuristics and attack patterns."""
    return render_template("security_insights.html")


@model_performance_bp.route("/settings")
def settings():
    """Platform settings, UI display preferences, and system diagnostics."""
    db_info = get_system_diagnostics()
    metrics = get_metrics()
    model = get_model()
    return render_template(
        "settings.html",
        db_info=db_info,
        metrics=metrics,
        model_online=model is not None
    )


@model_performance_bp.route("/about")
def about():
    """Enterprise platform documentation and system architecture guide."""
    return render_template("about.html")

