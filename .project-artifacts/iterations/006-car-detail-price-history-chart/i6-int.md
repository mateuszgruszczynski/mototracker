# i6-int.md — Car Detail & Price-History Chart

## Build

`uv run uvicorn app.main:app` — OK, no import errors.

## Environment

Dev DB at `./data/mototracker.db` with listings from a previous live scan (iteration 004). No new migrations required.

## Start Result

Server started cleanly. All three routers registered without conflict.

## Smoke Outcome

| Check | Result |
|-------|--------|
| `GET /` | 200 |
| `GET /listings/6147744165` | 200 — title, year, mileage, fuel, gearbox, location, VIN, seller, first_seen rendered |
| Status badge | "Active" (green) |
| Otomoto external link | present, correct URL |
| Single price point | "Only one price point — no chart yet." shown |
| ≥2 price points (manual seed) | `<canvas id="priceChart">` rendered; chart_data JSON inlined correctly |
| Price history table | rows with date, price_fmt, delta_fmt (↓ −99 000 PLN, green badge) |
| `GET /listings/nonexistent999` | 404 |

## Verification Roll-up

No Verification phase (test_coverage=none per policy).

## AC Pass/Fail Table

| AC | Status |
|----|--------|
| 1. GET /listings/{id} renders detail page; 404 when not found | PASS |
| 2. Metadata block: title, year, mileage, fuel, gearbox, location, VIN, seller_id, external link | PASS |
| 3. Status badge: Active/Likely sold/Confirmed sold with correct colour | PASS |
| 4. Chart.js line chart when ≥2 points; "only one" message otherwise | PASS |
| 5. Price history table with delta vs previous | PASS |

## Integration-phase Issues

None.

## Demo

`GET /listings/6147744165` — BMW Seria 3 330i Luxury Line detail page with metadata grid, status badge, Chart.js price-history chart, and scan-history table with green delta badge.
