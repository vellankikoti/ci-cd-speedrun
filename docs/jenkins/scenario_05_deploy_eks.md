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

**This scenario helps you master Kubernetes deployments in Jenkins, preparing you for real-world cloud CI/CD challenges!** 