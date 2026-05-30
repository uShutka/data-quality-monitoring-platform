import pandas as pd

from data_quality_monitoring_platform.models import QualityCheck


def check_nulls(frame: pd.DataFrame) -> QualityCheck:
    nulls_by_column = frame.isna().sum()
    failed = int(nulls_by_column.sum())
    return QualityCheck(
        "nulls",
        "passed" if failed == 0 else "failed",
        failed,
        {"nulls_by_column": {column: int(value) for column, value in nulls_by_column.items() if value}},
    )
