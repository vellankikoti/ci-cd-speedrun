# 🧪 Scenario 02: Testcontainers Chaos

## Overview

This scenario demonstrates how to use Testcontainers in Jenkins to run real database integration tests in isolated Docker containers.

---

## 📁 Directory Structure

```
Jenkins/jenkins_scenarios/scenario_02_testcontainers/
├── Dockerfile
├── Jenkinsfile
├── README.md
├── requirements.txt
└── tests/
    ├── test_postgres_pass.py
    ├── test_postgres_fail.py
    ├── test_redis_pass.py
    └── test_redis_fail.py
```

---

## ✅ How to Set Up the Pipeline in Jenkins UI

1. **Open Jenkins** in your browser.
2. Click **"New Item"**.
3. Enter a name (e.g., `scenario_02_testcontainers`), select **Pipeline**, and click OK.
4. In the pipeline config:
   - Under **Pipeline script**, select **Pipeline script from SCM**.
   - Set **SCM** to **Git** and enter your repository URL.
   - Set **Script Path** to `Jenkins/jenkins_scenarios/scenario_02_testcontainers/Jenkinsfile`.
5. Click **Save**.

---

## ✅ How to Run the Pipeline

1. Click **"Build with Parameters"**.
2. Set the `TEST_MODE` parameter to `pass` (for passing tests) or `fail` (for chaos/failing tests).
3. Click **Build**.
4. Watch the console output for test execution and results.
5. Check for success or failure messages.

---

## ✅ What the Pipeline Does

- Builds a Docker image with all dependencies
- Runs Testcontainers-based integration tests for Postgres and Redis
- Supports both passing and intentionally failing test modes
- Cleans up containers after tests

---

## ✅ Troubleshooting

- **Tests fail to start:**
  - Ensure Docker is running and accessible from Jenkins.
  - Check that the Docker socket is mounted in Jenkins.
- **Database containers not starting:**
  - Check for port conflicts or resource limits on the Jenkins agent.
- **Permission errors:**
  - Make sure Jenkins has permission to run Docker commands.
- **Test mode confusion:**
  - Double-check the `TEST_MODE` parameter value (`pass` or `fail`).

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

**This scenario helps you master integration testing with real services in Jenkins using Testcontainers!** 