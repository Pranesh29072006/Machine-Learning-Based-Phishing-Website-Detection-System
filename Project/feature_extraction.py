"""
Feature Extraction Module for Phishing Website Detection System.

This module provides standardized lexical and structural URL feature extraction.
Both the ML training pipeline (train_model.py) and the Flask live inference backend (app.py)
MUST use this exact module to guarantee feature consistency.
"""

import re
import ipaddress
from urllib.parse import urlparse
import numpy as np

# Well-known URL shortening domains
SHORTENING_SERVICES = {
    'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'cli.gs', 'yfrog.com',
    'migre.me', 'ff.im', 'tiny.cc', 'url4.eu', 'twit.ac', 'su.pr', 'twurl.nl',
    'snipurl.com', 'short.to', 'budurl.com', 'ping.fm', 'post.ly', 'just.as',
    'bkite.com', 'snipr.com', 'fic.kr', 'loopt.us', 'doiop.com', 'short.ie',
    'kl.am', 'wp.me', 'rubyurl.com', 'om.ly', 'to.ly', 'bit.do', 't.ly',
    'lnkd.in', 'db.tt', 'qr.ae', 'adf.ly', 'cur.lv', 'ity.im', 'q.gs',
    'po.st', 'bc.vc', 'twitthis.com', 'u.to', 'j.mp', 'buzurl.com', 'cutt.ly',
    'u.bb', 'yourls.org', 'x.co', 'prettylinkpro.com', 'scrnch.me', 'filoops.info',
    'vzturl.com', 'qr.net', '1url.com', 'tweez.me', 'v.gd', 'tr.im', 'link.zip'
}

# Suspicious keywords commonly observed in credential harvesting and phishing attacks
SENSITIVE_KEYWORDS = [
    'login', 'signin', 'verify', 'verification', 'account', 'banking',
    'secure', 'security', 'update', 'confirm', 'confirmation', 'authenticate',
    'credential', 'password', 'wallet', 'unlock', 'support', 'service',
    'billing', 'invoice', 'paypal', 'appleid', 'recovery', 'revalidate'
]

# Strict ordered list of features used for training and model inference
FEATURE_NAMES = [
    'url_length',
    'domain_length',
    'num_dots',
    'num_hyphens',
    'num_digits',
    'has_ip_address',
    'is_https',
    'has_at_symbol',
    'num_suspicious_symbols',
    'num_subdomains',
    'is_shortened',
    'path_length',
    'num_query_params',
    'has_sensitive_keywords',
    'has_double_slash_redirect',
    'prefix_suffix_hyphen',
    'has_tld_in_subdomain'
]


def normalize_url(url: str) -> str:
    """Ensure URL has an HTTP/HTTPS scheme for parsing."""
    if not url:
        return ""
    url = url.strip()
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    return url


def is_ip(hostname: str) -> int:
    """Check if the domain/hostname is an IPv4 or IPv6 address."""
    if not hostname:
        return 0
    clean_host = hostname.strip()
    # Handle bracketed IPv6 literals with or without port (e.g. [::1], [::1]:8080)
    if clean_host.startswith('['):
        if ']:' in clean_host:
            clean_host = clean_host.split(']:')[0].lstrip('[')
        else:
            clean_host = clean_host.strip('[]')
    elif ':' in clean_host and clean_host.count(':') == 1 and '.' in clean_host:
        # IPv4 with port (e.g. 192.168.1.1:8080)
        clean_host = clean_host.split(':')[0]
    try:
        ipaddress.ip_address(clean_host)
        return 1
    except ValueError:
        return 0


def count_subdomains(hostname: str) -> int:
    """
    Calculate the number of subdomains in the hostname.
    Raw IP addresses return 0 subdomains.
    """
    if not hostname or is_ip(hostname):
        return 0
    # Strip port if present
    if ':' in hostname:
        hostname = hostname.split(':')[0]
    parts = [p for p in hostname.split('.') if p]
    if len(parts) <= 2:
        return 0
    return max(0, len(parts) - 2)


