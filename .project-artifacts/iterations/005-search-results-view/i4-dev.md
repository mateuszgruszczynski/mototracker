# i4-dev.md — Search Results View

## Files changed

Added:
- `app/templates/searches/results.html` — results table, Alpine.js sort, badge rendering, scan header, empty state

Modified:
- `app/routes/searches.py` — added GET /{search_id} results route; reordered routes (literal /new before /{search_id}); _badge() helper
- `app/templates/index.html` — search name linked to /searches/{id}

## In-process tests

None — test_coverage=none per policy.

## External interfaces wired

- `GET /searches/{id}` — returns HTML with rows_json embedded for Alpine.js

## Self-review

- Route ordering: /new registered before /{search_id} to prevent int parse error ✓
- JSON must use `| safe` filter in Jinja2 to avoid HTML escaping ✓ (found and fixed during integration)
- 32 rows with correct prices, mileage, badge values confirmed ✓
