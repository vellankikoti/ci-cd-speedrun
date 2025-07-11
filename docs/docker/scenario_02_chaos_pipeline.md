# 🚀 Docker Scenario 02 — Chaos-Proof Python CI/CD Pipeline with Testcontainers

**Goal:**  
- Demonstrate powerful Docker capabilities in CI/CD pipelines  
- Show how Testcontainers enables true **environment-independent testing**  
- Run chaos tests to simulate failures and prove pipeline resilience  
- Teach how to run Docker **inside** Docker (DinD) safely

This scenario fully justifies the title:

> **Setting Up Reliable CI/CD Pipelines with Python, K8s & Testcontainers**

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
✅ Jenkins runs a pipeline inside a Docker agent:
  - Spins up **Testcontainers** (ephemeral MySQL).
  - Runs Python tests talking to MySQL.
  - Launches a Chaos Monkey to kill containers randomly.

✅ Entire environment runs in Docker:
- No external MySQL
- No external services
- 100% self-contained

---

# ✅ Directory Structure

Your workshop directory will look like this:

```

docker-scenario-02/
│
├── jenkins-docker/
│     └── Dockerfile
│
├── pipeline/
│     ├── Jenkinsfile
│     └── requirements.txt
│
├── tests/
│     └── test\_mysql.py
│
└── README.md

````

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

## ✅ 3. Prepare Python Test with Testcontainers

---

### **`docker-scenario-02/tests/test_mysql.py`**

```python
# test_mysql.py

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

### **`docker-scenario-02/pipeline/Jenkinsfile`**

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        PIP_DISABLE_PIP_VERSION_CHECK = "1"
    }

    stages {
        stage('Install Requirements') {
            steps {
                sh '''
                    pip install -r pipeline/requirements.txt
                '''
            }
        }

        stage('Run Testcontainers Tests') {
            steps {
                sh '''
                    pytest tests/test_mysql.py
                '''
            }
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

## ✅ 6. Run the Pipeline

---

### 🔹 Jenkins UI Setup

1. Access Jenkins:

```
http://localhost:8080
```

2. Unlock Jenkins:

   * Get initial admin password:

     ```bash
     docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
     ```
   * Paste into browser.

3. Install recommended plugins.

4. Create a new Pipeline job:

* Name:

  ```
  chaos-ci-pipeline
  ```
* Pipeline script:

  * Copy-paste the entire **Jenkinsfile**

---

### 🔹 Run the Job

✅ Click **Build Now**.

Observe:

* Testcontainers starts a MySQL container.
* Python test connects and verifies MySQL.
* Chaos Monkey launches and kills a container.
* Pipeline still completes → proving resilience.

---

# ✅ What This Proves

✅ **Docker Power:**

* Run Docker inside Docker (DinD)
* Launch ephemeral services in pipelines
* Chaos engineering simulations

✅ **Testcontainers Magic:**

* Run databases for tests without installing anything
* Perfect for reliable CI/CD

✅ **Reliable Pipelines:**

* Even with chaos, the pipeline recovers

✅ **K8s Ready:**

* This entire pipeline can move into Kubernetes clusters:

  * Jenkins as Deployment
  * Docker socket in DinD pods
  * Works identically

---

# ✅ Running Everything

Run Jenkins:

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins-docker
```

Go to:

```
http://localhost:8080
```

Run the pipeline → watch chaos tests complete successfully.

---

# 🚦 Optional — Clean Up

```bash
docker stop jenkins
docker rm jenkins
docker rmi jenkins-docker
```
