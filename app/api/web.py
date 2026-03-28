from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.report_repo import ReportRepository
from app.services.analysis_service import AnalysisService
from app.services.build_loader import BuildLoader

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


def _service(db: Session) -> AnalysisService:
    return AnalysisService(ReportRepository(db))


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    loader = BuildLoader()
    rows = []
    for build_id in loader.list_build_ids():
        build = loader.load(build_id)
        latest = _service(db).latest_for_build(build_id)
        rows.append({"build": build, "report": latest.report if latest else None})
    return templates.TemplateResponse("index.html", {"request": request, "rows": rows})


@router.get("/build/{build_id}")
def build_detail(build_id: str, request: Request, db: Session = Depends(get_db)):
    loader = BuildLoader()
    build = loader.load(build_id)
    service = _service(db)
    report = service.latest_for_build(build_id)
    if not report:
        report = service.analyze(build)
    return templates.TemplateResponse("detail.html", {"request": request, "item": report})
