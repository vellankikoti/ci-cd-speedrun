# 🚀 Kubernetes Blue-Green Demo - Scripts Guide

This guide explains all the scripts available for the Kubernetes Blue-Green deployment demo and how to use them effectively.

## 📋 Available Scripts

### 1. **`rebuild-and-deploy.sh`** - Complete Rebuild & Deploy
**Purpose**: Complete rebuild of all components with latest code changes

**What it does**:
- ✅ Stops and removes existing containers
- ✅ Removes old Docker images
- ✅ Rebuilds backend and frontend images
- ✅ Creates namespace if needed
- ✅ Applies all Kubernetes manifests
- ✅ Waits for deployments to be ready
- ✅ Sets up initial blue-green strategy (5 blue, 5 green)

**Usage**:
```bash
./rebuild-and-deploy.sh
```

**When to use**:
- First time setup
- After code changes
- When you want to ensure fresh builds
- To avoid caching issues

---

### 2. **`redeploy-local.sh`** - Quick Local Redeploy
**Purpose**: Quick rebuild and deployment for local development

**What it does**:
- ✅ Builds Docker images
- ✅ Applies Kubernetes deployments
- ✅ Waits for deployments to be ready
- ✅ Sets up port forwarding (backend:5000, frontend:3000)
- ✅ Tests API connectivity
- ✅ Opens browser automatically

**Usage**:
```bash
./redeploy-local.sh
```

**When to use**:
- Quick testing after code changes
- Local development
- When you want to see the demo immediately

---

### 3. **`deploy-strategies.sh`** - Deployment Strategy Management
**Purpose**: Manage different deployment strategies via command line

**Available commands**:
```bash
./deploy-strategies.sh setup      # Initial setup (5 blue, 5 green)
./deploy-strategies.sh status     # Show current status
./deploy-strategies.sh blue-green # Switch to blue-green (5 blue, 5 green)
./deploy-strategies.sh green      # Switch to green (0 blue, 10 green)
./deploy-strategies.sh rollout    # Progressive rollout (3 blue, 7 green)
./deploy-strategies.sh canary     # Canary deployment (8 blue, 2 green)
./deploy-strategies.sh kill       # Kill random pod to test self-healing
./deploy-strategies.sh help       # Show help
```

**When to use**:
- Command-line deployment management
- Testing different strategies
- Demonstrating self-healing
- Automation and scripting

---

### 4. **`validate-demo.sh`** - Comprehensive Validation
**Purpose**: Validate that all components are working correctly

**What it checks**:
- ✅ Prerequisites (docker, kubectl)
- ✅ Docker images exist
- ✅ Kubernetes namespace exists
- ✅ All deployments are ready
- ✅ All services exist
- ✅ All pods are running
- ✅ API endpoints are responding

**Usage**:
```bash
./validate-demo.sh
```

**When to use**:
- After setup to verify everything works
- Troubleshooting issues
- Before demonstrations
- CI/CD validation

---

## 🎯 Demo Workflow

### **First Time Setup**
```bash
# 1. Navigate to the demo directory
cd Kubernetes/kubernetes-scenarios/04-blue-green

# 2. Complete rebuild and deploy
./rebuild-and-deploy.sh

# 3. Validate everything is working
./validate-demo.sh

# 4. Start the interactive demo
./redeploy-local.sh
```

### **After Code Changes**
```bash
# Option 1: Complete rebuild (recommended for major changes)
./rebuild-and-deploy.sh

# Option 2: Quick redeploy (for minor changes)
./redeploy-local.sh
```

### **Testing Different Strategies**
```bash
# Show current status
./deploy-strategies.sh status

# Test different deployment strategies
./deploy-strategies.sh green      # All green
./deploy-strategies.sh rollout    # Progressive
./deploy-strategies.sh canary     # Canary
./deploy-strategies.sh blue-green # Reset to 50/50

# Test self-healing
./deploy-strategies.sh kill
```

### **Troubleshooting**
```bash
# 1. Validate current state
./validate-demo.sh

# 2. If validation fails, rebuild everything
./rebuild-and-deploy.sh

# 3. Check logs if needed
kubectl logs deployment/backend-deployment -n scaling-challenge
kubectl logs deployment/frontend-deployment -n scaling-challenge
```

