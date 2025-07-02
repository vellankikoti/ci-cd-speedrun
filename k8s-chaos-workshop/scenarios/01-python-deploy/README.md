# 🎭 Scenario 1: Chaos Strikes Manual Deployments

**"Python K8s Automation Saves the Day!"**

---

## 📖 **SCENARIO OVERVIEW**

### **The Challenge**
Chaos Agent has infiltrated your Kubernetes deployments! Manual `kubectl` commands are failing left and right due to missing namespaces, broken ConfigMaps, and service misconfigurations. Your team is frustrated, deployments are unreliable, and production is at risk.

### **The Hero Solution**
Deploy a bulletproof Python automation system that handles Kubernetes deployments with enterprise-grade reliability. No more manual errors, no more missing dependencies, no more chaos!

### **What You'll Build**
- 🐍 **Python Kubernetes Client** automation
- 🗳️ **Interactive Vote Application** for real-world testing
- 📊 **Real-time Monitoring System** for deployment health
- 🛡️ **Chaos-proof Deployment Process** with error handling

---

## ⏱️ **TIME ALLOCATION**

| **Activity** | **Duration** | **Type** |
|--------------|--------------|----------|
| Live Demo (Instructor) | 10 minutes | 👀 Watch |
| Your Deployment | 5 minutes | 🛠️ Hands-on |
| App Interaction | 5 minutes | 🎮 Interactive |
| **Total** | **20 minutes** | |

---

## 🎯 **LEARNING OBJECTIVES**

By completing this scenario, you will:

✅ **Understand** why manual Kubernetes deployments fail  
✅ **Master** Python Kubernetes client library basics  
✅ **Implement** automated resource creation and management  
✅ **Experience** enterprise-grade error handling  
✅ **Build** monitoring and observability systems  
✅ **Defeat** Chaos Agent's manual deployment attacks! 🦸‍♂️

---

## 🧨 **THE CHAOS AGENT'S ATTACK**

> *"Your manual kubectl commands are unreliable! Watch me break your deployments with 'simple' configuration errors! Good luck debugging YAML hell in production!"* 😈

**What Chaos Agent Breaks:**
- ❌ Missing namespaces cause deployment failures
- ❌ Wrong ConfigMap names break application startup  
- ❌ Service misconfigurations prevent access
- ❌ Missing resource limits cause production chaos
- ❌ No health checks = unknown application state

---

## 🦸‍♂️ **THE PYTHON HERO'S RESPONSE**

> *"Not so fast, Chaos Agent! Python automation makes deployments bulletproof. Watch this!"*

**How Python Hero Wins:**
- ✅ **Automatic namespace management** - creates if missing
- ✅ **Dependency handling** - ConfigMaps before deployments  
- ✅ **Configuration validation** - catches errors before applying
- ✅ **Best practices enforcement** - resource limits, health checks
- ✅ **Graceful error handling** - conflicts and failures managed
- ✅ **Real-time monitoring** - know exactly what's happening

---

## 📁 **FILE STRUCTURE**

```
scenarios/01-python-deploy/
├── README.md                          # This comprehensive guide
├── demo-script.sh                     # Instructor live demo script
├── chaos/
│   ├── broken-vote-app.yaml          # Intentionally broken for demo
│   └── chaos-explanation.md          # What's wrong with manual approach
├── hero-solution/
│   ├── deploy-vote-app.py            # 🚀 Main Python deployment automation
│   ├── monitor-deployment.py         # 📊 Real-time monitoring system
│   ├── requirements.txt              # Python dependencies
│   └── k8s-manifests/               # Generated Kubernetes resources
│       ├── namespace.yaml
│       ├── configmap.yaml
│       ├── deployment.yaml
│       └── service.yaml
├── participant-guide.md               # Step-by-step participant instructions
└── troubleshooting.md                # Complete troubleshooting guide
```

---

## 🚀 **QUICK START** (For Participants)

### **Prerequisites**
- ✅ Kubernetes cluster running (Docker Desktop, Minikube, or EKS)
- ✅ Python 3.8+ installed
- ✅ kubectl configured and working

