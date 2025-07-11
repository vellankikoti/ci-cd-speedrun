#!/usr/bin/env python3
"""
🔧 Metrics Server Fix Script
Automatically diagnoses and fixes metrics server issues for auto-scaling
"""

import subprocess
import time
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def run_command(cmd, description, ignore_errors=False):
    """Run a command and return success status"""
    try:
        print(f"{Fore.CYAN}🔧 {description}...{Style.RESET_ALL}")
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print(f"{Fore.GREEN}✅ {description} completed{Style.RESET_ALL}")
        if result.stdout.strip():
            print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"{Fore.YELLOW}⚠️ {description} failed (ignoring): {e}{Style.RESET_ALL}")
            return False, e.stderr if e.stderr else str(e)
        else:
            print(f"{Fore.RED}❌ {description} failed: {e}{Style.RESET_ALL}")
            if e.stderr:
                print(f"Error: {e.stderr}")
            return False, e.stderr if e.stderr else str(e)

def detect_kubernetes_environment():
    """Detect the type of Kubernetes environment"""
    print(f"{Fore.CYAN}🔍 Detecting Kubernetes environment...{Style.RESET_ALL}")
    
    # Check for Docker Desktop
    success, output = run_command("kubectl get nodes -o wide", "Check nodes", ignore_errors=True)
    if success and "docker-desktop" in output:
        print(f"{Fore.GREEN}📱 Detected: Docker Desktop{Style.RESET_ALL}")
        return "docker-desktop"
    
    # Check for Minikube
    try:
        result = subprocess.run(["minikube", "status"], capture_output=True, text=True)
        if "Running" in result.stdout:
            print(f"{Fore.GREEN}🎯 Detected: Minikube{Style.RESET_ALL}")
            return "minikube"
    except FileNotFoundError:
        pass
    
    # Check for kind
    if success and "kind" in output:
        print(f"{Fore.GREEN}🐳 Detected: kind{Style.RESET_ALL}")
        return "kind"
    
    # Default to generic
    print(f"{Fore.BLUE}☁️ Detected: Generic Kubernetes (likely cloud){Style.RESET_ALL}")
    return "generic"

def check_metrics_server_status():
    """Check if metrics server is installed and running"""
    print(f"\n{Fore.YELLOW}📊 Checking metrics server status...{Style.RESET_ALL}")
    
    # Check if metrics server deployment exists
    success, output = run_command(
        "kubectl get deployment metrics-server -n kube-system", 
        "Check metrics server deployment", 
        ignore_errors=True
    )
    
    if not success:
        print(f"{Fore.RED}❌ Metrics server not installed{Style.RESET_ALL}")
        return False
    
    # Check if pods are running
    success, output = run_command(
        "kubectl get pods -n kube-system -l k8s-app=metrics-server", 
        "Check metrics server pods", 
        ignore_errors=True
    )
    
    if success and "Running" in output:
        print(f"{Fore.GREEN}✅ Metrics server pods are running{Style.RESET_ALL}")
        
        # Test if metrics are actually available
        success, _ = run_command("kubectl top nodes", "Test metrics availability", ignore_errors=True)
        if success:
            print(f"{Fore.GREEN}✅ Metrics API working correctly{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️ Metrics server running but API not responding{Style.RESET_ALL}")
            return False
    else:
        print(f"{Fore.RED}❌ Metrics server pods not running{Style.RESET_ALL}")
        return False

