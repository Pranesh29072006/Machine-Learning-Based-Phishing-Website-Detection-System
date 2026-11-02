"""
Machine Learning Model & Metrics Loader Module
Manages model deserialization, caching, and fallback handling.
"""

import os
import json
import logging
from typing import Optional, Any, Dict
import joblib

from config import Config

logger = logging.getLogger("codepulse.ml.loader")

_model_pipeline: Optional[Any] = None
_model_metrics: Optional[Dict[str, Any]] = None


def get_model(model_path: Optional[str] = None) -> Optional[Any]:
    """Load and cache the trained Scikit-Learn Random Forest model pipeline."""
    global _model_pipeline

    # Check if app module has explicitly configured or overridden _model_pipeline or MODEL_PATH
    try:
        import app as app_pkg
        if hasattr(app_pkg, "_model_pipeline"):
            if app_pkg._model_pipeline is not None:
                return app_pkg._model_pipeline
            else:
                _model_pipeline = None
        if hasattr(app_pkg, "MODEL_PATH"):
            model_path = app_pkg.MODEL_PATH
    except Exception:
        pass

    path = model_path or Config.MODEL_PATH
    if _model_pipeline is None:
        if os.path.exists(path):
            try:
                _model_pipeline = joblib.load(path)
                logger.info(f"Loaded trained ML model from {path}")
            except Exception as e:
                logger.error(f"Error loading model from {path}: {e}")
                _model_pipeline = None
        else:
            logger.warning(f"Model file not found at {path}")
            _model_pipeline = None
    return _model_pipeline


def set_model(model: Optional[Any]) -> None:
    """Manually set or reset the active cached model pipeline (useful for testing)."""
    global _model_pipeline
    _model_pipeline = model


def get_metrics(metrics_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Load and cache empirical model evaluation metrics."""
    global _model_metrics
    path = metrics_path or Config.METRICS_PATH
    if _model_metrics is None:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    _model_metrics = json.load(f)
                logger.info(f"Loaded evaluation metrics from {path}")
            except Exception as e:
                logger.error(f"Error loading metrics from {path}: {e}")
                _model_metrics = None
        else:
            logger.warning(f"Metrics file not found at {path}")
    return _model_metrics


def set_metrics(metrics: Optional[Dict[str, Any]]) -> None:
    """Manually set or reset cached evaluation metrics (useful for testing)."""
    global _model_metrics
    _model_metrics = metrics
