# 🔄 Scenario 04: Blue-Green Deployment Hero

**"Visual, Interactive Deployment Strategies Defeat Chaos!"**

---

## 📖 **SCENARIO OVERVIEW**

### **The Deployment Challenge**
Chaos Agent has discovered that manual deployments are causing service downtime and user complaints! Deployment failures lead to user errors, and there's no rollback capability when things go wrong. Your team needs a visual, interactive way to manage deployment strategies with zero downtime.

### **The Deployment Hero Solution**
Deploy a visual, interactive demonstration showcasing multiple Kubernetes deployment strategies including Blue-Green, Rolling, and Canary deployments with real-time pod management and self-healing capabilities. Experience deployment strategies that ensure zero downtime and instant rollbacks!

### **What You'll Build**
- 🔄 **Visual & Interactive Deployment Demo** with real-time pod visualization
- 🔵🔴 **Blue-Green Deployment Strategy** with instant traffic switching
- 📈 **Progressive Rollout Strategy** with gradual pod replacement
- 🎯 **Canary Deployment Strategy** with safe testing approach
- 🛡️ **Self-Healing Demonstrations** with automatic pod recreation

---

## ⏱️ **TIME ALLOCATION**

| **Activity** | **Duration** | **Type** |
|--------------|--------------|----------|
| Live Demo (Instructor) | 10 minutes | 👀 Watch |
| Your Deployment Setup | 5 minutes | 🛠️ Hands-on |
| Interactive Strategy Testing | 15 minutes | 🎮 Interactive |
| Self-Healing Demonstrations | 5 minutes | 🛡️ Testing |
| **Total** | **35 minutes** | |

---

## 🎯 **LEARNING OBJECTIVES**

By completing this scenario, you will:

✅ **Master** multiple Kubernetes deployment strategies  
✅ **Understand** zero-downtime deployment techniques  
✅ **Experience** visual deployment management  
✅ **Learn** self-healing and high availability concepts  
✅ **Implement** instant rollback capabilities  
✅ **Defeat** Chaos Agent's deployment downtime attacks! 🔄

---

## 🧨 **THE CHAOS AGENT'S DEPLOYMENT ATTACK**

> *"Deployment failed! Users are seeing errors! Your manual deployments are causing downtime and user complaints! Your deployment process is a mess!"* 😈

**What Chaos Agent Exploits:**
- ❌ Manual deployments causing service downtime
- ❌ No rollback capability when deployments fail
- ❌ Users experience errors during updates
- ❌ No testing environment for new versions
- ❌ Single point of failure during deployments
- ❌ No visual feedback on deployment progress

---

## 🦸‍♂️ **THE DEPLOYMENT HERO'S RESPONSE**

> *"Not anymore! My visual, interactive deployment strategies will ensure zero-downtime updates and instant rollbacks. Watch as I demonstrate multiple deployment strategies with real-time pod management!"* 🦸‍♂️🔄

**How Deployment Hero Wins:**
- ✅ **Visual deployment management** - Real-time pod visualization
- ✅ **Zero-downtime deployments** - Blue-green traffic switching
- ✅ **Instant rollback capability** - One-click reversion
- ✅ **Self-healing demonstrations** - Automatic pod recreation
- ✅ **Multiple strategy support** - Blue-green, rolling, canary
- ✅ **Interactive controls** - Real-time strategy switching
- ✅ **Health monitoring** - Live status updates

---

## 📁 **FILE STRUCTURE**

```
scenarios/04-blue-green/
├── README.md                          # This comprehensive guide
├── deploy-strategies.sh               # Deployment strategy management
├── backend/
│   ├── app.py                        # Flask API with K8s integration
│   ├── requirements.txt              # Python dependencies
│   └── Dockerfile                    # Backend container
├── frontend/
│   ├── src/                          # React TypeScript application
│   ├── package.json                  # Node.js dependencies
│   └── Dockerfile                    # Frontend container
├── k8s/
│   ├── blue-deployment.yaml          # Blue deployment (stable)
│   ├── green-deployment.yaml         # Green deployment (new)
│   ├── service.yaml                  # Load balancer service
│   └── rbac.yaml                     # RBAC permissions
└── docker-compose.yml                # Local development setup
```

---

## 🚀 **QUICK START** (For Participants)

### **Prerequisites**
- ✅ **Scenario 3 completed** (auto-scaling should still be running)
- ✅ Kubernetes cluster running (Docker Desktop, Minikube, or cloud)
- ✅ Node.js installed for frontend development
- ✅ kubectl configured and working

### **Step 1: Environment Setup** (2 minutes)
```bash
# Navigate to blue-green scenario
cd scenarios/04-blue-green

# Install backend dependencies
pip3 install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### **Step 2: Deploy Blue-Green Demo** (3 minutes)
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Start the backend API
cd backend
python app.py &
cd ..

# Start the frontend
cd frontend
npm start &
cd ..
```

