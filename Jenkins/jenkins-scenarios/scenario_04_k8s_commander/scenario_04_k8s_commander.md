# 🚀 K8s Commander - Interactive Kubernetes Masterclass
**20-30 Minutes - Bridge Jenkins to Kubernetes**

*"Master Kubernetes concepts interactively before deploying to production"*

## 🎯 **The Challenge**

**Real-world scenario:** You're a Jenkins expert, but your team is moving to Kubernetes. You need to:
- 📚 Learn K8s concepts quickly
- 🏭 Understand production patterns
- 🧪 Practice safely before real deployments
- 🎯 Bridge CI/CD to container orchestration

**Your mission:** Master Kubernetes through an interactive learning platform deployed via Jenkins.

---

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Create Jenkins Pipeline**
```bash
# In Jenkins UI:
# 1. New Item → Pipeline
# 2. Name: scenario_04_k8s_commander
# 3. Pipeline script from SCM → Git
# 4. Repository URL: https://github.com/vellankikoti/ci-cd-chaos-workshop
# 5. Branch: jenkins-test
# 6. Script Path: Jenkins/jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile
```

### **Step 2: Configure Parameters**
```bash
K8S_CONCEPT: Pods              # Start with Pods
LEARNING_LEVEL: Beginner       # Choose your level
INTERACTIVE_DEMO: true         # Enable interactivity
HANDS_ON_LAB: true            # Enable labs
NAMESPACE: k8s-learning        # Default namespace
K8S_VERSION: 1.28             # K8s version
```

### **Step 3: Run & Access**
```bash
# 1. Click "Build with Parameters"
# 2. Wait ~30 seconds
# 3. Check console output for URL:
#    "🌐 Access your K8s Commander at: http://localhost:XXXX"
# 4. Open URL in browser
```

---

## 📚 **What You'll Master**

### **5 Kubernetes Concepts**
| Concept | What You'll Learn | Duration |
|---------|-------------------|----------|
| **Pods** | Container orchestration basics | 40 min |
| **Services** | Networking and load balancing | 45 min |
| **Deployments** | Rolling updates and scaling | 50 min |
| **ConfigMaps** | Configuration management | 35 min |
| **Secrets** | Secure secrets handling | 40 min |

### **Interactive Learning Platform Features**
- 📊 **Overview Tab**: Progress tracking and status
- 📚 **Lessons Tab**: 5 interactive lessons per concept
- 🏭 **Production Patterns Tab**: Real YAML examples
- 🧪 **Labs Tab**: Hands-on kubectl exercises
- 🚀 **Next Steps Tab**: Navigate to full K8s scenarios

---

## 🎓 **Learning Journey**

### **Lesson 1: Core Concepts (5 min)**
```yaml
# Example: What are Pods?
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```
**What you learn:** Basic K8s resource structure, YAML syntax, Pod lifecycle

### **Lesson 2: Advanced Patterns (8 min)**
```yaml
# Example: Multi-container Pod
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  containers:
  - name: app
    image: myapp:1.0
  - name: logging-sidecar
    image: fluentd:latest
```
**What you learn:** Sidecar pattern, container communication, shared volumes

### **Lesson 3: Production Patterns (10 min)**
```yaml
# Example: Production-ready Pod
apiVersion: v1
kind: Pod
metadata:
  name: production-pod
spec:
  containers:
  - name: app
    image: myapp:1.0
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 15
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
```
**What you learn:** Resource limits, health checks, security contexts, production best practices

### **Lesson 4: Scaling & Updates (12 min)**
```bash
# Hands-on kubectl commands
kubectl get pods -n k8s-learning
kubectl describe pod nginx-pod
kubectl logs nginx-pod -f
kubectl exec -it nginx-pod -- /bin/bash
kubectl delete pod nginx-pod
```
**What you learn:** Pod management, debugging, troubleshooting

### **Lesson 5: Real-World Scenarios (15 min)**
**What you learn:** Common production issues and solutions:
- Pod CrashLoopBackOff → How to debug
- ImagePullBackOff → Registry authentication
- Pending Pods → Resource constraints
- OOMKilled → Memory management

---

## 🏭 **Production Patterns Included**

