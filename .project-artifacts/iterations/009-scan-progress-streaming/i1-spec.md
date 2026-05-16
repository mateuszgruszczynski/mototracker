# i1-spec — Iteration 009: Scan Progress Streaming (SSE)

## Acceptance Criteria

1. **In-process event store** — `app/scraper/events.py` exposes:
   - `scan_queues: dict[int, asyncio.Queue]` — one queue per active scan id.
   - `scan_snapshots: dict[int, dict]` — last-known-state per scan id for late subscribers.
   - Helper `emit(scan_id, event: dict)` that puts to the queue and overwrites the snapshot.
   - Entries are removed from both dicts when a terminal event (`"done"` or `"failed"`) is consumed by the streaming route.

2. **`run_scan` emits progress events** at the following boundaries:
   - After each page of listings is scraped: `{type: "page", page: N, total_pages: N, listings_so_far: N}`.
   - After each re-check completes: `{type: "recheck", checked: N, total_rechecks: N}`.
   - On success: `{type: "done", listings: N}`.
   - On unhandled exception: `{type: "failed", error: "<message>"}`.

3. **`GET /scans/{scan_id}/stream` SSE route** added to `app/routes/searches.py` (or a new `scans.py` router registered in `main.py`):
   - Uses `sse-starlette` (`EventSourceResponse`); package added to `pyproject.toml`.
   - On connect: immediately yields the current snapshot (if any) as the first event, then tails the queue.
   - Closes the response after yielding a terminal (`done`/`failed`) event.
   - Returns HTTP 404 if no queue exists for `scan_id`.

4. **`POST /searches/{search_id}/scan`** returns a redirect to `/searches/{search_id}` (not the home page) and passes the new `scan_id` as a query param: `/searches/{search_id}?scan_id={scan_id}`.

5. **`searches/results.html` progress panel** — when `scan_id` is present in the query string:
   - An Alpine.js component opens `EventSource('/scans/{scan_id}/stream')`.
   - Displays a status bar: `"Page {page} / {total_pages} — {listings_so_far} listings parsed — {checked} / {total_rechecks} re-checks"`.
   - On `done`: shows "Scan complete — {listings} listings" and reloads the page after 1 second.
   - On `failed`: shows the error message inline; does not reload.
   - Panel is hidden when no `scan_id` param is present.

## Out of Scope

- Persistent event log in the database.
- Multiple concurrent subscribers per scan (one SSE client is enough for a prototype).
- WebSocket upgrade path.
- Authentication or per-user isolation of scan streams.
- Automatic retry / exponential back-off beyond browser-native SSE reconnect.
- Unit or integration tests.

## Key Decisions

- **`asyncio.Queue` in-process** — no Redis or broker; the background task and the SSE route share the same event loop within a single Uvicorn worker. Acceptable for a single-worker prototype.
- **Snapshot for late subscribers** — storing the last event dict in `scan_snapshots` satisfies the reconnect-safe requirement without replaying the full history.
- **`sse-starlette`** — preferred over a raw `StreamingResponse` because it handles `text/event-stream` framing, keep-alive pings, and client-disconnect detection out of the box.
- **Redirect carries `scan_id`** — avoids server-side session state; the results page is fully stateless and driven by the URL parameter.
- **Page reload on done** — simplest way to refresh the listing table after a completed scan; no partial DOM update required.
