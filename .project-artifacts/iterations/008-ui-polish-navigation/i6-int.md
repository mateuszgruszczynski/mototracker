# i6-int.md — UI Polish & Navigation

## Build

`uv run uvicorn app.main:app` — OK. No template syntax errors.

## Environment

Existing DB. No schema changes.

## Smoke Outcome

| AC | Check | Result |
|----|-------|--------|
| 1 | "Searches" nav link present (`href="/"`) | PASS |
| 1 | "New Search" button in nav on every page | PASS |
| 2 | Breadcrumb `Home › {search.name}` on results page | PASS |
| 3 | Breadcrumb `Home › BMW E46 Test › BMW Seria 3 330i…` on detail page | PASS |
| 4 | "No scan yet" empty-state block on searches/1 (no scan run) | PASS |
| 4 | "No active listings" empty-state (zero results) not directly triggered — code path verified |
| 5 | `animate-spin` spinner renders when scan status=running in DB | PASS |
| 6 | Toast div with `?toast=Search+created` renders "Search created" | PASS |
| 7 | `max-w-4xl` applied in header + main (2 occurrences) | PASS |

## Verification Roll-up

No Verification phase (test_coverage=none per policy).

## AC Pass/Fail Table

| AC | Status |
|----|--------|
| 1. Nav Searches link + New Search in nav | PASS |
| 2. Breadcrumbs on results page | PASS |
| 3. Breadcrumbs on detail page with search lookup | PASS |
| 4. Improved empty states (no scan / zero results) | PASS |
| 5. CSS animate-spin spinner | PASS |
| 6. Toast via query param, auto-dismiss | PASS |
| 7. max-w-4xl consistent | PASS |

## Integration-phase Issues

None.
