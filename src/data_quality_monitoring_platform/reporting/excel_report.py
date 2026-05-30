from pathlib import Path

import pandas as pd

from data_quality_monitoring_platform.models import QualityCheck, QualityReport


def write_excel_report(report: QualityReport, checks: list[QualityCheck], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame([report.to_dict()]).to_excel(writer, index=False, sheet_name="summary")
        pd.DataFrame(
            [{"check_name": check.check_name, "status": check.status, "failed_rows_count": check.failed_rows_count} for check in checks]
        ).to_excel(writer, index=False, sheet_name="checks")
    return output_path
