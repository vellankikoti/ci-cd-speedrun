# 🔧 Scenario 3: Auto-scaling Troubleshooting Guide

**Comprehensive troubleshooting for auto-scaling challenges**

---

## 🚨 **CRITICAL ISSUES**

### **Issue 1: HPA Shows "Unknown" CPU Metrics**

**Symptoms:**
```bash
kubectl get hpa -n scaling-challenge
# Shows: TARGETS: <unknown>/50%
```

**Root Causes:**
- Metrics server not running or not ready
- Resource requests not defined on pods
- Metrics server can't reach kubelet

**Solutions:**

#### **Check Metrics Server Status:**
```bash
# Check if metrics server is running
kubectl get pods -n kube-system | grep metrics-server

# Check metrics server logs
kubectl logs -n kube-system -l k8s-app=metrics-server

# Check if metrics are available
kubectl top nodes
kubectl top pods -n scaling-challenge
```

#### **Fix Metrics Server (Docker Desktop):**
```bash
# Restart metrics server
kubectl rollout restart deployment/metrics-server -n kube-system

# Wait for it to be ready
kubectl rollout status deployment/metrics-server -n kube-system
```

#### **Fix Metrics Server (Minikube):**
```bash
# Enable metrics server addon
minikube addons enable metrics-server

# Verify it's enabled
minikube addons list | grep metrics-server
```

#### **Verify Resource Requests:**
```bash
# Check if pods have resource requests
kubectl describe deployment scaling-demo-app -n scaling-challenge | grep -A 5 requests

# Should show:
#   requests:
#     cpu: 100m
#     memory: 128Mi
```

#### **Manual Metrics Server Installation (if needed):**
```bash
# Install metrics server manually
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# For local clusters, may need insecure mode
kubectl patch deployment metrics-server -n kube-system --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'
```

---

### **Issue 2: Pods Not Scaling Up Despite High CPU**

**Symptoms:**
- CPU usage high (>50%) but pods stay at 1 replica
- HPA shows correct CPU but no scaling action

**Root Causes:**
- HPA scaling policies preventing scale-up
- Resource limits preventing pods from starting
- Node resource constraints
- Stabilization windows preventing rapid scaling

**Solutions:**

#### **Check HPA Configuration:**
```bash
# Describe HPA for detailed status
kubectl describe hpa scaling-demo-app-hpa -n scaling-challenge

# Look for conditions like:
# - AbleToScale: False (indicates scaling is blocked)
# - ScalingActive: False (indicates HPA is not active)
```

#### **Check Resource Availability:**
```bash
# Check node resources
kubectl describe nodes

# Check if nodes have enough CPU/memory
kubectl top nodes

# Check pod resource usage
kubectl top pods -n scaling-challenge
```

#### **Check Scaling Events:**
```bash
# View scaling events
kubectl get events -n scaling-challenge --sort-by='.lastTimestamp' | grep HPA

# Check for messages like:
# - "New size: 2; reason: cpu resource utilization above target"
# - "couldn't get resource utilization metric"
```

#### **Force Scaling Test:**
```bash
# Manually patch HPA to force scaling
kubectl patch hpa scaling-demo-app-hpa -n scaling-challenge -p '{"spec":{"minReplicas":3}}'

# Wait and check if pods scale
kubectl get pods -n scaling-challenge -w

# Reset to original
kubectl patch hpa scaling-demo-app-hpa -n scaling-challenge -p '{"spec":{"minReplicas":1}}'
```

---

### **Issue 3: Interactive Dashboard Not Loading**

**Symptoms:**
- Browser shows connection refused or timeout
- Dashboard doesn't load at expected URL

**Root Causes:**
- Service not created or misconfigured
- NodePort conflicts
- Pods not running
- Network connectivity issues

**Solutions:**

#### **Check Service Status:**
```bash
# Check if service exists
kubectl get svc -n scaling-challenge

# Should show scaling-demo-service with NodePort
kubectl describe svc scaling-demo-service -n scaling-challenge
```

#### **Check Pod Status:**
```bash
# Verify pods are running
kubectl get pods -n scaling-challenge

# Check pod logs for errors
kubectl logs -l app=scaling-demo-app -n scaling-challenge

# Describe problematic pods
kubectl describe pod -l app=scaling-demo-app -n scaling-challenge
```

