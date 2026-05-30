import pandas as pd
import plotly.express as px
import streamlit as st

from data_quality_monitoring_platform.alerts.telegram import build_quality_alert
from data_quality_monitoring_platform.cleaning import clean_customer_dataset
from data_quality_monitoring_platform.engine import build_quality_report, normalize_types, run_checks, run_quality_audit

st.set_page_config(page_title="Data Quality Monitoring", layout="wide")

audit = run_quality_audit()
report = audit["report"]
checks = audit["checks"]
cleaned = normalize_types(clean_customer_dataset(audit["data"]))
cleaned_checks = run_checks(cleaned, audit["baseline"])
cleaned_report = build_quality_report("customers_cleaned", cleaned, cleaned_checks)

st.title("Data Quality Monitoring Platform")

top = st.columns(5)
top[0].metric("Initial score", f"{report.quality_score}/100", report.quality_band)
top[1].metric("After cleaning", f"{cleaned_report.quality_score}/100", cleaned_report.quality_band)
top[2].metric("Duplicates", report.duplicates_count)
top[3].metric("Invalid emails", report.invalid_emails_count)
top[4].metric("Outliers", report.outliers_count)

check_frame = pd.DataFrame(
    [{"check": check.check_name, "status": check.status, "failed_rows": check.failed_rows_count} for check in checks]
)

left, right = st.columns([1, 1])
with left:
    st.subheader("Quality checks")
    st.dataframe(check_frame, use_container_width=True)
with right:
    st.subheader("Issue distribution")
    st.plotly_chart(px.bar(check_frame, x="check", y="failed_rows", color="status"), use_container_width=True)

st.subheader("Invalid rows")
st.dataframe(audit["data"].loc[audit["data"].isna().any(axis=1)].head(20), use_container_width=True)

st.subheader("Telegram alert preview")
st.code(build_quality_alert(report.to_dict()))
