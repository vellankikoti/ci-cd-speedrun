# 🚀 Docker Scenario 02 — Progressive Chaos Engineering Workshop

**Goal:**  
- Demonstrate powerful Docker capabilities in CI/CD pipelines  
- Show progressive chaos engineering with 5 different failure scenarios
- Run chaos tests to simulate failures and prove pipeline resilience  
- Teach how to run Docker **inside** Docker (DinD) safely
- Provide educational, interactive experience with clear learning objectives

This scenario creates an unforgettable learning experience:

> **Progressive Chaos Engineering: From Broken to Production-Ready**

---

# ✅ Prerequisites

- Docker installed
- Basic Python knowledge
- Basic familiarity with Jenkins pipelines
- Enough RAM (~2GB) for Docker containers

---

# ✅ Scenario Overview

In this scenario:

✅ We spin up Jenkins in Docker.  
✅ Jenkins runs a progressive chaos engineering pipeline:
  - **Step 1**: Network failure simulation
  - **Step 2**: Resource limitation (memory constraints)
  - **Step 3**: Service dependency failure (missing Redis)
  - **Step 4**: Database connection failure (missing MySQL)
  - **Step 5**: Success! All issues resolved

✅ Each step provides:
- Clear educational messages
- Line-by-line error explanations
- Progressive learning objectives
- Interactive debugging experience

✅ Entire environment runs in Docker:
- No external services required
- 100% self-contained chaos engineering
- Real-world failure simulation

---

# ✅ Directory Structure

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
│     │   ├── app.py
│     │   └── Dockerfile
│     ├── step2_fail_resource/
│     │   ├── app.py
│     │   └── Dockerfile
│     ├── step3_fail_service/
│     │   ├── app.py
│     │   └── Dockerfile
│     ├── step4_fail_db/
│     │   ├── app.py
│     │   └── Dockerfile
│     └── step5_success/
│         ├── app.py
│         └── Dockerfile
│
├── tests/
│     └── test_mysql.py
│
├── setup.sh
├── cleanup.sh
├── install_plugins.sh
├── test_setup.sh
├── test_all_scenarios.sh
└── README.md

````

---

# ✅ Progressive Chaos Engineering Steps

## 🎯 Learning Objectives

This scenario teaches chaos engineering through 5 progressive steps:

### **Step 1: Network Failure** 🌐
- **What happens**: App tries to connect to nonexistent host
- **Learning**: Network connectivity issues in containers
- **Error**: `ConnectionError: [Errno -2] Name or service not known`
- **Educational value**: Understanding container networking limitations

### **Step 2: Resource Failure** 💾
- **What happens**: App runs with 64MB memory limit (too low)
- **Learning**: Resource constraints and container limits
- **Error**: `MemoryError: Unable to allocate array`
- **Educational value**: Understanding Docker resource management

### **Step 3: Service Failure** 🔌
- **What happens**: App tries to connect to Redis (not running)
- **Learning**: Service dependencies and microservices
- **Error**: `ConnectionRefusedError: [Errno 111] Connection refused`
- **Educational value**: Understanding service discovery and dependencies

### **Step 4: Database Failure** 🗄️
- **What happens**: App tries to connect to MySQL (not running)
- **Learning**: Database connectivity and persistence
- **Error**: `OperationalError: (2003, "Can't connect to MySQL server")`
- **Educational value**: Understanding database dependencies

### **Step 5: Success!** 🎉
- **What happens**: All previous issues are resolved
- **Learning**: Complete, production-ready pipeline
- **Result**: All tests pass, app runs successfully
- **Educational value**: Understanding what makes a system resilient

---

# ✅ Step-by-Step Implementation

---

## ✅ 1. Build a Jenkins Docker Image

We’ll build a custom Jenkins Docker image that:

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
````

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

## ✅ 3. Progressive Chaos Engineering Apps

Each scenario step has its own educational Python app:

### **Step 1: Network Failure** (`scenarios/step1_fail_network/app.py`)

```python
import sys
import socket

print("STEP 1: NETWORK FAILURE")
print("=" * 30)
print("Trying to connect to nonexistent host...")

try:
    s = socket.create_connection(("nonexistent-host-12345.com", 80), timeout=3)
    print("Unexpected: Network is working!")
    s.close()
    sys.exit(1)
except Exception as e:
    print(f"Network error as expected: {e}")
    print("This step is supposed to fail due to network issues.")
    sys.exit(1)
```