#### **Test Different Access Methods:**
```bash
# Method 1: Direct NodePort (if available)
curl http://localhost:31003

# Method 2: Port forwarding (universal)
kubectl port-forward svc/scaling-demo-service -n scaling-challenge 8080:80
curl http://localhost:8080

# Method 3: Cluster IP (from within cluster)
kubectl run test-pod --image=nginx --rm -it -- curl http://scaling-demo-service.scaling-challenge.svc.cluster.local
```

#### **Check for Port Conflicts:**
```bash
# Check if port 31003 is in use
lsof -i :31003  # On macOS/Linux
netstat -an | grep 31003  # On Windows

# If conflict, change NodePort in deployment script
# Edit deploy-auto-scaling-hero.py and change self.node_port = 31004
```

---

### **Issue 4: Load Testing Not Generating CPU Load**

**Symptoms:**
- Load test runs but CPU usage stays low
- No scaling triggered despite high intensity settings

**Root Causes:**
- Load tester pods not running
- CPU requests too low for load generation
- Load testing logic not CPU-intensive enough
- Resource limits preventing CPU usage

**Solutions:**

#### **Check Load Tester Status:**
```bash
# Verify load tester is running
kubectl get pods -l app=load-tester -n scaling-challenge

# Check load tester logs
kubectl logs -l app=load-tester -n scaling-challenge

# Describe load tester pod
kubectl describe pod -l app=load-tester -n scaling-challenge
```

#### **Increase Load Tester Resources:**
```bash
# Edit the deployment to increase load tester CPU limits
kubectl patch deployment load-tester -n scaling-challenge -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "load-tester",
          "resources": {
            "limits": {
              "cpu": "2000m",
              "memory": "512Mi"
            }
          }
        }]
      }
    }
  }
}'
```

#### **Manual Load Testing:**
```bash
# Test load generation manually
python3 load-test.py chaos --intensity 90 --duration 60

# Monitor CPU during test
watch kubectl top pods -n scaling-challenge

# Check if scaling occurs
kubectl get pods -n scaling-challenge -w
```

#### **Alternative Load Generation:**
```bash
# Use stress tool directly in pods
kubectl exec -it deployment/scaling-demo-app -n scaling-challenge -- sh
# Inside pod: stress --cpu 1 --timeout 60s
```

---

## ⚠️ **COMMON ISSUES**

### **Issue 5: Scaling Too Slow**

**Solution:**
```bash
# Reduce HPA stabilization windows for faster scaling
kubectl patch hpa scaling-demo-app-hpa -n scaling-challenge --type='merge' -p='{
  "spec": {
    "behavior": {
      "scaleUp": {
        "stabilizationWindowSeconds": 15
      }
    }
  }
}'
```

### **Issue 6: Scaling Too Aggressive**

**Solution:**
```bash
# Increase stabilization windows for more conservative scaling
kubectl patch hpa scaling-demo-app-hpa -n scaling-challenge --type='merge' -p='{
  "spec": {
    "behavior": {
      "scaleUp": {
        "stabilizationWindowSeconds": 60,
        "policies": [{
          "type": "Pods",
          "value": 1,
          "periodSeconds": 60
        }]
      }
    }
  }
}'
```

### **Issue 7: Pods Stuck in Pending State**

**Solution:**
```bash
# Check resource constraints
kubectl describe pod -l app=scaling-demo-app -n scaling-challenge | grep -A 5 Events

# Common causes:
# - Insufficient node resources
# - Image pull errors
# - Storage issues

# Check node capacity
kubectl describe nodes | grep -A 5 "Allocated resources"
```

### **Issue 8: Monitor Script Crashes**

**Solution:**
```bash
# Check Python dependencies
pip3 install -r requirements.txt

# Run with debug output
python3 monitor-scaling.py 2>&1 | tee monitor-debug.log

# Check kubectl access
kubectl auth can-i get hpa --namespace scaling-challenge
```

---

## 🔧 **DIAGNOSTIC COMMANDS**

