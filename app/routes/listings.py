import json
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, subqueryload

from app.db import get_db
from app.models.listing import Listing
from app.models.saved_search import SavedSearch

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

router = APIRouter(prefix="/listings")


def _fmt(n: int | None) -> str:
    if n is None:
        return "–"
    return f"{n:,}".replace(",", " ")


@router.get("/{otomoto_id}", response_class=HTMLResponse)
async def detail(request: Request, otomoto_id: str, db: Session = Depends(get_db)):
    listing = (
        db.query(Listing)
        .filter_by(id=otomoto_id)
        .options(subqueryload(Listing.price_points))
        .first()
    )
    if listing is None:
        return HTMLResponse("Listing not found", status_code=404)

    pps = listing.price_points
    chart_data = None
    if len(pps) >= 2:
        chart_data = json.dumps(
            {
                "labels": [pp.observed_at.strftime("%Y-%m-%d %H:%M") for pp in pps],
                "prices": [float(pp.price) for pp in pps],
            },
            ensure_ascii=False,
        )

    history = []
    for i, pp in enumerate(pps):
        if i == 0:
            delta = None
        else:
            delta = float(pp.price) - float(pps[i - 1].price)
        history.append(
            {
                "date": pp.observed_at.strftime("%Y-%m-%d %H:%M"),
                "price": float(pp.price),
                "currency": pp.currency,
                "price_fmt": f"{_fmt(int(pp.price))} {pp.currency}",
                "delta": delta,
                "delta_fmt": (
                    f"↑ +{_fmt(int(abs(delta)))} {pp.currency}" if delta and delta > 0
                    else f"↓ −{_fmt(int(abs(delta)))} {pp.currency}" if delta and delta < 0
                    else "= same" if delta == 0
                    else "–"
                ),
                "delta_color": (
                    "red" if delta and delta > 0
                    else "green" if delta and delta < 0
                    else "gray"
                ),
            }
        )

    status_map = {
        "active": ("Active", "green"),
        "likely_sold": ("Likely sold", "amber"),
        "confirmed_sold": ("Confirmed sold", "red"),
    }
    status_label, status_color = status_map.get(listing.status, ("Unknown", "gray"))

    search = db.get(SavedSearch, listing.saved_search_id) if listing.saved_search_id else None

    return templates.TemplateResponse(
        request,
        "listings/detail.html",
        {
            "listing": listing,
            "search": search,
            "chart_data": chart_data,
            "history": history,
            "status_label": status_label,
            "status_color": status_color,
            "mileage_fmt": _fmt(listing.mileage),
        },
    )
