import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc
from sqlalchemy.orm import Session, subqueryload

from app.db import get_db
from app.models.listing import Listing
from app.models.price_point import PricePoint
from app.models.saved_search import SavedSearch
from app.models.scan import Scan
from app.scraper.persist import run_scan

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

router = APIRouter(prefix="/searches")


def _fmt_int(n: int | None) -> str:
    if n is None:
        return "–"
    return f"{n:,}".replace(",", " ")


def _badge(listing: Listing) -> tuple[str, str]:
    pps = listing.price_points
    if not pps:
        return "", "gray"
    if len(pps) == 1:
        if listing.first_seen_at and listing.last_seen_at and listing.first_seen_at.date() == listing.last_seen_at.date():
            return "New", "blue"
        return "= same", "gray"
    diff = float(pps[-1].price) - float(pps[-2].price)
    amt = _fmt_int(int(abs(diff)))
    if diff > 0:
        return f"↑ +{amt} {pps[-1].currency}", "red"
    return f"↓ −{amt} {pps[-1].currency}", "green"


def _validate(name: str, make: str, model: str) -> dict[str, str]:
    errors: dict[str, str] = {}
    if not name.strip():
        errors["name"] = "Name is required."
    if not make.strip():
        errors["make"] = "Make is required."
    if not model.strip():
        errors["model"] = "Model is required."
    return errors


# ── literal routes first ───────────────────────────────────────────────────

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
    return RedirectResponse("/?toast=Search+created", status_code=303)


# ── parameterised routes ───────────────────────────────────────────────────

@router.get("/{search_id}", response_class=HTMLResponse)
async def results(request: Request, search_id: int, db: Session = Depends(get_db)):
    search = db.get(SavedSearch, search_id)
    if search is None:
        return HTMLResponse("Not found", status_code=404)

    last_scan = (
        db.query(Scan)
        .filter_by(saved_search_id=search_id, status="done")
        .order_by(desc(Scan.finished_at))
        .first()
    )

    listings = (
        db.query(Listing)
        .filter_by(saved_search_id=search_id, status="active")
        .options(subqueryload(Listing.price_points))
        .all()
    )

    rows = []
    for lst in listings:
        pps = lst.price_points
        current_price = float(pps[-1].price) if pps else None
        current_currency = pps[-1].currency if pps else "PLN"
        badge_text, badge_color = _badge(lst)
        rows.append({
            "id": lst.id,
            "title": lst.title or "–",
            "year": lst.year,
            "mileage": lst.mileage,
            "price": current_price,
            "currency": current_currency,
            "price_fmt": f"{_fmt_int(int(current_price))} {current_currency}" if current_price else "–",
            "mileage_fmt": f"{_fmt_int(lst.mileage)} km",
            "badge_text": badge_text,
            "badge_color": badge_color,
            "location": lst.location or "–",
            "last_seen": lst.last_seen_at.strftime("%Y-%m-%d") if lst.last_seen_at else "–",
            "url": lst.url,
        })

    rows_json = json.dumps(rows, ensure_ascii=False)
    return templates.TemplateResponse(
        request,
        "searches/results.html",
        {
            "search": search,
            "last_scan": last_scan,
            "total": len(rows),
            "rows_json": rows_json,
        },
    )


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
    return RedirectResponse("/?toast=Search+updated", status_code=303)


@router.post("/{search_id}/scan")
async def trigger_scan(search_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from app.scraper.events import emit, scan_queues
    import asyncio

    search = db.get(SavedSearch, search_id)
    if search is None:
        return HTMLResponse("Not found", status_code=404)
    running = db.query(Scan).filter_by(saved_search_id=search_id, status="running").first()
    if running:
        return RedirectResponse(f"/searches/{search_id}?scan_id={running.id}", status_code=303)

    # Create scan row here so we have the scan_id before the background task starts.
    from datetime import datetime, timezone
    from app.models.scan import Scan as ScanModel
    scan = ScanModel(saved_search_id=search_id, started_at=datetime.now(timezone.utc), status="running")
    db.add(scan)
    db.commit()
    db.refresh(scan)
    scan_id = scan.id

    # Initialise the queue so the SSE route finds it immediately.
    scan_queues[scan_id] = asyncio.Queue()

    background_tasks.add_task(run_scan, search_id, scan)
    return RedirectResponse(f"/searches/{search_id}?scan_id={scan_id}", status_code=303)


@router.post("/{search_id}/delete")
async def delete(search_id: int, db: Session = Depends(get_db)):
    search = db.get(SavedSearch, search_id)
    if search:
        db.delete(search)
        db.commit()
    return RedirectResponse("/?toast=Search+deleted", status_code=303)
