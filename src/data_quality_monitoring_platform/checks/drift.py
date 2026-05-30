import pandas as pd

from data_quality_monitoring_platform.models import QualityCheck


def detect_data_drift(
    current: pd.DataFrame,
    baseline: pd.DataFrame,
    numeric_columns: list[str] | None = None,
    categorical_columns: list[str] | None = None,
    threshold: float = 0.25,
) -> QualityCheck:
    numeric = numeric_columns or [column for column in current.columns if pd.api.types.is_numeric_dtype(current[column])]
    categorical = categorical_columns or [column for column in current.columns if current[column].dtype == "object"]
    drifted: dict[str, float] = {}

    for column in numeric:
        if column not in baseline:
            continue
        current_mean = pd.to_numeric(current[column], errors="coerce").mean()
        baseline_mean = pd.to_numeric(baseline[column], errors="coerce").mean()
        if baseline_mean and abs(current_mean - baseline_mean) / abs(baseline_mean) > threshold:
            drifted[column] = round(abs(current_mean - baseline_mean) / abs(baseline_mean), 3)

    for column in categorical:
        if column not in baseline:
            continue
        current_top = current[column].fillna("missing").value_counts(normalize=True).max()
        baseline_top = baseline[column].fillna("missing").value_counts(normalize=True).max()
        if abs(current_top - baseline_top) > threshold:
            drifted[column] = round(abs(current_top - baseline_top), 3)

    return QualityCheck("data_drift", "passed" if not drifted else "failed", len(drifted), {"drifted_columns": drifted})
