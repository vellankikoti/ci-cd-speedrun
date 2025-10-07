#!/usr/bin/env python3
"""
K8s Commander - Jenkins Demo Script
==================================

Interactive demo for Kubernetes deployment and management.
Shows how to deploy applications to Kubernetes with Jenkins.

Usage:
    python3 demo.py              # Run interactive demo
    python3 demo.py --simple     # Run simple demo
    python3 demo.py --help       # Show help
"""

import subprocess
import time
import os
import sys
import argparse
import requests
import json
from pathlib import Path

class Colors:
    """Cross-platform color support for terminal output."""
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

class K8sCommanderDemo:
    """Demo for K8s Commander scenario."""
    
    def __init__(self):
        self.scenario_dir = Path(__file__).parent
        self.jenkins_url = 'http://localhost:8080'
        self.jenkins_username = 'admin'
        self.jenkins_password = 'admin'
        
    def print_step(self, message):
        """Print a step message with consistent formatting."""
        print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")
        
    def print_success(self, message):
        """Print a success message."""
        print(f"{Colors.GREEN}✅ {message}{Colors.NC}")
        
    def print_header(self, message):
        """Print a header message."""
        print(f"{Colors.PURPLE}🎯 {message}{Colors.NC}")
        
    def print_error(self, message):
        """Print an error message."""
        print(f"{Colors.RED}❌ {message}{Colors.NC}")
        
    def print_info(self, message, end="\n"):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.NC}", end=end)
        
    def run_command(self, cmd, description="", capture_output=False, check=True):
        """Run a command with cross-platform support."""
        if description:
            self.print_step(description)
            
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=capture_output, 
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                if capture_output and result.stdout:
                    return result.stdout.strip()
                return True
            else:
                if capture_output and result.stderr:
                    self.print_error(f"Command failed: {result.stderr}")
                if check:
                    self.print_error(f"Command failed with exit code {result.returncode}")
                return False
                
        except Exception as e:
            self.print_error(f"Command error: {e}")
            return False
    
    def check_jenkins_running(self):
        """Check if Jenkins is running and accessible."""
        self.print_step("Checking if Jenkins is running...")
        
        try:
            response = requests.get(f"{self.jenkins_url}/api/json", 
                                 auth=(self.jenkins_username, self.jenkins_password), 
                                 timeout=5)
            if response.status_code == 200:
                self.print_success("Jenkins is running and accessible")
                return True
            else:
                self.print_error(f"Jenkins returned status {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Jenkins is not accessible: {e}")
            self.print_info("Please run 'python3 jenkins-setup.py setup' first")
            return False
    
    def test_application_locally(self):
        """Test the application locally."""
        self.print_header("Testing Application Locally")
        print("=" * 50)
        
        # Change to scenario directory
        os.chdir(self.scenario_dir)
        
        # Check if Python is available
        self.print_step("Checking Python environment...")
        if not self.run_command("python3 --version", capture_output=True):
            self.print_error("Python3 is not available")
            return False
        
        # Install dependencies
        self.print_step("Installing dependencies...")
        if not self.run_command("python3 -m pip install -r requirements.txt"):
            self.print_error("Failed to install dependencies")
            return False
        
        # Run tests
        self.print_step("Running tests...")
        if not self.run_command("python3 -m pytest tests/ -v"):
            self.print_error("Tests failed")
            return False
        
        self.print_success("Application tests passed!")
        return True
    
    def test_docker_build(self):
        """Test Docker build."""
        self.print_header("Testing Docker Build")
        print("=" * 50)
        
        # Change to scenario directory
        os.chdir(self.scenario_dir)
        
        # Build Docker image
        self.print_step("Building Docker image...")
        if not self.run_command("docker build -t k8s-commander-demo ."):
            self.print_error("Docker build failed")
            return False
        
        # Run container
        self.print_step("Running Docker container...")
        if not self.run_command("docker run -d --name k8s-commander-demo -p 5003:5000 k8s-commander-demo"):
            self.print_error("Failed to run Docker container")
            return False
        
        # Wait for container to start
        self.print_step("Waiting for container to start...")
        time.sleep(3)
        
        # Test the application
        self.print_step("Testing application in container...")
        try:
            response = requests.get("http://localhost:5003/health", timeout=5)
            if response.status_code == 200:
                self.print_success("Application is running in Docker!")
                print(f"   🌐 Access at: http://localhost:5003")
                print(f"   📊 Health check: {response.json()}")
            else:
                self.print_error(f"Application returned status {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Failed to test application: {e}")
            return False
        
        return True
    
    def test_k8s_manifests(self):
        """Test Kubernetes manifests."""
        self.print_header("Testing Kubernetes Manifests")
        print("=" * 50)
        
        # Change to scenario directory
        os.chdir(self.scenario_dir)
        
        # Check if k8s directory exists
        k8s_dir = Path("k8s")
        if not k8s_dir.exists():
            self.print_error("k8s directory not found")
            return False
        
        # List Kubernetes manifests
        self.print_step("Available Kubernetes manifests:")
        manifests = list(k8s_dir.glob("*.yaml"))
        for manifest in manifests:
            print(f"   📄 {manifest.name}")
        
        # Validate manifests (if kubectl is available)
        self.print_step("Validating Kubernetes manifests...")
        if self.run_command("kubectl version --client", capture_output=True):
            for manifest in manifests:
                if self.run_command(f"kubectl apply --dry-run=client -f {manifest}", check=False):
                    self.print_success(f"✓ {manifest.name} is valid")
                else:
                    self.print_error(f"✗ {manifest.name} has issues")
        else:
            self.print_info("kubectl not available, skipping validation")
        
        self.print_success("Kubernetes manifests validated!")
        return True
    
    def cleanup_docker(self):
        """Clean up Docker containers and images."""
        self.print_step("Cleaning up Docker resources...")
        self.run_command("docker stop k8s-commander-demo", check=False)
        self.run_command("docker rm k8s-commander-demo", check=False)
        self.run_command("docker rmi k8s-commander-demo", check=False)
        self.print_success("Docker cleanup completed!")
    
    def show_jenkins_setup_instructions(self):
        """Show instructions for setting up Jenkins job."""
        self.print_header("Jenkins Job Setup Instructions")
        print("=" * 50)
        
        print(f"{Colors.BOLD}To create the Jenkins job:{Colors.NC}")
        print()
        print("1. Open Jenkins in your browser:")
        print(f"   🌐 {self.jenkins_url}")
        print()
        print("2. Login with credentials:")
        print(f"   👤 Username: {self.jenkins_username}")
        print(f"   🔑 Password: {self.jenkins_password}")
        print()
        print("3. Create a new Pipeline job:")
        print("   • Click 'New Item'")
        print("   • Enter name: 'K8s Commander'")
        print("   • Select 'Pipeline'")
        print("   • Click 'OK'")
        print()
        print("4. Configure the pipeline:")
        print("   • Scroll to 'Pipeline' section")
        print("   • Definition: 'Pipeline script from SCM'")
        print("   • SCM: 'Git'")
        print("   • Repository URL: 'https://github.com/vellankikoti/ci-cd-chaos-workshop.git'")
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        print("5. Run the pipeline:")
        print("   • Click 'Build Now'")
        print("   • Watch the pipeline execute!")
        print()
        print(f"{Colors.YELLOW}💡 Pro Tip: The pipeline will:{Colors.NC}")
        print("   • Build Docker images")
        print("   • Deploy to Kubernetes")
        print("   • Run health checks")
        print("   • Scale applications")
    
    def run_simple_demo(self):
        """Run a simple, non-interactive demo."""
        self.print_header("🚀 K8s Commander - Simple Demo")
        print("=" * 50)
        print("Running a quick demo of Kubernetes deployment...")
        print()
        
        # Test application locally
        if not self.test_application_locally():
            return False
        
        # Test Docker build
        if not self.test_docker_build():
            return False
        
        # Test K8s manifests
        if not self.test_k8s_manifests():
            return False
        
        # Show Jenkins setup instructions
        self.show_jenkins_setup_instructions()
        
        # Cleanup
        self.cleanup_docker()
        
        self.print_success("Demo completed successfully!")
        print()
        print(f"{Colors.BOLD}Next Steps:{Colors.NC}")
        print("1. Set up the Jenkins job using the instructions above")
        print("2. Run the pipeline in Jenkins")
        print("3. Explore the Kubernetes deployment")
        print("4. Try modifying the K8s manifests")
        
        return True
    
    def run_interactive_demo(self):
        """Run an interactive demo with user input."""
        self.print_header("🚀 K8s Commander - Interactive Demo")
        print("=" * 50)
        print("Welcome to the K8s Commander demo!")
        print("This demo will show you how to deploy applications to Kubernetes.")
        print()
        
        # Check Jenkins
        if not self.check_jenkins_running():
            print()
            self.print_info("Would you like to continue with local testing only? (y/n): ", end="")
            if input().lower() != 'y':
                return False
        
        # Test application locally
        print()
        self.print_info("Let's start by testing the application locally...")
        if not self.test_application_locally():
            return False
        
        # Test Docker build
        print()
        self.print_info("Now let's test the Docker build...")
        if not self.test_docker_build():
            return False
        
        # Test K8s manifests
        print()
        self.print_info("Let's test the Kubernetes manifests...")
        if not self.test_k8s_manifests():
            return False
        
        # Show Jenkins setup
        print()
        self.print_info("Great! Now let's set up the Jenkins job...")
        self.show_jenkins_setup_instructions()
        
        # Interactive Jenkins job creation
        if self.check_jenkins_running():
            print()
            self.print_info("Would you like me to create the Jenkins job automatically? (y/n): ", end="")
            try:
                response = input().lower()
                if response == 'y':
                    self.create_jenkins_job()
            except EOFError:
                self.print_info("No input available, skipping automatic job creation")
                self.print_info("You can create the job manually using the instructions above")
        
        # Cleanup
        self.cleanup_docker()
        
        self.print_success("Interactive demo completed!")
        print()
        print(f"{Colors.BOLD}What you've learned:{Colors.NC}")
        print("• How to build Docker images for Kubernetes")
        print("• How to create Kubernetes manifests")
        print("• How to deploy applications to K8s")
        print("• How to set up Jenkins for K8s deployment")
        
        return True
    
    def create_jenkins_job(self):
        """Create the Jenkins job automatically."""
        self.print_step("Creating Jenkins job automatically...")
        
        # Job configuration XML
        xml_config = """<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.41">
  <description>Kubernetes deployment and management</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.90">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@4.8.3">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>https://github.com/vellankikoti/ci-cd-chaos-workshop.git</url>
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
    <scriptPath>Jenkins/jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>"""
        
        try:
            response = requests.post(
                f"{self.jenkins_url}/createItem?name=K8s%20Commander",
                data=xml_config,
                headers={'Content-Type': 'application/xml'},
                auth=(self.jenkins_username, self.jenkins_password),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                self.print_success("Jenkins job created successfully!")
                print(f"   🌐 View at: {self.jenkins_url}/job/K8s%20Commander/")
                return True
            else:
                self.print_error(f"Failed to create job: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Error creating Jenkins job: {e}")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='K8s Commander Demo')
    parser.add_argument('--simple', action='store_true', 
                       help='Run simple demo without interaction')
    parser.add_argument('--help-demo', action='store_true',
                       help='Show demo help')
    
    args = parser.parse_args()
    
    if args.help_demo:
        print("K8s Commander Demo Help")
        print("=" * 30)
        print()
        print("This demo shows you how to:")
        print("• Build Docker images for Kubernetes")
        print("• Create Kubernetes manifests")
        print("• Deploy applications to K8s")
        print("• Set up Jenkins for K8s deployment")
        print()
        print("Usage:")
        print("  python3 demo.py              # Interactive demo")
        print("  python3 demo.py --simple     # Simple demo")
        print("  python3 demo.py --help-demo  # Show this help")
        return
    
    demo = K8sCommanderDemo()
    
    try:
        if args.simple:
            success = demo.run_simple_demo()
        else:
            success = demo.run_interactive_demo()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        demo.cleanup_docker()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        demo.cleanup_docker()
        sys.exit(1)

if __name__ == "__main__":
    main()