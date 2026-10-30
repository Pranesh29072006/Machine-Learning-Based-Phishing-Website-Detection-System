"""
Machine Learning Training Pipeline for Phishing Website Detection System.

This script:
1. Loads the labeled dataset from data/phishing_dataset.csv.
2. Extracts lexical and structural URL features via feature_extraction.py.
3. Performs an 80/20 stratified train-test split.
4. Trains and evaluates multiple ML algorithms:
   - Random Forest Classifier
   - Logistic Regression
   - Decision Tree Classifier
   - Gradient Boosting Classifier
5. Measures test Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
6. Saves the best performing model to models/phishing_model.joblib.
7. Saves comprehensive evaluation metrics to models/model_metrics.json for the UI dashboard.
"""

import os
import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import joblib

from urllib.parse import urlparse
import shutil

from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

import feature_extraction as fe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "phishing_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
BEST_MODEL_PATH = os.path.join(MODEL_DIR, "phishing_model.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")


def load_dataset():
    """Load and validate the dataset."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Please run 'python data/download_dataset.py' to generate or download the dataset."
        )
    print(f"[*] Reading dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    if 'url' not in df.columns or 'label' not in df.columns:
        raise ValueError("Dataset must contain 'url' and 'label' columns.")
    
    # Drop empty or null entries
    df = df.dropna(subset=['url', 'label'])
    df['label'] = df['label'].astype(int)
    print(f"[+] Loaded {len(df)} samples ({sum(df['label'] == 0)} legitimate, {sum(df['label'] == 1)} phishing).")
    return df


def extract_all_features(df):
    """Extract features for all URLs using the standardized feature extractor."""
    print(f"[*] Extracting {len(fe.FEATURE_NAMES)} features from {len(df)} URLs...")
    start_time = time.time()
    feature_matrix = []
    
    for url in df['url']:
        vec = fe.extract_features(url)
        feature_matrix.append(vec)
        
    X = np.array(feature_matrix)
    y = df['label'].values
    elapsed = time.time() - start_time
    print(f"[+] Feature extraction completed in {elapsed:.2f} seconds. Feature shape: {X.shape}")
    return X, y


def train_and_evaluate():
    """Run full training, evaluation, comparison, and persistence."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    df = load_dataset()
    X, y = extract_all_features(df)
    
    # 80/20 Stratified Split
    print("[*] Splitting dataset: 80% Training, 20% Testing (Stratified)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[+] Training samples: {len(X_train)} | Testing samples: {len(X_test)}")
    
    # Candidate models to evaluate
    candidate_models = {
        "Random Forest": Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(n_estimators=100, max_depth=16, random_state=42, n_jobs=-1))
        ]),
        "Logistic Regression": Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', LogisticRegression(max_iter=1000, random_state=42))
        ]),
        "Decision Tree": Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', DecisionTreeClassifier(max_depth=12, random_state=42))
        ]),
        "Gradient Boosting": Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42))
        ])
    }
    
    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_pipeline = None
    
    print("\n" + "=" * 75)
    print(f"{'MODEL NAME':<22} | {'ACCURACY':<10} | {'PRECISION':<10} | {'RECALL':<10} | {'F1-SCORE':<10}")
    print("=" * 75)
    
    for name, pipeline in candidate_models.items():
        # Train
        pipeline.fit(X_train, y_train)
        
        # Predict on held-out test data
        y_pred = pipeline.predict(X_test)
        if hasattr(pipeline, "predict_proba"):
            y_proba = pipeline.predict_proba(X_test)[:, 1]
            auc_val = float(roc_auc_score(y_test, y_proba))
        else:
            auc_val = 0.0
            
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        cm = confusion_matrix(y_test, y_pred).tolist()  # [[TN, FP], [FN, TP]]
        
        print(f"{name:<22} | {acc * 100:>8.2f}% | {prec * 100:>8.2f}% | {rec * 100:>8.2f}% | {f1 * 100:>8.2f}%")
        
        results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(auc_val, 4),
            "confusion_matrix": cm,
            "classification_report": classification_report(y_test, y_pred, output_dict=True)
        }
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipeline
            
    print("=" * 75)
    print(f"[+] Best Performing Model: {best_model_name} (F1-Score: {best_f1 * 100:.2f}%)")
    
    # Feature Importances (from classifier if available)
    feature_importances = []
    clf = best_pipeline.named_steps['classifier']
    if hasattr(clf, 'feature_importances_'):
        importances = clf.feature_importances_
        sorted_indices = np.argsort(importances)[::-1]
        for idx in sorted_indices:
            feature_importances.append({
                "feature": fe.FEATURE_NAMES[idx],
                "importance": round(float(importances[idx]), 4)
            })
    elif hasattr(clf, 'coef_'):
        coefs = np.abs(clf.coef_[0])
        sorted_indices = np.argsort(coefs)[::-1]
        for idx in sorted_indices:
            feature_importances.append({
                "feature": fe.FEATURE_NAMES[idx],
                "importance": round(float(coefs[idx]), 4)
            })
            
    # Domain-Disjoint Evaluation (Zero Domain Overlap between Train and Test)
    print("\n[*] Running Domain-Disjoint Evaluation (GroupShuffleSplit by domain)...")
    def get_url_domain(u):
        norm = fe.normalize_url(u)
        try:
            p = urlparse(norm)
            return (p.hostname or p.netloc or "").lower()
        except Exception:
            return "unknown"

    domains = df['url'].apply(get_url_domain).values
    gss = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
    grp_train_idx, grp_test_idx = next(gss.split(X, y, groups=domains))
    
    # Train champion architecture on domain-disjoint split
    clf_class = best_pipeline.named_steps['classifier'].__class__
    disjoint_pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', clf_class(**best_pipeline.named_steps['classifier'].get_params()))
    ])
    disjoint_pipe.fit(X[grp_train_idx], y[grp_train_idx])
    y_disjoint_pred = disjoint_pipe.predict(X[grp_test_idx])
    
    disjoint_metrics = {
        "train_samples": int(len(grp_train_idx)),
        "test_samples": int(len(grp_test_idx)),
        "accuracy": round(float(accuracy_score(y[grp_test_idx], y_disjoint_pred)), 4),
        "precision": round(float(precision_score(y[grp_test_idx], y_disjoint_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y[grp_test_idx], y_disjoint_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y[grp_test_idx], y_disjoint_pred, zero_division=0)), 4),
        "confusion_matrix": confusion_matrix(y[grp_test_idx], y_disjoint_pred).tolist()
    }
    print(f"[+] Domain-Disjoint Held-Out Accuracy: {disjoint_metrics['accuracy'] * 100:.2f}% | F1: {disjoint_metrics['f1_score'] * 100:.2f}%")

    # Backup existing model if present
    if os.path.exists(BEST_MODEL_PATH):
        backup_path = BEST_MODEL_PATH + ".bak"
        shutil.copy2(BEST_MODEL_PATH, backup_path)
        print(f"[*] Created backup of existing model at: {backup_path}")

    # Persist the Best Model
    print(f"[*] Saving best model pipeline to: {BEST_MODEL_PATH}")
    joblib.dump(best_pipeline, BEST_MODEL_PATH)
    
    # Structure comprehensive metrics artifact
    best_metrics = results[best_model_name]
    metrics_payload = {
        "model_name": best_model_name,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "accuracy": best_metrics["accuracy"],
        "precision": best_metrics["precision"],
        "recall": best_metrics["recall"],
        "f1_score": best_metrics["f1_score"],
        "roc_auc": best_metrics["roc_auc"],
        "confusion_matrix": best_metrics["confusion_matrix"],
        "domain_disjoint_evaluation": disjoint_metrics,
        "feature_importances": feature_importances,
        "model_comparison": results,
        "feature_names": fe.FEATURE_NAMES
    }
    
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_payload, f, indent=4)
    print(f"[+] Evaluation metrics saved to: {METRICS_PATH}")
    print("[SUCCESS] Model training and evaluation successfully completed.")
    return metrics_payload


if __name__ == "__main__":
    train_and_evaluate()

