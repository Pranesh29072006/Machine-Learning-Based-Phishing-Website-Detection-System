"""
Prediction Service Module
Coordinates validation, feature extraction, ML classification, and database persistence.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from app.ml.predictor import classify_url
from app.ml.model_loader import get_model
from app.database.operations import save_scan, get_scan_by_id
from app.ml.feature_extraction import get_feature_details
from app.utils.helpers import format_timestamp


def process_url_scan(url: str, persist: bool = True, model: Any = None) -> Dict[str, Any]:
    """
    Execute complete end-to-end URL threat analysis:
    1. Feature extraction and model classification.
    2. Execution time latency profiling.
    3. SQLite audit persistence (optional, default True).
    4. Structured payload formatting.
    """
    # Dynamically resolve model to respect test patches on app.get_model or app._model_pipeline
    if model is None:
        try:
            import app as app_pkg
            if getattr(app_pkg, "_model_pipeline", None) is not None:
                model = app_pkg._model_pipeline
            elif hasattr(app_pkg, "get_model"):
                target_path = getattr(app_pkg, "MODEL_PATH", None)
                model = app_pkg.get_model(target_path)
            else:
                model = get_model()
        except Exception:
            model = get_model()

    if model is None:
        return {
            "success": False,
            "error": "The machine learning model is not yet loaded or trained. Please run 'python train_model.py'."
        }

    # Run classification
    result = classify_url(url, model=model)
    if not result.get("success"):
        return result

    scan_id: Optional[int] = None
    if persist:
        # Save to SQLite database
        scan_id = save_scan(
            url=url,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            processing_time_ms=result["processing_time_ms"]
        )

    return {
        "success": True,
        "scan_id": scan_id,
        "url": url,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "risk_level": result["risk_level"],
        "risk_color": result["risk_color"],
        "summary": result["summary"],
        "feature_details": result["feature_details"],
        "processing_time_ms": result["processing_time_ms"],
        "analyzed_at": format_timestamp()
    }


def get_historical_scan_report(scan_id: int) -> Optional[Dict[str, Any]]:
    """
    Reconstruct full scan analysis report from saved SQLite record.
    """
    scan = get_scan_by_id(scan_id)
    if not scan:
        return None

    feature_details = get_feature_details(scan["url"])
    is_phish = scan["prediction"] == "Phishing"
    risk_level = scan.get("risk_level", "High Risk" if is_phish else "Low Risk")
    
    if is_phish:
        risk_color = "danger" if "Moderate" not in risk_level else "warning"
        summary_verdict = (
            "Analyzed from stored audit record. This URL displayed heuristic markers and lexical anomalies "
            "frequently associated with credential harvesting, brand impersonation, or phishing attacks."
        )
    else:
        risk_color = "success" if "Moderate" not in risk_level else "info"
        summary_verdict = (
            "Analyzed from stored audit record. This URL conformed to standard domain structures and lexical patterns "
            "of benign websites. Always inspect SSL certificates and sender identity before providing sensitive data."
        )
        
    latency = round(float(scan["processing_time_ms"]) if scan["processing_time_ms"] is not None else 0.0, 2)

    return {
        "success": True,
        "scan_id": scan["id"],
        "url": scan["url"],
        "prediction": scan["prediction"],
        "confidence": scan["confidence"],
        "risk_level": risk_level,
        "risk_color": risk_color,
        "processing_time_ms": latency,
        "summary": summary_verdict,
        "feature_details": feature_details,
        "analyzed_at": scan["created_at"]
    }
