# 🚀 Scenario 05: GitOps with ArgoCD & Argo Rollouts

**"Enterprise-Grade GitOps Defeats Deployment Chaos!"**

---

## 📖 **SCENARIO OVERVIEW**

### **The GitOps Challenge**
Chaos Agent has discovered that manual deployments lead to environment drift and inconsistent configurations! Different environments have different configurations, teams can't track what's deployed where, and the deployment process is a mess. There's no audit trail and no automated rollback capabilities.

### **The GitOps Hero Solution**
Deploy an enterprise-grade GitOps system using ArgoCD and Argo Rollouts that provides declarative, automated, and visual deployment management. Experience advanced deployment strategies with real-time monitoring and comprehensive dashboards!

### **What You'll Build**
- 🚀 **ArgoCD Application Management** with declarative GitOps workflows
- 📊 **Argo Rollouts Dashboard** for visual deployment strategies
- 🎭 **Canary Deployment** with gradual traffic shifting (25% → 50% → 75% → 100%)
- 🔵🔴 **Blue-Green Deployment** with environment switching and manual promotion
- 🔄 **Rolling Update Strategy** with pod-by-pod updates
- 👁️ **Real-time Monitoring** with comprehensive dashboards

---

## ⏱️ **TIME ALLOCATION**

| **Activity** | **Duration** | **Type** |
|--------------|--------------|----------|
| Live Demo (Instructor) | 10 minutes | 👀 Watch |
| ArgoCD & Argo Rollouts Setup | 5 minutes | 🛠️ Hands-on |
| Interactive Deployment Strategies | 15 minutes | 🎮 Interactive |
| Dashboard Monitoring | 5 minutes | 📊 Analysis |
| **Total** | **35 minutes** | |

---

## 🎯 **LEARNING OBJECTIVES**

By completing this scenario, you will:

✅ **Master** GitOps principles and ArgoCD workflows  
✅ **Implement** advanced deployment strategies with Argo Rollouts  
✅ **Experience** visual deployment management and monitoring  
✅ **Learn** enterprise-grade deployment automation  
✅ **Understand** declarative infrastructure management  
✅ **Defeat** Chaos Agent's deployment inconsistency attacks! 🚀

---

## 🧨 **THE CHAOS AGENT'S GITOPS ATTACK**

> *"Your manual deployments are inconsistent! Different environments have different configurations! Your team can't track what's deployed where! Your deployment process is a mess!"* 😈

**What Chaos Agent Exploits:**
- ❌ Manual deployments lead to environment drift
- ❌ No audit trail of what's deployed
- ❌ Inconsistent deployment processes across teams
- ❌ No automated rollback capabilities
- ❌ Lack of deployment strategy visualization
- ❌ No declarative infrastructure management

---

## 🦸‍♂️ **THE GITOPS HERO'S RESPONSE**

> *"Enter the world of GitOps! ArgoCD and Argo Rollouts will provide declarative, automated, and visual deployment management. Watch as I demonstrate enterprise-grade GitOps workflows!"* 🦸‍♂️🚀

**How GitOps Hero Wins:**
- ✅ **Declarative GitOps workflows** - Infrastructure as code
- ✅ **Automated deployment management** - Git-driven deployments
- ✅ **Visual deployment strategies** - Real-time dashboard monitoring
- ✅ **Advanced deployment strategies** - Canary, blue-green, rolling
- ✅ **Comprehensive audit trails** - Complete deployment history
- ✅ **Instant rollback capabilities** - Automated reversion
- ✅ **Multi-environment management** - Consistent deployments

---

## 📁 **FILE STRUCTURE**

