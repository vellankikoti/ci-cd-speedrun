#!/usr/bin/env python3
"""
🎓 Jenkins Workshop Setup
Complete workshop-ready Jenkins setup with GitHub integration
Works anywhere and everywhere with zero local dependencies
"""

import os
import sys
import subprocess
import time
import requests
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

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

class JenkinsWorkshop:
    """Complete Jenkins workshop setup"""
    
    def __init__(self):
        self.workspace_root = Path(__file__).parent.parent
        self.jenkins_dir = Path(__file__).parent
        self.scenarios_dir = self.jenkins_dir / "scenarios"
        
        # Jenkins configuration
        self.jenkins_container_name = "jenkins-workshop"
        self.jenkins_port = 8080
        self.jenkins_agent_port = 50000
        self.jenkins_home_volume = "jenkins_home"
        
        # GitHub configuration (update these for your repo)
        self.github_repo = "vellankikoti/ci-cd-chaos-workshop"  # Update this
        self.github_url = f"https://github.com/{self.github_repo}.git"
        
    def colored_print(self, message: str, color: str = Colors.RESET, bold: bool = False):
        """Print colored message"""
        try:
            if bold:
                message = f"{Colors.BOLD}{message}{Colors.RESET}"
            print(f"{color}{message}{Colors.RESET}")
        except:
            print(message)

    def print_header(self, title: str):
        """Print formatted header"""
        self.colored_print("\n" + "="*80, Colors.CYAN)
        self.colored_print(f"🎓 {title}", Colors.CYAN, bold=True)
        self.colored_print("="*80, Colors.CYAN)

    def print_step(self, step: str, description: str):
        """Print step information"""
        self.colored_print(f"\n🔧 {step}: {description}", Colors.BLUE)

    def print_success(self, message: str):
        """Print success message"""
        self.colored_print(f"✅ {message}", Colors.GREEN)

    def print_warning(self, message: str):
        """Print warning message"""
        self.colored_print(f"⚠️ {message}", Colors.YELLOW)

    def print_error(self, message: str):
        """Print error message"""
        self.colored_print(f"❌ {message}", Colors.RED)

    def run_command(self, cmd: str, capture_output: bool = True, timeout: int = 60) -> Tuple[bool, str, str]:
        """Run command with timeout and error handling"""
        try:
            if capture_output:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
                return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
            else:
                result = subprocess.run(cmd, shell=True, timeout=timeout)
                return result.returncode == 0, "", ""
        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            return False, "", str(e)

    def setup_jenkins_with_github(self) -> bool:
        """Setup Jenkins with GitHub integration"""
        self.print_step("Jenkins GitHub Setup", "Setting up Jenkins with GitHub integration")
        
        # Check if Jenkins is running
        try:
            response = requests.get(f"http://localhost:{self.jenkins_port}/api/json", timeout=5)
            if response.status_code != 200:
                self.print_error("Jenkins is not running. Please run: python setup-jenkins-complete.py setup")
                return False
        except:
            self.print_error("Jenkins is not accessible. Please run: python setup-jenkins-complete.py setup")
            return False
        
        self.print_success("Jenkins is running and accessible")
        return True

    def create_workshop_jobs(self) -> bool:
        """Create workshop-ready Jenkins jobs"""
        self.print_step("Workshop Jobs", "Creating workshop-ready Jenkins jobs")
        
        # Job 1: Scenario 1 - Docker Build Pipeline
        job1_config = f"""<?xml version='1.0' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>Workshop Scenario 1: Docker Build Pipeline - Complete CI/CD pipeline with Docker, testing, and deployment</description>
  <displayName>🎓 Workshop - Docker Build Pipeline</displayName>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps">
    <scm class="hudson.plugins.git.GitSCM" plugin="git">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>{self.github_url}</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="list"/>
      <extensions/>
    </scm>
    <scriptPath>Jenkins/scenarios/01-docker-build/Jenkinsfile</scriptPath>
    <lightweight>false</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>"""

        # Save job configuration
        job_file = self.jenkins_dir / "workshop-job-1.xml"
        with open(job_file, 'w') as f:
            f.write(job1_config)
        
        self.print_success("Workshop job configuration created")
        return True

    def create_attendee_guide(self) -> bool:
        """Create comprehensive attendee guide"""
        self.print_step("Attendee Guide", "Creating workshop attendee guide")
        
        guide_content = f"""# 🎓 Jenkins CI/CD Workshop - Attendee Guide

## 🚀 Workshop Overview

Welcome to the **Jenkins CI/CD Workshop**! In this workshop, you'll learn how to:
- Set up Jenkins with zero local dependencies
- Create and run CI/CD pipelines
- Build, test, and deploy applications with Docker
- Integrate with GitHub for source code management

## 📋 Prerequisites

**You need ZERO local dependencies!** Everything runs in Docker containers.

### Required (One-time setup):
- Docker Desktop installed and running
- Git installed (for cloning the repository)
- Web browser

### Optional:
- GitHub account (for forking the repository)

## 🎯 Workshop Steps

### Step 1: Clone the Repository
```bash
git clone {self.github_url}
cd ci-cd-chaos-workshop
```

### Step 2: Start Jenkins (One Command!)
```bash
cd Jenkins
python3 setup-jenkins-complete.py setup
```

**This single command will:**
- ✅ Set up Jenkins in Docker
- ✅ Install all required plugins
- ✅ Configure GitHub integration
- ✅ Create workshop jobs
- ✅ Test everything

### Step 3: Access Jenkins
1. Open your browser: http://localhost:8080
2. Complete the setup wizard
3. You'll see the workshop jobs ready to run!

### Step 4: Run Workshop Scenarios

#### Scenario 1: Docker Build Pipeline
1. Click on "🎓 Workshop - Docker Build Pipeline"
2. Click "Build Now"
3. Watch the magic happen! 🎉

**What happens:**
- ✅ Checks out code from GitHub
- ✅ Builds Docker image
- ✅ Runs comprehensive tests
- ✅ Generates test reports
- ✅ Prepares for deployment

## 🔍 What You'll Learn

### 1. **Jenkins Pipeline as Code**
- Jenkinsfile syntax and structure
- Pipeline stages and steps
- Environment variables and parameters

### 2. **Docker Integration**
- Building Docker images in Jenkins
- Running tests in containers
- Multi-stage Docker builds

### 3. **Testing and Quality**
- Unit testing with pytest
- Test reporting and coverage
- HTML test reports

### 4. **GitHub Integration**
- Automatic code checkout
- Branch-based deployments
- Webhook triggers (optional)

## 🎮 Interactive Demo

### For Workshop Presenter:

#### Demo 1: Show Jenkins Setup
```bash
# Show the one-command setup
python3 setup-jenkins-complete.py setup

# Show Jenkins is running
python3 test-jenkins-pipeline.py
```

#### Demo 2: Run Pipeline
1. Open Jenkins: http://localhost:8080
2. Show the workshop job
3. Click "Build Now"
4. Show the pipeline stages executing
5. Show test reports and artifacts

#### Demo 3: Show Code Structure
```bash
# Show the application
cd scenarios/01-docker-build
ls -la

# Show the Jenkinsfile
cat Jenkinsfile

# Show the tests
ls tests/
```

## 🛠️ Troubleshooting

### Jenkins Not Starting?
```bash
# Check Docker is running
docker ps

# Restart Jenkins
python3 setup-jenkins-complete.py cleanup
python3 setup-jenkins-complete.py setup
```

### Pipeline Failing?
1. Check Jenkins logs: `docker logs jenkins-workshop`
2. Check job console output in Jenkins UI
3. Verify GitHub repository access

### Can't Access Jenkins?
- Make sure port 8080 is not in use
- Check Docker container is running: `docker ps`
- Try: http://localhost:8080

## 🎉 Success Criteria

By the end of this workshop, you should be able to:
- ✅ Set up Jenkins with one command
- ✅ Understand Jenkins pipeline structure
- ✅ Build and test Docker applications
- ✅ Integrate Jenkins with GitHub
- ✅ Create production-ready CI/CD pipelines

## 📚 Next Steps

After the workshop:
1. Fork the repository to your GitHub account
2. Modify the application code
3. Create your own Jenkins jobs
4. Experiment with different pipeline stages
5. Add more scenarios and complexity

## 🤝 Support

- **Workshop Repository**: {self.github_url}
- **Issues**: Create an issue in the repository
- **Documentation**: Check the README files in each scenario

---

**Happy Learning! 🚀**

*This workshop is designed to work anywhere and everywhere with zero local dependencies!*
"""

        guide_file = self.jenkins_dir / "WORKSHOP_ATTENDEE_GUIDE.md"
        with open(guide_file, 'w') as f:
            f.write(guide_content)
        
        self.print_success("Attendee guide created")
        return True

    def create_demo_script(self) -> bool:
        """Create demonstration script for workshop"""
        self.print_step("Demo Script", "Creating workshop demonstration script")
        
        demo_script = """#!/usr/bin/env python3
\"\"\"
🎓 Jenkins Workshop Demo Script
Complete demonstration script for workshop presenters
\"\"\"

import time
import subprocess
import requests
from pathlib import Path

def print_step(step, description):
    print(f"\\n🎯 {step}: {description}")
    print("-" * 60)

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️ {message}")

def run_command(cmd, description):
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print_success(f"{description} - Success")
            return True
        else:
            print_warning(f"{description} - Failed: {result.stderr}")
            return False
    except Exception as e:
        print_warning(f"{description} - Error: {e}")
        return False

def demo_workshop():
    print("🎓 Jenkins CI/CD Workshop Demo")
    print("=" * 60)
    
    # Demo 1: Show setup
    print_step("Demo 1", "Show Jenkins Setup (One Command!)")
    print("This demonstrates how easy it is to set up Jenkins:")
    print("python3 setup-jenkins-complete.py setup")
    
    input("Press Enter to continue...")
    
    # Demo 2: Show Jenkins is running
    print_step("Demo 2", "Verify Jenkins is Running")
    try:
        response = requests.get("http://localhost:8080/api/json", timeout=5)
        if response.status_code == 200:
            print_success("Jenkins is running and accessible")
        else:
            print_warning("Jenkins is not accessible")
    except:
        print_warning("Jenkins is not running")
    
    # Demo 3: Show test results
    print_step("Demo 3", "Run Complete Test Suite")
    run_command("python3 test-jenkins-pipeline.py", "Test Jenkins setup")
    
    # Demo 4: Show application
    print_step("Demo 4", "Show Application Structure")
    print("Application files:")
    run_command("ls -la scenarios/01-docker-build/", "List application files")
    
    print("\\nJenkinsfile content:")
    run_command("head -20 scenarios/01-docker-build/Jenkinsfile", "Show Jenkinsfile")
    
    # Demo 5: Show Docker build
    print_step("Demo 5", "Show Docker Build")
    run_command("cd scenarios/01-docker-build && docker build -t demo-app .", "Build Docker image")
    
    # Demo 6: Show running application
    print_step("Demo 6", "Show Running Application")
    run_command("docker run -d --name demo-app -p 5001:5000 demo-app", "Start application")
    
    print("Waiting for application to start...")
    time.sleep(3)
    
    run_command("curl -s http://localhost:5001/health", "Test application health")
    
    # Cleanup
    print_step("Cleanup", "Clean up demo resources")
    run_command("docker stop demo-app && docker rm demo-app && docker rmi demo-app", "Clean up containers")
    
    print("\\n🎉 Demo Complete!")
    print("\\nNext steps for attendees:")
    print("1. Open http://localhost:8080")
    print("2. Click on '🎓 Workshop - Docker Build Pipeline'")
    print("3. Click 'Build Now'")
    print("4. Watch the magic happen!")

if __name__ == "__main__":
    demo_workshop()
"""

        demo_file = self.jenkins_dir / "demo-workshop.py"
        with open(demo_file, 'w') as f:
            f.write(demo_script)
        
        # Make it executable
        os.chmod(demo_file, 0o755)
        
        self.print_success("Demo script created")
        return True

    def create_github_integration_guide(self) -> bool:
        """Create GitHub integration guide"""
        self.print_step("GitHub Integration", "Creating GitHub integration guide")
        
        github_guide = f"""# 🔗 GitHub Integration Guide

## 📋 Setup Steps

### 1. Update Repository URL
Edit `workshop-setup.py` and update:
```python
self.github_repo = "your-username/ci-cd-chaos-workshop"  # Update this
```

### 2. Push to GitHub
```bash
git add .
git commit -m "Add Jenkins workshop setup"
git push origin main
```

### 3. Test GitHub Integration
```bash
python3 workshop-setup.py test-github
```

## 🎯 Workshop Jobs

### Job 1: Docker Build Pipeline
- **Source**: {self.github_url}
- **Branch**: main
- **Jenkinsfile**: Jenkins/scenarios/01-docker-build/Jenkinsfile
- **Triggers**: Manual (for workshop)

### Job 2: Multi-Stage Pipeline (Future)
- **Source**: {self.github_url}
- **Branch**: main
- **Jenkinsfile**: Jenkins/scenarios/02-multi-stage/Jenkinsfile
- **Triggers**: Manual (for workshop)

## 🔧 Jenkins Configuration

### GitHub Credentials
1. Go to Jenkins → Manage Jenkins → Manage Credentials
2. Add GitHub credentials if needed
3. Configure GitHub webhook (optional)

### Webhook Setup (Optional)
1. Go to your GitHub repository
2. Settings → Webhooks
3. Add webhook: http://your-jenkins-url/github-webhook/
4. Select "Just the push event"

## 🎓 Workshop Flow

1. **Attendees clone repository**
2. **Run setup script** (one command)
3. **Access Jenkins** (http://localhost:8080)
4. **Run workshop jobs**
5. **See results and reports**

## 🚀 Benefits

- ✅ **Zero local dependencies** - Everything in Docker
- ✅ **Works anywhere** - Windows, macOS, Linux
- ✅ **GitHub integration** - Real source code management
- ✅ **Production ready** - Real CI/CD pipelines
- ✅ **Easy setup** - One command does everything
"""

        github_file = self.jenkins_dir / "GITHUB_INTEGRATION.md"
        with open(github_file, 'w') as f:
            f.write(github_guide)
        
        self.print_success("GitHub integration guide created")
        return True

    def test_github_integration(self) -> bool:
        """Test GitHub integration"""
        self.print_step("GitHub Test", "Testing GitHub integration")
        
        # Test if we can access the repository
        try:
            response = requests.get(f"https://api.github.com/repos/{self.github_repo}", timeout=10)
            if response.status_code == 200:
                self.print_success("GitHub repository is accessible")
                return True
            else:
                self.print_warning(f"GitHub repository not accessible: {response.status_code}")
                return False
        except Exception as e:
            self.print_warning(f"GitHub test failed: {e}")
            return False

    def run_workshop_setup(self) -> bool:
        """Run complete workshop setup"""
        self.print_header("Jenkins Workshop Setup")
        
        try:
            # Setup Jenkins with GitHub
            if not self.setup_jenkins_with_github():
                return False
            
            # Create workshop jobs
            if not self.create_workshop_jobs():
                return False
            
            # Create attendee guide
            if not self.create_attendee_guide():
                return False
            
            # Create demo script
            if not self.create_demo_script():
                return False
            
            # Create GitHub integration guide
            if not self.create_github_integration_guide():
                return False
            
            # Test GitHub integration
            self.test_github_integration()
            
            self.print_success("Workshop setup completed successfully!")
            self.print_success("Your workshop is ready!")
            
            print("\\n🎓 Workshop Ready!")
            print("=" * 50)
            print("1. Attendees clone: git clone {self.github_url}")
            print("2. Run setup: python3 setup-jenkins-complete.py setup")
            print("3. Access Jenkins: http://localhost:8080")
            print("4. Run workshop jobs!")
            print("\\n📚 Documentation created:")
            print("- WORKSHOP_ATTENDEE_GUIDE.md")
            print("- GITHUB_INTEGRATION.md")
            print("- demo-workshop.py")
            
            return True
            
        except Exception as e:
            self.print_error(f"Workshop setup failed: {e}")
            return False

def main():
    """Main entry point"""
    workshop = JenkinsWorkshop()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test-github":
        workshop.test_github_integration()
    else:
        workshop.run_workshop_setup()

if __name__ == "__main__":
    main()