**Expected Output:**
```
🔄 BLUE-GREEN DEPLOYMENT DEMO STARTING
======================================================================
🏠 Creating namespace: deployment-demo
✅ Namespace created
🔵 Deploying blue deployment (stable version)...
✅ Blue deployment ready
🔴 Deploying green deployment (new version)...
✅ Green deployment ready
🌐 Creating load balancer service...
✅ Service created
🚀 Starting backend API...
✅ Backend API running on port 5000
🎨 Starting frontend application...
✅ Frontend running on port 3000

======================================================================
🎉 BLUE-GREEN DEPLOYMENT DEMO READY!
✅ Interactive deployment strategies available!
======================================================================

🎯 ACCESS YOUR DEPLOYMENT DEMO:
   💻 Frontend: http://localhost:3000
   🔧 Backend API: http://localhost:5000
   ☸️ Kubernetes: kubectl get pods -n deployment-demo
```

### **Step 3: Access Your Deployment Demo** (Immediate)

#### **🌐 Frontend Application:**
```
💻 Primary: http://localhost:3000
```

#### **🔧 Backend API:**
```
🔧 API: http://localhost:5000
```

#### **☸️ Kubernetes Dashboard:**
```bash
# Check deployment status
kubectl get pods -n deployment-demo

# View services
kubectl get svc -n deployment-demo

# Monitor deployments
kubectl get deployments -n deployment-demo
```

### **Step 4: Interactive Deployment Strategies** (15 minutes)

1. **🔵🔴 Blue-Green Switch**:
   - Click "Switch to Green" button
   - Watch all pods become green instantly
   - Experience zero-downtime deployment

2. **📈 Progressive Rollout**:
   - Click "Progressive Rollout" button
   - Observe pods gradually change from blue to green
   - See controlled, gradual deployment

3. **🎯 Canary Testing**:
   - Click "Canary Deployment" button
   - See 2 green pods among 8 blue pods
   - Experience safe testing with minimal risk

4. **🔄 Reset to 50/50**:
   - Click "Reset to 50/50" button
   - Return to balanced state with 5 blue and 5 green pods

### **Step 5: Self-Healing Demonstrations** (5 minutes)

1. **🗡️ Kill Pod Test**:
   - Click "🗡️ Kill Pod" button on any pod
   - Watch the pod disappear
   - Observe Kubernetes recreate it automatically

2. **🛡️ Health Monitoring**:
   - Monitor real-time health status updates
   - See color-coded status indicators
   - Experience automatic health checks

---

## 🎬 **LIVE DEMO WALKTHROUGH** (For Instructors)

### **Demo Script Overview**

#### **Part 1: Deployment Chaos Exposed (3 minutes)**
```bash
# Show deployment failures
./demo-script.sh
```

**What Students See:**
1. Manual deployment causing downtime
2. Users experiencing errors
3. No rollback capability
4. "This is deployment chaos!"

#### **Part 2: Deployment Hero Saves the Day (4 minutes)**
```bash
# Deploy the visual demo
kubectl apply -f k8s/
python backend/app.py &
cd frontend && npm start &
```

**Key Teaching Points:**
- 🔄 **Visual deployment management**
- 🔄 **Zero-downtime strategies**
- 🔄 **Instant rollback capability**
- 🔄 **Self-healing demonstrations**

#### **Part 3: Interactive Strategy Testing (3 minutes)**
- Demonstrate blue-green switching
- Show progressive rollout
- Test canary deployment
- Highlight self-healing

---

## 🔄 **DEPLOYMENT STRATEGIES**

### **1. Blue-Green Deployment**
```yaml
# Blue deployment (stable)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blue-deployment
  namespace: deployment-demo
spec:
  replicas: 5
  selector:
    matchLabels:
      app: demo-app
      version: blue
  template:
    metadata:
      labels:
        app: demo-app
        version: blue
    spec:
      containers:
      - name: app
        image: demo-app:blue
        ports:
        - containerPort: 8080

# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: green-deployment
  namespace: deployment-demo
spec:
  replicas: 0  # Start with 0 replicas
  selector:
    matchLabels:
      app: demo-app
      version: green
  template:
    metadata:
      labels:
        app: demo-app
        version: green
    spec:
      containers:
      - name: app
        image: demo-app:green
        ports:
        - containerPort: 8080
```

### **2. Service Configuration**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-service
  namespace: deployment-demo
spec:
  selector:
    app: demo-app
    version: blue  # Initially route to blue
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

### **3. Deployment Strategy Script**
```bash
#!/bin/bash
# deploy-strategies.sh

case $1 in
  "blue-green")
    # Switch to blue-green (5 blue, 5 green)
    kubectl scale deployment blue-deployment --replicas=5 -n deployment-demo
    kubectl scale deployment green-deployment --replicas=5 -n deployment-demo
    ;;
  "green")
    # Switch to green (0 blue, 10 green)
    kubectl scale deployment blue-deployment --replicas=0 -n deployment-demo
    kubectl scale deployment green-deployment --replicas=10 -n deployment-demo
    kubectl patch service demo-service -n deployment-demo --type='merge' -p='{"spec":{"selector":{"version":"green"}}}'
    ;;
  "rollout")
    # Progressive rollout (3 blue, 7 green)
    kubectl scale deployment blue-deployment --replicas=3 -n deployment-demo
    kubectl scale deployment green-deployment --replicas=7 -n deployment-demo
    ;;
  "canary")
    # Canary deployment (8 blue, 2 green)
    kubectl scale deployment blue-deployment --replicas=8 -n deployment-demo
    kubectl scale deployment green-deployment --replicas=2 -n deployment-demo
    ;;
  "kill")
    # Kill random pod
    kubectl get pods -n deployment-demo -o name | shuf -n 1 | xargs kubectl delete
    ;;
esac
```

