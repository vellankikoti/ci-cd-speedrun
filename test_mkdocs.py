#!/usr/bin/env python3
"""
Test script for MkDocs setup
Verifies that all documentation files exist and are properly configured
"""

import os
import yaml
from pathlib import Path

def test_mkdocs_setup():
    """Test the MkDocs setup and verify all files exist"""
    
    print("🔍 Testing MkDocs Setup for CI/CD Chaos Workshop")
    print("=" * 50)
    
    # Check if mkdocs.yml exists
    if not os.path.exists("mkdocs.yml"):
        print("❌ mkdocs.yml not found!")
        return False
    
    print("✅ mkdocs.yml found")
    
    # Load mkdocs.yml
    try:
        with open("mkdocs.yml", "r") as f:
            config = yaml.safe_load(f)
        print("✅ mkdocs.yml is valid YAML")
    except Exception as e:
        print(f"❌ Error loading mkdocs.yml: {e}")
        return False
    
    # Check navigation structure
    if "nav" not in config:
        print("❌ No navigation found in mkdocs.yml")
        return False
    
    print("✅ Navigation structure found")
    
    # Check if docs directory exists
    if not os.path.exists("docs"):
        print("❌ docs directory not found!")
        return False
    
    print("✅ docs directory found")
    
    # Check required files
    required_files = [
        "docs/index.md",
        "docs/phases/setup.md",
        "docs/phases/docker.md",
        "docs/phases/jenkins.md",
        "docs/phases/k8s.md",
        "docs/certificate.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    # Check testcontainers files
    testcontainers_dir = "docs/testcontainers"
    if os.path.exists(testcontainers_dir):
        testcontainers_files = [
            "mysql.md",
            "mariadb.md", 
            "postgres.md",
            "mongodb.md",
            "redis.md"
        ]
        
        for file_name in testcontainers_files:
            file_path = os.path.join(testcontainers_dir, file_name)
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"⚠️  {file_path} (optional)")
    
    # Check jenkins files
    jenkins_dir = "docs/jenkins"
    if os.path.exists(jenkins_dir):
        jenkins_files = [
            "scenario_01_docker_build.md",
            "scenario_02_testcontainers.md",
            "scenario_03_html_reports.md",
            "scenario_04_manage_secrets.md",
            "scenario_05_deploy_eks.md"
        ]
        
        for file_name in jenkins_files:
            file_path = os.path.join(jenkins_dir, file_name)
            if os.path.exists(file_path):
                print(f"✅ {file_path}")
            else:
                print(f"⚠️  {file_path} (optional)")
    
    print("\n🎉 MkDocs setup test completed!")
    print("📖 To build the documentation:")
    print("   mkdocs build")
    print("📖 To serve locally:")
    print("   mkdocs serve")
    
    return True

if __name__ == "__main__":
    test_mkdocs_setup() 