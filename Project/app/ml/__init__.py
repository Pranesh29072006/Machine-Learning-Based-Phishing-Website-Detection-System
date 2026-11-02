"""
Machine Learning Subpackage
Provides model loading, feature extraction, and prediction engines.
"""

from app.ml.feature_extraction import (
    SHORTENING_SERVICES,
    SENSITIVE_KEYWORDS,
    FEATURE_NAMES,
    is_ip,
    extract_features,
    get_feature_dict,
    get_feature_details
)

from app.ml.model_loader import (
    get_model,
    set_model,
    get_metrics,
    set_metrics
)

from app.ml.predictor import (
    classify_url
)

__all__ = [
    "SHORTENING_SERVICES",
    "SENSITIVE_KEYWORDS",
    "FEATURE_NAMES",
    "is_ip",
    "extract_features",
    "get_feature_dict",
    "get_feature_details",
    "get_model",
    "set_model",
    "get_metrics",
    "set_metrics",
    "classify_url"
]

