# Jenkins CI/CD Workshop - Complete Setup Guide

## 📋 Prerequisites

Before starting, ensure you have:
- Docker Desktop installed and running
- Terminal/Command prompt access
- At least 4GB RAM available for containers
- Internet connection for plugin downloads

## 🚀 One-Time Setup (5 minutes)

### Step 1: Build Custom Jenkins Image

```bash
# Navigate to Jenkins directory
cd /path/to/ci-cd-chaos-workshop/Jenkins

# Build custom Jenkins with all plugins pre-installed
docker build -t jenkins-workshop:custom .
```

This will take 2-3 minutes to download and install 146+ plugins.

### Step 2: Start Jenkins Container

```bash
docker run -d \
  --name jenkins-workshop \
  --restart=unless-stopped \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)/../":/workspace \
  jenkins-workshop:custom
```

### Step 3: Wait for Jenkins to Start

```bash
# Check status (wait until it returns 200)
curl -u admin:admin -s -o /dev/null -w "%{http_code}" http://localhost:8080

# Or check logs to see "Jenkins is fully up and running"
docker logs jenkins-workshop --tail 5
```

### Step 4: Access Jenkins Dashboard

1. Open browser: **http://localhost:8080**
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin`
3. ✅ You should see the Jenkins dashboard with all features available

---

## 🎯 Workshop Scenarios

### Scenario 1: Docker Build Pipeline (Recommended Start)

**What it demonstrates**: Complete CI/CD pipeline with Docker builds, testing, and deployment

**Setup Steps**:

1. **Create Pipeline Job**:
   - Click "New Item"
   - Name: `01-docker-build`
   - Type: "Pipeline"
   - Click "OK"

2. **Configure Pipeline**:
   - Scroll to "Pipeline" section
   - Definition: "Pipeline script from SCM"
   - SCM: "Git"
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - Script Path: `Jenkins/scenarios/01-docker-build/Jenkinsfile`
   - Click "Save"

3. **Run Pipeline**:
   - Click "Build Now"
   - Watch the pipeline execute through 9 stages
   - View test results, coverage reports, and deployment configs

**Expected Results**:
- ✅ All 13 tests pass
- ✅ Docker image builds successfully
- ✅ HTML test reports generated
- ✅ Security scan completed
- ✅ Deployment configuration created

### Scenario 2: Testcontainers Integration

**What it demonstrates**: Integration testing with database containers

**Setup**: Same as Scenario 1, but use:
- Name: `02-testcontainers`
- Script Path: `Jenkins/scenarios/02-testcontainers/Jenkinsfile`

### Scenario 3: HTML Reports

**What it demonstrates**: Test result visualization and reporting

**Setup**: Same as Scenario 1, but use:
- Name: `03-html-reports`
- Script Path: `Jenkins/scenarios/03-html-reports/Jenkinsfile`

### Scenario 4: Secrets Management

**What it demonstrates**: Secure handling of credentials and secrets

**Setup**: Same as Scenario 1, but use:
- Name: `04-secrets-management`
- Script Path: `Jenkins/scenarios/04-secrets-management/Jenkinsfile`

### Scenario 5: EKS Deployment

**What it demonstrates**: Kubernetes deployment pipeline

**Setup**: Same as Scenario 1, but use:
- Name: `05-eks-deployment`
- Script Path: `Jenkins/scenarios/05-eks-deployment/Jenkinsfile`

---

## 🔧 Local Testing (Optional)

Before running pipelines, you can test scenarios locally:

### Test Scenario 1 Application

```bash
cd scenarios/01-docker-build

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and run tests
pip install -r requirements.txt
python3 -m pytest tests/ -v

# Test Docker build
docker build -t test-app .
docker run -d -p 5000:5000 --name test-app test-app
curl http://localhost:5000/health
docker stop test-app && docker rm test-app
```

---

## 🔍 Verification & Troubleshooting

### ✅ Verify Setup is Working

```bash
# 1. Check container is running
docker ps | grep jenkins-workshop

# 2. Check Jenkins responds
curl -u admin:admin -s http://localhost:8080/api/json | grep "mode"

# 3. Check plugin count (should be 146+)
curl -u admin:admin -s http://localhost:8080/pluginManager/api/json?depth=1 | grep -o '"shortName"' | wc -l

