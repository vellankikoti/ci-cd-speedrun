# 🚀 Scenario 04: K8s Commander - Interactive Kubernetes Masterclass

**Duration**: 20-30 minutes
**Level**: Beginner to Intermediate
**Goal**: Learn Kubernetes concepts interactively before deploying to production

---

## 🎯 What is K8s Commander?

K8s Commander is an **interactive web-based learning platform** that bridges the gap between Jenkins CI/CD expertise and Kubernetes knowledge. It provides a hands-on masterclass experience that prepares you for real Kubernetes deployments.

### 🌟 Key Features

✅ **Interactive Tabbed Interface** - Navigate between Overview, Lessons, Production Patterns, Labs, and Next Steps
✅ **Progress Tracking** - Monitor your learning journey with visual progress indicators
✅ **Production-Ready Patterns** - Learn real-world best practices with YAML examples
✅ **Hands-on Labs** - Practice with actual kubectl commands
✅ **Bridge to K8s Scenarios** - Seamless transition to full Kubernetes deployment
✅ **Beautiful UI** - Modern, responsive design with smooth animations

---

## 🚀 Quick Start

### Run from Jenkins

1. **Create Pipeline Job** in Jenkins:
   - New Item → Pipeline
   - Name: `scenario_04_k8s_commander`
   - Pipeline → Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop`
   - Branch: `jenkins-test`
   - Script Path: `Jenkins/jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile`

2. **Configure Parameters** (automatically available):
   - **K8S_CONCEPT**: Pods, Services, Deployments, ConfigMaps, Secrets
   - **LEARNING_LEVEL**: Beginner, Intermediate, Advanced
   - **NAMESPACE**: k8s-learning (default)
   - **K8S_VERSION**: 1.28 (default)
   - **INTERACTIVE_DEMO**: true (enable interactive features)
   - **HANDS_ON_LAB**: true (enable lab exercises)

3. **Run the Pipeline** → Access the web application at the provided URL

---

## 📚 What You'll Learn

### Tab 1: 📊 Overview
- Current learning focus and configuration
- Progress tracking with visual indicators
- Learning statistics and time estimates
- Interactive features status

### Tab 2: 📚 Lessons
Interactive modules covering:
1. **What are Pods?** (5 min) - Core concepts
2. **Pod Lifecycle** (8 min) - States and transitions
3. **Multi-Container Pods** (10 min) - Sidecar patterns
4. **Production Patterns** (12 min) - Real-world best practices
5. **Hands-on Lab** (15 min) - Practical exercises

### Tab 3: 🏭 Production Patterns
Production-ready configurations with real YAML:

#### ⚡ Resource Limits & Requests
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

#### 🔍 Health Checks & Probes
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

#### 🛡️ Security Best Practices
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

#### 🔄 Rolling Updates
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

### Tab 4: 🧪 Hands-on Labs
Practice kubectl commands:
```bash
# Lab 1: Create Your First Pod
kubectl apply -f k8s-demo/pod-demo.yaml

# Lab 2: Check Pod Status
kubectl get pods -n k8s-learning
kubectl describe pod nginx-pod

# Lab 3: View Logs
kubectl logs nginx-pod -n k8s-learning

# Lab 4: Execute Commands
kubectl exec -it nginx-pod -- /bin/bash
```

### Tab 5: 🚀 Next Steps
Navigate to full Kubernetes deployment scenarios:
- **Scenario 1**: Python App Deployment
- **Scenario 2**: Secret Automation
- **Scenario 3**: Auto-Scaling
- **Scenario 4**: Blue-Green Deployments

---

## 🎓 Learning Path

### Beginner Track
1. Learn basic K8s concepts
2. Understand Pod lifecycle
3. Practice with simple deployments
4. Explore basic networking

### Intermediate Track
1. Master Service types
2. Learn advanced Pod patterns
3. Practice rolling updates
4. Explore configuration management

### Advanced Track
1. Design complex architectures
2. Master security patterns
3. Optimize resource usage
4. Implement monitoring

---

## 🏭 Production-Ready Concepts

This masterclass teaches concepts you'll use in real production environments:

### 🔒 Security
- Non-root containers
- Security contexts
- Capability dropping
- Read-only filesystems

### 📊 Reliability
- Liveness probes (automatic healing)
- Readiness probes (zero-downtime deployments)
- Resource limits (prevent resource exhaustion)
- Rolling updates (safe deployments)

### ⚡ Performance
- Resource requests (scheduling efficiency)
- Resource limits (isolation)
- Multi-container patterns (sidecar, ambassador)
- Horizontal Pod Autoscaling

### 🔄 Operational Excellence
- Health check monitoring
- Graceful shutdown
- Rolling update strategies
- Rollback capabilities

---

## 🌐 API Endpoints

The application exposes several REST API endpoints:

### GET /api/status
Returns current system status and uptime:
```json
{
  "status": "running",
  "concept": "Pods",
  "level": "Beginner",
  "namespace": "k8s-learning",
  "k8s_version": "1.28",
  "interactive_demo": "true",
  "hands_on_lab": "true",
  "timestamp": "2025-10-09T17:55:44",
  "uptime": 43
}
```

### GET /api/concept
Returns detailed information about the current K8s concept:
```json
{
  "description": "The smallest deployable unit in Kubernetes",
  "purpose": "Run containers and manage their lifecycle",
  "examples": ["nginx-pod", "redis-pod", "mysql-pod"]
}
```

### GET /api/learning-path
Returns recommended learning steps based on level:
```json
[
  "Learn basic K8s concepts",
  "Understand Pod lifecycle",
  "Practice with simple deployments",
  "Explore basic networking"
]
```

### GET /api/lessons
Returns available learning modules:
```json
{
  "title": "Mastering Kubernetes Pods",
  "modules": [
    {"id": 1, "name": "What are Pods?", "duration": "5 min", "status": "available"},
    {"id": 2, "name": "Pod Lifecycle", "duration": "8 min", "status": "available"}
  ]
}
```

---

## 🎨 UI Features

### Interactive Elements
- **Tab Navigation** - Switch between different learning sections
- **Progress Tracking** - Visual progress bars and completion tracking
- **Hover Effects** - Interactive cards with smooth animations
- **Responsive Design** - Works on desktop and mobile devices

### Visual Design
- **Gradient Background** - Modern purple gradient (#667eea to #764ba2)
- **Glass Morphism** - Frosted glass effect for cards
- **Color-Coded Levels** - Beginner (green), Intermediate (orange), Advanced (red)
- **Code Highlighting** - Syntax highlighting for YAML and bash

---

## 🔧 Technical Architecture

### Container Configuration
- **Internal Port**: Always 8080 (fixed for consistency)
- **External Port**: Dynamically assigned (8081-8131)
- **Base Image**: python:3.11-slim
- **Health Checks**: HTTP probe on /api/status

### Retry Logic
The deployment implements robust TOCTTOU (Time-Of-Check-Time-Of-Use) protection:
- Checks port availability comprehensively (netstat, lsof, docker)
- Immediately attempts to use the port (minimizes race window)
- Automatically retries with next port if conflict occurs
- Up to 50 port attempts (8081-8131)

### Resource Files
Generated during pipeline execution:
- `k8s-demo/pod-demo.yaml` - Sample Pod configuration
- `k8s-lab/lab-instructions.md` - Hands-on lab guide
- `Dockerfile` - Dynamically generated container image
- `webapp.port` - Current external port number

---

## 🚀 Integration with Kubernetes Scenarios

K8s Commander is designed as a **bridge** to the full Kubernetes deployment scenarios:

### Learning Progression
```
K8s Commander (Concepts)
    ↓
