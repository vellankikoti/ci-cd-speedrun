import json
import pytest

def test_config_validation_fail():
    config_path = "Jenkins/jenkins_scenarios/scenario_03_html_reports/configs/app_config.json"

    # Write bad config
    config = {
        "ENV": "dev",
        "REPLICAS": 0
    }
    with open(config_path, "w") as f:
        json.dump(config, f)

    with open(config_path, "r") as f:
        config_data = json.load(f)

    assert config_data.get("REPLICAS", 0) >= 2, "REPLICAS must be >= 2!"
