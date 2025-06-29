# 🚀 Phase 2: Docker Builds & Multi-Version Chaos

> **“If you build it… make sure you can deploy it anywhere!”**  
> — CI/CD Chaos Workshop

Welcome to **Phase 2** of our CI/CD Chaos Workshop.  
This is where we bring chaos to life in containers!

---

## 🐳 Why Docker?

✅ Runs anywhere: laptop, cloud, Kubernetes  
✅ Simplifies deployments  
✅ Makes every app version reproducible  
✅ Perfect for CI/CD pipelines  
✅ Easy to test chaos versions side by side

---

## 🧩 What You’ll Learn

- How to write a **production-grade Dockerfile**
- How to use **multi-stage builds** for tiny images
- How to build multiple app versions for chaos testing
- How to deploy and switch versions with zero downtime
- How to inject visual changes for a **WOW factor** in demos

---

## 📦 Multi-Version Strategy

For this workshop, we built **5 versions** of our Python app.

| Version | Demo Content |
| ------- | ------------ |
| v1      | Simple Hello World |
| v2      | Emoji animations |
| v3      | Colored terminal output |
| v4      | Multi-line ASCII art |
| v5      | Randomized messages for a chaos surprise |

Each version:
- Has its own Python file (`main_vX.py`)
- Builds into a separate Docker image tag
- Runs on port **3000**

---

## 🔥 Example Multi-Stage Dockerfile

Here’s our **Dockerfile** using Python 3.12 slim:

```dockerfile
# Stage 1 - Builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 - Runtime
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY ./app ./app

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
````

Benefits:
✅ Tiny image size
✅ Fast deploys
✅ Clean environment for each build

---

## 🔨 Build & Run One Version

Let’s build version 3:

```bash
# Copy the right main.py
cp app/main_v3.py app/main.py

# Build Docker image
docker build -t ci-cd-chaos-app:v3 .

# Run it
docker run -d -p 3000:3000 --name chaos-app-v3 ci-cd-chaos-app:v3
```

---

## 🪄 Deploy Different Versions Easily

Instead of doing all those steps manually, we created a deploy script:

```bash
./deploy_version.sh 2
```

The script:

* Stops & removes any running container on port 3000
* Copies the version file into `main.py`
* Builds the Docker image
* Runs the new container

This makes **live demos super smooth**!

---

## ⚙️ Script Example

Here’s our deploy script:

```bash
#!/bin/bash

VERSION=$1

echo "👉 Switching to version $VERSION"

# Check for running containers
EXISTING=$(docker ps --filter "publish=3000" --format "{{.ID}}")

if [ ! -z "$EXISTING" ]; then
    echo "⚠️  A container is running on port 3000. Stopping and removing it..."
    docker stop $EXISTING
    docker rm $EXISTING
fi

cp app/main_v${VERSION}.py app/main.py

echo "🔨 Building Docker image..."
docker build -t ci-cd-chaos-app:v${VERSION} .

echo "🚀 Running container chaos-app-v${VERSION}..."
docker run -d -p 3000:3000 --name chaos-app-v${VERSION} ci-cd-chaos-app:v${VERSION}
```

---

## 🌈 Demo Magic

During your live workshop:

✅ Switch versions on the fly:

```bash
./deploy_version.sh 4
```

✅ Hit the app in your browser:

```
http://localhost:3000/
```

✅ Show how each version has:

* Different visuals
* Different Python logos
* Random chaos surprises (in v5)

This demonstrates:

* Reproducible Docker builds
* Safe version switching
* How small changes can become chaos in production

---

## 🤯 Why This Rocks

This phase proves:

* You can package chaos into Docker images
* You can confidently roll back or deploy new versions
* You can show chaos visually—**people remember this!**

This is pure CI/CD power.

---

[⬅️ Previous Phase](./tests.md) | [➡️ Next Phase → CI/CD Pipelines](./jenkins.md)

---
