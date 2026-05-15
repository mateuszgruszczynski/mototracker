# Epic Backlog — MotoTracker

## Backlog (prioritized)

| # | Priority | Epic | Type | Size | Status | Depends on |
|---|---|---|---|---|---|---|
| E1 | P1 | Project Scaffold | INFRA | S | TODO | — |
| E2 | P1 | Saved Searches CRUD | FEATURE | S | TODO | E1 |
| E3 | P1 | Otomoto Scraper Engine | FEATURE | L | TODO | E1 |
| E4 | P1 | Scan Execution & Persistence | FEATURE | M | TODO | E1, E2, E3 |
| E5 | P1 | Search Results View | FEATURE | S | TODO | E4 |
| E6 | P1 | Car Detail & Price-History Chart | FEATURE | M | TODO | E4 |
| E7 | P1 | Sold Detection & Re-listing Match | FEATURE | M | TODO | E3, E4 |
| E8 | P2 | UI Polish & Navigation | DESIGN | S | TODO | E5, E6 |
| E9 | P2 | Scan Progress Streaming (SSE) | FEATURE | S | TODO | E4 |

---

## E1 — Project Scaffold  *(INFRA, P1, S)*
FastAPI app skeleton, SQLAlchemy + Alembic, SQLite, Jinja2/HTMX/Tailwind wiring, base layout, `uv` deps, devcontainer integration.

**Scenarios**
- As the dev, I can `uv run uvicorn` inside the container and the app serves a placeholder home page on `127.0.0.1:8000`.
- As the dev, I can run `alembic upgrade head` and a SQLite file is created.

**ACs**
- App boots; root route returns 200.
- SQLAlchemy session works; one trivial table exists via Alembic migration.
- Base Jinja layout includes Tailwind, HTMX, Alpine, Chart.js (CDN).
- Project structured: `app/{main.py, db.py, models/, routes/, scraper/, templates/, static/}`.

**Out of scope:** any business logic, scraping, real schema.

**Risks:** Playwright install in container can be slow/brittle — defer Playwright bring-up to E3 if it blocks scaffold.

---

## E2 — Saved Searches CRUD  *(FEATURE, P1, S)*
Define, list, edit, delete saved searches with v1 filters (make, model, year_from, year_to, country_of_origin=Poland, condition=not damaged).

**Scenarios**
- I can create a saved search "BMW Seria 3 2015–2020, PL, not damaged".
- I can see all my saved searches on the home page with last-scan info.
- I can delete a saved search.

**ACs**
- Form validates required fields (make, model).
- `saved_search` row created; listed on home page sorted by `updated_at` desc.
- Delete is confirmed and cascades to scans/listings via FK rules (or soft delete — TBD in Refinement).

**Out of scope:** scheduling, sharing, import/export.

**Risks:** make/model selection UX — free text vs dropdown sourced from Otomoto's taxonomy. Defer to Refinement.

---

## E3 — Otomoto Scraper Engine  *(FEATURE, P1, L)*
Headless Playwright engine that fetches Otomoto search-result pages (paginated) and listing detail pages, parsing the relevant fields. Centralised selectors. Polite throttling, retries, UA, error handling. Detail re-check via httpx where the page is plain HTML.

**Scenarios**
- Given a saved-search filter set, the engine returns a list of parsed listings (id, url, title, price, currency, year, mileage, fuel, gearbox, location, VIN if shown, seller_id).
- Given an Otomoto listing URL, the engine returns its current parsed state or `not_found`.

**ACs**
- All Otomoto-specific HTML/JSON selectors live in one module.
- Throttle ≥ 1 s between requests; configurable; jitter applied.
- Retries 2× on 5xx; gives up on 403/429/captcha and emits a structured error.
- Identifiable, configurable user agent. Honour `robots.txt` for excluded paths.
- Parses paginated search results until exhausted or a configurable max-pages cap.

**Out of scope:** other portals; bypassing captchas; logged-in features.

**Risks:** Otomoto anti-bot may block headless Chromium; may need stealth tweaks. Listing detail layouts vary. VIN often hidden behind "show".

---

## E4 — Scan Execution & Persistence  *(FEATURE, P1, M)*
Trigger a scan for a saved search; persist a `scan` row; for each parsed listing, upsert into `listing` and append a `price_point`. Dedupe by Otomoto ID first.

**Scenarios**
- I click "Run scan" on a saved search; a scan starts; when finished I see the result count.
- A second scan on the same search appends new price points for re-seen cars and adds new cars as needed.

**ACs**
- `scan` row tracks `started_at`, `finished_at`, `status` (`running` | `done` | `failed`), `result_count`, `error_summary`.
- For each parsed listing: existing → update `last_seen_at` + append `price_point` (skip if price unchanged from latest stored point — record-of-change semantics is TBD in Refinement).
- For each parsed listing: new → insert `listing` (status=`active`) and a first `price_point`.
- Scans run in background (FastAPI BackgroundTasks/asyncio); only one scan per saved search at a time.

