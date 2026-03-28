from __future__ import annotations

from app.schemas import BuildInput


def detect_blockers(build: BuildInput) -> list[str]:
    blockers: list[str] = []
    failed = int(build.validation_suites.get("failed", 0))

    if build.open_blocker_issues > 0:
        blockers.append(f"{build.open_blocker_issues} open blocker issues")
    if failed >= 5:
        blockers.append(f"{failed} failed validation suites")
    if build.field_anomaly_count >= 20:
        blockers.append("High field anomaly count")
    if len(build.missing_validation_areas) >= 3:
        blockers.append("Critical validation coverage gaps")

    return blockers
