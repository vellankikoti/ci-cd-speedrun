# 🎯 Participant Guide: Auto-scaling Hero Challenge

**Step-by-step guide to mastering Kubernetes auto-scaling**

---

## 🎬 **BEFORE YOU START**

### **What You Need:**
- ✅ **Completed Scenario 2** (secure todo app running)
- ✅ **Working Kubernetes cluster** (Docker Desktop, Minikube, or cloud)
- ✅ **Python 3.8+** installed
- ✅ **kubectl** configured and working
- ✅ **10-15 minutes** for hands-on learning

### **What You'll Learn:**
- 📈 Horizontal Pod Autoscaler (HPA) configuration
- ⚡ Load testing and performance monitoring
- 🎮 Interactive scaling simulation
- 📊 Real-time metrics and scaling decisions
- 🏆 Production auto-scaling best practices

---

## 📋 **STEP-BY-STEP INSTRUCTIONS**

### **Step 1: Setup and Validation** (3 minutes)

#### **1.1 Navigate to Scenario 3:**
```bash
cd scenarios/03-auto-scaling
```

#### **1.2 Install Dependencies:**
```bash
# Install required Python packages
pip3 install -r requirements.txt

# Verify installation
python3 -c "import kubernetes; print('✅ Kubernetes client ready')"
python3 -c "import requests; print('✅ Requests library ready')"
python3 -c "import colorama; print('✅ Colorama ready')"
```

#### **1.3 Verify Kubernetes Access:**
```bash
# Check cluster connection
kubectl cluster-info

# Verify metrics server (crucial for HPA)
kubectl top nodes

# If metrics server fails, see troubleshooting.md
```

### **Step 2: Deploy Auto-scaling Challenge** (3 minutes)

#### **2.1 Run the Deployment:**
```bash
python3 deploy-auto-scaling-hero.py
```

#### **2.2 Expected Output:**
```
📈 AUTO-SCALING HERO DEPLOYMENT STARTING
======================================================================
🏠 Creating scaling challenge namespace: scaling-challenge
✅ Scaling namespace created
🚀 Deploying scalable demonstration application...
✅ Scalable application deployed
⚡ Deploying load testing application...
✅ Load testing application deployed
📈 Creating Horizontal Pod Autoscaler (HPA)...
✅ HPA created with intelligent scaling policies
🌐 Creating application services...
✅ Services created for scaling demo and load testing
⏳ Waiting for auto-scaling deployments to be ready...
✅ scaling-demo-app ready! 1/1 pods
✅ load-tester ready! 1/1 pods
📊 Checking metrics server availability...
✅ Metrics server is available

======================================================================
🎉 AUTO-SCALING HERO DEPLOYMENT SUCCESSFUL!
✅ Interactive auto-scaling challenge ready!
======================================================================
```

#### **2.3 Verify Deployment:**
```bash
# Check all components are running
kubectl get all -n scaling-challenge

# Verify HPA is created
kubectl get hpa -n scaling-challenge

# Should show something like:
# NAME                   REFERENCE                     TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
# scaling-demo-app-hpa   Deployment/scaling-demo-app   5%/50%    1         10        1          1m
```

### **Step 3: Access the Interactive Dashboard** (2 minutes)

#### **3.1 Get Access Information:**
The deployment script will show you access methods. Try in this order:

#### **3.2 Method 1 - Direct NodePort (Usually Works):**
```bash
# Open in browser: http://localhost:31003
```

#### **3.3 Method 2 - Port Forwarding (Universal Backup):**
```bash
# If direct access doesn't work, use port forwarding
kubectl port-forward svc/scaling-demo-service -n scaling-challenge 8080:80

# Then open: http://localhost:8080
```

#### **3.4 Method 3 - Environment-Specific:**
```bash
# For Minikube:
minikube service scaling-demo-service -n scaling-challenge --url

# For Cloud K8s: Use external node IP
kubectl get nodes -o wide
# Access: http://<external-ip>:31003
```

### **Step 4: Interactive Auto-scaling Challenge** (10 minutes)

#### **4.1 Understand the Dashboard:**
When you open the dashboard, you'll see:
- 📊 **Real-time Metrics**: Current pods, CPU usage, traffic load
- 🎮 **Control Panel**: Load testing controls with sliders
- 📋 **Scaling Log**: Live updates of scaling decisions
- 🎯 **Challenge Progress**: Track your learning objectives