### **Step 1: Environment Setup** (2 minutes)
```bash
# Navigate to this scenario
cd scenarios/01-python-deploy

# Install Python dependencies
pip3 install -r hero-solution/requirements.txt

# Verify your cluster connection
kubectl cluster-info
```

### **Step 2: Deploy with Python Automation** (3 minutes)
```bash
# Run the Python hero solution
python3 hero-solution/deploy-vote-app.py
```

**Expected Output:**
```
🚀 Initializing Python K8s Hero System...
✅ Hero system ready to defeat Chaos Agent!
📁 Creating namespace: vote-app
✅ Namespace created successfully
⚙️  Creating ConfigMap with poll configuration
✅ ConfigMap created with poll settings
🚀 Creating bulletproof deployment
✅ Deployment created with health checks and resource limits
🌐 Creating service for external access
✅ Service created - accessible at port 30001
⏳ Waiting for deployment to be ready...
🎉 Deployment ready! 2/2 pods running
🎯 ACCESS YOUR VOTE APP:
   💻 Local: http://localhost:30001
   🌐 Minikube: http://$(minikube ip):30001
   ☁️  EKS: http://<any-node-ip>:30001
🎉 CHAOS AGENT DEFEATED!
```

### **Step 5: Access Your Vote Application** (5 minutes)

The script will provide **environment-specific access instructions** based on auto-detection:

#### **🐳 Docker Desktop Environment:**
```
💻 Primary: http://localhost:31000
🔄 If blocked: Use port forwarding below
```

#### **🎯 Minikube Environment:**
```
🌐 Minikube: http://<minikube-ip>:31000 (auto-detected)
🚀 Auto-open: minikube service vote-app-service -n vote-app
💡 Manual IP: minikube ip
```

#### **☁️ Cloud Environment (EKS/GKE/AKS):**
```
🌍 Get node IP: kubectl get nodes -o wide
🔗 Access: http://<any-external-ip>:31000
```

#### **🌐 Universal Access (Always Works):**
```bash
# This works on ANY Kubernetes environment - no conflicts!
kubectl port-forward svc/vote-app-service -n vote-app 31500:80

# Then access: http://localhost:31500
# Note: Uses port 31500 to avoid Jenkins (8080) and MkDocs (8000) conflicts
```

### **🔧 Automatic Port Forwarding Option**
The script will ask:
```
🚀 Start port forwarding automatically? (y/n):
```

If you choose **yes**:
- ✅ Port forwarding starts in background
- ✅ No manual setup needed
- ✅ Automatic conflict-free port selection
- ✅ Clean URL provided: `http://localhost:31500+`

### **Step 6: Interact with Your Vote App** (5 minutes)

Once you access the vote app through any of the above methods:

1. **🗳️ Cast Your Vote**:
   - Select your favorite programming language
   - Click "Vote" button
   - See your vote recorded instantly

2. **📊 Watch Real-time Results**:
   - View the live chart updating
   - See vote percentages change
   - Notice the interactive features

3. **🔄 Test Multiple Votes**:
   - Try different browsers
   - Vote multiple times (each counts!)
   - Refresh page and see persistence

4. **🎮 Challenge Others**:
   - Share your URL with neighbors
   - See collaborative voting
   - Watch real-time updates from multiple users
```bash
# Run the monitoring system
python3 hero-solution/monitor-deployment.py

# Choose option:
# 1 = One-time status check
# 2 = Continuous monitoring (Press Ctrl+C to stop)
```

---

## 🎬 **LIVE DEMO WALKTHROUGH** (For Instructors)

### **Demo Script Overview**

#### **Part 1: Chaos Agent Strikes (3 minutes)**
```bash
# Show the chaos - run this live
./demo-script.sh
```

**What Students See:**
1. Manual deployment fails - missing namespace
2. Fix namespace, still fails - missing ConfigMap  
3. Create ConfigMap manually, still fails - service misconfiguration
4. Frustration mounts - "This is production reality!"

#### **Part 2: Python Hero Saves the Day (4 minutes)**
```bash
# Run the hero solution
python3 hero-solution/deploy-vote-app.py
```

**Key Teaching Points:**
- ✨ **Automation handles all dependencies**
- ✨ **Error handling prevents failures**
- ✨ **Best practices applied automatically**
- ✨ **Monitoring built-in from the start**

