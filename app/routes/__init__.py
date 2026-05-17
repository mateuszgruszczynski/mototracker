from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.saved_search import SavedSearch
from app.models.scan import Scan

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    searches = db.query(SavedSearch).all()

    # Last completed scan per search
    last_scan_rows = (
        db.query(Scan.saved_search_id, func.max(Scan.finished_at).label("last_scan_at"))
        .filter(Scan.status == "done")
        .group_by(Scan.saved_search_id)
        .all()
    )
    last_scan_at = {row.saved_search_id: row.last_scan_at for row in last_scan_rows}

    # Sort: never-scanned first, then oldest scan first
    searches.sort(key=lambda s: last_scan_at.get(s.id) or "")

    running_ids = {
        row.saved_search_id
        for row in db.query(Scan.saved_search_id).filter_by(status="running").all()
    }
    return templates.TemplateResponse(
        request, "index.html",
        {"searches": searches, "running_ids": running_ids, "last_scan_at": last_scan_at},
    )
