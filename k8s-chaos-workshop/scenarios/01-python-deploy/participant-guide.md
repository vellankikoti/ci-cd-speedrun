# 🎯 Scenario 1: Participant Guide

**"Defeat Chaos Agent with Python Automation!"**

---

## 🎭 **YOUR MISSION**

Chaos Agent has sabotaged manual Kubernetes deployments! Your job is to deploy a bulletproof voting application using Python automation and prove that automation defeats chaos every time.

**Time Limit**: 20 minutes  
**Difficulty**: ⭐⭐☆☆☆ (Beginner-friendly)

---

## ✅ **PREREQUISITES CHECKLIST**

Before starting, verify you have:

- [ ] **Kubernetes cluster running** (Docker Desktop, Minikube, or EKS)
- [ ] **Python 3.8+** installed (`python3 --version`)
- [ ] **kubectl configured** (`kubectl cluster-info` works)
- [ ] **Workshop repository** cloned
- [ ] **Terminal/Command Prompt** open

### **Quick Environment Check**
```bash
# Run these commands - all should work:
kubectl cluster-info                    # Shows cluster info
python3 --version                       # Shows Python 3.8+
kubectl get nodes                       # Shows cluster nodes
```

If any fail, ask for help before proceeding! 🆘

---

## 🚀 **STEP-BY-STEP EXECUTION**

### **Step 1: Navigate to Scenario Directory** (30 seconds)
```bash
# Go to the scenario folder
cd scenarios/01-python-deploy

# Verify you're in the right place
ls -la
# Should see: hero-solution/, chaos/, README.md, etc.
```

### **Step 2: Install Python Dependencies** (2 minutes)
```bash
# Install required Python packages
pip3 install -r hero-solution/requirements.txt

# If you get permission errors, try:
pip3 install --user -r hero-solution/requirements.txt

# Or use virtual environment (recommended):
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip3 install -r hero-solution/requirements.txt
```

**Expected Output**: Successful installation of kubernetes, colorama, etc.

### **Step 3: Watch the Live Demo** (10 minutes)
Your instructor will demonstrate:

1. **🧨 Chaos Agent's Attack**: Manual `kubectl` deployment failures
2. **🦸‍♂️ Python Hero's Response**: Automated deployment success
3. **🎮 Interactive Victory**: Working vote application

**Pay attention to**: The difference between manual chaos and automated reliability!

### **Step 4: Deploy Your Own Vote App** (3 minutes)
```bash
# Run the Python automation hero script
python3 hero-solution/deploy-vote-app.py
```

**Expected Output**:
```
🎭 SCENARIO 1: Chaos Strikes Manual Deployments
🦸‍♂️ Python Hero to the rescue!

🚀 Initializing Python K8s Hero System...
✅ Hero system ready to defeat Chaos Agent!
============================================================
🦸‍♂️ PYTHON HERO DEPLOYMENT STARTING
============================================================
📁 Creating namespace: vote-app
✅ Namespace created successfully
⚙️  Creating ConfigMap with poll configuration
✅ ConfigMap created with poll settings
🚀 Creating bulletproof deployment
✅ Deployment created with health checks and resource limits
🌐 Creating service for external access (port 31000)
✅ Service created - accessible at port 31000
⏳ Waiting for deployment to be ready...
🎉 Deployment ready! 2/2 pods running
🌐 Getting access information...
🎯 ACCESS YOUR VOTE APP:
   Environment detected: DOCKER-DESKTOP

[Access instructions will appear here based on your environment]
```

### **Step 5: Access Your Vote Application** (5 minutes)

The script will provide **multiple access options** based on your environment:

#### **🐳 If Using Docker Desktop:**
```
💻 Try: http://localhost:31000
🔄 If that fails, use port forwarding below
```

#### **🎯 If Using Minikube:**
```
🌐 Minikube: http://<minikube-ip>:31000
🚀 Auto-open: minikube service vote-app-service -n vote-app
```

