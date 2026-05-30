from fastapi import FastAPI

from data_quality_monitoring_platform.alerts.telegram import build_quality_alert
from data_quality_monitoring_platform.cleaning import clean_customer_dataset
from data_quality_monitoring_platform.engine import build_quality_report, normalize_types, run_checks, run_quality_audit
from data_quality_monitoring_platform.reporting.html_report import render_html_report

app = FastAPI(title="Data Quality Monitoring Platform", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "data-quality-monitoring-platform"}


@app.get("/quality/summary")
def quality_summary() -> dict[str, object]:
    audit = run_quality_audit()
    return audit["report"].to_dict()


@app.get("/quality/checks")
def quality_checks() -> list[dict[str, object]]:
    audit = run_quality_audit()
    return [
        {"check_name": check.check_name, "status": check.status, "failed_rows_count": check.failed_rows_count, "details": check.details}
        for check in audit["checks"]
    ]


@app.get("/quality/report/html")
def quality_report_html() -> dict[str, str]:
    audit = run_quality_audit()
    return {"html": render_html_report(audit["report"], audit["checks"])}


@app.get("/quality/alert-preview")
def quality_alert_preview() -> dict[str, str]:
    audit = run_quality_audit()
    return {"message": build_quality_alert(audit["report"].to_dict())}


@app.get("/quality/cleaned-summary")
def cleaned_summary() -> dict[str, object]:
    audit = run_quality_audit()
    cleaned = normalize_types(clean_customer_dataset(audit["data"]))
    checks = run_checks(cleaned, audit["baseline"])
    report = build_quality_report("customers_cleaned", cleaned, checks)
    return report.to_dict()
