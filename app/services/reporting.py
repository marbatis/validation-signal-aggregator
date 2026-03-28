from __future__ import annotations


def build_recommendations(blockers: list[str], weak_signals: list[str]) -> list[str]:
    recs: list[str] = []
    if blockers:
        recs.append("Resolve blocker issues before release consideration")
    if any("Missing validation" in item for item in weak_signals):
        recs.append("Add missing validation suites for uncovered subsystems")
    if any("Flaky" in item for item in weak_signals):
        recs.append("Stabilize flaky subsystems and rerun validation")
    if any("Slow CI" in item for item in weak_signals):
        recs.append("Optimize CI bottlenecks and parallelize heavy suites")
    if not recs:
        recs.append("Maintain current validation guardrails and monitoring")
    return recs


def build_summary(build_id: str, level: str, score: float, blockers: list[str]) -> str:
    blocker_text = "; ".join(blockers) if blockers else "No blocking signals"
    return f"Build {build_id} is {level} with confidence {score}. {blocker_text}."
