#!/usr/bin/env python3
"""
TestContainers Integration - Jenkins Job Setup Script
Automatically creates the Jenkins job for this scenario.
"""

import requests
import json
import time
import sys
import os

def wait_for_jenkins():
    """Wait for Jenkins to be ready."""
    print("⏳ Waiting for Jenkins to be ready...")
    
    for i in range(30):  # Wait up to 5 minutes
        try:
            response = requests.get("http://localhost:8080/api/json", timeout=5)
            if response.status_code == 200:
                print("✅ Jenkins is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"   Attempt {i+1}/30 - Jenkins not ready yet...")
        time.sleep(10)
    
    print("❌ Jenkins is not responding. Please check if it's running.")
    return False

def create_jenkins_job():
    """Create the Jenkins job for TestContainers Integration."""
    print("🔧 Creating Jenkins job for TestContainers Integration...")
    
    # Job configuration for Freestyle job (not pipeline)
    xml_config = f"""<?xml version='1.1' encoding='UTF-8'?>
<project>
  <description>TestContainers Integration Demo - Real database testing with PostgreSQL containers</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>DB_TYPE</name>
          <description>Database type for testing</description>
          <defaultValue>testcontainers</defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>TEST_MODE</name>
          <description>Test mode to run</description>
          <defaultValue>all</defaultValue>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@4.8.3">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>https://github.com/vellankikoti/ci-cd-chaos-workshop.git</url>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/docker-test</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/bash
set -e

echo "🐳 TestContainers Integration Demo"
echo "=================================="
echo ""

# Change to scenario directory
cd Jenkins/jenkins-scenarios/scenario_02_testcontainers

echo "📋 Job Parameters:"
echo "  DB_TYPE: $DB_TYPE"
echo "  TEST_MODE: $TEST_MODE"
echo ""

# Cross-platform Python detection
PYTHON_CMD="python3"
PIP_CMD="pip3"

if ! command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python"
fi

if ! command -v pip3 >/dev/null 2>&1; then
    if command -v pip >/dev/null 2>&1; then
        PIP_CMD="pip"
    else
        PIP_CMD="${PYTHON_CMD} -m pip"
    fi
fi

echo "🔧 Environment Setup:"
echo "  Python: $PYTHON_CMD"
echo "  Pip: $PIP_CMD"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
${PIP_CMD} install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Run different test modes
case "$TEST_MODE" in
    "demo")
        echo "🎬 Running TestContainers Demo..."
        ${PYTHON_CMD} demo_testcontainers.py
        ;;
    "tests")
        echo "🧪 Running TestContainers Tests..."
        ${PYTHON_CMD} -m pytest tests/test_testcontainers_integration.py -v --tb=short
        ;;
    "app-tests")
        echo "🧪 Running Application Tests..."
        ${PYTHON_CMD} -m pytest tests/test_app.py -v --tb=short
        ;;
    "docker")
        echo "🐳 Running Docker Compose Test..."
        docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
        ;;
    "all")
        echo "🚀 Running Complete TestContainers Suite..."
        echo ""
        
        echo "1️⃣ Running TestContainers Integration Tests..."
        ${PYTHON_CMD} -m pytest tests/test_testcontainers_integration.py -v --tb=short
        echo ""
        
        echo "2️⃣ Running Application Tests..."
        ${PYTHON_CMD} -m pytest tests/test_app.py -v --tb=short
        echo ""
        
        echo "3️⃣ Running Demo Script..."
        timeout 60 ${PYTHON_CMD} demo_testcontainers.py || echo "Demo completed or timed out"
        echo ""
        
        echo "✅ All tests completed successfully!"
        ;;
    *)
        echo "❌ Unknown test mode: $TEST_MODE"
        echo "Available modes: demo, tests, app-tests, docker, all"
        exit 1
        ;;
esac

echo ""
echo "🎉 TestContainers Integration Demo completed!"
echo "📊 Check the console output above for detailed results."
      </command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.tasks.junit.JUnitResultArchiver plugin="junit@1.52">
      <testResults>Jenkins/jenkins-scenarios/scenario_02_testcontainers/test-results/*.xml</testResults>
      <keepLongStdio>false</keepLongStdio>
      <healthScaleFactor>1.0</healthScaleFactor>
      <allowEmptyResults>true</allowEmptyResults>
    </hudson.tasks.junit.JUnitResultArchiver>
    <hudson.tasks.ArtifactArchiver>
      <artifacts>Jenkins/jenkins-scenarios/scenario_02_testcontainers/test-results/**</artifacts>
      <allowEmptyArchive>true</allowEmptyArchive>
      <onlyIfSuccessful>false</onlyIfSuccessful>
      <fingerprint>false</fingerprint>
      <defaultExcludes>true</defaultExcludes>
      <caseSensitive>true</caseSensitive>
    </hudson.tasks.ArtifactArchiver>
  </publishers>
  <buildWrappers>
    <hudson.plugins.ws__cleanup.PreBuildCleanup plugin="ws-cleanup@0.41">
      <deleteDirs>false</deleteDirs>
      <cleanupParameter></cleanupParameter>
      <externalDelete></externalDelete>
      <disableDeferredWipeout>false</disableDeferredWipeout>
    </hudson.plugins.ws__cleanup.PreBuildCleanup>
  </buildWrappers>
</project>"""
    
    try:
        # Create the job
        response = requests.post(
            "http://localhost:8080/createItem?name=TestContainers%20Integration",
            data=xml_config,
            headers={'Content-Type': 'application/xml'},
            auth=('admin', 'admin'),
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            print("✅ Jenkins job created successfully!")
            return True
        else:
            print(f"❌ Failed to create job: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating Jenkins job: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 TestContainers Integration - Jenkins Job Setup")
    print("=" * 60)
    print("This script will create a Jenkins job for TestContainers integration testing!")
    print()
    print("🎯 What this job will do:")
    print("• Run real TestContainers with PostgreSQL")
    print("• Execute comprehensive integration tests")
    print("• Demonstrate container-based testing patterns")
    print("• Show database operations and API testing")
    print()
    
    # Wait for Jenkins
    if not wait_for_jenkins():
        sys.exit(1)
    
    # Create the job
    if create_jenkins_job():
        print("\n🎉 Setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Go to Jenkins: http://localhost:8080")
        print("2. Find the 'TestContainers Integration' job")
        print("3. Click 'Build with Parameters'")
        print("4. Choose your test mode:")
        print("   • demo - Interactive TestContainers demo")
        print("   • tests - Run TestContainers integration tests")
        print("   • app-tests - Run application tests")
        print("   • docker - Run with Docker Compose")
        print("   • all - Run complete test suite")
        print("5. Click 'Build' and watch the magic happen!")
        print()
        print("Login credentials: admin/admin")
        print()
        print("🔍 What you'll see:")
        print("• Real PostgreSQL containers starting up")
        print("• Database initialization and testing")
        print("• API endpoint testing")
        print("• Performance and concurrent operation tests")
        print("• Complete TestContainers integration workflow")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
