#!/usr/bin/env python3
"""
📝 Add Jenkins Job Creation to All Scenarios
Adds comprehensive Jenkins job creation instructions to all scenario README files
"""

import os
from pathlib import Path

def add_jenkins_section(readme_path: Path, scenario_name: str) -> bool:
    """Add Jenkins job creation section to a README file"""
    
    if not readme_path.exists():
        print(f"❌ README not found: {readme_path}")
        return False
    
    # Read current content
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Check if Jenkins section already exists
    if "## 🏭 Production Jenkins Job Setup" in content:
        print(f"✅ Jenkins section already exists in {readme_path}")
        return True
    
    # Create the Jenkins section
    jenkins_section = f"""

## 🏭 Production Jenkins Job Setup

### Quick Setup (Workshop Mode)
```bash
# 1. Clone the repository
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop

# 2. Start Jenkins (one command!)
cd Jenkins
python3 setup-jenkins-complete.py setup

# 3. Access Jenkins
# Open http://localhost:8080
# Complete the setup wizard

# 4. Run the pre-configured workshop job
# Click "🎓 Workshop - {scenario_name}" → "Build Now"
```

### Manual Jenkins Job Creation (Production Mode)

#### Step 1: Create New Pipeline Job
1. **Access Jenkins** at `http://localhost:8080`
2. **Click "New Item"**
3. **Enter job name**: `{scenario_name} - Production`
4. **Select "Pipeline"** and click "OK"

#### Step 2: Configure Pipeline
1. **Description**: "Complete {scenario_name.lower()} pipeline with testing and deployment"
2. **Pipeline section**:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - **Branches to build**: `*/main` (or your preferred branch)
   - **Script Path**: `Jenkins/scenarios/{scenario_name.lower().replace(' ', '-')}/Jenkinsfile`

#### Step 3: Configure Build Triggers (Optional)
- **GitHub hook trigger for GITScm polling** (if using webhooks)
- **Poll SCM** with schedule: `H/5 * * * *` (every 5 minutes)

#### Step 4: Configure Build Environment (Optional)
- **Delete workspace before build starts**
- **Add timestamps to the Console Output**

#### Step 5: Save and Run
1. **Click "Save"**
2. **Click "Build Now"**
3. **Monitor the pipeline execution**

### Pipeline Stages Overview

The Jenkinsfile includes these production-ready stages:

1. **Checkout Code** - Fetches source code from GitHub
2. **Build Docker Image** - Creates production-ready Docker image
3. **Run Unit and Integration Tests** - Executes comprehensive test suite
4. **Security Scan** - Scans Docker image for vulnerabilities
5. **Push Docker Image** - Pushes to Docker registry (configurable)
6. **Deploy to Staging** - Deploys to staging environment
7. **Run Acceptance Tests** - Validates staging deployment
8. **Approve for Production** - Manual approval gate
9. **Deploy to Production** - Production deployment

### Monitoring and Debugging

#### View Pipeline Progress
- Go to the job page
- Click on the build number
- View "Pipeline Steps" for detailed execution

#### Check Logs
- Click on any stage to see detailed logs
- Use "Console Output" for full build log

#### View Reports
- **Test Results**: JUnit test reports
- **Coverage Report**: Code coverage metrics
- **HTML Reports**: Detailed test and build reports

#### Troubleshooting
```bash
# Check Jenkins container logs
docker logs jenkins-workshop

# Check Docker daemon
docker info

# Verify Git access
docker exec jenkins-workshop git --version

# Check Jenkins workspace
docker exec jenkins-workshop ls -la /var/jenkins_home/workspace/
```

### Advanced Configuration

#### Environment Variables
Configure these in Jenkins → Manage Jenkins → Configure System → Global Properties:

- `DOCKER_REGISTRY`: Your Docker registry URL
- `DOCKER_CREDENTIAL_ID`: Jenkins credential ID for Docker registry
- `STAGING_URL`: Staging environment URL
- `PRODUCTION_URL`: Production environment URL

#### Credentials Setup
1. **Jenkins → Manage Jenkins → Manage Credentials**
2. **Add credentials for**:
   - Docker registry login
   - GitHub access (if using private repos)
   - Cloud provider access (AWS, Azure, GCP)

#### Webhook Configuration (Optional)
1. **GitHub Repository → Settings → Webhooks**
2. **Add webhook**: `http://your-jenkins-url/github-webhook/`
3. **Select events**: "Just the push event"
4. **Test webhook** to ensure connectivity

"""
    
    # Add the section before the last section or at the end
    if "## Testing" in content:
        # Insert before Testing section
        new_content = content.replace("## Testing", jenkins_section + "\n## Testing")
    elif "## Docker" in content:
        # Insert before Docker section
        new_content = content.replace("## Docker", jenkins_section + "\n## Docker")
    else:
        # Add at the end
        new_content = content + jenkins_section
    
    # Write updated content
    with open(readme_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Updated {readme_path}")
    return True

def main():
    """Add Jenkins section to all scenario README files"""
    print("📝 Adding Jenkins Job Creation to All Scenarios")
    print("=" * 60)
    
    scenarios_dir = Path(__file__).parent / "scenarios"
    
    if not scenarios_dir.exists():
        print(f"❌ Scenarios directory not found: {scenarios_dir}")
        return False
    
    updated_count = 0
    total_count = 0
    
    # Find all scenario directories
    for scenario_dir in scenarios_dir.iterdir():
        if scenario_dir.is_dir() and not scenario_dir.name.startswith("SCENARIO_"):
            total_count += 1
            readme_path = scenario_dir / "README.md"
            scenario_name = scenario_dir.name.replace("-", " ").replace("_", " ").title()
            
            if add_jenkins_section(readme_path, scenario_name):
                updated_count += 1
    
    print(f"\n📊 Summary:")
    print(f"Total scenarios: {total_count}")
    print(f"Updated: {updated_count}")
    print(f"Failed: {total_count - updated_count}")
    
    if updated_count == total_count:
        print("🎉 All scenario README files updated successfully!")
        return True
    else:
        print("⚠️ Some scenario README files could not be updated")
        return False

if __name__ == "__main__":
    main()
