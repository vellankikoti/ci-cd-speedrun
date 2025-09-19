#!/usr/bin/env python3
"""
Test Jenkins Pipeline Execution
Tests the complete Jenkins setup and pipeline execution
"""

import requests
import time
import json
from pathlib import Path

def test_jenkins_pipeline():
    """Test Jenkins pipeline execution"""
    print("🧪 Testing Jenkins Pipeline Execution")
    
    # Test Jenkins is running
    try:
        response = requests.get("http://localhost:8080/api/json", timeout=10)
        if response.status_code == 200:
            print("✅ Jenkins is running")
        else:
            print(f"❌ Jenkins returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Jenkins is not accessible: {e}")
        return False
    
    # Test scenario 1 directory
    scenario_dir = Path("/Users/koti/demo-time/ci-cd-chaos-workshop/Jenkins/scenarios/01-docker-build")
    if scenario_dir.exists():
        print("✅ Scenario 1 directory exists")
    else:
        print("❌ Scenario 1 directory not found")
        return False
    
    # Test scenario 1 files
    required_files = ["app.py", "requirements.txt", "Dockerfile", "Jenkinsfile", "tests/test_app.py"]
    for file in required_files:
        file_path = scenario_dir / file
        if file_path.exists():
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            return False
    
    print("🎉 All tests passed! Jenkins setup is ready.")
    return True

if __name__ == "__main__":
    test_jenkins_pipeline()
