"""
Analytics Service Module
Provides telemetry computation, scan trend analysis, and KPI summaries.
"""

from typing import Dict, Any, List, Optional
from app.database.operations import (
    get_scan_stats,
    get_analytics_summary,
    get_recent_scans,
    get_paginated_scans,
    get_db_info
)


def get_dashboard_kpis() -> Dict[str, Any]:
    """Retrieve operational KPI overview metrics."""
    return get_scan_stats()


def get_recent_activity(limit: int = 8) -> List[Dict[str, Any]]:
    """Retrieve recent scan activity for table feeds."""
    return get_recent_scans(limit=limit)


def get_telemetry_report() -> Dict[str, Any]:
    """Compile comprehensive analytics payload for Chart.js telemetry."""
    return get_analytics_summary()


def get_history_feed(
    search_query: Optional[str] = None,
    classification: Optional[str] = "All",
    sort_order: Optional[str] = "desc",
    page: int = 1,
    per_page: int = 15
) -> Dict[str, Any]:
    """Retrieve filtered, sorted, and paginated scan records."""
    return get_paginated_scans(
        search_query=search_query,
        classification=classification,
        sort_order=sort_order,
        page=page,
        per_page=per_page
    )


def get_system_diagnostics() -> Dict[str, Any]:
    """Compile SQLite storage and database diagnostics."""
    return get_db_info()

