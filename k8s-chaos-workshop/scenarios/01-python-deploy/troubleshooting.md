# 🛠️ Scenario 1: Troubleshooting Guide

**"Even Heroes Need Debugging Sometimes!" 🦸‍♂️🐛**

---

## 🚨 **QUICK EMERGENCY RESET**

If everything is broken and you need to start fresh:

```bash
# Nuclear option - delete everything and start over
kubectl delete namespace vote-app --force --grace-period=0

# Wait 30 seconds, then re-run
sleep 30
python3 hero-solution/deploy-vote-app.py
```

---

## 🔍 **COMMON ISSUES AND SOLUTIONS**

### **Issue 1: "Could not load K8s config"**

**Symptoms**: 
```
❌ Could not load K8s config!
```

**Root Cause**: Python can't connect to your Kubernetes cluster

**Solutions**:

```bash
# Step 1: Verify kubectl works
kubectl cluster-info

# If kubectl fails, fix your cluster connection first:

# For Docker Desktop:
# 1. Open Docker Desktop
# 2. Settings → Kubernetes → Enable Kubernetes
# 3. Apply & Restart

# For Minikube:
minikube status
minikube start  # if not running

# For EKS:
aws eks update-kubeconfig --region <your-region> --name <cluster-name>

# Step 2: Verify config file exists
ls -la ~/.kube/config

# Step 3: Test connection
kubectl get nodes
```

**Alternative Fix**:
```bash
# Sometimes the kubeconfig context is wrong
kubectl config get-contexts
kubectl config use-context <correct-context>
```

---

### **Issue 2: "Connection refused" accessing vote app**

**Symptoms**: 
- Browser shows "This site can't be reached"
- URL http://localhost:30001 doesn't work

**Root Cause**: Service not accessible from your machine

**Solutions by Environment**:

#### **Docker Desktop Kubernetes:**
```bash
# Should work with localhost
curl http://localhost:30001

# If not working, check service
kubectl get svc -n vote-app
kubectl describe svc vote-app-service -n vote-app
```

#### **Minikube:**
```bash
# Get Minikube IP (don't use localhost!)
minikube ip
# Example output: 192.168.49.2

# Access using Minikube IP
open http://$(minikube ip):30001

# Alternative: Use port forwarding
kubectl port-forward svc/vote-app-service -n vote-app 8080:80
# Then access: http://localhost:8080
```

#### **EKS (AWS):**
```bash
# Get external IP of any node
kubectl get nodes -o wide

# Use any External-IP with port 30001
# Example: http://3.15.24.76:30001

# Alternative: Use port forwarding
kubectl port-forward svc/vote-app-service -n vote-app 8080:80
# Then access: http://localhost:8080
```

#### **Universal Solution (Works Everywhere):**
```bash
# Port forward always works
kubectl port-forward svc/vote-app-service -n vote-app 8080:80

# Access at: http://localhost:8080
# Keep this terminal open while testing
```

---

### **Issue 3: Pods stuck in "Pending" state**

**Symptoms**:
```bash
kubectl get pods -n vote-app
# Shows: vote-app-xxx   0/1   Pending   0   5m
```

**Diagnosis**:
```bash
# Check what's wrong
kubectl describe pod -n vote-app $(kubectl get pods -n vote-app -o name | head -1)

# Look for events at the bottom of the output
```

**Common Causes & Fixes**:

#### **Insufficient Resources:**
```bash
# Check node resources
kubectl describe nodes

# Look for:
# - Allocatable CPU/Memory
# - Non-terminated Pods usage

# Solution: Free up resources or use smaller limits
# Edit deploy-vote-app.py and reduce resources:
# requests: {"memory": "64Mi", "cpu": "50m"}
# limits: {"memory": "128Mi", "cpu": "100m"}
```

#### **Image Pull Issues:**
```bash
# Check if image exists and is accessible
docker pull quay.io/sjbylo/flask-vote-app:latest

# If this fails, you have connectivity issues
# For corporate networks, check proxy settings
```

#### **Node Selector Problems:**
```bash
# Check node labels
kubectl get nodes --show-labels

# Our deployment doesn't use node selectors, so this is rare
```

