# 🔧 Troubleshooting Guide

Welcome to the **CI/CD Chaos Workshop Troubleshooting Guide**! This guide will help you resolve common issues and get back to defeating the Chaos Agent quickly.

> 🎯 **Goal:** Get you unstuck and back to the workshop action! 🚀

---

## 🐍 Python Issues

### Python Not Found
**Error:** `python: command not found` or `python3: command not found`

**Solutions:**
1. **Check if Python is installed:**
   ```bash
   python --version
   python3 --version
   ```

2. **Install Python if missing:**
   - **Windows:** Download from [python.org](https://python.org/downloads)
   - **macOS:** `brew install python@3.10`
   - **Linux:** `sudo apt install python3.10`

3. **Add to PATH (Windows):**
   - Reinstall Python and check "Add to PATH"
   - Or manually add Python to system PATH

### Virtual Environment Issues
**Error:** `venv: command not found`

**Solutions:**
```bash
# Install venv module
python3 -m pip install virtualenv

# Create virtual environment
python3 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

---

## 🐳 Docker Issues

### Docker Not Running
**Error:** `Cannot connect to the Docker daemon`

**Solutions:**
1. **Start Docker Desktop:**
   - Launch Docker Desktop application
   - Wait for the whale icon to stop animating

2. **Linux Docker Service:**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Add user to docker group (Linux):**
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

### Permission Denied
**Error:** `Got permission denied while trying to connect to the Docker daemon`

**Solutions:**
1. **Add user to docker group:**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Restart Docker service:**
   ```bash
   sudo systemctl restart docker
   ```

### Port Already in Use
**Error:** `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Solutions:**
1. **Find what's using the port:**
   ```bash
   # Linux/macOS
   lsof -i :8080
   
   # Windows
   netstat -ano | findstr :8080
   ```

2. **Stop the process or change port:**
   ```bash
   # Kill process
   kill -9 <PID>
   
   # Or use different port
   docker run -p 8081:8080 your-image
   ```

---

## ☸️ Kubernetes Issues

### kubectl Not Found
**Error:** `kubectl: command not found`

**Solutions:**
1. **Install kubectl:**
   ```bash
   # macOS
   brew install kubectl
   
   # Linux
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   
   # Windows
   # Download from: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
   ```

### Cluster Not Accessible
**Error:** `The connection to the server localhost:8080 was refused`

**Solutions:**
1. **Start your cluster:**
   ```bash
   # Docker Desktop
   # Enable Kubernetes in Docker Desktop settings
   
   # Minikube
   minikube start
   
   # Kind
   kind create cluster
   ```

2. **Check cluster status:**
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

### ArgoCD Issues

#### ArgoCD Server Not Accessible
**Error:** `Unable to connect to ArgoCD server`

**Solutions:**
1. **Check if ArgoCD is running:**
   ```bash
   kubectl get pods -n argocd
   ```

2. **Port forward ArgoCD server:**
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```

3. **Get admin password:**
   ```bash
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
   ```

#### Argo Rollouts Dashboard Issues
**Error:** `Argo Rollouts dashboard not accessible`

**Solutions:**
1. **Install Argo Rollouts:**
   ```bash
   kubectl apply -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
   ```

2. **Port forward dashboard:**
   ```bash
   kubectl argo rollouts dashboard
   ```

---

## 🧪 TestContainers Issues

### Container Startup Failures
**Error:** `Container startup failed`

**Solutions:**
1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Increase timeout:**
   ```python
   @pytest.fixture(scope="session")
   def mysql_container():
       with mysql_container() as mysql:
           mysql.with_startup_timeout(120)  # 2 minutes
           yield mysql
   ```

3. **Check container logs:**
   ```bash
   docker logs <container_id>
   ```

### Network Connectivity Issues
**Error:** `Connection refused` or `Network unreachable`

**Solutions:**
1. **Check container networking:**
   ```bash
   docker network ls
   docker network inspect bridge
   ```

2. **Use host networking (if needed):**
   ```python
   container = mysql_container.with_network_mode("host")
   ```

---

## 🤖 Jenkins Issues

### Jenkins Not Starting
**Error:** `Jenkins failed to start`

**Solutions:**
1. **Check Docker logs:**
   ```bash
   docker logs jenkins
   ```

2. **Check port conflicts:**
   ```bash
   lsof -i :8080
   ```

3. **Get initial admin password:**
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

### Plugin Installation Failures
**Error:** `Plugin installation failed`

**Solutions:**
1. **Update Jenkins:**
   - Go to Manage Jenkins → Manage Plugins
   - Update Jenkins to latest version

2. **Install plugins manually:**
   - Download plugin .hpi files
   - Upload via Manage Plugins → Advanced

---

## 🔧 General Issues

### Permission Issues
**Error:** `Permission denied`

**Solutions:**
1. **Check file permissions:**
   ```bash
   ls -la
   chmod +x script.sh
   ```

2. **Use sudo when needed:**
   ```bash
   sudo docker run ...
   ```

### Network Issues
**Error:** `Network unreachable` or `Connection timeout`

**Solutions:**
1. **Check internet connection:**
   ```bash
   ping google.com
   ```

2. **Check firewall settings:**
   - Windows: Check Windows Firewall
   - macOS: Check System Preferences → Security & Privacy
   - Linux: Check iptables/ufw

3. **Use VPN if behind corporate firewall**

### Disk Space Issues
**Error:** `No space left on device`

**Solutions:**
1. **Clean Docker:**
   ```bash
   docker system prune -a
   ```

2. **Clean Kubernetes:**
   ```bash
   kubectl delete all --all
   ```

3. **Check disk space:**
   ```bash
   df -h
   ```

---

## 🆘 Still Stuck?

### Get Help
1. **Check the logs:**
   ```bash
   # Docker logs
   docker logs <container_name>
   
   # Kubernetes logs
   kubectl logs <pod_name>
   
   # Application logs
   tail -f /var/log/application.log
   ```

2. **Ask for help:**
   - Workshop Discord/Slack channel
   - GitHub Issues: [Create an issue](https://github.com/vellankikoti/ci-cd-chaos-workshop/issues)
   - Stack Overflow with `#ci-cd-chaos-workshop` tag

3. **Reset and try again:**
   ```bash
   # Reset Docker
   docker system prune -a
   
   # Reset Kubernetes
   kubectl delete all --all
   
   # Start fresh
   minikube delete && minikube start
   ```

### Common Commands Reference
```bash
# Check system status
docker ps
kubectl get pods
python --version
node --version

# Restart services
sudo systemctl restart docker
minikube stop && minikube start

# Clean up
docker system prune
kubectl delete all --all
```

---

## 🎯 Quick Fixes by Scenario

### TestContainers Scenarios
- **MySQL connection issues:** Check if port 3306 is free
- **Container startup slow:** Increase startup timeout
- **Network issues:** Use host networking mode

### Docker Scenarios
- **Port conflicts:** Change ports or kill conflicting processes
- **Permission issues:** Use sudo or add user to docker group
- **Image build failures:** Check Dockerfile syntax

### Jenkins Scenarios
- **Plugin installation:** Update Jenkins first
- **Pipeline failures:** Check Groovy syntax
- **Agent connection:** Check agent configuration

### Kubernetes Scenarios
- **Pod not starting:** Check resource limits and requests
- **Service not accessible:** Check service type and ports
- **ArgoCD sync issues:** Check Git repository access

---

> 💡 **Pro Tip:** When in doubt, restart your environment and try again. The Chaos Agent loves to exploit configuration drift! 🔄

**Happy troubleshooting! May your CI/CD pipelines be chaos-resistant! 🛡️** 