---

## 🔧 Script Details

### **Image Names**
- Backend: `bluegreen-backend:latest`
- Frontend: `bluegreen-frontend:latest`

### **Namespace**
- All resources use: `scaling-challenge`

### **Ports**
- Backend API: `5000`
- Frontend UI: `3000`
- Kubernetes services: `ClusterIP` (accessed via port-forward)

### **Deployment Structure**
```
scaling-challenge/
├── backend-deployment (1 replica)
├── frontend-deployment (1 replica)
├── blue-deployment (5 replicas)
├── green-deployment (5 replicas)
└── Services (backend, frontend, demo-app)
```

---

## 🚨 Common Issues & Solutions

### **Issue: Images not building**
```bash
# Solution: Check Docker is running
docker ps

# Solution: Clean and rebuild
docker system prune -f
./rebuild-and-deploy.sh
```

### **Issue: Pods not starting**
```bash
# Solution: Check pod status
kubectl get pods -n scaling-challenge

# Solution: Check pod logs
kubectl logs <pod-name> -n scaling-challenge

# Solution: Rebuild everything
./rebuild-and-deploy.sh
```

### **Issue: API not responding**
```bash
# Solution: Check backend logs
kubectl logs deployment/backend-deployment -n scaling-challenge

# Solution: Check port forwarding
kubectl port-forward svc/backend-service 5000:5000 -n scaling-challenge

# Solution: Test API directly
curl http://localhost:5000/api/pods
```

### **Issue: Frontend not loading**
```bash
# Solution: Check frontend logs
kubectl logs deployment/frontend-deployment -n scaling-challenge

# Solution: Check port forwarding
kubectl port-forward svc/frontend-service 3000:80 -n scaling-challenge

# Solution: Access via browser
open http://localhost:3000
```

---

## 📊 Monitoring & Debugging

### **Check Status**
```bash
# Overall status
./validate-demo.sh

# Kubernetes resources
kubectl get all -n scaling-challenge

# Pod details
kubectl describe pods -n scaling-challenge

# Service details
kubectl describe services -n scaling-challenge
```

### **View Logs**
```bash
# Backend logs
kubectl logs deployment/backend-deployment -n scaling-challenge

# Frontend logs
kubectl logs deployment/frontend-deployment -n scaling-challenge

# Follow logs in real-time
kubectl logs -f deployment/backend-deployment -n scaling-challenge
```

### **Access Pods Directly**
```bash
# Get into a pod
kubectl exec -it <pod-name> -n scaling-challenge -- /bin/sh

# Test API from within cluster
kubectl run test-pod --image=curlimages/curl -i --rm --restart=Never -- curl http://backend-service:5000/api/pods
```

---

## 🎉 Success Indicators

### **✅ Everything Working**
- All scripts run without errors
- `./validate-demo.sh` shows all green checkmarks
- Frontend accessible at `http://localhost:3000`
- Backend API responding at `http://localhost:5000`
- Pods showing in the web UI
- Deployment strategies working via buttons

### **🎯 Demo Ready**
- 5 blue pods and 5 green pods visible
- "Kill Pod" buttons working
- Deployment strategy buttons functional
- Real-time updates working
- Animations and visual feedback smooth

---

## 💡 Tips & Best Practices

1. **Always validate after setup**: Run `./validate-demo.sh` to ensure everything works
2. **Use rebuild for major changes**: `./rebuild-and-deploy.sh` for code changes
3. **Use redeploy for quick tests**: `./redeploy-local.sh` for minor changes
4. **Check logs when troubleshooting**: Use `kubectl logs` to debug issues
5. **Test self-healing**: Use `./deploy-strategies.sh kill` to demonstrate Kubernetes resilience
6. **Use web UI for demos**: The visual interface is perfect for demonstrations
7. **Keep namespace clean**: Delete namespace and recreate if things get messy

---

**🎉 Happy deploying! Use these scripts to create amazing Kubernetes demonstrations!** 