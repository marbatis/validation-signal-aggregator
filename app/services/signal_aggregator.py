from __future__ import annotations

from app.schemas import BuildInput


def collect_weak_signals(build: BuildInput) -> list[str]:
    weak = []
    if build.flaky_subsystem_signals:
        weak.append("Flaky subsystems: " + ", ".join(build.flaky_subsystem_signals))
    if build.missing_validation_areas:
        weak.append("Missing validation: " + ", ".join(build.missing_validation_areas))
    if build.ci_duration_minutes > 60:
        weak.append("Slow CI duration")
    if build.field_anomaly_count > 0:
        weak.append("Field anomalies present")
    return weak
