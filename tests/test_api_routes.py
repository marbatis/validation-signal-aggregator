
def test_health(client) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200


def test_analyze_sample(client) -> None:
    response = client.post("/api/analyze/sample/healthy_build")
    assert response.status_code == 200
    assert response.json()["report"]["build_risk_level"] in {"HEALTHY", "BORDERLINE", "BLOCKED"}


def test_dashboard_and_detail(client) -> None:
    assert client.get("/").status_code == 200
    assert client.get("/build/healthy_build").status_code == 200
