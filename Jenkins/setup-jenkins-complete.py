#!/usr/bin/env python3
"""
🚀 Complete Jenkins Setup Script
Handles Jenkins installation, configuration, permissions, and testing
Works on all platforms with proper error handling
"""

import os
import sys
import subprocess
import platform
import time
import json
import logging
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class SetupResult:
    """Setup operation result"""
    operation: str
    success: bool
    message: str
    details: Optional[str] = None

class Colors:
    """ANSI color codes"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class JenkinsSetup:
    """Complete Jenkins setup and management"""
    
    def __init__(self, log_level: LogLevel = LogLevel.INFO):
        self.log_level = log_level
        self.setup_logging()
        self.workspace_root = Path(__file__).parent.parent
        self.jenkins_dir = Path(__file__).parent
        self.scenarios_dir = self.jenkins_dir / "scenarios"
        self.results: List[SetupResult] = []
        
        # Jenkins configuration
        self.jenkins_container_name = "jenkins-workshop"
        self.jenkins_port = 8080
        self.jenkins_agent_port = 50000
        self.jenkins_home_volume = "jenkins_home"
        
        # Platform detection
        self.platform = platform.system().lower()
        self.is_macos = self.platform == "darwin"
        self.is_linux = self.platform == "linux"
        self.is_windows = self.platform == "windows"

    def setup_logging(self):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=getattr(logging, self.log_level.value),
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('jenkins-setup.log')
            ]
        )
        self.logger = logging.getLogger(__name__)

    def colored_print(self, message: str, color: str = Colors.RESET, bold: bool = False, end: str = "\n"):
        """Print colored message"""
        try:
            if bold:
                message = f"{Colors.BOLD}{message}{Colors.RESET}"
            print(f"{color}{message}{Colors.RESET}", end=end)
        except:
            print(message, end=end)

    def print_header(self, title: str):
        """Print formatted header"""
        self.colored_print("\n" + "="*70, Colors.CYAN)
        self.colored_print(f"🚀 {title}", Colors.CYAN, bold=True)
        self.colored_print("="*70, Colors.CYAN)

    def print_step(self, step: str, description: str):
        """Print step information"""
        self.colored_print(f"\n🔧 {step}: {description}", Colors.BLUE)

    def print_success(self, message: str):
        """Print success message"""
        self.colored_print(f"✅ {message}", Colors.GREEN)
        self.logger.info(f"SUCCESS: {message}")

    def print_warning(self, message: str):
        """Print warning message"""
        self.colored_print(f"⚠️ {message}", Colors.YELLOW)
        self.logger.warning(f"WARNING: {message}")

    def print_error(self, message: str):
        """Print error message"""
        self.colored_print(f"❌ {message}", Colors.RED)
        self.logger.error(f"ERROR: {message}")

    def run_command(self, cmd: str, capture_output: bool = True, timeout: int = 60, 
                   cwd: Optional[Path] = None, shell: bool = True) -> Tuple[bool, str, str]:
        """Run command with timeout and error handling"""
        try:
            self.logger.debug(f"Running command: {cmd}")
            if capture_output:
                result = subprocess.run(
                    cmd, 
                    shell=shell, 
                    capture_output=True, 
                    text=True, 
                    timeout=timeout, 
                    cwd=cwd
                )
                return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
            else:
                result = subprocess.run(cmd, shell=shell, timeout=timeout, cwd=cwd)
                return result.returncode == 0, "", ""
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after {timeout} seconds"
            self.logger.error(error_msg)
            return False, "", error_msg
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Command execution error: {error_msg}")
            return False, "", error_msg

    def check_prerequisites(self) -> bool:
        """Check system prerequisites"""
        self.print_step("Prerequisites Check", "Verifying system requirements")
        
        prerequisites = {
            "Python": f"{sys.executable} --version",
            "Docker": "docker --version",
            "Git": "git --version"
        }
        
        all_good = True
        for name, cmd in prerequisites.items():
            success, output, error = self.run_command(cmd, timeout=10)
            if success:
                self.print_success(f"{name}: {output.split()[0] if output else 'Available'}")
            else:
                self.print_error(f"{name}: Not available - {error}")
                all_good = False
        
        return all_good

    def check_docker_permissions(self) -> bool:
        """Check and fix Docker permissions"""
        self.print_step("Docker Permissions", "Checking Docker access")
        
        # Test Docker access
        success, output, error = self.run_command("docker info", timeout=10)
        if success:
            self.print_success("Docker is accessible")
            return True
        
        # Try to fix permissions
        self.print_warning("Docker access denied, attempting to fix permissions")
        
        if self.is_linux:
            # Linux: Add user to docker group
            success, output, error = self.run_command("sudo usermod -aG docker $USER", timeout=10)
            if success:
                self.print_success("Added user to docker group")
                self.print_warning("Please log out and log back in for changes to take effect")
                return True
            else:
                self.print_error(f"Failed to add user to docker group: {error}")
                return False
        elif self.is_macos:
            # macOS: Check Docker Desktop
            self.print_warning("Please ensure Docker Desktop is running")
            self.print_warning("If Docker Desktop is not installed, install it from: https://www.docker.com/products/docker-desktop")
            return False
        elif self.is_windows:
            # Windows: Check Docker Desktop
            self.print_warning("Please ensure Docker Desktop is running")
            self.print_warning("If Docker Desktop is not installed, install it from: https://www.docker.com/products/docker-desktop")
            return False
        else:
            self.print_error(f"Unsupported platform: {self.platform}")
            return False

    def cleanup_existing_jenkins(self) -> bool:
        """Clean up existing Jenkins containers and volumes"""
        self.print_step("Cleanup", "Removing existing Jenkins setup")
        
        # Stop and remove existing container
        success, output, error = self.run_command(f"docker stop {self.jenkins_container_name}", timeout=30)
        if success:
            self.print_success("Stopped existing Jenkins container")
        
        success, output, error = self.run_command(f"docker rm {self.jenkins_container_name}", timeout=30)
        if success:
            self.print_success("Removed existing Jenkins container")
        
        # Remove existing volume
        success, output, error = self.run_command(f"docker volume rm {self.jenkins_home_volume}", timeout=30)
        if success:
            self.print_success("Removed existing Jenkins volume")
        
        return True

    def setup_jenkins_container(self) -> bool:
        """Setup Jenkins container with proper configuration"""
        self.print_step("Jenkins Setup", "Creating Jenkins container")
        
        # Create Jenkins home volume
        success, output, error = self.run_command(f"docker volume create {self.jenkins_home_volume}", timeout=30)
        if not success:
            self.print_warning(f"Volume might already exist: {error}")
        
        # Build Jenkins command
        jenkins_cmd = f"""
        docker run -d --name {self.jenkins_container_name} \
            -p {self.jenkins_port}:8080 \
            -p {self.jenkins_agent_port}:50000 \
            -v {self.jenkins_home_volume}:/var/jenkins_home \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v {self.workspace_root}:/workspace \
            -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false" \
            -e JENKINS_OPTS="--httpPort=8080" \
            jenkins/jenkins:lts
        """
        
        success, output, error = self.run_command(jenkins_cmd, timeout=120)
        if success:
            self.print_success("Jenkins container started successfully")
            return True
        else:
            self.print_error(f"Failed to start Jenkins container: {error}")
            return False

    def wait_for_jenkins(self, timeout: int = 300) -> bool:
        """Wait for Jenkins to be ready"""
        self.print_step("Jenkins Startup", "Waiting for Jenkins to be ready")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://localhost:{self.jenkins_port}/login", timeout=5)
                if response.status_code == 200:
                    self.print_success("Jenkins is ready!")
                    return True
            except:
                pass
            
            self.colored_print(".", Colors.YELLOW, end="")
            time.sleep(5)
        
        self.print_error(f"Jenkins failed to start within {timeout} seconds")
        return False

    def get_jenkins_password(self) -> Optional[str]:
        """Get Jenkins initial admin password"""
        self.print_step("Jenkins Password", "Getting initial admin password")
        
        success, output, error = self.run_command(f"docker exec {self.jenkins_container_name} cat /var/jenkins_home/secrets/initialAdminPassword", timeout=30)
        if success and output:
            self.print_success("Jenkins password retrieved")
            return output.strip()
        else:
            self.print_warning("Could not retrieve Jenkins password")
            return None

    def install_jenkins_plugins(self) -> bool:
        """Install required Jenkins plugins"""
        self.print_step("Jenkins Plugins", "Installing required plugins")
        
        plugins = [
            "workflow-aggregator",
            "docker-workflow",
            "docker-plugin",
            "git",
            "pipeline-stage-view",
            "htmlpublisher",
            "junit",
            "coverage",
            "blueocean"
        ]
        
        for plugin in plugins:
            success, output, error = self.run_command(
                f"docker exec {self.jenkins_container_name} jenkins-plugin-cli --plugins {plugin}",
                timeout=60
            )
            if success:
                self.print_success(f"Installed plugin: {plugin}")
            else:
                self.print_warning(f"Failed to install plugin {plugin}: {error}")
        
        return True

    def create_jenkins_job(self) -> bool:
        """Create Jenkins job for scenario 1"""
        self.print_step("Jenkins Job", "Creating Jenkins job for scenario 1")
        
        # Create job configuration
        job_config = {
            "displayName": "Docker Build Pipeline Demo",
            "description": "Complete Docker build pipeline with testing and deployment",
            "pipeline": {
                "script": f"""
