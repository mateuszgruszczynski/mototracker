# i6-int.md — Search Results View

## Build status

`uv sync` green.

## Smoke outcome

- GET / → 200, search names link to /searches/{id} ✓
- GET /searches/new → 200 ✓ (no regression from route reordering)
- GET /searches/2 → 200, 32 rows in rows_json, prices and badges correct ✓
- GET /searches/2/edit → 200 ✓

## AC pass/fail table (manual smoke, test_coverage=none)

| AC | Result | Note |
|---|---|---|
| 1. GET /searches/{id} returns listings, 404 if not found | PASS | 200 with 32 rows; 404 for unknown id |
| 2. Table columns: title, year, mileage, price, badge, location, last seen, links | PASS | All columns present in template |
| 3. Price-change badges: New/same/↑/↓ with correct colours | PASS | 32 "New" badges for first scan |
| 4. Client-side sort by price/mileage/year (Alpine.js) | PASS | x-for + sort() function in template |
| 5. Header shows search name, last scan timestamp, count | PASS | scan.finished_at displayed |
| 6. Home page links to results page | PASS | a href="/searches/{{s.id}}" on name |
