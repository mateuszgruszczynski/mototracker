# i4-dev.md — Otomoto Scraper Engine

## Files changed

Added:
- `app/scraper/models.py` — ParsedListing dataclass (12 fields) + ScraperError(details: dict)
- `app/scraper/selectors.py` — all Otomoto CSS selectors, BASE_URL, SEARCH_PATH, PARAM_LABEL_MAP, CAPTCHA_INDICATORS
- `app/scraper/throttle.py` — AsyncThrottler: enforces min_seconds + uniform jitter, monotonic clock
- `app/scraper/robots.py` — RobotsChecker: fetches robots.txt once per host via httpx, stdlib RobotFileParser, assert_allowed()
- `app/scraper/engine.py` — _build_search_url(), _parse_price(), _navigate_with_retry() (2× retry on 5xx, raise on 403/429/captcha), _parse_listings_from_page(), scrape_search(), check_listing_exists()

Modified:
- `app/config.py` — added scraper_user_agent, throttle_min_seconds, throttle_jitter_seconds, scraper_max_pages
- `.env.example` — documented new scraper settings
- `.devcontainer/devcontainer.json` — postCreateCommand now runs uv sync + playwright install chromium

## In-process tests

None — test_coverage=none per policy.

## External interfaces wired

- `scrape_search(filters: dict) -> list[ParsedListing]` — async; consumes Playwright; no HTTP routes yet
- `check_listing_exists(url: str) -> bool` — async; httpx HEAD; no HTTP routes yet
Both will be called from E4 (Scan Execution).

## Self-review

- All selectors in selectors.py only ✓
- Throttle enforced on every page navigation ✓
- robots.txt fetched once per session (host cache) ✓
- Retry 2× on 5xx; bail on 403/429/captcha with ScraperError ✓
- User-agent configurable via Settings ✓
- No hardcoded credentials ✓
- Note: selectors are best-effort based on known Otomoto structure; may need tuning after first live test in E4
