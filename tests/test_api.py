from fastapi.testclient import TestClient

from data_quality_monitoring_platform.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_summary_endpoint_returns_score():
    response = client.get("/quality/summary")
    assert response.status_code == 200
    assert response.json()["quality_score"] == 64


def test_checks_endpoint_returns_named_checks():
    response = client.get("/quality/checks")
    assert response.status_code == 200
    names = {item["check_name"] for item in response.json()}
    assert {"schema", "nulls", "duplicates", "data_drift"}.issubset(names)


def test_html_endpoint_returns_report_markup():
    response = client.get("/quality/report/html")
    assert response.status_code == 200
    assert "<html>" in response.json()["html"]


def test_alert_preview_endpoint_returns_message():
    response = client.get("/quality/alert-preview")
    assert response.status_code == 200
    assert "Data quality alert" in response.json()["message"]


def test_cleaned_summary_endpoint_improves_score():
    response = client.get("/quality/cleaned-summary")
    assert response.status_code == 200
    assert response.json()["quality_score"] == 93
