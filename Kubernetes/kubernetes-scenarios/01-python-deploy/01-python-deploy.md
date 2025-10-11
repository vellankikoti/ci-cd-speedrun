# 🗳️ Scenario 01: Kubernetes Deployment - WFH vs WFO Voting App

**"From Manual YAML Hell to Python-Powered Success"**

A simple, working voting application built from scratch with guaranteed functionality. Vote for Work From Home vs Work From Office!

---

## ⚡ Quick Start (5 Minutes)

```bash
cd Kubernetes/kubernetes-scenarios/01-python-deploy/hero-solution

# 1. Deploy everything
python3 deploy.py
```

**The script will output ready-to-copy commands!** Look for:

```
🔧 PORT-FORWARD COMMANDS (Copy & Paste - Works on All Platforms):

   # Terminal 1: Start port-forward for voting app
   kubectl port-forward -n voting-app svc/vote-app 31004:80

   # Then open in browser: http://localhost:31004
```

**Copy and paste the commands from the output!** They include:
- ✅ Port-forward command (with correct port)
- ✅ Browser URL to open
- ✅ Curl commands to test voting
- ✅ Cleanup commands

**That's it!** You'll see a beautiful voting interface with real-time results.

> **💡 Pro Tip:** The deployment script outputs everything you need. No need to memorize commands - just copy and paste!

---

## 🎯 What You'll Learn

- Experience the pain of manual YAML deployment (and why it fails)
- Master Python-based Kubernetes automation
- Deploy production-ready apps with ONE command
- Handle cross-platform deployments (Mac, Linux, Windows, Codespaces)
- Build real-time web applications on Kubernetes
- Understand port management and service exposure

**Time**: 15-20 minutes | **Difficulty**: ⭐⭐☆☆☆

---

## 📊 What Gets Deployed

### The WFH vs WFO Voting App

```
┌─────────────────────────────────────────┐
│         Voting App Namespace            │
├─────────────────────────────────────────┤
│  Vote App (2 replicas)                  │  ← 🏠 WFH vs 🏢 WFO
│    - Flask web app                      │  ← Beautiful UI
│    - Real-time updates                  │  ← JavaScript polling
│    - Embedded results                   │  ← All-in-one
├─────────────────────────────────────────┤
│  Redis (1 replica)                      │  ← Vote storage
│    - In-memory database                 │  ← Fast & reliable
│    - Port 6379                          │
└─────────────────────────────────────────┘
```

### Stack

- **Frontend:** Flask + HTML/CSS/JavaScript (embedded)
- **Backend:** Python 3.11
- **Database:** Redis (in-memory)
- **Container:** Docker (slim image)
- **Orchestration:** Kubernetes

### Features

✅ **Actually Works** - Tested and confirmed voting functionality
✅ **Beautiful UI** - Gradient design, emoji buttons, smooth animations
✅ **Real-time Updates** - Results update every 2 seconds
✅ **Simple Architecture** - No complex databases, just Redis
✅ **Smart Port Management** - Auto-detects conflicts, finds free ports
✅ **Cross-Platform** - Works on Mac, Linux, Windows, Codespaces
✅ **Health Monitoring** - Waits for pods to be ready
✅ **Resource Limits** - Optimized for lightweight environments
✅ **Retry Logic** - Waits for Redis to be ready before starting

---

## 🎮 How to Use the Voting App

1. **Open the URL** (shown in deployment output)
   - Default: http://localhost:31004

2. **Vote for your preference:**
   - Click 🏠 **WFH** (Work From Home)
   - Click 🏢 **WFO** (Work From Office)

3. **Watch results update in real-time**
   - Vote counts appear instantly
   - Smooth animations
   - No page refresh needed

4. **Test it works!**
   - Open multiple browser tabs
   - Vote from different tabs
   - See all votes counted

---

## 🔍 Verify Deployment

```bash
# Check all resources
kubectl get all -n voting-app

# Watch pods
kubectl get pods -n voting-app -w

# View logs
kubectl logs -n voting-app -l app=vote-app -f

# Check vote counts
curl http://localhost:31004/results
```

---

## 🧪 Test Voting from Command Line

