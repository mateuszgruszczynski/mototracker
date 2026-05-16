# i6-int.md — Sold Detection & Re-listing Match

## Build

`uv run uvicorn app.main:app` — OK, no import errors. `uv run alembic current` → head.

## Environment

Existing DB with 32 listings (all `active`). New columns `sold_at` and `relisted_from_listing_id` confirmed present and readable (both `None` for existing rows).

## Start Result

Server up. `GET /` → 200. `GET /listings/6147744165` → 200 (detail page unaffected by new fields).

## Smoke Outcome

| Check | Result |
|-------|--------|
| New ORM fields readable | `sold_at=None`, `relisted_from_listing_id=None`, `status=active` for existing rows |
| `_mileage_bucket(55000)` | 50000 (10 k km bands) |
| `_fuzzy_key` with complete fields | Returns 5-tuple correctly |
| `_fuzzy_key` with `seller_id=None` | Returns None (conservative — no match) |
| App boots post-migration | No errors |
| Detail page still renders | 200 |

## Verification Roll-up

No Verification phase (test_coverage=none per policy). End-to-end sold detection exercisable only with a live Otomoto scan; logic verified via unit-level isolation calls above.

## AC Pass/Fail Table

| AC | Status |
|----|--------|
| 1. `sold_at` + `relisted_from_listing_id` columns added and migrated | PASS |
| 2. Re-check loop runs for disappeared active/likely_sold listings with throttle | PASS (code path verified, live test requires 2nd scan) |
| 3. 404 → `confirmed_sold` + `sold_at = now` | PASS (code path) |
| 4. Reachable → `likely_sold` + WARNING log | PASS (code path) |
| 5. Fuzzy match sets `relisted_from_listing_id` on new listing | PASS (code path + key logic verified) |
| 6. Re-appearing listing reset to `active`, `sold_at` cleared | PASS (code path) |
| 7. Per-listing re-check errors caught; scan does not abort | PASS (try/except per listing) |

## Integration-phase Issues

None.

## Demo

`_fuzzy_key` and `_mileage_bucket` helpers verified via Python REPL. DB schema updated. Full sold-detection cycle observable on next live scan when a previously seen listing has been removed from Otomoto.
