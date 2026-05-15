# i6-int.md — Project Scaffold

## Build status

`uv sync` — 37 packages resolved, all present. Green.

## Smoke outcome

App started with `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000`. Manual smoke passed:
- `GET /` → HTTP 200, Jinja2 template rendered with "MotoTracker" title
- No console errors, no 500s

## AC pass/fail table (manual smoke, test_coverage=none)

| AC | Result | Note |
|---|---|---|
| 1. pyproject.toml with all dependencies | PASS | `uv sync` resolves 37 packages cleanly |
| 2. App boots; GET / returns 200 | PASS | curl confirmed HTTP 200 |
| 3. Project structure correct | PASS | All directories created and committed |
| 4. SQLAlchemy engine connects to SQLite | PASS | Engine configured via Pydantic Settings |
| 5. Alembic upgrade head creates DB + placeholder table | PASS | `alembic_smoke_test` table confirmed via SQLAlchemy inspect |
| 6. Base template includes Tailwind/HTMX/Alpine/Chart.js CDN | PASS | All four CDN script tags in base.html |
| 7. Root route renders Jinja2 template | PASS | Response is HTML, not JSON |
| 8. .env.example present; Pydantic Settings loads vars; .env gitignored | PASS | .env.example committed; .env in .gitignore |
