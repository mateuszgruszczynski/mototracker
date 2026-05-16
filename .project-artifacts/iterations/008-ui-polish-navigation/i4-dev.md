# i4-dev.md — UI Polish & Navigation

## Files Changed

| File | Change |
|------|--------|
| `app/templates/base.html` | "Searches" nav link, "New Search" moved to nav, max-w-4xl, toast component |
| `app/templates/index.html` | Removed standalone "New Search" button; CSS animate-spin spinner |
| `app/templates/searches/results.html` | Breadcrumb; improved empty states (no scan / zero results) |
| `app/templates/listings/detail.html` | Breadcrumb replacing ← Back link |
| `app/routes/searches.py` | ?toast= appended to all 4 redirect responses |
| `app/routes/listings.py` | Passes `search` object to template context |

## Tasks

- [x] T01 — base.html: Searches link, New Search in nav, max-w-4xl
- [x] T02 — base.html: Alpine.js toast component reading `request.query_params.get("toast")`
- [x] T03 — Routes: ?toast= on create/update/delete/scan redirects
- [x] T04 — results.html: breadcrumb (Home › search.name)
- [x] T05 — results.html: improved empty states
- [x] T06 — index.html: CSS animate-spin spinner replacing plain text
- [x] T07 — listings.py: pass `search` via SavedSearch lookup by listing.saved_search_id
- [x] T08 — detail.html: breadcrumb (Home › search.name › listing title); ← Back removed

## In-process Tests

None (test_coverage=none per policy).

## Key Decisions

- Toast reads `request.query_params.get("toast")` directly in Jinja2; `request` is auto-added to context by Starlette's TemplateResponse.
- `?toast=` uses URL-encoded spaces (`+`) for readability.
- `search` on detail page gracefully falls back (no search breadcrumb segment) when `listing.saved_search_id` is None.

## Self-review

- No security issues: `_toast` value is rendered via Jinja2 auto-escaping (HTML-safe).
- Empty-state emojis used as pure visual decoration (no semantic meaning).
