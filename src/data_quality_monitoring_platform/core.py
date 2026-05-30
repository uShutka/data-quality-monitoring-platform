from pathlib import Path

import pandas as pd

from data_quality_monitoring_platform.engine import load_dataset, run_quality_audit


def load_sample(path: str | Path | None = None) -> pd.DataFrame:
    return load_dataset(path)


def quality_report(frame: pd.DataFrame | None = None) -> dict[str, object]:
    if frame is None:
        return run_quality_audit()["report"].to_dict()
    audit = run_quality_audit()
    return audit["report"].to_dict()


def run_demo() -> dict[str, object]:
    audit = run_quality_audit()
    return {"report": audit["report"].to_dict(), "checks": audit["checks"]}
