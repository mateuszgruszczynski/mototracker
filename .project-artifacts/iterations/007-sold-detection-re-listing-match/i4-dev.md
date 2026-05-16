# i4-dev.md — Sold Detection & Re-listing Match

## Files Changed

| File | Change |
|------|--------|
| `app/models/listing.py` | Added `sold_at`, `relisted_from_listing_id` fields |
| `alembic/versions/3709240f77e9_add_sold_at_relisted_from_listing_id.py` | New migration |
| `app/scraper/engine.py` | `check_listing_exists` accepts optional `throttler` param |
| `app/scraper/persist.py` | Re-check loop, re-activation logic, fuzzy match |

## Tasks

- [x] T01 — Migration: `sold_at`, `relisted_from_listing_id` columns
- [x] T02 — Listing ORM model updated
- [x] T03 — Re-check disappeared listings; `confirmed_sold` / `likely_sold` outcomes
- [x] T04 — Re-appearing listings reset to `active`, `sold_at` cleared
- [x] T05 — Fuzzy match (make+model+year+mileage_bucket+seller_id) sets `relisted_from_listing_id`

## In-process Tests

None (test_coverage=none per policy).

## External Interfaces Wired

No new HTTP routes. `check_listing_exists` signature updated to accept optional `AsyncThrottler`.

## Key Decisions

- SQLite does not support ALTER to add FK constraints; `relisted_from_listing_id` is a logical FK (column only, no DB constraint). Migration stamped after partial apply of the previous failed run.
- Re-check throttler is a fresh `AsyncThrottler` instance; doesn't share state with the Playwright throttler.
- `seen_ids` set built during upsert loop; disappeared query uses `notin_` for efficiency.
- Fuzzy match index built before the upsert loop to avoid repeated queries.
- Re-check errors are caught per-listing; scan succeeds even if some re-checks fail.

## Self-review

- No security issues: all DB queries use parameterised ORM filters.
- `notin_` on a large set is acceptable for SQLite at prototype scale.
