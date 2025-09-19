# 🎓 Jenkins CI/CD Workshop - Attendee Guide

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
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
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

- **Workshop Repository**: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
- **Issues**: Create an issue in the repository
- **Documentation**: Check the README files in each scenario

---

**Happy Learning! 🚀**

*This workshop is designed to work anywhere and everywhere with zero local dependencies!*
