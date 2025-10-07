# 🐳 Docker Ninja - Advanced Container Orchestration

**Master advanced Docker techniques in Jenkins pipelines!**

Learn multi-stage builds, container optimization, security scanning, and blue-green deployments - become a Docker ninja!

## 🎯 What You'll Learn

- **Multi-stage Builds**: Optimize image sizes and security
- **Container Security**: Vulnerability scanning and hardening
- **Blue-Green Deployment**: Zero-downtime deployments
- **Container Orchestration**: Docker Compose and advanced patterns

## 📁 Project Structure

```
03-docker-ninja/
├── README.md              # This guide
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Multi-stage optimized build
├── docker-compose.yml    # Container orchestration
├── Jenkinsfile           # Advanced Docker pipeline
├── security-scan.py      # Security scanning script
└── tests/
    ├── test_app.py       # Application tests
    └── test_docker.py    # Docker-specific tests
```

## 🚀 Quick Start (5 Minutes Total)

### Step 1: The Application (1 minute)
A Flask app with advanced features and monitoring.

```bash
# Run locally
python app.py
# Visit: http://localhost:5000
```

### Step 2: Multi-stage Docker Build (2 minutes)
Optimized Dockerfile with security and performance:

```dockerfile
# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
USER 1000
EXPOSE 5000
CMD ["python", "app.py"]
```

### Step 3: Jenkins Pipeline (1 minute)
Advanced pipeline with security scanning and deployment:

```groovy
stage('🔒 Security Scan') {
    steps {
        sh 'python security-scan.py'
    }
}

stage('🚀 Blue-Green Deploy') {
    steps {
        sh 'docker-compose up -d --scale app=2'
    }
}
```

### Step 4: Understanding the Power (1 minute)
- **Image Optimization**: 90% size reduction with multi-stage builds
- **Security Hardening**: Vulnerability scanning and non-root users
- **Zero Downtime**: Blue-green deployment strategy
- **Container Orchestration**: Docker Compose for complex applications

## 🎮 Learning Experience

### What Makes This Special:
- ✅ **Real Optimization**: See actual image size reductions
- ✅ **Security Focus**: Learn container security best practices
- ✅ **Production Ready**: Deploy like a pro with blue-green strategy
- ✅ **Performance**: Optimized builds and deployments

### Key Concepts You'll Master:
1. **Multi-stage Builds**: Separate build and runtime environments
2. **Security Scanning**: Identify and fix vulnerabilities
3. **Blue-Green Deployment**: Zero-downtime deployment strategy
4. **Container Orchestration**: Managing complex applications

## 🧪 The Application

A Flask app with advanced features:
- **Health Monitoring**: Comprehensive health checks
- **Metrics Endpoint**: Performance and system metrics
- **Security Headers**: Security best practices
- **Graceful Shutdown**: Proper container lifecycle management

### API Endpoints:
- `GET /` - Application dashboard
- `GET /health` - Health check with metrics
- `GET /metrics` - Performance metrics
- `GET /info` - System information
- `POST /shutdown` - Graceful shutdown (for testing)

## 🐳 Docker Features

### Multi-stage Build:
```dockerfile
# Build stage - install dependencies
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage - minimal runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
USER 1000
EXPOSE 5000
CMD ["python", "app.py"]
```

### Security Features:
- **Non-root user**: Application runs as user 1000
- **Minimal base image**: Python slim for smaller size
- **Health checks**: Container health monitoring
- **Security scanning**: Vulnerability assessment

## ⚙️ Jenkins Pipeline

### Advanced Docker Pipeline:
```groovy
pipeline {
    agent any
    
    stages {
        stage('🔒 Security Scan') {
            steps {
                sh 'python security-scan.py'
            }
        }
        
        stage('🐳 Multi-stage Build') {
            steps {
                sh 'docker build --no-cache -t docker-ninja:latest .'
            }
        }
        
        stage('🚀 Blue-Green Deploy') {
            steps {
                sh 'docker-compose up -d --scale app=2'
            }
        }
    }
}
```

## 🚀 Jenkins Setup

### Quick Setup (Workshop Mode):
```bash
# 1. Start Jenkins
cd Jenkins
python3 setup-jenkins-complete.py setup

# 2. Access Jenkins
# Open http://localhost:8080

# 3. Create Pipeline Job
# - New Item → Pipeline
# - Name: "Docker Ninja"
# - Pipeline script from SCM
# - Repository: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
# - Script Path: Jenkins/jenkins-scenarios/03-docker-ninja/Jenkinsfile
```

### Manual Setup:
1. **Create New Pipeline Job**
2. **Configure Pipeline**:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - Script Path: `Jenkins/jenkins-scenarios/03-docker-ninja/Jenkinsfile`
3. **Save and Build**

## 🎯 Success Criteria

You've mastered this scenario when:
- ✅ You understand multi-stage Docker builds
- ✅ You can implement security scanning
- ✅ You know how to do blue-green deployments
- ✅ You can orchestrate containers with Docker Compose
- ✅ You feel confident about advanced Docker techniques

## 🚀 Next Steps

After completing this scenario:
1. **Try different base images** - Alpine, distroless
2. **Experiment with security scanning** - Add more security tools
3. **Move to Scenario 4** - K8s Commander with Kubernetes
4. **Build your confidence** - You're now a Docker ninja!

## 💡 Pro Tips

- **Start Simple**: Begin with basic multi-stage builds
- **Security First**: Always scan for vulnerabilities
- **Monitor Resources**: Watch container resource usage
- **Test Deployments**: Always test blue-green deployments

---

**Ready to become a Docker ninja? Let's optimize and deploy! 🐳**
