#!/usr/bin/env python3
"""
Test Master - Educational Jenkins Workshop
=========================================

An unforgettable hands-on learning experience for advanced testing with Jenkins.
This workshop teaches you how to become a test master in your CI/CD pipelines!

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

class TestMasterWorkshop:
    """Educational Test Master Workshop."""
    
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
        """Welcome participants to the Test Master workshop."""
        self.print_header("🧪 Welcome to the Test Master Workshop!")
        print("=" * 60)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• Advanced testing strategies with Jenkins")
        print("• Test automation in CI/CD pipelines")
        print("• Test reporting and analytics")
        print("• Test data management")
        print("• Performance testing integration")
        print("• Test orchestration and parallelization")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Master:{Colors.NC}")
        print("• A Flask application with comprehensive testing")
        print("• Multi-database testing with TestContainers")
        print("• Parallel test execution strategies")
        print("• Test reporting and visualization")
        print("• Production-ready testing workflows")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 90-105 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to become a test master?")
        print()
    
    def step_1_understand_testing_strategies(self):
        """Step 1: Understand advanced testing strategies."""
        self.print_header("Step 1: Understanding Advanced Testing Strategies")
        print("=" * 60)
        
        self.print_learning("Let's explore the art of test mastery!")
        print()
        
        # Show application structure
        self.print_step("Exploring our test-driven application...")
        os.chdir(self.scenario_dir)
        
        print("📁 Test Master Application Structure:")
        print("├── app.py                 # Main Flask application")
        print("├── database.py            # Database connection logic")
        print("├── requirements.txt       # Python dependencies")
        print("├── tests/                 # Comprehensive test suite")
        print("│   ├── test_app.py        # Unit tests")
        print("│   └── test_containers.py # Integration tests")
        print("└── Jenkinsfile            # Test automation pipeline")
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
        
        self.print_learning("Test Master Techniques We'll Master:")
        print("• Unit testing with pytest")
        print("• Integration testing with TestContainers")
        print("• Parallel test execution")
        print("• Test data management")
        print("• Test reporting and analytics")
        print()
        
        self.wait_for_user("Ready to explore our test suite?")
        print()
    
    def step_2_explore_test_suite(self):
        """Step 2: Explore the comprehensive test suite."""
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
        
        self.print_learning("Test Master Features We're Using:")
        print("• PostgreSQL container for data persistence")
        print("• MySQL container for cross-database testing")
        print("• Redis container for caching tests")
        print("• Parallel container execution")
        print("• Comprehensive test coverage")
        print()
        
        self.wait_for_user("Ready to run tests locally?")
        print()
    
    def step_3_local_testing(self):
        """Step 3: Run tests locally."""
        self.print_header("Step 3: Local Testing & Test Mastery")
        print("=" * 50)
        
        self.print_learning("Let's see test mastery in action!")
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
        
        self.print_learning("Test Master Skills Demonstrated:")
        print("• Comprehensive test coverage")
        print("• TestContainers integration")
        print("• Parallel test execution")
        print("• Test data management")
        print("• Local development workflows")
        print()
        
        self.wait_for_user("Ready to create your Test Master Jenkins pipeline?")
        print()
    
    def step_4_jenkins_job_creation(self):
        """Step 4: Create Jenkins job for Test Master."""
        self.print_header("Step 4: Creating Your Test Master Jenkins Job")
        print("=" * 60)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now let's create a Jenkins job that masters testing!")
        print()
        print("This job will demonstrate advanced testing strategies")
        print("and test automation in CI/CD pipelines.")
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
        print("   • Enter job name: 'Test Master Automation'")
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
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_02_test_master/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types for test automation")
        print("• Git SCM integration for testing workflows")
        print("• Pipeline script location for test mastery")
        print("• Jenkins configuration for advanced testing")
        print()
        
        self.wait_for_user("Press Enter after configuring the pipeline...")
        print()
    
    def step_5_pipeline_execution(self):
        """Step 5: Execute and monitor the Test Master pipeline."""
        self.print_header("Step 5: Running Your Test Master Pipeline")
        print("=" * 60)
        
        self.print_learning("Time to see test mastery in action!")
        print()
        
        print("4️⃣  Execute Pipeline:")
        print("   • Click 'Build Now' to start the pipeline")
        print("   • Watch the pipeline execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Observe test execution and reporting")
        print()
        
        self.print_learning("Pipeline Stages You'll See:")
        print("   🧪 Welcome - Test Master introduction")
        print("   📦 Setup - Check Python and Docker environment")
        print("   🔧 Install Dependencies - Install test dependencies")
        print("   🧪 Run Unit Tests - Execute unit test suite")
        print("   🐳 Run Integration Tests - TestContainers in action")
        print("   📊 Test Reporting - Generate test reports")
        print("   ✅ Success! - Pipeline completion")
        print()
        
        self.wait_for_user("Press Enter after running the pipeline...")
        print()
        
        self.print_learning("Test Master CI/CD Benefits:")
        print("• Automated test execution")
        print("• Comprehensive test coverage")
        print("• Parallel test execution")
        print("• Test reporting and analytics")
        print("• Production-ready testing workflows")
        print()
        
        self.wait_for_user("Ready to explore the Jenkinsfile?")
        print()
    
    def step_6_jenkinsfile_exploration(self):
        """Step 6: Explore and understand the Test Master Jenkinsfile."""
        self.print_header("Step 6: Understanding the Test Master Jenkinsfile")
        print("=" * 60)
        
        self.print_learning("The Jenkinsfile orchestrates test mastery!")
        print()
        
        # Show Jenkinsfile
        self.print_step("Let's examine our Test Master Jenkinsfile...")
        with open("Jenkinsfile", "r") as f:
            jenkinsfile_content = f.read()
        
        print("📝 Test Master Jenkinsfile:")
        print("-" * 35)
        print(jenkinsfile_content)
        print("-" * 35)
        print()
        
        self.print_learning("Test Master Jenkinsfile Key Concepts:")
        print("• Test automation orchestration")
        print("• TestContainers integration")
        print("• Parallel test execution")
        print("• Test reporting and analytics")
        print("• Test data management")
        print()
        
        self.print_learning("Advanced Testing Patterns:")
        print("• Test parallelization strategies")
        print("• Test data seeding and cleanup")
        print("• Test reporting and visualization")
        print("• Test performance optimization")
        print("• Test failure analysis")
        print()
        
        self.wait_for_user("Ready to modify the Jenkinsfile?")
        print()
    
    def step_7_hands_on_modification(self):
        """Step 7: Hands-on Test Master modification."""
        self.print_header("Step 7: Hands-On Test Master Modification")
        print("=" * 60)
        
        self.print_learning("Let's customize your Test Master pipeline!")
        print()
        
        print("🛠️  Modification Exercise:")
        print("Let's add a new test analytics stage:")
        print()
        print("1. Go back to your Jenkins job")
        print("2. Click 'Configure'")
        print("3. Scroll to the Pipeline section")
        print("4. Change 'Pipeline script from SCM' to 'Pipeline script'")
        print("5. Copy the Jenkinsfile content into the text area")
        print("6. Add a new stage after the 'Test Reporting' stage:")
        print()
        
        print("```groovy")
        print("stage('📊 Test Analytics') {")
        print("    steps {")
        print("        echo 'Analyzing test results!'")
        print("        sh 'echo \"Test coverage: 95%\"'")
        print("        sh 'echo \"Test execution time: 2.5 minutes\"'")
        print("    }")
        print("}")
        print("```")
        print()
        
        self.wait_for_user("Press Enter after adding the analytics stage...")
        print()
        
        print("7. Click 'Save'")
        print("8. Click 'Build Now' to run the modified pipeline")
        print("9. Watch your test analytics stage execute!")
        print()
        
        self.wait_for_user("Press Enter after running the modified pipeline...")
        print()
        
        self.print_celebration("Congratulations! You've customized your Test Master pipeline!")
        print()
        
        self.print_learning("What you just accomplished:")
        print("• Modified a Test Master pipeline")
        print("• Added custom test analytics")
        print("• Tested your changes in CI/CD")
        print("• Learned advanced testing patterns")
        print()
    
    def step_8_advanced_concepts(self):
        """Step 8: Advanced testing concepts and best practices."""
        self.print_header("Step 8: Advanced Testing Concepts & Best Practices")
        print("=" * 60)
        
        self.print_learning("Let's explore advanced testing mastery!")
        print()
        
        print("🔧 Advanced Testing Features:")
        print("• Test parallelization and optimization")
        print("• Test data management and seeding")
        print("• Test reporting and visualization")
        print("• Performance testing integration")
        print("• Test failure analysis and debugging")
        print("• Test automation frameworks")
        print()
        
        print("📊 Test Analytics & Reporting:")
        print("• Test coverage analysis")
        print("• Test execution metrics")
        print("• Test failure trends")
        print("• Test performance monitoring")
        print("• Test quality gates")
        print()
        
        print("🛡️ Testing Best Practices:")
        print("• Test-driven development (TDD)")
        print("• Behavior-driven development (BDD)")
        print("• Test automation strategies")
        print("• Test maintenance and refactoring")
        print("• Continuous testing practices")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• Microservices testing")
        print("• API testing automation")
        print("• End-to-end testing")
        print("• Performance testing")
        print("• Test orchestration")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the Test Master workshop."""
        self.print_header("🎓 Test Master Workshop Conclusion")
        print("=" * 60)
        
        self.print_celebration("Congratulations! You've become a Test Master!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Mastered:{Colors.NC}")
        print("✅ Created a Test Master Jenkins job from scratch")
        print("✅ Configured advanced testing strategies in CI/CD")
        print("✅ Executed comprehensive test automation")
        print("✅ Modified and customized testing workflows")
        print("✅ Learned advanced testing patterns")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• Advanced testing strategies with Jenkins")
        print("• Test automation in CI/CD pipelines")
        print("• Test reporting and analytics")
        print("• Test data management")
        print("• Performance testing integration")
        print("• Test orchestration and parallelization")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other Jenkins scenarios in this workshop")
        print("• Try advanced testing frameworks")
        print("• Integrate with your own projects")
        print("• Study test automation patterns")
        print("• Learn about performance testing")
        print("• Explore test orchestration tools")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• pytest Documentation: https://docs.pytest.org/")
        print("• TestContainers: https://testcontainers.org/")
        print("• Jenkins Testing Plugin: https://plugins.jenkins.io/junit/")
        print("• Test Automation Best Practices: https://testautomationu.applitools.com/")
        print()
        
        self.print_celebration("Thank you for participating in this workshop!")
        print("Keep mastering tests like a true test master! 🧪")
        print()
    
    def run_full_workshop(self):
        """Run the complete Test Master workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_testing_strategies()
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
        """Run a quick Test Master demo."""
        self.print_header("🚀 Quick Test Master Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Test application locally
        if not self.step_3_local_testing():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins Test Master Job Setup")
        print("=" * 40)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Pipeline job: 'Test Master Automation'")
        print("4. Configure Git SCM with this repository")
        print("5. Set Script Path: Jenkins/jenkins-scenarios/scenario_02_test_master/Jenkinsfile")
        print("6. Save and run the pipeline!")
        print()
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Test Master Educational Workshop')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick demo instead of full workshop')
    parser.add_argument('--help-workshop', action='store_true',
                       help='Show workshop help')
    
    args = parser.parse_args()
    
    if args.help_workshop:
        print("Test Master Educational Workshop")
        print("=" * 40)
        print()
        print("This workshop provides hands-on learning for:")
        print("• Advanced testing strategies with Jenkins")
        print("• Test automation in CI/CD pipelines")
        print("• Test reporting and analytics")
        print("• Test data management")
        print("• Performance testing integration")
        print("• Test orchestration and parallelization")
        print()
        print("Usage:")
        print("  python3 demo.py              # Full educational workshop")
        print("  python3 demo.py --quick      # Quick demo")
        print("  python3 demo.py --help-workshop  # Show this help")
        return
    
    workshop = TestMasterWorkshop()
    
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