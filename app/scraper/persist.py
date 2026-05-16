import asyncio
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.listing import Listing
from app.models.price_point import PricePoint
from app.models.saved_search import SavedSearch
from app.models.scan import Scan
from app.scraper.engine import scrape_search


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def run_scan(saved_search_id: int) -> None:
    db: Session = SessionLocal()
    scan = Scan(saved_search_id=saved_search_id, started_at=_now(), status="running")
    try:
        db.add(scan)
        db.commit()
        db.refresh(scan)

        search: SavedSearch | None = db.get(SavedSearch, saved_search_id)
        if search is None:
            scan.status = "failed"
            scan.error_summary = "SavedSearch not found"
            db.commit()
            return

        filters = {
            "make": search.make,
            "model": search.model,
            "year_from": search.year_from,
            "year_to": search.year_to,
            "country_of_origin": search.country_of_origin,
            "condition": search.condition,
        }

        listings = await scrape_search(filters)

        result_count = 0
        now = _now()
        for pl in listings:
            existing: Listing | None = db.get(Listing, pl.otomoto_id)
            if existing:
                existing.last_seen_at = now
                if pl.year is not None:
                    existing.year = pl.year
                if pl.mileage is not None:
                    existing.mileage = pl.mileage
                last_pp = (
                    db.query(PricePoint)
                    .filter_by(listing_id=pl.otomoto_id)
                    .order_by(PricePoint.observed_at.desc())
                    .first()
                )
                if pl.price is not None and (last_pp is None or float(last_pp.price) != float(pl.price)):
                    db.add(
                        PricePoint(
                            listing_id=pl.otomoto_id,
                            scan_id=scan.id,
                            price=float(pl.price),
                            currency=pl.currency,
                            observed_at=now,
                        )
                    )
            else:
                new_listing = Listing(
                    id=pl.otomoto_id,
                    saved_search_id=saved_search_id,
                    make=search.make,
                    model=search.model,
                    year=pl.year,
                    mileage=pl.mileage,
                    fuel=pl.fuel,
                    gearbox=pl.gearbox,
                    vin=pl.vin,
                    seller_id=pl.seller_id,
                    url=pl.url,
                    title=pl.title,
                    location=pl.location,
                    first_seen_at=now,
                    last_seen_at=now,
                    status="active",
                )
                db.add(new_listing)
                if pl.price is not None:
                    db.add(
                        PricePoint(
                            listing_id=pl.otomoto_id,
                            scan_id=scan.id,
                            price=float(pl.price),
                            currency=pl.currency,
                            observed_at=now,
                        )
                    )
            result_count += 1

        db.commit()
        scan.finished_at = _now()
        scan.status = "done"
        scan.result_count = result_count
        db.commit()

    except Exception as exc:
        try:
            scan.status = "failed"
            scan.error_summary = str(exc)[:500]
            scan.finished_at = _now()
            db.commit()
        except Exception:
            pass
        raise
    finally:
        db.close()
