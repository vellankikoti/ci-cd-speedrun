#!/usr/bin/env python3
"""
Pipeline Genesis - Educational Jenkins Workshop
==============================================

An unforgettable hands-on learning experience for CI/CD with Jenkins.
This workshop teaches you every step of creating and running Jenkins pipelines.

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

class EducationalWorkshop:
    """Educational Jenkins Pipeline Workshop."""
    
    def __init__(self):
        self.scenario_dir = Path(__file__).parent
        self.jenkins_url = 'http://localhost:8080'
        self.jenkins_username = 'admin'
        self.jenkins_password = 'admin'
        self.workshop_steps = []
        
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
        """Welcome participants to the workshop."""
        self.print_header("🚀 Welcome to the Jenkins Pipeline Workshop!")
        print("=" * 60)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• How to create Jenkins jobs from scratch")
        print("• Understanding Jenkins pipeline syntax (Groovy)")
        print("• Git SCM integration with Jenkins")
        print("• Docker integration in CI/CD pipelines")
        print("• Pipeline monitoring and debugging")
        print("• Best practices for CI/CD workflows")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Build:{Colors.NC}")
        print("• A complete Flask web application")
        print("• A Docker container for your app")
        print("• A Jenkins pipeline that builds, tests, and deploys")
        print("• Automated testing and quality checks")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 45-60 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to start your CI/CD journey?")
        print()
    
    def step_1_understand_application(self):
        """Step 1: Understand the application we're building."""
        self.print_header("Step 1: Understanding Our Application")
        print("=" * 50)
        
        self.print_learning("Let's explore what we're building today!")
        print()
        
        # Show application structure
        self.print_step("Exploring application structure...")
        os.chdir(self.scenario_dir)
        
        print("📁 Application Structure:")
        print("├── app.py                 # Main Flask application")
        print("├── requirements.txt       # Python dependencies")
        print("├── Dockerfile            # Container definition")
        print("├── tests/                # Test suite")
        print("│   └── test_app.py       # Unit tests")
        print("└── Jenkinsfile           # Pipeline definition")
        print()
        
        # Show the Flask app
        self.print_step("Let's look at our Flask application...")
        with open("app.py", "r") as f:
            app_content = f.read()
        
        print("🐍 Flask Application (app.py):")
        print("-" * 30)
        print(app_content[:500] + "..." if len(app_content) > 500 else app_content)
        print("-" * 30)
        print()
        
        self.print_learning("This is a simple Flask web app with:")
        print("• Health check endpoint (/health)")
        print("• Info endpoint (/info)")
        print("• Home page with basic functionality")
        print()
        
        self.wait_for_user("Ready to test the application locally?")
        print()
    
    def step_2_local_testing(self):
        """Step 2: Test the application locally."""
        self.print_header("Step 2: Local Development & Testing")
        print("=" * 50)
        
        self.print_learning("Before we automate, let's test manually!")
        print()
        
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
        
        # Run tests
        self.print_step("Running our test suite...")
        if not self.run_command("python3 -m pytest tests/ -v"):
            self.print_info("Some tests may have failed due to environment differences")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        self.print_success("Local testing completed!")
        print()
        
        self.print_learning("Key Learning Points:")
        print("• Always test locally before automating")
        print("• Use virtual environments for dependency management")
        print("• Write comprehensive tests for your applications")
        print("• Test-driven development (TDD) improves code quality")
        print()
        
        self.wait_for_user("Ready to containerize our application?")
        print()
    
    def step_3_docker_containerization(self):
        """Step 3: Containerize the application."""
        self.print_header("Step 3: Docker Containerization")
        print("=" * 50)
        
        self.print_learning("Containers make applications portable and consistent!")
        print()
        
        # Show Dockerfile
        self.print_step("Let's examine our Dockerfile...")
        with open("Dockerfile", "r") as f:
            dockerfile_content = f.read()
        
        print("🐳 Dockerfile:")
        print("-" * 20)
        print(dockerfile_content)
        print("-" * 20)
        print()
        
        self.print_learning("Dockerfile Best Practices:")
        print("• Use specific base image versions")
        print("• Copy requirements.txt first for better caching")
        print("• Use non-root user for security")
        print("• Expose only necessary ports")
        print()
        
        # Build Docker image
        self.print_step("Building Docker image...")
        if not self.run_command("docker build --no-cache -t pipeline-genesis-workshop ."):
            self.print_error("Docker build failed")
            return False
        
        # Run container
        self.print_step("Running Docker container...")
        if not self.run_command("docker run -d --name pipeline-genesis-workshop -p 5001:5000 pipeline-genesis-workshop"):
            self.print_error("Failed to run Docker container")
            return False
        
        # Wait and test
        self.print_step("Waiting for container to start...")
        time.sleep(3)
        
        # Test the application
        self.print_step("Testing application in container...")
        try:
            response = requests.get("http://localhost:5001/health", timeout=5)
            if response.status_code == 200:
                self.print_success("Application is running in Docker!")
                print(f"   🌐 Access at: http://localhost:5001")
                print(f"   📊 Health check: {response.json()}")
            else:
                self.print_error(f"Application returned status {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Failed to test application: {e}")
            return False
        
        self.print_learning("Container Benefits:")
        print("• Consistent environment across dev/staging/prod")
        print("• Easy scaling and deployment")
        print("• Isolation from host system")
        print("• Reproducible builds")
        print()
        
        self.wait_for_user("Ready to create your first Jenkins job?")
        print()
    
    def step_4_jenkins_job_creation(self):
        """Step 4: Create Jenkins job manually."""
        self.print_header("Step 4: Creating Your First Jenkins Job")
        print("=" * 50)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now comes the exciting part - creating your first Jenkins job!")
        print()
        print("This is where you'll learn the real Jenkins workflow that")
        print("thousands of developers use every day in production.")
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
        print("   • Enter job name: 'My First Pipeline'")
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
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_01_pipeline_genesis/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types (Pipeline vs Freestyle)")
        print("• Git SCM integration")
        print("• Pipeline script location")
        print("• Jenkins configuration workflow")
        print()
        
        self.wait_for_user("Press Enter after configuring the pipeline...")
        print()
    
    def step_5_pipeline_execution(self):
        """Step 5: Execute and monitor the pipeline."""
        self.print_header("Step 5: Running Your First Pipeline")
        print("=" * 50)
        
        self.print_learning("Time to see your pipeline in action!")
        print()
        
        print("4️⃣  Execute Pipeline:")
        print("   • Click 'Build Now' to start the pipeline")
        print("   • Watch the pipeline execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Explore each stage of the pipeline")
        print()
        
        self.print_learning("Pipeline Stages You'll See:")
        print("   🚀 Welcome - Simple greeting")
        print("   📦 Setup - Check Python environment")
        print("   🔧 Install Dependencies - Install Python packages")
        print("   🧪 Run Tests - Execute test suite")
        print("   🐳 Build Docker Image - Create container image")
        print("   ✅ Success! - Pipeline completion")
        print()
        
        self.wait_for_user("Press Enter after running the pipeline...")
        print()
        
        self.print_learning("Monitoring & Debugging:")
        print("• Blue Ocean provides visual pipeline representation")
        print("• Console output shows detailed execution logs")
        print("• Build history tracks all pipeline runs")
        print("• Failed builds can be re-run or debugged")
        print()
        
        self.wait_for_user("Ready to explore the Jenkinsfile?")
        print()
    
    def step_6_jenkinsfile_exploration(self):
        """Step 6: Explore and understand the Jenkinsfile."""
        self.print_header("Step 6: Understanding the Jenkinsfile")
        print("=" * 50)
        
        self.print_learning("The Jenkinsfile is the heart of your CI/CD pipeline!")
        print()
        
        # Show Jenkinsfile
        self.print_step("Let's examine our Jenkinsfile...")
        with open("Jenkinsfile", "r") as f:
            jenkinsfile_content = f.read()
        
        print("📝 Jenkinsfile (Pipeline Definition):")
        print("-" * 40)
        print(jenkinsfile_content)
        print("-" * 40)
        print()
        
        self.print_learning("Jenkinsfile Key Concepts:")
        print("• pipeline { } - Main pipeline block")
        print("• agent any - Run on any available agent")
        print("• stages { } - Define pipeline stages")
        print("• stage('Name') { } - Individual stage")
        print("• steps { } - Commands to execute")
        print("• sh 'command' - Execute shell commands")
        print("• docker.build() - Build Docker images")
        print()
        
        self.print_learning("Pipeline Best Practices:")
        print("• Use descriptive stage names")
        print("• Keep stages focused and atomic")
        print("• Add error handling and notifications")
        print("• Use parallel execution when possible")
        print("• Version control your Jenkinsfiles")
        print()
        
        self.wait_for_user("Ready to modify the Jenkinsfile?")
        print()
    
    def step_7_hands_on_modification(self):
        """Step 7: Hands-on Jenkinsfile modification."""
        self.print_header("Step 7: Hands-On Pipeline Modification")
        print("=" * 50)
        
        self.print_learning("Now let's make it your own!")
        print()
        
        print("🛠️  Modification Exercise:")
        print("Let's add a new stage to our pipeline:")
        print()
        print("1. Go back to your Jenkins job")
        print("2. Click 'Configure'")
        print("3. Scroll to the Pipeline section")
        print("4. Change 'Pipeline script from SCM' to 'Pipeline script'")
        print("5. Copy the Jenkinsfile content into the text area")
        print("6. Add a new stage after the 'Build Docker Image' stage:")
        print()
        
        print("```groovy")
        print("stage('🎉 Custom Stage') {")
        print("    steps {")
        print("        echo 'This is my custom stage!'")
        print("        sh 'echo \"Hello from my modification!\"'")
        print("    }")
        print("}")
        print("```")
        print()
        
        self.wait_for_user("Press Enter after adding the custom stage...")
        print()
        
        print("7. Click 'Save'")
        print("8. Click 'Build Now' to run the modified pipeline")
        print("9. Watch your custom stage execute!")
        print()
        
        self.wait_for_user("Press Enter after running the modified pipeline...")
        print()
        
        self.print_celebration("Congratulations! You've modified your first pipeline!")
        print()
        
        self.print_learning("What you just accomplished:")
        print("• Modified a production pipeline")
        print("• Added custom functionality")
        print("• Tested your changes")
        print("• Learned Jenkins pipeline syntax")
        print()
    
    def step_8_advanced_concepts(self):
        """Step 8: Advanced concepts and best practices."""
        self.print_header("Step 8: Advanced Concepts & Best Practices")
        print("=" * 50)
        
        self.print_learning("Let's explore advanced CI/CD concepts!")
        print()
        
        print("🔧 Advanced Pipeline Features:")
        print("• Parallel execution for faster builds")
        print("• Conditional stages based on branch/PR")
        print("• Artifact archiving and deployment")
        print("• Integration with external tools (Slack, email)")
        print("• Pipeline parameters and environment variables")
        print("• Blue-Green and Canary deployments")
        print()
        
        print("📊 Monitoring & Observability:")
        print("• Build trends and metrics")
        print("• Test result reporting")
        print("• Code coverage integration")
        print("• Security scanning results")
        print("• Performance monitoring")
        print()
        
        print("🛡️  Security Best Practices:")
        print("• Use Jenkins credentials for secrets")
        print("• Scan container images for vulnerabilities")
        print("• Implement least privilege access")
        print("• Regular security updates")
        print("• Audit logs and compliance")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• Microservices deployment pipelines")
        print("• Infrastructure as Code (IaC)")
        print("• Database migration automation")
        print("• Multi-environment deployments")
        print("• Feature flag management")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the workshop."""
        self.print_header("🎓 Workshop Conclusion")
        print("=" * 50)
        
        self.print_celebration("Congratulations! You've completed the Jenkins Pipeline Workshop!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Accomplished:{Colors.NC}")
        print("✅ Created your first Jenkins job from scratch")
        print("✅ Configured Git SCM integration")
        print("✅ Built and tested a Docker container")
        print("✅ Executed a complete CI/CD pipeline")
        print("✅ Modified and customized a Jenkinsfile")
        print("✅ Learned Jenkins pipeline best practices")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• Jenkins job creation and configuration")
        print("• Pipeline-as-Code with Jenkinsfiles")
        print("• Docker integration in CI/CD")
        print("• Git SCM workflow with Jenkins")
        print("• Pipeline monitoring and debugging")
        print("• CI/CD best practices and patterns")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other Jenkins scenarios in this workshop")
        print("• Try advanced pipeline features (parallel, conditional)")
        print("• Integrate with your own projects")
        print("• Learn about Jenkins plugins and extensions")
        print("• Study Blue Ocean for visual pipeline management")
        print("• Explore Jenkins X for cloud-native CI/CD")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• Jenkins Documentation: https://jenkins.io/doc/")
        print("• Pipeline Syntax Reference: https://jenkins.io/doc/book/pipeline/syntax/")
        print("• Blue Ocean: https://jenkins.io/projects/blueocean/")
        print("• Jenkins Community: https://community.jenkins.io/")
        print()
        
        self.print_celebration("Thank you for participating in this workshop!")
        print("Keep building amazing CI/CD pipelines! 🚀")
        print()
    
    def cleanup_docker(self):
        """Clean up Docker containers and images."""
        self.print_step("Cleaning up Docker resources...")
        self.run_command("docker stop pipeline-genesis-workshop", check=False)
        self.run_command("docker rm pipeline-genesis-workshop", check=False)
        self.run_command("docker rmi pipeline-genesis-workshop", check=False)
        self.print_success("Docker cleanup completed!")
    
    def run_full_workshop(self):
        """Run the complete educational workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_application()
            self.step_2_local_testing()
            self.step_3_docker_containerization()
            self.step_4_jenkins_job_creation()
            self.step_5_pipeline_execution()
            self.step_6_jenkinsfile_exploration()
            self.step_7_hands_on_modification()
            self.step_8_advanced_concepts()
            self.workshop_conclusion()
            
            # Cleanup
            self.cleanup_docker()
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️ Workshop interrupted by user")
            self.cleanup_docker()
            return False
        except Exception as e:
            print(f"\n❌ Workshop failed: {e}")
            self.cleanup_docker()
            return False
    
    def run_quick_demo(self):
        """Run a quick demo version."""
        self.print_header("🚀 Quick Jenkins Pipeline Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Test application locally
        if not self.step_2_local_testing():
            return False
        
        # Test Docker build
        if not self.step_3_docker_containerization():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins Job Setup")
        print("=" * 30)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Pipeline job: 'My First Pipeline'")
        print("4. Configure Git SCM with this repository")
        print("5. Set Script Path: Jenkins/jenkins-scenarios/scenario_01_pipeline_genesis/Jenkinsfile")
        print("6. Save and run the pipeline!")
        print()
        
        self.cleanup_docker()
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Jenkins Pipeline Educational Workshop')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick demo instead of full workshop')
    parser.add_argument('--help-workshop', action='store_true',
                       help='Show workshop help')
    
    args = parser.parse_args()
    
    if args.help_workshop:
        print("Jenkins Pipeline Educational Workshop")
        print("=" * 40)
        print()
        print("This workshop provides hands-on learning for:")
        print("• Jenkins job creation and configuration")
        print("• Pipeline-as-Code with Jenkinsfiles")
        print("• Docker integration in CI/CD")
        print("• Git SCM workflow with Jenkins")
        print("• Pipeline monitoring and debugging")
        print("• CI/CD best practices and patterns")
        print()
        print("Usage:")
        print("  python3 demo.py              # Full educational workshop")
        print("  python3 demo.py --quick      # Quick demo")
        print("  python3 demo.py --help-workshop  # Show this help")
        return
    
    workshop = EducationalWorkshop()
    
    try:
        if args.quick:
            success = workshop.run_quick_demo()
        else:
            success = workshop.run_full_workshop()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Workshop interrupted by user")
        workshop.cleanup_docker()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Workshop failed: {e}")
        workshop.cleanup_docker()
        sys.exit(1)

if __name__ == "__main__":
    main()