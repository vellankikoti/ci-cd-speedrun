# 🗳️ Simple Voting App - WFH vs WFO

**A working, simple voting application that actually works!**

No more frustration - this is a clean, minimal voting app built from scratch with guaranteed functionality.

---

## ✅ What This Is

A simple, beautiful voting application where users vote for **Work From Home** vs **Work From Office**.

- **Real-time updates** - votes appear instantly
- **Clean UI** - gradient design, emoji buttons, smooth animations
- **Actually works** - uses Redis for reliable vote storage
- **Production-ready** - health checks, resource limits, proper container configuration

---

## 🚀 Deploy in ONE Command

```bash
python3 deploy.py
```

That's it! The script will:
1. Build the Docker image
2. Deploy to Kubernetes
3. Wait for pods to be ready
4. Give you the URL to access the app

---

## 🎯 Access the App

### Docker Desktop / Kind
```bash
kubectl port-forward -n voting-app svc/vote-app 9090:80
```
Open: **http://localhost:9090**

### Minikube
```bash
minikube service vote-app -n voting-app
```

---

## 🎮 How to Use

1. Open the URL in your browser
2. Click 🏠 **WFH** or 🏢 **WFO** to vote
3. Watch results update in real-time
4. Open multiple tabs - all votes are counted!

---

## 📊 Architecture

```
┌──────────────┐
│  Vote App    │  ← Flask web app (2 replicas)
│  Port 8080   │  ← Beautiful UI, real-time updates
└───────┬──────┘
        │
        ▼
┌──────────────┐
│   Redis      │  ← Vote storage
│  Port 6379   │  ← In-memory database
└──────────────┘
```

**Stack:**
- **Frontend:** Flask + HTML/CSS/JavaScript
- **Backend:** Python 3.11
- **Database:** Redis (in-memory)
- **Container:** Docker
- **Orchestration:** Kubernetes

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
kubectl port-forward -n voting-app svc/vote-app 9090:80 &
curl http://localhost:9090/results
```

---

## 🧪 Test Voting from Command Line

```bash
# Start port-forward
kubectl port-forward -n voting-app svc/vote-app 9090:80 &

# Vote for WFH
curl -X POST http://localhost:9090/vote \
  -H "Content-Type: application/json" \
  -d '{"option":"WFH"}'

# Vote for WFO
curl -X POST http://localhost:9090/vote \
  -H "Content-Type: application/json" \
  -d '{"option":"WFO"}'

# Check results
curl http://localhost:9090/results

# Output: {"WFH": 1, "WFO": 1}
```

---

## 🧹 Cleanup

```bash
kubectl delete namespace voting-app
```

---

## 📁 Files

```
simple-voting-app/
├── vote-app.py           # Flask application (main app)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image
├── k8s-manifests.yaml    # Kubernetes resources
├── deploy.py             # One-command deployment script
└── README.md             # This file
```

---

## 🔧 Manual Deployment (Optional)

If you want to deploy manually:

```bash
# 1. Build image
docker build -t simple-vote-app:latest .

# 2. Update manifest
sed 's/YOUR_DOCKER_IMAGE_HERE/simple-vote-app:latest/g' k8s-manifests.yaml > k8s-deploy.yaml

# 3. Deploy
kubectl apply -f k8s-deploy.yaml

# 4. Wait for pods
kubectl wait --for=condition=ready pod -l app=vote-app -n voting-app --timeout=120s

# 5. Access
kubectl port-forward -n voting-app svc/vote-app 9090:80
```

---

## 💡 Why This Works

Unlike the previous voting app that had database connection issues:

✅ **Simple Redis storage** - no complex databases
✅ **Retry logic** - waits for Redis to be ready
✅ **Embedded UI** - no separate result app needed
✅ **Real-time updates** - JavaScript polls every 2 seconds
✅ **Health checks** - Kubernetes knows when pods are ready
✅ **Resource limits** - prevents container chaos
✅ **Clean code** - easy to understand and modify

---

## 🎨 Screenshots

**Vote Interface:**
- Beautiful gradient background
- Big emoji buttons (🏠 🏢)
- Real-time vote counts
- Smooth animations

**Results Display:**
- Embedded in the same page
- Updates automatically every 2 seconds
- Clean, modern design

---

## 🛠️ Troubleshooting

### Pods not starting?
```bash
kubectl describe pod -n voting-app -l app=vote-app
```

### Can't access app?
```bash
# Make sure port-forward is running
kubectl port-forward -n voting-app svc/vote-app 9090:80

# Check if pods are running
kubectl get pods -n voting-app
```

### Votes not working?
```bash
# Check Redis is running
kubectl get pods -n voting-app -l app=redis

# Check vote app logs
kubectl logs -n voting-app -l app=vote-app
```

---

## 🎉 Success Criteria

✅ Pods running: `kubectl get pods -n voting-app`
✅ Vote endpoint works: `curl -X POST http://localhost:9090/vote -H "Content-Type: application/json" -d '{"option":"WFH"}'`
✅ Results endpoint works: `curl http://localhost:9090/results`
✅ Browser shows UI: Open http://localhost:9090
✅ Clicking buttons registers votes
✅ Results update in real-time

---

## 📚 Learning Outcomes

By deploying this app, you've learned:

1. **Flask web applications** - Build simple HTTP APIs
2. **Docker containers** - Package apps for deployment
3. **Kubernetes deployments** - Manage replicated applications
4. **Kubernetes services** - Expose apps with networking
5. **Redis** - Use in-memory databases for fast storage
6. **Health checks** - Ensure pods are ready before serving traffic
7. **Port forwarding** - Access cluster services locally
8. **Resource management** - Set CPU/memory limits

---

## 🚀 Next Steps

- Add authentication (login to vote)
- Implement vote limits (one vote per user)
- Add more options (hybrid, flex, etc.)
- Create admin dashboard
- Add charts/graphs for results
- Deploy to production cluster
- Add database persistence

---

**Built with ❤️ for hands-on Kubernetes learning**

No more spending a week on broken apps - this one works in minutes!