#### **Part 3: Victory Celebration (3 minutes)**
- Show vote app working in browser
- Demonstrate monitoring system
- Emphasize reliability and repeatability

---

## 🏗️ **TECHNICAL ARCHITECTURE**

### **Application Stack**
- **Frontend**: Interactive Vote App with real-time charts
- **Backend**: Flask application (`quay.io/sjbylo/flask-vote-app`)
- **Data**: SQLite database (embedded)
- **Container**: Production-ready image with health checks

### **Kubernetes Resources Created**
```yaml
# Namespace
vote-app

# ConfigMap
vote-config:
  poll_question: "What's your favorite programming language?"
  poll_options: "Python,JavaScript,Go,Rust,Java"
  db_type: "sqlite"

# Deployment  
vote-app:
  replicas: 2
  image: quay.io/sjbylo/flask-vote-app:latest
  resources: 128Mi memory, 100m CPU
  health_checks: liveness + readiness probes

# Service
vote-app-service:
  type: NodePort
  port: 80 → 8080
  nodePort: 31000  # Updated to avoid Jenkins (8080) conflicts
```

### **Python Automation Features**
- 🔧 **Resource Management**: Create, update, conflict resolution
- 🛡️ **Error Handling**: Graceful handling of all failure modes
- 📊 **Status Monitoring**: Real-time deployment progress
- 🎯 **Best Practices**: Resource limits, health checks, labels
- 🌐 **Universal Access**: Works on all Kubernetes distributions
- 🚫 **Port Conflict Resolution**: Auto-detects and avoids conflicts
- 🔍 **Environment Detection**: Smart access instructions per environment

---

## 🔍 **KEY CONCEPTS DEMONSTRATED**

### **1. Kubernetes Python Client**
```python
from kubernetes import client, config

# Load cluster configuration
config.load_kube_config()

# Create API clients
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

# Create resources programmatically
deployment = client.V1Deployment(...)
apps_v1.create_namespaced_deployment(body=deployment)
```

### **2. Automated Resource Management**
- **Namespace Creation**: Automatic namespace management
- **ConfigMap Handling**: Configuration before deployment
- **Dependency Order**: Correct resource creation sequence
- **Conflict Resolution**: Handle existing resources gracefully

### **3. Production Best Practices**
- **Resource Limits**: Prevent resource starvation
- **Health Checks**: Liveness and readiness probes
- **Labels**: Proper resource organization
- **Error Handling**: Graceful failure management

### **4. Monitoring and Observability**
- **Real-time Status**: Live deployment monitoring
- **Health Indicators**: Color-coded status display
- **Resource Metrics**: Pod and service information
- **Event Tracking**: Kubernetes event monitoring

---

## 🎯 **SUCCESS CRITERIA**

### **You've Successfully Completed This Scenario When:**

✅ **Deployment Succeeds**
```bash
kubectl get pods -n vote-app
# Should show: vote-app-xxx   1/1   Running   0   XXm
```

✅ **Application Accessible**
- Vote app loads in your browser
- You can select options and vote  
- Results display correctly

✅ **Monitoring Works**
```bash
python3 hero-solution/monitor-deployment.py
# Shows green status indicators
# Displays accurate pod/service information
```

✅ **Understanding Gained**
- You can explain why manual deployments fail
- You understand Python K8s client benefits
- You recognize automation advantages

---

## 🚨 **TROUBLESHOOTING**

### **Quick Fixes for Common Issues**

#### **Can't Access Vote App?**
```bash
# Universal solution - port forwarding works everywhere, no conflicts
kubectl port-forward svc/vote-app-service -n vote-app 31500:80
# Then access: http://localhost:31500

# For Minikube specifically:
minikube service vote-app-service -n vote-app --url

# For Docker Desktop, also try:
curl http://127.0.0.1:31000
```

#### **Python Script Fails?**
```bash
# Check cluster connection
kubectl cluster-info

# Reinstall dependencies
pip3 install --upgrade -r hero-solution/requirements.txt
```

#### **Pods Stuck Pending?**
```bash
# Check cluster resources
kubectl describe nodes
kubectl describe pod -n vote-app <pod-name>
```