Kubernetes Scenario 1 (Python App Deployment)
    ↓
Kubernetes Scenario 2 (Secret Automation)
    ↓
Kubernetes Scenario 3 (Auto-Scaling)
    ↓
Kubernetes Scenario 4 (Blue-Green Deployments)
```

### Shared Concepts
All production patterns learned in K8s Commander are used in the Kubernetes scenarios:
- Resource limits → Used in all K8s deployments
- Health probes → Implemented in Python app deployment
- Security contexts → Applied in production pods
- Rolling updates → Used in blue-green deployments

---

## 🎯 Use Cases

### 📚 Training & Workshops
- Interactive K8s introduction for teams
- Pre-requisite training before K8s deployment
- Hands-on learning with immediate feedback

### 🏢 Onboarding
- New team members learning Kubernetes
- Transitioning from Docker to K8s
- Understanding production patterns

### 🎓 Self-Paced Learning
- Individual study with progress tracking
- Practice labs at your own pace
- Review production patterns anytime

### 🔬 Experimentation
- Test K8s concepts safely
- Explore different configurations
- Learn from interactive examples

---

## 📊 Success Metrics

After completing K8s Commander, you should be able to:

✅ Explain core Kubernetes concepts (Pods, Services, etc.)
✅ Write production-ready YAML configurations
✅ Implement health checks and resource limits
✅ Use kubectl commands confidently
✅ Understand security best practices
✅ Deploy applications to Kubernetes clusters

---

## 🐛 Troubleshooting

### Port Already in Use
The pipeline automatically finds available ports (8081-8131). If all ports are in use:
```bash
# Check what's using the ports
docker ps --format "{{.Names}}: {{.Ports}}"

# Clean up old containers
docker ps -a --filter "name=k8s-commander" --format "{{.Names}}" | xargs docker rm -f
```

### Container Won't Start
```bash
# Check container logs
docker logs k8s-commander-<BUILD_NUMBER>

# Verify image exists
docker images | grep k8s-commander
```

### Can't Access Web Application
1. Check the Jenkins console output for the access URL
2. Verify the port mapping: `docker port k8s-commander-<BUILD_NUMBER>`
3. Ensure the port isn't blocked by firewall

---

## 🔗 Related Files

- `Jenkinsfile` - Main pipeline definition
- `PORT_FIX_EXPLANATION.md` - Technical details on port binding fix
- `verify-fix.sh` - Verification script for deployment
- `../SCENARIOS_OVERVIEW.md` - Overview of all Jenkins scenarios

---

## 🌟 What's Next?

After mastering K8s Commander:

1. **Explore Kubernetes Scenarios** - Navigate to `/Kubernetes/kubernetes-scenarios/`
2. **Deploy Real Applications** - Start with Scenario 1 (Python App Deployment)
3. **Implement Production Patterns** - Apply what you learned here
4. **Master GitOps** - Progress to Scenario 5 (GitOps with ArgoCD)

---

## 📞 Support

Need help?
- Check the troubleshooting section above
- Review the `PORT_FIX_EXPLANATION.md` for technical details
- Run the verification script: `./verify-fix.sh`

---

**Ready to master Kubernetes? Start your journey with K8s Commander!** 🚀
