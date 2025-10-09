# 🚀 K8s Commander - Quick Start Guide

**Duration**: 5 minutes to get started
**Level**: All levels welcome

---

## ⚡ Getting Started in 3 Steps

### Step 1: Create the Pipeline Job

1. Open Jenkins at `http://localhost:8080`
2. Click **"New Item"**
3. Enter name: `scenario_04_k8s_commander`
4. Select **"Pipeline"**
5. Click **OK**

### Step 2: Configure the Pipeline

1. Scroll to **"Pipeline"** section
2. Set **Definition**: `Pipeline script from SCM`
3. Set **SCM**: `Git`
4. Set **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop`
5. Set **Branch**: `jenkins-test`
6. Set **Script Path**: `Jenkins/jenkins-scenarios/scenario_04_k8s_commander/Jenkinsfile`
7. Click **Save**

### Step 3: Run Your First Build

1. Click **"Build with Parameters"**
2. Choose your learning preferences:
   - **K8S_CONCEPT**: `Pods` (start here!)
   - **LEARNING_LEVEL**: `Beginner`
   - Leave other defaults as-is
3. Click **Build**
4. Wait ~30 seconds for the web app to deploy
5. Click on the **URL** shown in the console output

---

## 🎯 What to Explore

Once the web app opens, you'll see 5 tabs:

### 📊 Overview
- See your learning progress
- Check which features are enabled
- Track completed modules

### 📚 Lessons
- 5 interactive lessons per concept
- Click any lesson to start learning
- Real YAML examples you can copy

### 🏭 Production Patterns
- Resource limits and requests
- Health checks and probes
- Security best practices
- Rolling update strategies

### 🧪 Hands-on Labs
- Practice kubectl commands
- Lab exercises with step-by-step instructions
- Apply what you learned

### 🚀 Next Steps
- Navigate to full Kubernetes scenarios
- Deploy real applications
- Master production deployments

---

## 🎮 Try Different Concepts

After mastering Pods, run new builds with different concepts:

| Concept | What You'll Learn | Duration |
|---------|-------------------|----------|
| **Pods** | Container orchestration basics | 40 min |
| **Services** | Networking and load balancing | 45 min |
| **Deployments** | Rolling updates and scaling | 50 min |
| **ConfigMaps** | Configuration management | 35 min |
| **Secrets** | Secure secrets handling | 40 min |

---

## 🎛️ Parameters Explained

### K8S_CONCEPT
Choose which Kubernetes concept to learn:
- **Pods**: Start here if you're new
- **Services**: After understanding Pods
- **Deployments**: After understanding Services
- **ConfigMaps**: Configuration management
- **Secrets**: Security and secrets

### LEARNING_LEVEL
- **Beginner**: Core concepts with simple examples
- **Intermediate**: Advanced patterns and use cases
- **Advanced**: Production-ready architectures

### INTERACTIVE_DEMO
- **true** (default): Full interactivity enabled
- **false**: Static content only (faster load)

### HANDS_ON_LAB
- **true** (default): Shows Labs tab with exercises
- **false**: Hides Labs tab (lessons only)

### NAMESPACE
- Default: `k8s-learning`
- Use for organizing K8s resources

### K8S_VERSION
- Default: `1.28`
- Kubernetes version for examples

---

## 🐛 Troubleshooting

### Can't Access the Web Application?
1. Check Jenkins console output for the URL
2. Look for: `🌐 Access your K8s Commander at: http://localhost:XXXX`
3. Make sure the port isn't blocked by firewall

### Build Failed?
1. Check if Docker is running: `docker ps`
2. Check if ports 8081-8131 are available
3. Try running the build again

### Lessons Not Loading?
1. Check browser console for errors (F12)
2. Verify the container is running: `docker ps | grep k8s-commander`
3. Check container logs: `docker logs k8s-commander-<BUILD_NUMBER>`

### Need to Clean Up?
```bash
# Stop all k8s-commander containers
docker ps -a --filter "name=k8s-commander" --format "{{.Names}}" | xargs docker rm -f

# Or use the cleanup script
cd Jenkins/jenkins-scenarios/scenario_04_k8s_commander
python3 cleanup.py
```

---

## 📚 Additional Resources

- **Full Documentation**: See `README.md`
- **Verification Script**: Run `./verify-fix.sh` to test deployment
- **Cleanup Script**: Run `python3 cleanup.py` to clean up resources

---

## 🎉 Ready to Start?

**Follow the 3 steps above and begin your Kubernetes journey!**

Questions? Check the full README.md or ask your instructor.

---

**Happy Learning! 🚀✨**
