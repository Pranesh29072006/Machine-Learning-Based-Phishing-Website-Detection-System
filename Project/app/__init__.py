"""
CodePulse AI - Application Factory Package
Configures the Flask WSGI app, Jinja template resolution, blueprints, and security filters.
"""

import os
from typing import Optional, Type
from flask import Flask, render_template, url_for
from jinja2 import ChoiceLoader, FileSystemLoader

from config import Config, get_config
from app.database.connection import init_db
from app.services.analytics_service import get_dashboard_kpis, get_recent_activity
from app.ml.model_loader import get_model, get_metrics
from app.routes import all_blueprints


def create_app(config_class: Optional[Type[Config]] = None) -> Flask:
    """
    Application Factory Pattern for CodePulse AI.
    Constructs and configures the Flask application instance.
    """
    config_obj = config_class or get_config()

    app = Flask(
        __name__,
        template_folder=str(config_obj.TEMPLATES_DIR),
        static_folder=str(config_obj.STATIC_DIR)
    )

    # Apply configuration
    app.config.from_object(config_obj)

    # Configure flexible Jinja template discovery across root and category subdirectories
    template_dir = str(config_obj.TEMPLATES_DIR)
    subdirs = ["dashboard", "scanner", "history", "analytics", "components"]
    loaders = [FileSystemLoader(template_dir)]
    for sub in subdirs:
        sub_path = os.path.join(template_dir, sub)
        if os.path.exists(sub_path):
            loaders.append(FileSystemLoader(sub_path))
    app.jinja_loader = ChoiceLoader(loaders)

    # Global Context Processor
    @app.context_processor
    def inject_global_context():
        """Inject global system telemetry and model health status across all templates."""
        return {
            "app_name": config_obj.APP_NAME,
            "app_tagline": config_obj.APP_TAGLINE,
            "app_version": config_obj.APP_VERSION,
            "global_stats": get_dashboard_kpis(),
            "recent_events": get_recent_activity(limit=5),
            "model_online": get_model() is not None,
            "global_metrics": get_metrics()
        }

    # Defensive HTTP Security Headers
    @app.after_request
    def set_security_headers(response):
        """Enforce standard defensive HTTP headers."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    # Global HTTP Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html"), 500

    # Register Route Blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    # Transparent Endpoint Resolution (supports both url_for('scanner') and url_for('scanner_bp.scanner'))
    def resolve_unprefixed_endpoint(error, endpoint, values):
        for bp_instance in all_blueprints:
            candidate = f"{bp_instance.name}.{endpoint}"
            if candidate in app.view_functions:
                return url_for(candidate, **values)
        raise error

    app.url_build_error_handlers.append(resolve_unprefixed_endpoint)

    # Initialize SQLite database schema
    with app.app_context():
        init_db()

    return app


# Default application instance for WSGI, CLI, and test suites
app = create_app()

# Backward-compatible convenience imports & test introspection hooks
from config import Config
import app.ml.model_loader as model_loader
from app.utils.validators import validate_url
from app.services.prediction_service import process_url_scan as run_prediction
from app.ml.model_loader import get_model, get_metrics

MODEL_PATH = Config.MODEL_PATH
METRICS_PATH = Config.METRICS_PATH
_model_pipeline = model_loader._model_pipeline
_model_metrics = model_loader._model_metrics

__all__ = [
    "create_app",
    "app",
    "validate_url",
    "run_prediction",
    "get_model",
    "get_metrics",
    "MODEL_PATH",
    "METRICS_PATH",
    "_model_pipeline",
    "_model_metrics"
]
