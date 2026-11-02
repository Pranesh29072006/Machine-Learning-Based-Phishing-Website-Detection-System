"""
CodePulse AI - Intelligent Phishing Website Detection System
Main Application Entrypoint & WSGI Gateway
"""

import os
from config import get_config
from app import create_app
from app.utils.validators import validate_url
from app.services.prediction_service import process_url_scan as run_prediction
from app.ml.model_loader import get_model, get_metrics

# Initialize WSGI application instance
app = create_app()

__all__ = [
    "app",
    "create_app",
    "validate_url",
    "run_prediction",
    "get_model",
    "get_metrics"
]

if __name__ == "__main__":
    config = get_config()
    print(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    print(f"Operations Console available at: http://{config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
