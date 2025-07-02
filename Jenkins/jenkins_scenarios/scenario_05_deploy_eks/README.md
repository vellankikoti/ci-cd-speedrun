# 🚀 Scenario 5: EKS Deployment Chaos — CI/CD Chaos Workshop

## Overview

**Scenario 5** simulates real-world AWS EKS deployment chaos by testing both successful and intentionally failing deployments. It provides robust reporting and integrates seamlessly with Jenkins CI/CD pipelines.

---

## 📁 File Structure

```
Jenkins/jenkins_scenarios/scenario_05_deploy_eks/
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── run_tests.py
├── tests/
│   ├── test_deploy_eks_pass.py
│   ├── test_deploy_eks_fail.py
│   └── deploy/
│       ├── deployment-pass.yaml
│       ├── deployment-fail.yaml
│       ├── service.yaml
│       └── configmap.yaml
└── reports/
    ├── eks_deployment_report.html
    ├── eks_deployment_report.json
    └── pytest_*.html
```

---

## ⚡️ Quick Start

### 1. **Prerequisites**
- AWS EKS cluster (running and accessible)
- AWS CLI v2, `kubectl`, Docker, Python 3.11+
- Jenkins with credentials:
  - `aws-credentials` (AWS Access Key ID/Secret)

### 2. **Local Testing**

```bash
cd Jenkins/jenkins_scenarios/scenario_05_deploy_eks
pip install -r requirements.txt
python run_tests.py           # Run all tests
python run_tests.py --pass-only   # Only PASS test
python run_tests.py --fail-only   # Only FAIL test
```

### 3. **Docker Testing**

```bash
docker build -t chaos-workshop-scenario-5 .
docker run --rm \
  -v $HOME/.kube/config:/root/.kube/config:ro \
  -v $(pwd)/reports:/app/reports \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  -e AWS_DEFAULT_REGION=us-west-2 \
  chaos-workshop-scenario-5
```

---

## 🏗️ Jenkins Pipeline Usage

- Use the provided `Jenkinsfile` in this directory.
- **Parameters:**
  - `RUN_SCENARIO_5` (boolean): Enable/disable scenario
  - `SCENARIO_5_PASS` (boolean): Run successful deployment test
  - `SCENARIO_5_FAIL` (boolean): Run failure simulation test
  - `CLUSTER_NAME`: EKS cluster name
  - `AWS_REGION`: AWS region
  - `CLEANUP_AFTER_TESTS`: Clean up resources after tests

### **Pipeline Steps:**
1. **Preparation:** Verifies scenario files and structure
2. **Build Docker Image:** Builds isolated test image
3. **Setup AWS & Kubernetes:** Creates kubeconfig for cluster access
4. **Validate Kubernetes Files:** Ensures all manifests exist
5. **Live Cluster Monitoring:** Shows cluster state before deployment
6. **Deploy & Monitor PASS Test:** Deploys working app and validates
7. **Deploy & Monitor FAIL Test:** Deploys broken app and captures chaos
8. **Cleanup:** Optionally removes test resources
9. **Archive Reports:** Saves HTML/JSON reports as Jenkins artifacts

### **To Run:**
- Go to Jenkins → This scenario pipeline
- Click **"Build with Parameters"**
- Set parameters as needed
- Download/view reports from Jenkins artifacts

---

## 📊 Report Details
- **HTML reports:** Executive summary, timeline, pod status, events, failure analysis
- **JSON reports:** Machine-readable results for automation
- **Location:** `reports/` directory (archived by Jenkins)

---

## 🛠️ Troubleshooting
- **Cannot connect to EKS?**
  - Check kubeconfig and AWS credentials
  - Run `aws eks update-kubeconfig --region <region> --name <cluster>`
- **Permission denied?**
  - Check Kubernetes RBAC and AWS IAM permissions
- **Build fails?**
  - Clean Docker cache: `docker system prune -f`
- **Test timeouts?**
  - Increase timeout in `run_tests.py`
- **No reports?**
  - Check container logs and ensure `reports/` is present

---

## 🏆 Best Practices
- Use non-root user in Docker for security
- Never hardcode secrets; use Jenkins credentials
- Clean up resources after tests
- Review HTML/JSON reports for actionable insights
- Integrate with `run_all_scenarios.py` for full workshop automation

---

## 🙌 Credits
Built for the **CI/CD Chaos Workshop** — Scenario 5: EKS Deployment Chaos

For questions or improvements, contact the workshop maintainers.