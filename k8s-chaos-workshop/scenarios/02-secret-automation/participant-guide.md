# 🔐 Scenario 2: Participant Guide

**"Defeat Chaos Agent's Security Attacks with Python Automation!"**

---

## 🎭 **YOUR SECURITY MISSION**

Chaos Agent has escalated the attack! Now they're targeting your secrets and trying to steal your database credentials. Your mission is to deploy a bulletproof todo application with enterprise-grade secret management that makes data theft impossible.

**Time Limit**: 30 minutes  
**Difficulty**: ⭐⭐⭐☆☆ (Intermediate Security Focus)

---

## ✅ **PREREQUISITES CHECKLIST**

Before starting, verify you have:

- [ ] **Scenario 1 completed** (vote app should still be running)
- [ ] **Kubernetes cluster running** (same as Scenario 1)
- [ ] **Python 3.8+** with security libraries
- [ ] **kubectl configured** and working
- [ ] **Workshop repository** cloned
- [ ] **Terminal/Command Prompt** open

### **Quick Security Environment Check**
```bash
# Run these commands - all should work:
kubectl cluster-info                    # Shows cluster info
python3 --version                       # Shows Python 3.8+
kubectl get namespaces | grep vote-app  # Should show vote-app from Scenario 1
pip3 list | grep kubernetes            # Should show kubernetes library
```

If any fail, ask for help before proceeding! 🆘

---

## 🚀 **STEP-BY-STEP EXECUTION**

### **Step 1: Navigate to Security Scenario** (30 seconds)
```bash
# Go to the security scenario folder
cd scenarios/02-secret-management

# Verify you're in the right place
ls -la
# Should see: hero-solution/, chaos/, README.md, etc.
```

### **Step 2: Install Security Dependencies** (2 minutes)
```bash
# Install additional security libraries
pip3 install -r hero-solution/requirements.txt

# Key security dependencies:
# - cryptography (for secure password generation)
# - mysql-connector-python (for database connectivity)

# If you get permission errors:
pip3 install --user -r hero-solution/requirements.txt

# Or use virtual environment:
python3 -m venv security-venv
source security-venv/bin/activate  # Linux/Mac
# security-venv\Scripts\activate   # Windows
pip3 install -r hero-solution/requirements.txt
```

### **Step 3: Watch the Security Demo** (10 minutes)
Your instructor will demonstrate:

1. **🧨 Chaos Agent's Security Attack**: 
   - Exposed passwords in YAML files
   - Database accessible from internet
   - Missing security configurations

2. **🔐 Python Security Hero's Response**: 
   - Automated secure secret generation
   - Enterprise-grade secret management
   - Zero-downtime secret rotation

3. **🛡️ Security Victory**: 
   - Bulletproof todo app with encrypted secrets
   - Real-time security monitoring

**Pay attention to**: The difference between exposed secrets and secure automation!

### **Step 4: Deploy Your Secure Todo App** (5 minutes)
```bash
# Run the security hero automation
python3 hero-solution/deploy-secure-todo.py
```

**Expected Output**:
```
🎭 SCENARIO 2: Chaos Attacks Your Secrets!
🔐 Python Security Hero to the rescue!

🔐 Initializing Enterprise Secret Management...
✅ Security system armed and ready!
======================================================================
🔐 PYTHON SECURITY HERO DEPLOYMENT STARTING
======================================================================
🏠 Creating secure namespace: secure-todo
✅ Secure namespace created
🔐 Generating secure MySQL credentials...
✅ MySQL secrets created with enterprise security
🔑 Generating application security tokens...
✅ Application secrets created with rotation policy
🗄️ Deploying secure MySQL database...
✅ Secure MySQL deployed with secret integration
📝 Deploying secure todo application...
✅ Secure todo app deployed with encrypted secrets
🌐 Creating secure network services...
✅ Secure services created with proper network isolation
⏳ Waiting for secure deployments to be ready...
📊 Checking secure-mysql...
✅ secure-mysql ready! 1/1 pods
📊 Checking secure-todo-app...
✅ secure-todo-app ready! 2/2 pods
🌐 Getting secure access information...
🎯 ACCESS YOUR SECURE TODO APP:
   💻 NodePort: http://localhost:31001
   🔧 Port Forward: kubectl port-forward svc/secure-todo-service -n secure-todo 31501:80
   🌍 Then access: http://localhost:31501

======================================================================
🎉 CHAOS AGENT'S SECURITY ATTACK DEFEATED!
✅ Secure todo app deployed with enterprise-grade secrets
======================================================================
```

