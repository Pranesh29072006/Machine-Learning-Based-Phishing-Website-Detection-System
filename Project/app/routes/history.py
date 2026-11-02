"""
Scan History & Audit Log Blueprint
Provides searchable, filterable, paginated scan history and CSV export.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response

from app.services.analytics_service import get_history_feed, get_dashboard_kpis
from app.database.operations import export_scans_to_csv, clear_history as db_clear_history

history_bp = Blueprint("history_bp", __name__)


@history_bp.route("/history")
def history():
    """Paginated, searchable, and filterable scan history view."""
    search_query = request.args.get("q", "").strip()
    classification = request.args.get("type", "All").strip()
    sort_order = request.args.get("sort", "desc").strip()

    try:
        page = int(request.args.get("page", 1))
    except (ValueError, TypeError):
        page = 1

    try:
        per_page = int(request.args.get("per_page", 15))
    except (ValueError, TypeError):
        per_page = 15

    # Retrieve paginated scans
    pagination = get_history_feed(
        search_query=search_query,
        classification=classification,
        sort_order=sort_order,
        page=page,
        per_page=per_page
    )

    scans = pagination["records"]
    stats = get_dashboard_kpis()

    return render_template(
        "history.html",
        scans=scans,
        pagination=pagination,
        search_query=search_query,
        selected_type=classification,
        sort_order=sort_order,
        stats=stats
    )


@history_bp.route("/history/export")
def export_history():
    """Export all scan records as a downloadable RFC 4180 CSV document."""
    csv_data = export_scans_to_csv()
    filename = f"codepulse_scan_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
    )


@history_bp.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear all records from SQLite scan history."""
    db_clear_history()
    flash("Scan history has been successfully cleared.", "info")
    return redirect(url_for("history"))

