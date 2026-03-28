from app.services.blocker_detection import detect_blockers
from app.services.build_loader import BuildLoader


def test_detect_blockers_for_blocked_build() -> None:
    build = BuildLoader().load("blocked_build")
    blockers = detect_blockers(build)
    assert blockers
    assert any("open blocker" in item for item in blockers)
