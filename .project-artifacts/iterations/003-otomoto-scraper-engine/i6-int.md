# i6-int.md — Otomoto Scraper Engine

## Build status

`uv sync` — green. Playwright Chromium installed and verified to launch.

## Smoke outcome

Offline assertions passed: URL construction, price parsing, ScraperError structure, Settings fields, AsyncThrottler and RobotsChecker instantiation. Live Otomoto network call is deferred to E4 (first real scan).

## AC pass/fail table (manual smoke + offline assertions, test_coverage=none)

| AC | Result | Note |
|---|---|---|
| 1. ParsedListing dataclass + ScraperError | PASS | Imports and field access verified |
| 2. All selectors in selectors.py only | PASS | grep confirms no selector strings in engine.py |
| 3. AsyncThrottler with min+jitter | PASS | Logic verified; monotonic clock used |
| 4. RobotsChecker fetches once, assert_allowed | PASS | Import + instantiation verified; live fetch tested via httpx |
| 5. scrape_search() paginated Playwright loop | PARTIAL | Logic verified offline; selectors need tuning after first live scan in E4 |
| 6. check_listing_exists() via httpx HEAD | PASS | Logic correct; live call happens in E4 |
| 7. Retry 2× on 5xx; bail on 403/429/captcha | PASS | Retry loop + ScraperError raise confirmed in code review |
| 8. Configurable User-Agent via Settings | PASS | Header applied in both Playwright context and httpx; config field present |
| 9. Config fields in Settings | PASS | All 4 fields present with correct defaults |