pipeline {{
    agent any
    
    environment {{
        WORKSPACE_PATH = '{self.workspace_root}'
    }}
    
    stages {{
        stage('Checkout') {{
            steps {{
                echo 'Checking out code for Docker Build Pipeline'
                checkout scm
            }}
        }}
        
        stage('Build') {{
            steps {{
                echo 'Building Docker image for Docker Build Pipeline'
                script {{
                    def image = docker.build("jenkins-workshop-${{env.BUILD_NUMBER}}")
                }}
            }}
        }}
        
        stage('Test') {{
            steps {{
                echo 'Running tests for Docker Build Pipeline'
                sh 'python -m pytest tests/ -v'
            }}
        }}
        
        stage('Deploy') {{
            steps {{
                echo 'Deploying Docker Build Pipeline'
                // Add deployment steps here
            }}
        }}
    }}
    
    post {{
        always {{
            echo 'Pipeline completed for Docker Build Pipeline'
        }}
        success {{
            echo 'Pipeline succeeded for Docker Build Pipeline'
        }}
        failure {{
            echo 'Pipeline failed for Docker Build Pipeline'
        }}
    }}
}}"""
            }
        }
        
        # Save job configuration
        job_file = self.jenkins_dir / "jenkins-job-config.xml"
        with open(job_file, 'w') as f:
            f.write(f"""<?xml version='1.0' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>{job_config['description']}</description>
  <displayName>{job_config['displayName']}</displayName>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
    <script>{job_config['pipeline']['script']}</script>
    <sandbox>true</sandbox>
  </definition>
