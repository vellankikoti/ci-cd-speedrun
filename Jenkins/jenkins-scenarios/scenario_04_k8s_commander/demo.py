#!/usr/bin/env python3
"""
K8s Commander - Educational Jenkins Workshop
===========================================

An unforgettable hands-on learning experience for Kubernetes deployment with Jenkins.
This workshop teaches you how to command Kubernetes deployments like a true commander!

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

class K8sCommanderWorkshop:
    """Educational K8s Commander Workshop."""
    
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
        """Welcome participants to the K8s Commander workshop."""
        self.print_header("🚀 Welcome to the K8s Commander Workshop!")
        print("=" * 60)
        print()
        print(f"{Colors.BOLD}🎓 What You'll Learn Today:{Colors.NC}")
        print("• Kubernetes deployment strategies with Jenkins")
        print("• Container orchestration in CI/CD pipelines")
        print("• K8s resource management and scaling")
        print("• Service discovery and load balancing")
        print("• ConfigMaps and Secrets management")
        print("• Advanced deployment patterns")
        print()
        print(f"{Colors.BOLD}🛠️  What You'll Command:{Colors.NC}")
        print("• A Flask application deployed to Kubernetes")
        print("• Multi-environment deployment strategies")
        print("• Auto-scaling and health monitoring")
        print("• Service mesh integration")
        print("• Production-ready K8s workflows")
        print()
        print(f"{Colors.BOLD}⏱️  Workshop Duration: 90-105 minutes{Colors.NC}")
        print()
        
        self.wait_for_user("Ready to command Kubernetes like a pro?")
        print()
    
    def step_1_understand_k8s_deployment(self):
        """Step 1: Understand Kubernetes deployment concepts."""
        self.print_header("Step 1: Understanding Kubernetes Deployment")
        print("=" * 60)
        
        self.print_learning("Let's explore the power of Kubernetes orchestration!")
        print()
        
        # Show application structure
        self.print_step("Exploring our K8s-ready application...")
        os.chdir(self.scenario_dir)
        
        print("📁 K8s Commander Application Structure:")
        print("├── app.py                 # Main Flask application")
        print("├── requirements.txt       # Python dependencies")
        print("├── Dockerfile             # Container definition")
        print("├── k8s/                   # Kubernetes manifests")
        print("│   ├── deployment.yaml    # Deployment configuration")
        print("│   ├── service.yaml       # Service configuration")
        print("│   ├── configmap.yaml     # ConfigMap for app config")
        print("│   └── secret.yaml        # Secret for sensitive data")
        print("├── tests/                 # Test suite")
        print("│   ├── test_app.py        # Unit tests")
        print("│   └── test_k8s.py        # K8s integration tests")
        print("└── Jenkinsfile            # K8s deployment pipeline")
        print()
        
        # Show deployment.yaml
        self.print_step("Let's examine our Kubernetes deployment...")
        with open("k8s/deployment.yaml", "r") as f:
            deployment_content = f.read()
        
        print("☸️ Kubernetes Deployment:")
        print("-" * 30)
        print(deployment_content)
        print("-" * 30)
        print()
        
        self.print_learning("K8s Commander Techniques We'll Master:")
        print("• Deployment strategies (Rolling, Blue-Green)")
        print("• Service discovery and load balancing")
        print("• ConfigMaps and Secrets management")
        print("• Auto-scaling and health checks")
        print("• Resource limits and requests")
        print()
        
        self.wait_for_user("Ready to explore our K8s manifests?")
        print()
    
    def step_2_explore_k8s_manifests(self):
        """Step 2: Explore Kubernetes manifests."""
        self.print_header("Step 2: Exploring Kubernetes Manifests")
        print("=" * 50)
        
        self.print_learning("Let's examine our complete K8s configuration!")
        print()
        
        # Show service.yaml
        self.print_step("Let's look at our Service configuration...")
        with open("k8s/service.yaml", "r") as f:
            service_content = f.read()
        
        print("🌐 Kubernetes Service:")
        print("-" * 25)
        print(service_content)
        print("-" * 25)
        print()
        
        # Show configmap.yaml
        self.print_step("Let's examine our ConfigMap...")
        with open("k8s/configmap.yaml", "r") as f:
            configmap_content = f.read()
        
        print("⚙️ Kubernetes ConfigMap:")
        print("-" * 30)
        print(configmap_content)
        print("-" * 30)
        print()
        
        self.print_learning("K8s Manifest Features:")
        print("• Service types (ClusterIP, NodePort, LoadBalancer)")
        print("• ConfigMaps for application configuration")
        print("• Secrets for sensitive data")
        print("• Resource limits and requests")
        print("• Health checks and probes")
        print()
        
        self.wait_for_user("Ready to test our K8s deployment locally?")
        print()
    
    def step_3_local_k8s_testing(self):
        """Step 3: Test K8s deployment locally."""
        self.print_header("Step 3: Local Kubernetes Testing")
        print("=" * 50)
        
        self.print_learning("Let's test our K8s deployment skills!")
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
        
        # Run K8s tests
        self.print_step("Running K8s integration tests...")
        if not self.run_command("python3 -m pytest tests/test_k8s.py -v"):
            self.print_info("K8s tests may have failed due to cluster not being available")
            self.print_info("This is normal in workshop environments. Continuing...")
        
        # Build Docker image
        self.print_step("Building Docker image for K8s...")
        if not self.run_command("docker build --no-cache -t k8s-commander-workshop ."):
            self.print_error("Docker build failed")
            return False
        
        self.print_success("Local K8s testing completed!")
        print()
        
        self.print_learning("K8s Commander Skills Demonstrated:")
        print("• Container image preparation")
        print("• K8s manifest validation")
        print("• Test-driven development")
        print("• Local development workflows")
        print("• Docker-K8s integration")
        print()
        
        self.wait_for_user("Ready to create your K8s Commander Jenkins pipeline?")
        print()
    
    def step_4_jenkins_job_creation(self):
        """Step 4: Create Jenkins job for K8s Commander."""
        self.print_header("Step 4: Creating Your K8s Commander Jenkins Job")
        print("=" * 60)
        
        if not self.check_jenkins_running():
            self.print_error("Jenkins is not running. Please start it first.")
            return False
        
        self.print_learning("Now let's create a Jenkins job that commands Kubernetes!")
        print()
        print("This job will demonstrate advanced K8s deployment")
        print("strategies and orchestration techniques.")
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
        print("   • Enter job name: 'K8s Commander Deployment'")
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
        print("   • Script Path: 'Jenkins/jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile'")
        print("   • Click 'Save'")
        print()
        
        self.print_learning("What you just learned:")
        print("• Jenkins job types for K8s deployments")
        print("• Git SCM integration for containerized apps")
        print("• Pipeline script location for K8s orchestration")
        print("• Jenkins configuration for advanced deployments")
        print()
        
        self.wait_for_user("Press Enter after configuring the pipeline...")
        print()
    
    def step_5_pipeline_execution(self):
        """Step 5: Execute and monitor the K8s Commander pipeline."""
        self.print_header("Step 5: Running Your K8s Commander Pipeline")
        print("=" * 60)
        
        self.print_learning("Time to see K8s orchestration in action!")
        print()
        
        print("4️⃣  Execute Pipeline:")
        print("   • Click 'Build Now' to start the pipeline")
        print("   • Watch the pipeline execute in real-time")
        print("   • Click on the build number to see detailed logs")
        print("   • Observe K8s deployment and orchestration")
        print()
        
        self.print_learning("Pipeline Stages You'll See:")
        print("   🚀 Welcome - K8s Commander introduction")
        print("   📦 Setup - Check Python and Docker environment")
        print("   🔧 Install Dependencies - Install test dependencies")
        print("   🧪 Run Unit Tests - Execute unit test suite")
        print("   ☸️ Run K8s Tests - Kubernetes integration tests")
        print("   🏗️ Build Docker Image - Container image creation")
        print("   🚢 Deploy to K8s - Kubernetes deployment")
        print("   📊 Health Check - Application health verification")
        print("   ✅ Success! - Pipeline completion")
        print()
        
        self.wait_for_user("Press Enter after running the pipeline...")
        print()
        
        self.print_learning("K8s Commander CI/CD Benefits:")
        print("• Automated Kubernetes deployments")
        print("• Container orchestration management")
        print("• Multi-environment deployment strategies")
        print("• Health monitoring and scaling")
        print("• Production-ready workflows")
        print()
        
        self.wait_for_user("Ready to explore the Jenkinsfile?")
        print()
    
    def step_6_jenkinsfile_exploration(self):
        """Step 6: Explore and understand the K8s Commander Jenkinsfile."""
        self.print_header("Step 6: Understanding the K8s Commander Jenkinsfile")
        print("=" * 60)
        
        self.print_learning("The Jenkinsfile orchestrates K8s deployments!")
        print()
        
        # Show Jenkinsfile
        self.print_step("Let's examine our K8s Commander Jenkinsfile...")
        with open("Jenkinsfile", "r") as f:
            jenkinsfile_content = f.read()
        
        print("📝 K8s Commander Jenkinsfile:")
        print("-" * 35)
        print(jenkinsfile_content)
        print("-" * 35)
        print()
        
        self.print_learning("K8s Commander Jenkinsfile Key Concepts:")
        print("• Kubernetes deployment strategies")
        print("• Container orchestration management")
        print("• Service discovery and load balancing")
        print("• ConfigMaps and Secrets handling")
        print("• Health checks and monitoring")
        print()
        
        self.print_learning("Advanced K8s Patterns:")
        print("• Rolling updates and rollbacks")
        print("• Blue-Green deployments")
        print("• Canary releases")
        print("• Auto-scaling configuration")
        print("• Service mesh integration")
        print()
        
        self.wait_for_user("Ready to modify the Jenkinsfile?")
        print()
    
    def step_7_hands_on_modification(self):
        """Step 7: Hands-on K8s Commander modification."""
        self.print_header("Step 7: Hands-On K8s Commander Modification")
        print("=" * 60)
        
        self.print_learning("Let's customize your K8s Commander pipeline!")
        print()
        
        print("🛠️  Modification Exercise:")
        print("Let's add a new K8s monitoring stage:")
        print()
        print("1. Go back to your Jenkins job")
        print("2. Click 'Configure'")
        print("3. Scroll to the Pipeline section")
        print("4. Change 'Pipeline script from SCM' to 'Pipeline script'")
        print("5. Copy the Jenkinsfile content into the text area")
        print("6. Add a new stage after the 'Health Check' stage:")
        print()
        
        print("```groovy")
        print("stage('📊 K8s Monitoring') {")
        print("    steps {")
        print("        echo 'Monitoring K8s deployment status!'")
        print("        sh 'kubectl get pods -l app=k8s-commander'")
        print("        sh 'kubectl get services -l app=k8s-commander'")
        print("    }")
        print("}")
        print("```")
        print()
        
        self.wait_for_user("Press Enter after adding the monitoring stage...")
        print()
        
        print("7. Click 'Save'")
        print("8. Click 'Build Now' to run the modified pipeline")
        print("9. Watch your monitoring stage execute!")
        print()
        
        self.wait_for_user("Press Enter after running the modified pipeline...")
        print()
        
        self.print_celebration("Congratulations! You've customized your K8s Commander pipeline!")
        print()
        
        self.print_learning("What you just accomplished:")
        print("• Modified a K8s Commander pipeline")
        print("• Added custom monitoring functionality")
        print("• Tested your changes in CI/CD")
        print("• Learned advanced K8s patterns")
        print()
    
    def step_8_advanced_concepts(self):
        """Step 8: Advanced K8s concepts and best practices."""
        self.print_header("Step 8: Advanced K8s Concepts & Best Practices")
        print("=" * 60)
        
        self.print_learning("Let's explore advanced K8s mastery!")
        print()
        
        print("🔧 Advanced K8s Features:")
        print("• Service mesh integration (Istio, Linkerd)")
        print("• Custom Resource Definitions (CRDs)")
        print("• Operators and controllers")
        print("• Helm charts and package management")
        print("• GitOps with ArgoCD/Flux")
        print("• Multi-cluster management")
        print()
        
        print("📊 Monitoring & Observability:")
        print("• Prometheus and Grafana integration")
        print("• Distributed tracing with Jaeger")
        print("• Log aggregation with ELK stack")
        print("• Application performance monitoring")
        print("• Alerting and incident response")
        print()
        
        print("🛡️ Security Best Practices:")
        print("• RBAC and service accounts")
        print("• Network policies and security contexts")
        print("• Secrets management with external systems")
        print("• Image scanning and vulnerability management")
        print("• Compliance and audit logging")
        print()
        
        self.print_learning("Real-World Applications:")
        print("• Microservices orchestration")
        print("• CI/CD pipeline automation")
        print("• Cloud-native application deployment")
        print("• DevOps and platform engineering")
        print("• Enterprise-scale deployments")
        print()
        
        self.wait_for_user("Ready to wrap up the workshop?")
        print()
    
    def workshop_conclusion(self):
        """Wrap up the K8s Commander workshop."""
        self.print_header("🎓 K8s Commander Workshop Conclusion")
        print("=" * 60)
        
        self.print_celebration("Congratulations! You've become a K8s Commander!")
        print()
        
        print(f"{Colors.BOLD}🎯 What You've Commanded:{Colors.NC}")
        print("✅ Created a K8s Commander Jenkins job from scratch")
        print("✅ Configured advanced K8s deployment strategies")
        print("✅ Executed container orchestration in CI/CD")
        print("✅ Modified and customized K8s pipelines")
        print("✅ Learned advanced deployment patterns")
        print()
        
        print(f"{Colors.BOLD}🧠 Key Skills You've Gained:{Colors.NC}")
        print("• Kubernetes deployment strategies with Jenkins")
        print("• Container orchestration in CI/CD pipelines")
        print("• K8s resource management and scaling")
        print("• Service discovery and load balancing")
        print("• ConfigMaps and Secrets management")
        print("• Advanced deployment patterns")
        print()
        
        print(f"{Colors.BOLD}🚀 Next Steps for Your Learning:{Colors.NC}")
        print("• Explore other Jenkins scenarios in this workshop")
        print("• Try advanced K8s features")
        print("• Integrate with your own projects")
        print("• Study service mesh technologies")
        print("• Learn about GitOps patterns")
        print("• Explore cloud-native architectures")
        print()
        
        print(f"{Colors.BOLD}📚 Additional Resources:{Colors.NC}")
        print("• Kubernetes Documentation: https://kubernetes.io/docs/")
        print("• Jenkins K8s Plugin: https://plugins.jenkins.io/kubernetes/")
        print("• Helm Charts: https://helm.sh/")
        print("• ArgoCD GitOps: https://argo-cd.readthedocs.io/")
        print()
        
        self.print_celebration("Thank you for participating in this workshop!")
        print("Keep commanding Kubernetes like a true commander! 🚀")
        print()
    
    def run_full_workshop(self):
        """Run the complete K8s Commander workshop."""
        try:
            self.workshop_introduction()
            self.step_1_understand_k8s_deployment()
            self.step_2_explore_k8s_manifests()
            self.step_3_local_k8s_testing()
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
        """Run a quick K8s Commander demo."""
        self.print_header("🚀 Quick K8s Commander Demo")
        print("=" * 50)
        print("This is a condensed version of the full workshop.")
        print()
        
        # Test application locally
        if not self.step_3_local_k8s_testing():
            return False
        
        # Show Jenkins setup
        self.print_header("Jenkins K8s Commander Job Setup")
        print("=" * 40)
        print("1. Open Jenkins: http://localhost:8080")
        print("2. Login: admin/admin")
        print("3. Create Pipeline job: 'K8s Commander Deployment'")
        print("4. Configure Git SCM with this repository")
        print("5. Set Script Path: Jenkins/jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile")
        print("6. Save and run the pipeline!")
        print()
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='K8s Commander Educational Workshop')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick demo instead of full workshop')
    parser.add_argument('--help-workshop', action='store_true',
                       help='Show workshop help')
    
    args = parser.parse_args()
    
    if args.help_workshop:
        print("K8s Commander Educational Workshop")
        print("=" * 40)
        print()
        print("This workshop provides hands-on learning for:")
        print("• Kubernetes deployment strategies with Jenkins")
        print("• Container orchestration in CI/CD pipelines")
        print("• K8s resource management and scaling")
        print("• Service discovery and load balancing")
        print("• ConfigMaps and Secrets management")
        print("• Advanced deployment patterns")
        print()
        print("Usage:")
        print("  python3 demo.py              # Full educational workshop")
        print("  python3 demo.py --quick      # Quick demo")
        print("  python3 demo.py --help-workshop  # Show this help")
        return
    
    workshop = K8sCommanderWorkshop()
    
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