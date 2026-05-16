import asyncio
import logging
from datetime import datetime, timezone
from math import floor

from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal
from app.models.listing import Listing
from app.models.price_point import PricePoint
from app.models.saved_search import SavedSearch
from app.models.scan import Scan
from app.scraper.engine import check_listing_exists, scrape_search
from app.scraper.throttle import AsyncThrottler

logger = logging.getLogger(__name__)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _mileage_bucket(mileage: int | None) -> int | None:
    if mileage is None:
        return None
    return floor(mileage / 10_000) * 10_000


def _fuzzy_key(listing: Listing) -> tuple | None:
    """Five-field exact match key. Returns None if any field is missing."""
    bucket = _mileage_bucket(listing.mileage)
    if None in (listing.make, listing.model, listing.year, bucket, listing.seller_id):
        return None
    return (listing.make, listing.model, listing.year, bucket, listing.seller_id)


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
        seen_ids: set[str] = set()

        # Build fuzzy-match index of confirmed_sold listings for this search.
        sold_listings: list[Listing] = (
            db.query(Listing)
            .filter_by(saved_search_id=saved_search_id, status="confirmed_sold")
            .all()
        )
        sold_by_key: dict[tuple, Listing] = {}
        for sl in sold_listings:
            key = _fuzzy_key(sl)
            if key is not None:
                sold_by_key[key] = sl

        for pl in listings:
            seen_ids.add(pl.otomoto_id)
            existing: Listing | None = db.get(Listing, pl.otomoto_id)
            if existing:
                existing.last_seen_at = now
                # Re-activate if it had been marked sold/likely_sold.
                if existing.status in ("likely_sold", "confirmed_sold"):
                    existing.status = "active"
                    existing.sold_at = None
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
                # Fuzzy match against confirmed_sold listings.
                candidate_key = (
                    search.make,
                    search.model,
                    pl.year,
                    _mileage_bucket(pl.mileage),
                    pl.seller_id,
                )
                relisted_from: str | None = None
                if None not in candidate_key:
                    matched = sold_by_key.get(candidate_key)
                    if matched:
                        relisted_from = matched.id

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
                    relisted_from_listing_id=relisted_from,
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

        # Re-check disappeared active/likely_sold listings.
        disappeared: list[Listing] = (
            db.query(Listing)
            .filter(
                Listing.saved_search_id == saved_search_id,
                Listing.status.in_(("active", "likely_sold")),
                Listing.id.notin_(seen_ids),
            )
            .all()
        )

        if disappeared:
            throttler = AsyncThrottler(
                min_seconds=settings.throttle_min_seconds,
                jitter_seconds=settings.throttle_jitter_seconds,
            )
            for listing in disappeared:
                try:
                    still_up = await check_listing_exists(listing.url, throttler=throttler)
                    if still_up:
                        listing.status = "likely_sold"
                        logger.warning(
                            "Listing %s still reachable but not in scan %s results — marked likely_sold",
                            listing.id,
                            scan.id,
                        )
                    else:
                        listing.status = "confirmed_sold"
                        listing.sold_at = now
                except Exception as exc:
                    logger.warning("Re-check failed for listing %s: %s", listing.id, exc)
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
