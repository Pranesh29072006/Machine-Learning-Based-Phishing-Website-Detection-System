"""
Shared Helper Utilities
Provides date formatting, response wrapping, and defensive text sanitization.
"""

from datetime import datetime
from typing import Dict, Any, Optional


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format a datetime object to standard audit timestamp."""
    dt = dt or datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_input_text(text: str) -> str:
    """Strip dangerous characters and normalize whitespace."""
    if not text:
        return ""
    return "".join(ch for ch in text.strip() if ch not in "\r\n\t\0")


def build_api_response(
    success: bool,
    data: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """Construct consistent JSON API envelope."""
    response: Dict[str, Any] = {"success": success}
    if error:
        response["error"] = error
    if data:
        response.update(data)
    return response