#### **☁️ If Using Cloud (EKS/GKE/AKS):**
```
🌍 Get node IP: kubectl get nodes -o wide
🔗 Access: http://<any-external-ip>:31000
```

#### **🌐 Universal Access (Always Works):**
```bash
# This works on ANY Kubernetes environment
kubectl port-forward svc/vote-app-service -n vote-app 31500:80

# Then access: http://localhost:31500
# Keep this terminal open while using the app
```

### **Step 6: Interact with the Vote App** (5 minutes)

Once you have the vote app open:

1. **🗳️ Cast Your Vote**:
   - Select your favorite programming language
   - Click "Vote"
   - See your vote recorded

2. **📊 Watch Real-time Results**:
   - View the live chart updating
   - See vote percentages
   - Notice the interactive features

3. **🔄 Test Multiple Votes**:
   - Try different browsers
   - Vote multiple times
   - Refresh and see persistence

4. **🎮 Challenge Others**:
   - Share your URL with neighbors
   - See votes from multiple people
   - Watch real-time collaboration

### **Step 7: Monitor Your Deployment** (5 minutes)
```bash
# Run the monitoring system
python3 hero-solution/monitor-deployment.py
```

**Choose your monitoring option**:
```
📊 Vote App Monitoring System
Choose monitoring mode:
   1. One-time status check
   2. Continuous monitoring

Enter choice (1 or 2): 2
```

**For Continuous Monitoring**:
- Watch live pod status updates
- See resource utilization
- Monitor service health
- Press `Ctrl+C` to stop

---

## 🎯 **SUCCESS CRITERIA**

### **✅ You've Successfully Completed This Scenario When:**

- [ ] **Deployment Script Runs Successfully**
  ```bash
  # Check pods are running
  kubectl get pods -n vote-app
  # Should show: vote-app-xxx   1/1   Running   0   XXm
  ```

- [ ] **Vote Application is Accessible**
  - [ ] Vote app loads in your browser
  - [ ] You can select options and vote
  - [ ] Results display correctly
  - [ ] Vote counts persist after refresh

- [ ] **Monitoring System Works**
  - [ ] Monitoring script shows green status
  - [ ] Pod information displays correctly
  - [ ] Service details are accurate

- [ ] **Understanding Gained**
  - [ ] You can explain why automation beats manual processes
  - [ ] You understand Python Kubernetes client benefits
  - [ ] You recognize enterprise deployment patterns

---

## 🚨 **TROUBLESHOOTING QUICK FIXES**

### **Problem: Can't Access Vote App**
```bash
# Universal solution - works on any Kubernetes
kubectl port-forward svc/vote-app-service -n vote-app 31500:80
# Access: http://localhost:31500
```

### **Problem: Python Script Fails**
```bash
# Check cluster connection
kubectl cluster-info

# Reinstall dependencies
pip3 install --upgrade -r hero-solution/requirements.txt
```

### **Problem: Pods Stuck "Pending"**
```bash
# Check what's wrong
kubectl describe pod -n vote-app $(kubectl get pods -n vote-app -o name | head -1)
# Look at the "Events" section at the bottom
```

### **Problem: Everything is Broken**
```bash
# Nuclear reset - start fresh
kubectl delete namespace vote-app --force --grace-period=0
sleep 30
python3 hero-solution/deploy-vote-app.py
```

### **Need More Help?**
- 📖 Check detailed `troubleshooting.md`
- 🙋‍♂️ Ask your instructor
- 💬 Use workshop chat
- 👥 Help your neighbors (and get help!)

---

## 🧠 **WHAT YOU'RE LEARNING**

### **Technical Skills**
- **Python Kubernetes Client**: Programmatic cluster interaction
- **Resource Management**: Automated creation and configuration
- **Error Handling**: Production-grade failure management
- **Monitoring**: Real-time status tracking and observability
- **Best Practices**: Security, resources, health checks

### **DevOps Concepts**
- **Automation Benefits**: Reliability over manual processes
- **Infrastructure as Code**: Programmatic resource management
- **Observability**: Monitoring and status visibility
- **Error Recovery**: Graceful handling of failures
- **Production Patterns**: Enterprise-ready deployment strategies

