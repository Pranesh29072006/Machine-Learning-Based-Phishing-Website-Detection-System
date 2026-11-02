"""
Backward-compatibility proxy for feature_extraction
Re-exports the modularized app.ml.feature_extraction functions and constants.
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

__all__ = [
    "SHORTENING_SERVICES",
    "SENSITIVE_KEYWORDS",
    "FEATURE_NAMES",
    "is_ip",
    "extract_features",
    "get_feature_dict",
    "get_feature_details"
]