```
scenarios/05-gitops/
├── README.md                          # This comprehensive guide
├── argocd-apps/
│   ├── app-of-apps.yaml              # ArgoCD Application of Applications
│   └── apps/                         # Individual ArgoCD Applications
│       ├── frontend.yaml             # Points to overlays/rollouts
│       ├── recommendationservice.yaml # Points to overlays/rollouts
│       └── [other services].yaml
├── services/                         # Base manifests (ClusterIP, Deployments)
│   ├── frontend/
│   │   ├── service-frontend.yaml     # ClusterIP
│   │   ├── service-frontend-external.yaml # NodePort (30081)
│   │   ├── deployment-frontend.yaml
│   │   └── serviceaccount-frontend.yaml
│   └── [other services]/
├── overlays/
│   ├── local/
│   │   └── frontend/
│   │       └── service-frontend-external.yaml # NodePort (30081)
│   ├── cloud/
│   │   └── frontend/
│   │       └── service-frontend-external.yaml # LoadBalancer
│   └── rollouts/                     # Advanced deployment strategies
│       ├── frontend-rollout.yaml     # Canary deployment
│       ├── frontend-preview-service.yaml
│       ├── recommendationservice-rollout.yaml # Blue-green deployment
│       ├── recommendationservice-preview-service.yaml
│       └── analysis-template.yaml    # Health checks
├── scripts/
│   ├── interactive-demo.sh           # Interactive demo script
│   ├── setup.sh
│   ├── teardown.sh
│   ├── switch-overlay.sh
│   └── reset-demo.sh
└── scenario_05_gitops_argocd.md     # Complete handbook
```

---

## 🚀 **QUICK START** (For Participants)

### **Prerequisites**
- ✅ **Scenario 4 completed** (blue-green demo should still be running)
- ✅ Kubernetes cluster running (Docker Desktop, Minikube, or cloud)
- ✅ kubectl configured and working
- ✅ ArgoCD CLI installed (optional but recommended)

### **Step 1: Install ArgoCD & Argo Rollouts** (3 minutes)
```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Install Argo Rollouts
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/dashboard-install.yaml
```

### **Step 2: Access Dashboards** (2 minutes)
```bash
# Start ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
# Visit http://localhost:8080

# Start Argo Rollouts UI
kubectl port-forward deployment/argo-rollouts-dashboard -n argo-rollouts 3100:3100 &
# Visit http://localhost:3100 (switch to gitops-demo namespace)
```

### **Step 3: Get ArgoCD Admin Password**
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
# Username: admin
# Password: (output from above)
```

### **Step 4: Bootstrap the App-of-Apps** (2 minutes)
```bash
# Navigate to gitops scenario
cd scenarios/05-gitops

# Bootstrap ArgoCD applications
kubectl apply -f argocd-apps/app-of-apps.yaml
```

**Expected Output:**
```
🚀 GITOPS WITH ARGOCD & ARGO ROLLOUTS
======================================================================
🔧 Installing ArgoCD and Argo Rollouts...
✅ ArgoCD installed successfully
✅ Argo Rollouts installed successfully
🌐 Starting dashboards...
✅ ArgoCD UI: http://localhost:8080
✅ Argo Rollouts UI: http://localhost:3100
🔐 Getting admin credentials...
✅ Username: admin
✅ Password: <auto-generated>
🚀 Bootstrapping applications...
✅ App-of-apps pattern deployed
⏳ Syncing applications...
✅ All applications synced successfully

======================================================================
🎉 GITOPS DEPLOYMENT SUCCESSFUL!
✅ Enterprise-grade GitOps ready!
======================================================================

🎯 ACCESS YOUR GITOPS DASHBOARDS:
   🔧 ArgoCD UI: http://localhost:8080 (admin/<password>)
   📊 Argo Rollouts UI: http://localhost:3100 (switch to gitops-demo namespace)
   🌐 Demo App: http://localhost:8080 (via port-forward)
