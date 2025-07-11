# 🐳 Docker Mastery

Welcome to **Phase 2** of the CI/CD Chaos Workshop — the stage where we dive deep into Docker, learn how to build Python apps properly, and create chaos-worthy Docker images for production!

---

## 🚀 What You'll Experience in This Phase

### **Scenario 01: Streaming Server with Docker**
- Launch your own live streaming server using Docker and Owncast.
- Connect OBS Studio, stream video, and share it with the world.
- Learn about containerized media, port mapping, and real-world Docker deployment.
- See how Docker makes complex app stacks portable and reproducible.

### **Scenario 02: Progressive Chaos Engineering Pipeline**
- Enter the world of chaos engineering — safely, in Docker!
- Run a Jenkins pipeline that simulates real-world failures: network outages, resource exhaustion, missing dependencies, and database crashes.
- Watch as each pipeline step introduces a new failure, then learn how to fix it.
- Master Docker-in-Docker (DinD), container orchestration, and resilient CI/CD design.
- Build confidence in troubleshooting and debugging containerized pipelines.

### **Scenario 03: Docker Networking Magic**
- Deploy a live voting app and see how containers communicate (or fail to!).
- Simulate broken networks, missing databases, and container isolation.
- Fix networking issues live and watch your app come to life.
- Learn about Docker networks, bridges, and best practices for multi-container apps.
- Experience the "AHA!" moment when everything just works.

### **Scenario 04: Docker Image Scanner**
- Upload any Dockerfile and get instant, real-world security and best-practices analysis.
- See how Trivy scans for vulnerabilities and how small Dockerfile changes impact security.
- Learn to optimize, harden, and benchmark your images — and get actionable feedback.
- Discover the power of automated image analysis in modern DevOps.

### **Scenario 05: Docker Escape Room**
- Enter a gamified, puzzle-based Docker adventure.
- Solve hands-on challenges: volumes, networking, secrets, resource limits, and multi-stage builds.
- Race against the clock, outsmart Dr. NullPointer, and escape the Docker Vault!
- Experience Docker as a real-world troubleshooting and problem-solving journey.
- Walk away with Docker mastery, confidence, and a smile.

---

## 🎬 What You'll Learn
- How to containerize and run real-world apps (media, web, CI/CD, games)
- The art of troubleshooting and debugging Dockerized systems
- Chaos engineering and resilience in pipelines
- Docker networking, volumes, and resource management
- Security scanning and best practices for Dockerfiles
- The fun and power of hands-on, scenario-based learning

> **This phase is your Docker bootcamp, playground, and proving ground.**
> Get ready to build, break, fix, and master Docker — with a little chaos and a lot of fun!

---

## 🚀 What We're Building

We're developing a FastAPI Python app:

- 5 different versions
- Each with new features, animations, or visuals
- Deployed via Docker
- Automatically analyzed for:
    - image size
    - layer count
    - base image details

> **Chaos Agent says:** "Let's bloat those images!"  
> Our mission: keep images lean and secure.

---

## ✨ How to Deploy Versions

Instead of manually switching files and building containers, we've automated everything!

Run:

```bash
python Docker/workshop_tools/deploy_version.py 3
```

✅ This:

- Copies the correct `main_vX.py` to `main.py`
- Builds your Docker image
- Stops/removes any container running on port 3000
- Runs the new version
- Generates a beautiful HTML Docker report under:

```
reports/version_3/docker_report.html
```

---

## 📊 Docker Analysis Reports

Every deploy automatically runs:

```bash
python Docker/workshop_tools/generate_docker_report.py 3
```

This analyzes:

✅ Image size (MB)  
✅ Number of layers  
✅ Base image used  
✅ Recommendations for optimization

It creates a report like:

**Why it matters:** This makes Docker transparent for developers and helps avoid bloat.

---

## 🐍 Demo Scenarios

During the workshop, we'll:

✅ Deploy version 1 → tiny image  
✅ Deploy version 2 → adds emojis → image grows  
✅ Deploy version 3 → multi-stage build → image shrinks  
✅ Deploy version 4 → adds background workers → image grows  
✅ Deploy version 5 → chaos animations → biggest image

We'll learn how to:

- Avoid large images
- Use `.dockerignore` effectively
- Minimize layers
- Prefer multi-stage builds
- Separate dev vs prod images

**Chaos Agent's trap:**  
> "Add one more pip install… what's the harm?"

We'll prove why that's dangerous.

---

## 🤹 Why Multi-Stage Builds Matter

Without multi-stage:

- Images ~400MB or more
- Contains unnecessary build tools
- Slower deployments

With multi-stage:

- Images ~100MB or less
- Production only includes:
    - compiled Python code
    - minimal runtime packages
- Fewer attack surfaces

Example Dockerfile:

```dockerfile
# First stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Second stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
```

**Best Practice:** Keep the runtime image as slim as possible.

---

## 💡 Tips for Workshop Demos

✅ Show Docker image size differences:

```bash
docker images
```

✅ Check layer digests:

```bash
docker inspect ci-cd-chaos-app:v3
```

✅ Show Docker build history:

```bash
docker history ci-cd-chaos-app:v3
```

✅ Explain why small images deploy faster.

✅ Highlight how multi-stage prevents secrets from leaking into final images.

**Chaos Agent:**  
> "Let's leave secrets in the image. No one will find them…"

We'll prove how scanning tools and image inspection can expose secrets.

---

## 🔥 Chaos Engineering with Docker

Optional chaos ideas:

- Randomly build incorrect versions
- Introduce slow builds to show Docker caching
- Simulate Docker build errors
- Show how CI/CD detects Docker issues early

**Mission:** Prove that pipelines protect you from Docker chaos.

---

## ✅ Run It All Together

To deploy version 5 and see the full chaos experience:

```bash
python Docker/workshop_tools/deploy_version.py --version 5
```

Then check:

```bash
# View the running app
curl http://localhost:3000

# Check the Docker report
open reports/version_5/docker_report.html
```

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Docker Build Failures

```bash
# Simulate Docker build failures
docker build --no-cache -t chaos-app:broken .
# Expected: Build fails due to missing dependencies
```

### ✅ Scenario 2: Image Size Explosion

```bash
# Compare image sizes
docker images chaos-app --format "table {{.Tag}}\t{{.Size}}"
# Expected: Version 5 should be significantly larger than Version 1
```

### ✅ Scenario 3: Security Vulnerabilities

```bash
# Scan for vulnerabilities
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image chaos-app:v1
# Expected: Find potential security issues
```

---

## 📊 Monitoring & Reporting

### ✅ Docker Metrics

- Image build time
- Image size trends
- Layer count analysis
- Security vulnerability count

### ✅ Chaos Metrics

- Build failure rate
- Image size explosion rate
- Security issue detection rate

---

## 🎯 Next Steps

✅ **Phase 2 Complete:** You now have Docker mastery!  
✅ **Ready for Phase 3:** [Jenkins Pipeline Chaos](jenkins.md)  
✅ **Chaos Agent Status:** Defeated in Docker optimization! 🕶️

---

**Remember:** Docker is your first line of defense against deployment chaos. Keep images lean, secure, and fast! 🔥
