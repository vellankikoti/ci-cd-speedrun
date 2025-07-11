# 🚀 Kubernetes Deployment Strategy Demo

A **visual, interactive demo** showcasing Kubernetes deployment strategies including **Blue-Green**, **Rollout**, and **Canary** deployments with real-time pod management and self-healing capabilities.

## 🎯 Demo Features

### ✨ **Visual & Interactive**
- **Real-time pod visualization** with color-coded blue/green pods
- **Animated pod transitions** when switching deployment strategies
- **Self-healing demonstrations** - kill pods and watch them recreate
- **Health indicators** with live status updates
- **Confetti celebration** when deployments succeed

### 🔄 **Deployment Strategies**
- **Blue-Green Switch**: Instantly switch all traffic to green pods (zero downtime)
- **Progressive Rollout**: Gradually replace blue pods with green (rolling update)
- **Canary Deployment**: Deploy small percentage to test before full rollout
- **Reset to 50/50**: Return to initial state with 5 blue and 5 green pods

### 🛠️ **Kubernetes Features Demonstrated**
- **Self-healing**: Kill pods and watch Kubernetes recreate them
- **High Availability**: No downtime during deployments
- **Load balancing**: Traffic distribution across healthy pods
- **Health checks**: Liveness and readiness probes
- **Resource management**: CPU and memory limits

## 🚀 Quick Start

### Prerequisites
- Kubernetes cluster (local or remote)
- `kubectl` configured
- Docker (for building images)

### 1. Setup the Demo
```bash
# Navigate to the demo directory
cd Kubernetes/kubernetes-scenarios/04-blue-green

# Apply Kubernetes manifests and setup initial state
./deploy-strategies.sh setup
```

### 2. Start the Application
```bash
# Start the backend API
cd backend
python app.py

# In another terminal, start the frontend
cd frontend
npm start
```

### 3. Access the Demo
Open your browser to: **http://localhost:3000**

## 🎮 Demo Usage

### **Deployment Strategy Buttons**
- **Switch to Green**: Instantly move all traffic to green pods
- **Progressive Rollout**: Gradually replace blue with green pods
- **Canary Deployment**: Deploy 20% green pods for testing
- **Reset to 50/50**: Return to balanced state

### **Pod Management**
- **Kill Pod**: Click the "🗡️ Kill Pod" button on any pod
- **Watch Self-healing**: Observe Kubernetes automatically recreate killed pods
- **Health Monitoring**: Real-time health status updates

### **Visual Feedback**
- **Pod Animations**: Smooth transitions when pods change state
- **Health Indicators**: Color-coded status (green=healthy, red=unhealthy)
- **Success Celebrations**: Confetti when deployments complete successfully

## 📊 Demo Scenarios

### **Scenario 1: Blue-Green Deployment**
1. Start with 5 blue, 5 green pods
2. Click "Switch to Green" 
3. Watch all pods become green instantly
4. **Result**: Zero downtime deployment

### **Scenario 2: Progressive Rollout**
1. Click "Progressive Rollout"
2. Observe pods gradually change from blue to green
3. **Result**: Gradual, controlled deployment

### **Scenario 3: Canary Testing**
1. Click "Canary Deployment"
2. See 2 green pods among 8 blue pods
3. **Result**: Safe testing with minimal risk

### **Scenario 4: Self-Healing Test**
1. Click "🗡️ Kill Pod" on any pod
2. Watch the pod disappear
3. Observe Kubernetes recreate it automatically
4. **Result**: Demonstrates Kubernetes resilience

## 🏗️ Architecture

### **Backend API** (`backend/app.py`)
- **Flask API** with Kubernetes client integration
- **Real-time pod monitoring** and health simulation
- **Deployment strategy management**
- **Pod lifecycle simulation**

### **Frontend UI** (`frontend/src/`)
- **React TypeScript** with Tailwind CSS
- **Real-time updates** every 2 seconds
- **Interactive pod management**
- **Animated transitions** and visual feedback

