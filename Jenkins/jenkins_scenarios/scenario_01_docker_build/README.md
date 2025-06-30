# 🚀 Scenario 1 – Building Docker Images in Jenkins

## ✅ Why It Matters

Building Docker images in Jenkins ensures **consistent deployments** and reliable environments for all future phases of your CI/CD pipeline.

> **Chaos Event:**  
> "Docker build fails with: `Cannot connect to the Docker daemon!`"

---

## ✅ What You’ll Do

✅ Build a Docker image for your Python app.  
✅ Learn to pass parameters to Jenkins jobs.  
✅ See how Jenkins pipelines handle Docker builds.

---

## ✅ How to Run

1. Start Jenkins via Docker:
    ```bash
    docker run -d \
      -p 8080:8080 \
      -v jenkins_home:/var/jenkins_home \
      -v /var/run/docker.sock:/var/run/docker.sock \
      jenkins/jenkins:lts-docker
    ```

2. Copy this Jenkinsfile into a new pipeline job.

3. Run the job.

---

## ✅ Chaos Fixes

- Mount `/var/run/docker.sock` into your Jenkins container.
- Avoid building Docker images on Jenkins master. Use agents if possible.

---

## ✅ Expected Output

✅ Console log should show:
````

✅ Built image: sha256\:xxxxxxxxxxxxxx

```

---

## ✅ Best Practices

- Always tag images with a unique version.
- Keep images minimal for faster builds.
- Clean up old images to save disk space.

---
