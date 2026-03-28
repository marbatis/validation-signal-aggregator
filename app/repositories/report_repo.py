from __future__ import annotations

import json
from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models import BuildReportRecord


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, report_id: str, build_id: str, report_json: str) -> None:
        self.db.add(BuildReportRecord(report_id=report_id, build_id=build_id, report_json=report_json))
        self.db.commit()

    def latest_for_build(self, build_id: str) -> Optional[dict]:
        rec = self.db.scalar(
            select(BuildReportRecord)
            .where(BuildReportRecord.build_id == build_id)
            .order_by(desc(BuildReportRecord.created_at))
            .limit(1)
        )
        return None if not rec else json.loads(rec.report_json)

    def list_recent(self, limit: int = 50) -> list[dict]:
        rows = self.db.scalars(select(BuildReportRecord).order_by(desc(BuildReportRecord.created_at)).limit(limit)).all()
        return [json.loads(row.report_json) for row in rows]
