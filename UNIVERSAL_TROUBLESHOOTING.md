# 🛠️ Universal Troubleshooting Guide

> **Your workshop safety net! When things go wrong, this guide has your back.**

## 🚨 Quick Diagnosis

### 1. Run Universal Validation First
```bash
# Check TestContainers
cd testcontainers && python3 setup.py --validate-only

# Check Jenkins
cd Jenkins && ./validate-environment.sh

# Check Kubernetes
cd Kubernetes && python3 universal-setup.py --validate-only
```

---

## 🔧 Common Issues & Universal Solutions

### 1. **Docker Permission Denied**

#### Problem:
```
permission denied while trying to connect to the Docker daemon socket
```

#### Universal Solutions:
```bash
# Option 1: Fix permissions (Linux/macOS)
sudo chmod 666 /var/run/docker.sock

# Option 2: Add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again

# Option 3: On Windows (WSL2)
# Ensure Docker Desktop is running and WSL2 integration is enabled

# Option 4: On Cloud/CI
# Ensure Docker socket is mounted: -v /var/run/docker.sock:/var/run/docker.sock
```

### 2. **Python Environment Issues**

#### Problem:
```
ModuleNotFoundError: No module named 'testcontainers'
externally-managed-environment error
```

#### Universal Solutions:
```bash
# Option 1: Use virtual environment (RECOMMENDED)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Option 2: User-level install
python3 -m pip install --user -r requirements.txt

# Option 3: Force install (last resort)
python3 -m pip install --break-system-packages -r requirements.txt
```

### 3. **Workspace Path Issues**

#### Problem:
```
❌ Jenkins directory not found in workspace
❌ Scenario directory not found
```

#### Universal Solutions:
```bash
# Verify you're in the right directory
pwd
ls -la

# Should see: Jenkins/, Kubernetes/, testcontainers/, etc.

# If not, navigate to workshop root:
cd path/to/ci-cd-chaos-workshop

# Verify workspace structure
find . -name "Jenkinsfile" -type f
```

### 4. **Kubernetes Cluster Issues**

#### Problem:
```
❌ Cannot connect to Kubernetes cluster
The connection to the server localhost:8080 was refused
```

#### Universal Solutions:

**For Docker Desktop:**
```bash
# Enable Kubernetes in Docker Desktop settings
# Settings → Kubernetes → Enable Kubernetes
kubectl config use-context docker-desktop
```

**For minikube:**
```bash
# Start minikube
minikube start

# Verify
minikube status
kubectl get nodes
```

**For Cloud Clusters (EKS/GKE/AKS):**
```bash
# Ensure kubeconfig is properly set
kubectl config current-context
kubectl cluster-info

# For EKS:
aws eks update-kubeconfig --name YOUR_CLUSTER_NAME

# For GKE:
gcloud container clusters get-credentials YOUR_CLUSTER_NAME

# For AKS:
az aks get-credentials --resource-group YOUR_RG --name YOUR_CLUSTER_NAME
```

### 5. **Port Conflicts**

#### Problem:
```
Port 8080 already in use
Port 3000 already in use
```

#### Universal Solutions:
```bash
# Find what's using the port
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill the process or use different ports
# For Jenkins: Change port in docker run command
docker run -p 8081:8080 jenkins/jenkins:lts

# For apps: Modify deployment configs to use different ports
```

### 6. **Network Connectivity Issues**

#### Problem:
```
Cannot reach Docker Hub
pip install timeout
kubectl: connection refused
```

#### Universal Solutions:
```bash
# Test connectivity
ping registry-1.docker.io  # Docker Hub
ping pypi.org               # Python packages
ping 8.8.8.8               # General internet

# For corporate networks:
# Set proxy if needed
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Use local mirrors if available
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ package_name
```

---

## 🌍 Environment-Specific Solutions

### **Windows (WSL2)**
```bash
# Ensure WSL2 is properly set up
wsl --version
wsl --status

# Docker Desktop integration
# Settings → Resources → WSL Integration → Enable for your distro

# Path issues
# Use Linux paths in WSL2: /mnt/c/Users/...
# Or work entirely within WSL2 filesystem
```

### **macOS**
```bash
# Apple Silicon (M1/M2) specific
# Ensure Docker images support ARM64
docker pull --platform linux/amd64 image_name  # Force x86 if needed

# Homebrew path issues
echo $PATH  # Should include /opt/homebrew/bin
```

### **Linux**
```bash
# Permission issues
sudo chown -R $USER:$USER /path/to/workshop

# Package manager differences
# Ubuntu/Debian: apt-get
# CentOS/RHEL: yum or dnf
# Alpine: apk
```

