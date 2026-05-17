import subprocess
from pathlib import Path

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse

from app.config import settings
from app.db import engine

router = APIRouter(prefix="/admin")

SQLITE_MAGIC = b"SQLite format 3\x00"


def _db_path() -> Path:
    # database_url is e.g. "sqlite:///./data/mototracker.db"
    relative = settings.database_url.removeprefix("sqlite:///")
    return Path(relative)


@router.get("/export")
async def export_db():
    db_path = _db_path()
    if not db_path.exists():
        return HTMLResponse("Database file not found", status_code=404)

    # Checkpoint WAL so the downloaded file is self-contained.
    with engine.connect() as conn:
        conn.execute(__import__("sqlalchemy").text("PRAGMA wal_checkpoint(TRUNCATE)"))

    return FileResponse(
        path=str(db_path),
        media_type="application/octet-stream",
        filename="mototracker.db",
    )


@router.post("/import")
async def import_db(request: Request, file: UploadFile = File(...)):
    data = await file.read()

    if not data.startswith(SQLITE_MAGIC):
        return RedirectResponse("/?toast=Invalid+SQLite+file", status_code=303)

    db_path = _db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Close all pooled connections before replacing the file.
    engine.dispose()

    db_path.write_bytes(data)

    # Apply any pending migrations to the restored database.
    subprocess.run(["uv", "run", "alembic", "upgrade", "head"], check=False)

    return RedirectResponse("/?toast=Database+restored+successfully", status_code=303)