# 4. Test workspace mount
docker exec jenkins-workshop ls -la /workspace
```

### 🚨 Common Issues & Solutions

#### Jenkins Won't Start
```bash
# Check logs for errors
docker logs jenkins-workshop

# Restart if needed
docker restart jenkins-workshop

# If persistent issues, rebuild
docker stop jenkins-workshop && docker rm jenkins-workshop
docker volume rm jenkins_home
# Then run Step 2 again
```

#### Login Issues
- Make sure you're using `admin` / `admin`
- Try clearing browser cache
- Verify container is fully started (logs show "fully up and running")

#### Port 8080 Already in Use
```bash
# Find what's using the port
lsof -i :8080

# Use different port
docker run -d --name jenkins-workshop -p 8081:8080 -p 50001:50000 ... jenkins-workshop:custom
# Then access at http://localhost:8081
```

#### Docker Socket Permission Issues
```bash
# Fix Docker socket permissions (Linux/Mac)
sudo chmod 666 /var/run/docker.sock

# Or run Jenkins container with different Docker group
docker run -d --name jenkins-workshop --group-add $(stat -c '%g' /var/run/docker.sock) ...
```

#### Pipeline Can't Find Workspace Files
```bash
# Verify workspace mount
docker exec jenkins-workshop ls -la /workspace/Jenkins/scenarios/

# If empty, check your mount path in docker run command
# Should be: -v "$(pwd)/../":/workspace
```

---

## 📊 What's Included

### 🔌 Pre-installed Plugins (146+)
- **Pipeline & Blue Ocean**: Modern CI/CD visualization
- **Docker**: Full Docker workflow support
- **Git/GitHub**: Source code management
- **Testing**: JUnit, HTML Publisher, Coverage reports
- **Build Tools**: Maven, Gradle, Ant
- **Security**: Credentials, authentication
- **Utilities**: Timestamper, workspace cleanup, Job DSL

### 📁 Available Job Types
- ✅ **Pipeline** - Jenkinsfile-based pipelines (recommended)
- ✅ **Multibranch Pipeline** - Auto-discovery from Git branches
- ✅ **Freestyle Project** - Traditional Jenkins jobs
- ✅ **Maven Project** - Java build integration
- ✅ **Folder** - Organize related jobs
- ✅ **Organization Folder** - GitHub/GitLab organization scanning

### 🏗️ Container Architecture
```
jenkins-workshop container
├── 146+ plugins pre-installed
├── admin/admin user configured
├── Docker CLI available
├── /workspace mounted → your project files
├── /var/jenkins_home → persistent data
└── Ports: 8080 (web), 50000 (agents)
```

---

## 🎓 Workshop Flow Recommendation

1. **Start with Scenario 1** (most comprehensive)
2. **Demonstrate features**:
   - Pipeline visualization
   - Test reports
   - Docker integration
   - Blue Ocean interface
3. **Show different job types** (Pipeline vs Freestyle)
4. **Explore specific scenarios** based on audience interest
5. **Customize pipelines** for specific use cases

---

## 🆘 Need Help?

### Quick Health Check
```bash
# Run this to verify everything is working
curl -u admin:admin -s http://localhost:8080/api/json | jq '.mode'
# Should return: "NORMAL"
```

### Reset Everything
```bash
# Nuclear option - completely reset Jenkins
docker stop jenkins-workshop
docker rm jenkins-workshop
docker volume rm jenkins_home
docker rmi jenkins-workshop:custom

# Then start from Step 1
```

### Success Criteria Checklist
- [ ] Jenkins accessible at http://localhost:8080 with admin/admin
- [ ] Can create Pipeline jobs
- [ ] Workspace files visible in `/workspace`
- [ ] Docker commands work in pipeline
- [ ] Test scenario 1 runs successfully
- [ ] Blue Ocean interface accessible

---

## 🎉 You're Ready!

Your Jenkins workshop environment is now fully configured with:
- **Production-grade setup** following Jenkins best practices
- **All major plugins** for comprehensive CI/CD demos
- **5 real-world scenarios** covering different use cases
- **Complete Docker integration** for modern workflows

**Next**: Open http://localhost:8080, login with admin/admin, and start creating your first pipeline! 🚀