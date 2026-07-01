from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_redirect_and_stats():
    create_response = client.post(
        "/links",
        json={"original_url": "https://example.com"},
    )
    assert create_response.status_code == 200
    short_code = create_response.json()["short_code"]

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 307

    stats_response = client.get(f"/links/{short_code}/stats")
    assert stats_response.status_code == 200
    assert stats_response.json()["total_clicks"] >= 1


def test_expired_link_returns_410():
    expired_at = (datetime.now(timezone.utc) - timedelta(days=1)).replace(tzinfo=None).isoformat()
    create_response = client.post(
        "/links",
        json={"original_url": "https://expired.example.com", "expires_at": expired_at},
    )
    assert create_response.status_code == 200
    short_code = create_response.json()["short_code"]

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 410


def test_engineering_pipeline_output_shape():
    payload = {
        "requirement": "Build a scalable URL shortener service with APIs, persistence, and analytics.",
        "scenario_type": "greenfield",
    }
    response = client.post("/engineering/run", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "clarified_problem" in data
    assert "ambiguities" in data
    assert "assumptions" in data
    assert "tasks" in data
    assert "artifacts" in data
    assert "validation" in data
