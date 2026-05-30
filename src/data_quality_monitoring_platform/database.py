import sqlite3
from pathlib import Path

from data_quality_monitoring_platform.models import QualityCheck, QualityReport


def init_db(path: Path | str) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.execute(
        """
        create table if not exists datasets (
            id integer primary key autoincrement,
            name text not null,
            source_type text not null,
            created_at text not null
        )
        """
    )
    connection.execute(
        """
        create table if not exists quality_checks (
            id integer primary key autoincrement,
            dataset_id integer not null,
            check_name text not null,
            status text not null,
            failed_rows_count integer not null,
            created_at text not null
        )
        """
    )
    connection.execute(
        """
        create table if not exists quality_reports (
            id integer primary key autoincrement,
            dataset_id integer not null,
            total_rows integer not null,
            duplicates_count integer not null,
            nulls_count integer not null,
            invalid_emails_count integer not null,
            outliers_count integer not null,
            quality_score integer not null,
            created_at text not null
        )
        """
    )
    return connection


def save_report(connection: sqlite3.Connection, report: QualityReport, checks: list[QualityCheck], source_type: str = "csv") -> int:
    cursor = connection.execute(
        "insert into datasets (name, source_type, created_at) values (?, ?, ?)",
        (report.dataset_name, source_type, report.created_at.isoformat()),
    )
    dataset_id = int(cursor.lastrowid)
    connection.execute(
        """
        insert into quality_reports (
            dataset_id, total_rows, duplicates_count, nulls_count,
            invalid_emails_count, outliers_count, quality_score, created_at
        ) values (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dataset_id,
            report.total_rows,
            report.duplicates_count,
            report.nulls_count,
            report.invalid_emails_count,
            report.outliers_count,
            report.quality_score,
            report.created_at.isoformat(),
        ),
    )
    for check in checks:
        connection.execute(
            "insert into quality_checks (dataset_id, check_name, status, failed_rows_count, created_at) values (?, ?, ?, ?, ?)",
            (dataset_id, check.check_name, check.status, check.failed_rows_count, check.created_at.isoformat()),
        )
    connection.commit()
    return dataset_id
