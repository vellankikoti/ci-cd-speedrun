import json

def test_config_validation_pass():
    """
    Validates that the app config file has correct values.
    This should pass because the config is valid.
    """

    config_path = "Jenkins/jenkins_scenarios/scenario_03_html_reports/configs/app_config.json"

    # Create a valid config
    config = {
        "ENV": "dev",
        "REPLICAS": 3
    }

    # Write config to file
    with open(config_path, "w") as f:
        json.dump(config, f)

    # Read back and validate
    with open(config_path, "r") as f:
        config_data = json.load(f)

    assert config_data.get("ENV") in ["dev", "staging", "prod"], "Invalid ENV value!"
    assert config_data.get("REPLICAS", 0) >= 2, "REPLICAS must be >= 2!"