```bash
# Make sure port-forward is running
kubectl port-forward -n voting-app svc/vote-app 31004:80 &

# Vote for WFH
curl -X POST http://localhost:31004/vote \
  -H "Content-Type: application/json" \
  -d '{"option":"WFH"}'

# Output: {"success": true, "votes": {"WFH": 1, "WFO": 0}}

# Vote for WFO
curl -X POST http://localhost:31004/vote \
  -H "Content-Type: application/json" \
  -d '{"option":"WFO"}'

# Output: {"success": true, "votes": {"WFH": 1, "WFO": 1}}

# Check results
curl http://localhost:31004/results

# Output: {"WFH": 1, "WFO": 1}
```

---

## 🌐 Accessing Your App

### Docker Desktop (Mac/Windows)
```bash
kubectl port-forward -n voting-app svc/vote-app 31004:80
# Open: http://localhost:31004
```

### Minikube
```bash
minikube service vote-app -n voting-app --url
# Use the URL shown
```

### Universal (Always Works)
```bash
# Terminal 1: Start port forward
kubectl port-forward -n voting-app svc/vote-app 31004:80

# Terminal 2: Open browser or use curl
curl http://localhost:31004
```

---

## 🎮 The Chaos-First Experience (Optional)

### Option A: See It Fail First (Educational)

```bash
# Watch manual YAML deployment fail
python3 chaos/chaos-demo.py
```

**What happens:**
- Shows broken YAML with 6+ mistakes highlighted
- Attempts deployment → fails
- Explains each error educationally
- Makes you WANT the automation solution!

**Then deploy the hero solution:**
```bash
python3 hero-solution/deploy.py
```

### Option B: Compare YAML Files

```bash
# View the broken YAML side-by-side with working YAML
diff -y chaos/broken-vote-app.yaml hero-solution/working-vote-app.yaml | less

# Or view them separately
cat chaos/broken-vote-app.yaml         # ❌ The broken version
cat hero-solution/working-vote-app.yaml  # ✅ The fixed version
```

**What you'll learn:**
- Why manual YAML fails (missing namespaces, wrong selectors, invalid ports)
- All the fixes needed (resource limits, health checks, proper labels)
- Best practices for production deployments
- How to debug YAML issues yourself

### Option C: Visual Comparison Dashboard

```bash
# Launch interactive dashboard
python3 chaos/comparison-dashboard.py

# Open: http://localhost:5000 (or auto-selected port)
```

**Shows:**
- Split-screen: Chaos (red) vs Hero (green)
- Real-time metrics updating every 5 seconds
- Pods, services, uptime comparison
- Beautiful UI with animations

---

## 🔧 How It Works

### The Hero Solution

**File**: `hero-solution/deploy.py`

```python
class VoteAppDeployer:
    def __init__(self):
        # Auto-detect free ports
        self.node_port = self.find_available_port()

    def get_used_k8s_nodeports(self):
        # Check ALL existing Kubernetes services
        # Avoid port conflicts automatically

    def deploy_everything(self):
        # Create namespace
        # Deploy Redis (with retry logic)
        # Deploy Vote app (with proper config)
        # Wait for pods to be ready
        # Show access information
```

**Key Features:**
- Scans existing Kubernetes services for used ports
- Checks local port availability
- Handles errors gracefully with retries
- Provides clear progress output
- Builds Docker image automatically
- Updates manifests dynamically

### What Makes It Cross-Platform

1. **Environment Detection**: Identifies Minikube, Docker Desktop, Kind, Cloud
2. **Port Auto-Selection**: No hardcoded ports, finds what's available
3. **Universal Fallback**: Always provides port-forward instructions
4. **Resource Awareness**: Lightweight defaults for small VMs
5. **Image Building**: Works with local Docker daemon or Minikube's

---

## 💥 The Chaos Demo Explained

### What's Wrong with Manual YAML?

**File**: `chaos/broken-vote-app.yaml`

```yaml
# ❌ PROBLEM 1: Missing namespace
metadata:
  name: vote-app
  # namespace: vote-app  ← MISSING!

# ❌ PROBLEM 2: Wrong ConfigMap reference
configMapKeyRef:
  name: vote-config-missing  # ← DOESN'T EXIST!

# ❌ PROBLEM 3: Invalid NodePort
nodePort: 99999  # ← Must be 30000-32767!

# ❌ PROBLEM 4: Wrong selector
selector:
  app: vote-app-wrong  # ← Doesn't match pods!

# ❌ PROBLEM 5: No resource limits
# ❌ PROBLEM 6: No health checks
```