def install_metrics_server_docker_desktop():
    """Install metrics server for Docker Desktop"""
    print(f"\n{Fore.YELLOW}🐳 Installing metrics server for Docker Desktop...{Style.RESET_ALL}")
    
    metrics_server_yaml = """
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    k8s-app: metrics-server
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
    rbac.authorization.k8s.io/aggregate-to-view: "true"
  name: system:aggregated-metrics-reader
rules:
- apiGroups:
  - metrics.k8s.io
  resources:
  - pods
  - nodes
  verbs:
  - get
  - list
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    k8s-app: metrics-server
  name: system:metrics-server
rules:
- apiGroups:
  - ""
  resources:
  - nodes/metrics
  verbs:
  - get
- apiGroups:
  - ""
  resources:
  - pods
  - nodes
  verbs:
  - get
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server-auth-reader
  namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: extension-apiserver-authentication-reader
subjects:
- kind: ServiceAccount
  name: metrics-server
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server:system:auth-delegator
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
- kind: ServiceAccount
  name: metrics-server
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    k8s-app: metrics-server
  name: system:metrics-server
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:metrics-server
subjects:
- kind: ServiceAccount
  name: metrics-server
  namespace: kube-system
---
apiVersion: v1
kind: Service
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server
  namespace: kube-system
spec:
  ports:
  - name: https
    port: 443
    protocol: TCP
    targetPort: https
  selector:
    k8s-app: metrics-server
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: metrics-server
  strategy:
    rollingUpdate:
      maxUnavailable: 0
  template:
    metadata:
      labels:
        k8s-app: metrics-server
    spec:
      containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
        - --kubelet-insecure-tls
        image: registry.k8s.io/metrics-server/metrics-server:v0.6.4
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /livez
            port: https
            scheme: HTTPS
          periodSeconds: 10
        name: metrics-server
        ports:
        - containerPort: 4443
          name: https
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /readyz
            port: https
            scheme: HTTPS
          initialDelaySeconds: 20
          periodSeconds: 10
        resources:
          requests:
            cpu: 100m
            memory: 200Mi
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
        volumeMounts:
        - mountPath: /tmp
          name: tmp-dir
      nodeSelector:
        kubernetes.io/os: linux
      priorityClassName: system-cluster-critical
      serviceAccountName: metrics-server
      volumes:
      - emptyDir: {}
        name: tmp-dir
---
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  labels:
    k8s-app: metrics-server
  name: v1beta1.metrics.k8s.io
spec:
  group: metrics.k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: metrics-server
    namespace: kube-system
  version: v1beta1
  versionPriority: 100
"""
    
    # Write YAML to file
    with open('/tmp/metrics-server.yaml', 'w') as f:
        f.write(metrics_server_yaml)
    
    # Apply the configuration
    success, _ = run_command("kubectl apply -f /tmp/metrics-server.yaml", "Install metrics server")
    return success

def install_metrics_server_minikube():
    """Install metrics server for Minikube"""
    print(f"\n{Fore.YELLOW}🎯 Installing metrics server for Minikube...{Style.RESET_ALL}")
    
    # Enable metrics server addon
    success, _ = run_command("minikube addons enable metrics-server", "Enable metrics server addon")
    return success

def install_metrics_server_generic():
    """Install metrics server for generic Kubernetes"""
    print(f"\n{Fore.YELLOW}☁️ Installing metrics server for generic Kubernetes...{Style.RESET_ALL}")
    
    # Use official metrics server
    success, _ = run_command(
        "kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml",
        "Install official metrics server"
    )
    return success

def fix_metrics_server_permissions():
    """Fix common metrics server permission issues"""
    print(f"\n{Fore.YELLOW}🔐 Fixing metrics server permissions...{Style.RESET_ALL}")
    
    # Patch metrics server for insecure TLS (local development)
    patch_cmd = '''kubectl patch deployment metrics-server -n kube-system --type='json' -p='[
      {
        "op": "add",
        "path": "/spec/template/spec/containers/0/args/-",
        "value": "--kubelet-insecure-tls"
      }
    ]' '''
    
    success, _ = run_command(patch_cmd, "Patch metrics server for insecure TLS", ignore_errors=True)
    return success

