import pandas as pd

from data_quality_monitoring_platform.checks.anomalies import check_outliers
from data_quality_monitoring_platform.checks.completeness import check_nulls
from data_quality_monitoring_platform.checks.drift import detect_data_drift
from data_quality_monitoring_platform.checks.duplicates import check_duplicates
from data_quality_monitoring_platform.checks.formats import check_email_format, check_phone_format, invalid_email_mask
from data_quality_monitoring_platform.checks.schema import validate_schema


def test_schema_check_detects_missing_columns():
    check = validate_schema(pd.DataFrame({"customer_id": ["C1"]}))
    assert check.status == "failed"
    assert "email" in check.details["missing_columns"]


def test_schema_check_passes_complete_frame():
    frame = pd.DataFrame(
        {
            "customer_id": ["C1"],
            "name": ["Alice"],
            "email": ["alice@example.com"],
            "phone": ["+3725550101"],
            "country": ["EE"],
            "age": [31],
            "signup_date": ["2025-01-01"],
            "lifetime_value": [100],
        }
    )
    assert validate_schema(frame).status == "passed"


def test_null_check_counts_missing_values():
    check = check_nulls(pd.DataFrame({"a": [1, None], "b": [None, 2]}))
    assert check.failed_rows_count == 2


def test_duplicate_check_counts_duplicate_customer_ids():
    check = check_duplicates(pd.DataFrame({"customer_id": ["C1", "C1", "C2"]}), subset=["customer_id"])
    assert check.failed_rows_count == 2


def test_email_check_detects_invalid_emails():
    frame = pd.DataFrame({"email": ["ok@example.com", "broken"]})
    assert invalid_email_mask(frame).tolist() == [False, True]
    assert check_email_format(frame).failed_rows_count == 1


def test_phone_check_detects_invalid_phones():
    frame = pd.DataFrame({"phone": ["+3725550101", "abc"]})
    assert check_phone_format(frame).failed_rows_count == 1


def test_outlier_check_uses_iqr():
    frame = pd.DataFrame({"value": [10, 11, 12, 13, 1000]})
    check = check_outliers(frame, numeric_columns=["value"])
    assert check.failed_rows_count == 1


def test_drift_check_detects_numeric_shift():
    current = pd.DataFrame({"value": [100, 120, 140], "country": ["EE", "EE", "EE"]})
    baseline = pd.DataFrame({"value": [10, 12, 14], "country": ["EE", "LV", "LT"]})
    check = detect_data_drift(current, baseline, numeric_columns=["value"], categorical_columns=["country"], threshold=0.25)
    assert check.status == "failed"
    assert check.failed_rows_count >= 1
