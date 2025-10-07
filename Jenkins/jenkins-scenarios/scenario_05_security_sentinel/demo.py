#!/usr/bin/env python3
"""
Security Sentinel - Educational Jenkins Workshop
==============================================

An unforgettable hands-on learning experience for security scanning with Jenkins.
This workshop teaches you how to become a security sentinel in your CI/CD pipelines!

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

class SecuritySentinelWorkshop:
    """Educational Security Sentinel Workshop."""
    
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
        """Welcome participants to the Security Sentinel workshop."""
        self.print_header("🛡️ Welcome to the Security Sentinel Workshop!")
        print("=" * 60)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• Security scanning integration with Jenkins")
        print("• Vulnerability assessment in CI/CD pipelines")
        print("• Container security best practices")
        print("• SAST and DAST security testing")
        print("• Security reporting and compliance")
        print("• Threat modeling and risk assessment")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Secure:{Colors.NC}")
        print("• A Flask application with security scanning")
        print("• Container vulnerability assessment")
        print("• Code quality and security analysis")
        print("• Automated security gates")
        print("• Production-ready security workflows")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 75-90 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to become a security sentinel?")
        print()
    
    def step_1_understand_security_scanning(self):
        """Step 1: Understand security scanning concepts."""
        self.print_header("Step 1: Understanding Security Scanning")
        print("=" * 60)
        
        self.print_learning("Let's explore the art of security scanning!")
        print()
        
        # Show application structure
        self.print_step("Exploring our security-focused application...")
        os.chdir(self.scenario_dir)
        
        print("📁 Security Sentinel Application Structure:")
        print("├── app.py                 # Main Flask application")
        print("├── requirements.txt       # Python dependencies")
        print("├── Dockerfile             # Container definition")
        print("├── security/              # Security scanning tools")
        print("│   └── scan.py            # Security scanning script")
        print("├── tests/                 # Test suite")
        print("│   ├── test_app.py        # Unit tests")
        print("│   └── test_security.py   # Security tests")
        print("└── Jenkinsfile            # Security pipeline")
        print()
        
        # Show security scan script
        self.print_step("Let's examine our security scanning script...")
        with open("security/scan.py", "r") as f:
            security_content = f.read()
        
        print("🛡️ Security Scanning Script:")
        print("-" * 35)
        print(security_content[:500] + "..." if len(security_content) > 500 else security_content)
        print("-" * 35)
        print()
        
        self.print_learning("Security Sentinel Techniques We'll Master:")
        print("• Container vulnerability scanning")
        print("• Code quality analysis")
        print("• Dependency vulnerability assessment")
        print("• Security policy enforcement")
        print("• Automated security reporting")
        print()
        
        self.wait_for_user("Ready to explore our security tests?")
        print()
    
    def step_2_explore_security_tests(self):
        """Step 2: Explore security testing capabilities."""
        self.print_header("Step 2: Exploring Security Testing")
        print("=" * 50)
        
        self.print_learning("Let's examine our comprehensive security test suite!")
        print()
        
        # Show test files
        self.print_step("Examining our security test files...")
        
        print("🧪 Security Test Suite Overview:")
        print("├── test_app.py - Unit tests for Flask app")
        print("└── test_security.py - Security integration tests")
        print()
        
        # Show test_security.py
        self.print_step("Let's look at our security integration tests...")
        with open("tests/test_security.py", "r") as f:
            test_content = f.read()
        
        print("🔒 Security Integration Tests:")
        print("-" * 35)
        print(test_content[:600] + "..." if len(test_content) > 600 else test_content)
        print("-" * 35)
        print()
        
        self.print_learning("Security Testing Features We're Using:")
        print("• Container vulnerability scanning")
        print("• Code quality analysis")
        print("• Dependency security assessment")
        print("• Security policy validation")
        print("• Automated security reporting")
        print()
        
        self.wait_for_user("Ready to run security tests locally?")
        print()
    
    def step_3_local_security_testing(self):
        """Step 3: Run security tests locally."""
        self.print_header("Step 3: Local Security Testing")
        print("=" * 50)
        
        self.print_learning("Let's see security scanning in action!")
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
        
        # Run security tests
        self.print_step("Running security integration tests...")
        if not self.run_command("python3 -m pytest tests/test_security.py -v"):
            self.print_info("Security tests may have failed due to scanning tools not being installed")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        # Build Docker image
        self.print_step("Building Docker image for security scanning...")
        if not self.run_command("docker build --no-cache -t security-sentinel-workshop ."):
            self.print_error("Docker build failed")
            return False
        
        # Run security scan
        self.print_step("Running security scan...")
        if not self.run_command("python3 security/scan.py"):
            self.print_info("Security scan may have failed due to scanning tools not being installed")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        self.print_success("Local security testing completed!")
        print()
        
        self.print_learning("Security Sentinel Skills Demonstrated:")
        print("• Container vulnerability scanning")
        print("• Code quality analysis")
        print("• Security policy enforcement")
        print("• Test-driven security development")
        print("• Local security workflows")
        print()
        
        self.wait_for_user("Ready to create your Security Sentinel Jenkins pipeline?")
        print()
    
    def step_4_jenkins_job_creation(self):
        """Step 4: Create Jenkins job for Security Sentinel."""
        self.print_header("Step 4: Creating Your Security Sentinel Jenkins Job")
        print("=" * 60)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now let's create a Jenkins job that guards security!")
        print()
        print("This job will demonstrate advanced security scanning")
        print("and vulnerability assessment in CI/CD pipelines.")
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
        print("   • Enter job name: 'Security Sentinel Guard'")
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
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_05_security_sentinel/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types for security scanning")
        print("• Git SCM integration for security workflows")
        print("• Pipeline script location for security gates")
        print("• Jenkins configuration for security automation")
        print()
        
        self.wait_for_user("Press Enter after configuring the pipeline...")
        print()
    
    def step_5_pipeline_execution(self):
        """Step 5: Execute and monitor the Security Sentinel pipeline."""
        self.print_header("Step 5: Running Your Security Sentinel Pipeline")
        print("=" * 60)
        
        self.print_learning("Time to see security scanning in action!")
        print()
        
        print("4️⃣  Execute Pipeline:")
        print("   • Click 'Build Now' to start the pipeline")
        print("   • Watch the pipeline execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Observe security scanning and vulnerability assessment")
        print()
        
        self.print_learning("Pipeline Stages You'll See:")
        print("   🛡️ Welcome - Security Sentinel introduction")
        print("   📦 Setup - Check Python and Docker environment")
        print("   🔧 Install Dependencies - Install security tools")
        print("   🧪 Run Unit Tests - Execute unit test suite")
        print("   🔒 Run Security Tests - Security integration tests")
        print("   🏗️ Build Docker Image - Container image creation")
        print("   🛡️ Security Scan - Vulnerability assessment")
        print("   📊 Security Report - Generate security reports")
        print("   ✅ Success! - Pipeline completion")
        print()
        
        self.wait_for_user("Press Enter after running the pipeline...")
        print()
        
        self.print_learning("Security Sentinel CI/CD Benefits:")
        print("• Automated security scanning")
        print("• Vulnerability assessment in CI/CD")
        print("• Security policy enforcement")
        print("• Compliance reporting")
        print("• Production-ready security workflows")
        print()
        
        self.wait_for_user("Ready to explore the Jenkinsfile?")
        print()
    
    def step_6_jenkinsfile_exploration(self):
        """Step 6: Explore and understand the Security Sentinel Jenkinsfile."""
        self.print_header("Step 6: Understanding the Security Sentinel Jenkinsfile")
        print("=" * 60)
        
        self.print_learning("The Jenkinsfile orchestrates security scanning!")
        print()
        
        # Show Jenkinsfile
        self.print_step("Let's examine our Security Sentinel Jenkinsfile...")
        with open("Jenkinsfile", "r") as f:
            jenkinsfile_content = f.read()
        
        print("📝 Security Sentinel Jenkinsfile:")
        print("-" * 40)
        print(jenkinsfile_content)
        print("-" * 40)
        print()
        
        self.print_learning("Security Sentinel Jenkinsfile Key Concepts:")
        print("• Security scanning integration")
        print("• Vulnerability assessment automation")
        print("• Security policy enforcement")
        print("• Compliance reporting")
        print("• Security gates and thresholds")
        print()
        
        self.print_learning("Advanced Security Patterns:")
        print("• SAST and DAST integration")
        print("• Container security scanning")
        print("• Dependency vulnerability assessment")
        print("• Security policy as code")
        print("• Threat modeling automation")
        print()
        
        self.wait_for_user("Ready to modify the Jenkinsfile?")
        print()
    
    def step_7_hands_on_modification(self):
        """Step 7: Hands-on Security Sentinel modification."""
        self.print_header("Step 7: Hands-On Security Sentinel Modification")
        print("=" * 60)
        
        self.print_learning("Let's customize your Security Sentinel pipeline!")
        print()
        
        print("🛠️  Modification Exercise:")
        print("Let's add a new security monitoring stage:")
        print()
        print("1. Go back to your Jenkins job")
        print("2. Click 'Configure'")
        print("3. Scroll to the Pipeline section")
        print("4. Change 'Pipeline script from SCM' to 'Pipeline script'")
        print("5. Copy the Jenkinsfile content into the text area")
        print("6. Add a new stage after the 'Security Report' stage:")
        print()
        
        print("```groovy")
        print("stage('🔍 Security Monitoring') {")
        print("    steps {")
        print("        echo 'Monitoring security metrics!'")
        print("        sh 'echo \"Security scan completed at $(date)\"'")
        print("        sh 'echo \"Vulnerability count: 0\"'")
        print("    }")
        print("}")
        print("```")
        print()
        
        self.wait_for_user("Press Enter after adding the monitoring stage...")
        print()
        
        print("7. Click 'Save'")
        print("8. Click 'Build Now' to run the modified pipeline")
        print("9. Watch your security monitoring stage execute!")
        print()
        
        self.wait_for_user("Press Enter after running the modified pipeline...")
        print()
        
        self.print_celebration("Congratulations! You've customized your Security Sentinel pipeline!")
        print()
        
        self.print_learning("What you just accomplished:")
        print("• Modified a Security Sentinel pipeline")
        print("• Added custom security monitoring")
        print("• Tested your changes in CI/CD")
        print("• Learned advanced security patterns")
        print()
    
    def step_8_advanced_concepts(self):
        """Step 8: Advanced security concepts and best practices."""
        self.print_header("Step 8: Advanced Security Concepts & Best Practices")
        print("=" * 60)
        
        self.print_learning("Let's explore advanced security mastery!")
        print()
        
        print("🔧 Advanced Security Features:")
        print("• SAST (Static Application Security Testing)")
        print("• DAST (Dynamic Application Security Testing)")
        print("• IAST (Interactive Application Security Testing)")
        print("• Container security scanning")
        print("• Dependency vulnerability assessment")
        print("• Secrets scanning and management")
        print()
        
        print("📊 Security Monitoring & Compliance:")
        print("• Security metrics and dashboards")
        print("• Compliance reporting (SOC2, PCI-DSS)")
        print("• Threat intelligence integration")
        print("• Incident response automation")
        print("• Security policy as code")
        print()
        
        print("🛡️ Security Best Practices:")
        print("• Shift-left security testing")
        print("• Security by design principles")
        print("• Threat modeling and risk assessment")
        print("• Security training and awareness")
        print("• Continuous security improvement")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• DevSecOps integration")
        print("• Cloud security automation")
        print("• Enterprise security compliance")
        print("• Security orchestration")
        print("• Risk management automation")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the Security Sentinel workshop."""
        self.print_header("🎓 Security Sentinel Workshop Conclusion")
        print("=" * 60)
        
        self.print_celebration("Congratulations! You've become a Security Sentinel!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Secured:{Colors.NC}")
        print("✅ Created a Security Sentinel Jenkins job from scratch")
        print("✅ Configured advanced security scanning in CI/CD")
        print("✅ Executed vulnerability assessment pipelines")
        print("✅ Modified and customized security workflows")
        print("✅ Learned advanced security patterns")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• Security scanning integration with Jenkins")
        print("• Vulnerability assessment in CI/CD pipelines")
        print("• Container security best practices")
        print("• SAST and DAST security testing")
        print("• Security reporting and compliance")
        print("• Threat modeling and risk assessment")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other Jenkins scenarios in this workshop")
        print("• Try advanced security scanning tools")
        print("• Integrate with your own projects")
        print("• Study DevSecOps methodologies")
        print("• Learn about compliance frameworks")
        print("• Explore security orchestration")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• OWASP Top 10: https://owasp.org/www-project-top-ten/")
        print("• NIST Cybersecurity Framework: https://www.nist.gov/cyberframework")
        print("• Trivy Security Scanner: https://trivy.dev/")
        print("• Jenkins Security Plugin: https://plugins.jenkins.io/security/")
        print()
        
        self.print_celebration("Thank you for participating in this workshop!")
        print("Keep guarding security like a true sentinel! 🛡️")
        print()
    
    def run_full_workshop(self):
        """Run the complete Security Sentinel workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_security_scanning()
            self.step_2_explore_security_tests()
            self.step_3_local_security_testing()
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
        """Run a quick Security Sentinel demo."""
        self.print_header("🚀 Quick Security Sentinel Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Test application locally
        if not self.step_3_local_security_testing():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins Security Sentinel Job Setup")
        print("=" * 40)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Pipeline job: 'Security Sentinel Guard'")
        print("4. Configure Git SCM with this repository")
        print("5. Set Script Path: Jenkins/jenkins-scenarios/scenario_05_security_sentinel/Jenkinsfile")
        print("6. Save and run the pipeline!")
        print()
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Security Sentinel Educational Workshop')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick demo instead of full workshop')
    parser.add_argument('--help-workshop', action='store_true',
                       help='Show workshop help')
    
    args = parser.parse_args()
    
    if args.help_workshop:
        print("Security Sentinel Educational Workshop")
        print("=" * 40)
        print()
        print("This workshop provides hands-on learning for:")
        print("• Security scanning integration with Jenkins")
        print("• Vulnerability assessment in CI/CD pipelines")
        print("• Container security best practices")
        print("• SAST and DAST security testing")
        print("• Security reporting and compliance")
        print("• Threat modeling and risk assessment")
        print()
        print("Usage:")
        print("  python3 demo.py              # Full educational workshop")
        print("  python3 demo.py --quick      # Quick demo")
        print("  python3 demo.py --help-workshop  # Show this help")
        return
    
    workshop = SecuritySentinelWorkshop()
    
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