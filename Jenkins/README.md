# Jenkins CI/CD Workshop - Complete Setup Guide

## 📋 Prerequisites

Before starting, ensure you have:
- Docker Desktop installed and running
- Terminal/Command prompt access
- At least 4GB RAM available for containers
- Internet connection for plugin downloads

## 🚀 One-Command Setup (Cross-Platform)

### Quick Start

```bash
# Navigate to Jenkins directory
cd Jenkins

# Setup Jenkins (works on Windows, Mac, Linux, VMs)
python3 jenkins-setup.py setup

# Check status
python3 jenkins-setup.py status

# Run demos
python3 jenkins-setup.py demo

# Cleanup when done
python3 jenkins-setup.py cleanup
```

**That's it!** The script handles everything automatically across all platforms.

## 🎯 Available Commands

| Command | Description |
|---------|-------------|
| `setup` | Complete Jenkins setup with all scenarios |
| `status` | Check if Jenkins is running and healthy |
| `demo` | Show available demo scenarios |
| `cleanup` | Remove Jenkins container and data |

## 🌍 Cross-Platform Support

This setup works seamlessly on:
- ✅ **Windows** (PowerShell, CMD, Git Bash)
- ✅ **macOS** (Terminal, iTerm2)
- ✅ **Linux** (Ubuntu, CentOS, RHEL, etc.)
- ✅ **Virtual Machines** (VMware, VirtualBox, etc.)
- ✅ **Cloud Instances** (AWS, Azure, GCP, etc.)

## 🎮 Workshop Scenarios

### Scenario 1: Pipeline Genesis
**What it demonstrates**: Your first Jenkins pipeline - simple and clean!

```bash
cd jenkins-scenarios/scenario_01_pipeline_genesis
python3 demo.py
```

**Features**:
- Basic pipeline structure
- Stage organization
- Simple automation
- Immediate success

### Scenario 2: TestContainers Integration
**What it demonstrates**: Integration testing with database containers

```bash
cd jenkins-scenarios/scenario_02_testcontainers
python3 demo.py
```

**Features**:
- Database integration testing
- Container orchestration
- Test isolation
- Automated cleanup

### Scenario 3: Docker Ninja
**What it demonstrates**: Advanced Docker workflows and security scanning

```bash
cd jenkins-scenarios/scenario_03_docker_ninja
python3 demo.py
```

**Features**:
- Multi-stage Docker builds
- Security scanning
- HTML report generation
- Production deployment

### Scenario 4: K8s Commander
**What it demonstrates**: Kubernetes deployment and management

```bash
cd jenkins-scenarios/scenario_04_k8s_commander
python3 demo.py
```

**Features**:
- Kubernetes manifests
- Container orchestration
- Health checks
- Auto-scaling

### Scenario 5: Security Sentinel
**What it demonstrates**: Security scanning and compliance checking

```bash
cd jenkins-scenarios/scenario_05_security_sentinel
python3 demo.py
```

**Features**:
- Automated security scanning
- Compliance checking
- Vulnerability detection
- Security reporting

## 🔧 Manual Setup (If Needed)

### Step 1: Build Custom Jenkins Image

```bash
# Navigate to Jenkins directory
cd Jenkins

# Build custom Jenkins with all plugins pre-installed
docker build -t jenkins-workshop:custom .
```

### Step 2: Start Jenkins Container

```bash
# Windows (PowerShell/CMD)
docker run -d --name jenkins-workshop --restart=unless-stopped -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v "%cd%\..":/workspace --privileged jenkins-workshop:custom

# macOS/Linux
docker run -d --name jenkins-workshop --restart=unless-stopped -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)/../":/workspace --privileged jenkins-workshop:custom
```

### Step 3: Wait for Jenkins to Start

```bash
# Wait 2 minutes for Jenkins to fully start
sleep 120

# Check status
curl -u admin:admin -s -o /dev/null -w "%{http_code}" http://localhost:8080
```

### Step 4: Access Jenkins Dashboard

1. Open browser: **http://localhost:8080**
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin`

## 🎯 Success Criteria

You've successfully set up Jenkins when:
- ✅ Jenkins accessible at http://localhost:8080 with admin/admin
- ✅ Can create Pipeline jobs
- ✅ Workspace files visible in `/workspace`
- ✅ Docker commands work in pipeline
- ✅ All demo scenarios run successfully
- ✅ Blue Ocean interface accessible

## 🔍 Verification & Troubleshooting

### ✅ Verify Setup is Working

```bash
# Check container is running
docker ps | grep jenkins-workshop

# Check Jenkins responds
curl -u admin:admin -s http://localhost:8080/api/json | grep "mode"

# Check plugin count (should be 146+)
curl -u admin:admin -s http://localhost:8080/pluginManager/api/json?depth=1 | grep -o '"shortName"' | wc -l

# Test workspace mount
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
python3 jenkins-setup.py cleanup
python3 jenkins-setup.py setup
```

#### Login Issues
- Make sure you're using `admin` / `admin`
- Try clearing browser cache
- Verify container is fully started (logs show "fully up and running")

#### Port 8080 Already in Use
```bash
# Find what's using the port
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

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

## 🆘 Need Help?

### Quick Health Check
```bash
# Run this to verify everything is working
python3 jenkins-setup.py status
```

### Reset Everything
```bash
# Nuclear option - completely reset Jenkins
python3 jenkins-setup.py cleanup
python3 jenkins-setup.py setup
```

### Demo All Scenarios
```bash
# Show all available demos
python3 jenkins-setup.py demo

# Run specific scenario demo
cd jenkins-scenarios/scenario_01_pipeline_genesis
python3 demo.py --simple
```

## 🎉 You're Ready!

Your Jenkins workshop environment is now fully configured with:
- **Production-grade setup** following Jenkins best practices
- **All major plugins** for comprehensive CI/CD demos
- **5 real-world scenarios** covering different use cases
- **Complete Docker integration** for modern workflows
- **Cross-platform compatibility** for any environment

**Next**: Run `python3 jenkins-setup.py setup` and start your first pipeline! 🚀