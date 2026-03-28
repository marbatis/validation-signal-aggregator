from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BuildInput(BaseModel):
    build_id: str
    commit_sha: str
    timestamp: str
    validation_suites: dict
    field_anomaly_count: int = 0
    open_blocker_issues: int = 0
    flaky_subsystem_signals: list[str] = Field(default_factory=list)
    missing_validation_areas: list[str] = Field(default_factory=list)
    ci_duration_minutes: float = 0.0


class BuildReport(BaseModel):
    report_id: str
    build_id: str
    build_confidence_score: float
    build_risk_level: str
    blockers: list[str]
    weak_signal_areas: list[str]
    recommended_next_checks: list[str]
    summary_memo: str
    created_at: datetime


class BuildAnalysisResponse(BaseModel):
    report: BuildReport
    build: BuildInput