---

## 🧪 **DEPLOYMENT TESTING**

### **Test 1: Blue-Green Switch**
```bash
# Switch to green deployment
./deploy-strategies.sh green

# Verify traffic routing
kubectl get endpoints -n deployment-demo
```

### **Test 2: Progressive Rollout**
```bash
# Start progressive rollout
./deploy-strategies.sh rollout

# Watch gradual transition
kubectl get pods -n deployment-demo -w
```

### **Test 3: Canary Testing**
```bash
# Deploy canary version
./deploy-strategies.sh canary

# Test with limited traffic
curl http://demo-service.deployment-demo.svc.cluster.local
```

### **Test 4: Self-Healing**
```bash
# Kill a random pod
./deploy-strategies.sh kill

# Watch automatic recreation
kubectl get pods -n deployment-demo -w
```

---

## 📊 **DEPLOYMENT MONITORING**

### **Real-time Pod Visualization**
```bash
# Watch pod status
kubectl get pods -n deployment-demo -w

# Monitor deployment status
kubectl get deployments -n deployment-demo -w

# Check service endpoints
kubectl get endpoints -n deployment-demo
```

### **Health Monitoring**
```bash
# Check pod health
kubectl describe pods -n deployment-demo

# View application logs
kubectl logs -f deployment/blue-deployment -n deployment-demo
kubectl logs -f deployment/green-deployment -n deployment-demo
```

### **Performance Metrics**
```bash
# Monitor resource usage
kubectl top pods -n deployment-demo

# Check network connectivity
kubectl exec -it deployment/blue-deployment -n deployment-demo -- curl -I http://demo-service
```

---

## 🎯 **SUCCESS CRITERIA**

### ✅ **Scenario 04 Complete Checklist:**
- ✅ Blue-green deployment demo deployed successfully
- ✅ Visual pod management interface working
- ✅ Blue-green switching operational
- ✅ Progressive rollout functional
- ✅ Canary deployment working
- ✅ Self-healing demonstrations verified
- ✅ Zero-downtime deployments confirmed
- ✅ Chaos Agent's deployment attacks defeated! 🔄

### **Key Learning Outcomes:**
- ✅ **Multiple Deployment Strategies** - Mastered blue-green, rolling, canary
- ✅ **Zero-Downtime Deployments** - Implemented seamless updates
- ✅ **Visual Management** - Experienced interactive deployment control
- ✅ **Self-Healing** - Understood automatic pod recreation
- ✅ **Instant Rollback** - Implemented quick reversion capability
- ✅ **Health Monitoring** - Applied real-time status tracking

---

## 🚀 **NEXT STEPS**

### **What's Next:**
1. **Scenario 05:** GitOps with ArgoCD and Argo Rollouts

### **Production Deployment Strategies:**
- Apply these deployment patterns to production applications
- Implement automated deployment pipelines
- Add comprehensive health monitoring
- Regular deployment strategy testing

---

## 🆘 **TROUBLESHOOTING**

### **Common Deployment Issues:**

#### **Issue: Pods not switching colors**
```bash
# Solution: Check deployment labels
kubectl get pods -n deployment-demo --show-labels
```

#### **Issue: Service not routing traffic**
```bash
# Solution: Check service selector
kubectl describe service demo-service -n deployment-demo
```

#### **Issue: Frontend not connecting to backend**
```bash
# Solution: Check API connectivity
kubectl exec -it deployment/blue-deployment -n deployment-demo -- curl http://demo-service
```

#### **Issue: Self-healing not working**
```bash
# Solution: Check pod events
kubectl get events -n deployment-demo --sort-by='.lastTimestamp'
```

---

## 🎉 **CONCLUSION**

**Congratulations! You've successfully defeated Chaos Agent's deployment attacks!** 🔄

### **What You've Accomplished:**
- ✅ **Implemented multiple deployment strategies** (blue-green, rolling, canary)
- ✅ **Created visual, interactive deployment management**
- ✅ **Achieved zero-downtime deployments**
- ✅ **Built instant rollback capabilities**
- ✅ **Demonstrated self-healing and high availability**

### **Key Deployment Takeaways:**
- **Multiple strategies** provide flexibility for different scenarios
- **Zero-downtime deployments** ensure continuous service availability
- **Visual management** improves deployment control and understanding
- **Self-healing** provides automatic recovery from failures
- **Instant rollback** enables quick recovery from deployment issues

**You're now ready for the final challenge: GitOps with ArgoCD! 🚀**

---

**Remember:** In the world of Kubernetes deployments, strategy and automation are your weapons against chaos! 🔄 