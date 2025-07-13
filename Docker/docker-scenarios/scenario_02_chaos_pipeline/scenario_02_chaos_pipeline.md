# 🚀 Docker Scenario 02 — Enhanced Progressive Chaos Engineering Workshop

**Goal:**  
- Demonstrate powerful Docker capabilities in CI/CD pipelines  
- Show progressive chaos engineering with 5 different failure scenarios
- Run chaos tests to simulate failures and prove pipeline resilience  
- Teach how to run Docker **inside** Docker (DinD) safely
- Provide educational, interactive experience with real microservices
- **NEW:** Enhanced learning experience with real microservices, interactive debugging, and comprehensive monitoring

This scenario creates an unforgettable learning experience:

> **Progressive Chaos Engineering: From Broken to Production-Ready with Real Microservices**

---

# 🚀 Quick Start

## Option 1: Local Demo (Recommended for Presentations)

1. **Clone and navigate to the scenario:**
   ```bash
   cd Docker/docker-scenarios/scenario_02_chaos_pipeline
   ```

2. **Run the manual demo (step-by-step control):**
   ```bash
   ./demo_manual.sh
   ```
   This script allows you to control the pace and explain each step.

3. **Run the simple demo (automated):**
   ```bash
   ./demo_simple.sh
   ```
   This script runs automatically without user interaction.

## Option 2: Jenkins Pipeline (Recommended for CI/CD)

1. **Set up Jenkins workspace:**
   ```bash
   cd Docker/docker-scenarios/scenario_02_chaos_pipeline
   ./setup_jenkins_workspace.sh
   ```

2. **Configure Jenkins pipeline:**
   
   **Step-by-step Jenkins job configuration:**
   
   a) **Create New Job:**
   - Go to Jenkins Dashboard
   - Click "New Item" or "Create new jobs"
   - Enter job name: `chaos-ci-pipeline`
   - Select "Pipeline"
   - Click "OK"
   
   b) **Configure Parameters:**
   - In the job configuration, check "This project is parameterized"
   - Add parameter: Name: `SCENARIO`, Type: `Choice Parameter`
   - Choices:
     ```
     chaos-full
     chaos-1
     chaos-2
     chaos-3
     chaos-free
     progressive-demo
     ```
   - Default Value: `progressive-demo`
   - Description: `Select the chaos scenario to run`
   
   c) **Configure Pipeline:**
   - **Definition:** Select "Pipeline script from SCM"
   - **SCM:** Select "Git"
   - **Repository URL:** Your repository URL (e.g., `https://github.com/your-username/your-repo.git`)
   - **Credentials:** Add your Git credentials if needed
   - **Branch Specifier:** `*/main` (or `*/master` depending on your default branch)
   - **Script Path:** `Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile`
   
   d) **Save Configuration:**
   - Click "Save" to create the job

3. **Run the pipeline:**
   - Go to Jenkins dashboard
   - Click "Build with Parameters"
   - Select scenario: `progressive-demo`
   - Click "Build"

## Demo Scripts Explained

- **`demo_manual.sh`**: Step-by-step control with educational pauses
- **`demo_simple.sh`**: Automated demo for quick demonstrations
- **`cleanup.sh`**: Clean up all containers and resources
- **`setup_jenkins_workspace.sh`**: Prepare Jenkins workspace with all required files

## Jenkins Pipeline Scenarios

The Jenkins pipeline supports multiple scenarios:

- **`progressive-demo`**: Complete educational journey (recommended)
- **`chaos-full`**: Maximum chaos (everything broken)
- **`chaos-free`**: Perfect pipeline (all working)
- **`chaos-1/2/3`**: Progressive fixes showing issue cascades

For detailed Jenkins setup instructions, see [JENKINS_SETUP.md](JENKINS_SETUP.md).

**Quick Setup:** For a 5-minute setup guide, see [JENKINS_QUICK_REFERENCE.md](JENKINS_QUICK_REFERENCE.md).

---

# ✅ Prerequisites

- Docker installed
- Basic Python knowledge
- Basic familiarity with Jenkins pipelines
- Enough RAM (~2GB) for Docker containers
- **NEW:** `jq` for JSON formatting (will be auto-installed if missing)

