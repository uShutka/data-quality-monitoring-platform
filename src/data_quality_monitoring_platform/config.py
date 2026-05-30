from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_current_dataset() -> Path:
    return project_root() / "data" / "raw" / "customers_dirty.csv"


def default_baseline_dataset() -> Path:
    return project_root() / "data" / "reference" / "customers_baseline.csv"
