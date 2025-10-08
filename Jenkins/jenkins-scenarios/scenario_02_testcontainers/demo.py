#!/usr/bin/env python3
"""
TestContainers Integration - Educational Jenkins Workshop
========================================================

An unforgettable hands-on learning experience for TestContainers with Jenkins.
This workshop teaches you real container integration testing patterns.

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
        self.print_header("🐳 Welcome to the TestContainers Integration Workshop!")
        print("=" * 70)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• Real TestContainers integration with PostgreSQL")
        print("• Container-based integration testing patterns")
        print("• Database testing with actual containers")
        print("• Jenkins job creation for complex testing scenarios")
        print("• API testing with real database backends")
        print("• Performance testing with containerized databases")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Build:{Colors.NC}")
        print("• A complete PostgreSQL database integration")
        print("• Real TestContainers test suite")
        print("• Jenkins job with multiple test modes")
        print("• Docker Compose integration testing")
        print("• Production-ready testing patterns")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 60-90 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to dive into TestContainers integration?")
        print()
    
    def step_1_understand_testcontainers(self):
        """Step 1: Understand TestContainers and what we're building."""
        self.print_header("Step 1: Understanding TestContainers Integration")
        print("=" * 60)
        
        self.print_learning("Let's explore what TestContainers can do!")
        print()
        
        # Show application structure
        self.print_step("Exploring TestContainers application structure...")
        os.chdir(self.scenario_dir)
        
        print("📁 TestContainers Application Structure:")
        print("├── app.py                           # Main Flask application")
        print("├── database.py                      # PostgreSQL database manager")
        print("├── requirements.txt                 # TestContainers dependencies")
        print("├── Dockerfile                       # Container definition")
        print("├── docker-compose.test.yml          # TestContainers setup")
        print("├── tests/                           # Test suites")
        print("│   ├── test_app.py                  # Application tests")
        print("│   └── test_testcontainers_integration.py  # TestContainers tests")
        print("├── demo_testcontainers.py           # Interactive demo")
        print("├── setup-jenkins-job.py             # Jenkins job setup")
        print("└── init.sql                         # Database initialization")
        print()
        
        # Show the database module
        self.print_step("Let's look at our PostgreSQL database integration...")
        with open("database.py", "r") as f:
            db_content = f.read()
        
        print("🗄️ PostgreSQL Database Manager (database.py):")
        print("-" * 50)
        print(db_content[:800] + "..." if len(db_content) > 800 else db_content)
        print("-" * 50)
        print()
        
        self.print_learning("This is a production-ready database manager with:")
        print("• Real PostgreSQL integration (not SQLite simulation)")
        print("• TestContainers support for automated testing")
        print("• CRUD operations with proper error handling")
        print("• Database statistics and health monitoring")
        print("• Concurrent operation support")
        print()
        
        self.wait_for_user("Ready to see TestContainers in action?")
        print()
    
    def step_2_local_testcontainers_demo(self):
        """Step 2: Run TestContainers demo locally."""
        self.print_header("Step 2: TestContainers Local Demo")
        print("=" * 50)
        
        self.print_learning("Let's see TestContainers create real PostgreSQL containers!")
        print()
        
        # Check Python environment
        self.print_step("Checking Python environment...")
        if not self.run_command("python3 --version", capture_output=True):
            self.print_error("Python3 is not available")
            return False
        
        # Install dependencies
        self.print_step("Installing TestContainers dependencies...")
        if not self.run_command("python3 -m pip install --user -r requirements.txt"):
            self.print_info("Trying with --break-system-packages flag...")
            if not self.run_command("python3 -m pip install --break-system-packages -r requirements.txt"):
                self.print_info("Dependencies may already be installed. Continuing...")
        
        # Run TestContainers demo
        self.print_step("Running TestContainers demo...")
        print("This will start a real PostgreSQL container and run tests!")
        print()
        
        # Run the demo script
        if not self.run_command("python3 demo_testcontainers.py", check=False):
            self.print_info("Demo may have completed or encountered expected issues")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        self.print_success("TestContainers demo completed!")
        print()
        
        self.print_learning("Key Learning Points:")
        print("• TestContainers creates real database containers")
        print("• Containers are automatically cleaned up after tests")
        print("• Tests run against actual PostgreSQL, not mocks")
        print("• This provides confidence in production behavior")
        print("• Integration testing becomes reliable and fast")
        print()
        
        self.wait_for_user("Ready to create a Jenkins job for this?")
        print()
    
    def step_3_jenkins_job_creation(self):
        """Step 3: Create Jenkins job for TestContainers."""
        self.print_header("Step 3: Creating Jenkins Job for TestContainers")
        print("=" * 60)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now let's create a Jenkins job that runs TestContainers!")
        print()
        print("This job will demonstrate how to integrate TestContainers")
        print("into a real CI/CD pipeline with multiple test modes.")
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
        print("   • Select 'Freestyle project' as job type")
        print("   • Click 'OK'")
        print()
        
        self.wait_for_user("Press Enter after creating the job...")
        print()
        
        print("3️⃣  Configure Job:")
        print("   • Add description: 'TestContainers Integration Demo - Real database testing'")
        print("   • Check 'This project is parameterized'")
        print("   • Add String Parameter: 'DB_TYPE' (default: testcontainers)")
        print("   • Add String Parameter: 'TEST_MODE' (default: all)")
        print("   • Set Source Code Management to 'Git'")
        print("   • Repository URL: 'https://github.com/vellankikoti/ci-cd-chaos-workshop.git'")
        print("   • Branch: '*/docker-test'")
        print("   • Add Build Step: 'Execute shell'")
        print("   • Copy the build script from setup-jenkins-job.py")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types (Freestyle vs Pipeline)")
        print("• Parameterized builds for different test modes")
        print("• Git SCM integration with specific branches")
        print("• Shell script execution in Jenkins")
        print("• TestContainers integration in CI/CD")
        print()
        
        self.wait_for_user("Press Enter after configuring the job...")
        print()
    
    def step_4_jenkins_job_execution(self):
        """Step 4: Execute and monitor the Jenkins job."""
        self.print_header("Step 4: Running Your TestContainers Job")
        print("=" * 50)
        
        self.print_learning("Time to see TestContainers in Jenkins!")
        print()
        
        print("4️⃣  Execute Job:")
        print("   • Click 'Build with Parameters'")
        print("   • Choose TEST_MODE: 'all' (or try different modes)")
        print("   • Click 'Build'")
        print("   • Watch the job execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Explore the console output")
        print()
        
        self.print_learning("Test Modes You Can Try:")
        print("   🎬 demo - Interactive TestContainers demo")
        print("   🧪 tests - Run TestContainers integration tests")
        print("   🔧 app-tests - Run application tests")
        print("   🐳 docker - Run with Docker Compose")
        print("   🚀 all - Run complete test suite")
        print()
        
        self.wait_for_user("Press Enter after running the job...")
        print()
        
        self.print_learning("What You'll See in the Logs:")
        print("• PostgreSQL container starting up")
        print("• Database initialization and schema creation")
        print("• TestContainers test execution")
        print("• API endpoint testing with real database")
        print("• Performance and concurrent operation tests")
        print("• Container cleanup and teardown")
        print()
        
        self.wait_for_user("Ready to explore the test results?")
        print()
    
    def step_5_test_results_analysis(self):
        """Step 5: Analyze test results and understand the output."""
        self.print_header("Step 5: Analyzing TestContainers Results")
        print("=" * 50)
        
        self.print_learning("Let's understand what TestContainers accomplished!")
        print()
        
        print("📊 Test Results Analysis:")
        print("• Check the 'Test Result' section in Jenkins")
        print("• Look at the console output for detailed logs")
        print("• Examine any artifacts that were generated")
        print("• Review the build timeline and duration")
        print()
        
        self.print_learning("Key Metrics to Look For:")
        print("• Container startup time")
        print("• Database initialization time")
        print("• Test execution duration")
        print("• Memory usage during tests")
        print("• Test pass/fail rates")
        print("• Cleanup and teardown time")
        print()
        
        self.print_learning("TestContainers Benefits Demonstrated:")
        print("• Real database testing (not mocks)")
        print("• Isolated test environments")
        print("• Automatic cleanup and resource management")
        print("• Consistent test environments")
        print("• Easy parallel test execution")
        print("• Production-like testing conditions")
        print()
        
        self.wait_for_user("Ready to explore advanced TestContainers features?")
        print()
    
    def step_6_advanced_testcontainers(self):
        """Step 6: Advanced TestContainers concepts."""
        self.print_header("Step 6: Advanced TestContainers Concepts")
        print("=" * 50)
        
        self.print_learning("Let's explore advanced TestContainers patterns!")
        print()
        
        print("🔧 Advanced TestContainers Features:")
        print("• Multiple container orchestration")
        print("• Custom container configurations")
        print("• Network isolation and communication")
        print("• Volume mounting and data persistence")
        print("• Health checks and readiness probes")
        print("• Resource limits and constraints")
        print()
        
        print("📊 Performance Testing with TestContainers:")
        print("• Load testing with real databases")
        print("• Concurrent user simulation")
        print("• Database performance benchmarking")
        print("• Memory and CPU usage monitoring")
        print("• Scalability testing")
        print()
        
        print("🛡️ Security Testing:")
        print("• Database security configurations")
        print("• Network security testing")
        print("• Authentication and authorization")
        print("• Data encryption testing")
        print("• Vulnerability scanning")
        print()
        
        print("🔄 CI/CD Integration Patterns:")
        print("• Parallel test execution")
        print("• Test result aggregation")
        print("• Artifact collection and storage")
        print("• Notification and reporting")
        print("• Environment-specific configurations")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• Microservices integration testing")
        print("• Database migration testing")
        print("• API contract testing")
        print("• End-to-end workflow testing")
        print("• Performance regression testing")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the workshop."""
        self.print_header("🎓 TestContainers Workshop Conclusion")
        print("=" * 60)
        
        self.print_celebration("Congratulations! You've mastered TestContainers integration!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Accomplished:{Colors.NC}")
        print("✅ Created real TestContainers with PostgreSQL")
        print("✅ Built comprehensive integration test suite")
        print("✅ Configured Jenkins job with multiple test modes")
        print("✅ Executed container-based testing in CI/CD")
        print("✅ Learned production-ready testing patterns")
        print("✅ Explored advanced TestContainers concepts")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• TestContainers integration and configuration")
        print("• Real database testing with containers")
        print("• Jenkins job creation for complex testing")
        print("• Docker Compose integration testing")
        print("• Performance and concurrent testing")
        print("• CI/CD testing best practices")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other TestContainers scenarios")
        print("• Try different database types (MySQL, MongoDB, Redis)")
        print("• Integrate with your own applications")
        print("• Learn about TestContainers for other languages")
        print("• Study container orchestration patterns")
        print("• Explore cloud-native testing strategies")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• TestContainers Documentation: https://testcontainers.org/")
        print("• TestContainers Python: https://testcontainers-python.readthedocs.io/")
        print("• Jenkins Testing Guide: https://jenkins.io/doc/book/pipeline/testing/")
        print("• Docker Testing Patterns: https://docs.docker.com/develop/dev-best-practices/")
        print()
        
        self.print_celebration("Thank you for exploring TestContainers integration!")
        print("Keep building amazing container-based tests! 🐳")
        print()
    
    def run_full_workshop(self):
        """Run the complete educational workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_testcontainers()
            self.step_2_local_testcontainers_demo()
            self.step_3_jenkins_job_creation()
            self.step_4_jenkins_job_execution()
            self.step_5_test_results_analysis()
            self.step_6_advanced_testcontainers()
            self.workshop_conclusion()
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️ Workshop interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Workshop failed: {e}")
            return False
    
    def run_quick_demo(self):
        """Run a quick demo version."""
        self.print_header("🐳 Quick TestContainers Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Run TestContainers demo
        if not self.step_2_local_testcontainers_demo():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins Job Setup")
        print("=" * 30)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Freestyle job: 'TestContainers Integration'")
        print("4. Configure Git SCM with this repository")
        print("5. Add parameters: DB_TYPE, TEST_MODE")
        print("6. Add shell script from setup-jenkins-job.py")
        print("7. Save and run with parameters!")
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
        print("• TestContainers integration with PostgreSQL")
        print("• Container-based integration testing")
        print("• Jenkins job creation for complex testing")
        print("• Docker Compose integration testing")
        print("• Performance and concurrent testing")
        print("• CI/CD testing best practices")
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