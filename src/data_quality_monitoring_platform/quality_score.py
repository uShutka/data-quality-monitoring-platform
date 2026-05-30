from data_quality_monitoring_platform.models import QualityCheck


def score_band(score: int) -> str:
    if score == 100:
        return "excellent"
    if score >= 80:
        return "minor issues"
    if score >= 60:
        return "needs cleaning"
    return "dangerous for analytics"


def calculate_quality_score(total_rows: int, checks: list[QualityCheck], missing_columns_count: int = 0) -> int:
    total_rows = max(total_rows, 1)
    metrics = {check.check_name: check.failed_rows_count for check in checks}
    duplicate_rate = metrics.get("duplicates", 0) / total_rows
    invalid_email_rate = metrics.get("email_format", 0) / total_rows
    invalid_phone_rate = metrics.get("phone_format", 0) / total_rows
    outlier_rate = metrics.get("outliers", 0) / total_rows
    null_rate = metrics.get("nulls", 0) / (total_rows * 8)
    drift_count = metrics.get("data_drift", 0)

    deductions = (
        missing_columns_count * 15
        + duplicate_rate * 70
        + null_rate * 150
        + invalid_email_rate * 35
        + invalid_phone_rate * 30
        + outlier_rate * 25
        + drift_count * 3.5
    )
    return max(0, min(100, round(100 - deductions)))