---

### **Issue 4: "ImagePullBackOff" errors**

**Symptoms**:
```bash
kubectl get pods -n vote-app
# Shows: vote-app-xxx   0/1   ImagePullBackOff   0   2m
```

**Diagnosis**:
```bash
# Get detailed error
kubectl describe pod -n vote-app $(kubectl get pods -n vote-app -o name | head -1)

# Look for "Failed to pull image" messages
```

**Solutions**:

#### **Test Image Manually:**
```bash
# Try pulling the image yourself
docker pull quay.io/sjbylo/flask-vote-app:latest

# If this works, the issue is cluster-specific
# If this fails, you have network/proxy issues
```

#### **Corporate Network Issues:**
```bash
# Configure Docker for corporate proxy
# Add to ~/.docker/config.json:
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.company.com:8080",
      "httpsProxy": "http://proxy.company.com:8080"
    }
  }
}

# Configure Kubernetes nodes for proxy (ask admin)
```

#### **Use Alternative Image:**
```bash
# Edit deploy-vote-app.py and change the image to a simpler one:
# self.image = "nginx:alpine"  # Simple test image

# This will at least test the deployment mechanism
```

---

### **Issue 5: Python dependencies installation fails**

**Symptoms**:
```bash
pip3 install -r requirements.txt
# Shows various error messages
```

**Solutions**:

#### **Update pip first:**
```bash
# Update pip to latest version
pip3 install --upgrade pip

# Try again
pip3 install -r hero-solution/requirements.txt
```

#### **Use Virtual Environment (Recommended):**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r hero-solution/requirements.txt

# Run scripts
python deploy-vote-app.py
```

#### **Install Specific Versions:**
```bash
# If latest versions conflict, use specific versions
pip3 install kubernetes==28.1.0 pyyaml==6.0.1 requests==2.31.0 colorama==0.4.6
```

#### **System Package Installation:**
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# On CentOS/RHEL
sudo yum install python3-pip

# On macOS
brew install python3
```

---

### **Issue 6: "Permission denied" / RBAC errors**

**Symptoms**:
```
Forbidden: User "xxx" cannot create deployments.apps in namespace "vote-app"
```

**Diagnosis**:
```bash
# Check your permissions
kubectl auth can-i create deployments
kubectl auth can-i create services
kubectl auth can-i create namespaces
```

**Solutions**:

#### **For Local Clusters (Docker Desktop/Minikube):**
```bash
# You should have admin access by default
# If not, grant yourself admin rights
kubectl create clusterrolebinding workshop-admin \
  --clusterrole=cluster-admin \
  --user=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.user}')
```

#### **For EKS/Cloud Clusters:**
```bash
# Check your AWS/cloud permissions
# You need appropriate IAM roles

# Quick check
aws sts get-caller-identity

# Contact your cluster administrator if you don't have sufficient permissions
```

#### **Create Service Account (If Needed):**
```bash
# Create service account with appropriate permissions
kubectl create serviceaccount workshop-sa -n default
kubectl create clusterrolebinding workshop-sa-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=default:workshop-sa

# Get token (for manual configuration)
kubectl create token workshop-sa
```

---

### **Issue 7: "ModuleNotFoundError: No module named 'kubernetes'"**

**Symptoms**:
```python
ModuleNotFoundError: No module named 'kubernetes'
```

**Solutions**:

```bash
# Install the Python Kubernetes library
pip3 install kubernetes

# If using virtual environment:
source venv/bin/activate  # Activate first
pip install kubernetes

# Verify installation
python3 -c "import kubernetes; print('✅ Kubernetes library installed')"
```

---

### **Issue 8: Deployment succeeds but app doesn't work**

**Symptoms**:
- Pods are running
- Service exists  
- But vote app shows errors or won't load

**Diagnosis**:
```bash
# Check pod logs
kubectl logs -n vote-app deployment/vote-app

# Check pod status
kubectl describe pods -n vote-app

# Check service endpoints
kubectl get endpoints -n vote-app
```

**Solutions**:

