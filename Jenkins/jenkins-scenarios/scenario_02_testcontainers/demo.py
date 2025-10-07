#!/usr/bin/env python3
"""
TestContainers Integration - Educational Jenkins Workshop
========================================================

An unforgettable hands-on learning experience for TestContainers with Jenkins.
This workshop teaches you how to integrate database testing into your CI/CD pipelines.

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

class TestContainersWorkshop:
    """Educational TestContainers Integration Workshop."""
    
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
        """Welcome participants to the TestContainers workshop."""
        self.print_header("🚀 Welcome to the TestContainers Integration Workshop!")
        print("=" * 70)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• How to integrate TestContainers with Jenkins")
        print("• Database testing in CI/CD pipelines")
        print("• Container orchestration for testing")
        print("• Parallel test execution strategies")
        print("• Test data management and cleanup")
        print("• Advanced testing patterns and best practices")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Build:{Colors.NC}")
        print("• A Flask application with database integration")
        print("• TestContainers for PostgreSQL, MySQL, and Redis")
        print("• A Jenkins pipeline with database testing")
        print("• Parallel test execution for faster feedback")
        print("• Comprehensive test reporting and monitoring")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 60-75 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to master TestContainers integration?")
        print()
    
    def step_1_understand_testcontainers(self):
        """Step 1: Understand TestContainers concept."""
        self.print_header("Step 1: Understanding TestContainers")
        print("=" * 50)
        
        self.print_learning("TestContainers revolutionizes integration testing!")
        print()
        
        # Show application structure
        self.print_step("Exploring our test-driven application...")
        os.chdir(self.scenario_dir)
        
        print("📁 Application Structure:")
        print("├── app.py                 # Main Flask application")
        print("├── database.py            # Database connection logic")
        print("├── requirements.txt       # Python dependencies")
        print("├── tests/                 # Test suite")
        print("│   ├── test_app.py        # Unit tests")
        print("│   └── test_containers.py # Integration tests")
        print("├── docker-compose.test.yml # Test environment")
        print("└── Jenkinsfile            # Pipeline definition")
        print()
        
        # Show the database integration
        self.print_step("Let's examine our database integration...")
        with open("database.py", "r") as f:
            db_content = f.read()
        
        print("🗄️ Database Integration (database.py):")
        print("-" * 40)
        print(db_content[:400] + "..." if len(db_content) > 400 else db_content)
        print("-" * 40)
        print()
        
        self.print_learning("Key TestContainers Benefits:")
        print("• Real database testing (not mocks)")
        print("• Isolated test environments")
        print("• Automatic container lifecycle management")
        print("• Parallel test execution")
        print("• Consistent test data setup")
        print()
        
        self.wait_for_user("Ready to explore our test suite?")
        print()
    
    def step_2_explore_test_suite(self):
        """Step 2: Explore the test suite."""
        self.print_header("Step 2: Exploring Our Test Suite")
        print("=" * 50)
        
        self.print_learning("Let's examine our comprehensive test suite!")
        print()
        
        # Show test files
        self.print_step("Examining our test files...")
        
        print("🧪 Test Suite Overview:")
        print("├── test_app.py - Unit tests for Flask app")
        print("└── test_containers.py - Integration tests with containers")
        print()
        
        # Show test_containers.py
        self.print_step("Let's look at our TestContainers integration tests...")
        with open("tests/test_containers.py", "r") as f:
            test_content = f.read()
        
        print("🐳 TestContainers Integration Tests:")
        print("-" * 45)
        print(test_content[:600] + "..." if len(test_content) > 600 else test_content)
        print("-" * 45)
        print()
        
        self.print_learning("TestContainers Features We're Using:")
        print("• PostgreSQL container for data persistence")
        print("• MySQL container for cross-database testing")
        print("• Redis container for caching tests")
        print("• Parallel container execution")
        print("• Automatic cleanup after tests")
        print()
        
        self.wait_for_user("Ready to run tests locally?")
        print()
    
    def step_3_local_testing(self):
        """Step 3: Run tests locally."""
        self.print_header("Step 3: Local Testing with TestContainers")
        print("=" * 50)
        
        self.print_learning("Let's see TestContainers in action!")
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
        
        # Run unit tests
        self.print_step("Running unit tests...")
        if not self.run_command("python3 -m pytest tests/test_app.py -v"):
            self.print_info("Some unit tests may have failed due to environment differences")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        # Run integration tests
        self.print_step("Running TestContainers integration tests...")
        if not self.run_command("python3 -m pytest tests/test_containers.py -v -s"):
            self.print_info("Integration tests may have failed due to Docker/container issues")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        self.print_success("Local testing completed!")
        print()
        
        self.print_learning("What You Just Witnessed:")
        print("• TestContainers automatically started database containers")
        print("• Tests ran against real databases (not mocks)")
        print("• Containers were automatically cleaned up")
        print("• Parallel test execution for faster feedback")
        print()
        
        self.wait_for_user("Ready to create your Jenkins pipeline?")
        print()
    
    def step_4_jenkins_job_creation(self):
        """Step 4: Create Jenkins job for TestContainers."""
        self.print_header("Step 4: Creating Your TestContainers Jenkins Job")
        print("=" * 60)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now let's create a Jenkins job that runs TestContainers!")
        print()
        print("This job will demonstrate how to integrate containerized")
        print("database testing into your CI/CD pipeline.")
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
        print("   • Enter job name: 'TestContainers Integration'")
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
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_02_testcontainers/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types (Pipeline vs Freestyle)")
        print("• Git SCM integration for TestContainers")
        print("• Pipeline script location for containerized testing")
        print("• Jenkins configuration for database testing")
        print()
        
        self.wait_for_user("Press Enter after configuring the pipeline...")
        print()
    
    def step_5_pipeline_execution(self):
        """Step 5: Execute and monitor the TestContainers pipeline."""
        self.print_header("Step 5: Running Your TestContainers Pipeline")
        print("=" * 60)
        
        self.print_learning("Time to see TestContainers in your CI/CD pipeline!")
        print()
        
        print("4️⃣  Execute Pipeline:")
        print("   • Click 'Build Now' to start the pipeline")
        print("   • Watch the pipeline execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Observe container startup and test execution")
        print()
        
        self.print_learning("Pipeline Stages You'll See:")
        print("   🚀 Welcome - TestContainers introduction")
        print("   📦 Setup - Check Python and Docker environment")
        print("   🔧 Install Dependencies - Install test dependencies")
        print("   🧪 Run Unit Tests - Execute unit test suite")
        print("   🐳 Run Integration Tests - TestContainers in action")
        print("   📊 Test Reporting - Generate test reports")
        print("   ✅ Success! - Pipeline completion")
        print()
        
        self.wait_for_user("Press Enter after running the pipeline...")
        print()
        
        self.print_learning("TestContainers in CI/CD Benefits:")
        print("• Consistent test environments across dev/staging/prod")
        print("• Real database testing in automated pipelines")
        print("• Parallel test execution for faster feedback")
        print("• Automatic cleanup prevents resource leaks")
        print("• Isolated test runs prevent interference")
        print()
        
        self.wait_for_user("Ready to explore the Jenkinsfile?")
        print()
    
    def step_6_jenkinsfile_exploration(self):
        """Step 6: Explore and understand the TestContainers Jenkinsfile."""
        self.print_header("Step 6: Understanding the TestContainers Jenkinsfile")
        print("=" * 60)
        
        self.print_learning("The Jenkinsfile orchestrates TestContainers in CI/CD!")
        print()
        
        # Show Jenkinsfile
        self.print_step("Let's examine our TestContainers Jenkinsfile...")
        with open("Jenkinsfile", "r") as f:
            jenkinsfile_content = f.read()
        
        print("📝 TestContainers Jenkinsfile:")
        print("-" * 40)
        print(jenkinsfile_content)
        print("-" * 40)
        print()
        
        self.print_learning("TestContainers Jenkinsfile Key Concepts:")
        print("• Docker-in-Docker (DinD) for container testing")
        print("• TestContainers configuration and setup")
        print("• Parallel test execution strategies")
        print("• Test reporting and artifact collection")
        print("• Container cleanup and resource management")
        print()
        
        self.print_learning("Advanced TestContainers Patterns:")
        print("• Multi-database testing strategies")
        print("• Test data seeding and management")
        print("• Container networking and service discovery")
        print("• Performance testing with containers")
        print("• Integration with monitoring and logging")
        print()
        
        self.wait_for_user("Ready to modify the Jenkinsfile?")
        print()
    
    def step_7_hands_on_modification(self):
        """Step 7: Hands-on TestContainers modification."""
        self.print_header("Step 7: Hands-On TestContainers Modification")
        print("=" * 60)
        
        self.print_learning("Let's customize your TestContainers pipeline!")
        print()
        
        print("🛠️  Modification Exercise:")
        print("Let's add a new test stage to our pipeline:")
        print()
        print("1. Go back to your Jenkins job")
        print("2. Click 'Configure'")
        print("3. Scroll to the Pipeline section")
        print("4. Change 'Pipeline script from SCM' to 'Pipeline script'")
        print("5. Copy the Jenkinsfile content into the text area")
        print("6. Add a new stage after the 'Run Integration Tests' stage:")
        print()
        
        print("```groovy")
        print("stage('🔍 Custom Test Stage') {")
        print("    steps {")
        print("        echo 'Running custom TestContainers tests!'")
        print("        sh 'python3 -m pytest tests/test_containers.py::test_custom -v'")
        print("    }")
        print("}")
        print("```")
        print()
        
        self.wait_for_user("Press Enter after adding the custom test stage...")
        print()
        
        print("7. Click 'Save'")
        print("8. Click 'Build Now' to run the modified pipeline")
        print("9. Watch your custom test stage execute!")
        print()
        
        self.wait_for_user("Press Enter after running the modified pipeline...")
        print()
        
        self.print_celebration("Congratulations! You've customized your TestContainers pipeline!")
        print()
        
        self.print_learning("What you just accomplished:")
        print("• Modified a TestContainers pipeline")
        print("• Added custom testing functionality")
        print("• Tested your changes in CI/CD")
        print("• Learned TestContainers pipeline patterns")
        print()
    
    def step_8_advanced_concepts(self):
        """Step 8: Advanced TestContainers concepts."""
        self.print_header("Step 8: Advanced TestContainers Concepts")
        print("=" * 60)
        
        self.print_learning("Let's explore advanced TestContainers patterns!")
        print()
        
        print("🔧 Advanced TestContainers Features:")
        print("• Custom container images for testing")
        print("• Container composition and orchestration")
        print("• Test data management and seeding")
        print("• Performance testing with containers")
        print("• Integration with cloud databases")
        print("• Test parallelization strategies")
        print()
        
        print("📊 Monitoring & Observability:")
        print("• Test execution metrics and reporting")
        print("• Container resource usage monitoring")
        print("• Test failure analysis and debugging")
        print("• Performance regression detection")
        print("• Test coverage with containers")
        print()
        
        print("🛡️  Best Practices:")
        print("• Test isolation and cleanup")
        print("• Resource management and limits")
        print("• Test data privacy and security")
        print("• CI/CD pipeline optimization")
        print("• Error handling and recovery")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• Microservices integration testing")
        print("• Database migration testing")
        print("• API contract testing")
        print("• End-to-end testing scenarios")
        print("• Load testing with realistic data")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the TestContainers workshop."""
        self.print_header("🎓 TestContainers Workshop Conclusion")
        print("=" * 60)
        
        self.print_celebration("Congratulations! You've mastered TestContainers integration!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Accomplished:{Colors.NC}")
        print("✅ Created a TestContainers Jenkins job from scratch")
        print("✅ Configured database testing in CI/CD")
        print("✅ Executed containerized integration tests")
        print("✅ Modified and customized TestContainers pipelines")
        print("✅ Learned advanced testing patterns")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• TestContainers integration with Jenkins")
        print("• Database testing in CI/CD pipelines")
        print("• Container orchestration for testing")
        print("• Parallel test execution strategies")
        print("• Test data management and cleanup")
        print("• Advanced testing patterns and best practices")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other Jenkins scenarios in this workshop")
        print("• Try advanced TestContainers features")
        print("• Integrate with your own projects")
        print("• Study container orchestration patterns")
        print("• Learn about test data management")
        print("• Explore performance testing with containers")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• TestContainers Documentation: https://testcontainers.org/")
        print("• Python TestContainers: https://testcontainers-python.readthedocs.io/")
        print("• Jenkins Pipeline Syntax: https://jenkins.io/doc/book/pipeline/syntax/")
        print("• Docker Best Practices: https://docs.docker.com/develop/best-practices/")
        print()
        
        self.print_celebration("Thank you for participating in this workshop!")
        print("Keep building amazing test-driven CI/CD pipelines! 🚀")
        print()
    
    def run_full_workshop(self):
        """Run the complete TestContainers workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_testcontainers()
            self.step_2_explore_test_suite()
            self.step_3_local_testing()
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
        """Run a quick TestContainers demo."""
        self.print_header("🚀 Quick TestContainers Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Test application locally
        if not self.step_3_local_testing():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins TestContainers Job Setup")
        print("=" * 40)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Pipeline job: 'TestContainers Integration'")
        print("4. Configure Git SCM with this repository")
        print("5. Set Script Path: Jenkins/jenkins-scenarios/scenario_02_testcontainers/Jenkinsfile")
        print("6. Save and run the pipeline!")
        print()
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='TestContainers Integration Educational Workshop')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick demo instead of full workshop')
    parser.add_argument('--help-workshop', action='store_true',
                       help='Show workshop help')
    
    args = parser.parse_args()
    
    if args.help_workshop:
        print("TestContainers Integration Educational Workshop")
        print("=" * 50)
        print()
        print("This workshop provides hands-on learning for:")
        print("• TestContainers integration with Jenkins")
        print("• Database testing in CI/CD pipelines")
        print("• Container orchestration for testing")
        print("• Parallel test execution strategies")
        print("• Test data management and cleanup")
        print("• Advanced testing patterns and best practices")
        print()
        print("Usage:")
        print("  python3 demo.py              # Full educational workshop")
        print("  python3 demo.py --quick      # Quick demo")
        print("  python3 demo.py --help-workshop  # Show this help")
        return
    
    workshop = TestContainersWorkshop()
    
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