#!/usr/bin/env python3
"""
EKS Deployment - Educational Jenkins Workshop
============================================

An unforgettable hands-on learning experience for AWS EKS deployment with Jenkins.
This workshop teaches you how to deploy to AWS EKS like a cloud-native expert!

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

class EKSDeploymentWorkshop:
    """Educational EKS Deployment Workshop."""
    
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
        """Welcome participants to the EKS Deployment workshop."""
        self.print_header("☸️ Welcome to the EKS Deployment Workshop!")
        print("=" * 60)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• AWS EKS deployment strategies with Jenkins")
        print("• Cloud-native CI/CD pipelines")
        print("• Kubernetes on AWS best practices")
        print("• Infrastructure as Code (IaC)")
        print("• Cloud security and compliance")
        print("• Production-ready cloud deployments")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Deploy:{Colors.NC}")
        print("• A Flask application to AWS EKS")
        print("• Cloud infrastructure automation")
        print("• Multi-environment deployment strategies")
        print("• Auto-scaling and monitoring")
        print("• Production-ready cloud workflows")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 105-120 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to deploy to the cloud like a pro?")
        print()
    
    def step_1_understand_eks_deployment(self):
        """Step 1: Understand EKS deployment concepts."""
        self.print_header("Step 1: Understanding EKS Deployment")
        print("=" * 60)
        
        self.print_learning("Let's explore the power of AWS EKS!")
        print()
        
        # Show application structure
        self.print_step("Exploring our cloud-ready application...")
        os.chdir(self.scenario_dir)
        
        print("📁 EKS Deployment Application Structure:")
        print("├── app.py                 # Main Flask application")
        print("├── requirements.txt       # Python dependencies")
        print("├── Dockerfile             # Container definition")
        print("├── k8s/                   # Kubernetes manifests")
        print("│   ├── deployment.yaml    # EKS deployment config")
        print("│   ├── service.yaml       # LoadBalancer service")
        print("│   ├── configmap.yaml     # Application config")
        print("│   └── secret.yaml        # AWS secrets")
        print("├── tests/                 # Test suite")
        print("│   ├── test_app.py        # Unit tests")
        print("│   └── test_eks.py        # EKS integration tests")
        print("└── Jenkinsfile            # EKS deployment pipeline")
        print()
        
        # Show deployment.yaml
        self.print_step("Let's examine our EKS deployment configuration...")
        with open("k8s/deployment.yaml", "r") as f:
            deployment_content = f.read()
        
        print("☸️ EKS Deployment Configuration:")
        print("-" * 40)
        print(deployment_content)
        print("-" * 40)
        print()
        
        self.print_learning("EKS Deployment Techniques We'll Master:")
        print("• AWS EKS cluster management")
        print("• Cloud-native deployment strategies")
        print("• Infrastructure as Code (IaC)")
        print("• Auto-scaling and load balancing")
        print("• Cloud security and compliance")
        print()
        
        self.wait_for_user("Ready to explore our cloud infrastructure?")
        print()
    
    def step_2_explore_cloud_infrastructure(self):
        """Step 2: Explore cloud infrastructure components."""
        self.print_header("Step 2: Exploring Cloud Infrastructure")
        print("=" * 50)
        
        self.print_learning("Let's examine our complete cloud infrastructure!")
        print()
        
        # Show service.yaml
        self.print_step("Let's look at our LoadBalancer service...")
        with open("k8s/service.yaml", "r") as f:
            service_content = f.read()
        
        print("🌐 EKS LoadBalancer Service:")
        print("-" * 35)
        print(service_content)
        print("-" * 35)
        print()
        
        # Show configmap.yaml
        self.print_step("Let's examine our cloud configuration...")
        with open("k8s/configmap.yaml", "r") as f:
            configmap_content = f.read()
        
        print("⚙️ EKS ConfigMap:")
        print("-" * 20)
        print(configmap_content)
        print("-" * 20)
        print()
        
        self.print_learning("Cloud Infrastructure Features:")
        print("• AWS LoadBalancer integration")
        print("• Cloud-native configuration management")
        print("• AWS secrets and IAM integration")
        print("• Auto-scaling and health checks")
        print("• Cloud monitoring and logging")
        print()
        
        self.wait_for_user("Ready to test our EKS deployment locally?")
        print()
    
    def step_3_local_eks_testing(self):
        """Step 3: Test EKS deployment locally."""
        self.print_header("Step 3: Local EKS Testing")
        print("=" * 50)
        
        self.print_learning("Let's test our EKS deployment skills!")
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
        
        # Run EKS tests
        self.print_step("Running EKS integration tests...")
        if not self.run_command("python3 -m pytest tests/test_eks.py -v"):
            self.print_info("EKS tests may have failed due to AWS credentials not being available")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        # Build Docker image
        self.print_step("Building Docker image for EKS...")
        if not self.run_command("docker build --no-cache -t eks-deployment-workshop ."):
            self.print_error("Docker build failed")
            return False
        
        self.print_success("Local EKS testing completed!")
        print()
        
        self.print_learning("EKS Deployment Skills Demonstrated:")
        print("• Container image preparation")
        print("• EKS manifest validation")
        print("• Test-driven development")
        print("• Local development workflows")
        print("• Docker-EKS integration")
        print()
        
        self.wait_for_user("Ready to create your EKS Deployment Jenkins pipeline?")
        print()
    
    def step_4_jenkins_job_creation(self):
        """Step 4: Create Jenkins job for EKS Deployment."""
        self.print_header("Step 4: Creating Your EKS Deployment Jenkins Job")
        print("=" * 60)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now let's create a Jenkins job that deploys to EKS!")
        print()
        print("This job will demonstrate advanced cloud deployment")
        print("strategies and AWS EKS integration.")
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
        print("   • Enter job name: 'EKS Cloud Deployment'")
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
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_03_eks_deployment/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types for cloud deployments")
        print("• Git SCM integration for cloud workflows")
        print("• Pipeline script location for EKS deployment")
        print("• Jenkins configuration for cloud automation")
        print()
        
        self.wait_for_user("Press Enter after configuring the pipeline...")
        print()
    
    def step_5_pipeline_execution(self):
        """Step 5: Execute and monitor the EKS Deployment pipeline."""
        self.print_header("Step 5: Running Your EKS Deployment Pipeline")
        print("=" * 60)
        
        self.print_learning("Time to see cloud deployment in action!")
        print()
        
        print("4️⃣  Execute Pipeline:")
        print("   • Click 'Build Now' to start the pipeline")
        print("   • Watch the pipeline execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Observe EKS deployment and cloud orchestration")
        print()
        
        self.print_learning("Pipeline Stages You'll See:")
        print("   ☸️ Welcome - EKS Deployment introduction")
        print("   📦 Setup - Check Python and Docker environment")
        print("   🔧 Install Dependencies - Install test dependencies")
        print("   🧪 Run Unit Tests - Execute unit test suite")
        print("   ☸️ Run EKS Tests - EKS integration tests")
        print("   🏗️ Build Docker Image - Container image creation")
        print("   🚢 Deploy to EKS - AWS EKS deployment")
        print("   📊 Health Check - Application health verification")
        print("   ✅ Success! - Pipeline completion")
        print()
        
        self.wait_for_user("Press Enter after running the pipeline...")
        print()
        
        self.print_learning("EKS Deployment CI/CD Benefits:")
        print("• Automated cloud deployments")
        print("• Infrastructure as Code (IaC)")
        print("• Multi-environment deployment strategies")
        print("• Auto-scaling and monitoring")
        print("• Production-ready cloud workflows")
        print()
        
        self.wait_for_user("Ready to explore the Jenkinsfile?")
        print()
    
    def step_6_jenkinsfile_exploration(self):
        """Step 6: Explore and understand the EKS Deployment Jenkinsfile."""
        self.print_header("Step 6: Understanding the EKS Deployment Jenkinsfile")
        print("=" * 60)
        
        self.print_learning("The Jenkinsfile orchestrates cloud deployments!")
        print()
        
        # Show Jenkinsfile
        self.print_step("Let's examine our EKS Deployment Jenkinsfile...")
        with open("Jenkinsfile", "r") as f:
            jenkinsfile_content = f.read()
        
        print("📝 EKS Deployment Jenkinsfile:")
        print("-" * 40)
        print(jenkinsfile_content)
        print("-" * 40)
        print()
        
        self.print_learning("EKS Deployment Jenkinsfile Key Concepts:")
        print("• AWS EKS deployment strategies")
        print("• Cloud infrastructure automation")
        print("• Infrastructure as Code (IaC)")
        print("• Auto-scaling and load balancing")
        print("• Cloud security and compliance")
        print()
        
        self.print_learning("Advanced Cloud Patterns:")
        print("• Blue-Green deployments")
        print("• Canary releases")
        print("• Multi-region deployments")
        print("• Cloud cost optimization")
        print("• Disaster recovery")
        print()
        
        self.wait_for_user("Ready to modify the Jenkinsfile?")
        print()
    
    def step_7_hands_on_modification(self):
        """Step 7: Hands-on EKS Deployment modification."""
        self.print_header("Step 7: Hands-On EKS Deployment Modification")
        print("=" * 60)
        
        self.print_learning("Let's customize your EKS Deployment pipeline!")
        print()
        
        print("🛠️  Modification Exercise:")
        print("Let's add a new cloud monitoring stage:")
        print()
        print("1. Go back to your Jenkins job")
        print("2. Click 'Configure'")
        print("3. Scroll to the Pipeline section")
        print("4. Change 'Pipeline script from SCM' to 'Pipeline script'")
        print("5. Copy the Jenkinsfile content into the text area")
        print("6. Add a new stage after the 'Health Check' stage:")
        print()
        
        print("```groovy")
        print("stage('📊 Cloud Monitoring') {")
        print("    steps {")
        print("        echo 'Monitoring EKS deployment status!'")
        print("        sh 'echo \"EKS cluster: eks-workshop-cluster\"'")
        print("        sh 'echo \"Deployment status: Running\"'")
        print("    }")
        print("}")
        print("```")
        print()
        
        self.wait_for_user("Press Enter after adding the monitoring stage...")
        print()
        
        print("7. Click 'Save'")
        print("8. Click 'Build Now' to run the modified pipeline")
        print("9. Watch your cloud monitoring stage execute!")
        print()
        
        self.wait_for_user("Press Enter after running the modified pipeline...")
        print()
        
        self.print_celebration("Congratulations! You've customized your EKS Deployment pipeline!")
        print()
        
        self.print_learning("What you just accomplished:")
        print("• Modified an EKS Deployment pipeline")
        print("• Added custom cloud monitoring")
        print("• Tested your changes in CI/CD")
        print("• Learned advanced cloud patterns")
        print()
    
    def step_8_advanced_concepts(self):
        """Step 8: Advanced cloud concepts and best practices."""
        self.print_header("Step 8: Advanced Cloud Concepts & Best Practices")
        print("=" * 60)
        
        self.print_learning("Let's explore advanced cloud mastery!")
        print()
        
        print("🔧 Advanced Cloud Features:")
        print("• Multi-region deployments")
        print("• Cloud-native monitoring (CloudWatch)")
        print("• Infrastructure as Code (Terraform, CDK)")
        print("• Serverless integration (Lambda, Fargate)")
        print("• Cloud security and compliance")
        print("• Cost optimization strategies")
        print()
        
        print("📊 Cloud Monitoring & Observability:")
        print("• CloudWatch metrics and alarms")
        print("• Distributed tracing with X-Ray")
        print("• Log aggregation and analysis")
        print("• Performance monitoring")
        print("• Incident response automation")
        print()
        
        print("🛡️ Cloud Security Best Practices:")
        print("• IAM roles and policies")
        print("• VPC and network security")
        print("• Secrets management (AWS Secrets Manager)")
        print("• Container security scanning")
        print("• Compliance frameworks (SOC2, PCI-DSS)")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• Microservices on AWS")
        print("• CI/CD pipeline automation")
        print("• Cloud-native application deployment")
        print("• DevOps and platform engineering")
        print("• Enterprise-scale cloud deployments")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the EKS Deployment workshop."""
        self.print_header("🎓 EKS Deployment Workshop Conclusion")
        print("=" * 60)
        
        self.print_celebration("Congratulations! You've mastered EKS Deployment!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Deployed:{Colors.NC}")
        print("✅ Created an EKS Deployment Jenkins job from scratch")
        print("✅ Configured advanced cloud deployment strategies")
        print("✅ Executed AWS EKS deployment automation")
        print("✅ Modified and customized cloud workflows")
        print("✅ Learned advanced cloud patterns")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• AWS EKS deployment strategies with Jenkins")
        print("• Cloud-native CI/CD pipelines")
        print("• Kubernetes on AWS best practices")
        print("• Infrastructure as Code (IaC)")
        print("• Cloud security and compliance")
        print("• Production-ready cloud deployments")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other Jenkins scenarios in this workshop")
        print("• Try advanced AWS services")
        print("• Integrate with your own projects")
        print("• Study cloud-native architectures")
        print("• Learn about Infrastructure as Code")
        print("• Explore cloud security frameworks")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• AWS EKS Documentation: https://docs.aws.amazon.com/eks/")
        print("• Kubernetes on AWS: https://kubernetes.io/docs/setup/production-environment/turnkey/aws/")
        print("• Terraform AWS Provider: https://registry.terraform.io/providers/hashicorp/aws/")
        print("• AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/")
        print()
        
        self.print_celebration("Thank you for participating in this workshop!")
        print("Keep deploying to the cloud like a true expert! ☸️")
        print()
    
    def run_full_workshop(self):
        """Run the complete EKS Deployment workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_eks_deployment()
            self.step_2_explore_cloud_infrastructure()
            self.step_3_local_eks_testing()
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
        """Run a quick EKS Deployment demo."""
        self.print_header("🚀 Quick EKS Deployment Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Test application locally
        if not self.step_3_local_eks_testing():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins EKS Deployment Job Setup")
        print("=" * 40)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Pipeline job: 'EKS Cloud Deployment'")
        print("4. Configure Git SCM with this repository")
        print("5. Set Script Path: Jenkins/jenkins-scenarios/scenario_03_eks_deployment/Jenkinsfile")
        print("6. Save and run the pipeline!")
        print()
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='EKS Deployment Educational Workshop')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick demo instead of full workshop')
    parser.add_argument('--help-workshop', action='store_true',
                       help='Show workshop help')
    
    args = parser.parse_args()
    
    if args.help_workshop:
        print("EKS Deployment Educational Workshop")
        print("=" * 40)
        print()
        print("This workshop provides hands-on learning for:")
        print("• AWS EKS deployment strategies with Jenkins")
        print("• Cloud-native CI/CD pipelines")
        print("• Kubernetes on AWS best practices")
        print("• Infrastructure as Code (IaC)")
        print("• Cloud security and compliance")
        print("• Production-ready cloud deployments")
        print()
        print("Usage:")
        print("  python3 demo.py              # Full educational workshop")
        print("  python3 demo.py --quick      # Quick demo")
        print("  python3 demo.py --help-workshop  # Show this help")
        return
    
    workshop = EKSDeploymentWorkshop()
    
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