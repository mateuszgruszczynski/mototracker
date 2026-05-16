# i1-spec.md — Car Detail & Price-History Chart

## Acceptance Criteria

1. `GET /listings/{otomoto_id}` renders a per-listing detail page; returns 404 if listing not found.
2. Metadata block shows: title, year, mileage (km), fuel, gearbox, location, VIN (or "–"), seller_id (or "–"), Otomoto external link.
3. Status badge: `Active` (green), `Likely sold` (amber), or `Confirmed sold` (red) reflecting `listing.status`.
4. Chart.js line chart: x-axis = observed_at dates, y-axis = price; tooltips show exact price and date; rendered only when ≥2 price_points exist; "Only one price point — no chart yet" shown otherwise.
5. Price history table below chart: one row per price_point (scan date, price, delta vs previous — `–` for first row).

**Out of scope:** editing listing status, comparing multiple listings, predictive analytics.