#### **Application Startup Issues:**
```bash
# Check container logs for errors
kubectl logs -n vote-app -l app=vote-app

# Common issues:
# - Missing environment variables
# - Application startup errors
# - Port binding issues
```

#### **Service Configuration:**
```bash
# Verify service is working
kubectl get svc -n vote-app

# Test service internally
kubectl run test-pod --image=busybox -it --rm -- wget -qO- vote-app-service.vote-app.svc.cluster.local
```

---

### **Issue 9: "Context deadline exceeded" / Timeout errors**

**Symptoms**:
```
kubernetes.client.rest.ApiException: (504) Gateway Timeout
```

**Solutions**:

```bash
# Check cluster health
kubectl cluster-info
kubectl get nodes

# Check if cluster is overloaded
kubectl top nodes  # if metrics-server is installed

# Restart cluster components (Minikube)
minikube stop
minikube start

# For other clusters, contact administrator
```

---

### **Issue 10: Python script runs but nothing happens**

**Symptoms**:
- Script completes without errors
- But no resources created
- No obvious error messages

**Diagnosis**:
```bash
# Check if resources were created
kubectl get all -n vote-app

# Check namespaces
kubectl get namespaces | grep vote

# Run script with verbose output
python3 deploy-vote-app.py 2>&1 | tee deployment.log
```

**Solutions**:

```bash
# Enable debug logging in the script
# Add this at the top of deploy-vote-app.py:
import logging
logging.basicConfig(level=logging.DEBUG)

# Or run with Python verbose mode
python3 -v deploy-vote-app.py
```

---

## 📞 **GETTING HELP**

### **Step-by-Step Debugging Process:**

1. **Read the error message carefully** 📖
   - Look for specific error codes
   - Note which component is failing

2. **Check basic connectivity** 🔗
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

3. **Verify prerequisites** ✅
   ```bash
   python3 --version
   kubectl version --client
   docker version
   ```

4. **Look at system logs** 📝
   ```bash
   kubectl get events --all-namespaces --sort-by='.lastTimestamp'
   ```

5. **Try the nuclear option** 💥
   ```bash
   kubectl delete namespace vote-app
   python3 deploy-vote-app.py
   ```

### **When to Ask for Help:**

- ✅ **After trying the above steps**
- ✅ **With specific error messages**
- ✅ **With your environment details** (Docker Desktop/Minikube/EKS)

### **What to Include When Asking:**

```bash
# Run this info-gathering script:
echo "=== ENVIRONMENT INFO ==="
kubectl version --client
python3 --version
docker version --format '{{.Client.Version}}'

echo "=== CLUSTER INFO ==="
kubectl cluster-info
kubectl get nodes

echo "=== VOTE APP STATUS ==="
kubectl get all -n vote-app
kubectl get events -n vote-app --sort-by='.lastTimestamp'

echo "=== RECENT ERRORS ==="
kubectl logs -n vote-app -l app=vote-app --tail=50
```

---

## 🎯 **SUCCESS VALIDATION**

### **How to Know Everything is Working:**

✅ **Deployment Success Indicators:**
```bash
# All pods running
kubectl get pods -n vote-app
# Should show: vote-app-xxx   1/1   Running   0   XXm

# Service accessible
curl -s http://localhost:30001 | grep -i vote
# Should return HTML with "vote" in it
```

✅ **Application Success Indicators:**
- Vote app loads in browser
- You can select an option and vote
- Results display (even if 0 votes initially)
- Page refreshes work

✅ **Monitoring Success Indicators:**
```bash
python3 monitor-deployment.py
# Should show green status indicators
# Should display pod information
# Should show service details
```

---

## 🏆 **REMEMBER: YOU'VE GOT THIS!**

**Even experienced DevOps engineers hit these issues!** 

- Kubernetes is complex - debugging is normal ✅
- Python automation makes it better - you're learning the right way ✅  
- Each problem you solve makes you stronger 💪
- The Chaos Agent is no match for persistent heroes! 🦸‍♂️

**When in doubt**: Delete everything and start fresh. Sometimes the fastest path forward is backward! 🔄