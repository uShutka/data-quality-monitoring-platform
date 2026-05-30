import pandas as pd

from data_quality_monitoring_platform.models import QualityCheck

REQUIRED_SCHEMA = {
    "customer_id": "object",
    "name": "object",
    "email": "object",
    "phone": "object",
    "country": "object",
    "age": "numeric",
    "signup_date": "datetime",
    "lifetime_value": "numeric",
}


def validate_schema(frame: pd.DataFrame, required_schema: dict[str, str] | None = None) -> QualityCheck:
    schema = required_schema or REQUIRED_SCHEMA
    missing = sorted(set(schema) - set(frame.columns))
    status = "passed" if not missing else "failed"
    return QualityCheck("schema", status, len(missing), {"missing_columns": missing})
