# 🎯 Scenario 1: Participant Guide

## Your Mission: Defeat Chaos with Python!

### Prerequisites
- Kubernetes cluster running (Docker Desktop, Minikube, or EKS)
- Python 3.8+ installed
- kubectl configured

### Step 1: Setup (2 minutes)
```bash
# Navigate to scenario directory
cd scenarios/01-python-deploy

# Install Python dependencies
pip3 install -r hero-solution/requirements.txt

# Verify your cluster is working
kubectl cluster-info