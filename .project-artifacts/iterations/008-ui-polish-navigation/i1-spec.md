# i1-spec.md — UI Polish & Navigation

## Acceptance Criteria

1. **Top nav "Searches" link.** `base.html` nav bar includes a "Searches" link (`href="/"`) alongside the existing brand link. The "New Search" button moves into the nav bar at the right end so it is available from every page.

2. **Breadcrumbs on results page.** `searches/results.html` renders a breadcrumb row above the page heading: `Home > {search.name}`. Each segment is a link except the last.

3. **Breadcrumbs on detail page.** `listings/detail.html` renders: `Home > {search.name} > {listing.title or listing.id}`. The detail route receives `search` in its template context (currently it does not — the route must look it up via `listing.saved_search_id`). The existing `← Back` link is removed.

4. **Improved empty state on results page.** When `last_scan` is `None`, replace the plain amber text with a styled empty-state block: centred icon placeholder, heading "No scan yet", subtext "Run a scan to fetch listings", and the existing "Run Scan" button. When `last_scan` exists but `total == 0`, replace the plain `<p>` with a styled block: heading "No active listings", subtext "All listings may have been sold or the search returned no results."

5. **Scanning spinner on home page.** In `index.html`, replace the `"Scanning…"` text span with a flex row containing a CSS `animate-spin` border-spinner div and the label "Scanning…". No JavaScript polling — the spinner is purely CSS.

6. **Toast notifications.** `base.html` includes an Alpine.js toast component anchored bottom-right. Pages that redirect after a write action pass a `?toast=<message>` query parameter on the redirect URL. The base template reads `request.query_params.get("toast")` via a Jinja2 context variable injected by a `base_context` helper and auto-shows the toast for 3 seconds. Actions covered: create search ("Search created"), update search ("Search updated"), delete search ("Search deleted"), scan triggered ("Scan started").

7. **Consistent max-width.** `base.html` `<main>` uses `max-w-4xl mx-auto px-4 py-8` (currently `max-w-5xl`). The results table wrapper already has `overflow-x-auto`; verify it is on the outermost container so the table scrolls horizontally on narrow viewports without breaking the page layout.

## Out of scope

Dark mode, pagination, real-time scan progress via WebSocket/SSE, accessibility audit beyond semantic HTML, search filtering/sorting persistence across page loads.

## Key decisions

- **Toast via query param, not session/cookie.** No session middleware is installed; a `?toast=` param on the redirect is the simplest stateless approach compatible with existing `RedirectResponse(status_code=303)` calls.
- **Spinner is pure CSS, no polling.** The home page already tracks running scans server-side via `running_ids`; a CSS `animate-spin` div is sufficient visual feedback without adding HTMX polling complexity.
- **Breadcrumb search context on detail page requires a one-line ORM lookup**, not a new route parameter, since `listing.saved_search_id` is already on the model.
- **`max-w-4xl` replaces `max-w-5xl`** to match the width used by most content cards throughout the app.
