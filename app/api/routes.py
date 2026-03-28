from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.report_repo import ReportRepository
from app.services.analysis_service import AnalysisService
from app.services.build_loader import BuildLoader

router = APIRouter(prefix="/api", tags=["api"])


def _service(db: Session) -> AnalysisService:
    return AnalysisService(ReportRepository(db))


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/analyze/sample/{build_id}")
def analyze_sample(build_id: str, db: Session = Depends(get_db)) -> dict:
    build = BuildLoader().load(build_id)
    return _service(db).analyze(build).model_dump(mode="json")
