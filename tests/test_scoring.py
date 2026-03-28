from app.services.build_loader import BuildLoader
from app.services.confidence_scoring import compute_confidence_score, risk_level


def test_score_ordering() -> None:
    loader = BuildLoader()
    healthy = loader.load("healthy_build")
    blocked = loader.load("blocked_build")

    healthy_score = compute_confidence_score(healthy)
    blocked_score = compute_confidence_score(blocked)

    assert healthy_score > blocked_score
    assert risk_level(blocked_score, ["x"]) == "BLOCKED"