### **Real-World Applications**
- 🏢 **Enterprise Deployments**: Scale these patterns for production
- 🔄 **CI/CD Integration**: Use in automated pipelines
- 📊 **Operations Tools**: Build custom monitoring and management
- 🛡️ **Site Reliability**: Reduce human error, increase reliability

---

## 🎉 **CELEBRATION CHECKPOINTS**

### **🎯 Milestone 1: Script Success**
When you see:
```
🎉 CHAOS AGENT DEFEATED!
✅ Vote app deployed successfully with Python automation
```
**Celebrate!** 🎉 You've automated Kubernetes deployment!

### **🎯 Milestone 2: App Access**
When your vote app loads in the browser:
**Take a screenshot!** 📸 Share your success!

### **🎯 Milestone 3: First Vote**
When you successfully cast your first vote:
**Vote for Python!** 🐍 (Just kidding - vote for your favorite!)

### **🎯 Milestone 4: Monitoring**
When the monitoring system shows green status:
**You're a DevOps Hero!** 🦸‍♂️ You can monitor production systems!

---

## 🚀 **BONUS CHALLENGES** (Optional)

If you finish early, try these enhancements:

### **Challenge 1: Multiple Environments**
```bash
# Deploy to a different namespace
# Edit deploy-vote-app.py and change:
# self.namespace = "vote-app-staging"
```

### **Challenge 2: Custom Configuration**
```bash
# Modify the poll question
# Edit the configmap data in deploy-vote-app.py
```

### **Challenge 3: Resource Scaling**
```bash
# Scale up the deployment
kubectl scale deployment vote-app --replicas=5 -n vote-app
# Watch in monitoring system
```

### **Challenge 4: Log Investigation**
```bash
# Check application logs
kubectl logs -n vote-app -l app=vote-app -f
# See real-time vote logging
```

---

## 🔄 **PREPARATION FOR NEXT SCENARIO**

### **Keep Your App Running!**
- 🚫 **Don't delete** the vote-app namespace
- ✅ **Keep it running** - we'll enhance it in Scenario 2
- 🔄 **Same Python environment** - dependencies are ready

### **What's Coming Next:**
- **Scenario 2**: Secret Management & Automation
- **Enhancement**: Add secure database with automated secret rotation
- **Same App**: We'll upgrade your vote app with enterprise security

### **Get Ready For:**
- 🔐 Kubernetes Secrets management
- 🔄 Automated credential rotation
- 🛡️ Security best practices
- 📊 Enhanced monitoring with security metrics

---

## 📝 **SCENARIO COMPLETION CHECKLIST**

Before moving to the next scenario, verify:

- [ ] ✅ Vote app is running and accessible
- [ ] ✅ You can vote and see results
- [ ] ✅ Monitoring system works
- [ ] ✅ You understand Python K8s automation benefits
- [ ] ✅ You took a screenshot of your working app
- [ ] ✅ You're excited about the next scenario!

### **Final Validation Commands:**
```bash
# Quick verification that everything is working
kubectl get all -n vote-app
kubectl get pods -n vote-app
curl -s http://localhost:31000 | grep -i vote  # If using NodePort
# OR
curl -s http://localhost:31500 | grep -i vote  # If using port-forward
```

**All should return successful results!**

---

## 🎊 **CONGRATULATIONS!**

**🎉 You've successfully defeated Chaos Agent in Scenario 1!**

You've proven that:
- ✅ **Python automation** beats manual chaos
- ✅ **Programmatic deployments** are reliable and repeatable  
- ✅ **Monitoring and observability** are essential
- ✅ **You have the skills** to build production-ready systems

**🚀 Ready for the next challenge?** Scenario 2 awaits, where we'll add enterprise-grade secret management to your vote app!

---

*"Every expert was once a beginner. Every pro was once an amateur. You're now a certified Chaos Slayer!"* 🦸‍♂️⚔️