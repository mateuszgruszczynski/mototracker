# i2-tasks.md — Saved Searches CRUD

## Tasks

- [ ] T01 — DEV — `SavedSearch` SQLAlchemy model in `app/models/saved_search.py` with all columns and `updated_at` auto-update
- [ ] T02 — DEV — Alembic migration creating `saved_search` table (drop `alembic_smoke_test` in same migration)
- [ ] T03 — DEV — Saved searches router `app/routes/searches.py`: GET /searches/new, POST /searches, GET /searches/{id}/edit, POST /searches/{id}, POST /searches/{id}/delete
- [ ] T04 — DEV — Home route updated to query and pass all saved searches to template (sorted by updated_at desc)
- [ ] T05 — DESIGN — Home template `templates/index.html` updated: saved searches table with name/make/model/year range/edit+delete actions; empty state
- [ ] T06 — DESIGN — Form template `templates/searches/form.html`: create/edit form with validation error display
- [ ] T07 — DEV — Register searches router in `app/main.py`
