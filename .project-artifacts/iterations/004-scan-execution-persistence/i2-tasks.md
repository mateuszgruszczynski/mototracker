# i2-tasks.md — Scan Execution & Persistence

## Tasks

- [x] T01 — DEV — `app/models/scan.py`, `app/models/listing.py`, `app/models/price_point.py`: SQLAlchemy models with all columns and FKs
- [x] T02 — DEV — `app/models/__init__.py` updated to import all new models; Alembic migration generated and applied
- [x] T03 — DEV — `app/scraper/persist.py`: `run_scan(saved_search_id, db)` async function — calls scrape_search, upserts listings, appends price_points on change, updates scan status
- [x] T04 — DEV — `app/routes/searches.py` extended: `POST /searches/{id}/scan` — guard against concurrent scans, enqueue background task
- [x] T05 — DESIGN — Home page updated: "Run Scan" button per row; shows "Scanning…" state when scan is running (using scan status from DB)
