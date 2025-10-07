# ☸️ K8s Commander - Kubernetes Deployment

**Master Kubernetes deployment in Jenkins pipelines!**

Learn Kubernetes fundamentals, deployment strategies, service management, and scaling - become a K8s commander!

## 🎯 What You'll Learn

- **Kubernetes Basics**: Pods, Services, Deployments, and ConfigMaps
- **Deployment Strategies**: Rolling updates, blue-green, and canary deployments
- **Service Management**: Load balancing and service discovery
- **Scaling & Monitoring**: Horizontal Pod Autoscaling and resource management

## 📁 Project Structure

```
04-k8s-commander/
├── README.md              # This guide
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container image
├── Jenkinsfile           # Kubernetes deployment pipeline
├── k8s/                  # Kubernetes manifests
│   ├── namespace.yaml    # Namespace definition
│   ├── configmap.yaml    # Configuration
│   ├── secret.yaml       # Secrets
│   ├── deployment.yaml   # Application deployment
│   ├── service.yaml      # Service definition
│   ├── ingress.yaml      # Ingress configuration
│   └── hpa.yaml          # Horizontal Pod Autoscaler
└── tests/
    ├── test_app.py       # Application tests
    └── test_k8s.py       # Kubernetes tests
```

## 🚀 Quick Start (5 Minutes Total)

### Step 1: The Application (1 minute)
A Flask app with Kubernetes-native features.

```bash
# Run locally
python app.py
# Visit: http://localhost:5000
```

### Step 2: Kubernetes Deployment (2 minutes)
Deploy to Kubernetes with proper manifests:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k8s-commander
spec:
  replicas: 3
  selector:
    matchLabels:
      app: k8s-commander
  template:
    metadata:
      labels:
        app: k8s-commander
    spec:
      containers:
      - name: app
        image: k8s-commander:latest
        ports:
        - containerPort: 5000
```

### Step 3: Jenkins Pipeline (1 minute)
Kubernetes-enabled pipeline with deployment:

```groovy
stage('☸️ Deploy to Kubernetes') {
    steps {
        sh 'kubectl apply -f k8s/'
        sh 'kubectl rollout status deployment/k8s-commander'
    }
}
```

### Step 4: Understanding the Power (1 minute)
- **Container Orchestration**: Manage multiple containers across nodes
- **Service Discovery**: Automatic load balancing and service discovery
- **Scaling**: Automatic scaling based on metrics
- **Rolling Updates**: Zero-downtime deployments

## 🎮 Learning Experience

### What Makes This Special:
- ✅ **Real Kubernetes**: Deploy to actual Kubernetes cluster
- ✅ **Production Patterns**: Use industry-standard deployment strategies
- ✅ **Service Management**: Learn service discovery and load balancing
- ✅ **Scaling**: Understand horizontal pod autoscaling

### Key Concepts You'll Master:
1. **Kubernetes Objects**: Pods, Services, Deployments, ConfigMaps
2. **Deployment Strategies**: Rolling updates and blue-green deployments
3. **Service Discovery**: How services communicate in Kubernetes
4. **Resource Management**: CPU, memory, and scaling policies

## 🧪 The Application

A Flask app with Kubernetes-native features:
- **Health Checks**: Kubernetes-compatible health endpoints
- **Metrics**: Prometheus-compatible metrics
- **Graceful Shutdown**: Proper signal handling
- **Configuration**: Environment-based configuration

### API Endpoints:
- `GET /` - Application dashboard
- `GET /health` - Kubernetes health check
- `GET /ready` - Kubernetes readiness check
- `GET /metrics` - Prometheus metrics
- `GET /info` - System information

## ☸️ Kubernetes Features

### Deployment Strategy:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k8s-commander
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

### Service Configuration:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: k8s-commander-service
spec:
  selector:
    app: k8s-commander
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### Horizontal Pod Autoscaler:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: k8s-commander-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: k8s-commander
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## ⚙️ Jenkins Pipeline

### Kubernetes Deployment Pipeline:
```groovy
pipeline {
    agent any
    
    stages {
        stage('☸️ Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
                sh 'kubectl rollout status deployment/k8s-commander'
            }
        }
        
        stage('📊 Verify Deployment') {
            steps {
                sh 'kubectl get pods -l app=k8s-commander'
                sh 'kubectl get services'
            }
        }
    }
}
```

## 🚀 Jenkins Setup

### Quick Setup (Workshop Mode):
```bash
# 1. Start Jenkins
cd Jenkins
python3 setup-jenkins-complete.py setup

# 2. Access Jenkins
# Open http://localhost:8080

# 3. Create Pipeline Job
# - New Item → Pipeline
# - Name: "K8s Commander"
# - Pipeline script from SCM
# - Repository: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
# - Script Path: Jenkins/jenkins-scenarios/04-k8s-commander/Jenkinsfile
```

### Manual Setup:
1. **Create New Pipeline Job**
2. **Configure Pipeline**:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - Script Path: `Jenkins/jenkins-scenarios/04-k8s-commander/Jenkinsfile`
3. **Save and Build**

## 🎯 Success Criteria

You've mastered this scenario when:
- ✅ You understand Kubernetes objects and their relationships
- ✅ You can deploy applications to Kubernetes
- ✅ You know how to manage services and ingress
- ✅ You understand scaling and resource management
- ✅ You feel confident about Kubernetes deployment

## 🚀 Next Steps

After completing this scenario:
1. **Try different deployment strategies** - Canary, blue-green
2. **Experiment with scaling** - Test HPA and VPA
3. **Move to Scenario 5** - Security Sentinel with DevSecOps
4. **Build your confidence** - You're now a K8s commander!

## 💡 Pro Tips

- **Start Simple**: Begin with basic deployments
- **Use Namespaces**: Organize your resources
- **Monitor Resources**: Watch CPU and memory usage
- **Test Rollouts**: Always test deployment strategies

---

**Ready to command Kubernetes? Let's deploy like a pro! ☸️**