**Out of scope:** sold detection (E7), real-time progress UI (E9), parallel multi-search scans.

**Risks:** "price unchanged" policy — append every point vs only on change — decide in Refinement.

---

## E5 — Search Results View  *(FEATURE, P1, S)*
Per-saved-search page showing the **latest-scan snapshot** as a table of listings with price-change badges relative to the previous scan.

**Scenarios**
- I open a saved search and see a table of currently-active listings with current price, mileage, year, link to the Otomoto ad, and link to the in-app car detail.
- For each row I see a badge: `new`, `↓ -1 200 zł`, `↑ +500 zł`, or `=`.

**ACs**
- Table columns: title, year, mileage, price, change badge, location, last seen, in-app detail link, Otomoto link.
- Sortable by price / mileage / year.
- Shows the scan timestamp and result count at the top.
- Empty state when no scan has run yet.

**Out of scope:** filters/search inside the results table, exports, market analytics aggregates.

**Risks:** large result sets (>500) — pagination or virtual scrolling TBD.

---

## E6 — Car Detail & Price-History Chart  *(FEATURE, P1, M)*
Per-listing page showing metadata + a line chart of price over time + status (active / likely_sold / confirmed_sold) + scan history.

**Scenarios**
- I open a car from a results table and see all its metadata and a price-history chart with one point per scan.
- I see when the car was first seen, last seen, and its current status.

**ACs**
- Chart.js line chart, x = observed_at, y = price; tooltip shows exact value and date.
- Metadata block: title, year, mileage, fuel, gearbox, location, VIN (if known), seller, Otomoto URL.
- Status badge reflects current `status` field.
- Scan-history list: timestamp, price, delta.

**Out of scope:** chart for multiple cars overlaid, predictive analytics.

**Risks:** none significant; depends on having ≥2 price points for the chart to be interesting.

---

## E7 — Sold Detection & Re-listing Match  *(FEATURE, P1, M)*
After each scan: any previously-`active` listing **not seen** in this scan's results is re-checked via its detail URL. 404/missing → `confirmed_sold`. Still present → keep `active` (means it dropped out of filter results — log it). Re-listings detected via fuzzy key (make+model+year+mileage_bucket+seller) inherit price history.

**Scenarios**
- A listing seen in scan #1 is gone in scan #2; detail re-check returns 404 → marked `confirmed_sold` with `sold_at` ≈ scan #2 timestamp.
- A listing seen in scan #1 is gone in scan #2 but its detail page still loads → marked `likely_sold` (out of filter, perhaps moved).
- A new listing in scan #3 fuzzy-matches a `confirmed_sold` listing → linked as re-listing; price history retained.

**ACs**
- New columns/states: `listing.status ∈ {active, likely_sold, confirmed_sold}`, `sold_at`, `relisted_from_listing_id`.
- Re-check honours scraper throttle.
- Fuzzy match policy documented in code; conservative (no false merges).

**Out of scope:** seller-specific dashboards, manual override UI (could be P2 later).

**Risks:** false positives on disappearance (Otomoto pagination flakiness) — mitigated by `likely_sold` intermediate state. Fuzzy match accuracy.

---

## E8 — UI Polish & Navigation  *(DESIGN, P2, S)*
Consistent Tailwind layout: top nav (Home, Searches), breadcrumbs, empty states, loading spinners, toast notifications, mobile-acceptable widths.

**Scenarios**
- I always see a top nav and can jump between Home and a saved search in one click.
- When a scan is running, I see a clear indicator without needing to refresh.

**ACs**
- Single base template; all pages extend it.
- Consistent typography and spacing scale.
- Empty states for: no saved searches, no scans yet, no results.
- Toast component for success/failure.

**Out of scope:** dark mode, custom branding, animations.

**Risks:** none.

---

## E9 — Scan Progress Streaming (SSE)  *(FEATURE, P2, S)*
While a scan runs, stream progress events (pages fetched, listings parsed, listings re-checked, errors) to the running-saved-search page over Server-Sent Events.

**Scenarios**
- I click "Run scan" and watch a live counter: "Page 3 / 7 — 42 listings parsed — 2 re-checks pending".
- If scraping fails, I see the failure inline.

**ACs**
- SSE endpoint per active scan id.
- Progress events emitted at meaningful boundaries (page complete, re-check complete, terminal).
- Reconnect-safe: late subscribers get the current state.

**Out of scope:** WebSockets, multi-tab sync, push notifications.

**Risks:** Async coordination between scrape coroutine and SSE subscribers — keep it dead simple.