---

# ✅ Enhanced Scenario Overview

In this **enhanced** scenario:

✅ We spin up Jenkins in Docker.  
✅ Jenkins runs a progressive chaos engineering pipeline with **real microservices**:
  - **Step 1**: Network failure simulation with web API
  - **Step 2**: Resource limitation with image processing service
  - **Step 3**: Service dependency failure with Redis session management
  - **Step 4**: Database connection failure with MySQL user management
  - **Step 5**: Success! Complete resilient microservices architecture

✅ **NEW:** Each step provides:
- **Real microservices** with actual functionality
- **Interactive debugging endpoints** (`/health`, `/debug`, `/metrics`)
- **Comprehensive health monitoring** and observability
- **Educational insights** and learning objectives
- **Progressive complexity** and hands-on learning
- **Production-ready patterns** and best practices

✅ **NEW:** Enhanced learning experience:
- **Real web APIs** that participants can interact with
- **Comprehensive monitoring** with health checks and metrics
- **Debugging tools** for troubleshooting
- **Educational content** explaining what's happening
- **Production-ready features** like fallback mechanisms

✅ Entire environment runs in Docker:
- No external services required
- 100% self-contained chaos engineering
- Real-world failure simulation with real microservices

---

# ✅ Enhanced Directory Structure

Your workshop directory will look like this:

```
scenario_02_chaos_pipeline/
│
├── jenkins-docker/
│     └── Dockerfile
│
├── pipeline/
│     ├── Jenkinsfile
│     └── requirements.txt
│
├── scenarios/
│     ├── step1_fail_network/
│     │   ├── app.py          # NEW: Real web API with network testing
│     │   └── Dockerfile      # NEW: Enhanced with Flask and monitoring
│     ├── step2_fail_resource/
│     │   ├── app.py          # NEW: Image processing service with memory limits
│     │   └── Dockerfile      # NEW: Enhanced with numpy, PIL, psutil
│     ├── step3_fail_service/
│     │   ├── app.py          # NEW: Session management with Redis
│     │   └── Dockerfile      # NEW: Enhanced with Redis integration
│     ├── step4_fail_db/
│     │   ├── app.py          # NEW: User management with MySQL
│     │   └── Dockerfile      # NEW: Enhanced with SQLAlchemy
│     └── step5_success/
│         ├── app.py          # NEW: Complete resilient microservices
│         └── Dockerfile      # NEW: Production-ready with all dependencies
│
├── tests/
│     └── test_mysql.py
│
├── setup.sh
├── cleanup.sh
├── install_plugins.sh
├── test_setup.sh
├── test_all_scenarios.sh
├── demo_enhanced_chaos.sh    # NEW: Enhanced demo script
└── README.md
```

---

# ✅ Enhanced Progressive Chaos Engineering Steps

## 🎯 Learning Objectives

This **enhanced** scenario teaches chaos engineering through 5 progressive steps with **real microservices**:

### **Step 1: Network Failure** 🌐
- **What happens**: Web API tries to connect to external services and internal dependencies
- **Learning**: Network connectivity issues in containers with real API testing
- **Real Service**: Web API with network diagnostics and health monitoring
- **Educational value**: Understanding container networking limitations with hands-on debugging

### **Step 2: Resource Failure** 💾
- **What happens**: Image processing service runs with memory constraints
- **Learning**: Resource constraints and container limits with real image processing
- **Real Service**: Image processing microservice with memory monitoring
- **Educational value**: Understanding Docker resource management with actual workloads

### **Step 3: Service Failure** 🔌
- **What happens**: Session management service tries to connect to Redis (not running)
- **Learning**: Service dependencies and microservices with real session management
- **Real Service**: Session management microservice with Redis integration
- **Educational value**: Understanding service discovery and dependencies with real use case

### **Step 4: Database Failure** 🗄️
- **What happens**: User management service tries to connect to MySQL (not running)
- **Learning**: Database connectivity and persistence with real user management
- **Real Service**: User management microservice with MySQL integration
- **Educational value**: Understanding database dependencies with actual user operations

