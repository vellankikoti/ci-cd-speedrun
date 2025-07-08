# ☸️ Scenario 05: Deploy to AWS EKS

## Overview

This scenario teaches you how to deploy applications to AWS EKS using Jenkins, including both successful and intentionally failing deployments. You'll learn to validate manifests, monitor rollouts, and troubleshoot Kubernetes chaos.

---

## 📁 Directory Structure

```
Jenkins/jenkins_scenarios/scenario_05_deploy_eks/
├── Dockerfile
├── Jenkinsfile
├── JenkinsfileAuth
├── Jenkins-Setup.md
├── README.md
├── requirements.txt
└── tests/
    └── deploy/
        ├── deployment-pass.yaml
        ├── deployment-fail.yaml
        ├── service.yaml
        └── configmap.yaml
```

---

## ✅ How to Set Up the Pipeline in Jenkins UI

1. **Open Jenkins** in your browser.
2. Click **"New Item"**.
3. Enter a name (e.g., `scenario_05_deploy_eks`), select **Pipeline**, and click OK.
4. In the pipeline config:
   - Under **Pipeline script**, select **Pipeline script from SCM**.
   - Set **SCM** to **Git** and enter your repository URL.
   - Set **Script Path** to `Jenkins/jenkins_scenarios/scenario_05_deploy_eks/Jenkinsfile`.
5. Click **Save**.

---

## ✅ How to Run the Pipeline

1. Click **"Build with Parameters"**.
2. Set the following parameters as needed:
   - `RUN_SCENARIO_5`: Enable/disable scenario
   - `SCENARIO_5_PASS`: Run successful deployment test
   - `SCENARIO_5_FAIL`: Run failure simulation test
   - `CLUSTER_NAME`: EKS cluster name
   - `AWS_REGION`: AWS region
   - `CLEANUP_AFTER_TESTS`: Clean up resources after tests
3. Click **Build**.
4. Watch the console output for deployment, monitoring, and results.
5. Download/view reports from Jenkins artifacts after the build completes.

---

## ✅ What the Pipeline Does

- Builds a Docker image with all dependencies
- Sets up AWS and Kubernetes access
- Validates Kubernetes manifests
- Deploys to EKS (both PASS and FAIL scenarios)
- Monitors rollout and pod status
- Optionally cleans up resources after tests
- Archives reports as Jenkins build artifacts

---

## 🧪 Chaos Testing Scenarios

### ✅ Scenario 1: Deployment Failures

```yaml
# deployment-fail.yaml - Intentionally broken deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chaos-app-fail
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chaos-app
  template:
    metadata:
      labels:
        app: chaos-app
    spec:
      containers:
      - name: chaos-app
        image: chaos-app:latest
        resources:
          requests:
            memory: "1Gi"  # Too much memory request
            cpu: "1000m"   # Too much CPU request
        ports:
        - containerPort: 3000
```

### ✅ Scenario 2: Pod Eviction Simulation

```python
def test_pod_eviction():
    """Simulate pod eviction in EKS"""
    # Deploy application
    kubectl_apply("deployment-pass.yaml")
    
    # Simulate node pressure
    kubectl_drain_node("node-1", "--force", "--ignore-daemonsets")
    
    # Verify pods reschedule
    pods = kubectl_get_pods("--field-selector=spec.nodeName=node-1")
    assert len(pods) == 0
```

### ✅ Scenario 3: Service Discovery Failures

```python
def test_service_discovery_failure():
    """Test service discovery under chaos"""
    # Deploy service
    kubectl_apply("service.yaml")
    
    # Simulate DNS failure
    kubectl_patch_service("chaos-app-service", 
                         '{"spec":{"clusterIP":"10.0.0.999"}}')
    
    # Verify service is unreachable
    with pytest.raises(Exception):
        kubectl_exec("chaos-app-pod", "curl", "chaos-app-service:3000")
```

---

## ✅ Troubleshooting

- **Cannot connect to EKS:**
  - Check kubeconfig and AWS credentials.
  - Ensure your cluster is running and accessible.
- **YAML validation fails:**
  - Check for syntax errors in your manifest files in `tests/deploy/`.
- **Pods stuck or failing:**
  - Use Jenkins logs to inspect rollout status and pod events.
- **Build fails:**
  - Check for missing dependencies in `requirements.txt`.
  - Review the Docker build logs for errors.
- **No reports generated:**
  - Check the Jenkins workspace and ensure reports are written to the correct directory.

---

## ✅ Useful Commands

- See running pods and services:
  ```bash
  kubectl get pods
  kubectl get services
  ```
- Check rollout status:
  ```bash
  kubectl rollout status deployment/<deployment-name>
  ```
- View events for troubleshooting:
  ```bash
  kubectl get events --sort-by=.metadata.creationTimestamp
  ```

---

## 📊 Monitoring & Reporting

### ✅ Deployment Metrics

- Deployment success rate
- Rollout time
- Pod startup time
- Resource utilization

### ✅ Chaos Metrics

- Number of deployment failures
- Recovery time from failures
- Service discovery reliability
- Node failure resilience

---

**Next:** [Scenario 01: Docker Build](scenario_01_docker_build.md) | [Scenario 02: Testcontainers](scenario_02_testcontainers.md) | [Scenario 03: HTML Reports](scenario_03_html_reports.md) | [Scenario 04: Manage Secrets](scenario_04_manage_secrets.md)

---

**This scenario helps you master Kubernetes deployments in Jenkins, preparing you for real-world cloud CI/CD challenges!** 🔥 