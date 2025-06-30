
# 🚀 Scenario 01 — Docker Build Chaos

> **Operation Chaos**  
> Chaos Agent wants your Docker builds to fail and your containers to break!  
> In this mission, we build Python Docker images, run containers, and prove our pipeline can defeat Docker sabotage.

---

## 🎯 Scenario Goal

✅ Learn how to:
- Build Docker images from multiple app versions
- Parameterize Docker builds in Jenkins
- Run and test Docker containers dynamically
- Detect and defeat Chaos Agent’s sabotage

---

## 🛠️ Technical Stack

- **Python 3.12+**
- **Docker**
- **Jenkins Pipeline**


---

## 🚀 How It Works

You have **5 versions** of a Python app in:

```

app/v1/
app/v2/
...
app/v5/

````

Each version demonstrates:
- Different Dockerfile configurations
- Intentional Docker build or runtime problems (Chaos Agent sabotage!)

---

## ✅ Jenkins Pipeline Overview

Your Jenkins pipeline:

✅ Takes a **version number** as input:

- `APP_VERSION = 1`
- or `2`, `3`, etc.

✅ Steps:
1. **Cleanup** any containers running on port 3000
2. Build Docker image:
    ```
    docker build -t ci-cd-chaos-app:v<APP_VERSION> .
    ```
3. Run Docker container:
    ```
    docker run -d -p 3000:3000 --name chaos-app-v<APP_VERSION> ...
    ```
4. Test HTTP response:
    ```
    curl http://localhost:3000
    ```
5. Clean up the container

---

## 🎯 Pipeline Parameters

| Parameter      | Description                                  |
|----------------|----------------------------------------------|
| `APP_VERSION`  | Which app version to build (1-5)             |

✅ If an invalid version is passed, Chaos Agent triggers a **funny error message**.

---

## ⚙️ Running Locally

Build version 2 locally:

```bash
docker build -t ci-cd-chaos-app:v2 \
    --build-arg APP_VERSION=2 \
    .
````

Run it:

```bash
docker run -d --name chaos-app-v2 -p 3000:3000 ci-cd-chaos-app:v2
```

Test:

```bash
curl http://localhost:3000
```

Stop the container:

```bash
docker rm -f chaos-app-v2
```

---

## 💥 Example Chaos

Chaos Agent might:

* Break the Docker build (missing requirements)
* Break the container startup (missing app)
* Cause HTTP failures

…but our pipeline **detects and fixes these issues!**

---

## ✅ Victory Condition

✨ You’ve defeated Chaos Agent if:

* Docker images build successfully
* Containers start correctly
* HTTP checks succeed
* Chaos-induced problems are detected and reported

---

## 🤯 Sample Jenkins Logs

```
=== Listing Docker build context ===
Dockerfile
app/v2/...

=== Building Docker image ===
Successfully tagged ci-cd-chaos-app:v2

=== Running container ===
Uvicorn running on http://0.0.0.0:3000

=== Testing app HTTP ===
HTTP Status: 200
✅ App responded successfully!
```

---

## 👊 Remember:

> **“Chaos is inevitable. Victory is optional. Choose wisely.”**
> — CI/CD Chaos Workshop

Go forth and defeat Chaos Agent! 🎉

---