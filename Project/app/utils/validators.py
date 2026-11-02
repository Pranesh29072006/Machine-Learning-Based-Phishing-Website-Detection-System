"""
URL Input Validation Module
Performs defensive syntax checks on URLs without initiating network connections.
"""

import re
from urllib.parse import urlparse
from typing import Tuple

from app.ml.feature_extraction import is_ip
from config import Config


def validate_url(url_string: str) -> Tuple[bool, str, str]:
    """
    Validate user-submitted URL.
    Enforces HTTP/HTTPS protocol, basic hostname structure, and length limits.
    Does NOT initiate any external network connection.
    Returns: (is_valid, sanitized_url, error_message)
    """
    if not url_string or not isinstance(url_string, str):
        return False, "", "Please enter a valid website URL."
    
    # Strip whitespace and dangerous control characters
    sanitized = "".join(ch for ch in url_string.strip() if ch not in "\r\n\t\0")
    if not sanitized:
        return False, "", "Please enter a valid website URL."

    if len(sanitized) > Config.MAX_URL_LENGTH:
        return False, "", f"URL exceeds maximum permissible length of {Config.MAX_URL_LENGTH} characters."

    # Check for disallowed schemes early
    scheme_match = re.match(r"^([a-zA-Z][a-zA-Z0-9\+\.\-]*):", sanitized)
    if scheme_match:
        remainder = sanitized[len(scheme_match.group(0)):]
        if re.match(r"^\d+(/|$)", remainder) and not sanitized.lower().startswith(("http://", "https://")):
            pass  # Host:port pattern without explicit scheme
        else:
            scheme_prefix = scheme_match.group(1).lower()
            if scheme_prefix not in ("http", "https"):
                return False, "", f"Disallowed URL scheme '{scheme_prefix}:'. Only HTTP and HTTPS protocols are supported."

    # Prepend http:// if protocol is omitted to parse correctly
    if not (sanitized.startswith("http://") or sanitized.startswith("https://")):
        sanitized = "http://" + sanitized

    try:
        parsed = urlparse(sanitized)
    except Exception:
        return False, "", "Malformed URL structure."

    if parsed.scheme.lower() not in ("http", "https"):
        return False, "", f"Unsupported protocol '{parsed.scheme}'. Only HTTP and HTTPS are permitted."

    hostname = (parsed.hostname or "").strip()
    if not hostname:
        netloc = (parsed.netloc or "").strip()
        if netloc and not netloc.startswith("/"):
            hostname = netloc.split(":")[0]

    if not hostname:
        return False, "", "URL must contain a valid domain name or IP host address."

    # Strip port if present
    clean_host = hostname.split(":")[0] if ":" in hostname else hostname

    # Check if host is an IPv4 or IPv6 address or localhost
    if is_ip(hostname) or clean_host.lower() == "localhost":
        return True, sanitized, ""

    # Domain syntax validation: at least 2 labels, valid DNS characters
    labels = clean_host.split(".")
    if len(labels) < 2:
        return False, "", "Invalid domain format. Domain must contain a valid domain name and TLD."

    for label in labels:
        if not label:
            return False, "", "Invalid domain format: domain labels cannot be empty."
        if not re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$", label):
            return False, "", f"Invalid domain label '{label}'. Domains must contain alphanumeric characters."

    return True, sanitized, ""

