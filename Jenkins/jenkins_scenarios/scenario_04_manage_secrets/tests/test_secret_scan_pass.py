import os
import subprocess
import json
from jinja2 import Environment, FileSystemLoader

def run_gitleaks(output_json):
    # Scan only the current directory (should be clean)
    result = subprocess.run(
        ["gitleaks", "detect", "--source=.", f"--report-format=json", f"--report-path={output_json}"],
        capture_output=True, text=True
    )
    return result.returncode

def generate_html(json_path, html_path, mode):
    env = Environment(loader=FileSystemLoader('../report_templates'))
    template = env.get_template('html_report_template.html')
    secrets = []
    summary = "No secrets found."
    bar_chart_data = {}
    if os.path.exists(json_path):
        with open(json_path) as f:
            data = json.load(f)
            if data:
                summary = "Unexpected secrets found!"
                for finding in data:
                    secrets.append({
                        "type": finding.get("RuleID", "Unknown"),
                        "file": finding.get("File", "Unknown"),
                        "line": finding.get("StartLine", "-"),
                        "snippet": finding.get("Match", ""),
                        "severity": finding.get("Severity", "Low").capitalize()
                    })
                # Bar chart data
                for s in secrets:
                    bar_chart_data[s["type"]] = bar_chart_data.get(s["type"], 0) + 1
    html = template.render(
        title="Secret Scan PASS Report",
        mode=mode,
        summary=summary,
        secrets=secrets,
        bar_chart_data=bar_chart_data
    )
    with open(html_path, "w") as f:
        f.write(html)

def test_secret_scan_pass():
    os.makedirs("../reports", exist_ok=True)
    json_report = "../reports/secret_scan_pass.json"
    html_report = "../reports/secret_scan_pass.html"
    rc = run_gitleaks(json_report)
    generate_html(json_report, html_report, "PASS")
    assert rc == 0, "Gitleaks found secrets in clean code!"

if __name__ == "__main__":
    test_secret_scan_pass()
    print("PASS: No secrets found.")