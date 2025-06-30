import re
import pytest

def test_no_secrets_in_config_fail():
    fake_secret = "AKIAEXAMPLESECRETKEY"
    test_file = "Jenkins/jenkins_scenarios/scenario_03_html_reports/configs/sample_config.txt"

    # Write fake secret
    with open(test_file, "w") as f:
        f.write(f"This is a secret: {fake_secret}")

    with open(test_file, "r") as f:
        content = f.read()
        secrets = re.findall(r"AKIA[0-9A-Z]{16}", content)
        assert not secrets, f"Secret found in config: {secrets}"