#### **4.2 Challenge 1 - Light Load Test (3 minutes):**
1. **Set Traffic Intensity:** Move slider to 30%
2. **Set Duration:** 60 seconds
3. **Click "🚀 Start Load Test"**
4. **Observe:**
   - CPU usage increases gradually
   - Pod count may increase to 2 if CPU > 50%
   - Scaling log shows decisions in real-time

**What to Watch:**
- CPU target is 50% - scaling triggers when exceeded
- HPA waits 30 seconds before scaling up
- New pods take 10-20 seconds to become ready

#### **4.3 Challenge 2 - Heavy Load Test (3 minutes):**
1. **Set Traffic Intensity:** Move slider to 70%
2. **Set Duration:** 120 seconds  
3. **Click "🚀 Start Load Test"**
4. **Observe:**
   - Rapid CPU increase
   - More aggressive scaling (1 → 2 → 4 → 6 pods)
   - System adapts to handle the load

**What to Watch:**
- Multiple scaling events in quick succession
- CPU usage stabilizes as more pods handle load
- Response time to scaling decisions

#### **4.4 Challenge 3 - Chaos Agent Attack! (4 minutes):**
1. **Click the red "💥 Chaos Attack!" button**
2. **This automatically:**
   - Sets intensity to 95%
   - Duration to 180 seconds (3 minutes)
   - Triggers the most extreme load scenario
3. **Observe:**
   - Emergency scaling response
   - Maximum pod scaling (up to 10 pods)
   - System's ability to handle extreme load

**What to Watch:**
- How quickly the system responds to extreme load
- Maximum scaling behavior
- Resource efficiency under stress

#### **4.5 Challenge 4 - Scale-down Behavior (3 minutes):**
1. **Stop all load testing** (let current test finish or stop it)
2. **Watch the scale-down process:**
   - CPU usage drops as load decreases
   - Pods gradually scale down (slower than scale-up)
   - System returns to baseline (1 pod)

**What to Watch:**
- Scale-down is more conservative (60s stabilization)
- Gradual reduction to prevent service disruption
- Final state returns to minimum replicas

### **Step 5: Command-Line Monitoring** (Parallel Activity)

#### **5.1 Open a Second Terminal:**
While the interactive dashboard runs, open another terminal for monitoring:

#### **5.2 Real-time Scaling Monitor:**
```bash
# Start the real-time monitor
python3 monitor-scaling.py

# This shows:
# - Current pod count and status
# - CPU usage and averages
# - HPA status and conditions
# - Scaling insights and recommendations
```

#### **5.3 Alternative Monitoring Commands:**
```bash
# Quick stats only
python3 monitor-scaling.py stats

# Recent scaling events
python3 monitor-scaling.py events

# Watch pods scaling live
kubectl get pods -n scaling-challenge -w

# Watch HPA status
kubectl get hpa -n scaling-challenge -w
```

### **Step 6: Advanced Load Testing** (Optional)

#### **6.1 Command-Line Load Tests:**
```bash
# Light load test
python3 load-test.py light

# Heavy load test
python3 load-test.py heavy

# Chaos attack simulation
python3 load-test.py chaos

# Custom load test
python3 load-test.py custom --intensity 60 --duration 120 --type mixed
```

#### **6.2 Manual HPA Testing:**
```bash
# Manually force scaling
kubectl patch hpa scaling-demo-app-hpa -n scaling-challenge -p '{"spec":{"minReplicas":3}}'

# Watch scaling
kubectl get pods -n scaling-challenge -w

# Reset
kubectl patch hpa scaling-demo-app-hpa -n scaling-challenge -p '{"spec":{"minReplicas":1}}'
```

---

## 🎯 **LEARNING CHECKPOINTS**

### **Checkpoint 1: Basic Understanding**
- [ ] Can explain what HPA does
- [ ] Understands the role of CPU targets (50%)
- [ ] Knows the difference between scale-up and scale-down timing
- [ ] Sees the relationship between CPU usage and pod count

### **Checkpoint 2: Scaling Behavior**
- [ ] Observed successful scale-up during load
- [ ] Witnessed conservative scale-down behavior
- [ ] Understands stabilization windows (30s up, 60s down)
- [ ] Recognizes the role of resource requests in scaling

### **Checkpoint 3: Performance Testing**
- [ ] Successfully triggered scaling with load tests
- [ ] Used multiple load testing methods
- [ ] Monitored scaling in real-time
- [ ] Analyzed scaling decisions and timing

