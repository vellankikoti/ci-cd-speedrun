# ☸️ Phase 4 – Kubernetes Chaos & Scalability

Welcome to **Phase 4** of the CI/CD Chaos Workshop — where we deploy our Python apps to Kubernetes and learn to handle real-world chaos in production!

This phase covers:

✅ Kubernetes deployments  
✅ Auto-scaling with HPA  
✅ Chaos engineering experiments  
✅ Monitoring and observability  
✅ Blue-green deployments

> 🎯 **Goal:** Prove our apps survive chaos in Kubernetes — pods crashing, nodes failing, networks partitioning.

---

## 🚀 What We're Building

We're deploying our FastAPI Python app to Kubernetes with:

- **Auto-scaling** based on CPU/memory usage
- **Health checks** and readiness probes
- **Chaos experiments** to test resilience
- **Monitoring** with Prometheus and Grafana
- **Blue-green deployments** for zero-downtime updates

> **Chaos Agent says:** "Let's crash some pods and see what happens!"  
> Our mission: Build apps that survive anything.

---

## ☸️ Kubernetes Setup

### ✅ Local Development

For local testing, use one of these options:

**Option 1: Docker Desktop Kubernetes**
```bash
# Enable Kubernetes in Docker Desktop
# Settings → Kubernetes → Enable Kubernetes
kubectl cluster-info
```

**Option 2: Minikube**
```bash
# Start Minikube
minikube start
kubectl cluster-info
```

**Option 3: Kind**
```bash
# Create Kind cluster
kind create cluster --name chaos-workshop
kubectl cluster-info
```

---

## 🚀 Scenario 1 – Basic Deployment

### ✅ Why It Matters

Kubernetes deployments need proper **health checks** and **resource limits** to survive chaos.

> **Chaos Event:** "Pods keep crashing and restarting!"

---

### ✅ What We'll Do

✅ Deploy our FastAPI app to Kubernetes  
✅ Add health checks and readiness probes  
✅ Set resource limits and requests  
✅ Monitor pod status

---

### ✅ Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chaos-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chaos-app
  template:
    metadata:
      labels:
        app: chaos-app
    spec:
      containers:
      - name: chaos-app
        image: chaos-app:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

### ✅ Service YAML

```yaml
apiVersion: v1
kind: Service
metadata:
  name: chaos-app-service
spec:
  selector:
    app: chaos-app
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

---

## 🚀 Scenario 2 – Auto-Scaling

### ✅ Why It Matters

Auto-scaling ensures your app handles traffic spikes and recovers from failures.

> **Chaos Event:** "Traffic spike! Pods can't handle the load!"

---

### ✅ What We'll Do

✅ Create HorizontalPodAutoscaler (HPA)  
✅ Test scaling under load  
✅ Monitor scaling behavior

---

### ✅ HPA YAML

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: chaos-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: chaos-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 🚀 Scenario 3 – Chaos Engineering

### ✅ Why It Matters

Chaos engineering proves your app's resilience by intentionally causing failures.

> **Chaos Event:** "Let's kill some pods and see what happens!"

---

### ✅ What We'll Do

✅ Kill random pods  
✅ Simulate node failures  
✅ Test network partitions  
✅ Monitor recovery time

---

### ✅ Chaos Experiments

```python
def test_pod_kill_chaos():
    """Kill random pods and verify recovery"""
    # Get all pods
    pods = kubectl_get_pods("--selector=app=chaos-app")
    
    # Kill a random pod
    random_pod = random.choice(pods)
    kubectl_delete_pod(random_pod)
    
    # Wait for new pod to be ready
    time.sleep(30)
    
    # Verify service is still responding
    response = requests.get("http://localhost/health")
    assert response.status_code == 200
```

---

## 🚀 Scenario 4 – Blue-Green Deployment

### ✅ Why It Matters

Blue-green deployments enable zero-downtime updates and instant rollbacks.

> **Chaos Event:** "Deployment failed! Users are seeing errors!"

---

### ✅ What We'll Do

✅ Deploy new version alongside old  
✅ Switch traffic gradually  
✅ Rollback instantly if needed

---

### ✅ Blue-Green Strategy

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chaos-app-blue
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: chaos-app
        version: blue
    spec:
      containers:
      - name: chaos-app
        image: chaos-app:v1
        ports:
        - containerPort: 3000

# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chaos-app-green
spec:
  replicas: 0  # Start with 0 replicas
  template:
    metadata:
      labels:
        app: chaos-app
        version: green
    spec:
      containers:
      - name: chaos-app
        image: chaos-app:v2
        ports:
        - containerPort: 3000
```

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Pod Crash Chaos

```bash
# Kill random pods
kubectl get pods --selector=app=chaos-app -o name | xargs -I {} kubectl delete {}

# Verify auto-recovery
kubectl get pods --selector=app=chaos-app
```

### ✅ Scenario 2: Node Failure Simulation

```bash
# Drain a node (simulate node failure)
kubectl drain node-1 --force --ignore-daemonsets

# Verify pods reschedule
kubectl get pods --all-namespaces -o wide
```

### ✅ Scenario 3: Resource Exhaustion

```bash
# Create resource pressure
kubectl run stress-test --image=busybox --requests=cpu=1000m,memory=1Gi --limits=cpu=2000m,memory=2Gi --command -- stress --cpu 4 --vm 2 --vm-bytes 1G
```

---

## 📊 Monitoring & Observability

### ✅ Metrics to Track

- **Pod health:** Ready/NotReady ratio
- **Scaling:** HPA current/target replicas
- **Performance:** Response time, throughput
- **Resources:** CPU/memory utilization

### ✅ Monitoring Setup

```yaml
# Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: chaos-app-monitor
spec:
  selector:
    matchLabels:
      app: chaos-app
  endpoints:
  - port: metrics
    interval: 30s
```

---

## 🎯 Next Steps

✅ **Phase 4 Complete:** You now have Kubernetes mastery!  
✅ **Ready for Phase 5:** [Final Victory Deploy](final.md)  
✅ **Chaos Agent Status:** Defeated in Kubernetes resilience! 🕶️

---

## 📊 Monitoring & Reporting

### ✅ Kubernetes Metrics

- Deployment success rate
- Pod restart count
- Auto-scaling events
- Resource utilization

### ✅ Chaos Metrics

- Recovery time from pod failures
- Service availability during chaos
- Auto-scaling effectiveness

---

**Remember:** Kubernetes is your fortress against chaos. When pods crash, nodes fail, or networks partition, your app should keep running! 🔥