def has_tld_in_sub(hostname: str) -> int:
    """Check if common TLDs appear inside subdomains (e.g., paypal.com.attacker.com)."""
    if not hostname:
        return 0
    common_tlds = ['.com.', '.net.', '.org.', '.edu.', '.gov.', '.co.', '.info.', '.xyz.']
    host_lower = hostname.lower()
    for tld in common_tlds:
        if tld in host_lower:
            return 1
    return 0


def extract_features(url: str) -> np.ndarray:
    """
    Extract standardized numeric feature vector from a given URL string.
    Returns:
        1D numpy array of shape (17,) matching FEATURE_NAMES ordering.
    """
    norm_url = normalize_url(url)
    try:
        parsed = urlparse(norm_url)
    except Exception:
        parsed = urlparse('http://invalid.domain')

    hostname = (parsed.hostname or parsed.netloc or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""

    # 1. URL Length
    url_length = float(len(url))

    # 2. Domain Length
    domain_length = float(len(hostname))

    # 3. Number of dots
    num_dots = float(url.count('.'))

    # 4. Number of hyphens
    num_hyphens = float(url.count('-'))

    # 5. Number of digits
    num_digits = float(sum(c.isdigit() for c in url))

    # 6. Presence of IP Address
    has_ip = float(is_ip(hostname))

    # 7. Is HTTPS
    is_https = 1.0 if parsed.scheme.lower() == 'https' else 0.0

    # 8. Has '@' symbol (ignores auth prefix tricks)
    has_at = 1.0 if '@' in url else 0.0

    # 9. Suspicious symbols count (?, =, &, %, ~, +, //)
    suspicious_chars = ['?', '=', '&', '%', '~', '+', '$', '#', '!']
    num_suspicious = float(sum(url.count(c) for c in suspicious_chars))

    # 10. Number of subdomains
    num_subdomains = float(count_subdomains(hostname))

    # 11. Is Shortened URL
    is_shortened = 1.0 if hostname in SHORTENING_SERVICES else 0.0

    # 12. Path Length
    path_length = float(len(path))

    # 13. Number of Query Parameters
    num_query_params = float(len(query.split('&')) if query else 0)

    # 14. Has Sensitive Keywords
    url_lower = url.lower()
    keyword_count = sum(1 for kw in SENSITIVE_KEYWORDS if kw in url_lower)
    has_sensitive_keywords = float(keyword_count)

    # 15. Double slash redirection in path
    # When '//' appears in the path portion, browsers can be redirected
    has_double_slash = 1.0 if '//' in path else 0.0

    # 16. Prefix / Suffix hyphen in domain
    prefix_suffix_hyphen = 1.0 if '-' in hostname else 0.0

    # 17. TLD in subdomain / deceptive hostname
    has_tld_sub = float(has_tld_in_sub(hostname))

    features = [
        url_length,
        domain_length,
        num_dots,
        num_hyphens,
        num_digits,
        has_ip,
        is_https,
        has_at,
        num_suspicious,
        num_subdomains,
        is_shortened,
        path_length,
        num_query_params,
        has_sensitive_keywords,
        has_double_slash,
        prefix_suffix_hyphen,
        has_tld_sub
    ]

    return np.array(features, dtype=float)


def get_feature_details(url: str) -> list:
    """
    Returns an informative, human-readable list of feature dictionaries
    for presentation on the Result Page and security explanations.
    """
    raw_vec = extract_features(url)
    norm_url = normalize_url(url)
    try:
        parsed = urlparse(norm_url)
    except Exception:
        parsed = urlparse('http://invalid.domain')

    hostname = (parsed.hostname or parsed.netloc or "").lower()

    details = [
        {
            'name': 'URL Length',
            'value': int(raw_vec[0]),
            'status': 'warning' if raw_vec[0] > 75 else 'safe',
            'description': 'Excessively long URLs (>75 characters) are frequently used by attackers to hide malicious redirects or tokens.'
        },
        {
            'name': 'Domain Length',
            'value': int(raw_vec[1]),
            'status': 'warning' if raw_vec[1] > 30 else 'safe',
            'description': 'Long domain names (>30 chars) often spoof legitimate brand names with extra keywords.'
        },
        {
            'name': 'Dot Count',
            'value': int(raw_vec[2]),
            'status': 'warning' if raw_vec[2] >= 3 else 'safe',
            'description': 'Three or more dots in a URL usually indicate deep nested subdomains or disguised hosts.'
        },
        {
            'name': 'Hyphen Count',
            'value': int(raw_vec[3]),
            'status': 'warning' if raw_vec[3] >= 2 else 'safe',
            'description': 'Hyphens in hostnames (e.g., paypal-security-update) are a classic trademark spoofing indicator.'
        },
        {
            'name': 'Numeric Digits',
            'value': int(raw_vec[4]),
            'status': 'warning' if raw_vec[4] > 5 else 'safe',
            'description': 'High digit frequency often represents session IDs, IP hashes, or autogenerated malicious links.'
        },
        {
            'name': 'IP Address in Hostname',
            'value': 'Yes' if raw_vec[5] == 1 else 'No',
            'status': 'danger' if raw_vec[5] == 1 else 'safe',
            'description': 'Legitimate brands rarely use direct IP addresses (e.g., http://192.168.1.1/login) to host services.'
        },
        {
            'name': 'HTTPS Protocol',
            'value': 'Enabled' if raw_vec[6] == 1 else 'Disabled (HTTP)',
            'status': 'safe' if raw_vec[6] == 1 else 'warning',
            'description': 'HTTPS encrypts communications. Note: modern phishing pages may also use free TLS certificates.'
        },
        {
            'name': "'@' Symbol Present",
            'value': 'Yes' if raw_vec[7] == 1 else 'No',
            'status': 'danger' if raw_vec[7] == 1 else 'safe',
            'description': "The '@' character instructs browsers to ignore everything preceding it, leading to deceptive navigation."
        },
        {
            'name': 'Suspicious Symbols Count',
            'value': int(raw_vec[8]),
            'status': 'warning' if raw_vec[8] >= 4 else 'safe',
            'description': 'Abundance of query delimiters (?, &, =, %) may indicate obfuscated payload transmission.'
        },
        {
            'name': 'Subdomain Levels',
            'value': int(raw_vec[9]),
            'status': 'warning' if raw_vec[9] >= 2 else 'safe',
            'description': 'Multiple subdomain levels often camouflage fraudulent destinations behind recognized services.'
        },
        {
            'name': 'URL Shortening Service',
            'value': 'Detected' if raw_vec[10] == 1 else 'None',
            'status': 'warning' if raw_vec[10] == 1 else 'safe',
            'description': 'Shortened links (e.g., bit.ly, tinyurl) mask the true destination domain from user inspection.'
        },
        {
            'name': 'Sensitive Security Keywords',
            'value': int(raw_vec[13]),
            'status': 'warning' if raw_vec[13] > 0 else 'safe',
            'description': f'Presence of terms such as login, verify, secure, banking, or account.'
        },
        {
            'name': 'Double Slash in Path',
            'value': 'Detected' if raw_vec[14] == 1 else 'None',
            'status': 'danger' if raw_vec[14] == 1 else 'safe',
            'description': 'Double slashes (//) within the path component can cause redirect vulnerabilities in browsers.'
        },
        {
            'name': 'Hyphen in Hostname',
            'value': 'Yes' if raw_vec[15] == 1 else 'No',
            'status': 'warning' if raw_vec[15] == 1 else 'safe',
            'description': 'Hyphenated domain names (e.g. apple-login-id.com) are widely used to mimic trustworthy organizations.'
        },
        {
            'name': 'TLD in Subdomain',
            'value': 'Detected' if raw_vec[16] == 1 else 'None',
            'status': 'danger' if raw_vec[16] == 1 else 'safe',
            'description': 'Embedding domains like .com or .org in subdomains (e.g. google.com.secure.net) deceives users.'
        }
    ]
    return details