### **Checkpoint 4: Production Readiness**
- [ ] Understands min/max replica bounds
- [ ] Knows how to configure scaling policies
- [ ] Can interpret HPA status and conditions
- [ ] Recognizes production scaling patterns

---

## 🔍 **WHAT TO OBSERVE**

### **Key Metrics to Watch:**
1. **CPU Utilization:**
   - Starts low (~5-10%)
   - Increases with load
   - Triggers scaling at 50%
   - Stabilizes as pods scale

2. **Pod Count:**
   - Starts at 1 (minReplicas)
   - Scales up: 1 → 2 → 4 → 8 (depending on load)
   - Scales down: Gradual reduction back to 1
   - Never exceeds 10 (maxReplicas)

3. **Scaling Timing:**
   - Scale-up: ~30 seconds stabilization
   - Scale-down: ~60 seconds stabilization
   - Pod creation: ~15-30 seconds
   - Load balancing: Immediate

4. **HPA Conditions:**
   - AbleToScale: Should be True
   - ScalingActive: True during scaling
   - ScalingLimited: True if at min/max bounds

### **Common Patterns:**
- **Light Load (30%):** Usually 1-2 pods
- **Medium Load (50-60%):** 2-4 pods
- **Heavy Load (70%+):** 4-8 pods
- **Chaos Load (90%+):** 6-10 pods

---

## 🚨 **TROUBLESHOOTING QUICK REFERENCE**

### **Dashboard Won't Load:**
```bash
# Try port-forwarding (works everywhere)
kubectl port-forward svc/scaling-demo-service -n scaling-challenge 8080:80
# Access: http://localhost:8080
```

### **HPA Shows "Unknown" CPU:**
```bash
# Check metrics server
kubectl top pods -n scaling-challenge

# If fails, restart metrics server
kubectl rollout restart deployment/metrics-server -n kube-system
```

### **No Scaling Despite High CPU:**
```bash
# Check HPA status
kubectl describe hpa scaling-demo-app-hpa -n scaling-challenge

# Look for error conditions or scaling limits
```

### **Load Tests Don't Generate Load:**
```bash
# Increase load intensity or use chaos attack
# Check if pods have sufficient CPU limits
kubectl describe pod -l app=scaling-demo-app -n scaling-challenge | grep -A 5 limits
```

---

## 📊 **SUCCESS CRITERIA**

### **You've Successfully Completed When:**
- ✅ Dashboard loads and shows real-time metrics
- ✅ Light load test triggers scaling to 2-3 pods
- ✅ Heavy load test scales to 4+ pods
- ✅ Chaos attack scales to maximum pods (8-10)
- ✅ Scale-down occurs after load stops
- ✅ Monitor shows accurate HPA status
- ✅ You understand scaling policies and timing

### **Bonus Achievements:**
- 🏆 Successfully used command-line load testing
- 🏆 Interpreted HPA conditions and events
- 🏆 Manually triggered scaling with kubectl
- 🏆 Explained scaling behavior to others

---

## 🎓 **KEY TAKEAWAYS**

### **Production Scaling Principles:**
1. **Set Appropriate Targets:** 50% CPU is often good for web apps
2. **Conservative Scale-Down:** Prevents service disruption
3. **Aggressive Scale-Up:** Ensures availability during spikes
4. **Resource Requests Matter:** HPA uses these for calculations
5. **Monitor Everything:** Visibility is key to optimization

### **HPA Best Practices:**
- Always set resource requests on containers
- Use stabilization windows to prevent oscillation
- Monitor scaling events and tune policies
- Set realistic min/max replica bounds
- Test scaling behavior under realistic load

### **Real-World Applications:**
- Web applications handling traffic spikes
- API services with variable load patterns
- Background workers processing queues
- Gaming servers scaling with player count
- Data processing pipelines with varying workloads

---

## 🚀 **NEXT STEPS**

### **After Completing This Scenario:**
1. **Experiment** with different load patterns
2. **Analyze** scaling behavior and optimize policies
3. **Apply** these concepts to your own applications
4. **Learn** about Vertical Pod Autoscaler (VPA)
5. **Explore** custom metrics beyond CPU

### **Advanced Topics to Explore:**
- Multi-metric HPA (CPU + memory + custom)
- Vertical Pod Autoscaler (VPA) for right-sizing
- Cluster Autoscaler for node-level scaling
- Predictive scaling based on patterns
- Cost optimization through scaling policies

**Congratulations! You've mastered Kubernetes auto-scaling!** 🎉📈