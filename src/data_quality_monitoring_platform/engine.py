import logging
from pathlib import Path

import pandas as pd

from data_quality_monitoring_platform.checks.anomalies import check_outliers
from data_quality_monitoring_platform.checks.completeness import check_nulls
from data_quality_monitoring_platform.checks.drift import detect_data_drift
from data_quality_monitoring_platform.checks.duplicates import check_duplicates
from data_quality_monitoring_platform.checks.formats import check_email_format, check_phone_format
from data_quality_monitoring_platform.checks.schema import validate_schema
from data_quality_monitoring_platform.config import default_baseline_dataset, default_current_dataset
from data_quality_monitoring_platform.models import QualityCheck, QualityReport
from data_quality_monitoring_platform.quality_score import calculate_quality_score, score_band

logger = logging.getLogger(__name__)


def load_dataset(path: Path | str | None = None) -> pd.DataFrame:
    dataset_path = Path(path) if path else default_current_dataset()
    logger.info("Loading dataset", extra={"path": str(dataset_path)})
    return pd.read_csv(dataset_path)


def normalize_types(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    if "signup_date" in normalized:
        normalized["signup_date"] = pd.to_datetime(normalized["signup_date"], errors="coerce")
    for column in ["age", "lifetime_value"]:
        if column in normalized:
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce")
    return normalized


def run_checks(current: pd.DataFrame, baseline: pd.DataFrame | None = None) -> list[QualityCheck]:
    checks = [
        validate_schema(current),
        check_nulls(current),
        check_duplicates(current, subset=["customer_id"] if "customer_id" in current else None),
        check_email_format(current),
        check_phone_format(current),
        check_outliers(current, numeric_columns=[column for column in ["age", "lifetime_value"] if column in current]),
    ]
    if baseline is not None:
        checks.append(detect_data_drift(current, baseline, numeric_columns=["age", "lifetime_value"], categorical_columns=["country"]))
    return checks


def build_quality_report(dataset_name: str, frame: pd.DataFrame, checks: list[QualityCheck]) -> QualityReport:
    missing_columns = checks[0].details.get("missing_columns", [])
    metrics = {check.check_name: check.failed_rows_count for check in checks}
    score = calculate_quality_score(len(frame), checks, missing_columns_count=len(missing_columns))
    return QualityReport(
        dataset_name=dataset_name,
        total_rows=len(frame),
        duplicates_count=metrics.get("duplicates", 0),
        nulls_count=metrics.get("nulls", 0),
        invalid_emails_count=metrics.get("email_format", 0),
        invalid_phones_count=metrics.get("phone_format", 0),
        outliers_count=metrics.get("outliers", 0),
        drifted_columns_count=metrics.get("data_drift", 0),
        missing_columns=missing_columns,
        quality_score=score,
        quality_band=score_band(score),
    )


def run_quality_audit(current_path: Path | str | None = None, baseline_path: Path | str | None = None) -> dict[str, object]:
    current = normalize_types(load_dataset(current_path))
    baseline = normalize_types(load_dataset(baseline_path or default_baseline_dataset()))
    checks = run_checks(current, baseline)
    report = build_quality_report("customers_dirty", current, checks)
    return {"data": current, "baseline": baseline, "checks": checks, "report": report}
