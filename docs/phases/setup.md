# 🛠️ Complete Workshop Setup Guide

Welcome to the **CI/CD Chaos Workshop Setup Guide**! This comprehensive guide will prepare your environment for all phases and scenarios—from local Python testing to advanced Kubernetes GitOps with ArgoCD and Argo Rollouts.

> 🎯 **Goal:** Get your environment battle-ready to defeat the Chaos Agent in every scenario! 🕶️

---

## 📋 Prerequisites Checklist

### 💻 Hardware Requirements
- **RAM:** 8GB+ (16GB recommended for Kubernetes/ArgoCD scenarios)
- **Storage:** 10GB+ free disk space
- **Network:** Reliable internet connection
- **Access:** Administrator/root access

### 🛠️ Software Requirements
- **Python:** 3.10+ for automation and testing
- **Docker:** Desktop or Engine for containerization
- **Kubernetes:** Local cluster (Docker Desktop, Minikube, Kind, or cloud)
- **Git:** Version control
- **Node.js:** For frontend demos (optional but recommended)

### 🎯 Workshop Goals
- Build chaos-resistant CI/CD pipelines
- Master Testcontainers for reliable testing
- Deploy to Kubernetes with confidence
- Implement GitOps with ArgoCD and Argo Rollouts
- Defeat the Chaos Agent in all scenarios! 🔥

---

## 🐍 Step 1: Install Python 3.10+

### 🪟 Windows Installation

