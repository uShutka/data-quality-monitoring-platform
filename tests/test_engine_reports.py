import sqlite3

from data_quality_monitoring_platform.alerts.telegram import build_quality_alert
from data_quality_monitoring_platform.cleaning import clean_customer_dataset
from data_quality_monitoring_platform.database import init_db, save_report
from data_quality_monitoring_platform.engine import build_quality_report, normalize_types, run_checks, run_quality_audit
from data_quality_monitoring_platform.quality_score import score_band
from data_quality_monitoring_platform.reporting.excel_report import write_excel_report
from data_quality_monitoring_platform.reporting.html_report import render_html_report


def test_quality_audit_returns_expected_initial_score():
    audit = run_quality_audit()
    assert audit["report"].quality_score == 64
    assert audit["report"].duplicates_count == 2
    assert audit["report"].invalid_emails_count == 3


def test_cleaning_improves_score_to_minor_issues_band():
    audit = run_quality_audit()
    cleaned = normalize_types(clean_customer_dataset(audit["data"]))
    report = build_quality_report("customers_cleaned", cleaned, run_checks(cleaned, audit["baseline"]))
    assert report.quality_score == 93
    assert report.quality_band == "minor issues"


def test_score_band_labels_are_business_friendly():
    assert score_band(100) == "excellent"
    assert score_band(85) == "minor issues"
    assert score_band(70) == "needs cleaning"
    assert score_band(40) == "dangerous for analytics"


def test_html_report_contains_score():
    audit = run_quality_audit()
    html = render_html_report(audit["report"], audit["checks"])
    assert "64/100" in html
    assert "Data Quality Monitoring Platform" in html


def test_html_report_can_be_written(tmp_path):
    audit = run_quality_audit()
    path = tmp_path / "report.html"
    render_html_report(audit["report"], audit["checks"], path)
    assert path.exists()
    assert "customers_dirty" in path.read_text(encoding="utf-8")


def test_excel_report_can_be_written(tmp_path):
    audit = run_quality_audit()
    path = write_excel_report(audit["report"], audit["checks"], tmp_path / "quality.xlsx")
    assert path.exists()


def test_sqlite_persistence_saves_report(tmp_path):
    audit = run_quality_audit()
    connection = init_db(tmp_path / "quality.db")
    dataset_id = save_report(connection, audit["report"], audit["checks"])
    assert dataset_id == 1
    assert connection.execute("select count(*) from quality_checks").fetchone()[0] == len(audit["checks"])


def test_database_schema_contains_quality_reports(tmp_path):
    connection = init_db(tmp_path / "quality.db")
    rows = connection.execute("select name from sqlite_master where type='table'").fetchall()
    assert ("quality_reports",) in rows
    assert isinstance(connection, sqlite3.Connection)


def test_alert_message_contains_quality_score():
    audit = run_quality_audit()
    message = build_quality_alert(audit["report"].to_dict())
    assert "Score: 64/100" in message
    assert "Duplicates" in message


def test_report_to_dict_is_json_ready():
    audit = run_quality_audit()
    payload = audit["report"].to_dict()
    assert payload["dataset_name"] == "customers_dirty"
    assert isinstance(payload["created_at"], str)
