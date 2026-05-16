import logging
from pathlib import Path

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.routes.listings import router as listings_router
from app.routes.scans import router as scans_router
from app.routes.searches import router as searches_router

app = FastAPI(title="MotoTracker")

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
app.include_router(router)
app.include_router(searches_router)
app.include_router(listings_router)
app.include_router(scans_router)
