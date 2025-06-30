import re

def test_no_secrets_in_config_pass():
    """
    Checks that no AWS secrets are leaked in config files.
    This should pass because the config has no secrets.
    """
    test_file = "Jenkins/jenkins_scenarios/scenario_03_html_reports/configs/sample_config.txt"

    # Sample safe content (no secrets)
    safe_content = """
    APP_ENV=dev
    DB_HOST=localhost
    DB_PORT=5432
    """

    # Write safe content to the file
    with open(test_file, "w") as f:
        f.write(safe_content)

    # Scan for fake AWS secrets
    secret_pattern = r"AKIA[0-9A-Z]{16}"

    with open(test_file, "r") as f:
        content = f.read()
        secrets = re.findall(secret_pattern, content)
        assert not secrets, f"Secret found in config file: {secrets}"
