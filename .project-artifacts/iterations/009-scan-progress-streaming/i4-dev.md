# i4-dev.md — Scan Progress Streaming (SSE)

## Files Changed

| File | Change |
|------|--------|
| `pyproject.toml` | Added `sse-starlette>=3.4.4` |
| `app/scraper/events.py` | New — in-process store (`scan_queues`, `scan_snapshots`, `emit`, `cleanup`) |
| `app/scraper/engine.py` | `scrape_search` converted to async generator yielding `(page_num, page_listings)` |
| `app/scraper/persist.py` | `run_scan` accepts optional pre-created `Scan`; emits page/recheck/done/failed events; consumes async generator |
| `app/routes/scans.py` | New — `GET /scans/{scan_id}/stream` SSE route |
| `app/routes/searches.py` | Scan trigger creates Scan row upfront, inits queue, passes scan to background task, redirects to `/searches/{id}?scan_id={id}` |
| `app/main.py` | Registers `scans_router` |
| `app/templates/searches/results.html` | Alpine.js `scanProgress` component + progress panel |

## Tasks

- [x] T01 — sse-starlette added
- [x] T02 — events.py: in-process store + emit/cleanup
- [x] T03 — persist.py: page/recheck/done/failed events; async generator consumption
- [x] T04 — scans.py: SSE route with snapshot replay, queue tail, terminal close, 404
- [x] T05 — searches.py: redirect to results page with scan_id param
- [x] T06 — results.html: Alpine.js progress panel with live counters, done reload, error display

## In-process Tests

None (test_coverage=none per policy).

## External Interfaces Wired

`GET /scans/{scan_id}/stream` — `text/event-stream` SSE endpoint.

## Key Decisions

- `scrape_search` converted to async generator so persist.py can emit per-page events inline without coupling the engine to the event store.
- Scan row pre-created in the route before handing off to the background task — ensures SSE client can connect immediately after redirect.
- `scan_queues[scan_id]` initialised in the route; background task merges the pre-created scan into its own session via `db.merge()`.
- `asyncio.wait_for` with 30 s timeout in SSE generator produces keepalive comments without blocking.

## Self-review

- No security issues: `scan_id` is an integer from the DB row; SSE route just reads from an in-process dict.
- In-process state is process-local; fine for single-worker Uvicorn prototype.
