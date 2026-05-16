# i6-int.md — Scan Execution & Persistence

## Build status

`uv sync` green. All migrations applied.

## Smoke outcome

Live end-to-end scan completed: 32 BMW Seria 3 (2018-2020) listings persisted with 32 price points.
- POST /searches/2/scan → 303 (background task enqueued) ✓
- Scan row: status=done, result_count=32 ✓
- 32 Listing rows + 32 PricePoint rows in DB ✓
- Country/condition URL params removed (Otomoto param encoding incompatible — deferred to retro)

## AC pass/fail table (manual smoke, test_coverage=none)

| AC | Result | Note |
|---|---|---|
| 1. scan/listing/price_point tables via Alembic | PASS | Migration applied; tables confirmed |
| 2. SQLAlchemy models Scan, Listing, PricePoint | PASS | All three models defined and importable |
| 3. POST /searches/{id}/scan starts scan, guards concurrent | PASS | 303 redirect; concurrency guard in place |
| 4. Background scan: scrape, upsert listings, price_points on change | PASS | 32 listings + 32 price_points persisted |
| 5. Home page Run Scan button / Scanning… state | PASS | Button visible; UI updates with running_ids |
| 6. Live Otomoto scrape exercised + selectors adjusted | PASS | Selectors corrected; 32/32 listings parsed |
