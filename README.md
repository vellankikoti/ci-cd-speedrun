# Microservices Demo with ArgoCD & Argo Rollouts

## Prerequisites
- `kubectl` (configured for your cluster)
- `kustomize` (for overlays)
- [ArgoCD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/)
- [Argo Rollouts plugin](https://argoproj.github.io/argo-rollouts/installation/)
- Kubernetes cluster (Docker Desktop, minikube, kind, or cloud)

## 1. Install ArgoCD
### Local (Docker Desktop/minikube/kind)
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
- Expose ArgoCD UI:
  - `kubectl port-forward svc/argocd-server -n argocd 8080:443`
- Get initial admin password:
  - `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo`

### Cloud (GKE/EKS/AKS...)
- Same as above, but use a LoadBalancer or Ingress for the UI.

## 2. Bootstrap the App-of-Apps
```
kubectl apply -f argocd-apps/app-of-apps.yaml
```
- This will create all child Applications for each microservice.

## 3. Access the Demo App & ArgoCD UI
- **Frontend:**
  - Local: `http://localhost:30080` (NodePort overlay)
  - Cloud: Use the LoadBalancer IP
- **ArgoCD UI:**
  - Local: `http://localhost:8080`
  - Cloud: LoadBalancer/Ingress URL

## 4. Demo Deployment Strategies
- **Canary (frontend):**
  - Trigger a new image/tag in the Rollout manifest and watch the canary steps in ArgoCD and Argo Rollouts UI.
- **Blue-Green (recommendationservice):**
  - Trigger a new image/tag and watch preview/active services.
- **Rolling (other services):**
  - Update image/tag and observe standard rolling update.

## 5. Overlays for Local/Cloud
- Use `overlays/local` for NodePort (local demo)
- Use `overlays/cloud` for LoadBalancer (cloud demo)
- Switch overlays by updating the Application manifest `path` field or using kustomize.

## 6. Argo Rollouts UI
- Install Argo Rollouts dashboard:
  - `kubectl apply -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml`
  - `kubectl -n argo-rollouts port-forward deployment/argo-rollouts-dashboard 3100:3100`
  - Access at `http://localhost:3100`

## 7. Helper Scripts
- `scripts/setup.sh` – Install ArgoCD, bootstrap app-of-apps, apply overlays
- `scripts/teardown.sh` – Remove all resources
- `scripts/switch-overlay.sh` – Switch between overlays
- `scripts/reset-demo.sh` – Reset environment for a fresh demo

## 8. Troubleshooting
- Pods not starting? Check resource limits and cluster size.
- ArgoCD sync errors? Check Application manifest paths and overlay usage.
- Rollouts not visible? Ensure Argo Rollouts CRDs and dashboard are installed.

## 9. Folder Structure
```
05-gitops/
  argocd-apps/
    app-of-apps.yaml
    apps/
      frontend.yaml
      recommendationservice.yaml
      ...
  overlays/
    local/
    cloud/
    rollouts/
  services/
    adservice/
    cartservice/
    ...
```

## 10. Credits & References
- [GoogleCloudPlatform/microservices-demo](https://github.com/GoogleCloudPlatform/microservices-demo)
- [ArgoCD](https://argo-cd.readthedocs.io/)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
