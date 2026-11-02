"""
Routes Subpackage
Provides modular route blueprints for all application operational consoles.
"""

from app.routes.dashboard import dashboard_bp
from app.routes.scanner import scanner_bp
from app.routes.history import history_bp
from app.routes.analytics import analytics_bp
from app.routes.model_performance import model_performance_bp

all_blueprints = [
    dashboard_bp,
    scanner_bp,
    history_bp,
    analytics_bp,
    model_performance_bp
]

__all__ = [
    "dashboard_bp",
    "scanner_bp",
    "history_bp",
    "analytics_bp",
    "model_performance_bp",
    "all_blueprints"
]

