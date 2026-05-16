# i7-retro.md — UI Polish & Navigation

## What went well

- Jinja2's direct access to `request.query_params` made the stateless toast approach clean — no session middleware needed.
- Moving "New Search" to the shared nav removed the duplication that existed between `base.html` and `index.html`.
- All 7 ACs passed on first attempt.

## What could improve

- The toast is only shown after redirecting to `/` (home). Actions on the results or detail pages (e.g. scan trigger) redirect to home, which is acceptable but loses the results-page context. A future iteration could redirect back to the originating page instead.
- `sold_at` and `relisted_from_listing_id` (from E7) are not yet shown on the detail page; E8 addressed nav/layout only.

## Plan changes

None — backlog unchanged. E9 (Scan Progress Streaming) is the last remaining epic.
