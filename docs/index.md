# 🐙 CI/CD Chaos Workshop

Welcome to the **CI/CD Chaos Workshop** — a unique journey where we don’t just build software, we break it, fix it, and make it better than ever.

In this workshop, you’ll:
✅ Build real apps in Python  
✅ Containerize them with Docker  
✅ Test them dynamically with Testcontainers  
✅ Automate deployments with Jenkins & Kubernetes  
✅ Learn chaos engineering techniques for CI/CD pipelines  
✅ Generate interactive reports & visualizations

…and leave with skills your future self will thank you for!

---

## 🚀 Workshop Phases

Below is your roadmap through chaos:

---

## 💻 **Setup & Prerequisites**

👉 See:
- [Setup Guide](phases/setup.md)

Covers:
✅ Installing Python & Docker  
✅ Virtual environments  
✅ Local tools for testing and chaos

---

## 🧪 **Dynamic Database Testing**

**Phase:**  Testcontainers

👉 See:
- [MySQL Testing Docs](testcontainers/mysql.md)
- [MariaDB Testing Docs](testcontainers/mariadb.md)
- [Postgres Testing Docs](testcontainers/postgres.md)
- [MongoDB Testing Docs](testcontainers/mongodb.md)
- [Redis Testing Docs](testcontainers/redis.md)

You’ll:
✅ Spin up real databases in Docker  
✅ Write Python tests against live DBs  
✅ Generate HTML test reports  
✅ Visualize container startup/shutdown with Testcontainers Desktop  
✅ Practice chaos scenarios like container crashes and delays

---

## 🐳 **Docker Mastery & Multi-Version Apps**

👉 See:
- [Docker Phase](phases/docker.md)

Key takeaways:
✅ Multi-stage Docker builds  
✅ Python image best practices  
✅ Deploy multiple versions of your app  
✅ Compare image sizes & layers  
✅ Generate Docker analysis reports  
✅ Introduce chaos in builds

---

## 🤖 **Jenkins Pipeline Chaos**

👉 See:
- [Jenkins Phase](phases/jenkins.md)
- [Scenario 01: Docker Build](jenkins/scenario_01_docker_build.md)
- [Scenario 02: Testcontainers](jenkins/scenario_02_testcontainers.md)
- [Scenario 03: HTML Reports](jenkins/scenario_03_html_reports.md)
- [Scenario 04: Manage Secrets](jenkins/scenario_04_manage_secrets.md)
- [Scenario 05: Deploy to EKS](jenkins/scenario_05_deploy_eks.md)

Key takeaways:
✅ Building Jenkins pipelines for:
  - Docker builds
  - Testcontainers tests
  - Automated report publishing

✅ Chaos ideas:
- Randomly fail builds
- Slow steps to simulate network lag
- Break Docker layers intentionally

---

## ☸️ **Kubernetes Chaos & Scalability**

👉 See:
- [Kubernetes Phase](phases/k8s.md)

Key takeaways:
✅ Deploying our apps to Kubernetes  
✅ Chaos experiments with:
  - killing pods
  - random delays
  - pod resource limits
✅ Using tools like:
  - K9s
  - Chaos Mesh
  - Grafana dashboards for live insights

---

## 🎓 **Certificate of Chaos**

Once you complete all phases, you’ll:
✅ Receive a custom PDF Certificate  
✅ Have live demos you can show future employers  
✅ Feel confident in:
- Python DevOps
- Docker mastery
- Chaos engineering
- Dynamic testing

👉 [Certificate Info](certificate.md)

---

## 🧭 Why This Workshop Exists

Most workshops teach:
> “Here’s how to build a perfect pipeline.”

But real life looks like this:
- Servers crash
- DBs fail
- Docker images bloat
- Networks hang
- Tests mysteriously fail

This workshop prepares you for **the real world.** We deliberately cause chaos so you’ll know how to handle it—and look like a hero!

---

# Let’s Create Some Chaos. 🔥

→ Start with:
- [Setup Guide](phases/setup.md)
- Then dive into:
  - [TestContainers](phases/testcontainers.md)
  - [Docker](phases/docker.md)

…and prepare for chaos you’ll never forget!

---
