# i4-dev.md — Scan Execution & Persistence

## Files changed

Added:
- `app/models/scan.py`, `app/models/listing.py`, `app/models/price_point.py` — three new ORM models
- `alembic/versions/cf78aa649f8b_add_scan_listing_price_point.py` — migration
- `app/scraper/persist.py` — run_scan(): creates Scan row, calls scrape_search, upserts listings, appends price_points on price change, updates scan status

Modified:
- `app/models/__init__.py` — imports all four models
- `app/routes/searches.py` — POST /{id}/scan; concurrency guard; BackgroundTasks
- `app/routes/__init__.py` — home route passes running_ids set to template
- `app/templates/index.html` — Run Scan button + Scanning… state
- `app/scraper/selectors.py` — fixed selectors: h3=price, dd=params positional, li:has-text("(")=location
- `app/scraper/engine.py` — updated to use fixed selectors; separate currency parsing

## In-process tests

None — test_coverage=none per policy.

## External interfaces wired

- `POST /searches/{id}/scan` → 303 (scan enqueued as background task)
- Background `run_scan(saved_search_id)` → calls scrape_search, persists to DB

## Self-review

- Price policy (append on change only) implemented and documented ✓
- Only one running scan per saved_search at a time ✓
- Background task uses its own DB session (not request-scoped) ✓
- Scraper selectors verified against live Otomoto pages ✓ (32/32 listings with price+location)
