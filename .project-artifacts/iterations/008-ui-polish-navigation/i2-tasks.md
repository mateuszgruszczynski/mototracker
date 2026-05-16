# i2-tasks.md — UI Polish & Navigation

## Tasks

- [x] T01 — DESIGN — `base.html`: add "Searches" nav link + move "New Search" button into nav; change `max-w-5xl` → `max-w-4xl` on `<main>`
- [x] T02 — DESIGN — `base.html`: Alpine.js toast component; `toast` context var injected from query param
- [x] T03 — DEV — `app/routes/__init__.py` (home) + `app/routes/searches.py`: pass `toast` context and append `?toast=` to redirect URLs on create/update/delete/scan
- [x] T04 — DESIGN — `searches/results.html`: breadcrumb row (Home > search.name)
- [x] T05 — DESIGN — `searches/results.html`: improved empty states (no scan yet / scan ran, zero results)
- [x] T06 — DESIGN — `index.html`: replace "Scanning…" text with CSS animate-spin spinner
- [x] T07 — DEV — `app/routes/listings.py`: pass `search` object to template context
- [x] T08 — DESIGN — `listings/detail.html`: replace `← Back` with breadcrumb (Home > search.name > title); remove back link