### **Cloud Environments (GitPod, Codespaces, etc.)**
```bash
# Usually have Docker pre-installed
docker --version

# May need to start Docker service
sudo service docker start  # Some cloud environments

# Network restrictions
# Some ports may be blocked, use port forwarding
```

---

## 🔬 Advanced Debugging

### **Workshop Component Validation**

#### TestContainers Debug:
```bash
cd testcontainers
python3 -c "
import docker
client = docker.from_env()
print('Docker client:', client.info()['ServerVersion'])

from testcontainers.postgres import PostgresContainer
with PostgresContainer('postgres:13') as postgres:
    print('TestContainers working!')
"
```

#### Jenkins Debug:
```bash
# Check Jenkins logs
docker logs jenkins-chaos-workshop

# Test Jenkins API
curl -u admin:password http://localhost:8080/api/json

# Validate Jenkinsfile syntax
# In Jenkins: Pipeline Syntax → Declarative Directive Generator
```

#### Kubernetes Debug:
```bash
# Comprehensive cluster info
kubectl cluster-info dump

# Check node status
kubectl get nodes -o wide

# Check system pods
kubectl get pods -n kube-system

# Check resource usage
kubectl top nodes
kubectl top pods --all-namespaces
```

### **Container Debugging**
```bash
# Inspect running containers
docker ps -a
docker logs CONTAINER_NAME

# Enter container for debugging
docker exec -it CONTAINER_NAME /bin/bash

# Check container resource usage
docker stats

# Clean up resources
docker system prune -f
```

### **Network Debugging**
```bash
# Check container networks
docker network ls
docker network inspect bridge

# Test container connectivity
docker run --rm nicolaka/netshoot ping target_host

# Check port accessibility
telnet localhost 8080
nc -zv localhost 8080
```

---

## 🆘 Emergency Recovery

### **Complete Reset**
```bash
# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Clean up Docker system
docker system prune -af
docker volume prune -f

# Reset workshop
cd ci-cd-chaos-workshop
git clean -fdx  # WARNING: Removes all local changes
git reset --hard HEAD

# Start fresh
python3 -m venv fresh_venv
source fresh_venv/bin/activate
pip install --upgrade pip
```

### **Minimal Working Setup**
```bash
# Just TestContainers (most reliable)
cd testcontainers
python3 -m venv minimal_venv
source minimal_venv/bin/activate
pip install pytest testcontainers
python3 -c "
from testcontainers.postgres import PostgresContainer
with PostgresContainer() as postgres:
    print('✅ Minimal setup working!')
"
```

---

## 📞 Getting Help

### **Before Asking for Help**
1. Run the validation scripts
2. Check the error logs
3. Try the solutions in this guide
4. Search for your specific error message

### **When Reporting Issues**
Include this information:
```bash
# System info
uname -a
python3 --version
docker --version
kubectl version --client

# Workshop state
ls -la ci-cd-chaos-workshop/
pwd

# Error logs
# Copy the full error message and surrounding context
```

### **Quick Self-Help Commands**
```bash
# Check everything quickly
cd ci-cd-chaos-workshop

echo "=== System Info ==="
uname -a && python3 --version && docker --version

echo "=== Docker Status ==="
docker ps && docker images

echo "=== Workspace ==="
pwd && ls -la

echo "=== Python Packages ==="
pip list | grep -E "(pytest|testcontainers|kubernetes)"

echo "=== Network ==="
ping -c 1 8.8.8.8 && echo "Internet: OK" || echo "Internet: FAIL"
```

---

## ✅ Success Indicators

When everything is working correctly, you should see:

### **TestContainers:**
```
✅ Docker access verified successfully
✅ Virtual environment created successfully
✅ Requirements installed successfully
✅ Workshop setup completed successfully
```

### **Jenkins:**
```
✅ Docker access verified successfully
✅ Jenkins container started
✅ Jenkins is ready!
✅ All workspace verification checks passed!
```

### **Kubernetes:**
```
✅ Kubernetes cluster accessible
✅ Python dependencies installed
✅ Workshop namespace created
✅ All scenario files verified
```

---

## 🎯 Prevention Tips

### **Before Each Workshop:**
- [ ] Run validation scripts
- [ ] Test one scenario end-to-end
- [ ] Have backup plans ready
- [ ] Know your environment limitations

### **During Workshops:**
- [ ] Start with environment validation
- [ ] Use the universal setup scripts
- [ ] Keep this troubleshooting guide handy
- [ ] Have fallback demos ready

---

**Remember**: Every error is a learning opportunity! The goal is mastering DevOps, not fighting environment issues. Use these universal solutions to get back on track quickly! 🚀