```

### **Step 5: Access Your GitOps Dashboards** (Immediate)

#### **🔧 ArgoCD UI:**
```
💻 Primary: http://localhost:8080
👤 Username: admin
🔐 Password: <auto-generated>
```

#### **📊 Argo Rollouts UI:**
```
💻 Primary: http://localhost:3100
⚠️ Important: Switch namespace to gitops-demo
```

#### **🌐 Demo Application:**
```bash
# Port forward to demo app
kubectl port-forward service/frontend-external 8080:80 -n gitops-demo
# Then access: http://localhost:8080
```

### **Step 6: Interactive Deployment Strategies** (15 minutes)

1. **🎭 Canary Deployment (Frontend)**:
   - Edit `overlays/rollouts/frontend-rollout.yaml`
   - Change image tag to trigger canary
   - Watch traffic shift: 25% → 50% → 75% → 100%
   - Use Argo Rollouts UI to promote/rollback

2. **🔵🔴 Blue-Green Deployment (Recommendationservice)**:
   - Edit `overlays/rollouts/recommendationservice-rollout.yaml`
   - Change image tag to trigger blue-green
   - Watch blue (stable) and green (preview) environments
   - Use Argo Rollouts UI to promote green to blue

3. **🔄 Rolling Update Strategy**:
   - Edit deployment manifests
   - Watch pod-by-pod updates
   - Experience zero-downtime deployments

### **Step 7: Dashboard Monitoring** (5 minutes)

1. **📊 ArgoCD Dashboard**:
   - View application health and sync status
   - Monitor deployment history
   - Check resource synchronization

2. **📈 Argo Rollouts Dashboard**:
   - Visual deployment progress
   - Traffic shifting visualization
   - Health check monitoring

---

## 🎬 **LIVE DEMO WALKTHROUGH** (For Instructors)

### **Demo Script Overview**

#### **Part 1: GitOps Chaos Exposed (3 minutes)**
```bash
# Show deployment inconsistency chaos
./demo-script.sh
```

**What Students See:**
1. Manual deployments causing environment drift
2. No audit trail of deployments
3. Inconsistent configurations
4. "This is deployment chaos!"

#### **Part 2: GitOps Hero Saves the Day (4 minutes)**
```bash
# Deploy ArgoCD and Argo Rollouts
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl apply -f argocd-apps/app-of-apps.yaml
```

**Key Teaching Points:**
- 🚀 **Declarative GitOps workflows**
- 🚀 **Automated deployment management**
- 🚀 **Visual deployment strategies**
- 🚀 **Comprehensive monitoring**

#### **Part 3: Interactive Strategy Testing (3 minutes)**
- Demonstrate canary deployment
- Show blue-green switching
- Highlight dashboard monitoring
- Celebrate GitOps victory!

---

## 🚀 **GITOPS CONFIGURATION**

### **1. ArgoCD Application of Applications**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-of-apps
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/vellankikoti/ci-cd-chaos-workshop
    targetRevision: HEAD
    path: Kubernetes/kubernetes-scenarios/05-gitops/argocd-apps
  destination:
    server: https://kubernetes.default.svc
    namespace: gitops-demo
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### **2. Frontend Application**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: frontend
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/vellankikoti/ci-cd-chaos-workshop
    targetRevision: HEAD
    path: Kubernetes/kubernetes-scenarios/05-gitops/overlays/rollouts
  destination:
    server: https://kubernetes.default.svc
    namespace: gitops-demo
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### **3. Canary Deployment Strategy**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: frontend
  namespace: gitops-demo
spec:
  replicas: 4
  strategy:
    canary:
      steps:
      - setWeight: 25
      - pause: {}
      - setWeight: 50
      - pause: {}
      - setWeight: 75
      - pause: {}
      - setWeight: 100
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: server
        image: us-central1-docker.pkg.dev/google-samples/microservices-demo/frontend:v0.10.3
        ports:
        - containerPort: 8080
```

### **4. Blue-Green Deployment Strategy**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: recommendationservice
  namespace: gitops-demo
spec:
  replicas: 2
  strategy:
    blueGreen:
      activeService: recommendationservice
      previewService: recommendationservice-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
  selector:
    matchLabels:
      app: recommendationservice
  template:
    metadata:
      labels:
        app: recommendationservice
    spec:
      containers:
      - name: server
        image: us-central1-docker.pkg.dev/google-samples/microservices-demo/recommendationservice:v0.10.3
        ports:
        - containerPort: 8080
```

---

## 🧪 **GITOPS TESTING**

### **Test 1: Canary Deployment**
```bash
# Trigger canary deployment
kubectl apply -f overlays/rollouts/frontend-rollout.yaml

# Watch progress in Argo Rollouts UI
# Visit http://localhost:3100 and switch to gitops-demo namespace
```

### **Test 2: Blue-Green Deployment**
```bash
# Trigger blue-green deployment
kubectl apply -f overlays/rollouts/recommendationservice-rollout.yaml

# Watch environments in Argo Rollouts UI
# Promote green to blue when ready
kubectl argo rollouts promote recommendationservice -n gitops-demo
```

### **Test 3: GitOps Sync**
```bash
# Check ArgoCD applications
kubectl get applications -n argocd

