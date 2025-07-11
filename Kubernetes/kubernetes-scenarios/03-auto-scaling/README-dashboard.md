# Production-Grade Auto-scaling Dashboard

## Build and Deploy

1. **Build the Docker image:**
   ```bash
   docker build -t dashboard:latest -f Dockerfile.dashboard .
   ```

2. **Push the image to a registry (if using a remote cluster):**
   - Tag and push as needed for your environment.

3. **Create the namespace (if not already):**
   ```bash
   kubectl create namespace scaling-challenge
   ```

4. **Deploy the dashboard app and service:**
   ```bash
   kubectl apply -f dashboard-deployment.yaml
   ```

5. **Access the dashboard:**
   - **NodePort:**
     - Open [http://localhost:31500](http://localhost:31500) (Docker Desktop)
     - Or use your node IP if on a remote cluster
   - **Port Forward (alternative):**
     ```bash
     kubectl port-forward svc/dashboard-service -n scaling-challenge 8080:5000
     # Then open http://localhost:8080
     ```

## What You Get
- Real-time metrics and scaling events from the actual Kubernetes cluster
- No simulation or mimic data
- Production-grade, demo-ready auto-scaling dashboard

## Troubleshooting
- If you see connection issues, ensure the pod is running and the service is of type NodePort.
- Use `kubectl logs` to check for Flask errors.
- Make sure your Docker image is available to your cluster (push to a registry if needed). 