def wait_for_metrics_server():
    """Wait for metrics server to be ready"""
    print(f"\n{Fore.YELLOW}⏳ Waiting for metrics server to be ready...{Style.RESET_ALL}")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        print(f"{Fore.CYAN}⏳ Attempt {attempt + 1}/{max_attempts}...{Style.RESET_ALL}")
        
        # Check pod status
        success, output = run_command(
            "kubectl get pods -n kube-system -l k8s-app=metrics-server", 
            "Check pod status", 
            ignore_errors=True
        )
        
        if success and "Running" in output and "1/1" in output:
            # Test metrics API
            success, _ = run_command("kubectl top nodes", "Test metrics API", ignore_errors=True)
            if success:
                print(f"{Fore.GREEN}✅ Metrics server is ready and responding!{Style.RESET_ALL}")
                return True
        
        time.sleep(10)
    
    print(f"{Fore.RED}❌ Metrics server failed to become ready within timeout{Style.RESET_ALL}")
    return False

def restart_metrics_server():
    """Restart metrics server deployment"""
    print(f"\n{Fore.YELLOW}🔄 Restarting metrics server...{Style.RESET_ALL}")
    
    success, _ = run_command(
        "kubectl rollout restart deployment/metrics-server -n kube-system", 
        "Restart metrics server deployment"
    )
    
    if success:
        success, _ = run_command(
            "kubectl rollout status deployment/metrics-server -n kube-system --timeout=300s", 
            "Wait for restart to complete"
        )
    
    return success

def main():
    """Main metrics server fix function"""
    print(f"{Fore.CYAN}🔧 METRICS SERVER FIX UTILITY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Fixing metrics server for Kubernetes auto-scaling...{Style.RESET_ALL}")
    print()
    
    # Detect environment
    env_type = detect_kubernetes_environment()
    
    # Check current status
    metrics_working = check_metrics_server_status()
    
    if metrics_working:
        print(f"\n{Fore.GREEN}🎉 Metrics server is already working correctly!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ You can proceed with Scenario 3 deployment{Style.RESET_ALL}")
        return
    
    # Try to fix based on environment
    print(f"\n{Fore.YELLOW}🔧 Attempting to fix metrics server...{Style.RESET_ALL}")
    
    if env_type == "docker-desktop":
        # Try restart first
        if restart_metrics_server():
            if wait_for_metrics_server():
                print(f"\n{Fore.GREEN}🎉 Metrics server fixed with restart!{Style.RESET_ALL}")
                return
        
        # Install from scratch
        if install_metrics_server_docker_desktop():
            if wait_for_metrics_server():
                print(f"\n{Fore.GREEN}🎉 Metrics server installed successfully!{Style.RESET_ALL}")
                return
    
    elif env_type == "minikube":
        if install_metrics_server_minikube():
            if wait_for_metrics_server():
                print(f"\n{Fore.GREEN}🎉 Metrics server enabled successfully!{Style.RESET_ALL}")
                return
    
    else:  # generic or cloud
        if install_metrics_server_generic():
            # Try permission fix for local clusters
            fix_metrics_server_permissions()
            if wait_for_metrics_server():
                print(f"\n{Fore.GREEN}🎉 Metrics server installed successfully!{Style.RESET_ALL}")
                return
    
    # Final verification
    print(f"\n{Fore.CYAN}🧪 Final verification...{Style.RESET_ALL}")
    if check_metrics_server_status():
        print(f"\n{Fore.GREEN}🎉 SUCCESS! Metrics server is now working!{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}🚀 You can now proceed with Scenario 3:{Style.RESET_ALL}")
        print(f"   python3 deploy-auto-scaling-hero.py")
    else:
        print(f"\n{Fore.RED}❌ FAILED to fix metrics server automatically{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}🔧 MANUAL STEPS TO TRY:{Style.RESET_ALL}")
        print(f"   1. Check your Kubernetes version: kubectl version")
        print(f"   2. Check cluster resources: kubectl get nodes")
        print(f"   3. Check metrics server logs: kubectl logs -n kube-system -l k8s-app=metrics-server")
        print(f"   4. For Docker Desktop: Restart Docker Desktop completely")
        print(f"   5. For Minikube: minikube delete && minikube start")
        print(f"   6. See troubleshooting.md for more detailed steps")

if __name__ == "__main__":
    main()