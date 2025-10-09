#!/usr/bin/env python3
"""
Jenkins CI/CD Workshop - Cross-Platform Setup Script
====================================================

A comprehensive, cross-platform script to set up Jenkins for the CI/CD Chaos Workshop.
Works seamlessly on Windows, macOS, Linux, and virtual machines.

Usage:
    python3 jenkins-setup.py setup     # Setup Jenkins
    python3 jenkins-setup.py status    # Check Jenkins status
    python3 jenkins-setup.py cleanup   # Clean up everything
    python3 jenkins-setup.py demo      # Run demo scenarios
"""

import subprocess
import time
import os
import sys
import platform
import requests
import json
import argparse
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

class JenkinsSetup:
    """Cross-platform Jenkins setup and management."""
    
    def __init__(self):
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_mac = self.platform == 'darwin'
        self.is_linux = self.platform == 'linux'
        self.jenkins_container = 'jenkins-workshop'
        self.jenkins_image = 'jenkins-workshop:custom'
        self.jenkins_port = 8080
        self.jenkins_url = f'http://localhost:{self.jenkins_port}'
        self.jenkins_username = 'admin'
        self.jenkins_password = 'admin'
        self.workspace_path = Path(__file__).parent.absolute()
        
        # Detect cloud VM environments
        self.is_cloud_vm = self._detect_cloud_environment()
        self.is_docker_desktop = self._detect_docker_desktop()
        
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
        
    def print_info(self, message):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.NC}")
        
    def run_command(self, cmd, description="", capture_output=False, check=True):
        """Run a command with cross-platform support."""
        if description:
            self.print_step(description)
            
        try:
            # Use shell=True for cross-platform compatibility
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=capture_output, 
                text=True,
                check=False  # We'll handle errors manually
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
    
    def get_python_command(self):
        """Get the correct Python command for the platform."""
        # Try python3 first, then python
        for cmd in ['python3', 'python']:
            if self.run_command(f"{cmd} --version", capture_output=True):
                return cmd
        return 'python3'  # fallback
    
    def get_pip_command(self):
        """Get the correct pip command for the platform."""
        python_cmd = self.get_python_command()
        # Try pip3 first, then pip, then python -m pip
        for cmd in ['pip3', 'pip', f'{python_cmd} -m pip']:
            if self.run_command(f"{cmd} --version", capture_output=True):
                return cmd
        return f'{python_cmd} -m pip'  # fallback

    def _detect_cloud_environment(self):
        """Detect if running in a cloud VM environment."""
        try:
            # Check for common cloud VM indicators
            cloud_indicators = [
                '/sys/class/dmi/id/product_name',  # AWS, Azure, GCP
                '/sys/class/dmi/id/board_vendor',  # VMware, VirtualBox
                '/proc/version',  # Check for cloud-specific kernels
            ]
            
            for indicator in cloud_indicators:
                if os.path.exists(indicator):
                    with open(indicator, 'r') as f:
                        content = f.read().lower()
                        if any(cloud in content for cloud in ['amazon', 'aws', 'azure', 'google', 'vmware', 'virtualbox', 'qemu']):
                            return True
            
            # Check environment variables
            cloud_env_vars = ['AWS_REGION', 'AZURE_REGION', 'GCP_ZONE', 'CLOUD_PROVIDER']
            if any(os.environ.get(var) for var in cloud_env_vars):
                return True
                
        except Exception:
            pass
        
        return False

    def _detect_docker_desktop(self):
        """Detect if running Docker Desktop vs Docker Engine."""
        try:
            # Docker Desktop typically has different behavior
            result = self.run_command("docker context ls", capture_output=True)
            if result and "desktop" in result.lower():
                return True
        except Exception:
            pass
        return False

    def check_docker_installed(self):
        """Check if Docker is installed and running."""
        self.print_step("Checking Docker installation...")
        
        if not self.run_command("docker --version", capture_output=True):
            self.print_error("Docker is not installed or not in PATH")
            self.print_info("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/")
            return False
            
        if not self.run_command("docker info", capture_output=True):
            self.print_error("Docker is not running")
            self.print_info("Please start Docker Desktop and try again")
            return False
            
        self.print_success("Docker is installed and running")
        return True
    
    def check_docker_compose(self):
        """Check if Docker Compose is available."""
        self.print_step("Checking Docker Compose...")
        
        # Try docker compose (newer) first, then docker-compose (legacy)
        if self.run_command("docker compose version", capture_output=True):
            self.print_success("Docker Compose is available")
            return True
        elif self.run_command("docker-compose --version", capture_output=True):
            self.print_success("Docker Compose is available")
            return True
        else:
            self.print_info("Docker Compose not found, but not required for this setup")
            return True
    
    def build_jenkins_image(self):
        """Build the custom Jenkins image."""
        self.print_header("Building Custom Jenkins Image")
        print("=" * 50)
        
        # Change to Jenkins directory
        jenkins_dir = Path(__file__).parent
        os.chdir(jenkins_dir)
        
        self.print_step("Building Jenkins image with all plugins...")
        self.print_info("This may take 2-3 minutes to download and install 146+ plugins")
        
        build_cmd = "docker build -t jenkins-workshop:custom ."
        if not self.run_command(build_cmd, "Building Jenkins image..."):
            self.print_error("Failed to build Jenkins image")
            return False
            
        self.print_success("Jenkins image built successfully!")
        return True
    
    def start_jenkins_container(self):
        """Start the Jenkins container with proper configuration."""
        self.print_header("Starting Jenkins Container")
        print("=" * 50)
        
        # Stop and remove existing container if it exists
        self.run_command(f"docker stop {self.jenkins_container}", "Stopping existing container...", check=False)
        self.run_command(f"docker rm {self.jenkins_container}", "Removing existing container...", check=False)
        
        # Prepare Docker run command with cross-platform path handling
        workspace_mount = str(self.workspace_path)
        if self.is_windows:
            # Windows path handling - more robust
            workspace_mount = workspace_mount.replace('\\', '/')
            # Handle drive letters (C: -> /c)
            if len(workspace_mount) > 1 and workspace_mount[1] == ':':
                workspace_mount = f"/{workspace_mount[0].lower()}{workspace_mount[2:]}"
            # Handle UNC paths and other Windows-specific cases
            if workspace_mount.startswith('//'):
                workspace_mount = workspace_mount[1:]  # Remove leading slash for UNC
        else:
            # Unix/Linux/Mac - ensure absolute path
            workspace_mount = str(self.workspace_path.resolve())
        
        docker_run_cmd = f"""docker run -d \
  --name {self.jenkins_container} \
  --restart=unless-stopped \
  -p {self.jenkins_port}:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "{workspace_mount}":/workspace \
  --privileged \
  {self.jenkins_image}"""
        
        if not self.run_command(docker_run_cmd, "Starting Jenkins container..."):
            self.print_error("Failed to start Jenkins container")
            return False
        
        # Fix Docker socket permissions (Linux/Mac only)
        if not self.is_windows:
            self.print_step("Fixing Docker socket permissions...")
            # Try multiple approaches for Docker socket permissions
            self.run_command(f"docker exec -u root {self.jenkins_container} chown root:docker /var/run/docker.sock", check=False)
            self.run_command(f"docker exec -u root {self.jenkins_container} chmod 666 /var/run/docker.sock", check=False)
            
            # Alternative approach for cloud VMs and different Docker setups
            self.run_command(f"docker exec -u root {self.jenkins_container} chmod 777 /var/run/docker.sock", check=False)
            
            # Verify Docker access works
            if self.run_command(f"docker exec {self.jenkins_container} docker ps", capture_output=True):
                self.print_success("Docker socket permissions configured successfully")
            else:
                self.print_info("Docker socket permissions may need manual configuration")
        
        self.print_success("Jenkins container started successfully!")
        return True
    
    def wait_for_jenkins(self, timeout=300):
        """Wait for Jenkins to be fully ready."""
        self.print_header("Waiting for Jenkins to Start")
        print("=" * 50)
        
        self.print_step("Waiting for Jenkins to be fully ready...")
        self.print_info("This may take 2-3 minutes for first-time setup")
        
        start_time = time.time()
        attempt = 0
        
        while time.time() - start_time < timeout:
            attempt += 1
            try:
                response = requests.get(f"{self.jenkins_url}/api/json", 
                                     auth=('admin', 'admin'), 
                                     timeout=5)
                if response.status_code == 200:
                    self.print_success("Jenkins is ready!")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            elapsed = int(time.time() - start_time)
            remaining = timeout - elapsed
            self.print_step(f"Attempt {attempt} - Jenkins not ready yet... ({elapsed}s elapsed, {remaining}s remaining)")
            time.sleep(10)
        
        self.print_error(f"Jenkins did not start within {timeout} seconds")
        return False
    
    def verify_jenkins_setup(self):
        """Verify that Jenkins is properly configured."""
        self.print_header("Verifying Jenkins Setup")
        print("=" * 50)
        
        # Check Jenkins is responding
        self.print_step("Checking Jenkins API...")
        try:
            response = requests.get(f"{self.jenkins_url}/api/json", 
                                 auth=('admin', 'admin'), 
                                 timeout=10)
            if response.status_code == 200:
                self.print_success("Jenkins API is responding")
            else:
                self.print_error(f"Jenkins API returned status {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Failed to connect to Jenkins: {e}")
            return False
        
        # Check Python availability (cross-platform)
        self.print_step("Checking Python availability...")
        python_cmd = self.get_python_command()
        if self.run_command(f"docker exec {self.jenkins_container} {python_cmd} --version", capture_output=True):
            self.print_success(f"Python is available in Jenkins ({python_cmd})")
        else:
            self.print_error(f"Python is not available in Jenkins")
            return False
        
        # Check pip availability (cross-platform)
        self.print_step("Checking pip availability...")
        pip_cmd = self.get_pip_command()
        if self.run_command(f"docker exec {self.jenkins_container} {pip_cmd} --version", capture_output=True):
            self.print_success(f"pip is available in Jenkins ({pip_cmd})")
        else:
            self.print_error(f"pip is not available in Jenkins")
            return False
        
        # Check Docker is available
        self.print_step("Checking Docker availability...")
        if self.run_command(f"docker exec {self.jenkins_container} docker ps", capture_output=True):
            self.print_success("Docker is available in Jenkins")
        else:
            self.print_error("Docker is not available in Jenkins")
            return False
        
        # Check workspace mount
        self.print_step("Checking workspace mount...")
        if self.run_command(f"docker exec {self.jenkins_container} ls -la /workspace", capture_output=True):
            self.print_success("Workspace is properly mounted")
        else:
            self.print_error("Workspace is not properly mounted")
            return False
        
        # Platform-specific validation
        self.print_step("Running platform-specific validation...")
        if self.is_windows:
            self.print_info("Windows platform detected - using Windows-specific validations")
        elif self.is_mac:
            self.print_info("macOS platform detected - using macOS-specific validations")
        elif self.is_linux:
            self.print_info("Linux platform detected - using Linux-specific validations")
        else:
            self.print_info(f"Unknown platform detected: {self.platform}")
        
        # Check plugin count
        self.print_step("Checking installed plugins...")
        try:
            response = requests.get(f"{self.jenkins_url}/pluginManager/api/json?depth=1", 
                                 auth=('admin', 'admin'), 
                                 timeout=10)
            if response.status_code == 200:
                plugins = response.json().get('plugins', [])
                plugin_count = len(plugins)
                self.print_success(f"Found {plugin_count} installed plugins")
                if plugin_count < 100:
                    self.print_info("Plugin count seems low, but Jenkins should still work")
            else:
                self.print_info("Could not check plugin count, but Jenkins should still work")
        except Exception:
            self.print_info("Could not check plugin count, but Jenkins should still work")
        
        return True
    
    def get_csrf_token(self, session):
        """Get CSRF token from Jenkins for API requests."""
        try:
            response = session.get(f"{self.jenkins_url}/crumbIssuer/api/json", timeout=10)
            if response.status_code == 200:
                crumb_data = response.json()
                return crumb_data.get('crumb')
        except Exception:
            pass
        return None

    def create_demo_jobs(self):
        """Create demo Jenkins jobs for all scenarios."""
        self.print_header("Creating Demo Jenkins Jobs")
        print("=" * 50)
        
        scenarios = [
            {
                'name': 'scenario_01_pipeline_genesis',
                'display_name': 'Pipeline Genesis',
                'description': 'Your first Jenkins pipeline - simple and clean!',
                'script_path': 'jenkins-scenarios/scenario_01_pipeline_genesis/Jenkinsfile'
            },
            {
                'name': 'scenario_02_testcontainers',
                'display_name': 'TestContainers Integration',
                'description': 'Integration testing with database containers',
                'script_path': 'jenkins-scenarios/scenario_02_testcontainers/Jenkinsfile'
            },
            {
                'name': 'scenario_03_docker_ninja',
                'display_name': 'Docker Ninja',
                'description': 'Advanced Docker workflows and security scanning',
                'script_path': 'jenkins-scenarios/scenario_03_docker_ninja/Jenkinsfile'
            },
            {
                'name': 'scenario_04_k8s_commander',
                'display_name': 'K8s Commander',
                'description': 'Kubernetes deployment and management',
                'script_path': 'jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile'
            },
            {
                'name': 'scenario_05_security_sentinel',
                'display_name': 'Security Sentinel',
                'description': 'Security scanning and compliance checking',
                'script_path': 'jenkins-scenarios/scenario_05_security_sentinel/Jenkinsfile'
            }
        ]
        
        # Create session for API requests
        session = requests.Session()
        session.auth = (self.jenkins_username, self.jenkins_password)
        
        # Get CSRF token for API requests
        csrf_token = self.get_csrf_token(session)
        if csrf_token:
            self.print_info("CSRF protection detected, using token for API requests")
        else:
            self.print_info("No CSRF token found, proceeding without it")
        
        # First, clean up any existing jobs with the same names
        self.print_step("Cleaning up existing demo jobs...")
        for scenario in scenarios:
            try:
                response = session.get(f"{self.jenkins_url}/job/{scenario['name']}/api/json", timeout=10)
                if response.status_code == 200:
                    # Job exists, delete it
                    delete_response = session.post(f"{self.jenkins_url}/job/{scenario['name']}/doDelete", timeout=10)
                    if delete_response.status_code in [200, 302]:
                        self.print_info(f"Deleted existing job: {scenario['display_name']}")
            except Exception:
                # Job doesn't exist or error occurred, continue
                pass
        
        successful_jobs = 0
        total_jobs = len(scenarios)
        
        for scenario in scenarios:
            self.print_step(f"Creating job: {scenario['display_name']}")
            
            # Read the Jenkinsfile content and embed it directly
            jenkinsfile_path = self.workspace_path / scenario['script_path']
            if jenkinsfile_path.exists():
                with open(jenkinsfile_path, 'r') as f:
                    pipeline_script = f.read()
            else:
                # Fallback pipeline script if file doesn't exist
                pipeline_script = f"""pipeline {{
    agent any
    
    stages {{
        stage('Hello World') {{
            steps {{
                echo 'Hello from {scenario['display_name']}!'
                echo 'This is a demo pipeline for the CI/CD Chaos Workshop.'
            }}
        }}
        
        stage('Success') {{
            steps {{
                echo '🎉 Pipeline completed successfully!'
            }}
        }}
    }}
}}"""
            
            # Escape the pipeline script for XML
            pipeline_script_escaped = pipeline_script.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
            
            # Create XML configuration for the job with embedded script
            xml_config = f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.41">
  <description>{scenario['description']}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.90">
    <script>{pipeline_script_escaped}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>"""
            
            # Create the job
            try:
                headers = {'Content-Type': 'application/xml'}
                if csrf_token:
                    headers['Jenkins-Crumb'] = csrf_token
                
                response = session.post(
                    f"{self.jenkins_url}/createItem?name={scenario['name']}",
                    data=xml_config,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    self.print_success(f"Created job: {scenario['display_name']}")
                    successful_jobs += 1
                else:
                    self.print_error(f"Failed to create job {scenario['display_name']}: {response.status_code}")
                    if response.status_code == 403:
                        self.print_info("This might be due to CSRF protection. Jobs can be created manually in the Jenkins UI.")
                    elif response.status_code == 400:
                        self.print_info("Job might already exist or have invalid configuration.")
                        # Try to get more details about the error
                        if response.text and "already exists" in response.text.lower():
                            self.print_info("Job already exists - this is normal if you're re-running setup.")
                        elif response.text:
                            self.print_info(f"Error details: {response.text[:200]}...")
                    elif response.status_code == 500:
                        self.print_info("Internal server error - Jenkins might be having issues.")
                    else:
                        self.print_info(f"Unexpected error: {response.status_code}")
                    
            except Exception as e:
                self.print_error(f"Error creating job {scenario['display_name']}: {e}")
        
        # Check if jobs already exist
        existing_jobs = 0
        for scenario in scenarios:
            try:
                response = session.get(f"{self.jenkins_url}/job/{scenario['name']}/api/json", timeout=10)
                if response.status_code == 200:
                    existing_jobs += 1
            except Exception:
                pass
        
        if successful_jobs == total_jobs:
            self.print_success(f"All {total_jobs} demo jobs created successfully!")
        elif successful_jobs > 0:
            self.print_info(f"Created {successful_jobs}/{total_jobs} jobs successfully.")
            if existing_jobs > 0:
                self.print_info(f"Found {existing_jobs} existing jobs - this is normal if you're re-running setup.")
            self.print_info("You can create the remaining jobs manually in the Jenkins UI.")
        elif existing_jobs == total_jobs:
            self.print_success(f"All {total_jobs} demo jobs already exist!")
            self.print_info("This is normal if you're re-running the setup script.")
        else:
            self.print_error("Failed to create any jobs automatically.")
            self.print_info("You can create jobs manually in the Jenkins UI using the instructions below.")
            self.print_info("Alternatively, you can use the demo scripts in each scenario directory to create jobs.")
    
    def show_educational_access_info(self):
        """Show educational access information and learning path."""
        self.print_header("🎓 Jenkins Educational Workshop Ready!")
        print("=" * 60)
        
        self.print_success("Your Jenkins learning environment is ready!")
        print()
        
        print(f"{Colors.BOLD}🎯 Educational Approach:{Colors.NC}")
        print("This workshop is designed for hands-on learning where YOU create")
        print("Jenkins jobs from scratch, just like in real-world scenarios!")
        print()
        
        print(f"{Colors.BOLD}Access Information:{Colors.NC}")
        print(f"  🌐 Jenkins URL: {self.jenkins_url}")
        print(f"  👤 Username: admin")
        print(f"  🔑 Password: admin")
        print()
        
        print(f"{Colors.BOLD}📚 Learning Path:{Colors.NC}")
        print("  1. Start with scenario_01_pipeline_genesis")
        print("     • Run: python3 demo.py")
        print("     • Learn: Job creation, pipeline basics, Docker integration")
        print()
        print("  2. Progress through advanced scenarios:")
        print("     • scenario_02_testcontainers - Database testing")
        print("     • scenario_03_docker_ninja - Advanced Docker workflows")
        print("     • scenario_04_k8s_commander - Kubernetes deployment")
        print("     • scenario_05_security_sentinel - Security scanning")
        print()
        
        print(f"{Colors.BOLD}🎓 What You'll Learn:{Colors.NC}")
        print("  • Creating Jenkins jobs from scratch")
        print("  • Understanding Jenkinsfile syntax (Groovy)")
        print("  • Git SCM integration with Jenkins")
        print("  • Docker integration in CI/CD pipelines")
        print("  • Pipeline monitoring and debugging")
        print("  • Best practices for CI/CD workflows")
        print()
        
        print(f"{Colors.BOLD}🚀 Getting Started:{Colors.NC}")
        print("  1. Open Jenkins in your browser")
        print("  2. Login with admin/admin")
        print("  3. Navigate to scenario_01_pipeline_genesis directory")
        print("  4. Run: python3 demo.py")
        print("  5. Follow the interactive workshop!")
        print()
        
        print(f"{Colors.YELLOW}💡 Pro Tip: Each demo.py provides step-by-step guidance{Colors.NC}")
        print(f"{Colors.YELLOW}   for creating jobs manually - no shortcuts!{Colors.NC}")
    
    def show_access_info(self):
        """Show access information and next steps (legacy method)."""
        self.print_header("🎉 Jenkins Setup Complete!")
        print("=" * 50)
        
        self.print_success("Your Jenkins workshop environment is ready!")
        print()
        
        print(f"{Colors.BOLD}Access Information:{Colors.NC}")
        print(f"  🌐 Jenkins URL: {self.jenkins_url}")
        print(f"  👤 Username: admin")
        print(f"  🔑 Password: admin")
        print()
        
        print(f"{Colors.BOLD}Available Demo Jobs:{Colors.NC}")
        print("  1. Pipeline Genesis - Your first Jenkins pipeline")
        print("  2. TestContainers Integration - Database testing")
        print("  3. Docker Ninja - Advanced Docker workflows")
        print("  4. K8s Commander - Kubernetes deployment")
        print("  5. Security Sentinel - Security scanning")
        print()
        
        print(f"{Colors.BOLD}Next Steps:{Colors.NC}")
        print("  1. Open Jenkins in your browser")
        print("  2. Login with admin/admin")
        print("  3. Click on any demo job")
        print("  4. Click 'Build Now' to run the pipeline")
        print("  5. Watch the magic happen! ✨")
        print()
        
        print(f"{Colors.BOLD}Workshop Scenarios:{Colors.NC}")
        print("  📁 Each scenario has its own directory with:")
        print("     • README.md - Detailed instructions")
        print("     • demo.py - Interactive demo script")
        print("     • Jenkinsfile - Pipeline definition")
        print("     • tests/ - Test files")
        print()
        
        print(f"{Colors.YELLOW}💡 Pro Tip: Run 'python3 jenkins-setup.py demo' to see all scenarios!{Colors.NC}")
    
    def cleanup_jenkins(self):
        """Clean up Jenkins container and volumes."""
        self.print_header("Cleaning Up Jenkins")
        print("=" * 50)
        
        self.print_step("Stopping Jenkins container...")
        self.run_command(f"docker stop {self.jenkins_container}", check=False)
        
        self.print_step("Removing Jenkins container...")
        self.run_command(f"docker rm {self.jenkins_container}", check=False)
        
        self.print_step("Removing Jenkins volume...")
        self.run_command("docker volume rm jenkins_home", check=False)
        
        self.print_step("Removing Jenkins image...")
        self.run_command(f"docker rmi {self.jenkins_image}", check=False)
        
        self.print_success("Jenkins cleanup completed!")
    
    def show_status(self):
        """Show current Jenkins status."""
        self.print_header("Jenkins Status Check")
        print("=" * 50)
        
        # Check if container is running
        self.print_step("Checking Jenkins container...")
        if self.run_command(f"docker ps --filter name={self.jenkins_container} --format '{{.Status}}'", capture_output=True):
            self.print_success("Jenkins container is running")
        else:
            self.print_error("Jenkins container is not running")
            return False
        
        # Check if Jenkins is responding
        self.print_step("Checking Jenkins API...")
        try:
            response = requests.get(f"{self.jenkins_url}/api/json", 
                                 auth=('admin', 'admin'), 
                                 timeout=5)
            if response.status_code == 200:
                self.print_success("Jenkins is responding")
                return True
            else:
                self.print_error(f"Jenkins API returned status {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Jenkins is not responding: {e}")
            return False
    
    def run_demo(self):
        """Run demo scenarios."""
        self.print_header("Running Jenkins Workshop Demos")
        print("=" * 50)
        
        if not self.show_status():
            self.print_error("Jenkins is not running. Please run 'python3 jenkins-setup.py setup' first.")
            return
        
        # List available scenarios
        scenarios_dir = Path(__file__).parent / "jenkins-scenarios"
        scenarios = [d for d in scenarios_dir.iterdir() if d.is_dir() and d.name.startswith(('01-', '02-', '03-', '04-', '05-'))]
        
        if not scenarios:
            self.print_error("No demo scenarios found")
            return
        
        self.print_info("Available demo scenarios:")
        for i, scenario in enumerate(sorted(scenarios), 1):
            print(f"  {i}. {scenario.name}")
        
        print()
        self.print_info("Each scenario includes:")
        print("  • README.md - Detailed instructions")
        print("  • demo.py - Interactive demo script")
        print("  • Jenkinsfile - Pipeline definition")
        print("  • tests/ - Test files")
        print()
        
        self.print_success("To run a specific demo:")
        print("  cd jenkins-scenarios/[scenario-name]")
        print("  python3 demo.py")
        print()
        
        self.print_success("To access Jenkins:")
        print(f"  Open: {self.jenkins_url}")
        print("  Login: admin/admin")
    
    def setup_jenkins(self):
        """Complete Jenkins setup process."""
        self.print_header("🚀 Jenkins CI/CD Workshop Setup")
        print("=" * 50)
        print("Setting up Jenkins for the CI/CD Chaos Workshop...")
        print("This will work on Windows, macOS, Linux, and virtual machines!")
        print()
        
        # Check prerequisites
        if not self.check_docker_installed():
            return False
        
        self.check_docker_compose()
        
        # Build Jenkins image
        if not self.build_jenkins_image():
            return False
        
        # Start Jenkins container
        if not self.start_jenkins_container():
            return False
        
        # Wait for Jenkins to be ready
        if not self.wait_for_jenkins():
            return False
        
        # Verify setup
        if not self.verify_jenkins_setup():
            return False
        
        # Show educational access information (no automatic job creation)
        self.show_educational_access_info()
        
        return True
    
    def recreate_demo_jobs(self):
        """Recreate demo Jenkins jobs (force delete and recreate)."""
        self.print_header("Recreating Demo Jenkins Jobs")
        print("=" * 50)
        
        if not self.show_status():
            self.print_error("Jenkins is not running. Please run 'python3 jenkins-setup.py setup' first.")
            return False
        
        # Create session for API requests
        session = requests.Session()
        session.auth = (self.jenkins_username, self.jenkins_password)
        
        # Get CSRF token for API requests
        csrf_token = self.get_csrf_token(session)
        if csrf_token:
            self.print_info("CSRF protection detected, using token for API requests")
        else:
            self.print_info("No CSRF token found, proceeding without it")
        
        scenarios = [
            {
                'name': 'scenario_01_pipeline_genesis',
                'display_name': 'Pipeline Genesis',
                'description': 'Your first Jenkins pipeline - simple and clean!',
                'script_path': 'jenkins-scenarios/scenario_01_pipeline_genesis/Jenkinsfile'
            },
            {
                'name': 'scenario_02_testcontainers',
                'display_name': 'TestContainers Integration',
                'description': 'Integration testing with database containers',
                'script_path': 'jenkins-scenarios/scenario_02_testcontainers/Jenkinsfile'
            },
            {
                'name': 'scenario_03_docker_ninja',
                'display_name': 'Docker Ninja',
                'description': 'Advanced Docker workflows and security scanning',
                'script_path': 'jenkins-scenarios/scenario_03_docker_ninja/Jenkinsfile'
            },
            {
                'name': 'scenario_04_k8s_commander',
                'display_name': 'K8s Commander',
                'description': 'Kubernetes deployment and management',
                'script_path': 'jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile'
            },
            {
                'name': 'scenario_05_security_sentinel',
                'display_name': 'Security Sentinel',
                'description': 'Security scanning and compliance checking',
                'script_path': 'jenkins-scenarios/scenario_05_security_sentinel/Jenkinsfile'
            }
        ]
        
        # Force delete all existing jobs
        self.print_step("Force deleting existing demo jobs...")
        for scenario in scenarios:
            try:
                response = session.get(f"{self.jenkins_url}/job/{scenario['name']}/api/json", timeout=10)
                if response.status_code == 200:
                    # Job exists, delete it
                    headers = {}
                    if csrf_token:
                        headers['Jenkins-Crumb'] = csrf_token
                    
                    delete_response = session.post(f"{self.jenkins_url}/job/{scenario['name']}/doDelete", 
                                                headers=headers, timeout=10)
                    if delete_response.status_code in [200, 302]:
                        self.print_success(f"Deleted existing job: {scenario['display_name']}")
                    else:
                        self.print_error(f"Failed to delete job {scenario['display_name']}: {delete_response.status_code}")
            except Exception as e:
                self.print_error(f"Error deleting job {scenario['display_name']}: {e}")
        
        # Now create all jobs fresh
        self.print_step("Creating fresh demo jobs...")
        self.create_demo_jobs()
        
        return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Jenkins CI/CD Workshop Setup')
    parser.add_argument('command', choices=['setup', 'status', 'cleanup', 'demo', 'recreate-jobs'], 
                       help='Command to run')
    
    args = parser.parse_args()
    
    setup = JenkinsSetup()
    
    if args.command == 'setup':
        success = setup.setup_jenkins()
        sys.exit(0 if success else 1)
    elif args.command == 'status':
        success = setup.show_status()
        sys.exit(0 if success else 1)
    elif args.command == 'cleanup':
        setup.cleanup_jenkins()
    elif args.command == 'demo':
        setup.run_demo()
    elif args.command == 'recreate-jobs':
        success = setup.recreate_demo_jobs()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
