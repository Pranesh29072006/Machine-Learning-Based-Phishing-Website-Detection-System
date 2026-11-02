"""
Database Subpackage Initialization
Re-exports connection utilities, data models, and CRUD operations.
"""

from app.database.connection import (
    get_connection,
    init_db,
    get_db_path,
    set_db_path
)

from app.database.models import (
    ScanRecord,
    ScanStats
)

from app.database.operations import (
    save_scan,
    get_scan_by_id,
    get_recent_scans,
    get_all_scans,
    get_paginated_scans,
    get_scan_stats,
    get_analytics_summary,
    export_scans_to_csv,
    clear_history,
    get_db_info
)

__all__ = [
    "get_connection",
    "init_db",
    "get_db_path",
    "set_db_path",
    "ScanRecord",
    "ScanStats",
    "save_scan",
    "get_scan_by_id",
    "get_recent_scans",
    "get_all_scans",
    "get_paginated_scans",
    "get_scan_stats",
    "get_analytics_summary",
    "export_scans_to_csv",
    "clear_history",
    "get_db_info"
]

