# 🚀 Blue-Green Deployment Demo

**Simple, Clean, Zero-Downtime!**

A complete demonstration of blue-green deployment strategy using Kubernetes with instant version switching and zero downtime.

## What's Included

- **app.py** - Flask application with beautiful version display
- **deploy.py** - One-command deployment script
- **switch.py** - Interactive version switcher
- **Dockerfile** - Secure container definition (non-root user)
- **k8s-manifests.yaml** - Complete Kubernetes configuration
- **requirements.txt** - Python dependencies

## Quick Start

```bash
# One command to deploy everything:
python3 deploy.py
```

That's it! The script will:
1. Build Docker image
2. Deploy both blue and green versions
3. Start with blue version active
4. Show you how to switch between versions

## What You'll See

The deployment script provides **copy-paste ready commands**:

```
🔄 SWITCH BETWEEN VERSIONS:

   # Switch to GREEN (v2.0)
   python3 switch.py green

   # Switch to BLUE (v1.0)
   python3 switch.py blue

   # Check current version
   python3 switch.py status

🎮 TRY ZERO-DOWNTIME DEPLOYMENT:

   1. Open http://localhost:31006 in your browser
   2. Run: python3 switch.py green
   3. Watch the page auto-refresh to show GREEN version
   4. Run: python3 switch.py blue
   5. Watch it switch back to BLUE - zero downtime!
```

## Access the App

**Option 1:** NodePort (if available)
```bash
http://localhost:31006
```

**Option 2:** Port-forward (works everywhere)
```bash
kubectl port-forward -n blue-green-demo svc/demo-app 31006:80
# Then open: http://localhost:31006
```

## How Blue-Green Deployment Works

```
Initial State (BLUE active):
┌─────────────────────────────────────┐
│  Service (selector: version=blue)   │
│              ↓                      │
│  ┌──────────────────────────────┐  │
│  │ BLUE Deployment (v1.0)       │  │ ← ACTIVE (receives traffic)
│  │ Pods: 3                      │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ GREEN Deployment (v2.0)      │  │ ← STANDBY (no traffic)
│  │ Pods: 3                      │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘

After Switch (GREEN active):
┌─────────────────────────────────────┐
│  Service (selector: version=green)  │
│              ↓                      │
│  ┌──────────────────────────────┐  │
│  │ BLUE Deployment (v1.0)       │  │ ← STANDBY (no traffic)
│  │ Pods: 3                      │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │ GREEN Deployment (v2.0)      │  │ ← ACTIVE (receives traffic)
│  │ Pods: 3                      │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

**The Magic:** Only the Service selector changes - pods keep running!

## Features

### Application
- Beautiful gradient UI (blue for v1.0, green for v2.0)
- Auto-refresh every 3 seconds
- Shows version, color, pod name, hostname
- Health check endpoint

### Deployment Strategy
- **Zero Downtime:** Traffic switches instantly
- **Instant Rollback:** One command to roll back
- **Safe Testing:** Test new version before switching
- **Both Environments Running:** Blue and green always ready

### Security
- Non-root container (UID 1000)
- Read-only root filesystem
- No privileged escalation
- All capabilities dropped
- Resource limits enforced

## Interactive Demo

### 1. Deploy Initial State
```bash
python3 deploy.py
# Both blue and green deployed, blue is active
```

### 2. Check Current Status
```bash
python3 switch.py status

# Output shows:
# 🔵 BLUE: ACTIVE (receiving traffic)
# 🟢 GREEN: Standby (no traffic)
```

### 3. Switch to Green
```bash
python3 switch.py green

# Instant switch - zero downtime!
# Open http://localhost:31006 - now shows GREEN
```

### 4. Rollback to Blue
```bash
python3 switch.py blue

# Instant rollback!
# Refresh browser - back to BLUE
```

### 5. Watch Live Switching
```bash
# Terminal 1: Keep browser open at http://localhost:31006
# Terminal 2: Run switching commands
python3 switch.py green   # Watch page change color
python3 switch.py blue    # Watch it change back
```

## Verify Deployment

```bash
# Check all resources
kubectl get all -n blue-green-demo

# Show pods with version labels
kubectl get pods -n blue-green-demo -L version

# Check which version is active
kubectl describe service demo-app -n blue-green-demo | grep Selector

