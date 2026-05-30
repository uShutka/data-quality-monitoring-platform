from data_quality_monitoring_platform.core import load_sample, quality_report
def test_quality_report_detects_issues():
    report = quality_report(load_sample())
    assert report["quality_score"] < 100
    assert report["duplicate_rows"] == 1
    assert report["outliers"] == 1
