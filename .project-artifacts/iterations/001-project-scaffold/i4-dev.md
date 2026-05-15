# i4-dev.md — Project Scaffold

## Files changed

Added:
- `pyproject.toml` — uv project with all stack dependencies
- `uv.lock` — deterministic lockfile
- `app/main.py` — FastAPI app, static mount, router registration
- `app/config.py` — Pydantic Settings (DATABASE_URL, APP_HOST, APP_PORT)
- `app/db.py` — SQLAlchemy engine + SessionLocal + Base + get_db()
- `app/models/__init__.py` — package stub
- `app/routes/__init__.py` — GET / route returning Jinja2 index.html
- `app/scraper/__init__.py` — package stub
- `app/templates/base.html` — base layout with Tailwind/HTMX/Alpine/Chart.js CDN
- `app/templates/index.html` — placeholder home extending base
- `app/static/.gitkeep` — static dir placeholder
- `alembic.ini` — Alembic config (sqlalchemy.url set from Pydantic Settings at runtime)
- `alembic/env.py` — configured to read settings.database_url, target Base.metadata
- `alembic/versions/b625ccc0c12a_initial_smoke_test.py` — creates `alembic_smoke_test` table
- `.env.example` — documents DATABASE_URL, APP_HOST, APP_PORT
- `README.md` — setup and start instructions

Modified:
- `.gitignore` — added Python cache dirs, `.venv/`, `data/`, `*.db`

## In-process tests

None — test_coverage=none per policy.

## External interfaces wired

- `GET /` — HTTP 200, renders Jinja2 template (verified by live curl)

## Self-review

- Matches all 8 ACs from i1-spec.md ✓
- No hardcoded secrets ✓
- `.env` gitignored, `.env.example` committed ✓
- Architecture structure followed exactly ✓
- Starlette 1.0.0 TemplateResponse new signature applied ✓