# Test health endpoint
curl http://localhost:31006/health
```

## Cleanup

```bash
kubectl delete namespace blue-green-demo
rm k8s-deployed.yaml
```

## Architecture

### Application Components

**app.py:**
- Flask web server on port 8080
- Reads VERSION and COLOR from environment
- Beautiful responsive UI with gradients
- Health check endpoint at /health
- Auto-refresh for live demonstration

**deploy.py:**
- Detects Kubernetes environment
- Builds Docker image
- Deploys both blue and green versions
- Sets initial version to blue
- Provides comprehensive instructions

**switch.py:**
- Gets current active version
- Switches service selector
- Validates target deployment exists
- Shows before/after status
- Provides rollback instructions

### Kubernetes Resources

**Namespace:** `blue-green-demo`
- Isolates all resources

**Deployments:**
- `blue-deployment`: 3 replicas of v1.0
- `green-deployment`: 3 replicas of v2.0
- Both always running (key to blue-green!)

**Service:**
- NodePort on 31006
- Selector determines active version
- Switching changes selector only

## Blue-Green Benefits

### ✅ Advantages

1. **Zero Downtime**
   - Both environments pre-warmed
   - Instant traffic switch
   - No pod restarts needed

2. **Easy Rollback**
   - Instant rollback capability
   - Just change selector back
   - Previous version still running

3. **Testing in Production**
   - Test green in production
   - No traffic until ready
   - Validate before switching

4. **Reduced Risk**
   - Full environment validation
   - Gradual traffic shift possible
   - Quick disaster recovery

### ⚠️ Considerations

1. **Resource Usage**
   - Requires 2x infrastructure
   - Both versions always running
   - Higher cost than rolling update

2. **Database Migrations**
   - Schema must be backward compatible
   - Both versions access same DB
   - Requires careful planning

3. **Session Handling**
   - Stateless apps work best
   - Consider session stickiness
   - Plan for active sessions

## Learning Objectives

After completing this scenario, you'll understand:

1. **How blue-green deployment works**
   - Two identical production environments
   - Traffic switching via service selector
   - Zero-downtime principle

2. **When to use blue-green**
   - Critical applications needing zero downtime
   - When instant rollback is required
   - When you can afford 2x resources

3. **Kubernetes service selectors**
   - How labels and selectors work
   - Dynamic traffic routing
   - Service configuration

4. **Deployment strategies trade-offs**
   - Blue-green vs rolling update
   - Resource usage considerations
   - Complexity vs safety

## Advanced Usage

### Scale Individual Versions
```bash
# Scale blue to 5 replicas
kubectl scale deployment blue-deployment -n blue-green-demo --replicas=5

# Scale green to 1 (canary-like)
kubectl scale deployment green-deployment -n blue-green-demo --replicas=1
```

### Canary Testing
```bash
# Deploy green with 1 pod
kubectl scale deployment green-deployment -n blue-green-demo --replicas=1

# Switch to green (10% traffic to new version)
python3 switch.py green

# If good, scale up green
kubectl scale deployment green-deployment -n blue-green-demo --replicas=3
```

### Monitor During Switch
```bash
# Terminal 1: Watch pods
watch kubectl get pods -n blue-green-demo -L version

# Terminal 2: Watch service
watch kubectl get svc demo-app -n blue-green-demo

# Terminal 3: Switch versions
python3 switch.py green
```

## Pro Tips

1. **Test green before switching**
   ```bash
   # Port-forward directly to green pod
   kubectl port-forward -n blue-green-demo deploy/green-deployment 8080:8080
   # Test at http://localhost:8080
   ```

2. **Gradual traffic shift**
   - Use service mesh (Istio, Linkerd)
   - Implement weighted routing
   - Shift traffic 10% → 50% → 100%

3. **Automate with CI/CD**
   - Deploy green in pipeline
   - Run automated tests
   - Auto-switch if tests pass
   - Auto-rollback on failure

4. **Database compatibility**
   - Maintain backward compatibility
   - Use feature flags
   - Separate data migrations from code

## Troubleshooting

### Switch command fails
```bash
# Check if deployment exists
kubectl get deployments -n blue-green-demo

# Check if pods are running
kubectl get pods -n blue-green-demo -l version=green
```

### Can't access application
```bash
# Use port-forward instead of NodePort
kubectl port-forward -n blue-green-demo svc/demo-app 31006:80
```

### Pods not running
```bash
# Check pod status
kubectl get pods -n blue-green-demo

# Check pod logs
kubectl logs -n blue-green-demo -l version=blue

# Describe pod for events
kubectl describe pod -n blue-green-demo <pod-name>
```

## Resources

- [Blue-Green Deployment (Martin Fowler)](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Zero-Downtime Deployments](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
