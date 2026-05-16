# i1-spec.md — Otomoto Scraper Engine

## Acceptance Criteria

1. `app/scraper/models.py` defines `ParsedListing` dataclass (fields: `otomoto_id`, `url`, `title`, `price`, `currency`, `year`, `mileage`, `fuel`, `gearbox`, `location`, `vin`, `seller_id`) and `ScraperError` exception with a `details` dict.
2. `app/scraper/selectors.py` contains all Otomoto-specific CSS selectors and attribute names; no selector strings defined in any other scraper file.
3. `app/scraper/throttle.py` provides `AsyncThrottler` that enforces ≥ `throttle_min_seconds` (from Settings, default 1.0) between requests, with random jitter up to `throttle_jitter_seconds` (default 1.0).
4. `app/scraper/robots.py` provides `RobotsChecker` that fetches `robots.txt` from `otomoto.pl` once per session and exposes `is_allowed(url) -> bool`; blocked URLs raise `ScraperError`.
5. `app/scraper/engine.py` provides `async scrape_search(filters: dict, session: AsyncBrowserSession) -> list[ParsedListing]`: paginates through Otomoto search results until no next-page or `max_pages` (from Settings, default 20) reached; applies throttle between pages.
6. `app/scraper/engine.py` provides `async check_listing_exists(url: str) -> bool`: uses httpx HEAD to check if the listing URL is still reachable (2xx = True, 404 = False).
7. On 5xx response, the scraper retries up to 2 times with exponential back-off; on 403/429 or captcha detection (title contains known captcha strings) raises `ScraperError({"code": "blocked", ...})`.
8. All requests use a configurable `User-Agent` header (Settings `scraper_user_agent`, default `"MotoTracker/0.1"`); applied via both Playwright and httpx.
9. `app/config.py` exposes: `scraper_user_agent`, `throttle_min_seconds`, `throttle_jitter_seconds`, `scraper_max_pages`.

**Out of scope:** other portals, captcha bypass, logged-in features, parallel multi-search scraping, `scrape_listing_detail` full parse (added when E4 needs it).