**Result**: Pods crash, services don't connect, hours of debugging!

---

## 💡 Why This App Works (vs Old Vote Apps)

Unlike previous voting apps that had database connection issues:

| Old Apps | This App |
|----------|----------|
| ❌ Complex PostgreSQL setup | ✅ Simple Redis storage |
| ❌ Separate vote and result apps | ✅ All-in-one embedded UI |
| ❌ Database connection errors | ✅ Retry logic waits for Redis |
| ❌ Votes not persisting | ✅ Redis confirmed working |
| ❌ Unclear error messages | ✅ Clear progress feedback |
| ❌ Hours of debugging | ✅ Works in 5 minutes |

**Technical Improvements:**

✅ **Simple Redis storage** - no complex databases
✅ **Retry logic** - waits for Redis to be ready
✅ **Embedded UI** - no separate result app needed
✅ **Real-time updates** - JavaScript polls every 2 seconds
✅ **Health checks** - Kubernetes knows when pods are ready
✅ **Resource limits** - prevents container chaos
✅ **Clean code** - easy to understand and modify

---

## 🚨 Troubleshooting

### "Port already in use"

**No action needed!** Scripts automatically handle this:

```
📊 Starting deployment...
   🌐 Using port: 31005
   ℹ️  Port 31004 was busy, using 31005 instead
```

### "Pods not starting"

```bash
# Check status
kubectl get pods -n voting-app

# View logs
kubectl logs -n voting-app -l app=vote-app

# Describe for events
kubectl describe pod -n voting-app <pod-name>

# Common fix: Redis image issue
kubectl describe pod -n voting-app -l app=redis
```

### "Can't access vote app"

```bash
# Always works - port forward
kubectl port-forward -n voting-app svc/vote-app 31004:80

# Keep terminal open, access:
http://localhost:31004
```

### "Votes not working"

```bash
# Check Redis is running
kubectl get pods -n voting-app -l app=redis

# Check vote app logs
kubectl logs -n voting-app -l app=vote-app

# Test Redis connection
kubectl exec -it -n voting-app deploy/redis -- redis-cli ping
# Should return: PONG
```

### "Image pull errors"

```bash
# For Minikube: Build image inside Minikube
eval $(minikube docker-env)
docker build -t simple-vote-app:latest .

# For Docker Desktop: Image should be available automatically
docker images | grep simple-vote-app
```

---

## 🧹 Cleanup

```bash
# Remove everything
kubectl delete namespace voting-app

# Kill port-forward if running
pkill -f "port-forward.*voting-app"

# Verify cleanup
kubectl get namespaces | grep voting
# Should return nothing
```

---

## 📁 Files Structure

```
01-python-deploy/
├── 01-python-deploy.md           # This file
├── chaos/
│   ├── chaos-demo.py              # Interactive failure demo
│   ├── comparison-dashboard.py    # Visual comparison UI
│   └── broken-vote-app.yaml       # Intentionally broken YAML
└── hero-solution/
    ├── deploy.py                  # ONE-COMMAND DEPLOYMENT ⭐
    ├── vote-app.py                # Flask app with embedded UI
    ├── Dockerfile                 # Container image
    ├── k8s-manifests.yaml         # Kubernetes resources
    ├── requirements.txt           # Python dependencies
    └── working-vote-app.yaml      # Fixed YAML for comparison
```

---

## 🎨 UI Features

**Vote Interface:**
- Beautiful gradient background (purple to pink)
- Big emoji buttons (🏠 🏢)
- Real-time vote counts
- Smooth animations on click
- Success messages when voting
- Responsive design

**Results Display:**
- Embedded in the same page
- Updates automatically every 2 seconds
- Clean, modern design
- No page refresh needed

---

## 🎉 Success Criteria

After deployment, verify:

✅ Pods running: `kubectl get pods -n voting-app`
```
NAME                        READY   STATUS    RESTARTS   AGE
redis-86b7844bc4-xxxxx      1/1     Running   0          1m
vote-app-7cd84c7b86-xxxxx   1/1     Running   0          1m
vote-app-7cd84c7b86-xxxxx   1/1     Running   0          1m
```