### **Step 5: Success!** 🎉
- **What happens**: Complete resilient microservices architecture with all dependencies
- **Learning**: Production-ready, resilient system with comprehensive monitoring
- **Real Service**: Complete microservices architecture with health monitoring, metrics, and observability
- **Educational value**: Understanding what makes a system production-ready and resilient

---

# ✅ Enhanced Step-by-Step Implementation

---

## ✅ 1. Build a Jenkins Docker Image

We'll build a custom Jenkins Docker image that:

- Has Docker CLI available
- Allows running Docker commands in pipelines

### **`docker-scenario-02/jenkins-docker/Dockerfile`**

```Dockerfile
FROM jenkins/jenkins:lts

USER root

# Install Docker CLI inside Jenkins container
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

USER jenkins
```

---

### Build the image

```bash
cd docker-scenario-02/jenkins-docker

docker build -t jenkins-docker .
```

✅ This builds a Jenkins image that can run Docker commands inside itself.

---

## ✅ 2. Run Jenkins Container

Run Jenkins and mount Docker socket:

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins-docker
```

✅ Jenkins can now:

* Run Docker CLI commands
* Spin up containers during builds

---

## ✅ 3. Enhanced Progressive Chaos Engineering Apps

Each scenario step now has **real microservices** with actual functionality:

### **Step 1: Network Failure** (`scenarios/step1_fail_network/app.py`)

**NEW:** Real web API with network testing capabilities:

```python
# Enhanced with Flask web API, network diagnostics, health monitoring
# Real endpoints: /health, /debug, /run-experiment
# Educational content and debugging tools
```

**Educational Value**: Shows how containers handle network connectivity issues with real API testing.

### **Step 2: Resource Failure** (`scenarios/step2_fail_resource/app.py`)

**NEW:** Real image processing service with memory monitoring:

```python
# Enhanced with image processing, memory monitoring, resource diagnostics
# Real endpoints: /health, /debug, /process-image/<w>/<h>, /run-experiment
# Educational content and resource debugging tools
```

**Educational Value**: Demonstrates Docker resource limits and memory management with actual workloads.

### **Step 3: Service Failure** (`scenarios/step3_fail_service/app.py`)

**NEW:** Real session management service with Redis integration:

```python
# Enhanced with session management, Redis integration, service diagnostics
# Real endpoints: /health, /debug, /session/create, /session/<id>, /run-experiment
# Educational content and service debugging tools
```

**Educational Value**: Shows service dependencies and microservices architecture with real session management.

### **Step 4: Database Failure** (`scenarios/step4_fail_db/app.py`)

**NEW:** Real user management service with MySQL integration:

```python
# Enhanced with user management, MySQL integration, database diagnostics
# Real endpoints: /health, /debug, /user/create, /user/<id>, /run-experiment
# Educational content and database debugging tools
```

**Educational Value**: Demonstrates database connectivity and persistence with actual user operations.

### **Step 5: Success!** (`scenarios/step5_success/app.py`)

**NEW:** Complete resilient microservices architecture:

```python
# Enhanced with comprehensive monitoring, metrics, observability
# Real endpoints: /health, /debug, /metrics, /run-experiment
# Production-ready features and best practices
```

**Educational Value**: Shows what a production-ready, resilient system looks like with comprehensive monitoring.

---

## ✅ 4. Enhanced Dockerfiles

Each step now has enhanced Dockerfiles with proper dependencies:

### **Step 1 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask requests
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 2 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask numpy pillow psutil
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 3 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask redis
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 4 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask sqlalchemy pymysql
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

### **Step 5 Dockerfile**
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install flask redis sqlalchemy pymysql psutil requests
COPY app.py .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "app.py"]
```

---

## ✅ 5. Enhanced Demo Script

**NEW:** `demo_enhanced_chaos.sh` - Comprehensive demo script with:

- **Real microservices** with actual functionality
- **Interactive debugging** and health monitoring
- **Educational content** and learning objectives
- **Progressive complexity** and hands-on learning
- **Production-ready features** and best practices

### **Run the Enhanced Demo**

```bash
# Make the script executable
chmod +x demo_enhanced_chaos.sh

# Run the enhanced demo
./demo_enhanced_chaos.sh
```

