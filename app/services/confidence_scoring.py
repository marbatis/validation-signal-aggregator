from __future__ import annotations

from app.schemas import BuildInput


def compute_confidence_score(build: BuildInput) -> float:
    failed = int(build.validation_suites.get("failed", 0))
    penalties = 0.0
    penalties += failed * 6.0
    penalties += build.field_anomaly_count * 1.2
    penalties += build.open_blocker_issues * 20.0
    penalties += len(build.flaky_subsystem_signals) * 4.0
    penalties += len(build.missing_validation_areas) * 8.0

    score = 100.0 - penalties
    return round(max(0.0, min(100.0, score)), 2)


def risk_level(score: float, blockers: list[str]) -> str:
    if blockers or score < 55:
        return "BLOCKED"
    if score < 80:
        return "BORDERLINE"
    return "HEALTHY"
