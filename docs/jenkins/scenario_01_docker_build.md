# 🐳 Scenario 01: Docker Build Chaos

## Overview

This scenario teaches you how to build, tag, and run Python Docker images in Jenkins, simulating real-world CI/CD challenges and sabotage.

---

## 📁 Directory Structure

```
Jenkins/jenkins_scenarios/scenario_01_docker_build/
├── Dockerfile
├── Jenkinsfile
├── README.md
├── requirements.txt
```

---

## ✅ How to Set Up the Pipeline in Jenkins UI

1. **Open Jenkins** in your browser (usually at http://localhost:8080).
2. Click **"New Item"**.
3. Enter a name (e.g., `scenario_01_docker_build`), select **Pipeline**, and click OK.
4. In the pipeline config:
   - Under **Pipeline script**, select **Pipeline script from SCM**.
   - Set **SCM** to **Git** and enter your repository URL.
   - Set **Script Path** to `Jenkins/jenkins_scenarios/scenario_01_docker_build/Jenkinsfile`.
5. Click **Save**.

---

## ✅ How to Run the Pipeline

1. Click **"Build with Parameters"**.
2. Set the `APP_VERSION` parameter (1–5) to choose which app version to build.
3. Click **Build**.
4. Watch the console output for build, run, and test steps.
5. Check for success or failure messages.

---

## ✅ What the Pipeline Does

- Cleans up any containers running on port 3000
- Builds the Docker image for the selected app version
- Runs the container and exposes port 3000
- Tests the HTTP response from the app
- Cleans up the container after the test

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Docker Build Failures

```groovy
// Simulate Docker build failures
stage('Build Docker Image') {
    steps {
        script {
            // Randomly fail builds to test resilience
            if (Math.random() < 0.1) {
                error "Simulated Docker build failure"
            }
            
            sh "docker build -t chaos-app:${APP_VERSION} ."
        }
    }
}
```

### ✅ Scenario 2: Container Startup Delays

```groovy
// Simulate slow container startup
stage('Run Container') {
    steps {
        script {
            sh "docker run -d -p 3000:3000 --name chaos-app chaos-app:${APP_VERSION}"
            
            // Add artificial delay
            sleep 10
            
            // Test if app responds
            sh "curl -f http://localhost:3000/health || exit 1"
        }
    }
}
```

---

## ✅ Troubleshooting

- **Docker build fails:**
  - Ensure Docker is running and the Docker socket is mounted in Jenkins.
  - Check for typos in the `APP_VERSION` parameter.
- **App does not respond:**
  - Check the container logs in Jenkins output.
  - Make sure the app version exists in the repo.
- **Permission errors:**
  - Make sure Jenkins has permission to run Docker commands (mount `/var/run/docker.sock`).

---

## ✅ Useful Commands

- See running containers:
  ```bash
  docker ps
  ```
- Check logs for a container:
  ```bash
  docker logs <container_id>
  ```
- Remove a container:
  ```bash
  docker rm -f <container_id>
  ```

---

## 📊 Monitoring & Reporting

### ✅ Pipeline Metrics

- Build success rate
- Average build time
- Docker image size trends
- Container startup time

### ✅ Chaos Metrics

- Number of simulated failures
- Recovery time from failures
- System resilience score

---

**Next:** [Scenario 02: Testcontainers](scenario_02_testcontainers.md) | [Scenario 03: HTML Reports](scenario_03_html_reports.md) | [Scenario 04: Manage Secrets](scenario_04_manage_secrets.md) | [Scenario 05: Deploy to EKS](scenario_05_deploy_eks.md)

---

**This scenario helps you master Docker builds in Jenkins and prepares you for more advanced CI/CD chaos!** 🔥 