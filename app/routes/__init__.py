from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.saved_search import SavedSearch

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    searches = db.query(SavedSearch).order_by(desc(SavedSearch.updated_at)).all()
    return templates.TemplateResponse(request, "index.html", {"searches": searches})
