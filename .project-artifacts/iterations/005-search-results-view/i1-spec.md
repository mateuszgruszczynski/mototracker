# i1-spec.md — Search Results View

## Acceptance Criteria

1. `GET /searches/{id}` renders a page listing all `active` listings for that saved search, sorted by latest price_point descending by default; returns 404 if search not found.
2. Table columns: title (linked to `/listings/{id}`), year, mileage (formatted with spaces), price (formatted with spaces + currency), price-change badge, location, last seen (date only), Otomoto link (external).
3. Price-change badge: `New` (first scan, first_seen_at == last_seen_at), `= same` (re-seen, price unchanged), `↓ −X zł` (price dropped), `↑ +X zł` (price rose). Badge colour: new=blue, same=gray, drop=green, rise=red.
4. Table is client-side sortable by price, mileage, and year using Alpine.js (clicking column header toggles asc/desc).
5. Page header shows the saved search name, last scan timestamp (finished_at of most-recent done scan), and result count; shows "No scan run yet" when no completed scan exists.
6. Home page search rows link to `GET /searches/{id}` (the results page).

**Out of scope:** server-side pagination, filtering within results, export.
