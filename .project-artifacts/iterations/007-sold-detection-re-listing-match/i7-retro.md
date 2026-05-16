# i7-retro.md — Sold Detection & Re-listing Match

## What went well

- Re-check throttler pattern (fresh instance per phase) is clean and doesn't interfere with the Playwright throttler.
- `notin_` query for disappeared listings is concise; fuzzy-match index built upfront avoids N+1.
- All 7 ACs covered in code; conservative fuzzy match (all 5 fields required) avoids false merges.

## What could improve

- SQLite FK constraint limitation required a manual `alembic stamp` after a partially-applied migration. A batch migration with copy-and-move would be cleaner for future schema changes.
- `sold_at` and `relisted_from_listing_id` are not yet surfaced in the detail page UI (out of scope for this iteration; E8 UI Polish can expose them).

## Plan changes

None — backlog unchanged.