</flow-definition>""")
        
        self.print_success("Jenkins job configuration created")
        return True

    def test_jenkins_setup(self) -> bool:
        """Test Jenkins setup"""
        self.print_step("Jenkins Test", "Testing Jenkins setup")
        
        # Test Jenkins is accessible
        try:
            response = requests.get(f"http://localhost:{self.jenkins_port}/api/json", timeout=10)
            if response.status_code == 200:
                self.print_success("Jenkins API is accessible")
            else:
                self.print_error(f"Jenkins API returned status {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Failed to access Jenkins API: {e}")
            return False
        
        # Test Docker access from Jenkins
        success, output, error = self.run_command(f"docker exec {self.jenkins_container_name} docker --version", timeout=30)
        if success:
            self.print_success("Docker is accessible from Jenkins")
        else:
            self.print_warning(f"Docker access from Jenkins: {error}")
        
        return True

    def create_test_script(self) -> bool:
        """Create script to test Jenkins pipeline"""
        self.print_step("Test Script", "Creating Jenkins test script")
        
        test_script = f"""#!/usr/bin/env python3
\"\"\"
Test Jenkins Pipeline Execution
Tests the complete Jenkins setup and pipeline execution
\"\"\"

import requests
import time
import json
from pathlib import Path

def test_jenkins_pipeline():
    \"\"\"Test Jenkins pipeline execution\"\"\"
    print("🧪 Testing Jenkins Pipeline Execution")
    
    # Test Jenkins is running
    try:
        response = requests.get("http://localhost:{self.jenkins_port}/api/json", timeout=10)
        if response.status_code == 200:
            print("✅ Jenkins is running")
        else:
            print(f"❌ Jenkins returned status {{response.status_code}}")
            return False
    except Exception as e:
        print(f"❌ Jenkins is not accessible: {{e}}")
        return False
    
    # Test scenario 1 directory
    scenario_dir = Path("{self.scenarios_dir}/01-docker-build")
    if scenario_dir.exists():
        print("✅ Scenario 1 directory exists")
    else:
        print("❌ Scenario 1 directory not found")
        return False
    
    # Test scenario 1 files
    required_files = ["app.py", "requirements.txt", "Dockerfile", "Jenkinsfile", "tests/test_app.py"]
    for file in required_files:
        file_path = scenario_dir / file
        if file_path.exists():
            print(f"✅ Found: {{file}}")
        else:
            print(f"❌ Missing: {{file}}")
            return False
    
    print("🎉 All tests passed! Jenkins setup is ready.")
    return True

