# i1-spec.md — Saved Searches CRUD

## Acceptance Criteria

1. `saved_search` table created via Alembic migration: columns `id` (PK), `name`, `make`, `model`, `year_from` (nullable int), `year_to` (nullable int), `country_of_origin` (default `"PL"`), `condition` (default `"nie-uszkodzony"`), `created_at`, `updated_at`.
2. SQLAlchemy model `SavedSearch` defined in `app/models/saved_search.py` mapping to the table.
3. Home page (`GET /`) lists all saved searches sorted by `updated_at` desc; shows "No saved searches yet" empty state when table is empty.
4. `GET /searches/new` renders a creation form with fields: name (required), make (required), model (required), year_from (optional int), year_to (optional int).
5. `POST /searches` validates that `name`, `make`, and `model` are non-blank; on success inserts row and redirects to `/`; on failure re-renders form with error messages.
6. `GET /searches/{id}/edit` renders the form pre-filled with the existing row's values; returns 404 if id not found.
7. `POST /searches/{id}` updates all fields and sets `updated_at = now()`; on success redirects to `/`; validates same rules as create.
8. `POST /searches/{id}/delete` deletes the row (cascade delete configured for future FK children); redirects to `/`. Delete link on home page triggers a browser `confirm()` dialog before submitting.

**Out of scope:** make/model dropdowns, last-scan info column, scheduling, pagination, sharing, scans table (comes in E4).