### **Step 5: Access Your Secure Todo Application** (5 minutes)

The script will provide **environment-specific access instructions**:

#### **🐳 Docker Desktop:**
```
💻 Try: http://localhost:31001
```

#### **🎯 Minikube:**
```bash
# Use Minikube IP
minikube service secure-todo-service -n secure-todo --url
```

#### **☁️ Cloud (EKS/GKE/AKS):**
```bash
# Get node external IP
kubectl get nodes -o wide
# Access: http://<external-ip>:31001
```

#### **🌐 Universal Access (Always Works):**
```bash
# Port forwarding (no conflicts with Jenkins/MkDocs)
kubectl port-forward svc/secure-todo-service -n secure-todo 31501:80
# Access: http://localhost:31501
```

### **Step 6: Test Your Secure Todo App** (5 minutes)

Once you have the todo app open:

1. **📝 Add Todo Items**:
   - Click "Add Todo" or similar button
   - Enter todo text: "Learn Kubernetes Security"
   - Save the todo item

2. **✅ Mark Items Complete**:
   - Check off completed items
   - See status change in real-time

3. **🗑️ Delete Items**:
   - Remove unwanted todo items
   - Verify deletion works

4. **🔐 Test Data Persistence**:
   - Refresh the browser
   - Verify todos are saved in secure database
   - Add more items from different browsers

### **Step 7: Test Secret Rotation** (5 minutes)
```bash
# Run automated secret rotation
python3 hero-solution/rotate-secrets.py
```

**Expected Rotation Process**:
```
🔄 Secret Rotation System
Choose monitoring mode:
   1. One-time security scan
   2. Continuous security monitoring

Enter choice (1 or 2): 1

🔄 Initializing Secret Rotation System...
✅ Rotation system ready!
============================================================
🔄 STARTING AUTOMATED SECRET ROTATION
============================================================
📊 Secret Age Analysis:
   MySQL credentials: 0 days old
   App credentials: 0 days old
✅ Secrets are fresh - no rotation needed
🔄 Force rotation anyway? (y/n): y

🔄 Rotating MySQL credentials...
✅ MySQL credentials rotated successfully
🔑 Rotating application secrets...
✅ Application secrets rotated successfully
🔄 Restarting deployments to pick up new secrets...
✅ secure-mysql restart initiated
✅ secure-todo-app restart initiated
⏳ Waiting for rollout to complete...
📊 Checking secure-mysql rollout...
✅ secure-mysql rollout complete!
📊 Checking secure-todo-app rollout...
✅ secure-todo-app rollout complete!

============================================================
🎉 SECRET ROTATION COMPLETED SUCCESSFULLY!
✅ Zero downtime achieved - Chaos Agent thwarted!
============================================================
```

### **Step 8: Monitor Security Status** (5 minutes)
```bash
# Run security monitoring dashboard
python3 hero-solution/security-monitor.py
```

**Choose monitoring option**:
```
🔒 Security Monitoring System
Choose monitoring mode:
   1. One-time security scan
   2. Continuous security monitoring

Enter choice (1 or 2): 1
```

**Security Dashboard Output**:
```
🔒 SECURITY MONITORING DASHBOARD
============================================================
🕐 Scan Time: 14:30:15
🏠 Namespace: secure-todo

🔐 SECRET SECURITY STATUS:
   ✅ SECURE mysql-credentials
      Age: 0 days | Policy: 30-days
      Rotations: 2 | Level: high
   ✅ SECURE app-credentials
      Age: 0 days | Policy: 7-days
      Rotations: 1 | Level: high

🚀 DEPLOYMENT SECURITY STATUS:
   ✅ EXCELLENT secure-mysql
      Security Score: 5/5 | Replicas: 1/1
   ✅ EXCELLENT secure-todo-app
      Security Score: 5/5 | Replicas: 2/2

🌐 NETWORK SECURITY STATUS:
   Services: 2 total
   🔒 Internal: 1 | 🌐 External: 1
      🔒 Internal secure-mysql-service (ClusterIP) - Ports: 3306:3306
      🌐 External secure-todo-service (NodePort) - Ports: 80:5000

📊 OVERALL SECURITY STATUS:
   🛡️ EXCELLENT - All security controls are compliant
   ✅ Chaos Agent's attacks have been thwarted!
```

