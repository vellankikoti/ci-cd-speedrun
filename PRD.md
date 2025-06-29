# Product Requirements Document (PRD)

---

## 🎯 Workshop Title

**Setting Up Reliable CI/CD Pipelines with Python, K8s & Testcontainers**

---

## ✨ Abstract

CI/CD (Continuous Integration and Continuous Deployment) has become a fundamental part of DevOps, helping teams deliver code quickly and catch potential problems before they turn into costly production issues. Without a solid CI/CD process, developers often struggle with manual deployments, inconsistent environments, and unexpected bugs that slip through the cracks, causing frustration and unplanned downtime.

In this session, we will walk you step by step through setting up a dependable CI/CD pipeline using Python, Jenkins, TestContainers, AWS, and Kubernetes. Starting with basic configurations, we’ll automate everything from running tests to building containers and deploying them on a scalable Kubernetes cluster. By writing simple Python scripts, you will learn how to streamline repetitive tasks and create a smooth release workflow. We’ll also take time to discuss common pitfalls and show how to troubleshoot them, so you feel equipped to handle real-world challenges.

Whether you’re new to CI/CD or looking to refine your existing DevOps skills, this tutorial aims to make complex workflows easier to grasp. Expect hands-on practice, clear explanations, and practical takeaways that you can apply in your own projects right away. By the end, you’ll see how using Python at each stage not only automates time-consuming tasks but also brings a new level of reliability to the entire deployment process.

Our goal is to help you build confidence in creating a pipeline that brings predictability to your releases, saves your team time, and keeps your applications running smoothly in production. If you’ve ever wanted to see how a proper CI/CD setup can transform the way you ship software, this is your chance to dive in and see it come to life step by step.

---

## 🎬 Workshop Narrative

**Operation Chaos: Break It to Make It 🧨🔧**

> “Real DevOps heroes don’t fear chaos. They master it.”

Chaos Agent 🕶️ is sabotaging your deployments. Your mission is to build a robust CI/CD pipeline that defeats Chaos at every stage. You’ll intentionally break things — then fix them — proving how pipelines save the day.

---

## 👥 Target Audience

✅ Beginners new to DevOps  
✅ Intermediate engineers (comfortable with Git, Python, Docker)  
✅ Advanced DevOps engineers (production-grade expectations)

---

## 🕰️ Workshop Duration

- Total time: **120–150 minutes (2–2.5 hours)**
- Hands-on time: **80–90%**

---

## 💡 Design Philosophy

- **Steve Jobs’ Storytelling:** Emotional narrative, fun characters (Chaos Agent), “aha” moments.
- **Einstein’s Simplicity:** Explain complex topics in plain language.

---

## 📚 Learning Outcomes

By the end of the workshop, participants will:

✅ Understand why pipelines fail and how to prevent chaos  
✅ Confidently write Python automation for CI/CD  
✅ Know how to integrate:
  - Jenkins
  - Testcontainers
  - Docker
  - Kubernetes deployments  
✅ Deploy a Python app from scratch to production on Kubernetes  
✅ Understand how to troubleshoot real-world DevOps issues

---

## 🚀 Workshop Phases

---

### 🕒 0–15 min → Mission Briefing

- Introduce storyline
- Explain repo structure
- Check developer environment:
  - Python ≥ 3.10
  - Docker Desktop
  - Minikube or EKS
  - Git installed
- Clone starter repo

✅ Emotional hook:
> “Chaos Agent is coming for us!”

---

### 🕒 15–35 min → Phase 1: Test Mayhem

Chaos strikes:
- Flaky tests
- Misconfigured env vars
- Missing services for integration tests

Tasks:
- Write Python tests with pytest
- Integrate Testcontainers:
  - Postgres Testcontainer
  - Redis Testcontainer
- Prove tests pass reliably

✅ Emotional payoff:
> “My tests are bulletproof!”

---

### 🕒 35–55 min → Phase 2: Docker Sabotage

Chaos Agent breaks:
- Docker build errors
- Missing dependencies
- Wrong Python versions

Tasks:
- Create a Dockerfile
- Solve:
  - Multi-stage build
  - Pip caching
  - Runtime image size reduction
- Build + run locally

✅ Emotional payoff:
> “My image works everywhere!”

---

### 🕒 55–80 min → Phase 3: Pipeline Showdown

Chaos crashes Jenkins:
- Pipeline syntax errors
- Missing secrets
- Unmanaged credentials

Tasks:
- Write Jenkinsfile:
  - Lint
  - Build Docker
  - Run Testcontainers tests
- Add credentials management
- Learn blue/green deploy triggers

✅ Emotional payoff:
> “CI/CD saves me from disaster!”

---

### 🕒 80–105 min → Phase 4: K8s Warzone

Chaos deploys:
- Corrupt YAML manifests
- Wrong resource limits
- Environment misconfigs

Tasks:
- Deploy to K8s:
  - Helm or raw YAML
  - Probes
  - Rollbacks
- Validate YAML with kubeval
- Fix Chaos-induced errors

✅ Emotional payoff:
> “My cluster is safe from Chaos!”

---

### 🕒 105–130 min → Phase 5: Final Victory Deploy

- Run full pipeline end-to-end
- Check live deployment
- Simulate Chaos Agent’s attacks → verify pipeline defenses

✅ Emotional payoff:
> “Chaos Agent defeated!”

---

### 🕒 130–150 min → Wrap-Up & Certificates

- 5-question final quiz
- Generate PDF certificate:
  - Workshop title
  - Participant name
  - Unique completion ID
- Confetti animation

✅ Emotional payoff:
> “I’m a Certified Chaos Slayer!”

---

## 🛠️ Technical Stack

- Python 3.10+
- FastAPI (optional backend for certificate generation)
- Pytest
- Testcontainers Python
- Docker
- Jenkins
- Kubernetes (Minikube or EKS)
- Helm (optional)
- MkDocs + Material

---

## 🗂️ GitHub Repo Branching Strategy

- `main` → Complete working pipeline
- Phases:
  - `phase-0-setup`
  - `phase-1-tests`
  - `phase-2-docker`
  - `phase-3-jenkins`
  - `phase-4-k8s`
  - `phase-5-final`

Each branch:
✅ Fully functional  
✅ Includes instructions in README  
✅ Documented in MkDocs

---

## 📝 MkDocs Structure

Pages:
- Home
- Phases 1–5
- Quizzes
- Certificate page

Features:
✅ Navigation sidebar  
✅ LocalStorage progress tracking or backend progress tracking  
✅ Confetti animations  
✅ Emojis for Chaos events  
✅ Certificate download (PDF)  
✅ Ready for GitHub Pages, Netlify, or Vercel

---

## 🎯 Emotional and Educational Goals

By the end, participants should:
✅ Feel confident deploying real apps  
✅ Understand how to troubleshoot chaos  
✅ See how Python glues pipelines together  
✅ Leave with a working pipeline in GitHub  
✅ **Remember the experience for years** thanks to storytelling & visuals

---

## ✅ Metrics of Success

✅ >90% attendees complete the pipeline  
✅ >80% pass the final quiz  
✅ Positive emotional feedback: “I feel capable!”  
✅ Certificates downloaded  
✅ Attendees share the experience on social media

---

# ✅ Conclusion

This PRD fully defines:
- Title & abstract
- Narrative & emotional journey
- Technical steps & phases
- Repo structure
- MkDocs layout
- Storytelling integration

Any future LLM prompt referring to:
> “Be in context of my CI/CD Chaos Workshop”

…should automatically load this blueprint.

---

