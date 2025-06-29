# 🐳 Phase 2 - Docker Mastery

Welcome to **Phase 2** of the CI/CD Chaos Workshop — the stage where we dive deep into Docker, learn how to build Python apps properly, and create chaos-worthy Docker images for production!

This phase demonstrates:

✅ Multi-stage builds  
✅ Docker image size comparisons  
✅ Production vs. dev Dockerfiles  
✅ Deploying multiple versions of your app  
✅ Generating Docker analysis reports  
✅ Beautiful visuals and chaos engineering insights!

---

## 🚀 What We’re Building

We’re developing a FastAPI Python app:
- 5 different versions
- Each with new features, animations, or visuals
- Deployed via Docker
- Automatically analyzed for:
  - image size
  - layer count
  - potential vulnerabilities (future scope!)

> 🎯 **Goal:** Teach participants how tiny changes in Dockerfiles affect:
> - Build times
> - Image sizes
> - Security
> - Performance

---

## ✨ How to Deploy Versions

Instead of manually switching files and building containers, we’ve automated everything!

Run:

```bash
python workshop_tools/deploy_version.py --version 3
````

✅ This:

* Copies the correct `main_vX.py` to `main.py`
* Builds your Docker image
* Stops/removes any container running on port 3000
* Runs the new version
* Generates a beautiful HTML Docker report under:

  ```
  reports/version_3/docker_report.html
  ```

---

## 📊 Docker Analysis Reports

Every deploy automatically runs:

```bash
python workshop_tools/generate_docker_report.py --version 3
```

This analyzes:

* Image size (MB)
* Number of layers
* Base image used
* Warnings about potential optimization

And creates an HTML report like:

> ![Docker Report Screenshot](https://dummyimage.com/600x300/2c3e50/ffffff\&text=Docker+Report+Screenshot)

---

## 🐍 Demo Scenarios

During the workshop:
✅ Deploy version 1 → tiny image
✅ Deploy version 2 → adds emojis → image grows
✅ Deploy version 3 → multi-stage build → shrinks image
✅ Deploy version 4 → adds background workers → image grows
✅ Deploy version 5 → chaos animations → biggest image

Show how to:

* Avoid large images
* Use `.dockerignore` effectively
* Minimize layers
* Prefer multi-stage builds
* Separate dev vs prod images

---

## 🤹 Why Multi-Stage Builds Matter

Without multi-stage:

* Images \~400MB or more
* Contains unnecessary build tools
* Slower deployment

With multi-stage:

* Images \~100MB or less
* Production only includes:

  * compiled Python code
  * minimum runtime packages
* Fewer attack surfaces

Example snippet:

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

---

## 💡 Tips for Workshop Demos

✅ Show:

* Docker image size differences:

  ```bash
  docker images
  ```
* Layer differences:

  ```bash
  dive ci-cd-chaos-app:v3
  ```
* Why small images deploy faster
* How multi-stage prevents secrets from leaking into images

---

## 🔥 Chaos Engineering with Docker

Optional chaos ideas:

* Randomly build wrong versions
* Introduce slow builds to show caching
* Simulate “docker build” errors
* Show how CI/CD can detect these issues early

---

## ✅ Run It All Together

To deploy version 5 and see a full chaos experience:

```bash
python workshop_tools/deploy_version.py --version 5
```

Check:

* App running at [http://localhost:3000](http://localhost:3000)
* Docker report under:

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

[⬅️ Previous Phase](./tests.md) | [➡️ Next Phase → CI/CD Pipelines](./jenkins.md)

---
