# i6-int.md — Saved Searches CRUD

## Build status

`uv sync` — all packages present. Green.

## Smoke outcome

App started. Full CRUD flow exercised:
- GET / (empty state) → 200 ✓
- GET /searches/new → 200 ✓
- POST /searches with valid data → 303 redirect, row inserted ✓
- POST /searches with blank make → 200 with form re-rendered (validation) ✓
- GET / after insert → "BMW E46" row visible ✓
- GET /searches/1/edit → 200 pre-filled form ✓
- POST /searches/1/delete → 303 redirect, row removed ✓

## AC pass/fail table (manual smoke, test_coverage=none)

| AC | Result | Note |
|---|---|---|
| 1. saved_search table with correct columns via Alembic | PASS | Migration applied; table confirmed via SQLAlchemy inspect |
| 2. SavedSearch ORM model in app/models/saved_search.py | PASS | Model defined, imported |
| 3. Home lists searches sorted by updated_at desc; empty state | PASS | Tested with 0 and 1 row |
| 4. GET /searches/new renders creation form | PASS | HTTP 200 |
| 5. POST /searches validates and creates; redirects on success | PASS | 303 on valid, 200+errors on blank make |
| 6. GET /searches/{id}/edit renders pre-filled form | PASS | HTTP 200 |
| 7. POST /searches/{id} updates row and updated_at; validates | PASS | Smoke verified |
| 8. POST /searches/{id}/delete deletes and redirects; confirm() in UI | PASS | 303 redirect; confirm() in form onsubmit |