### **Kubernetes Manifests** (`k8s/`)
- **Blue Deployment**: Version 1.0 (stable)
- **Green Deployment**: Version 2.0 (new release)
- **Service**: Load balancer for traffic routing
- **RBAC**: Proper permissions for pod management

## 🛠️ Management Scripts

### **Deployment Strategy Script** (`deploy-strategies.sh`)
```bash
# Show current status
./deploy-strategies.sh status

# Switch to different strategies
./deploy-strategies.sh blue-green    # 5 blue, 5 green
./deploy-strategies.sh green         # 0 blue, 10 green
./deploy-strategies.sh rollout       # 3 blue, 7 green
./deploy-strategies.sh canary        # 8 blue, 2 green

# Test self-healing
./deploy-strategies.sh kill          # Kill random pod
```

## 🔧 Configuration

### **Environment Variables**
```bash
# Backend configuration
K8S_NAMESPACE=scaling-challenge
FLASK_ENV=development
```

### **Kubernetes Configuration**
- **Namespace**: `scaling-challenge`
- **Service Type**: ClusterIP
- **Resource Limits**: 128Mi memory, 100m CPU
- **Health Checks**: Liveness and readiness probes

## 📈 Monitoring & Observability

### **Health Metrics**
- **Pod Health**: Real-time status monitoring
- **Deployment Status**: Current strategy and pod counts
- **Resource Usage**: CPU and memory utilization
- **Response Times**: API endpoint performance

### **Visual Indicators**
- **Green Dots**: Healthy pods
- **Red Dots**: Unhealthy pods
- **Yellow Dots**: Pending pods
- **Animated Spinners**: Actions in progress

## 🎓 Educational Value

### **Kubernetes Concepts Demonstrated**
- **Deployments**: Blue-green, rolling, canary strategies
- **Services**: Load balancing and traffic routing
- **Pods**: Lifecycle management and health monitoring
- **Self-healing**: Automatic pod recreation
- **Resource Management**: CPU and memory limits

### **DevOps Best Practices**
- **Zero Downtime Deployments**: Blue-green switching
- **Gradual Rollouts**: Risk mitigation through progressive deployment
- **Canary Testing**: Safe feature testing with minimal impact
- **Monitoring**: Real-time health and status tracking

## 🚀 Advanced Features

### **API Endpoints**
```bash
# Get all pods
GET /api/pods

# Trigger deployment strategy
POST /api/deploy
{
  "strategy": "blue-green|rollout|canary"
}

# Kill a pod
POST /api/kill-pod
{
  "name": "pod-name"
}

# Get deployment status
GET /api/status

# Reset to initial state
POST /api/reset
```

### **Customization Options**
- **Pod Count**: Adjust replica counts in manifests
- **Health Simulation**: Modify health probability in backend
- **Animation Speed**: Configure transition durations in CSS
- **Color Schemes**: Customize pod colors and themes

## 🐛 Troubleshooting

### **Common Issues**
1. **Pods not showing**: Check namespace and labels
2. **API errors**: Verify backend is running and accessible
3. **Permission errors**: Ensure RBAC is properly configured
4. **Network issues**: Check service and pod connectivity

### **Debug Commands**
```bash
# Check pod status
kubectl get pods -n scaling-challenge

# Check deployments
kubectl get deployments -n scaling-challenge

# Check service
kubectl get service -n scaling-challenge

# View pod logs
kubectl logs <pod-name> -n scaling-challenge
```

## 🤝 Contributing

This demo is designed to be **educational and extensible**. Feel free to:

- **Add new deployment strategies**
- **Enhance visual animations**
- **Improve health monitoring**
- **Add more interactive features**

## 📚 Resources

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Canary Deployment](https://martinfowler.com/bliki/CanaryRelease.html)
- [Kubernetes Health Checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

---

**🎉 Enjoy exploring Kubernetes deployment strategies with this interactive demo!** 