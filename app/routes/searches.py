from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.saved_search import SavedSearch
from app.models.scan import Scan
from app.scraper.persist import run_scan

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

router = APIRouter(prefix="/searches")


@router.get("/new", response_class=HTMLResponse)
async def new_form(request: Request):
    return templates.TemplateResponse(request, "searches/form.html", {"errors": {}, "values": {}})


@router.post("", response_class=HTMLResponse)
async def create(
    request: Request,
    name: str = Form(""),
    make: str = Form(""),
    model: str = Form(""),
    year_from: str = Form(""),
    year_to: str = Form(""),
    db: Session = Depends(get_db),
):
    errors = _validate(name, make, model)
    if errors:
        values = {"name": name, "make": make, "model": model, "year_from": year_from, "year_to": year_to}
        return templates.TemplateResponse(request, "searches/form.html", {"errors": errors, "values": values})

    search = SavedSearch(
        name=name.strip(),
        make=make.strip(),
        model=model.strip(),
        year_from=int(year_from) if year_from.strip() else None,
        year_to=int(year_to) if year_to.strip() else None,
    )
    db.add(search)
    db.commit()
    return RedirectResponse("/", status_code=303)


@router.get("/{search_id}/edit", response_class=HTMLResponse)
async def edit_form(request: Request, search_id: int, db: Session = Depends(get_db)):
    search = db.get(SavedSearch, search_id)
    if search is None:
        return HTMLResponse("Not found", status_code=404)
    values = {
        "name": search.name,
        "make": search.make,
        "model": search.model,
        "year_from": search.year_from or "",
        "year_to": search.year_to or "",
    }
    return templates.TemplateResponse(request, "searches/form.html", {"errors": {}, "values": values, "search": search})


@router.post("/{search_id}", response_class=HTMLResponse)
async def update(
    request: Request,
    search_id: int,
    name: str = Form(""),
    make: str = Form(""),
    model: str = Form(""),
    year_from: str = Form(""),
    year_to: str = Form(""),
    db: Session = Depends(get_db),
):
    search = db.get(SavedSearch, search_id)
    if search is None:
        return HTMLResponse("Not found", status_code=404)

    errors = _validate(name, make, model)
    if errors:
        values = {"name": name, "make": make, "model": model, "year_from": year_from, "year_to": year_to}
        return templates.TemplateResponse(
            request, "searches/form.html", {"errors": errors, "values": values, "search": search}
        )

    search.name = name.strip()
    search.make = make.strip()
    search.model = model.strip()
    search.year_from = int(year_from) if year_from.strip() else None
    search.year_to = int(year_to) if year_to.strip() else None
    search.updated_at = datetime.now(timezone.utc)
    db.commit()
    return RedirectResponse("/", status_code=303)


@router.post("/{search_id}/scan")
async def trigger_scan(search_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    search = db.get(SavedSearch, search_id)
    if search is None:
        return HTMLResponse("Not found", status_code=404)
    running = db.query(Scan).filter_by(saved_search_id=search_id, status="running").first()
    if not running:
        background_tasks.add_task(run_scan, search_id)
    return RedirectResponse("/", status_code=303)


@router.post("/{search_id}/delete")
async def delete(search_id: int, db: Session = Depends(get_db)):
    search = db.get(SavedSearch, search_id)
    if search:
        db.delete(search)
        db.commit()
    return RedirectResponse("/", status_code=303)


def _validate(name: str, make: str, model: str) -> dict[str, str]:
    errors: dict[str, str] = {}
    if not name.strip():
        errors["name"] = "Name is required."
    if not make.strip():
        errors["make"] = "Make is required."
    if not model.strip():
        errors["model"] = "Model is required."
    return errors