---

## 🎯 **SUCCESS CRITERIA**

### **✅ You've Successfully Completed This Scenario When:**

- [ ] **Secure Deployment Succeeds**
  ```bash
  kubectl get pods -n secure-todo
  # Should show: secure-mysql-xxx   1/1   Running   0   XXm
  #              secure-todo-app-xxx 1/1   Running   0   XXm
  ```

- [ ] **Todo Application Works**
  - [ ] Todo app loads in browser
  - [ ] You can add todo items
  - [ ] You can mark items complete
  - [ ] You can delete items
  - [ ] Data persists after browser refresh

- [ ] **Security Features Work**
  - [ ] Secret rotation completes without errors
  - [ ] Security monitoring shows "EXCELLENT" status
  - [ ] Database is internal-only (ClusterIP service)
  - [ ] No secrets visible in plain text

- [ ] **Understanding Gained**
  - [ ] You can explain why hardcoded secrets are dangerous
  - [ ] You understand Kubernetes Secrets vs ConfigMaps
  - [ ] You recognize automated secret rotation benefits
  - [ ] You can identify security best practices

---

## 🔐 **SECURITY CONCEPTS LEARNED**

### **Secret Management:**
- **Kubernetes Secrets**: Encrypted storage vs plain text
- **Secret Rotation**: Automated credential lifecycle
- **Secret References**: Environment variables vs volume mounts
- **Secret Metadata**: Rotation policies and audit trails

### **Database Security:**
- **Network Isolation**: ClusterIP vs NodePort services
- **Authentication**: Secure credential management
- **Access Control**: Least privilege principles
- **Encryption**: Data protection in transit and at rest

### **Container Security:**
- **Security Contexts**: Non-root execution
- **Resource Limits**: Preventing resource exhaustion
- **Health Checks**: Detecting security failures
- **Image Security**: Using trusted base images

### **Monitoring & Compliance:**
- **Security Dashboards**: Real-time status monitoring
- **Compliance Tracking**: Policy enforcement
- **Audit Trails**: Security event logging
- **Automated Remediation**: Self-healing security

---

## 🚨 **TROUBLESHOOTING QUICK FIXES**

### **Problem: Can't Access Todo App**
```bash
# Universal solution
kubectl port-forward svc/secure-todo-service -n secure-todo 31501:80
# Access: http://localhost:31501
```

### **Problem: Secret Rotation Fails**
```bash
# Check RBAC permissions
kubectl auth can-i update secrets --namespace secure-todo

# Force recreation
kubectl delete secret mysql-credentials app-credentials -n secure-todo
python3 hero-solution/deploy-secure-todo.py
```

### **Problem: Database Connection Fails**
```bash
# Check MySQL status
kubectl logs -n secure-todo -l app=secure-mysql

# Test database connectivity
kubectl exec -n secure-todo deployment/secure-todo-app -- nc -zv secure-mysql-service 3306
```

### **Problem: Security Monitor Shows Issues**
```bash
# Check deployment configurations
kubectl describe deployment secure-mysql -n secure-todo
kubectl describe deployment secure-todo-app -n secure-todo

# Redeploy with security fixes
python3 hero-solution/deploy-secure-todo.py
```

### **Need More Help?**
- 📖 Check detailed `troubleshooting.md`
- 🙋‍♂️ Ask your instructor
- 💬 Use workshop chat
- 🔒 Remember: Security issues are learning opportunities!

---

## 🎉 **CELEBRATION CHECKPOINTS**

### **🎯 Milestone 1: Secure Deployment Success**
When you see:
```
🎉 CHAOS AGENT'S SECURITY ATTACK DEFEATED!
✅ Secure todo app deployed with enterprise-grade secrets
```
**Celebrate!** 🎉 You've implemented enterprise security!

### **🎯 Milestone 2: Todo App Access**
When your secure todo app loads in the browser:
**Take a screenshot!** 📸 You've defeated security chaos!

