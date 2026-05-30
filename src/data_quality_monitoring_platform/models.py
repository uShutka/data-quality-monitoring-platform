from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class QualityCheck:
    check_name: str
    status: str
    failed_rows_count: int
    details: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class QualityReport:
    dataset_name: str
    total_rows: int
    duplicates_count: int
    nulls_count: int
    invalid_emails_count: int
    invalid_phones_count: int
    outliers_count: int
    drifted_columns_count: int
    missing_columns: list[str]
    quality_score: int
    quality_band: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "total_rows": self.total_rows,
            "duplicates_count": self.duplicates_count,
            "nulls_count": self.nulls_count,
            "invalid_emails_count": self.invalid_emails_count,
            "invalid_phones_count": self.invalid_phones_count,
            "outliers_count": self.outliers_count,
            "drifted_columns_count": self.drifted_columns_count,
            "missing_columns": self.missing_columns,
            "quality_score": self.quality_score,
            "quality_band": self.quality_band,
            "created_at": self.created_at.isoformat(),
        }
