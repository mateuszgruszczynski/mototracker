# i2-tasks.md — Project Scaffold

## Tasks

- [ ] T01 — DEV — `pyproject.toml` with all project dependencies (FastAPI, Uvicorn, SQLAlchemy 2.x, Alembic, Jinja2, Pydantic-Settings, selectolax, BeautifulSoup4, httpx, Playwright)
- [ ] T02 — DEV — Project directory structure: `app/{main.py, db.py, models/__init__.py, routes/__init__.py, scraper/__init__.py, templates/, static/}`
- [ ] T03 — DEV — `app/config.py`: Pydantic Settings loading `DATABASE_URL`, `APP_HOST`, `APP_PORT` from `.env` with defaults
- [ ] T04 — SECURITY — `.env.example` documenting all env vars; `.env` added to `.gitignore`
- [ ] T05 — DEV — `app/db.py`: SQLAlchemy engine + `SessionLocal` factory connected to SQLite path from config
- [ ] T06 — DEV — Alembic init (`alembic.ini`, `alembic/env.py`); initial migration creating `alembic_smoke_test` placeholder table
- [ ] T07 — DESIGN — `templates/base.html` with Tailwind CSS, HTMX, Alpine.js, Chart.js loaded from CDN
- [ ] T08 — DEV — Root route `GET /` in `app/routes/__init__.py` registered in `app/main.py`; renders `index.html` extending `base.html`
- [ ] T09 — DEV — README.md: `uv sync`, `alembic upgrade head`, `uv run uvicorn` start instructions
