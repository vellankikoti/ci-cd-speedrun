# 🚀 Scenario 2 – Running Testcontainers Tests

## ✅ Why It Matters

Testcontainers lets you spin up **real databases in Docker** during testing. It guarantees:

- Same database versions as production
- No external dependencies in your CI/CD pipeline
- Clean teardown after each test

> **Chaos Event:**  
> “Tests fail with: `Cannot connect to Docker daemon.`”

---

## ✅ What You’ll Do

✅ Run Python tests with pytest.  
✅ Automatically launch Postgres, MySQL, Redis containers.  
✅ Ensure tests don’t depend on external infrastructure.

---

## ✅ How to Run

1. Make sure Docker is installed and accessible inside Jenkins:
    ```bash
    docker run -d \
      -p 8080:8080 \
      -v jenkins_home:/var/jenkins_home \
      -v /var/run/docker.sock:/var/run/docker.sock \
      jenkins/jenkins:lts
    ```

2. Install Python dependencies:
    ```bash
    pip install pytest testcontainers
    ```

3. Copy this Jenkinsfile into a new Jenkins pipeline job.

4. Run the job.

---

## ✅ Chaos Fixes

- Ensure Jenkins has access to Docker (`/var/run/docker.sock`).
- Clean up leftover containers after tests:
    ```bash
    docker ps -a
    docker rm -f <container-id>
    ```
- Avoid port conflicts by using randomized ports in Testcontainers.

---

## ✅ Expected Output

✅ Console log should show:
````

tests/test\_postgres\_container.py PASSED
tests/test\_mysql\_container.py PASSED
...

```

---

## ✅ Best Practices

- Use randomized ports for containers.
- Clean up containers after each test suite.
- Never run integration tests against real production databases.

---
