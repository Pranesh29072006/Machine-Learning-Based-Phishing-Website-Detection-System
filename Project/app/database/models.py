"""
Database Schema & Data Model Definitions
Provides typed dataclasses for scan audits, telemetry, and pagination records.
"""

from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


@dataclass
class ScanRecord:
    """Represents a single evaluated URL scan record."""
    id: Optional[int]
    url: str
    prediction: str
    confidence: float
    risk_level: str
    processing_time_ms: float = 0.0
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary."""
        return asdict(self)


@dataclass
class ScanStats:
    """Aggregate statistics of all historical scan audits."""
    total: int = 0
    legitimate: int = 0
    phishing: int = 0
    detection_rate: float = 0.0
    safe_percentage: float = 0.0
    avg_processing_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert statistics to dictionary."""
        return asdict(self)

