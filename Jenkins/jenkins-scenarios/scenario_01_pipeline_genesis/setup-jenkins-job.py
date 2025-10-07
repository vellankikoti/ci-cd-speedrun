#!/usr/bin/env python3
"""
Pipeline Genesis - Jenkins Job Setup Script
Automatically creates the Jenkins job for this scenario.
"""

import requests
import json
import time
import sys

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
    """Create the Jenkins job for Pipeline Genesis."""
    print("🔧 Creating Jenkins job for Pipeline Genesis...")
    
    # Job configuration
    job_config = {
        "name": "Pipeline Genesis",
        "description": "Your first Jenkins pipeline - simple and clean!",
        "pipeline": {
            "definition": {
                "type": "SCM",
                "scm": {
                    "type": "Git",
                    "repository": "https://github.com/vellankikoti/ci-cd-chaos-workshop.git",
                    "scriptPath": "Jenkins/jenkins-scenarios/01-pipeline-genesis/Jenkinsfile"
                }
            }
        }
    }
    
    # Convert to Jenkins XML format (simplified)
    xml_config = f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.41">
  <description>{job_config['description']}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.90">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@4.8.3">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>{job_config['pipeline']['definition']['scm']['repository']}</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="list"/>
      <extensions/>
    </scm>
    <scriptPath>{job_config['pipeline']['definition']['scm']['scriptPath']}</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>"""
    
    try:
        # Create the job
        response = requests.post(
            "http://localhost:8080/createItem?name=Pipeline%20Genesis",
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
    print("🚀 Pipeline Genesis - Jenkins Job Setup")
    print("=" * 50)
    print("This script will create a Jenkins job for your first pipeline!")
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
        print("2. Find the 'Pipeline Genesis' job")
        print("3. Click 'Build Now'")
        print("4. Watch your first pipeline run!")
        print()
        print("Login credentials: admin/admin")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
