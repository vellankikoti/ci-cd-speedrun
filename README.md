# 🚀 CI/CD Chaos Workshop

> **"Real DevOps heroes don't fear chaos. They master it."**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat&logo=docker)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue?style=flat&logo=kubernetes)](https://kubernetes.io)
[![Jenkins](https://img.shields.io/badge/Jenkins-Ready-blue?style=flat&logo=jenkins)](https://jenkins.io)
[![Testcontainers](https://img.shields.io/badge/Testcontainers-Ready-blue?style=flat&logo=testcontainers)](https://testcontainers.com)
[![Codespaces](https://img.shields.io/badge/Codespaces-Ready-green?style=flat&logo=github)](./CODESPACES.md)

---

## 🚀 Quick Start Options

### Option A: GitHub Codespaces (RECOMMENDED - Zero Setup!)

**Just 3 commands. No installation required!**

1. Open this repo in Codespaces
2. Navigate to a scenario (e.g., `cd scenario1-testcontainers`)
3. Run the workshop: `python3 setup.py && source venv/bin/activate && python3 workshop.py`

📚 **[Full Codespaces Guide →](CODESPACES.md)**

### Option B: Local Setup (Traditional)

Install dependencies and run locally. See [Prerequisites](#-prerequisites) below.

---

## 🎯 **Mission Statement**

Welcome to the **CI/CD Chaos Workshop** - where we intentionally break things to build unbreakable DevOps pipelines! This comprehensive workshop transforms you from a DevOps novice into a DevOps pro through hands-on scenarios that mirror real-world challenges.

> **"Chaos Agent 🕷️ is sabotaging your deployments. Your mission is to build a robust CI/CD pipeline that defeats Chaos at every stage."**

---

## 🌟 **What Makes This Workshop Special**

### 🎬 **Story-Driven Learning**
- **Narrative**: Follow the epic battle against Chaos Agent
- **Emotional Hooks**: Every phase has "aha" moments
- **Real-World Scenarios**: Based on actual production challenges

### 🧨 **Hands-On Chaos Scenarios**
- **25+ Interactive Scenarios** across 4 major technologies
- **Progressive Difficulty**: From basic to advanced production patterns
- **Failure Simulation**: Learn by breaking things intentionally

---

## 🛠️ **Prerequisites**

### **Required Software**
- **🐍 Python 3.10+** - Primary automation language
- **🐳 Docker Desktop** - Containerization platform
- **☸️ Kubernetes** - Container orchestration (minikube, Docker Desktop, or cloud cluster)
- **🤖 Jenkins** - CI/CD automation platform
- **🧪 Testcontainers Desktop** - Integration testing framework

### **Installation Guide**

#### **1. Python 3.10+**

**🍎 macOS:**
```bash
# Using Homebrew (Recommended)
brew install python@3.10

# Using pyenv (Alternative)
brew install pyenv
pyenv install 3.10.0
pyenv global 3.10.0

# Verify installation
python3 --version
pip3 --version
```

**🐧 Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install Python 3.10
sudo apt install python3.10 python3.10-pip python3.10-venv python3.10-dev

# Create symlink (if needed)
sudo ln -s /usr/bin/python3.10 /usr/bin/python3

# Verify installation
python3 --version
pip3 --version
```

**🐧 Linux (CentOS/RHEL/Fedora):**
```bash
# CentOS/RHEL 8+
sudo dnf install python3.10 python3.10-pip python3.10-devel

# Fedora
sudo dnf install python3.10 python3.10-pip python3.10-devel

# Verify installation
python3 --version
pip3 --version
```

**🪟 Windows:**
```powershell
# Option 1: Download from python.org
# Visit: https://python.org/downloads/
# Download Python 3.10+ installer
# Run installer with "Add Python to PATH" checked

# Option 2: Using Chocolatey
choco install python --version=3.10.0

# Option 3: Using Scoop
scoop install python@3.10

# Verify installation
python --version
pip --version
```

#### **2. Docker Desktop**

**🍎 macOS:**
```bash
# Using Homebrew (Recommended)
brew install --cask docker

# Manual installation
# Download from: https://docker.com/products/docker-desktop/
# Install Docker Desktop for Mac

# Start Docker Desktop
open -a Docker

# Verify installation
docker --version
docker-compose --version
```

**🐧 Linux (Ubocker Engine):**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
# Verify installation
docker --version
docker-compose --version

# Test Docker
docker run hello-world
```

**🐧 Linux (Docker Desktop - Optional):**
```bash
# Download Docker Desktop for Linux
wget https://desktop.docker.com/linux/main/amd64/docker-desktop-4.20.1-amd64.deb
sudo apt install ./docker-desktop-4.20.1-amd64.deb

# Start Docker Desktop
systemctl --user start docker-desktop
```

**🪟 Windows:**
```powershell
# Option 1: Download from docker.com
# Visit: https://docker.com/products/docker-desktop/
# Download Docker Desktop for Windows
# Run installer and follow setup wizard

# Option 2: Using Chocolatey
choco install docker-desktop

# Option 3: Using Winget
winget install Docker.DockerDesktop

# Start Docker Desktop
# Launch from Start Menu or Desktop

# Verify installation
docker --version
docker-compose --version
```

#### **3. Testcontainers Desktop**

**🍎 macOS:**
```bash
# Download and install
curl -L https://testcontainers.com/desktop/download/mac -o testcontainers-desktop.dmg
open testcontainers-desktop.dmg
# Drag to Applications folder

# Alternative: Using Homebrew
brew install --cask testcontainers-desktop

# Start Testcontainers Desktop
open -a Testcontainers\ Desktop
```

**🐧 Linux:**
```bash
# Download AppImage
wget https://testcontainers.com/desktop/download/linux -O testcontainers-desktop.AppImage
chmod +x testcontainers-desktop.AppImage

# Run Testcontainers Desktop
./testcontainers-desktop.AppImage

# Or install system-wide
sudo mv testcontainers-desktop.AppImage /usr/local/bin/
sudo chmod +x /usr/local/bin/testcontainers-desktop.AppImage
```

**🪟 Windows:**
```powershell
# Download installer
Invoke-WebRequest -Uri "https://testcontainers.com/desktop/download/windows" -OutFile "testcontainers-desktop.exe"

# Run installer
.\testcontainers-desktop.exe

# Or using Chocolatey
choco install testcontainers-desktop

# Start Testcontainers Desktop
# Launch from Start Menu
```

#### **4. Kubernetes (Choose One)**

**🍎 macOS:**
```bash
# Option 1: Docker Desktop (Easiest)
# Enable Kubernetes in Docker Desktop settings
# Go to Docker Desktop > Settings > Kubernetes > Enable Kubernetes

# Option 2: Minikube
brew install minikube
minikube start --driver=docker
minikube status

# Option 3: Kind (Kubernetes in Docker)
brew install kind
kind create cluster --name workshop
kind get clusters

# Option 4: k3d (Lightweight Kubernetes)
brew install k3d
k3d cluster create workshop
k3d cluster list
```

**🐧 Linux:**
```bash
# Option 1: Docker Desktop (if installed)
# Enable Kubernetes in Docker Desktop settings

# Option 2: Minikube
# Ubuntu/Debian
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --driver=docker
minikube status

# CentOS/RHEL/Fedora
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --driver=docker

# Option 3: Kind (Kubernetes in Docker)
# Ubuntu/Debian
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind create cluster --name workshop

# Option 4: k3d (Lightweight Kubernetes)
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
k3d cluster create workshop
k3d cluster list

# Option 5: MicroK8s (Snap package)
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
microk8s status --wait-ready
```

**🪟 Windows:**
```powershell
# Option 1: Docker Desktop (Easiest)
# Enable Kubernetes in Docker Desktop settings
# Go to Docker Desktop > Settings > Kubernetes > Enable Kubernetes

# Option 2: Minikube
# Using Chocolatey
choco install minikube
minikube start --driver=docker

# Using Scoop
scoop install minikube
minikube start --driver=docker

# Manual installation
# Download from: https://minikube.sigs.k8s.io/docs/start/
# Add to PATH and run: minikube start --driver=docker

# Option 3: Kind (Kubernetes in Docker)
# Using Chocolatey
choco install kind

# Using Scoop
scoop install kind

# Manual installation
# Download from: https://kind.sigs.k8s.io/docs/user/quick-start/
# Add to PATH and run: kind create cluster

# Option 4: k3d (Lightweight Kubernetes)
# Using Chocolatey
choco install k3d

# Manual installation
# Download from: https://k3d.io/
# Add to PATH and run: k3d cluster create workshop
```

#### **5. kubectl (Kubernetes CLI)**

**🍎 macOS:**
```bash
# Using Homebrew
brew install kubectl

# Using curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify installation
kubectl version --client
```

**🐧 Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install kubectl

# CentOS/RHEL/Fedora
sudo dnf install kubectl

# Using curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify installation
kubectl version --client
```

**🪟 Windows:**
```powershell
# Using Chocolatey
choco install kubernetes-cli

# Using Scoop
scoop install kubectl

# Using curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/windows/amd64/kubectl.exe"
# Add to PATH

# Verify installation
kubectl version --client
```

#### **6. Jenkins (Automated Setup)**
```bash
# The workshop includes automated Jenkins setup
# No manual installation required - we'll set it up for you!

# Jenkins will be automatically configured with:
# - All required plugins
# - Security settings
# - Pipeline configurations
# - Integration with Docker and Kubernetes
```

#### **7. Git (Version Control)**

**🍎 macOS:**
```bash
# Usually pre-installed, or install Xcode Command Line Tools
xcode-select --install

# Using Homebrew
brew install git
```

**🐧 Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git

# CentOS/RHEL/Fedora
sudo dnf install git

# Verify installation
git --version
```

**🪟 Windows:**
```powershell
# Download from: https://git-scm.com/download/win
# Or using Chocolatey
choco install git

# Or using Scoop
scoop install git

# Verify installation
git --version
```

#### **8. Verification Commands**
```bash
# Verify all installations
python3 --version          # Should show Python 3.10+
docker --version           # Should show Docker version
kubectl version --client   # Should show kubectl version
git --version              # Should show Git version

# Test Docker
docker run hello-world

# Test Kubernetes (if cluster is running)
kubectl get nodes

# Test Testcontainers Desktop
# Should be running and accessible
```

---

## 🗺️ **Workshop Roadmap**

### **Phase 1: 🧪 TestContainers Chaos** *(15-35 min)*
**Chaos Agent strikes with flaky tests and missing services!**

- ✅ **MySQL Integration Testing** - Real database testing with Testcontainers
- ✅ **PostgreSQL Chaos Scenarios** - Handle connection failures gracefully
- ✅ **MongoDB Resilience** - Test against NoSQL databases
- ✅ **Redis Caching Chaos** - Cache failures and recovery
- ✅ **MariaDB Production Patterns** - Enterprise database testing
- ✅ **Flaky Test Detection** - Identify and fix unreliable tests

**Learning Outcomes:**
- Write bulletproof integration tests
- Handle database connection failures
- Implement proper test isolation
- Debug flaky test scenarios

### **Phase 2: 🐳 Docker Sabotage** *(35-55 min)*
**Chaos Agent breaks your container builds!**

- ✅ **Streaming Server with Docker** - Real-time data processing
- ✅ **Resilience Engineering** - Intentional failure injection
- ✅ **Networking Chaos** - Network partition simulation
- ✅ **Multi-stage Builds** - Optimized container images

**Learning Outcomes:**
- Multi-stage Docker builds
- Container security best practices
- Network failure handling
- Image optimization techniques

### **Phase 3: 🤖 Jenkins Pipeline Showdown** *(55-80 min)*
**Chaos Agent crashes your CI/CD pipelines!**

- ✅ **Pipeline Genesis** - Your first Jenkins pipeline
- ✅ **Parameterized Builds** - Dynamic pipeline configuration
- ✅ **Jenkins Powerhouse** - Advanced pipeline patterns
- ✅ **K8s Commander** - Kubernetes deployment automation
- ✅ **CI/CD Mastery** - Production-ready pipelines

**Learning Outcomes:**
- Write robust Jenkinsfiles
- Integrate Testcontainers in CI/CD
- Generate professional reports
- Manage secrets securely

### **Phase 4: ☸️ Kubernetes Warzone** *(80-105 min)*
**Chaos Agent corrupts your cluster deployments!**

- ✅ **Python App Deployment** - Production-ready K8s manifests
- ✅ **Secret Automation** - Automated secret management
- ✅ **Blue-Green Deployments** - Zero-downtime deployments


**Learning Outcomes:**
- Deploy Python apps to Kubernetes
- Implement auto-scaling strategies
- Master blue-green deployments
- Understand GitOps principles

---

## 🚀 **Universal Quick Start Guide**

### **🎯 One-Click Workshop Setup**
```bash
# Clone the repository
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop

# 🚀 UNIVERSAL SETUP - Works Everywhere!

# For TestContainers scenarios:
cd Testcontainers
python3 setup.py

# For Jenkins scenarios:
cd ../Jenkins
python3 jenkins-setup.py

# For Kubernetes scenarios:
cd ../Kubernetes
python3 universal-setup.py

# For Docker scenarios:
cd ../Docker
# Follow individual scenario guides
```

### **🎯 Alternative: Quick Start Any Component**
```bash
# TestContainers only:
cd Testcontainers && python3 setup.py

# Jenkins only:
cd Jenkins && python3 jenkins-setup.py

# Kubernetes only:
cd Kubernetes && python3 universal-setup.py

# Docker only:
cd Docker && follow scenario guides
```

---

## 🎮 **Interactive Scenarios Overview**

### **🧪 TestContainers (6 Labs)**
```
Testcontainers/labs/
├── basics/
│   ├── lab1_postgresql_basics.py      # PostgreSQL fundamentals
│   ├── lab2_database_connection.py    # Database connectivity
│   ├── lab3_data_management.py        # Data operations
│   └── lab4_multiple_containers.py    # Multi-container testing
├── intermediate/
│   ├── lab5_multi_database.py         # Multi-database coordination
│   ├── lab6_api_testing.py            # API testing with databases
│   └── lab7_microservices.py          # Microservices testing
└── advanced/
    ├── lab8_advanced_patterns.py      # Advanced testing patterns
    ├── lab9_performance.py            # Performance testing
    └── lab10_real_world.py            # Real-world scenarios
```

### **🐳 Docker (5 Scenarios)**
```
Docker/docker-scenarios/
├── scenario_01_streaming-server-with-docker.md
├── scenario_02_resilience/
├── scenario_03_networking/
├── scenario_04_multistage/
└── scenario_05_security/
```

### **🤖 Jenkins (5 Scenarios)**
```
Jenkins/jenkins-scenarios/
├── scenario_01_pipeline_genesis/
├── scenario_02_parameterized_builds/
├── scenario_03_jenkins_powerhouse/
├── scenario_04_k8s_commander/
└── scenario_05_ci_cd_mastery/
```

### **☸️ Kubernetes (5 Scenarios)**
```
Kubernetes/kubernetes-scenarios/
├── 01-python-deploy/
├── 02-secret-automation/
├── 03-blue-green/
├── 04-auto-scaling/
└── 05-gitops/
```

---

## 🎯 **What We're Demonstrating**

### **🧪 TestContainers: Real Infrastructure Testing**
- **Problem**: Mock databases don't catch real integration issues
- **Solution**: TestContainers provides real database containers
- **Demonstration**: 
  - PostgreSQL, MySQL, MongoDB, Redis integration testing
  - Chaos scenarios with connection failures
  - Performance testing with realistic data loads
  - Microservices testing patterns

### **🐳 Docker: Containerization Mastery**
- **Problem**: Inconsistent environments and deployment issues
- **Solution**: Docker containers for consistent deployments
- **Demonstration**:
  - Multi-stage builds for optimized images
  - Security scanning and vulnerability detection
  - Network failure simulation
  - Real-time streaming applications

### **🤖 Jenkins: CI/CD Pipeline Excellence**
- **Problem**: Manual, error-prone deployment processes
- **Solution**: Automated Jenkins pipelines
- **Demonstration**:
  - Pipeline as Code with Jenkinsfiles
  - Parameterized builds for flexibility
  - Integration with TestContainers
  - Kubernetes deployment automation
  - Secret management and security

### **☸️ Kubernetes: Container Orchestration**
- **Problem**: Managing containers at scale
- **Solution**: Kubernetes orchestration platform
- **Demonstration**:
  - Python application deployment
  - Secret automation and management
  - Blue-green deployments
  - Auto-scaling based on metrics
  - GitOps with ArgoCD

---

## 🎯 **Learning Outcomes**

By completing this workshop, you will:

### **Technical Skills**
- ✅ **Write bulletproof integration tests** with Testcontainers
- ✅ **Build production-ready Docker images** with multi-stage builds
- ✅ **Create robust Jenkins pipelines** with proper error handling
- ✅ **Deploy Python applications** to Kubernetes clusters
- ✅ **Implement GitOps workflows** with ArgoCD
- ✅ **Handle chaos scenarios** gracefully in production

### **DevOps Mindset**
- ✅ **Think like a Chaos Engineer** - anticipate and prevent failures
- ✅ **Build resilient systems** that can handle unexpected issues
- ✅ **Automate everything** - reduce manual intervention
- ✅ **Monitor and alert** - know when things go wrong
- ✅ **Document everything** - make knowledge transferable

### **Real-World Experience**
- ✅ **25+ Production Scenarios** based on actual challenges
- ✅ **Portfolio Projects** you can showcase to employers
- ✅ **Community Recognition** in the DevOps space

---

## 🌟 **What Makes This Different**

### **🎭 Story-Driven Learning**
Unlike dry tutorials, this workshop tells a story. You're not just learning DevOps - you're on a mission to defeat Chaos Agent and save your deployments!

### **🧪 Real Chaos Scenarios**
Every scenario is based on real production issues. You'll encounter the same problems that DevOps engineers face daily.

### **🎮 Gamified Experience**
- Progress tracking with visual feedback
- Achievement badges for completed phases
- Community recognition

### **📚 Comprehensive Coverage**
From basic Docker builds to advanced GitOps patterns, this workshop covers the entire CI/CD spectrum.

---

## 🚀 **Quick Start Examples**

### **TestContainers Example**
```python
# TestContainers/labs/basics/lab1_postgresql_basics.py
from testcontainers.postgres import PostgresContainer

def test_postgres_connection():
    with PostgresContainer("postgres:13") as postgres:
        # Real PostgreSQL database for testing!
        connection = postgres.get_connection_url()
        # Your tests here...
```

### **Docker Example**
```dockerfile
# Multi-stage build for optimized images
FROM python:3.10-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
COPY --from=builder /root/.local /root/.local
COPY app.py .
CMD ["python", "app.py"]
```

### **Jenkins Example**
```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'python -m pytest tests/'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t myapp .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
```

### **Kubernetes Example**
```yaml
# Deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    spec:
      containers:
      - name: my-app
        image: myapp:latest
        ports:
        - containerPort: 8080
```

---

## 📊 **Workshop Statistics**

- **📚 25+ Interactive Scenarios**
- **⏱️ 2-2.5 Hours Total Duration**
- **🎯 4 Major Technology Areas**
- **📈 80-90% Hands-On Time**

---

## 🤝 **Community & Support**

### **📖 Documentation**
- 📚 **Comprehensive Guides**: Step-by-step instructions for every scenario
- 🎥 **Video Tutorials**: Coming soon for visual learners
- 💬 **Community Forum**: Get help from fellow Chaos Slayers

### **🔄 Continuous Updates**
- 🔄 **Regular Updates**: New scenarios added monthly
- 🐛 **Bug Fixes**: Quick response to issues
- 📈 **Feature Requests**: Community-driven improvements

### **🎯 Contributing**
We welcome contributions! Whether it's:
- 🐛 **Bug Reports**: Help improve the workshop
- 💡 **Feature Ideas**: Suggest new scenarios
- 📝 **Documentation**: Improve guides and tutorials
- 🌟 **Star the Repo**: Show your support

---

## 🚀 **Ready to Become a Chaos Slayer?**

> **"Chaos Agent is coming for your deployments. Are you ready to build the pipeline that will defeat them?"**

### **🎯 Start Your Journey**
1. **Clone this repository**
2. **Install prerequisites** (Python 3.10+, Docker Desktop, Testcontainers Desktop, Kubernetes)
3. **Follow the setup guide**
4. **Begin with Phase 1: TestContainers Chaos**
5. **Complete all scenarios**

### **🌟 Join the Community**
- ⭐ **Star this repository** if it helps you
- 🔄 **Fork and contribute** to improve it
- 💬 **Share your experience** with others

---

## 📞 **Get in Touch**

- 🌐 **Live Workshop**: [DevOps Workshop](https://ep2025.argo.in)
- 📧 **Email**: [vellankikoti@gmail.com]
- 🐦 **X/Twitter**: [DevOpsCircuit](https://x.com/DevOpsCircuit)
- 💼 **LinkedIn**: [Koti Vellanki](https://www.linkedin.com/in/vellankikoti/)

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎉 Ready to master chaos and become a DevOps hero? Let's get started! 🚀**

---

*"In chaos, there is opportunity. In DevOps, there is mastery."* - Chaos Slayer Mantra