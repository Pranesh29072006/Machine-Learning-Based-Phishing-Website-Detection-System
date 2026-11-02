"""
Feature Service Module
Provides feature extraction interfaces, feature schemas, and diagnostic mappings.
"""

from typing import Dict, Any, List
import numpy as np

from app.ml.feature_extraction import (
    FEATURE_NAMES,
    extract_features,
    get_feature_dict,
    get_feature_details
)


def get_url_feature_vector(url: str) -> np.ndarray:
    """Extract standard 17-dimensional numpy feature array."""
    return extract_features(url)


def get_url_feature_map(url: str) -> Dict[str, float]:
    """Extract named feature dictionary."""
    return get_feature_dict(url)


def get_url_feature_report(url: str) -> List[Dict[str, Any]]:
    """Extract full human-readable feature diagnostics."""
    return get_feature_details(url)


def get_feature_schema() -> List[str]:
    """Return ordered list of 17 supported feature identifiers."""
    return list(FEATURE_NAMES)