### **🎯 Milestone 3: First Todo Item**
When you successfully add your first secure todo:
**Add "Defeated Chaos Agent's Security Attacks"** ✅

### **🎯 Milestone 4: Secret Rotation Success**
When secret rotation completes:
**You're a Security Hero!** 🦸‍♂️ Zero-downtime security achieved!

### **🎯 Milestone 5: Security Monitoring**
When security monitoring shows "EXCELLENT":
**You've mastered Kubernetes security!** 🛡️

---

## 🚀 **BONUS SECURITY CHALLENGES** (Optional)

If you finish early, try these advanced security tasks:

### **Challenge 1: Security Audit**
```bash
# Compare vote app (Scenario 1) vs secure todo app security
kubectl get deployment vote-app -n vote-app -o yaml | grep -A 5 securityContext
kubectl get deployment secure-todo-app -n secure-todo -o yaml | grep -A 5 securityContext

# What security improvements do you notice?
```

### **Challenge 2: Network Security**
```bash
# Test network isolation
kubectl exec -n secure-todo deployment/secure-todo-app -- nc -zv secure-mysql-service 3306
# Should work (internal access)

kubectl run test-pod --image=busybox -it --rm -- nc -zv secure-mysql-service.secure-todo.svc.cluster.local 3306
# Should fail (external access blocked)
```

### **Challenge 3: Secret Forensics**
```bash
# Investigate secret metadata without exposing values
kubectl describe secret mysql-credentials -n secure-todo
kubectl get secret mysql-credentials -n secure-todo -o jsonpath='{.metadata.annotations}'

# What security metadata do you find?
```

### **Challenge 4: Simulate Security Incident**
```bash
# Try to access secrets from todo app container
kubectl exec -n secure-todo deployment/secure-todo-app -- env | grep -i secret
# Should show only references, not actual values

# Try to access MySQL from outside namespace
kubectl run hacker-pod --image=mysql:8.0 -it --rm -- mysql -h secure-mysql-service.secure-todo.svc.cluster.local -u root -p
# Should fail (network isolation working)
```

---

## 🔄 **PREPARATION FOR NEXT SCENARIO**

### **Keep Your Security Stack Running!**
- 🚫 **Don't delete** the secure-todo namespace
- ✅ **Keep it running** - we'll enhance it in Scenario 3
- 🔄 **Same Python environment** - security dependencies ready

### **What's Coming Next:**
- **Scenario 3**: Auto-scaling and Performance Management
- **Enhancement**: Add intelligent scaling to your secure applications
- **Same Security**: All security features maintained and enhanced

### **Get Ready For:**
- 📊 Python-powered auto-scaling
- 🔄 Custom metrics and scaling triggers
- 📈 Performance monitoring and optimization
- 🛡️ Security-aware scaling policies

---

## 📝 **SCENARIO COMPLETION CHECKLIST**

Before moving to the next scenario, verify:

- [ ] ✅ Secure todo app is running and accessible
- [ ] ✅ You can manage todo items successfully
- [ ] ✅ Secret rotation works without downtime
- [ ] ✅ Security monitoring shows "EXCELLENT" status
- [ ] ✅ You understand enterprise security concepts
- [ ] ✅ You took a screenshot of security dashboard
- [ ] ✅ You're excited about scaling secure applications!

### **Final Security Validation Commands:**
```bash
# Quick verification that security is working
kubectl get all -n secure-todo
kubectl get secrets -n secure-todo
python3 hero-solution/security-monitor.py | grep "OVERALL SECURITY STATUS" -A 2
```

**All should return successful, secure results!**

---

## 🎊 **CONGRATULATIONS!**

**🎉 You've successfully defeated Chaos Agent's security attacks in Scenario 2!**

You've proven that:
- ✅ **Enterprise security** can be automated with Python
- ✅ **Secret management** prevents data breaches  
- ✅ **Zero-downtime rotation** maintains security without service interruption
- ✅ **Security monitoring** provides real-time protection
- ✅ **You have the skills** to build production-ready secure systems

**🚀 Ready for the next challenge?** Scenario 3 awaits, where we'll add intelligent auto-scaling to your secure applications while maintaining all security protections!

---

*"Security is not a destination, it's a journey. And you're now a certified Security Slayer!"* 🦸‍♂️🔐⚔️