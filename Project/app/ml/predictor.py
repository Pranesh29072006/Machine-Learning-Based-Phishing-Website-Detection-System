"""
Machine Learning Predictor Module
Evaluates feature vectors against trained models to determine fraud classification,
probability certainty, risk tiers, and verdict rationales.
"""

import time
import logging
from typing import Dict, Any, Tuple
import numpy as np

from app.ml.model_loader import get_model
from app.ml.feature_extraction import extract_features, get_feature_details
from config import Config

logger = logging.getLogger("codepulse.ml.predictor")


def classify_url(url: str, model: Any = None) -> Dict[str, Any]:
    """
    Execute feature extraction and machine learning classification for a URL.
    Returns: dictionary with classification metrics, feature vector, latency, and status.
    """
    clf = model if model is not None else get_model()
    if clf is None:
        return {
            "success": False,
            "error": "The machine learning model is not yet loaded or trained. Please run 'python train_model.py'."
        }

    t_start = time.perf_counter()
    try:
        # Extract standardized 17-dimensional feature vector
        features = extract_features(url)
        X = features.reshape(1, -1)

        # Inference
        prediction_num = int(clf.predict(X)[0])  # 0 = Legitimate, 1 = Phishing

        # Probability scoring
        if hasattr(clf, "predict_proba"):
            probabilities = clf.predict_proba(X)[0]
            phishing_prob = float(probabilities[1])
            legitimate_prob = float(probabilities[0])
        else:
            phishing_prob = 1.0 if prediction_num == 1 else 0.0
            legitimate_prob = 1.0 - phishing_prob
    except Exception as e:
        logger.error(f"Inference exception for URL '{url}': {e}")
        return {
            "success": False,
            "error": "A machine learning inference error occurred while evaluating the URL."
        }

    elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)

    # Risk level categorization
    if prediction_num == 1:
        prediction_label = "Phishing"
        confidence = round(phishing_prob * 100, 2)
        if confidence >= Config.PHISHING_HIGH_RISK_THRESHOLD:
            risk_level = "High Risk"
            risk_color = "danger"
        else:
            risk_level = "Moderate-High Risk"
            risk_color = "warning"
        summary_verdict = (
            "This URL displays prominent heuristic markers and lexical anomalies "
            "frequently associated with credential harvesting, brand impersonation, or phishing attacks."
        )
    else:
        prediction_label = "Legitimate"
        confidence = round(legitimate_prob * 100, 2)
        if confidence >= Config.LEGITIMATE_LOW_RISK_THRESHOLD:
            risk_level = "Low Risk"
            risk_color = "success"
        else:
            risk_level = "Low-to-Moderate Risk"
            risk_color = "info"
        summary_verdict = (
            "This URL matches standard domain structures and lexical patterns of benign websites. "
            "However, always inspect SSL certificates and sender identity before providing sensitive information."
        )

    # Detailed vector implications
    feature_details = get_feature_details(url)

    return {
        "success": True,
        "url": url,
        "prediction": prediction_label,
        "confidence": confidence,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "summary": summary_verdict,
        "feature_details": feature_details,
        "processing_time_ms": elapsed_ms
    }