### **1. Resource Management**
```yaml
resources:
  requests:
    memory: "64Mi"    # Scheduling guarantee
    cpu: "250m"
  limits:
    memory: "128Mi"   # Hard limit
    cpu: "500m"
```
**Why:** Prevents resource starvation, ensures fair scheduling

### **2. Health Checks**
```yaml
livenessProbe:       # Restart if unhealthy
  httpGet:
    path: /healthz
    port: 8080
readinessProbe:      # Remove from service if not ready
  httpGet:
    path: /ready
    port: 8080
```
**Why:** Automatic healing, zero-downtime deployments

### **3. Security**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```
**Why:** Defense in depth, principle of least privilege

### **4. Rolling Updates**
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```
**Why:** Zero-downtime deployments, gradual rollout

---

## 🎮 **Parameters Explained**

### **K8S_CONCEPT**
Choose which concept to learn:
- **Pods**: Start here (container basics)
- **Services**: Networking and discovery
- **Deployments**: Application management
- **ConfigMaps**: Configuration injection
- **Secrets**: Sensitive data handling

### **LEARNING_LEVEL**
- **Beginner**: Core concepts, simple examples
- **Intermediate**: Advanced patterns, use cases
- **Advanced**: Production architectures, troubleshooting

### **INTERACTIVE_DEMO**
- `true`: Full interactivity, copy buttons, navigation
- `false`: Static content only (shows warning banner)

### **HANDS_ON_LAB**
- `true`: Shows Labs tab with kubectl exercises
- `false`: Hides Labs tab (lessons only)

---

## 🔧 **Behind the Scenes**

### **What the Pipeline Does**
1. **Creates Dockerfile** with embedded Python web app
2. **Builds Docker image** with all lesson content
3. **Finds available port** (8081-8131) with retry logic
4. **Deploys container** with health checks
5. **Generates K8s examples** based on selected concept
6. **Creates lab exercises** with kubectl commands

### **Technology Stack**
- **Backend**: Python 3.11 with HTTPServer
- **Frontend**: HTML/CSS/JavaScript (no framework)
- **Container**: Docker with health checks
- **Port Management**: Automatic retry with TOCTTOU protection

### **API Endpoints**
```bash
GET /api/status          # System status and config
GET /api/concept         # Current K8s concept details
GET /api/learning-path   # Recommended learning steps
GET /api/lessons         # Available lessons list
GET /api/lesson/{id}     # Specific lesson content
```

---

## 🐛 **Troubleshooting**

### **Build Failed?**
```bash
# Check Docker is running
docker ps

# Check available ports
netstat -tuln | grep "808[0-9]"

# Clean up old containers
docker ps -a --filter "name=k8s-commander" --format "{{.Names}}" | xargs docker rm -f
```

### **Can't Access Web App?**
```bash
# 1. Find the port from Jenkins console output
# 2. Check container is running
docker ps --filter "name=k8s-commander"

# 3. Check port mapping
docker port k8s-commander-<BUILD_NUMBER>

# 4. Test API
curl http://localhost:<PORT>/api/status
```

### **Lessons Not Loading?**
```bash
# Check container logs
docker logs k8s-commander-<BUILD_NUMBER>

# Check browser console (F12)
# Look for JavaScript errors or failed fetch requests
```

### **Port Conflict?**
```bash
# The pipeline automatically tries ports 8081-8131
# If all are in use, clean up:
docker ps -a --filter "name=k8s-commander" --format "{{.Names}}" | xargs docker rm -f

# Or use cleanup script:
python3 cleanup.py
```

---

## 🧹 **Cleanup**

### **Stop Current Container**
```bash
docker stop k8s-commander-<BUILD_NUMBER>
docker rm k8s-commander-<BUILD_NUMBER>
```

### **Stop All K8s Commander Containers**
```bash
docker ps -a --filter "name=k8s-commander" --format "{{.Names}}" | xargs docker rm -f
```

### **Clean Up Images**
```bash
docker images | grep k8s-commander | awk '{print $3}' | xargs docker rmi -f
```

### **Use Cleanup Script**
```bash
cd Jenkins/jenkins-scenarios/scenario_04_k8s_commander
python3 cleanup.py
```

---

## 🎯 **Success Criteria**

After completing K8s Commander, you should be able to:

✅ Explain core Kubernetes concepts (Pods, Services, Deployments, etc.)
✅ Write production-ready YAML configurations
✅ Implement health checks and resource limits
✅ Use kubectl commands confidently
✅ Understand security best practices
✅ Debug common Kubernetes issues
✅ Deploy applications to K8s clusters

---

## 🚀 **Next Steps**

### **Kubernetes Scenarios**
After mastering K8s Commander, continue to:

1. **Kubernetes Scenario 1**: Python App Deployment
2. **Kubernetes Scenario 2**: Secret Automation
3. **Kubernetes Scenario 3**: Auto-Scaling
4. **Kubernetes Scenario 4**: Blue-Green Deployments
5. **Kubernetes Scenario 5**: GitOps with ArgoCD

### **Learning Path**
```
K8s Commander (Concepts)
    ↓