### **Complete Health Check Script:**
```bash
#!/bin/bash
echo "🔍 Auto-scaling Health Check"
echo "=========================="

echo "📊 Cluster Status:"
kubectl get nodes
kubectl get pods -n kube-system | grep metrics-server

echo "🚀 Scaling Challenge Status:"
kubectl get all -n scaling-challenge

echo "📈 HPA Status:"
kubectl get hpa -n scaling-challenge
kubectl describe hpa scaling-demo-app-hpa -n scaling-challenge

echo "⚡ Current Metrics:"
kubectl top nodes
kubectl top pods -n scaling-challenge

echo "📋 Recent Events:"
kubectl get events -n scaling-challenge --sort-by='.lastTimestamp' | tail -10

echo "🌐 Service Access:"
kubectl get svc scaling-demo-service -n scaling-challenge

echo "✅ Health check complete!"
```

### **Quick Fix Commands:**
```bash
# Reset everything
kubectl delete namespace scaling-challenge
python3 deploy-auto-scaling-hero.py

# Restart metrics server
kubectl rollout restart deployment/metrics-server -n kube-system

# Force HPA refresh
kubectl patch hpa scaling-demo-app-hpa -n scaling-challenge -p '{"metadata":{"annotations":{"force-refresh":"'$(date)'"}}}'

# Check scaling manually
kubectl scale deployment scaling-demo-app -n scaling-challenge --replicas=3
```

---

## 📱 **ACCESS TROUBLESHOOTING**

### **Docker Desktop:**
```bash
# Should work: http://localhost:31003
# If not, try port-forward:
kubectl port-forward svc/scaling-demo-service -n scaling-challenge 8080:80
```

### **Minikube:**
```bash
# Get Minikube IP
minikube ip
# Access: http://<minikube-ip>:31003

# Or use service command
minikube service scaling-demo-service -n scaling-challenge --url
```

### **Cloud Providers (EKS/GKE/AKS):**
```bash
# Get external node IP
kubectl get nodes -o wide

# Access: http://<external-ip>:31003
# Note: May need to configure security groups/firewall rules
```

### **Universal Solution:**
```bash
# Port forwarding works everywhere
kubectl port-forward svc/scaling-demo-service -n scaling-challenge 8080:80
# Access: http://localhost:8080
```

---

## 🆘 **EMERGENCY RECOVERY**

### **Complete Reset:**
```bash
# Nuclear option - delete everything and redeploy
kubectl delete namespace scaling-challenge
sleep 30
python3 deploy-auto-scaling-hero.py
```

### **Partial Reset - Keep Namespace:**
```bash
# Delete just the problematic components
kubectl delete deployment,hpa,svc,configmap -l app=scaling-demo-app -n scaling-challenge
kubectl delete deployment,svc,configmap -l app=load-tester -n scaling-challenge

# Redeploy
python3 deploy-auto-scaling-hero.py
```

### **Metrics Server Reset:**
```bash
# Delete and reinstall metrics server
kubectl delete deployment metrics-server -n kube-system
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

---

## 📞 **GETTING HELP**

### **Information to Collect:**
1. **Kubernetes Version:** `kubectl version --short`
2. **Cluster Type:** Docker Desktop / Minikube / Cloud
3. **Pod Status:** `kubectl get pods -n scaling-challenge`
4. **HPA Status:** `kubectl describe hpa -n scaling-challenge`
5. **Metrics:** `kubectl top pods -n scaling-challenge`
6. **Events:** `kubectl get events -n scaling-challenge`
7. **Logs:** `kubectl logs -l app=scaling-demo-app -n scaling-challenge`

### **Common Solutions Summary:**
- ✅ **Metrics Issues** → Restart metrics-server
- ✅ **Access Issues** → Use port-forwarding
- ✅ **Scaling Issues** → Check resource requests and HPA config
- ✅ **Load Issues** → Verify load tester and increase intensity
- ✅ **Dashboard Issues** → Check pods and services

### **Support Channels:**
- 📖 Check participant-guide.md for step-by-step help
- 👨‍🏫 Ask instructor for assistance
- 💬 Use workshop chat for peer support
- 🔍 Review docs/hpa-deep-dive.md for technical details

**Remember: Port-forwarding (`kubectl port-forward`) works in ALL environments when direct access fails!**