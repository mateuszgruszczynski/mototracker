# i4-dev.md — Saved Searches CRUD

## Files changed

Added:
- `app/models/saved_search.py` — SavedSearch ORM model (all 10 columns, onupdate for updated_at)
- `app/routes/searches.py` — CRUD router: new form, create, edit form, update, delete
- `app/templates/searches/form.html` — create/edit form with inline validation errors
- `alembic/versions/8a41a2cec680_add_saved_search.py` — drops smoke_test table, creates saved_search

Modified:
- `app/models/__init__.py` — imports SavedSearch for Alembic autogenerate
- `app/routes/__init__.py` — home route now queries SavedSearch, sorted by updated_at desc
- `app/main.py` — registers searches_router
- `app/templates/index.html` — full table with edit/delete actions; empty state

## In-process tests

None — test_coverage=none per policy.

## External interfaces wired

- `GET /` — lists saved searches (HTML)
- `GET /searches/new` — create form (HTML)
- `POST /searches` — create; 303 on success, 200 with errors on validation failure
- `GET /searches/{id}/edit` — edit form (HTML), 404 if not found
- `POST /searches/{id}` — update; 303 on success
- `POST /searches/{id}/delete` — delete; 303 always

## Self-review

- All 8 ACs from i1-spec.md confirmed by smoke test ✓
- No hardcoded secrets ✓
- Validation rejects blank name/make/model ✓
- updated_at set explicitly on update (SQLAlchemy onupdate doesn't fire on direct assignment) ✓
- Architecture structure followed ✓
