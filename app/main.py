import logging
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(name)s:%(message)s", datefmt="%H:%M:%S")
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.routes.admin import router as admin_router
from app.routes.listings import router as listings_router
from app.routes.scans import router as scans_router
from app.routes.searches import router as searches_router

app = FastAPI(title="MotoTracker")


@app.on_event("startup")
async def _reset_stuck_scans() -> None:
    from app.db import SessionLocal
    from app.models.scan import Scan
    db = SessionLocal()
    try:
        stuck = db.query(Scan).filter_by(status="running").all()
        if stuck:
            for s in stuck:
                s.status = "failed"
                s.error_summary = "Server restarted while scan was in progress"
                s.finished_at = datetime.now(timezone.utc)
            db.commit()
            logging.getLogger(__name__).warning(
                "Reset %d stuck scan(s) to failed on startup", len(stuck)
            )
    finally:
        db.close()

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.include_router(router)
app.include_router(admin_router)
app.include_router(searches_router)
app.include_router(listings_router)
app.include_router(scans_router)
