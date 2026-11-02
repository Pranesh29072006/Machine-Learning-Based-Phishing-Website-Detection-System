"""
Database Operations Module for CodePulse AI
Encapsulates CRUD operations, telemetry aggregation, pagination, and CSV export.
"""

import os
import sqlite3
import csv
import io
import math
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.database.connection import get_connection, get_db_path


def save_scan(
    url: str,
    prediction: str,
    confidence: float,
    risk_level: str,
    processing_time_ms: float = 0.0
) -> int:
    """Save an analyzed URL scan record to SQLite with parameterized inputs."""
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute("""
                INSERT INTO scans (url, prediction, confidence, risk_level, processing_time_ms)
                VALUES (?, ?, ?, ?, ?);
            """, (url, prediction, confidence, risk_level, processing_time_ms))
            return cursor.lastrowid
    finally:
        conn.close()


def get_scan_by_id(scan_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve an individual scan record by its primary key ID."""
    conn = get_connection()
    try:
        row = conn.execute("""
            SELECT id, url, prediction, confidence, risk_level, processing_time_ms, created_at
            FROM scans WHERE id = ?;
        """, (scan_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_recent_scans(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve most recent scan records sorted chronologically descending."""
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT id, url, prediction, confidence, risk_level, processing_time_ms, created_at
            FROM scans
            ORDER BY created_at DESC, id DESC
            LIMIT ?;
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_all_scans(search_query: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve scans with optional search filter on URL or risk category."""
    conn = get_connection()
    try:
        if search_query:
            wildcard = f"%{search_query.strip()}%"
            rows = conn.execute("""
                SELECT id, url, prediction, confidence, risk_level, processing_time_ms, created_at
                FROM scans
                WHERE url LIKE ? OR prediction LIKE ? OR risk_level LIKE ?
                ORDER BY created_at DESC, id DESC
                LIMIT ?;
            """, (wildcard, wildcard, wildcard, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT id, url, prediction, confidence, risk_level, processing_time_ms, created_at
                FROM scans
                ORDER BY created_at DESC, id DESC
                LIMIT ?;
            """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_paginated_scans(
    search_query: Optional[str] = None,
    classification: Optional[str] = "All",
    sort_order: Optional[str] = "desc",
    page: int = 1,
    per_page: int = 15
) -> Dict[str, Any]:
    """Retrieve paginated, filtered, and sorted scans for the history UI."""
    page = max(1, int(page))
    per_page = max(1, min(100, int(per_page)))
    offset = (page - 1) * per_page
    
    where_clauses = []
    params = []
    
    if search_query and search_query.strip():
        where_clauses.append("(url LIKE ? OR risk_level LIKE ?)")
        wildcard = f"%{search_query.strip()}%"
        params.extend([wildcard, wildcard])
        
    if classification and classification in ("Legitimate", "Phishing"):
        where_clauses.append("prediction = ?")
        params.append(classification)
        
    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    order_dir = "ASC" if sort_order and sort_order.lower() == "asc" else "DESC"
    
    conn = get_connection()
    try:
        # Count total matching
        count_query = f"SELECT COUNT(*) FROM scans {where_sql};"
        total_count = conn.execute(count_query, params).fetchone()[0]
        total_pages = max(1, math.ceil(total_count / per_page))
        
        # Fetch page slice
        data_query = f"""
            SELECT id, url, prediction, confidence, risk_level, processing_time_ms, created_at
            FROM scans
            {where_sql}
            ORDER BY created_at {order_dir}, id {order_dir}
            LIMIT ? OFFSET ?;
        """
        rows = conn.execute(data_query, params + [per_page, offset]).fetchall()
        records = [dict(r) for r in rows]
        
        start_idx = offset + 1 if total_count > 0 else 0
        end_idx = min(offset + per_page, total_count)
        
        return {
            "records": records,
            "total_count": total_count,
            "current_page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages,
            "start_idx": start_idx,
            "end_idx": end_idx
        }
    finally:
        conn.close()


def get_scan_stats() -> Dict[str, Any]:
    """Compute aggregate telemetry across all stored scans."""
    conn = get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM scans;").fetchone()[0]
        if total == 0:
            return {
                "total": 0,
                "legitimate": 0,
                "phishing": 0,
                "detection_rate": 0.0,
                "safe_percentage": 0.0,
                "avg_processing_time_ms": 0.0
            }
            
        phishing = conn.execute("SELECT COUNT(*) FROM scans WHERE prediction = 'Phishing';").fetchone()[0]
        legitimate = total - phishing
        
        avg_time_row = conn.execute("SELECT AVG(processing_time_ms) FROM scans WHERE processing_time_ms > 0;").fetchone()
        avg_time = round(float(avg_time_row[0]), 2) if avg_time_row and avg_time_row[0] is not None else 0.0
        
        detection_rate = round((phishing / total) * 100, 1)
        safe_percentage = round((legitimate / total) * 100, 1)
        
        return {
            "total": total,
            "legitimate": legitimate,
            "phishing": phishing,
            "phishing_percentage": detection_rate,
            "detection_rate": detection_rate,
            "safe_percentage": safe_percentage,
            "avg_processing_time_ms": avg_time
        }
    finally:
        conn.close()


def get_analytics_summary() -> Dict[str, Any]:
    """Compile aggregated data structures required for Chart.js telemetry dashboards."""
    conn = get_connection()
    try:
        stats = get_scan_stats()
        
        # Risk tier distribution
        risk_counts = {"High Risk": 0, "Moderate-High Risk": 0, "Low-to-Moderate Risk": 0, "Low Risk": 0}
        rows = conn.execute("SELECT risk_level, COUNT(*) FROM scans GROUP BY risk_level;").fetchall()
        for r in rows:
            if r[0] in risk_counts:
                risk_counts[r[0]] = r[1]
                
        # Daily trends (last 30 days)
        daily_trends = []
        trend_rows = conn.execute("""
            SELECT 
                DATE(created_at) as scan_date,
                COUNT(*) as total_scans,
                SUM(CASE WHEN prediction = 'Legitimate' THEN 1 ELSE 0 END) as legit_count,
                SUM(CASE WHEN prediction = 'Phishing' THEN 1 ELSE 0 END) as phish_count
            FROM scans
            GROUP BY DATE(created_at)
            ORDER BY scan_date DESC
            LIMIT 30;
        """).fetchall()
        for tr in trend_rows:
            daily_trends.append({
                "scan_date": tr["scan_date"] or "Today",
                "total": tr["total_scans"],
                "legitimate": tr["legit_count"],
                "phishing": tr["phish_count"]
            })
            
        # Confidence score brackets
        confidence_distribution = {
            "50-60%": 0,
            "60-70%": 0,
            "70-80%": 0,
            "80-90%": 0,
            "90-100%": 0
        }
        conf_rows = conn.execute("""
            SELECT 
                CASE 
                    WHEN confidence >= 90 THEN '90-100%'
                    WHEN confidence >= 80 THEN '80-90%'
                    WHEN confidence >= 70 THEN '70-80%'
                    WHEN confidence >= 60 THEN '60-70%'
                    ELSE '50-60%'
                END as bracket,
                COUNT(*) as count
            FROM scans
            GROUP BY bracket;
        """).fetchall()
        for cr in conf_rows:
            if cr["bracket"] in confidence_distribution:
                confidence_distribution[cr["bracket"]] = cr["count"]

        # Storage size
        db_path = get_db_path()
        db_size_kb = round(os.path.getsize(db_path) / 1024, 2) if os.path.exists(db_path) else 0.0

        return {
            "stats": stats,
            "risk_distribution": risk_counts,
            "daily_trends": list(reversed(daily_trends)),
            "confidence_distribution": confidence_distribution,
            "db_size_kb": db_size_kb
        }
    finally:
        conn.close()


def _sanitize_csv_cell(value: Any) -> str:
    """Neutralize CSV formula injection (CWE-1236) by prefixing danger characters with a quote."""
    text = str(value) if value is not None else ""
    if text and text[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + text
    return text


def export_scans_to_csv() -> str:
    """Export all scan records as a sanitized RFC 4180 CSV document string."""
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT id, url, prediction, confidence, risk_level, processing_time_ms, created_at
            FROM scans
            ORDER BY created_at DESC, id DESC;
        """).fetchall()
        
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Scan ID", "Target URL", "Classification", "Confidence (%)", "Risk Level", "Latency (ms)", "Timestamp"])
        
        for r in rows:
            writer.writerow([
                _sanitize_csv_cell(r["id"]),
                _sanitize_csv_cell(r["url"]),
                _sanitize_csv_cell(r["prediction"]),
                _sanitize_csv_cell(r["confidence"]),
                _sanitize_csv_cell(r["risk_level"]),
                _sanitize_csv_cell(r["processing_time_ms"]),
                _sanitize_csv_cell(r["created_at"])
            ])
            
        return output.getvalue()
    finally:
        conn.close()


def clear_history() -> None:
    """Clear all records from the scans table."""
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM scans;")
            try:
                conn.execute("DELETE FROM sqlite_sequence WHERE name='scans';")
            except sqlite3.OperationalError:
                pass
    finally:
        conn.close()


def get_db_info() -> Dict[str, Any]:
    """Retrieve operational metadata regarding SQLite storage."""
    db_path = get_db_path()
    total_records = 0
    size_bytes = 0
    if os.path.exists(db_path):
        size_bytes = os.path.getsize(db_path)
    try:
        stats = get_scan_stats()
        total_records = stats.get("total", 0)
    except Exception:
        total_records = 0
        
    return {
        "path": db_path,
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 2),
        "total_records": total_records,
        "table_name": "scans"
    }
