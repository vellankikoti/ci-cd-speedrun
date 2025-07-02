
# 🐳 Phase 2 – Docker Mastery

Welcome to **Phase 2** of the CI/CD Chaos Workshop — the stage where we dive deep into Docker, learn how to build Python apps properly, and create chaos-worthy Docker images for production!

This phase demonstrates:

✅ Multi-stage builds  
✅ Docker image size comparisons  
✅ Production vs. dev Dockerfiles  
✅ Deploying multiple versions of your app  
✅ Generating Docker analysis reports

> 🎯 **Goal:** Show how tiny changes in Dockerfiles affect:
> - Build times
> - Image sizes
> - Security
> - Performance

---

## 🚀 What We’re Building

We’re developing a FastAPI Python app:

- 5 different versions
- Each with new features, animations, or visuals
- Deployed via Docker
- Automatically analyzed for:
    - image size
    - layer count
    - base image details

> **Chaos Agent says:** “Let’s bloat those images!”  
> Our mission: keep images lean and secure.

---

## ✨ How to Deploy Versions

Instead of manually switching files and building containers, we’ve automated everything!

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

During the workshop, we’ll:

✅ Deploy version 1 → tiny image  
✅ Deploy version 2 → adds emojis → image grows  
✅ Deploy version 3 → multi-stage build → image shrinks  
✅ Deploy version 4 → adds background workers → image grows  
✅ Deploy version 5 → chaos animations → biggest image

We’ll learn how to:

- Avoid large images
- Use `.dockerignore` effectively
- Minimize layers
- Prefer multi-stage builds
- Separate dev vs prod images

**Chaos Agent’s trap:**  
> “Add one more pip install… what’s the harm?”

We’ll prove why that’s dangerous.

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
> “Let’s leave secrets in the image. No one will find them…”

We’ll prove how scanning tools and image inspection can expose secrets.

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

- App running at [http://localhost:3000](http://localhost:3000)
- Docker report under:

```
reports/version_5/docker_report.html
```

---

## 🏆 Why This Matters

By the end of Phase 2, you’ll understand:

✅ Why Docker image size matters  
✅ How to keep production images secure  
✅ Why multi-stage builds are your friend  
✅ How to visualize Docker data for stakeholders

…and you’ll have fun chaos demos to prove it!

---

[⬅️ Previous Phase: TestContainers](./testcontainers.md) | [Next Phase: CI/CD Pipelines ➡️](./jenkins.md)