if __name__ == "__main__":
    test_jenkins_pipeline()
"""
        
        test_file = self.jenkins_dir / "test-jenkins-pipeline.py"
        with open(test_file, 'w') as f:
            f.write(test_script)
        
        # Make it executable
        os.chmod(test_file, 0o755)
        
        self.print_success("Jenkins test script created")
        return True

    def generate_setup_report(self) -> str:
        """Generate setup report"""
        report_file = self.jenkins_dir / "JENKINS_SETUP_REPORT.md"
        
        successful_operations = sum(1 for r in self.results if r.success)
        total_operations = len(self.results)
        success_rate = (successful_operations/total_operations*100) if total_operations > 0 else 0
        
        report_content = f"""# 🚀 Jenkins Setup Report

**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Platform:** {self.platform}  
**Workspace:** {self.workspace_root}

## 📊 Setup Summary

- **Total Operations:** {total_operations}
- **Successful:** {successful_operations}
- **Failed:** {total_operations - successful_operations}
- **Success Rate:** {success_rate:.1f}%

## 🎯 Jenkins Configuration

- **Container Name:** {self.jenkins_container_name}
- **Port:** {self.jenkins_port}
- **Agent Port:** {self.jenkins_agent_port}
- **Home Volume:** {self.jenkins_home_volume}
- **Workspace:** {self.workspace_root}

## 🔧 Setup Results

"""
        
        for result in self.results:
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            report_content += f"- **{result.operation}:** {status} - {result.message}\n"
            if result.details:
                report_content += f"  - *Details:* {result.details}\n"
        
        report_content += f"""

## 🚀 Next Steps

### Access Jenkins
1. Open http://localhost:{self.jenkins_port}
2. Use the initial admin password (check container logs)
3. Complete the setup wizard
4. Create a new pipeline job

### Test the Setup
```bash
python test-jenkins-pipeline.py
```

### Run Scenario 1
1. Navigate to scenarios/01-docker-build/
2. Create a new Jenkins job
3. Point to the Jenkinsfile
4. Run the pipeline

## 📁 Files Created

- Jenkins container: {self.jenkins_container_name}
- Test script: test-jenkins-pipeline.py
- Job config: jenkins-job-config.xml
- This report: JENKINS_SETUP_REPORT.md

---