This will:
- Build all enhanced scenario containers
- Start each service with proper configuration
- Run chaos experiments with real microservices
- Show health monitoring and debugging information
- Provide educational insights and learning objectives
- Demonstrate progressive complexity and resilience

---

## ✅ 6. Enhanced Jenkins Pipeline Script

### **`pipeline/Jenkinsfile`**

```groovy
pipeline {
    agent any

    parameters {
        choice(
            name: "STAGE",
            choices: ["step1_fail_network", "step2_fail_resource", "step3_fail_service", "step4_fail_db", "step5_success"],
            description: "Select the enhanced scenario step to run"
        )
    }

    environment {
        SCENARIO_DIR = "scenarios/${params.STAGE}"
        IMAGE_NAME = "chaos-${params.STAGE}"
        PORT_MAPPING = [
            "step1_fail_network": "8081:8080",
            "step2_fail_resource": "8082:8080",
            "step3_fail_service": "8083:8080",
            "step4_fail_db": "8084:8080",
            "step5_success": "8085:8080"
        ]
    }

    stages {
        stage("Build Enhanced Scenario Docker Image") {
            steps {
                echo "🚧 Building enhanced Docker image for ${params.STAGE}..."
                sh """
                    docker build -t $IMAGE_NAME $SCENARIO_DIR
                """
            }
        }
        stage("Run Enhanced Scenario Container") {
            steps {
                script {
                    echo "🚀 Running enhanced scenario: ${params.STAGE}"
                    def runArgs = ""
                    if (params.STAGE == "step2_fail_resource") {
                        runArgs = "--memory=128m --memory-swap=128m"
                    }
                    sh """
                        docker run -d --name chaos-${params.STAGE} -p ${PORT_MAPPING[params.STAGE]} $runArgs $IMAGE_NAME
                    """
                }
            }
        }
        stage("Wait for Service Health") {
            steps {
                script {
                    echo "⏳ Waiting for service to be healthy..."
                    def port = PORT_MAPPING[params.STAGE].split(":")[0]
                    sh """
                        timeout 60 bash -c 'until curl -f http://localhost:$port/health; do sleep 2; done'
                    """
                }
            }
        }
        stage("Run Chaos Experiment") {
            steps {
                script {
                    echo "🔬 Running chaos experiment..."
                    def port = PORT_MAPPING[params.STAGE].split(":")[0]
                    sh """
                        curl -s http://localhost:$port/run-experiment | jq '.'
                    """
                }
            }
        }
        stage("Show Debug Information") {
            steps {
                script {
                    echo "🔍 Showing debug information..."
                    def port = PORT_MAPPING[params.STAGE].split(":")[0]
                    sh """
                        echo "=== Health Status ==="
                        curl -s http://localhost:$port/health | jq '.'
                        echo "=== Debug Info ==="
                        curl -s http://localhost:$port/debug | jq '.'
                    """
                }
            }
        }
        stage("Highlight Educational Insights") {
            steps {
                script {
                    def messages = [
                        "step1_fail_network": [
                            fixed: "Nothing fixed yet! This is the first intentional failure.",
                            broken: "Network is broken. App cannot reach the outside world.",
                            learning: "Understanding container networking limitations"
                        ],
                        "step2_fail_resource": [
                            fixed: "Network is now working! (But... memory is too low)",
                            broken: "Resource limits are too strict. App crashes with MemoryError.",
                            learning: "Understanding Docker resource management"
                        ],
                        "step3_fail_service": [
                            fixed: "Network and resources are now fine! (But... missing Redis service)",
                            broken: "Service dependency (Redis) is missing. App cannot connect.",
                            learning: "Understanding service dependencies and microservices"
                        ],
                        "step4_fail_db": [
                            fixed: "Network, resources, and service are all good! (But... missing MySQL)",
                            broken: "Database connection fails. MySQL is not running.",
                            learning: "Understanding database dependencies and persistence"
                        ],
                        "step5_success": [
                            fixed: "All previous issues are fixed! 🎉",
                            broken: "Nothing! This is the chaos-free, production-ready step.",
                            learning: "Understanding production-ready, resilient systems"
                        ]
                    ]
                    def msg = messages[params.STAGE]
                    echo "✅ FIXED: ${msg.fixed}"
                    echo "❌ STILL BROKEN: ${msg.broken}"
                    echo "🎓 LEARNING: ${msg.learning}"
                }
            }
        }
    }
    post {
        always {
            echo "🏁 Enhanced scenario run complete! Check the logs above for details."
            script {
                echo "🔗 Service available at: http://localhost:${PORT_MAPPING[params.STAGE].split(':')[0]}"
            }
        }
        success {
            echo "🎉 Success!"
        }
        failure {
            echo "💥 Failure (as expected for some steps)!"
        }
    }
}
```

