# i1-spec.md — Scan Execution & Persistence

## Acceptance Criteria

1. Alembic migration creates three tables: `scan` (id, saved_search_id FK, started_at, finished_at, status [`running`|`done`|`failed`], result_count, error_summary); `listing` (id string PK = Otomoto ID, saved_search_id FK, make, model, year, mileage, fuel, gearbox, vin, seller_id, url, title, location, first_seen_at, last_seen_at, status [`active`|`likely_sold`|`confirmed_sold`]); `price_point` (id, listing_id FK, scan_id FK, price, currency, observed_at).
2. SQLAlchemy models `Scan`, `Listing`, `PricePoint` defined in `app/models/`.
3. `POST /searches/{id}/scan` starts a background scan via FastAPI `BackgroundTasks`; returns 303 redirect to `/`; if a scan is already `running` for this search, redirects without starting a new one.
4. Background scan function: calls `scrape_search(filters)`, upserts each `ParsedListing` into `listing` (insert new / update `last_seen_at` for existing), appends a `price_point` only when the price differs from the most-recent stored point (or when there is no prior point); updates `scan.result_count` and `scan.status = "done"` on completion; on unhandled exception sets `status = "failed"` with `error_summary`.
5. Home page shows a "Run Scan" button for each saved search; existing scan rows on the page are limited to what's needed for the button state.
6. The live Otomoto scrape is exercised during integration (first real scan run) and selectors adjusted if needed.

**Out of scope:** sold detection (E7), real-time progress (E9), parallel scans, scan history view (E5).
**Price policy decision:** store `price_point` only on price change or first observation (record-of-change semantics).
