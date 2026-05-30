from fastapi import FastAPI
from data_quality_monitoring_platform.core import load_sample, quality_report
app = FastAPI(title="Data Quality Monitoring Platform")
@app.get("/health")
def health(): return {"status": "ok"}
@app.get("/quality/summary")
def summary(): return quality_report(load_sample())
