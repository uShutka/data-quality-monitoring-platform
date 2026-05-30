import pandas as pd

from data_quality_monitoring_platform.models import QualityCheck


def outlier_mask_iqr(frame: pd.DataFrame, column: str) -> pd.Series:
    values = pd.to_numeric(frame[column], errors="coerce")
    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (values < lower) | (values > upper)


def check_outliers(frame: pd.DataFrame, numeric_columns: list[str] | None = None) -> QualityCheck:
    columns = numeric_columns or [column for column in frame.columns if pd.api.types.is_numeric_dtype(frame[column])]
    outliers: dict[str, list[int]] = {}
    for column in columns:
        mask = outlier_mask_iqr(frame, column)
        if mask.any():
            outliers[column] = frame.index[mask].tolist()
    failed = sum(len(rows) for rows in outliers.values())
    return QualityCheck("outliers", "passed" if failed == 0 else "failed", failed, {"outliers": outliers})
