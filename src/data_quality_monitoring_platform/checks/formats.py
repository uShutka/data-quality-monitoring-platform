import re

import pandas as pd

from data_quality_monitoring_platform.models import QualityCheck

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\+\d{8,15}$")


def invalid_email_mask(frame: pd.DataFrame, column: str = "email") -> pd.Series:
    if column not in frame:
        return pd.Series([False] * len(frame), index=frame.index)
    return ~frame[column].fillna("").astype(str).str.match(EMAIL_RE)


def invalid_phone_mask(frame: pd.DataFrame, column: str = "phone") -> pd.Series:
    if column not in frame:
        return pd.Series([False] * len(frame), index=frame.index)
    return ~frame[column].fillna("").astype(str).str.match(PHONE_RE)


def check_email_format(frame: pd.DataFrame, column: str = "email") -> QualityCheck:
    mask = invalid_email_mask(frame, column)
    return QualityCheck("email_format", "passed" if not mask.any() else "failed", int(mask.sum()), {"column": column, "row_indices": frame.index[mask].tolist()})


def check_phone_format(frame: pd.DataFrame, column: str = "phone") -> QualityCheck:
    mask = invalid_phone_mask(frame, column)
    return QualityCheck("phone_format", "passed" if not mask.any() else "failed", int(mask.sum()), {"column": column, "row_indices": frame.index[mask].tolist()})
