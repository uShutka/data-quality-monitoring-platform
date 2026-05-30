from pathlib import Path

from jinja2 import Template

from data_quality_monitoring_platform.models import QualityCheck, QualityReport

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Data Quality Report</title>
  <style>
    body { font-family: Arial, sans-serif; background: #0d1117; color: #f0f6fc; padding: 32px; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 16px; }
    .score { font-size: 44px; color: #58a6ff; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border-bottom: 1px solid #30363d; padding: 10px; text-align: left; }
  </style>
</head>
<body>
  <h1>Data Quality Monitoring Platform</h1>
  <div class="card">
    <div>Dataset: {{ report.dataset_name }}</div>
    <div class="score">{{ report.quality_score }}/100</div>
    <div>{{ report.quality_band }}</div>
  </div>
  <div class="card">
    <table>
      <tr><th>Check</th><th>Status</th><th>Failed rows</th></tr>
      {% for check in checks %}
      <tr><td>{{ check.check_name }}</td><td>{{ check.status }}</td><td>{{ check.failed_rows_count }}</td></tr>
      {% endfor %}
    </table>
  </div>
</body>
</html>
"""


def render_html_report(report: QualityReport, checks: list[QualityCheck], output_path: Path | None = None) -> str:
    html = Template(HTML_TEMPLATE).render(report=report, checks=checks)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
    return html