**Educational Value**: Shows how containers handle network connectivity issues.

### **Step 2: Resource Failure** (`scenarios/step2_fail_resource/app.py`)

```python
import sys
import numpy as np

print("STEP 2: RESOURCE FAILURE")
print("=" * 30)
print("Trying to allocate large array with limited memory...")

try:
    # Try to allocate 100MB array (will fail with 64MB limit)
    large_array = np.zeros((100, 100, 100), dtype=np.float64)
    print("Unexpected: Memory allocation succeeded!")
    sys.exit(1)
except MemoryError as e:
    print(f"Memory error as expected: {e}")
    print("This step is supposed to fail due to memory constraints.")
    sys.exit(1)
```

**Educational Value**: Demonstrates Docker resource limits and memory management.

### **Step 3: Service Failure** (`scenarios/step3_fail_service/app.py`)

```python
import sys
import redis

print("STEP 3: SERVICE FAILURE")
print("=" * 30)
print("Trying to connect to Redis service...")

try:
    r = redis.Redis(host='redis', port=6379, socket_connect_timeout=3)
    r.ping()
    print("Unexpected: Redis is available!")
    sys.exit(1)
except Exception as e:
    print(f"Service error as expected: {e}")
    print("This step is supposed to fail due to missing Redis service.")
    sys.exit(1)
```

**Educational Value**: Shows service dependencies and microservices architecture.

### **Step 4: Database Failure** (`scenarios/step4_fail_db/app.py`)

```python
import sys
import mysql.connector

print("STEP 4: DATABASE FAILURE")
print("=" * 30)
print("Trying to connect to MySQL database...")

try:
    conn = mysql.connector.connect(
        host='mysql',
        user='root',
        password='password',
        database='test',
        connection_timeout=3
    )
    print("Unexpected: MySQL is available!")
    conn.close()
    sys.exit(1)
except Exception as e:
    print(f"Database error as expected: {e}")
    print("This step is supposed to fail due to missing MySQL database.")
    sys.exit(1)
```

**Educational Value**: Demonstrates database connectivity and persistence issues.

### **Step 5: Success!** (`scenarios/step5_success/app.py`)

```python
import sys

print("STEP 5: SUCCESS!")
print("=" * 30)
print("All previous issues have been resolved!")
print("Network: Working")
print("Resources: Sufficient memory")
print("Services: Redis is running")
print("Database: MySQL is running")

print("CONGRATULATIONS!")
print("Your CI/CD pipeline is now chaos-resistant and production-ready!")

print("This is the final, chaos-free step. Well done!")

sys.exit(0)
```

**Educational Value**: Shows what a production-ready, resilient system looks like.

---

## ✅ 4. Test with Testcontainers

### **`tests/test_mysql.py`**

```python
from testcontainers.mysql import MySqlContainer
import sqlalchemy

def test_mysql_container():
    with MySqlContainer('mysql:8.0') as mysql:
        engine = sqlalchemy.create_engine(mysql.get_connection_url())
        with engine.connect() as conn:
            result = conn.execute("SELECT VERSION()")
            version = result.fetchone()[0]
            assert version.startswith("8.")
```

✅ This:

* Spins up a **real MySQL database** in Docker
* Connects via SQLAlchemy
* Confirms MySQL is running

---

## ✅ 4. Create Python Requirements

---

### **`docker-scenario-02/pipeline/requirements.txt`**

```
pytest
sqlalchemy
testcontainers[mysql]
```

---

## ✅ 5. Create Jenkins Pipeline Script

---

### **`pipeline/Jenkinsfile`**

