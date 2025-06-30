# 🚀 Scenario 5 – Deploying to AWS EKS

## ✅ Why It Matters

Modern apps run on Kubernetes. Jenkins pipelines must:

- Deploy apps safely
- Validate YAML manifests
- Handle rollbacks if chaos strikes

> **Chaos Event:**  
> “Bad YAML breaks production. Pods never come up.”

---

## ✅ What You’ll Do

✅ Update kubeconfig to connect to AWS EKS.  
✅ Validate your deployment YAML with `kubeval`.  
✅ Apply manifests to EKS cluster.  
✅ Monitor deployment rollout.

---

## ✅ How to Run

1. Ensure your AWS credentials exist in Jenkins as `aws-credentials`.

2. Place your Kubernetes YAML here:
    ```
    k8s/deployment.yaml
    ```

3. Copy this Jenkinsfile into a Jenkins pipeline job.

4. Run the job.

---

## ✅ Chaos Fixes

- Run `kubeval` before deploying.  
- Always check rollout status:
    ```bash
    kubectl rollout status deployment my-deployment
    ```
- Roll back if deployment fails:
    ```bash
    kubectl rollout undo deployment my-deployment
    ```

---

## ✅ Expected Output

✅ Console log should show:
````

✅ Validating Kubernetes YAML manifests...
🚀 Applying Kubernetes manifests...
deployment.apps/my-deployment successfully rolled out

```

---

## ✅ Best Practices

- Never deploy YAML without validating syntax first.  
- Use unique image tags for each deployment.  
- Prefer Helm or Kustomize for complex deployments.

---
