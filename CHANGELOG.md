# Changelog

## [Iteration 001] — Project Scaffold — 2026-05-15

### Added
- `pyproject.toml` with full stack dependencies (FastAPI, Uvicorn, SQLAlchemy 2.x, Alembic, Jinja2, Pydantic-Settings, Playwright, selectolax, httpx, BeautifulSoup4)
- `app/` package: `main.py`, `config.py`, `db.py`, `models/`, `routes/`, `scraper/`, `templates/`, `static/`
- Alembic initialised with initial migration (`alembic_smoke_test` placeholder table)
- Base Jinja2 template with Tailwind CSS, HTMX, Alpine.js, Chart.js loaded from CDN
- Root route `GET /` serving placeholder home page (HTTP 200)
- `.env.example` with `DATABASE_URL`, `APP_HOST`, `APP_PORT`
- `README.md` with setup and start instructions

Retro: iterations/001-project-scaffold/i7-retro.md
