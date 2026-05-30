import pandas as pd

from data_quality_monitoring_platform.models import QualityCheck


def check_duplicates(frame: pd.DataFrame, subset: list[str] | None = None) -> QualityCheck:
    mask = frame.duplicated(subset=subset, keep=False)
    failed = int(mask.sum())
    return QualityCheck(
        "duplicates",
        "passed" if failed == 0 else "failed",
        failed,
        {"duplicate_row_indices": frame.index[mask].tolist()},
    )
