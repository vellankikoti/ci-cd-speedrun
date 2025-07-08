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

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Database Connection Failures

```python
def test_postgres_connection_failure():
    """Simulate PostgreSQL connection failures in CI/CD"""
    with PostgresContainer("postgres:15") as postgres:
        # Simulate network partition
        postgres.get_docker_client().pause(postgres.get_container_id())
        
        # Verify our app handles the failure gracefully
        with pytest.raises(ConnectionError):
            create_connection(postgres.get_connection_url())
```

### ✅ Scenario 2: Slow Database Queries

```python
def test_redis_slow_operations():
    """Simulate slow Redis operations in CI/CD"""
    with RedisContainer("redis:7-alpine") as redis:
        client = redis.get_client()
        
        # Simulate slow operation
        import time
        start_time = time.time()
        
        # Perform operation
        client.set("test", "value")
        client.get("test")
        
        # Verify it completes within reasonable time
        assert time.time() - start_time < 5.0
```

### ✅ Scenario 3: Resource Constraints

```python
def test_memory_constrained_database():
    """Test database behavior under memory constraints"""
    with PostgresContainer("postgres:15") as postgres:
        # Set memory limit
        postgres.with_memory_limit("50m")
        
        conn = create_connection(postgres.get_connection_url())
        
        # Try to insert large dataset
        try:
            for i in range(1000):
                conn.execute(text(f"INSERT INTO test_table VALUES ({i}, 'data');"))
        except Exception as e:
            # Handle memory constraint gracefully
            assert "memory" in str(e).lower() or "resource" in str(e).lower()
```

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

## 📊 Monitoring & Reporting

### ✅ Test Metrics

- Test execution time
- Container startup time
- Database connection success rate
- Test pass/fail ratio

### ✅ Chaos Metrics

- Number of simulated failures
- Recovery time from database failures
- System resilience under stress

---

**Next:** [Scenario 01: Docker Build](scenario_01_docker_build.md) | [Scenario 03: HTML Reports](scenario_03_html_reports.md) | [Scenario 04: Manage Secrets](scenario_04_manage_secrets.md) | [Scenario 05: Deploy to EKS](scenario_05_deploy_eks.md)

---

**This scenario helps you master integration testing with real services in Jenkins using Testcontainers!** 🔥 