✅ Vote endpoint works:
```bash
curl -X POST http://localhost:31004/vote \
  -H "Content-Type: application/json" \
  -d '{"option":"WFH"}'
# Returns: {"success": true, "votes": {"WFH": 1, "WFO": 0}}
```

✅ Results endpoint works:
```bash
curl http://localhost:31004/results
# Returns: {"WFH": 1, "WFO": 0}
```

✅ Browser shows UI: Open http://localhost:31004
✅ Clicking buttons registers votes
✅ Results update in real-time

---

## 📚 Learning Outcomes

By deploying this app, you've learned:

### Kubernetes Concepts
1. **Deployments** - Manage replicated applications
2. **Services** - Expose apps with networking (ClusterIP)
3. **Namespaces** - Isolate resources
4. **Resource Limits** - Set CPU/memory constraints
5. **Health Checks** - Liveness and readiness probes
6. **Port Forwarding** - Access cluster services locally

### Application Development
1. **Flask web applications** - Build HTTP APIs
2. **Docker containers** - Package apps for deployment
3. **Redis** - Use in-memory databases
4. **Real-time updates** - JavaScript polling patterns
5. **Embedded UI** - Single-file web apps

### DevOps Best Practices
1. **Automation** - Python eliminates manual errors
2. **Port Management** - Handle conflicts dynamically
3. **Cross-platform** - Environment detection
4. **Error Handling** - Retry logic and graceful failures
5. **User Experience** - Clear output and progress feedback

---

## 🎓 Key Takeaways

### What You Learned

1. **Manual YAML is Error-Prone**: 6+ mistakes in just 51 lines
2. **Automation Wins**: Python eliminates human error
3. **Simplicity Matters**: Redis > PostgreSQL for demos
4. **Embedded UIs**: Single app > Multiple microservices (for small apps)
5. **Port Management**: Conflicts are common, need smart handling
6. **User Experience**: Clear output makes or breaks tools

### Production Patterns

- ✅ Validate before deploy
- ✅ Auto-detect environment
- ✅ Handle errors gracefully
- ✅ Provide multiple access methods
- ✅ Show clear progress feedback
- ✅ Make cleanup easy
- ✅ Build automation, not just scripts

---

## 🚀 Next Steps

### Immediate
1. **Try voting in the browser** - see the beautiful UI
2. **Test from command line** - understand the API
3. **Check the logs** - see real-time activity
4. **Vote multiple times** - confirm it works

### Learning Path
1. **Try the chaos demo** to experience the pain
2. **Compare YAML files** to understand fixes
3. **Launch the dashboard** for visual comparison
4. **Modify the vote app** - add new options
5. **Move to Scenario 02** for security automation

### Enhancements
- Add authentication (login to vote)
- Implement vote limits (one vote per user)
- Add more options (hybrid, flex, etc.)
- Create admin dashboard
- Add charts/graphs for results
- Deploy to production cluster
- Add database persistence

---

## 💡 Pro Tips

1. **Port Conflicts**: Scripts handle automatically, but on macOS disable "AirPlay Receiver" in System Settings if port 5000/7000 is always busy

2. **Resource Limits**: Defaults are optimized for 4GB RAM systems

3. **Multiple Runs**: Safe to run deployment multiple times - it updates existing resources

4. **Learning Path**: Do chaos first, then hero - makes concepts stick!

5. **Redis Testing**: Use `redis-cli` inside the pod to check data:
   ```bash
   kubectl exec -it -n voting-app deploy/redis -- redis-cli
   > GET votes
   ```

6. **Debugging**: Always check logs first before searching online

7. **Port Forwarding**: Keep the terminal open while using the app

---

## 🌟 What Makes This Special

**Built from scratch** because spending a week on broken apps is unacceptable!

- ⚡ **Works in 5 minutes** (not days)
- 🎨 **Beautiful UI** (not bare HTML forms)
- 🔧 **Actually tested** (voting confirmed working)
- 📦 **Simple stack** (Redis, not complex databases)
- 🚀 **One command** (not 10 manual steps)
- 💯 **Cross-platform** (Mac, Linux, Windows)

**Remember**: Chaos teaches, automation rescues! 🧨🦸

---

**Scenario 02**: Secret Management & Security Automation →

---

*Scenario 01 - Kubernetes Deployment Automation*
*Part of CI/CD Chaos Workshop - PyCon HK*
*Built with ❤️ for hands-on Kubernetes learning*
