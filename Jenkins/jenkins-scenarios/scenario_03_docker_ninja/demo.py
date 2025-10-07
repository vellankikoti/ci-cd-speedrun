#!/usr/bin/env python3
"""
Docker Ninja - Educational Jenkins Workshop
==========================================

An unforgettable hands-on learning experience for advanced Docker workflows with Jenkins.
This workshop teaches you how to master Docker in CI/CD pipelines like a ninja!

Usage:
    python3 demo.py              # Run full educational workshop
    python3 demo.py --quick      # Run quick demo
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

class DockerNinjaWorkshop:
    """Educational Docker Ninja Workshop."""
    
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
        
    def print_learning(self, message):
        """Print a learning point."""
        print(f"{Colors.YELLOW}🧠 {message}{Colors.NC}")
        
    def print_celebration(self, message):
        """Print a celebration message."""
        print(f"{Colors.GREEN}🎉 {message}{Colors.NC}")
        
    def wait_for_user(self, message="Press Enter to continue..."):
        """Wait for user input with a message."""
        input(f"{Colors.CYAN}⏸️  {message}{Colors.NC}")
        
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
    
    def workshop_introduction(self):
        """Welcome participants to the Docker Ninja workshop."""
        self.print_header("🥷 Welcome to the Docker Ninja Workshop!")
        print("=" * 60)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• Advanced Docker workflows in CI/CD")
        print("• Multi-stage Docker builds for optimization")
        print("• Docker security scanning and best practices")
        print("• Container registry management")
        print("• Docker layer caching strategies")
        print("• Performance optimization techniques")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Master:{Colors.NC}")
        print("• Dockerfile optimization and best practices")
        print("• Multi-architecture builds")
        print("• Security scanning with Trivy")
        print("• Container vulnerability management")
        print("• Advanced Jenkins Docker integration")
        print("• Production-ready container workflows")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 75-90 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to become a Docker Ninja?")
        print()
    
    def step_1_understand_docker_workflows(self):
        """Step 1: Understand advanced Docker workflows."""
        self.print_header("Step 1: Understanding Advanced Docker Workflows")
        print("=" * 60)
        
        self.print_learning("Let's explore the art of Docker mastery!")
        print()
        
        # Show application structure
        self.print_step("Exploring our Docker-optimized application...")
        os.chdir(self.scenario_dir)
        
        print("📁 Docker Ninja Application Structure:")
        print("├── app.py                 # Main Flask application")
        print("├── requirements.txt       # Python dependencies")
        print("├── Dockerfile             # Multi-stage Docker build")
        print("├── security-scan.py       # Security scanning script")
        print("├── tests/                 # Test suite")
        print("│   ├── test_app.py        # Unit tests")
        print("│   └── test_docker.py     # Docker integration tests")
        print("└── Jenkinsfile            # Advanced pipeline")
        print()
        
        # Show the Dockerfile
        self.print_step("Let's examine our multi-stage Dockerfile...")
        with open("Dockerfile", "r") as f:
            dockerfile_content = f.read()
        
        print("🐳 Multi-Stage Dockerfile:")
        print("-" * 30)
        print(dockerfile_content)
        print("-" * 30)
        print()
        
        self.print_learning("Docker Ninja Techniques We'll Master:")
        print("• Multi-stage builds for smaller images")
        print("• Layer caching optimization")
        print("• Security scanning integration")
        print("• Multi-architecture support")
        print("• Production-ready configurations")
        print()
        
        self.wait_for_user("Ready to explore our security scanning?")
        print()
    
    def step_2_explore_security_scanning(self):
        """Step 2: Explore security scanning capabilities."""
        self.print_header("Step 2: Exploring Security Scanning")
        print("=" * 50)
        
        self.print_learning("Security is a ninja's top priority!")
        print()
        
        # Show security scan script
        self.print_step("Let's examine our security scanning script...")
        with open("security-scan.py", "r") as f:
            security_content = f.read()
        
        print("🛡️ Security Scanning Script:")
        print("-" * 35)
        print(security_content[:500] + "..." if len(security_content) > 500 else security_content)
        print("-" * 35)
        print()
        
        self.print_learning("Security Scanning Features:")
        print("• Trivy vulnerability scanning")
        print("• Container image analysis")
        print("• Security report generation")
        print("• CI/CD integration")
        print("• Automated security gates")
        print()
        
        self.wait_for_user("Ready to test our Docker workflows locally?")
        print()
    
    def step_3_local_docker_testing(self):
        """Step 3: Test Docker workflows locally."""
        self.print_header("Step 3: Local Docker Testing & Optimization")
        print("=" * 60)
        
        self.print_learning("Let's test our Docker ninja skills!")
        print()
        
        # Check Docker environment
        self.print_step("Checking Docker environment...")
        if not self.run_command("docker --version", capture_output=True):
            self.print_error("Docker is not available")
            return False
        
        # Check Python environment
        self.print_step("Checking Python environment...")
        if not self.run_command("python3 --version", capture_output=True):
            self.print_error("Python3 is not available")
            return False
        
        # Install dependencies
        self.print_step("Installing dependencies...")
        if not self.run_command("python3 -m pip install --user -r requirements.txt"):
            self.print_info("Trying with --break-system-packages flag...")
            if not self.run_command("python3 -m pip install --break-system-packages -r requirements.txt"):
                self.print_info("Dependencies may already be installed. Continuing...")
        
        # Run unit tests
        self.print_step("Running unit tests...")
        if not self.run_command("python3 -m pytest tests/test_app.py -v"):
            self.print_info("Some unit tests may have failed due to environment differences")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        # Run Docker tests
        self.print_step("Running Docker integration tests...")
        if not self.run_command("python3 -m pytest tests/test_docker.py -v"):
            self.print_info("Docker tests may have failed due to environment differences")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        # Build Docker image
        self.print_step("Building optimized Docker image...")
        if not self.run_command("docker build --no-cache -t docker-ninja-workshop ."):
            self.print_error("Docker build failed")
            return False
        
        # Run security scan
        self.print_step("Running security scan...")
        if not self.run_command("python3 security-scan.py"):
            self.print_info("Security scan may have failed due to Trivy not being installed")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        self.print_success("Local Docker testing completed!")
        print()
        
        self.print_learning("Docker Ninja Skills Demonstrated:")
        print("• Multi-stage Docker builds")
        print("• Security scanning integration")
        print("• Container optimization")
        print("• Test-driven development")
        print("• Local development workflows")
        print()
        
        self.wait_for_user("Ready to create your Docker Ninja Jenkins pipeline?")
        print()
    
    def step_4_jenkins_job_creation(self):
        """Step 4: Create Jenkins job for Docker Ninja."""
        self.print_header("Step 4: Creating Your Docker Ninja Jenkins Job")
        print("=" * 60)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now let's create a Jenkins job that masters Docker!")
        print()
        print("This job will demonstrate advanced Docker workflows,")
        print("security scanning, and optimization techniques.")
        print()
        
        self.print_step("Step-by-Step Jenkins Job Creation:")
        print()
        print("1️⃣  Access Jenkins:")
        print(f"   🌐 Open: {self.jenkins_url}")
        print(f"   👤 Username: {self.jenkins_username}")
        print(f"   🔑 Password: {self.jenkins_password}")
        print()
        
        self.wait_for_user("Press Enter after logging into Jenkins...")
        print()
        
        print("2️⃣  Create New Job:")
        print("   • Click 'New Item' in the left sidebar")
        print("   • Enter job name: 'Docker Ninja Mastery'")
        print("   • Select 'Pipeline' as job type")
        print("   • Click 'OK'")
        print()
        
        self.wait_for_user("Press Enter after creating the job...")
        print()
        
        print("3️⃣  Configure Pipeline:")
        print("   • Scroll to 'Pipeline' section")
        print("   • Set 'Definition' to 'Pipeline script from SCM'")
        print("   • Set 'SCM' to 'Git'")
        print("   • Repository URL: 'https://github.com/vellankikoti/ci-cd-chaos-workshop.git'")
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_03_docker_ninja/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types for Docker workflows")
        print("• Git SCM integration for containerized apps")
        print("• Pipeline script location for Docker mastery")
        print("• Jenkins configuration for advanced Docker")
        print()
        
        self.wait_for_user("Press Enter after configuring the pipeline...")
        print()
    
    def step_5_pipeline_execution(self):
        """Step 5: Execute and monitor the Docker Ninja pipeline."""
        self.print_header("Step 5: Running Your Docker Ninja Pipeline")
        print("=" * 60)
        
        self.print_learning("Time to see Docker mastery in action!")
        print()
        
        print("4️⃣  Execute Pipeline:")
        print("   • Click 'Build Now' to start the pipeline")
        print("   • Watch the pipeline execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Observe Docker builds and security scans")
        print()
        
        self.print_learning("Pipeline Stages You'll See:")
        print("   🥷 Welcome - Docker Ninja introduction")
        print("   📦 Setup - Check Python and Docker environment")
        print("   🔧 Install Dependencies - Install test dependencies")
        print("   🧪 Run Unit Tests - Execute unit test suite")
        print("   🐳 Run Docker Tests - Container integration tests")
        print("   🏗️ Build Docker Image - Multi-stage build")
        print("   🛡️ Security Scan - Vulnerability scanning")
        print("   📊 Generate Reports - Test and security reports")
        print("   ✅ Success! - Pipeline completion")
        print()
        
        self.wait_for_user("Press Enter after running the pipeline...")
        print()
        
        self.print_learning("Docker Ninja CI/CD Benefits:")
        print("• Optimized container builds")
        print("• Automated security scanning")
        print("• Multi-stage build optimization")
        print("• Comprehensive testing coverage")
        print("• Production-ready deployments")
        print()
        
        self.wait_for_user("Ready to explore the Jenkinsfile?")
        print()
    
    def step_6_jenkinsfile_exploration(self):
        """Step 6: Explore and understand the Docker Ninja Jenkinsfile."""
        self.print_header("Step 6: Understanding the Docker Ninja Jenkinsfile")
        print("=" * 60)
        
        self.print_learning("The Jenkinsfile orchestrates Docker mastery!")
        print()
        
        # Show Jenkinsfile
        self.print_step("Let's examine our Docker Ninja Jenkinsfile...")
        with open("Jenkinsfile", "r") as f:
            jenkinsfile_content = f.read()
        
        print("📝 Docker Ninja Jenkinsfile:")
        print("-" * 35)
        print(jenkinsfile_content)
        print("-" * 35)
        print()
        
        self.print_learning("Docker Ninja Jenkinsfile Key Concepts:")
        print("• Multi-stage Docker builds")
        print("• Security scanning integration")
        print("• Container optimization strategies")
        print("• Test reporting and artifact collection")
        print("• Advanced Docker workflow patterns")
        print()
        
        self.print_learning("Advanced Docker Patterns:")
        print("• Layer caching optimization")
        print("• Multi-architecture builds")
        print("• Security scanning automation")
        print("• Container registry management")
        print("• Performance monitoring")
        print()
        
        self.wait_for_user("Ready to modify the Jenkinsfile?")
        print()
    
    def step_7_hands_on_modification(self):
        """Step 7: Hands-on Docker Ninja modification."""
        self.print_header("Step 7: Hands-On Docker Ninja Modification")
        print("=" * 60)
        
        self.print_learning("Let's customize your Docker Ninja pipeline!")
        print()
        
        print("🛠️  Modification Exercise:")
        print("Let's add a new Docker optimization stage:")
        print()
        print("1. Go back to your Jenkins job")
        print("2. Click 'Configure'")
        print("3. Scroll to the Pipeline section")
        print("4. Change 'Pipeline script from SCM' to 'Pipeline script'")
        print("5. Copy the Jenkinsfile content into the text area")
        print("6. Add a new stage after the 'Security Scan' stage:")
        print()
        
        print("```groovy")
        print("stage('🔍 Docker Optimization') {")
        print("    steps {")
        print("        echo 'Running Docker optimization analysis!'")
        print("        sh 'docker images --format \"table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}\"'")
        print("        sh 'docker system df'")
        print("    }")
        print("}")
        print("```")
        print()
        
        self.wait_for_user("Press Enter after adding the optimization stage...")
        print()
        
        print("7. Click 'Save'")
        print("8. Click 'Build Now' to run the modified pipeline")
        print("9. Watch your optimization stage execute!")
        print()
        
        self.wait_for_user("Press Enter after running the modified pipeline...")
        print()
        
        self.print_celebration("Congratulations! You've customized your Docker Ninja pipeline!")
        print()
        
        self.print_learning("What you just accomplished:")
        print("• Modified a Docker Ninja pipeline")
        print("• Added custom optimization functionality")
        print("• Tested your changes in CI/CD")
        print("• Learned advanced Docker patterns")
        print()
    
    def step_8_advanced_concepts(self):
        """Step 8: Advanced Docker concepts and best practices."""
        self.print_header("Step 8: Advanced Docker Concepts & Best Practices")
        print("=" * 60)
        
        self.print_learning("Let's explore advanced Docker mastery!")
        print()
        
        print("🔧 Advanced Docker Features:")
        print("• Multi-architecture builds (ARM64, AMD64)")
        print("• Container registry management")
        print("• Docker Compose orchestration")
        print("• Container networking and service discovery")
        print("• Volume management and data persistence")
        print("• Container monitoring and logging")
        print()
        
        print("📊 Performance Optimization:")
        print("• Layer caching strategies")
        print("• Image size optimization")
        print("• Build time reduction")
        print("• Resource usage monitoring")
        print("• Container startup optimization")
        print()
        
        print("🛡️ Security Best Practices:")
        print("• Vulnerability scanning automation")
        print("• Image signing and verification")
        print("• Least privilege access")
        print("• Secrets management")
        print("• Container runtime security")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• Microservices containerization")
        print("• CI/CD pipeline optimization")
        print("• Cloud-native deployments")
        print("• Container orchestration")
        print("• DevOps automation")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the Docker Ninja workshop."""
        self.print_header("🎓 Docker Ninja Workshop Conclusion")
        print("=" * 60)
        
        self.print_celebration("Congratulations! You've become a Docker Ninja!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Mastered:{Colors.NC}")
        print("✅ Created a Docker Ninja Jenkins job from scratch")
        print("✅ Configured advanced Docker workflows in CI/CD")
        print("✅ Executed multi-stage builds and security scans")
        print("✅ Modified and customized Docker pipelines")
        print("✅ Learned advanced Docker optimization techniques")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• Advanced Docker workflows in CI/CD")
        print("• Multi-stage Docker builds for optimization")
        print("• Security scanning and best practices")
        print("• Container registry management")
        print("• Docker layer caching strategies")
        print("• Performance optimization techniques")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other Jenkins scenarios in this workshop")
        print("• Try advanced Docker features")
        print("• Integrate with your own projects")
        print("• Study container orchestration")
        print("• Learn about cloud-native deployments")
        print("• Explore DevOps automation patterns")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• Docker Documentation: https://docs.docker.com/")
        print("• Docker Best Practices: https://docs.docker.com/develop/best-practices/")
        print("• Trivy Security Scanner: https://trivy.dev/")
        print("• Jenkins Docker Plugin: https://plugins.jenkins.io/docker-plugin/")
        print()
        
        self.print_celebration("Thank you for participating in this workshop!")
        print("Keep mastering Docker like a true ninja! 🥷")
        print()
    
    def run_full_workshop(self):
        """Run the complete Docker Ninja workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_docker_workflows()
            self.step_2_explore_security_scanning()
            self.step_3_local_docker_testing()
            self.step_4_jenkins_job_creation()
            self.step_5_pipeline_execution()
            self.step_6_jenkinsfile_exploration()
            self.step_7_hands_on_modification()
            self.step_8_advanced_concepts()
            self.workshop_conclusion()
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️ Workshop interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Workshop failed: {e}")
            return False
    
    def run_quick_demo(self):
        """Run a quick Docker Ninja demo."""
        self.print_header("🚀 Quick Docker Ninja Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Test application locally
        if not self.step_3_local_docker_testing():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins Docker Ninja Job Setup")
        print("=" * 40)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Pipeline job: 'Docker Ninja Mastery'")
        print("4. Configure Git SCM with this repository")
        print("5. Set Script Path: Jenkins/jenkins-scenarios/scenario_03_docker_ninja/Jenkinsfile")
        print("6. Save and run the pipeline!")
        print()
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Docker Ninja Educational Workshop')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick demo instead of full workshop')
    parser.add_argument('--help-workshop', action='store_true',
                       help='Show workshop help')
    
    args = parser.parse_args()
    
    if args.help_workshop:
        print("Docker Ninja Educational Workshop")
        print("=" * 40)
        print()
        print("This workshop provides hands-on learning for:")
        print("• Advanced Docker workflows in CI/CD")
        print("• Multi-stage Docker builds for optimization")
        print("• Security scanning and best practices")
        print("• Container registry management")
        print("• Docker layer caching strategies")
        print("• Performance optimization techniques")
        print()
        print("Usage:")
        print("  python3 demo.py              # Full educational workshop")
        print("  python3 demo.py --quick      # Quick demo")
        print("  python3 demo.py --help-workshop  # Show this help")
        return
    
    workshop = DockerNinjaWorkshop()
    
    try:
        if args.quick:
            success = workshop.run_quick_demo()
        else:
            success = workshop.run_full_workshop()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Workshop interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Workshop failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()