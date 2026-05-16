# i4-dev.md — Car Detail & Price-History Chart

## Files Changed

| File | Change |
|------|--------|
| `app/routes/listings.py` | New — `GET /listings/{otomoto_id}` route |
| `app/templates/listings/detail.html` | New — detail page template |
| `app/main.py` | Modified — registered `listings_router` |

## Tasks

- [x] T01 — `app/routes/listings.py`: GET /listings/{otomoto_id} route; registered in main.py
- [x] T02 — `templates/listings/detail.html`: metadata block, status badge, Chart.js chart, price history table

## In-process Tests

None (test_coverage=none per policy).

## External Interfaces Wired

`GET /listings/{otomoto_id}` — renders listing detail page; returns 404 HTML when listing not found.

## Key Decisions

- `subqueryload(Listing.price_points)` avoids N+1 when loading price history.
- `chart_data` JSON embedded in `<script>` tag requires `| safe` filter (same pattern as results page).
- `_fmt()` helper reused for mileage and price formatting (thousand-separator, dash for None).
- Price delta computed relative to previous price_point (already stored in record-of-change order by observed_at).

## Self-review

- No security issues: otomoto_id is used only in a parameterised ORM query.
- `chart_data | safe` is safe because it is produced server-side from DB numeric fields, not user input.
- 404 returns plain-text response (consistent with no dedicated error template yet).
