import os
import subprocess
import json
from jinja2 import Environment, FileSystemLoader

def create_leaky_file():
    # Simulate real-world secret leaks
    leaky_code = '''
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
db_password = "SuperSecret123!"
api_token = "ghp_1234567890abcdef1234567890abcdef1234"
'''
    with open("leaky_secrets.py", "w") as f:
        f.write(leaky_code)

def run_gitleaks(output_json):
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
                summary = f"{len(data)} secrets found!"
                for finding in data:
                    secrets.append({
                        "type": finding.get("RuleID", "Unknown"),
                        "file": finding.get("File", "Unknown"),
                        "line": finding.get("StartLine", "-"),
                        "snippet": finding.get("Match", ""),
                        "severity": finding.get("Severity", "High").capitalize()
                    })
                # Bar chart data
                for s in secrets:
                    bar_chart_data[s["type"]] = bar_chart_data.get(s["type"], 0) + 1
    html = template.render(
        title="Secret Scan FAIL Report",
        mode=mode,
        summary=summary,
        secrets=secrets,
        bar_chart_data=bar_chart_data
    )
    with open(html_path, "w") as f:
        f.write(html)

def test_secret_scan_fail():
    os.makedirs("../reports", exist_ok=True)
    create_leaky_file()
    json_report = "../reports/secret_scan_fail.json"
    html_report = "../reports/secret_scan_fail.html"
    rc = run_gitleaks(json_report)
    generate_html(json_report, html_report, "FAIL")
    # Clean up leaky file
    os.remove("leaky_secrets.py")
    assert rc != 0, "Gitleaks did not find secrets in leaky code!"

if __name__ == "__main__":
    test_secret_scan_fail()
    print("FAIL: Secrets detected as expected.")