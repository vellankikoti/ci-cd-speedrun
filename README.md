# 🚀 CI/CD Chaos Workshop

> **"Real DevOps heroes don't fear chaos. They master it."**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
[![MkDocs](https://img.shields.io/badge/MkDocs-Material-blue?style=flat&logo=markdown)](https://squidfunk.github.io/mkdocs-material/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat&logo=docker)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue?style=flat&logo=kubernetes)](https://kubernetes.io)

---

## 🎯 **Mission Statement**

Welcome to the **CI/CD Chaos Workshop** - where we intentionally break things to build unbreakable DevOps pipelines! This comprehensive workshop transforms you from a DevOps novice into a **Certified Chaos Slayer** through hands-on scenarios that mirror real-world challenges.

> **"Chaos Agent 🕶️ is sabotaging your deployments. Your mission is to build a robust CI/CD pipeline that defeats Chaos at every stage."**

---

## 🌟 **What Makes This Workshop Special**

### 🎬 **Story-Driven Learning**
- **Narrative**: Follow the epic battle against Chaos Agent
- **Emotional Hooks**: Every phase has "aha" moments
- **Real-World Scenarios**: Based on actual production challenges

### 🧪 **Hands-On Chaos Scenarios**
- **25+ Interactive Scenarios** across 4 major technologies
- **Progressive Difficulty**: From basic to advanced production patterns
- **Failure Simulation**: Learn by breaking things intentionally

### 🏆 **Certification Journey**
- **Progress Tracking**: Visual progress through phases
- **Certificate Generation**: Earn your "Chaos Slayer" certificate
- **Portfolio Ready**: Real projects you can showcase

---

## 🗺️ **Workshop Roadmap**

### **Phase 1: 🧪 TestContainers Chaos** *(15-35 min)*
**Chaos Agent strikes with flaky tests and missing services!**

- ✅ **MySQL Integration Testing** - Real database testing with Testcontainers
- ✅ **PostgreSQL Chaos Scenarios** - Handle connection failures gracefully
- ✅ **MongoDB Resilience** - Test against NoSQL databases
- ✅ **Redis Caching Chaos** - Cache failures and recovery
- ✅ **MariaDB Production Patterns** - Enterprise database testing
- ✅ **Flaky Test Detection** - Identify and fix unreliable tests

**Learning Outcomes:**
- Write bulletproof integration tests
- Handle database connection failures
- Implement proper test isolation
- Debug flaky test scenarios

### **Phase 2: 🐳 Docker Sabotage** *(35-55 min)*
**Chaos Agent breaks your container builds!**

- ✅ **Streaming Server with Docker** - Real-time data processing
- ✅ **Chaos Pipeline Engineering** - Intentional failure injection
- ✅ **Networking Chaos** - Network partition simulation
- ✅ **Docker Image Scanner** - Security vulnerability detection
- ✅ **Escape Room Challenge** - Container security puzzles

**Learning Outcomes:**
- Multi-stage Docker builds
- Container security best practices
- Network failure handling
- Image optimization techniques

### **Phase 3: 🤖 Jenkins Pipeline Showdown** *(55-80 min)*
**Chaos Agent crashes your CI/CD pipelines!**

- ✅ **Docker Build Automation** - Automated container building
- ✅ **Testcontainers Integration** - CI/CD with real databases
- ✅ **HTML Report Generation** - Beautiful test reports
- ✅ **Secret Management** - Secure credential handling
- ✅ **EKS Deployment** - Kubernetes cluster deployment

**Learning Outcomes:**
- Write robust Jenkinsfiles
- Integrate Testcontainers in CI/CD
- Generate professional reports
- Manage secrets securely

### **Phase 4: ☸️ Kubernetes Warzone** *(80-105 min)*
**Chaos Agent corrupts your cluster deployments!**

- ✅ **Python App Deployment** - Production-ready K8s manifests
- ✅ **Secret Automation** - Automated secret management
- ✅ **Auto Scaling Chaos** - Handle traffic spikes
- ✅ **Blue-Green Deployments** - Zero-downtime deployments
- ✅ **GitOps with ArgoCD** - Declarative deployment patterns

**Learning Outcomes:**
- Deploy Python apps to Kubernetes
- Implement auto-scaling strategies
- Master blue-green deployments
- Understand GitOps principles

---

## 🛠️ **Technology Stack**

### **Core Technologies**
- 🐍 **Python 3.10+** - Primary automation language
- 🐳 **Docker** - Containerization and orchestration
- ☸️ **Kubernetes** - Container orchestration
- 🤖 **Jenkins** - CI/CD automation
- 🧪 **Testcontainers** - Integration testing

### **Supporting Technologies**
- 📊 **FastAPI** - Modern Python web framework
- 🧪 **Pytest** - Testing framework
- 📚 **MkDocs + Material** - Documentation
- ☁️ **AWS EKS** - Managed Kubernetes
- 🔐 **HashiCorp Vault** - Secret management

---

## 🎮 **Interactive Scenarios Overview**

### **🧪 TestContainers (6 Scenarios)**
```
TestContainers/
├── test_mysql_container.py      # MySQL integration testing
├── test_postgres_container.py   # PostgreSQL chaos scenarios
├── test_mongodb_container.py    # NoSQL database testing
├── test_redis_container.py      # Cache failure simulation
├── test_mariadb_container.py    # Enterprise database patterns
└── test_flaky.py               # Flaky test detection
```

### **🐳 Docker (5 Scenarios)**
```
Docker/docker-scenarios/
├── scenario_01_streaming-server-with-docker.md
├── scenario_02_chaos_pipeline/
├── scenario_03_networking/
├── scenario_04_docker-image-scanner/
└── scenario_05_escape_room/
```

### **🤖 Jenkins (5 Scenarios)**
```
Jenkins/jenkins_scenarios/
├── scenario_01_docker_build/
├── scenario_02_testcontainers/
├── scenario_03_html_reports/
├── scenario_04_manage_secrets/
└── scenario_05_deploy_eks/
```

### **☸️ Kubernetes (5 Scenarios)**
```
Kubernetes/kubernetes-scenarios/
├── 01-python-deploy/
├── 02-secret-automation/
├── 03-auto-scaling/
├── 04-blue-green/
└── 05-gitops/
```

---

## 🚀 **Quick Start Guide**

### **Prerequisites**
```bash
# Required Software
- Python 3.10+
- Docker Desktop
- Git
- kubectl (for Kubernetes scenarios)
- minikube or EKS cluster
```

### **Workshop Setup**
```bash
# Clone the repository
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r Testcontainers/requirements.txt
pip install mkdocs mkdocs-material

# Start the workshop
mkdocs serve
```

### **Access the Workshop**
- 🌐 **Live Documentation**: [Deployed on Render](https://your-site-name.onrender.com)
- 📚 **Local Development**: `mkdocs serve` (http://127.0.0.1:8000)
- 🎯 **Interactive Scenarios**: Follow the phase-by-phase guide

---

## 🎯 **Learning Outcomes**

By completing this workshop, you will:

### **Technical Skills**
- ✅ **Write bulletproof integration tests** with Testcontainers
- ✅ **Build production-ready Docker images** with multi-stage builds
- ✅ **Create robust Jenkins pipelines** with proper error handling
- ✅ **Deploy Python applications** to Kubernetes clusters
- ✅ **Implement GitOps workflows** with ArgoCD
- ✅ **Handle chaos scenarios** gracefully in production

### **DevOps Mindset**
- ✅ **Think like a Chaos Engineer** - anticipate and prevent failures
- ✅ **Build resilient systems** that can handle unexpected issues
- ✅ **Automate everything** - reduce manual intervention
- ✅ **Monitor and alert** - know when things go wrong
- ✅ **Document everything** - make knowledge transferable

### **Real-World Experience**
- ✅ **25+ Production Scenarios** based on actual challenges
- ✅ **Portfolio Projects** you can showcase to employers
- ✅ **Certification** as a "Certified Chaos Slayer"
- ✅ **Community Recognition** in the DevOps space

---

## 🏆 **Certification Journey**

### **Progress Tracking**
- 📊 **Visual Progress Bar** through all phases
- 🎯 **Scenario Completion** tracking
- 🏅 **Achievement Badges** for each phase
- 📜 **Certificate Generation** with unique IDs

### **Final Assessment**
- 📝 **5-Question Quiz** covering all phases
- 🎨 **Beautiful Certificate** with your name
- 🎉 **Confetti Animation** upon completion
- 📱 **Shareable Badge** for social media

---

## 🌟 **What Makes This Different**

### **🎭 Story-Driven Learning**
Unlike dry tutorials, this workshop tells a story. You're not just learning DevOps - you're on a mission to defeat Chaos Agent and save your deployments!

### **🧪 Real Chaos Scenarios**
Every scenario is based on real production issues. You'll encounter the same problems that DevOps engineers face daily.

### **🎮 Gamified Experience**
- Progress tracking with visual feedback
- Achievement badges for completed phases
- Certificate generation upon completion
- Community recognition

### **📚 Comprehensive Coverage**
From basic Docker builds to advanced GitOps patterns, this workshop covers the entire CI/CD spectrum.

---

## 🤝 **Community & Support**

### **📖 Documentation**
- 📚 **Comprehensive Guides**: Step-by-step instructions for every scenario
- 🎥 **Video Tutorials**: Coming soon for visual learners
- 💬 **Community Forum**: Get help from fellow Chaos Slayers

### **🔄 Continuous Updates**
- 🔄 **Regular Updates**: New scenarios added monthly
- 🐛 **Bug Fixes**: Quick response to issues
- 📈 **Feature Requests**: Community-driven improvements

### **🎯 Contributing**
We welcome contributions! Whether it's:
- 🐛 **Bug Reports**: Help improve the workshop
- 💡 **Feature Ideas**: Suggest new scenarios
- 📝 **Documentation**: Improve guides and tutorials
- 🌟 **Star the Repo**: Show your support

---

## 📊 **Workshop Statistics**

- **📚 25+ Interactive Scenarios**
- **⏱️ 2-2.5 Hours Total Duration**
- **🎯 4 Major Technology Areas**
- **🏆 1 Certification Journey**
- **📈 80-90% Hands-On Time**

---

## 🚀 **Ready to Become a Chaos Slayer?**

> **"Chaos Agent is coming for your deployments. Are you ready to build the pipeline that will defeat them?"**

### **🎯 Start Your Journey**
1. **Clone this repository**
2. **Follow the setup guide**
3. **Begin with Phase 1: TestContainers Chaos**
4. **Complete all scenarios**
5. **Earn your "Certified Chaos Slayer" certificate**

### **🌟 Join the Community**
- ⭐ **Star this repository** if it helps you
- 🔄 **Fork and contribute** to improve it
- 💬 **Share your experience** with others
- 🏆 **Show off your certificate** on social media

---

## 📞 **Get in Touch**

- 🌐 **Live Workshop**: [Deployed on Render](https://your-site-name.onrender.com)
- 📧 **Email**: [your-email@example.com]
- 🐦 **Twitter**: [@your-handle]
- 💼 **LinkedIn**: [your-profile]

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎉 Ready to master chaos and become a DevOps hero? Let's get started! 🚀**

---

*"In chaos, there is opportunity. In DevOps, there is mastery."* - Chaos Slayer Mantra 