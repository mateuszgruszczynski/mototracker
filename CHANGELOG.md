# Changelog

## [Iteration 006] — Car Detail & Price-History Chart — 2026-05-16

### Added
- `GET /listings/{otomoto_id}` detail page with metadata grid (year, mileage, fuel, gearbox, location, VIN, seller, first_seen), status badge, and Otomoto external link
- Chart.js line chart of price history (rendered when ≥2 price points exist)
- Scan history table with per-row price delta badges (↑ red / ↓ green)

Retro: iterations/006-car-detail-price-history-chart/i7-retro.md

## [Iteration 005] — Search Results View — 2026-05-16

### Added
- `GET /searches/{id}` results page: sortable table (price/mileage/year) with price-change badges (New/same/↑/↓)
- Home page search names link to results page
- Scan header with timestamp and listing count; empty states

Retro: iterations/005-search-results-view/i7-retro.md

## [Iteration 004] — Scan Execution & Persistence — 2026-05-16

### Added
- Scan, Listing, PricePoint SQLAlchemy models + Alembic migration
- `run_scan()` background task: scrapes Otomoto, upserts listings, appends price_points on price change
- `POST /searches/{id}/scan` with concurrent-scan guard
- Run Scan button on home page; Scanning… state indicator
- Selector fixes: price (h3), params (dd positional), location (li:has-text)

### Fixed
- Country/condition URL filter params dropped (returned 0 results on Otomoto)

Retro: iterations/004-scan-execution-persistence/i7-retro.md

## [Iteration 003] — Otomoto Scraper Engine — 2026-05-16

### Added
- `app/scraper/models.py` — ParsedListing dataclass + ScraperError
- `app/scraper/selectors.py` — centralised Otomoto CSS selectors
- `app/scraper/throttle.py` — AsyncThrottler (≥1s + jitter)
- `app/scraper/robots.py` — RobotsChecker (fetch once, assert_allowed)
- `app/scraper/engine.py` — scrape_search() Playwright loop, check_listing_exists() httpx
- Scraper settings in config: user_agent, throttle params, max_pages

Retro: iterations/003-otomoto-scraper-engine/i7-retro.md

## [Iteration 002] — Saved Searches CRUD — 2026-05-15

### Added
- `SavedSearch` SQLAlchemy model and Alembic migration
- Full CRUD: create, list (sorted by updated_at), edit, delete with browser confirm
- Form validation: name, make, model required; inline error messages
- Home page lists saved searches with edit/delete actions; empty state

Retro: iterations/002-saved-searches-crud/i7-retro.md

## [Iteration 001] — Project Scaffold — 2026-05-15

### Added
- `pyproject.toml` with full stack dependencies (FastAPI, Uvicorn, SQLAlchemy 2.x, Alembic, Jinja2, Pydantic-Settings, Playwright, selectolax, httpx, BeautifulSoup4)
- `app/` package: `main.py`, `config.py`, `db.py`, `models/`, `routes/`, `scraper/`, `templates/`, `static/`
- Alembic initialised with initial migration (`alembic_smoke_test` placeholder table)
- Base Jinja2 template with Tailwind CSS, HTMX, Alpine.js, Chart.js loaded from CDN
- Root route `GET /` serving placeholder home page (HTTP 200)
- `.env.example` with `DATABASE_URL`, `APP_HOST`, `APP_PORT`
- `README.md` with setup and start instructions

Retro: iterations/001-project-scaffold/i7-retro.md
