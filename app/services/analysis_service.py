from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.repositories.report_repo import ReportRepository
from app.schemas import BuildAnalysisResponse, BuildInput, BuildReport
from app.services.blocker_detection import detect_blockers
from app.services.confidence_scoring import compute_confidence_score, risk_level
from app.services.reporting import build_recommendations, build_summary
from app.services.signal_aggregator import collect_weak_signals


class AnalysisService:
    def __init__(self, repo: ReportRepository):
        self.repo = repo

    def analyze(self, build: BuildInput) -> BuildAnalysisResponse:
        blockers = detect_blockers(build)
        score = compute_confidence_score(build)
        level = risk_level(score, blockers)
        weak_signals = collect_weak_signals(build)
        recommendations = build_recommendations(blockers, weak_signals)
        memo = build_summary(build.build_id, level, score, blockers)

        report = BuildReport(
            report_id=f"report_{uuid4().hex[:10]}",
            build_id=build.build_id,
            build_confidence_score=score,
            build_risk_level=level,
            blockers=blockers,
            weak_signal_areas=weak_signals,
            recommended_next_checks=recommendations,
            summary_memo=memo,
            created_at=datetime.now(timezone.utc),
        )
        response = BuildAnalysisResponse(report=report, build=build)
        self.repo.save(report.report_id, build.build_id, response.model_dump_json())
        return response

    def latest_for_build(self, build_id: str) -> BuildAnalysisResponse | None:
        payload = self.repo.latest_for_build(build_id)
        return BuildAnalysisResponse.model_validate(payload) if payload else None

    def history(self) -> list[BuildAnalysisResponse]:
        return [BuildAnalysisResponse.model_validate(item) for item in self.repo.list_recent()]
