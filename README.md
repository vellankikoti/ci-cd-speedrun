# 🚀 Operation Chaos: CI/CD Chaos Workshop

> **Workshop Title:** Setting Up Reliable CI/CD Pipelines with Python, K8s & Testcontainers  
> **Tagline:** Real DevOps heroes don’t fear chaos. They master it.

---

## 🎯 Workshop Overview

Welcome to **Operation Chaos!**  

In this workshop, we’ll build a **production-grade CI/CD pipeline** that can detect and defeat chaos:

✅ Python test automation with pytest + Testcontainers  
✅ Docker best practices  
✅ Jenkins pipeline for end-to-end automation  
✅ Kubernetes deployments (Minikube/EKS)  
✅ Troubleshooting real DevOps failures  
✅ MkDocs site for documentation  
✅ Certificate generation after completion

Your mission:
> Defeat Chaos Agent 🕶️ who’s sabotaging your deployments. Break things intentionally—and fix them with DevOps skills.

---

## 🕒 Workshop Duration

- Total time: ~2.5 hours
- Hands-on time: 80–90%
- Level: Beginner → Advanced DevOps

---

## 📂 Project Structure

```

ci-cd-chaos-workshop/
├── app/                  # FastAPI app
├── docs/                 # MkDocs documentation
├── requirements.txt      # Python dependencies
├── mkdocs.yml            # MkDocs config
├── PRD.md                # Product Requirements Document
├── README.md             # This file

````

---

## 🛠️ Tools You’ll Need

✅ Python ≥ 3.10  
✅ Docker Desktop  
✅ Git  
✅ Minikube (or an EKS cluster)  
✅ Node.js (optional for some dev tools)

Install:
```bash
brew install kubectl minikube
pip install mkdocs mkdocs-material
````

---

## 🚦 Branches

We’ll evolve the pipeline in **phases**:

| Branch            | Description                           |
| ----------------- | ------------------------------------- |
| `phase-0-setup`   | Initial project skeleton              |
| `phase-1-tests`   | Python tests + Testcontainers         |
| `phase-2-docker`  | Docker build and fixes                |
| `phase-3-jenkins` | Jenkins pipeline                      |
| `phase-4-k8s`     | Kubernetes deployments                |
| `phase-5-final`   | End-to-end pipeline, chaos simulation |

Each branch:
✅ Working code
✅ Instructions in README
✅ MkDocs pages updated

---

## 🚀 How to Run Locally

### Run the App

```bash
# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run FastAPI
uvicorn app.main:app --reload
```

Visit:

```
http://127.0.0.1:8000
```

---

### Serve the MkDocs Site

```bash
mkdocs serve -a localhost:8001
```

Visit:

```
http://127.0.0.1:8001
```

---

## 📜 License

MIT License

---

## 💬 Questions?

Raise an issue, or join the discussion during the live workshop!

Let’s defeat Chaos Agent together. 💥

```

---