```groovy
pipeline {
    agent any

    parameters {
        choice(
            name: "STAGE",
            choices: ["step1_fail_network", "step2_fail_resource", "step3_fail_service", "step4_fail_db", "step5_success"],
            description: "Select the scenario step to run"
        )
    }

    environment {
        SCENARIO_DIR = "scenarios/${params.STAGE}"
        IMAGE_NAME = "chaos-${params.STAGE}"
    }

    stages {
        stage("Build Scenario Docker Image") {
            steps {
                echo "🚧 Building Docker image for ${params.STAGE}..."
                sh """
                    docker build -t $IMAGE_NAME $SCENARIO_DIR
                """
            }
        }
        stage("Run Scenario Container") {
            steps {
                script {
                    echo "🚀 Running scenario: ${params.STAGE}"
                    def runArgs = ""
                    if (params.STAGE == "step2_fail_resource") {
                        runArgs = "--memory=64m --memory-swap=64m"
                    }
                    sh """
                        docker run --rm $runArgs $IMAGE_NAME | tee scenario.log
                    """
                }
            }
        }
        stage("Highlight What Was Fixed/Still Broken") {
            steps {
                script {
                    def messages = [
                        "step1_fail_network": [
                            fixed: "Nothing fixed yet! This is the first intentional failure.",
                            broken: "Network is broken. App cannot reach the outside world."
                        ],
                        "step2_fail_resource": [
                            fixed: "Network is now working! (But... memory is too low)",
                            broken: "Resource limits are too strict. App crashes with MemoryError."
                        ],
                        "step3_fail_service": [
                            fixed: "Network and resources are now fine! (But... missing Redis service)",
                            broken: "Service dependency (Redis) is missing. App cannot connect."
                        ],
                        "step4_fail_db": [
                            fixed: "Network, resources, and service are all good! (But... missing MySQL)",
                            broken: "Database connection fails. MySQL is not running."
                        ],
                        "step5_success": [
                            fixed: "All previous issues are fixed! 🎉",
                            broken: "Nothing! This is the chaos-free, production-ready step."
                        ]
                    ]
                    def msg = messages[params.STAGE]
                    echo "✅ FIXED: ${msg.fixed}"
                    echo "❌ STILL BROKEN: ${msg.broken}"
                }
            }
        }
    }
    post {
        always {
            echo "🏁 Scenario run complete! Check the logs above for details."
        }
        success {
            echo "🎉 Success!"
        }
        failure {
            echo "💥 Failure (as expected for some steps)!"
            script {
                echo "🔍 Last 10 lines of scenario.log (for debugging):"
                sh "tail -10 scenario.log || echo \"No scenario.log found\""
            }
        }
    }
}
```
        }

        stage('Chaos Monkey') {
            steps {
                sh '''
                    echo "Starting chaos container..."
                    docker run -d --name chaos busybox sh -c "while true; do sleep 5; done"
                    sleep 5
                    echo "Killing chaos container..."
                    docker kill chaos
                '''
            }
        }
    }
}
```

✅ What this pipeline does:

* Uses a Python Docker agent
* Installs Python dependencies
* Runs Python tests with Testcontainers (spins up MySQL inside Docker)
* Runs a Chaos Monkey:

  * Launches a random Docker container
  * Kills it to simulate unexpected failures

---

## ✅ 6. Automation and Testing Scripts

### **Setup Scripts**

- **`setup.sh`**: Complete Jenkins setup with Docker and plugins
- **`install_plugins.sh`**: Install required Jenkins plugins
- **`cleanup.sh`**: Clean up all containers and images
- **`test_setup.sh`**: Verify Jenkins is working correctly

### **Testing Scripts**

- **`test_all_scenarios.sh`**: Run all 5 scenarios locally for testing
- **`test_setup.sh`**: Verify the complete setup is working

### **Local Testing**

Run all scenarios locally to verify they work:

```bash
./test_all_scenarios.sh
```

This will:
- Build all scenario Docker images
- Run each scenario with appropriate parameters
- Show expected failures and success
- Provide educational output

---

## ✅ 7. Run the Pipeline

1. **Start Jenkins:**
   ```bash
   ./setup.sh
   ```

2. **Access Jenkins UI:**
   - Open [http://localhost:8080](http://localhost:8080)
   - Get initial password: `docker logs jenkins`

3. **Create Pipeline Job:**
   - Create new "Pipeline" job
   - Point to your Jenkinsfile
   - Run with parameters to select scenario step

4. **Watch Chaos Unfold:**
   - Each step demonstrates different failure modes
   - Educational messages explain what's happening
   - Progressive learning from failure to success
   - Clear "What's Fixed" and "What's Still Broken" messages

---

## ✅ 8. Educational Benefits

This scenario provides:

- **Progressive Learning**: Each step builds on the previous
- **Real-World Failures**: Simulates actual production issues
- **Clear Explanations**: Educational messages explain what's happening
- **Interactive Experience**: Participants can run and debug each step
- **Production Readiness**: Shows what makes a system resilient

---

## ✅ 9. Clean Up

When done, clean up everything:

```bash
./cleanup.sh
```

This removes:
- Jenkins container
- All scenario Docker images
- Docker networks
- Temporary files