#### **Everything Broken?**
```bash
# Nuclear reset option
kubectl delete namespace vote-app --force --grace-period=0
sleep 30
python3 hero-solution/deploy-vote-app.py
```

**📖 For detailed troubleshooting, see `troubleshooting.md`**

---

## 🏆 **WHAT YOU'VE LEARNED**

### **Technical Skills**
- ✅ **Python Kubernetes Client**: API interaction patterns
- ✅ **Resource Management**: Automated K8s resource creation
- ✅ **Error Handling**: Production-grade failure management
- ✅ **Monitoring**: Real-time status tracking
- ✅ **Best Practices**: Security, resource management, health checks

### **DevOps Concepts**
- ✅ **Automation Benefits**: Reliability over manual processes
- ✅ **Infrastructure as Code**: Programmatic resource management
- ✅ **Observability**: Monitoring and status tracking
- ✅ **Error Recovery**: Graceful handling of failures
- ✅ **Production Readiness**: Enterprise deployment patterns

### **Real-World Applications**
- 🏢 **Enterprise Deployments**: Scale this pattern for production
- 🔄 **CI/CD Integration**: Use in automated pipelines  
- 📊 **Operational Tools**: Build custom monitoring solutions
- 🛡️ **Reliability Engineering**: Reduce human error in deployments

---

## 🔄 **CLEANUP** (Optional)

When you're ready to clean up this scenario:

```bash
# Remove everything
kubectl delete namespace vote-app

# Verify cleanup
kubectl get namespaces | grep vote-app
# Should return nothing
```

**Note**: Keep it running if you want to continue to the next scenarios - we'll enhance this deployment!

---

## 🚀 **NEXT STEPS**

### **Immediate Next Actions**
1. ✅ **Celebrate** - You defeated Chaos Agent! 🎉
2. 🔍 **Explore** the Python code to understand the patterns
3. 🎮 **Experiment** with the vote app - try different browsers
4. 📊 **Play** with the monitoring system

### **Preparation for Scenario 2**
- **Keep your vote app running** - we'll enhance it with secret management
- **Your Python environment is ready** - same dependencies used
- **Your confidence is built** - automation is powerful!

### **Advanced Challenges** (Optional)
Want to go deeper? Try these enhancements:

```python
# Add these features to deploy-vote-app.py:
# 1. Custom polling questions via command line arguments
# 2. Multiple environment support (dev/staging/prod namespaces)  
# 3. Image validation before deployment
# 4. Slack/Teams notifications on deployment success
# 5. Prometheus metrics collection endpoints
# 6. Custom port selection via environment variables
```

### **Port Customization Challenge**:
```python
# In deploy-vote-app.py, make ports configurable:
import os
self.node_port = int(os.getenv("VOTE_NODE_PORT", "31000"))
self.port_forward_port = int(os.getenv("VOTE_PF_PORT", "31500"))
```

---

## 🤝 **GETTING HELP**

### **Resources**
- 📖 **Troubleshooting Guide**: `troubleshooting.md`
- 📋 **Participant Guide**: `participant-guide.md` 
- 🎯 **Workshop Chat**: Ask questions anytime
- 👨‍🏫 **Instructor**: Available for assistance

### **Community**
- Share your success on social media with `#ChaosSlayerWorkshop`
- Connect with other participants
- Share your Python automation enhancements

---

## 📜 **SCENARIO SUMMARY**

| **Aspect** | **Details** |
|------------|-------------|
| **Difficulty** | ⭐⭐☆☆☆ (Beginner-friendly) |
| **Duration** | 20 minutes |
| **Technologies** | Python, Kubernetes, Flask |
| **Skills** | Automation, monitoring, troubleshooting |
| **Outcome** | Working vote app + Python expertise |

---

## 🎉 **CONGRATULATIONS!**

**You've successfully completed Scenario 1!** 

You've proven that **Python automation** can defeat **Chaos Agent's manual deployment attacks**. Your vote app is running reliably, your monitoring system is active, and you've gained valuable Kubernetes automation skills.

**The battle against chaos continues in Scenario 2...** 🦸‍♂️

---

*Remember: Every expert was once a beginner. Every pro was once an amateur. Every icon was once an unknown. Keep learning, keep building, and keep defeating chaos!* 💪