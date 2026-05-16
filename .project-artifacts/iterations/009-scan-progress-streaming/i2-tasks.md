# i2-tasks.md — Scan Progress Streaming (SSE)

## Tasks

- [x] T01 — DEV — Add `sse-starlette` to `pyproject.toml`; `uv sync`
- [x] T02 — DEV — `app/scraper/events.py`: in-process store (`scan_queues`, `scan_snapshots`, `emit()`)
- [x] T03 — DEV — `app/scraper/persist.py`: call `emit()` at page/recheck/done/failed boundaries; pass max_pages into scrape_search or count pages internally
- [x] T04 — DEV — `app/routes/scans.py`: `GET /scans/{scan_id}/stream` SSE route using EventSourceResponse; snapshot replay + queue tail + terminal close; register in `main.py`
- [x] T05 — DEV — `app/routes/searches.py`: redirect scan trigger to `/searches/{search_id}?scan_id={scan_id}` instead of `/`
- [x] T06 — DESIGN — `searches/results.html`: Alpine.js progress panel driven by `scan_id` query param; EventSource, live counters, reload on done, error on failed