# Force sync with latest revision
kubectl patch application frontend -n argocd --type='merge' -p='{"spec":{"source":{"targetRevision":"HEAD"}}}'
```

### **Test 4: Rollback Capability**
```bash
# Rollback to previous version
kubectl argo rollouts rollback frontend -n gitops-demo

# Check rollback status
kubectl get rollout frontend -n gitops-demo
```

---

## 📊 **GITOPS MONITORING**

### **ArgoCD Dashboard Monitoring**
```bash
# Check application health
kubectl get applications -n argocd

# View sync status
kubectl describe application frontend -n argocd

# Check deployment history
kubectl get events -n argocd --sort-by='.lastTimestamp'
```

### **Argo Rollouts Dashboard Monitoring**
```bash
# Check rollout status
kubectl get rollouts -n gitops-demo

# View rollout details
kubectl describe rollout frontend -n gitops-demo

# Monitor traffic shifting
kubectl get services -n gitops-demo
```

### **Real-time Metrics**
```bash
# Monitor pod status
kubectl get pods -n gitops-demo -w

# Check resource usage
kubectl top pods -n gitops-demo

# View application logs
kubectl logs -f deployment/frontend -n gitops-demo
```

---

## 🎯 **SUCCESS CRITERIA**

### ✅ **Scenario 05 Complete Checklist:**
- ✅ ArgoCD installed and accessible
- ✅ Argo Rollouts installed and functional
- ✅ App-of-apps pattern deployed
- ✅ Canary deployment strategy working
- ✅ Blue-green deployment strategy operational
- ✅ Dashboard monitoring functional
- ✅ GitOps workflows automated
- ✅ Chaos Agent's deployment inconsistency attacks defeated! 🚀

### **Key Learning Outcomes:**
- ✅ **GitOps Principles** - Mastered declarative infrastructure
- ✅ **ArgoCD Management** - Implemented application automation
- ✅ **Argo Rollouts** - Experienced advanced deployment strategies
- ✅ **Dashboard Monitoring** - Applied visual deployment management
- ✅ **Automated Workflows** - Built Git-driven deployments
- ✅ **Enterprise Patterns** - Implemented production-ready GitOps

---

## 🚀 **NEXT STEPS**

### **What's Next:**
- **Production GitOps** - Apply these patterns to real applications
- **Advanced ArgoCD** - Explore more complex application patterns
- **Multi-Cluster GitOps** - Deploy across multiple environments
- **Custom Rollout Strategies** - Build application-specific strategies

### **Production GitOps:**
- Implement comprehensive GitOps workflows
- Add security scanning and compliance
- Build automated testing pipelines
- Regular GitOps strategy reviews

---

## 🆘 **TROUBLESHOOTING**

### **Common GitOps Issues:**

#### **Issue: ArgoCD not syncing applications**
```bash
# Solution: Check application status
kubectl get applications -n argocd
kubectl describe application frontend -n argocd
```

#### **Issue: Rollouts not visible in dashboard**
```bash
# Solution: Switch namespace in Argo Rollouts UI
# Navigate to http://localhost:3100 and select gitops-demo namespace
```

#### **Issue: Canary deployment stuck**
```bash
# Solution: Promote the rollout
kubectl argo rollouts promote frontend -n gitops-demo
```

#### **Issue: Blue-green not switching**
```bash
# Solution: Check service selectors
kubectl get services -n gitops-demo
kubectl describe service recommendationservice -n gitops-demo
```

---

## 🎉 **CONCLUSION**

**Congratulations! You've successfully defeated Chaos Agent's deployment inconsistency attacks!** 🚀

### **What You've Accomplished:**
- ✅ **Implemented enterprise-grade GitOps** with ArgoCD
- ✅ **Mastered advanced deployment strategies** with Argo Rollouts
- ✅ **Created visual deployment management** with dashboards
- ✅ **Built automated GitOps workflows** for consistency
- ✅ **Applied declarative infrastructure** principles

### **Key GitOps Takeaways:**
- **GitOps provides consistency** across all environments
- **Declarative infrastructure** ensures reproducibility
- **Visual dashboards** improve deployment visibility
- **Advanced strategies** enable safe deployments
- **Automation reduces** human error and deployment time

**You've completed all 5 Kubernetes scenarios and are now a GitOps master! 🎉**

---

**Remember:** In the world of GitOps, automation and consistency are your superpowers against chaos! 🚀 