✅ What this enhanced pipeline does:

* Builds enhanced Docker images with real microservices
* Runs containers with proper health monitoring
* Executes chaos experiments with real functionality
* Shows debugging information and educational insights
* Provides comprehensive monitoring and observability

---

## ✅ 7. Enhanced Automation and Testing Scripts

### **Setup Scripts**

- **`setup.sh`**: Complete Jenkins setup with Docker and plugins
- **`install_plugins.sh`**: Install required Jenkins plugins
- **`cleanup.sh`**: Clean up all containers and images
- **`test_setup.sh`**: Verify Jenkins is working correctly

### **Testing Scripts**

- **`test_all_scenarios.sh`**: Run all 5 enhanced scenarios locally for testing
- **`test_setup.sh`**: Verify the complete setup is working
- **`demo_enhanced_chaos.sh`**: **NEW** - Comprehensive demo with real microservices

### **Local Testing**

Run all enhanced scenarios locally to verify they work:

```bash
./demo_enhanced_chaos.sh
```

This will:
- Build all enhanced scenario Docker images
- Run each scenario with real microservices
- Show expected failures and success with educational content
- Provide interactive debugging and health monitoring
- Demonstrate progressive complexity and learning

---

## ✅ 8. Run the Enhanced Pipeline

1. **Start Jenkins:**
   ```bash
   ./setup.sh
   ```

2. **Access Jenkins UI:**
   - Open [http://localhost:8080](http://localhost:8080)
   - Get initial password: `docker logs jenkins`

3. **Create Pipeline Job:**
   - Create new "Pipeline" job
   - Point to your enhanced Jenkinsfile
   - Run with parameters to select scenario step

4. **Watch Enhanced Chaos Unfold:**
   - Each step demonstrates different failure modes with **real microservices**
   - **Educational messages** explain what's happening
   - **Interactive debugging** and health monitoring
   - **Progressive learning** from failure to success
   - **Clear "What's Fixed" and "What's Still Broken"** messages
   - **Real endpoints** for hands-on interaction

---

## ✅ 9. Enhanced Educational Benefits

This **enhanced** scenario provides:

- **Real Microservices**: Each step has actual functionality and real endpoints
- **Interactive Learning**: Participants can interact with services via web APIs
- **Comprehensive Monitoring**: Health checks, debugging, and metrics
- **Progressive Complexity**: Each step builds on the previous with real use cases
- **Production-Ready Patterns**: Best practices and resilience patterns
- **Hands-On Experience**: Real debugging and troubleshooting opportunities
- **Educational Content**: Clear explanations and learning objectives
- **Real-World Scenarios**: Simulates actual production issues with real services

---

## ✅ 10. Enhanced Clean Up

When done, clean up everything:

```bash
./cleanup.sh
```

This removes:
- Jenkins container
- All enhanced scenario Docker images
- Docker networks
- Temporary files

---

## ✅ 11. What Makes This Enhanced Version Super Useful

✅ **Participants actually BUILD and RUN** real microservices with actual functionality  
✅ **Interactive debugging** with real web APIs and health monitoring  
✅ **Comprehensive monitoring** with health checks, metrics, and observability  
✅ **Educational content** that explains what's happening and why  
✅ **Progressive learning** with real use cases and hands-on experience  
✅ **Production-ready patterns** and best practices  
✅ **Real-world scenarios** that mirror actual production issues  
✅ **Hands-on troubleshooting** with real debugging tools  
✅ **Comprehensive documentation** and learning objectives  

This enhanced version transforms the workshop from simple test runs into an **immersive, educational experience** that participants will remember and apply in their real work!