1. **Download Python**
   - Go to [python.org/downloads](https://python.org/downloads)
   - Download Python 3.10 or higher
   - **Important:** Check "Add Python to PATH" during installation

2. **Verify Installation**
   ```cmd
   python --version
   # Should show: Python 3.10.x or higher
   ```

### 🍎 macOS Installation

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew first if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10
```

**Option B: Download from python.org**
- Visit [python.org/downloads](https://python.org/downloads)
- Download the macOS installer
- Run the installer

**Verify Installation**
```bash
python3 --version
# Should show: Python 3.10.x or higher
```

### 🐧 Linux Installation

**Ubuntu/Debian**
```bash
# Update package list
sudo apt update

# Install Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip

# Verify installation
python3.10 --version
```

**CentOS/RHEL**
```bash
# Install Python 3.10
sudo yum install python3.10 python3-pip

# Verify installation
python3.10 --version
```

---

## 🐳 Step 2: Install Docker Desktop

### 🪟 Windows Installation

1. **Download Docker Desktop**
   - Go to [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
   - Download Docker Desktop for Windows
   - Run the installer
   - **Important:** Enable WSL 2 if prompted

2. **Start Docker Desktop**
   - Launch Docker Desktop from Start Menu
   - Wait for the whale icon to stop animating
   - Docker is ready when the icon is static

3. **Verify Installation**
   ```cmd
   docker --version
   docker run hello-world
   ```

### 🍎 macOS Installation

1. **Download Docker Desktop**
   - Go to [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
   - Download Docker Desktop for Mac
   - Drag Docker to Applications folder
   - Launch Docker Desktop

2. **Verify Installation**
   ```bash
   docker --version
   docker run hello-world
   ```

### 🐧 Linux Installation

**Install Docker using convenience script**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (log out and back in)
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
docker run hello-world
```

---

## ☸️ Step 3: Choose Your Kubernetes Cluster

### 🐳 Docker Desktop Kubernetes (Easiest)

**Perfect if you already installed Docker Desktop above!**

1. **Enable Kubernetes**
   - Open Docker Desktop
   - Go to Settings → Kubernetes
   - Check "Enable Kubernetes"
   - Click "Apply & Restart"

2. **Verify Installation**
   ```bash
   kubectl version --client
   kubectl cluster-info
   ```

### 🚀 Minikube (Most Popular)

**The most popular local Kubernetes cluster**

**Install Minikube:**

**Windows:**
```cmd
# Using Chocolatey
choco install minikube

# Or download manually from: https://minikube.sigs.k8s.io/docs/start/
```

**macOS:**
```bash
# Using Homebrew
brew install minikube
```

**Linux:**
```bash
# Download and install
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**Start and Verify:**
```bash
minikube start
kubectl version --client
minikube status
```

### 🐳 Kind (Kubernetes in Docker)

**Lightweight Kubernetes cluster using Docker**

**Install Kind:**

**Windows:**
```cmd
# Using Chocolatey
choco install kind
```

**macOS:**
```bash
# Using Homebrew
brew install kind
```

**Linux:**
```bash
# Download and install
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

**Create Cluster and Verify:**
```bash
kind create cluster --name chaos-workshop
kubectl version --client
kind get clusters
```

### ☁️ Cloud Kubernetes (GKE/EKS/AKS)

**For cloud-based development**

- **Google Kubernetes Engine (GKE):** Follow [GKE setup guide](https://cloud.google.com/kubernetes-engine/docs/quickstart)
- **Amazon EKS:** Follow [EKS setup guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html)
- **Azure Kubernetes Service (AKS):** Follow [AKS setup guide](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough)

---

## 🎯 Step 4: Install kubectl (Kubernetes CLI)

### 🪟 Windows Installation

```cmd
# Using Chocolatey
choco install kubernetes-cli

# Or download from: https://kubernetes.io/docs/tasks/tools/install-kubectl/
```

### 🍎 macOS Installation

```bash
# Using Homebrew
brew install kubectl

# Or using curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
```

### 🐧 Linux Installation

```bash
# Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Verify kubectl Installation:**
```bash
kubectl version --client
```

---

## 📦 Step 5: Clone Workshop Repository

### Install Git (if not already installed)

**Windows:**
Download from [git-scm.com](https://git-scm.com)

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git  # Ubuntu/Debian
sudo yum install git  # CentOS/RHEL
```

### Clone the workshop repository

```bash
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop
```

---

## 🐍 Step 6: Set Up Python Virtual Environment

### Create a virtual environment

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### Activate the virtual environment

**Windows:**
```cmd
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Verify activation

```bash
# You should see (venv) at the start of your prompt
which python  # macOS/Linux
where python  # Windows
```

---

## 📚 Step 7: Install Required Packages

### Upgrade pip

```bash
pip install --upgrade pip
```

### Install workshop dependencies

```bash
pip install -r requirements.txt
```

### Install additional packages

```bash
pip install docker
pip install kubernetes
pip install jenkins
pip install jinja2
pip install weasyprint
pip install mkdocs
pip install mkdocs-material
```

### Verify installations

```bash
python -c "import pytest, testcontainers, docker, kubernetes, fastapi, uvicorn; print('✅ All packages installed successfully!')"
```

---

## 🎯 Step 8: Install Node.js (for frontend demos)

### 🍎 macOS Installation

```bash
brew install node
```

### 🪟 Windows Installation

Download from [nodejs.org](https://nodejs.org/)

### 🐧 Linux Installation

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**CentOS/RHEL:**
```bash
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install -y nodejs
```

### Verify Node.js installation

```bash
node --version
npm --version
```

---

## 🚀 Step 9: Install ArgoCD CLI (Optional, for advanced GitOps)

### 🍎 macOS Installation

```bash
brew install argocd
```

### 🐧 Linux Installation

```bash
curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
chmod +x argocd
sudo mv argocd /usr/local/bin/
```

### 🪟 Windows Installation

```cmd
choco install argocd-cli
```

---

## 🔄 Step 10: Install Argo Rollouts Plugin (Optional, for advanced rollout UI)

### 🍎 macOS Installation

```bash
brew install argo-rollouts
```

### 🐧 Linux Installation

```bash
curl -sLO https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
chmod +x kubectl-argo-rollouts-linux-amd64
sudo mv kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts
```

### 🪟 Windows Installation

```cmd
choco install argo-rollouts
```

---

## 🧪 Step 11: Test Your Setup

### Test Python

```bash
python --version
```

### Test Docker

```bash
docker run hello-world
```

### Test Kubernetes

```bash
kubectl version --client
kubectl cluster-info
```

### Test Testcontainers

```bash
python -c "
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

# Test Redis container
with DockerContainer('redis:alpine') as redis:
    redis.with_exposed_ports(6379)
    redis.start()
    print('✅ Testcontainers working!')
"
```

### Test Node.js

```bash
node --version
npm --version
```

---

## 🎉 Step 12: You're Ready!

### 🎊 Congratulations! You're Ready for Chaos!

If all tests pass, you're ready to battle the Chaos Agent in every scenario!

### 🚀 Next Steps:

1. ✅ Read the [Workshop Overview](../index.md)
2. ✅ Start with [Phase 1: Test Mayhem](testcontainers.md)
3. ✅ Prepare to defeat chaos! 🔥

---

## 🆘 Troubleshooting

### Common Issues & Solutions

#### 🐳 Docker not starting

**Windows:**
- Make sure WSL 2 is enabled
- Check Docker Desktop is running

**macOS:**
- Check Docker Desktop is running
- Restart Docker Desktop if needed

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### ☸️ Kubernetes connection issues

**Minikube:**
```bash
minikube start
```

**Kind:**
```bash
kind create cluster
```

**Docker Desktop:**
- Enable Kubernetes in Docker Desktop settings

#### 🐍 Python package issues

- Make sure your virtual environment is activated
- Try: `pip install --upgrade pip setuptools wheel`
- Check Python version: `python --version`

#### 🔐 Permission errors

**Windows:**
- Run as Administrator

**Linux/macOS:**
- Use `sudo` where needed
- Check file permissions and ownership

### Still Stuck?

1. Check the [Troubleshooting Guide](../troubleshooting.md)
2. Ask in the workshop Discord/Slack
3. Open an issue on GitHub

---

## 🎯 Quick Verification Checklist

### Final Verification

Before the workshop starts, make sure you can run:

#### ✅ Python works
```bash
python --version
```

#### ✅ Docker works
```bash
docker run hello-world
```

#### ✅ Kubernetes works
```bash
kubectl version --client
```

#### ✅ Virtual environment is active
```bash
echo $VIRTUAL_ENV  # Should show path to venv
```

#### ✅ Packages are installed
```bash
python -c "import pytest, testcontainers, docker, kubernetes, fastapi, uvicorn; print('Ready!')"
```

#### ✅ Node.js works (optional)
```bash
node --version
npm --version
```

### Ready Message

**If all ✅ pass, you're ready to create some chaos! 🧨**

---

## 📊 Workshop Phases Overview

### Phase 1: Testcontainers
- **Goal:** Master reliable testing with containers
- **Skills:** Python testing, Docker integration, database testing
- **Duration:** 30 minutes

### Phase 2: Jenkins
- **Goal:** Build chaos-resistant CI/CD pipelines
- **Skills:** Jenkins automation, pipeline scripting, error handling
- **Duration:** 45 minutes

### Phase 3: Docker
- **Goal:** Containerize applications and handle Docker chaos
- **Skills:** Docker builds, multi-stage builds, image optimization
- **Duration:** 40 minutes

### Phase 4: Kubernetes
- **Goal:** Deploy to Kubernetes and survive chaos
- **Skills:** K8s deployments, auto-scaling, GitOps with ArgoCD
- **Duration:** 60 minutes

---

## 🎯 Success Criteria

### ✅ Complete Setup Checklist:
- ✅ Python 3.10+ installed and working
- ✅ Docker Desktop/Engine installed and running
- ✅ Kubernetes cluster accessible (local or cloud)
- ✅ kubectl configured and working
- ✅ Git installed and configured
- ✅ Virtual environment created and activated
- ✅ All Python packages installed
- ✅ Node.js installed (for frontend demos)
- ✅ ArgoCD CLI installed (for GitOps scenarios)
- ✅ Argo Rollouts plugin installed (for advanced rollouts)
- ✅ All verification tests passing

---

<div class="footer-note">

**See you in the workshop! Let's defeat that Chaos Agent together! 🕶️🔥**

</div>
