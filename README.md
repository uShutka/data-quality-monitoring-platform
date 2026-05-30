# Data Quality Monitoring Platform

Production-style data quality platform for validating CSV/Excel/SQL-like datasets, detecting missing values, duplicates, invalid formats, outliers, data drift, and generating structured HTML/Excel reports with API and dashboard access.

## Project Overview

The project demonstrates data engineering maturity: it treats data quality as a first-class system, not an afterthought. It includes modular checks, a quality scoring model, report generation, alert previews, persistence schema, tests, Docker, and CI.

## Business Problem

Analytics teams often receive datasets with duplicated records, missing values, broken emails or phone numbers, impossible amounts, and silent distribution changes. Reports built on this data can become misleading even when the dashboard itself looks polished.

## Solution

The platform validates incoming data, calculates a quality score, compares the latest dataset with a historical baseline, stores report-ready results, and exposes summaries through FastAPI and Streamlit.

## Architecture

```text
CSV / Excel / SQL Dataset
-> Schema & Format Checks
-> Completeness / Duplicates / Outliers
-> Historical Drift Comparison
-> Quality Score Engine
-> PostgreSQL-ready Persistence
-> HTML / Excel Reports + FastAPI + Dashboard + Telegram Alerts
```

## Features

- Schema validation
- Null and completeness checks
- Duplicate detection
- Email and phone format validation
- IQR-based outlier detection
- Historical baseline comparison and data drift detection
- `quality_score` with business-friendly bands
- HTML and Excel report generation
- SQLite/PostgreSQL-style persistence schema
- FastAPI endpoints
- Streamlit dashboard
- Telegram alert message builder
- Docker Compose and GitHub Actions

## Tech Stack

Python, pandas, pandera-ready validation style, FastAPI, Jinja2, OpenPyXL, PostgreSQL-ready schema, Docker, pytest, ruff, Streamlit.

## Database Schema

`datasets`

- `id`
- `name`
- `source_type`
- `created_at`

`quality_checks`

- `id`
- `dataset_id`
- `check_name`
- `status`
- `failed_rows_count`
- `created_at`

`quality_reports`

- `id`
- `dataset_id`
- `total_rows`
- `duplicates_count`
- `nulls_count`
- `invalid_emails_count`
- `outliers_count`
- `quality_score`
- `created_at`

## Data Pipeline

1. Load the current dataset and historical baseline.
2. Normalize dates and numeric columns.
3. Run schema, completeness, duplicate, format, anomaly, and drift checks.
4. Convert check results into a quality score.
5. Generate reports and alert-ready messages.
6. Serve results through API and dashboard.

## API Endpoints

- `GET /health`
- `GET /quality/summary`
- `GET /quality/checks`
- `GET /quality/report/html`
- `GET /quality/alert-preview`
- `GET /quality/cleaned-summary`

## Dashboard Screenshots

Screenshots are stored in `docs/screenshots/`:

- Data quality report
- Before/after quality score
- Invalid rows table
- API validation endpoint
- HTML report example

## Analytics Results

Demo quality summary:

- Initial data quality score: `64/100`
- After cleaning: `93/100`
- Duplicate records detected and removed
- Invalid emails and phones detected
- Outliers detected in customer lifetime value
- Data drift detected against the baseline distribution

Quality score interpretation:

- `100`: excellent data
- `80-99`: minor issues
- `60-79`: needs cleaning
- `<60`: dangerous for analytics

## How to Run

```bash
docker compose up --build
```

Open:

- API docs: `http://localhost:8002/docs`
- Dashboard: `http://localhost:8503`

Local development:

```bash
python -m pip install -e .
uvicorn data_quality_monitoring_platform.api.main:app --reload
streamlit run dashboard/streamlit_app.py
```

## Tests

```bash
pytest
ruff check .
```

The suite covers schema checks, nulls, duplicates, format validation, outliers, drift, scoring, cleaning, report rendering, persistence, alerts, and API endpoints.

## Engineering Notes

The checks are split into small modules so each rule can be tested and extended independently. The same quality engine powers API responses, dashboard metrics, reports, and alert previews.

## Known Limitations

- Demo data is compact for portfolio review.
- Outlier detection uses statistical thresholds, not ML.
- Drift detection uses lightweight distribution checks.
- Telegram sending is intentionally disabled unless credentials are provided through environment variables.

## Future Improvements

- Add scheduled checks with Prefect or APScheduler.
- Add dataset-level SLAs and quality trend history.
- Add Great Expectations or pandera schemas for stricter contracts.
- Add Prometheus/Grafana monitoring.
- Add PDF export and Slack alerts.
