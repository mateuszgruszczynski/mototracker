# i1-spec.md — Project Scaffold

## Acceptance Criteria

1. `pyproject.toml` configures `uv` with all required dependencies: FastAPI, Uvicorn, SQLAlchemy 2.x, Alembic, Jinja2, Pydantic-Settings, selectolax, BeautifulSoup4, httpx, Playwright.
2. App starts with `uv run uvicorn app.main:app --host 127.0.0.1 --port 8000`; GET `/` returns HTTP 200.
3. Project follows the structure `app/{main.py, db.py, models/__init__.py, routes/__init__.py, scraper/__init__.py, templates/base.html, static/}`.
4. SQLAlchemy engine and session factory configured in `app/db.py`, connecting to `./data/mototracker.db` (path from Pydantic Settings / `.env`).
5. Alembic initialised (`alembic.ini`, `alembic/`); `alembic upgrade head` creates the SQLite file and applies one initial migration with a placeholder table (`alembic_smoke_test`).
6. Base Jinja2 template (`templates/base.html`) loads Tailwind CSS, HTMX, Alpine.js, and Chart.js from CDN.
7. Root route (`GET /`) renders a Jinja2 template returning a "MotoTracker" placeholder page (not raw JSON).
8. `.env.example` documents `DATABASE_URL`, `APP_HOST`, `APP_PORT`; Pydantic Settings loads these with sensible defaults; `.env` is gitignored.

**Out of scope:** business logic, scraping, real data schema, auth.
