# MotoTracker

Track car prices on Otomoto. Define saved searches, run scans, and watch price history over time.

## Setup (inside dev container)

```bash
uv sync
uv run playwright install chromium
alembic upgrade head
```

## Run

```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Environment

Copy `.env.example` to `.env` and adjust as needed. Defaults work out of the box.

```
DATABASE_URL=sqlite:///./data/mototracker.db
APP_HOST=127.0.0.1
APP_PORT=8000
```
