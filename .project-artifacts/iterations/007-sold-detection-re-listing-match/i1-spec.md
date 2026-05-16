# i1 — Sold Detection & Re-listing Match

## Acceptance Criteria

1. **New columns exist and are migrated.** A 4th Alembic migration adds `listing.sold_at` (DateTime timezone-aware, nullable) and `listing.relisted_from_listing_id` (String FK → `listing.id`, nullable, `ondelete=SET NULL`). The `Listing` ORM model is updated accordingly.

2. **Disappeared listings are re-checked after each scan.** After `run_scan` commits the upsert loop, it queries all `active` and `likely_sold` listings for that `saved_search_id` whose `id` is not in the current scan's result set, then calls `check_listing_exists(listing.url)` for each, using the existing `AsyncThrottler` (re-instantiated or passed in) so the throttle rate is respected.

3. **404 → `confirmed_sold`.** If `check_listing_exists` returns `False`, set `listing.status = "confirmed_sold"` and `listing.sold_at` = scan timestamp (`now`).

4. **Still reachable → `likely_sold`.** If `check_listing_exists` returns `True` (page loads, just dropped out of filter results), set `listing.status = "likely_sold"` and log at WARNING level: listing id, url, and scan id.

5. **Re-listing fuzzy match.** When a new listing is inserted, before creating it, attempt a fuzzy match against `confirmed_sold` listings under the same `saved_search_id`. Match key: `make + model + year + mileage_bucket + seller_id`. Mileage bucket = `floor(mileage / 10000) * 10000` (10 k km bands). All five key fields must be non-null and equal for a match to fire. On match, set `new_listing.relisted_from_listing_id = matched.id`; price history is inherited implicitly (both listings share no rows — the existing rows stay on the old listing, which is by design; the FK allows the API to walk the chain).

6. **`status` field is actively maintained.** Any listing seen in the current scan that previously had status `likely_sold` or `confirmed_sold` is reset to `active` and `sold_at` is cleared to `None`.

7. **No scan-level failure on re-check errors.** A network error during `check_listing_exists` for a single listing is caught, logged at WARNING, and skipped; it does not abort the scan or roll back the main upsert commit.

## Out of scope

Re-checking listings belonging to other `saved_search_id`s; scraping the detail page for additional data; surfacing `relisted_from_listing_id` through API routes; de-duplicating across saved searches.

## Key decisions

- **Re-check uses `httpx` HEAD (existing `check_listing_exists`), not Playwright.** Fast and sufficient; full render not needed to detect 404. Throttle still applied to avoid hammering the server.
- **Fuzzy match is exact on all five fields, never partial.** Conservative by design — a missing `seller_id` or `mileage` on either side disqualifies the match entirely, preventing false merges.
- **Mileage bucket width is 10 000 km.** Balances tolerance for minor mileage corrections against accidental merges of distinct cars.
- **Re-check runs sequentially after the main commit.** Keeps the upsert transaction short; re-check failures cannot corrupt price history already written.
- **`AsyncThrottler` is instantiated fresh for the re-check loop** (same settings from `settings.throttle_*`); it does not share state with the Playwright scrape throttler, which has already been disposed.