Kubernetes Scenario 1 (Python Deployment)
    ↓
Kubernetes Scenario 2 (Secrets)
    ↓
Kubernetes Scenario 3 (Auto-Scaling)
    ↓
Kubernetes Scenario 4 (Blue-Green)
```

---

## 📊 **What Makes This Special**

### **Interactive Learning**
- Click lessons to see full content
- Copy YAML with one click
- Navigate through modules
- Track your progress

### **Production Focus**
- Real-world patterns
- Security best practices
- Resource management
- Health checks

### **Safe Practice**
- Learn in isolated environment
- No real cluster needed
- Experiment freely
- Easy cleanup

### **Parameter-Driven**
- Different concepts
- Multiple levels
- Configurable features
- Flexible learning

---

## 🎓 **For Workshop Instructors**

### **Preparation Checklist**
- [ ] Jenkins running on localhost:8080
- [ ] Docker installed and running
- [ ] Ports 8081-8131 available
- [ ] Git repository accessible
- [ ] Cleanup script tested

### **Workshop Flow**
1. **Introduction** (5 min): Explain K8s Commander purpose
2. **Setup** (5 min): Guide through pipeline creation
3. **Exploration** (15 min): Let attendees explore concepts
4. **Discussion** (5 min): Review production patterns
5. **Q&A** (5 min): Answer questions

### **Common Questions**
**Q: Do we need a real K8s cluster?**
A: No! This is pure learning. Real deployments come in later scenarios.

**Q: Can we deploy these YAMLs?**
A: Yes! Copy the YAML and use in any K8s cluster.

**Q: How long does each concept take?**
A: 30-50 minutes per concept, but you can go at your own pace.

---

## 📦 **Files in This Scenario**

```
scenario_04_k8s_commander/
├── Jenkinsfile                    # Pipeline definition (82KB)
├── scenario_04_k8s_commander.md   # This documentation
├── cleanup.py                     # Cleanup utility
└── verify-fix.sh                  # Verification script
```

**Generated during runtime** (not in git):
- `Dockerfile` - Dynamic Docker image
- `webapp.port` - Current port number
- `k8s-demo/` - Sample K8s YAML files
- `k8s-lab/` - Lab instructions

---

## 💡 **Pro Tips**

1. **Start with Pods** - Foundation for everything else
2. **Try different levels** - See how complexity increases
3. **Copy the YAML** - Use in real clusters
4. **Do the labs** - Practice makes perfect
5. **Read production patterns** - Learn from the best

---

## 🌟 **Why K8s Commander?**

**Problem:** Jenkins users need to learn Kubernetes, but:
- Documentation is overwhelming
- No safe practice environment
- Hard to bridge CI/CD to K8s
- Production patterns are scattered

**Solution:** K8s Commander provides:
- ✅ Interactive learning in familiar Jenkins environment
- ✅ Safe practice without real cluster
- ✅ Production patterns from day one
- ✅ Smooth transition to real K8s deployments

---

## 📞 **Support**

**Issues?**
1. Check troubleshooting section above
2. Run `./verify-fix.sh` for diagnostics
3. Check Docker and Jenkins logs
4. Run `python3 cleanup.py` and retry

**Questions?**
- Review this documentation
- Check Jenkins console output
- Inspect container logs
- Ask your instructor

---

**Ready to command Kubernetes? Start your journey now!** 🚀✨

---

*Built with ❤️ for the Jenkins and Kubernetes community*
