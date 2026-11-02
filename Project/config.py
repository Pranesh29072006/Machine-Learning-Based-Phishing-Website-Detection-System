"""
CodePulse AI - Centralized Application Configuration
Provides environment-aware settings, paths, and operational constants.
"""

import os
from pathlib import Path

# Base project directory (E:\PROJECT)
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "super-secret-cybersecurity-codepulse-ai-key-2026")
    DEBUG = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true")
    TESTING = False

    # Server binding
    HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
    PORT = int(os.environ.get("FLASK_PORT", 5000))

    # Core Directories
    APP_DIR = BASE_DIR / "app"
    TEMPLATES_DIR = BASE_DIR / "templates"
    STATIC_DIR = BASE_DIR / "static"
    MODELS_DIR = BASE_DIR / "models"
    DATA_DIR = BASE_DIR / "data"
    DATABASE_DIR = BASE_DIR / "database"

    # ML Model & Metrics Paths
    MODEL_PATH = os.environ.get("MODEL_PATH", str(MODELS_DIR / "phishing_model.joblib"))
    METRICS_PATH = os.environ.get("METRICS_PATH", str(MODELS_DIR / "model_metrics.json"))

    # SQLite Database Path
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(DATABASE_DIR / "scan_history.db"))

    # Security & Validation Thresholds
    MAX_URL_LENGTH = 2048
    NUM_FEATURES = 17
    
    # Classification Confidence Thresholds
    PHISHING_HIGH_RISK_THRESHOLD = 85.0
    LEGITIMATE_LOW_RISK_THRESHOLD = 80.0

    # Application Identity
    APP_NAME = "CodePulse AI"
    APP_TAGLINE = "Intelligent Phishing Website Detection System"
    APP_VERSION = "2.5.0"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration with isolated in-memory or temporary database."""
    TESTING = True
    DEBUG = False
    DATABASE_PATH = str(BASE_DIR / "database" / "test_scan_history.db")


class ProductionConfig(Config):
    """Production configuration with strict security defaults."""
    DEBUG = False


# Map configuration environments
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": Config
}

def get_config():
    """Retrieve active configuration based on FLASK_ENV or default."""
    env = os.environ.get("FLASK_ENV", "default").lower()
    return config_by_name.get(env, Config)