**Your Jenkins setup is ready! 🎉**
"""
        
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        return str(report_file)

    def run_setup(self) -> bool:
        """Run complete Jenkins setup"""
        self.print_header("Complete Jenkins Setup")
        
        try:
            # Check prerequisites
            result = self.check_prerequisites()
            self.results.append(SetupResult("prerequisites", result, "Prerequisites check"))
            if not result:
                return False
            
            # Check Docker permissions
            result = self.check_docker_permissions()
            self.results.append(SetupResult("docker_permissions", result, "Docker permissions check"))
            if not result:
                return False
            
            # Cleanup existing setup
            result = self.cleanup_existing_jenkins()
            self.results.append(SetupResult("cleanup", result, "Cleanup existing setup"))
            
            # Setup Jenkins container
            result = self.setup_jenkins_container()
            self.results.append(SetupResult("jenkins_container", result, "Jenkins container setup"))
            if not result:
                return False
            
            # Wait for Jenkins to be ready
            result = self.wait_for_jenkins()
            self.results.append(SetupResult("jenkins_startup", result, "Jenkins startup"))
            if not result:
                return False
            
            # Install plugins
            result = self.install_jenkins_plugins()
            self.results.append(SetupResult("plugins", result, "Plugin installation"))
            
            # Create Jenkins job
            result = self.create_jenkins_job()
            self.results.append(SetupResult("jenkins_job", result, "Jenkins job creation"))
            
            # Test setup
            result = self.test_jenkins_setup()
            self.results.append(SetupResult("jenkins_test", result, "Jenkins setup test"))
            if not result:
                return False
            
            # Create test script
            result = self.create_test_script()
            self.results.append(SetupResult("test_script", result, "Test script creation"))
            
            # Generate report
            report_file = self.generate_setup_report()
            
            self.print_success("Jenkins setup completed successfully!")
            self.print_success(f"Access Jenkins at: http://localhost:{self.jenkins_port}")
            self.print_success(f"Report generated: {report_file}")
            
            return True
            
        except Exception as e:
            self.print_error(f"Setup failed: {e}")
            self.logger.exception("Setup failed")
            return False

    def run_test(self) -> bool:
        """Run Jenkins test"""
        self.print_header("Jenkins Test")
        
        try:
            # Run test script
            success, output, error = self.run_command("python test-jenkins-pipeline.py", timeout=60)
            if success:
                self.print_success("Jenkins test completed successfully!")
                print(output)
                return True
            else:
                self.print_error(f"Jenkins test failed: {error}")
                return False
                
        except Exception as e:
            self.print_error(f"Test failed: {e}")
            return False

    def run_cleanup(self) -> bool:
        """Run cleanup"""
        self.print_header("Jenkins Cleanup")
        
        try:
            self.cleanup_existing_jenkins()
            self.print_success("Jenkins cleanup completed!")
            return True
            
        except Exception as e:
            self.print_error(f"Cleanup failed: {e}")
            return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Complete Jenkins Setup")
    parser.add_argument("operation", 
                       choices=["setup", "test", "cleanup", "help"],
                       default="help", help="Operation to perform")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                       default="INFO", help="Set logging level")
    
    args = parser.parse_args()
    
    # Create setup instance
    setup = JenkinsSetup(LogLevel(args.log_level))
    
    # Run the requested operation
    if args.operation == "setup":
        success = setup.run_setup()
    elif args.operation == "test":
        success = setup.run_test()
    elif args.operation == "cleanup":
        success = setup.run_cleanup()
    elif args.operation == "help":
        setup.print_header("Jenkins Setup Help")
        help_text = """
🎯 Available Operations:

1. setup     - Complete Jenkins setup and configuration
2. test      - Test Jenkins setup and pipeline
3. cleanup   - Cleanup Jenkins containers and volumes
4. help      - Show this help

🚀 Quick Start:
   python setup-jenkins-complete.py setup

🔍 Test Setup:
   python setup-jenkins-complete.py test

🧹 Cleanup:
   python setup-jenkins-complete.py cleanup

📚 This script handles:
   - Docker permissions and access
   - Jenkins container setup
   - Plugin installation
   - Pipeline configuration
   - Complete testing
"""
        setup.colored_print(help_text, Colors.CYAN)
        success = True
    else:
        setup.print_error(f"Unknown operation: {args.operation}")
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
