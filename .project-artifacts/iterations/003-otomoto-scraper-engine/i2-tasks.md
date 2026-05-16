# i2-tasks.md — Otomoto Scraper Engine

## Tasks

- [x] T01 — DEV — `app/scraper/models.py`: ParsedListing dataclass + ScraperError exception
- [x] T02 — DEV — `app/config.py` updated: scraper_user_agent, throttle_min_seconds, throttle_jitter_seconds, scraper_max_pages
- [x] T03 — DEV — `app/scraper/selectors.py`: all Otomoto CSS selectors for search-result listings and pagination
- [x] T04 — DEV — `app/scraper/throttle.py`: AsyncThrottler enforcing min delay + jitter
- [x] T05 — DEV — `app/scraper/robots.py`: RobotsChecker fetching robots.txt once; is_allowed(url) guard
- [x] T06 — DEV — `app/scraper/engine.py`: scrape_search() paginated Playwright loop + check_listing_exists() via httpx
