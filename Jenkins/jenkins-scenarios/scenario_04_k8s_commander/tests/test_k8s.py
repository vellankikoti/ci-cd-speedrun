#!/usr/bin/env python3
"""
K8s Commander - Kubernetes Tests
Tests for Kubernetes-specific functionality.
"""

import pytest
import subprocess
import os
import sys
import time
import yaml

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_kubectl_command(command):
    """Run a kubectl command and return the result."""
    try:
        result = subprocess.run(f"kubectl {command}", shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_kubectl_available():
    """Test that kubectl is available."""
    print("\n☸️ Testing kubectl availability...")
    
    success, stdout, stderr = run_kubectl_command("version --client")
    if not success:
        print(f"❌ kubectl not available: {stderr}")
        return False
    
    print("✅ kubectl is available!")
    print(f"Version: {stdout}")
    return True

def test_kubernetes_connection():
    """Test connection to Kubernetes cluster."""
    print("\n☸️ Testing Kubernetes connection...")
    
    success, stdout, stderr = run_kubectl_command("cluster-info")
    if not success:
        print(f"❌ Cannot connect to Kubernetes cluster: {stderr}")
        return False
    
    print("✅ Connected to Kubernetes cluster!")
    print(f"Cluster info: {stdout}")
    return True

def test_kubernetes_manifests():
    """Test that Kubernetes manifests are valid."""
    print("\n☸️ Testing Kubernetes manifests...")
    
    manifest_files = [
        "k8s/namespace.yaml",
        "k8s/configmap.yaml",
        "k8s/secret.yaml",
        "k8s/deployment.yaml",
        "k8s/service.yaml",
        "k8s/ingress.yaml",
        "k8s/hpa.yaml"
    ]
    
    for manifest_file in manifest_files:
        if not os.path.exists(manifest_file):
            print(f"❌ Manifest file not found: {manifest_file}")
            return False
        
        # Validate YAML syntax
        try:
            with open(manifest_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {manifest_file} - YAML syntax valid")
        except yaml.YAMLError as e:
            print(f"❌ {manifest_file} - YAML syntax error: {e}")
            return False
        
        # Validate with kubectl
        success, stdout, stderr = run_kubectl_command(f"apply --dry-run=client -f {manifest_file}")
        if not success:
            print(f"❌ {manifest_file} - kubectl validation failed: {stderr}")
            return False
        
        print(f"✅ {manifest_file} - kubectl validation passed")
    
    return True

def test_kubernetes_deployment():
    """Test Kubernetes deployment."""
    print("\n☸️ Testing Kubernetes deployment...")
    
    # Create namespace
    success, stdout, stderr = run_kubectl_command("apply -f k8s/namespace.yaml")
    if not success:
        print(f"❌ Failed to create namespace: {stderr}")
        return False
    
    print("✅ Namespace created!")
    
    # Apply all manifests
    success, stdout, stderr = run_kubectl_command("apply -f k8s/")
    if not success:
        print(f"❌ Failed to apply manifests: {stderr}")
        return False
    
    print("✅ Manifests applied!")
    
    # Wait for deployment to be ready
    print("⏳ Waiting for deployment to be ready...")
    success, stdout, stderr = run_kubectl_command("rollout status deployment/k8s-commander -n k8s-commander --timeout=60s")
    if not success:
        print(f"❌ Deployment not ready: {stderr}")
        return False
    
    print("✅ Deployment is ready!")
    
    # Check pods
    success, stdout, stderr = run_kubectl_command("get pods -n k8s-commander -l app=k8s-commander")
    if not success:
        print(f"❌ Failed to get pods: {stderr}")
        return False
    
    print("✅ Pods are running!")
    print(f"Pods: {stdout}")
    
    # Check services
    success, stdout, stderr = run_kubectl_command("get services -n k8s-commander")
    if not success:
        print(f"❌ Failed to get services: {stderr}")
        return False
    
    print("✅ Services are created!")
    print(f"Services: {stdout}")
    
    return True

def test_kubernetes_health_checks():
    """Test Kubernetes health checks."""
    print("\n☸️ Testing Kubernetes health checks...")
    
    # Get pod name
    success, stdout, stderr = run_kubectl_command("get pods -n k8s-commander -l app=k8s-commander -o jsonpath='{.items[0].metadata.name}'")
    if not success:
        print(f"❌ Failed to get pod name: {stderr}")
        return False
    
    pod_name = stdout.strip()
    print(f"Testing pod: {pod_name}")
    
    # Test health endpoint
    success, stdout, stderr = run_kubectl_command(f"exec -n k8s-commander {pod_name} -- curl -f http://localhost:5000/health")
    if not success:
        print(f"❌ Health check failed: {stderr}")
        return False
    
    print("✅ Health check passed!")
    
    # Test ready endpoint
    success, stdout, stderr = run_kubectl_command(f"exec -n k8s-commander {pod_name} -- curl -f http://localhost:5000/ready")
    if not success:
        print(f"❌ Readiness check failed: {stderr}")
        return False
    
    print("✅ Readiness check passed!")
    
    # Test metrics endpoint
    success, stdout, stderr = run_kubectl_command(f"exec -n k8s-commander {pod_name} -- curl -f http://localhost:5000/metrics")
    if not success:
        print(f"❌ Metrics check failed: {stderr}")
        return False
    
    print("✅ Metrics check passed!")
    
    return True

def test_kubernetes_scaling():
    """Test Kubernetes scaling."""
    print("\n☸️ Testing Kubernetes scaling...")
    
    # Scale up
    success, stdout, stderr = run_kubectl_command("scale deployment k8s-commander -n k8s-commander --replicas=5")
    if not success:
        print(f"❌ Failed to scale up: {stderr}")
        return False
    
    print("✅ Scaled up to 5 replicas!")
    
    # Wait for scaling
    time.sleep(10)
    
    # Check replicas
    success, stdout, stderr = run_kubectl_command("get pods -n k8s-commander -l app=k8s-commander")
    if not success:
        print(f"❌ Failed to get pods: {stderr}")
        return False
    
    print(f"✅ Pods after scaling: {stdout}")
    
    # Scale down
    success, stdout, stderr = run_kubectl_command("scale deployment k8s-commander -n k8s-commander --replicas=3")
    if not success:
        print(f"❌ Failed to scale down: {stderr}")
        return False
    
    print("✅ Scaled down to 3 replicas!")
    
    return True

def test_kubernetes_cleanup():
    """Test Kubernetes cleanup."""
    print("\n☸️ Testing Kubernetes cleanup...")
    
    # Delete all resources
    success, stdout, stderr = run_kubectl_command("delete -f k8s/")
    if not success:
        print(f"❌ Failed to delete resources: {stderr}")
        return False
    
    print("✅ Resources deleted!")
    
    # Wait for cleanup
    time.sleep(5)
    
    # Check that namespace is gone
    success, stdout, stderr = run_kubectl_command("get namespace k8s-commander")
    if success:
        print("⚠️ Namespace still exists")
        return False
    
    print("✅ Namespace deleted!")
    
    return True

def main():
    """Run all Kubernetes tests."""
    print("☸️ K8s Commander - Kubernetes Tests")
    print("=" * 50)
    
    tests = [
        ("kubectl Availability", test_kubectl_available),
        ("Kubernetes Connection", test_kubernetes_connection),
        ("Kubernetes Manifests", test_kubernetes_manifests),
        ("Kubernetes Deployment", test_kubernetes_deployment),
        ("Kubernetes Health Checks", test_kubernetes_health_checks),
        ("Kubernetes Scaling", test_kubernetes_scaling),
        ("Kubernetes Cleanup", test_kubernetes_cleanup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✅ {test_name} passed!")
                passed += 1
            else:
                print(f"❌ {test_name} failed!")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Kubernetes tests passed!")
        return True
    else:
        print("❌ Some Kubernetes tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
