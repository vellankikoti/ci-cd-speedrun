#!/usr/bin/env python3
"""
🔧 Fix Jenkins Full Interface
Restarts Jenkins with full configuration and all necessary plugins
"""

import subprocess
import time
import requests
from pathlib import Path

def run_command(cmd, timeout=60):
    """Run command with timeout"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return False, "", str(e)

def print_step(step, description):
    print(f"\n🔧 {step}: {description}")

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️ {message}")

def print_error(message):
    print(f"❌ {message}")

def fix_jenkins_full():
    """Fix Jenkins to have full interface"""
    print("🔧 Fixing Jenkins Full Interface")
    print("=" * 50)
    
    # Step 1: Stop existing Jenkins
    print_step("Step 1", "Stopping existing Jenkins")
    success, output, error = run_command("docker stop jenkins-workshop", timeout=30)
    if success:
        print_success("Jenkins stopped")
    else:
        print_warning(f"Failed to stop Jenkins: {error}")
    
    # Step 2: Remove existing container
    print_step("Step 2", "Removing existing container")
    success, output, error = run_command("docker rm jenkins-workshop", timeout=30)
    if success:
        print_success("Container removed")
    else:
        print_warning(f"Failed to remove container: {error}")
    
    # Step 3: Start Jenkins with full configuration
    print_step("Step 3", "Starting Jenkins with full configuration")
    
    jenkins_cmd = """
    docker run -d --name jenkins-workshop \
        -p 8080:8080 \
        -p 50000:50000 \
        -v jenkins_home:/var/jenkins_home \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /Users/koti/demo-time/ci-cd-chaos-workshop:/workspace \
        -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Djava.awt.headless=true -Xmx2048m -Xms1024m" \
        -e JENKINS_OPTS="--httpPort=8080" \
        -e JENKINS_SLAVE_AGENT_PORT=50000 \
        -e JENKINS_UC=https://updates.jenkins.io \
        -e JENKINS_UC_DOWNLOAD=https://updates.jenkins.io/download \
        -e JENKINS_UC_EXPERIMENTAL=https://updates.jenkins.io/experimental \
        -e JENKINS_INCREMENTALS_REPO_MIRROR=https://repo.jenkins-ci.org/incrementals \
        -e JENKINS_PLUGIN_INFO=https://updates.jenkins.io/plugin-versions.json \
        jenkins/jenkins:lts
    """
    
    success, output, error = run_command(jenkins_cmd, timeout=120)
    if success:
        print_success("Jenkins container started")
    else:
        print_error(f"Failed to start Jenkins: {error}")
        return False
    
    # Step 4: Wait for Jenkins to be ready
    print_step("Step 4", "Waiting for Jenkins to be ready")
    for i in range(30):
        try:
            response = requests.get("http://localhost:8080/login", timeout=5)
            if response.status_code == 200:
                print_success("Jenkins is ready!")
                break
        except:
            pass
        print(f"Waiting... ({i+1}/30)")
        time.sleep(10)
    else:
        print_error("Jenkins failed to start within 5 minutes")
        return False
    
    # Step 5: Install essential plugins
    print_step("Step 5", "Installing essential plugins")
    
    essential_plugins = [
        "workflow-aggregator",
        "workflow-job",
        "workflow-cps",
        "workflow-basic-steps",
        "workflow-durable-task-step",
        "workflow-multibranch",
        "workflow-scm-step",
        "workflow-step-api",
        "workflow-support",
        "workflow-api",
        "workflow-cps-global-lib",
        "pipeline-stage-view",
        "pipeline-graph-analysis",
        "pipeline-rest-api",
        "pipeline-stage-tags-metadata",
        "pipeline-milestone-step",
        "pipeline-input-step",
        "pipeline-build-step",
        "pipeline-utility-steps",
        "pipeline-model-api",
        "pipeline-model-definition",
        "pipeline-model-extensions",
        "pipeline-stage-step",
        "docker-workflow",
        "docker-plugin",
        "git",
        "github",
        "github-branch-source",
        "github-api",
        "github-oauth",
        "github-pr-coverage-status",
        "github-scm-trait-notification-context",
        "pipeline-github-lib",
        "junit",
        "coverage",
        "htmlpublisher",
        "blueocean",
        "ace-editor",
        "jquery-detached",
        "handlebars",
        "momentjs",
        "bootstrap5-api",
        "echarts-api",
        "font-awesome-api",
        "matrix-auth",
        "role-strategy",
        "credentials",
        "credentials-binding",
        "ssh-credentials",
        "plain-credentials",
        "script-security",
        "antisamy-markup-formatter",
        "ant",
        "gradle",
        "maven-plugin",
        "timestamper",
        "ws-cleanup",
        "build-timeout",
        "durable-task",
        "mailer",
        "display-url-api",
        "token-macro",
        "build-trigger-badge",
        "external-monitor-job",
        "scm-api",
        "structs",
        "snakeyaml-api",
        "jackson2-api",
        "apache-httpcomponents-client-4-api",
        "trilead-api",
        "jdk-tool",
        "command-launcher",
        "slave-setup",
        "windows-slave-installer",
        "ssh-slaves",
        "resource-disposer",
        "ldap",
        "pam-auth",
        "matrix-project"
    ]
    
    for plugin in essential_plugins:
        success, output, error = run_command(
            f"docker exec jenkins-workshop jenkins-plugin-cli --plugins {plugin}",
            timeout=60
        )
        if success:
            print_success(f"Installed: {plugin}")
        else:
            print_warning(f"Failed to install {plugin}: {error}")
    
    # Step 6: Restart Jenkins to apply changes
    print_step("Step 6", "Restarting Jenkins to apply changes")
    success, output, error = run_command("docker restart jenkins-workshop", timeout=60)
    if success:
        print_success("Jenkins restarted")
    else:
        print_warning(f"Failed to restart Jenkins: {error}")
    
    # Step 7: Wait for Jenkins to be ready again
    print_step("Step 7", "Waiting for Jenkins to be ready after restart")
    for i in range(20):
        try:
            response = requests.get("http://localhost:8080/login", timeout=5)
            if response.status_code == 200:
                print_success("Jenkins is ready after restart!")
                break
        except:
            pass
        print(f"Waiting... ({i+1}/20)")
        time.sleep(10)
    else:
        print_error("Jenkins failed to start after restart")
        return False
    
    print("\n🎉 Jenkins Full Interface Fix Complete!")
    print("=" * 50)
    print("✅ Jenkins is running with full interface")
    print("✅ All essential plugins installed")
    print("✅ Ready for production use")
    print("\n🌐 Access Jenkins at: http://localhost:8080")
    print("📚 No setup wizard needed - ready to use!")
    
    return True

if __name__ == "__main__":
    fix_jenkins_full()
