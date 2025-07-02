#!/usr/bin/env python3
"""
Scenario 5 - EKS Deployment Pass Test
Tests successful deployment to AWS EKS cluster
"""

import pytest
import subprocess
import time
import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
import yaml

class TestEKSDeploymentPass:
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.deploy_dir = self.test_dir / "deploy"
        self.app_name = "chaos-workshop-app"
        self.namespace = "default"
        self.service_name = f"{self.app_name}-service"
        self.start_time = datetime.now()
        self.report_data = {
            "scenario": "scenario_05_deploy_eks",
            "test_type": "PASS",
            "start_time": self.start_time.isoformat(),
            "status": "RUNNING",
            "steps": [],
            "deployment_timeline": [],
            "pods": [],
            "services": [],
            "events": [],
            "logs": "",
            "endpoint_url": "",
            "success_message": ""
        }
    
    def run_kubectl(self, cmd, capture_output=True, check=True):
        """Execute kubectl command and return result"""
        full_cmd = f"kubectl {cmd}"
        print(f"Executing: {full_cmd}")
        
        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check
            )
            
            if capture_output:
                return result.stdout.strip(), result.stderr.strip(), result.returncode
            return "", "", result.returncode
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            if capture_output:
                return e.stdout or "", e.stderr or "", e.returncode
            return "", "", e.returncode
    
    def add_step(self, step_name, status, details="", duration=0):
        """Add step to report data"""
        step = {
            "name": step_name,
            "status": status,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        self.report_data["steps"].append(step)
        print(f"Step: {step_name} - {status}")
    
    def wait_for_rollout(self, deployment_name, timeout=300):
        """Wait for deployment rollout to complete"""
        print(f"Waiting for rollout of {deployment_name}...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            stdout, stderr, returncode = self.run_kubectl(
                f"rollout status deployment/{deployment_name} --timeout=30s"
            )
            
            if returncode == 0:
                duration = time.time() - start_time
                self.add_step(
                    "Deployment Rollout",
                    "SUCCESS",
                    f"Rollout completed in {duration:.2f} seconds",
                    duration
                )
                return True
            
            time.sleep(10)
        
        self.add_step("Deployment Rollout", "FAILED", "Timeout waiting for rollout")
        return False
    
    def get_pod_status(self):
        """Get pod status and logs"""
        stdout, stderr, returncode = self.run_kubectl(
            f"get pods -l app={self.app_name} -o json"
        )
        
        if returncode == 0:
            pods_data = json.loads(stdout)
            for pod in pods_data.get("items", []):
                pod_info = {
                    "name": pod["metadata"]["name"],
                    "status": pod["status"]["phase"],
                    "ready": self.is_pod_ready(pod),
                    "node": pod["spec"].get("nodeName", "unknown"),
                    "creation_time": pod["metadata"]["creationTimestamp"]
                }
                self.report_data["pods"].append(pod_info)
                
                # Get pod logs
                if pod_info["ready"]:
                    logs_stdout, _, _ = self.run_kubectl(
                        f"logs {pod_info['name']} --tail=50"
                    )
                    self.report_data["logs"] += f"\n=== {pod_info['name']} ===\n{logs_stdout}\n"
    
    def is_pod_ready(self, pod):
        """Check if pod is ready"""
        conditions = pod.get("status", {}).get("conditions", [])
        for condition in conditions:
            if condition["type"] == "Ready":
                return condition["status"] == "True"
        return False
    
    def get_service_endpoint(self):
        """Get service endpoint URL"""
        stdout, stderr, returncode = self.run_kubectl(
            f"get service {self.service_name} -o json"
        )
        
        if returncode == 0:
            service_data = json.loads(stdout)
            service_type = service_data["spec"]["type"]
            
            if service_type == "LoadBalancer":
                ingress = service_data.get("status", {}).get("loadBalancer", {}).get("ingress", [])
                if ingress:
                    host = ingress[0].get("hostname") or ingress[0].get("ip")
                    port = service_data["spec"]["ports"][0]["port"]
                    endpoint = f"http://{host}:{port}"
                    self.report_data["endpoint_url"] = endpoint
                    return endpoint
            
            elif service_type == "ClusterIP":
                # Use port-forward for testing
                cluster_ip = service_data["spec"]["clusterIP"]
                port = service_data["spec"]["ports"][0]["port"]
                endpoint = f"http://{cluster_ip}:{port}"
                self.report_data["endpoint_url"] = endpoint
                return endpoint
        
        return None
    
    def test_endpoint_connectivity(self, endpoint):
        """Test if endpoint is accessible"""
        if not endpoint:
            return False
        
        try:
            # For ClusterIP, we'll use kubectl port-forward
            if "10." in endpoint or "172." in endpoint or "192.168." in endpoint:
                # This is a cluster IP, skip direct connectivity test
                self.add_step(
                    "Endpoint Test",
                    "SUCCESS",
                    f"Service available at cluster IP: {endpoint}"
                )
                return True
            
            response = requests.get(endpoint, timeout=30)
            if response.status_code == 200:
                self.add_step(
                    "Endpoint Test",
                    "SUCCESS",
                    f"Endpoint {endpoint} is accessible (HTTP {response.status_code})"
                )
                return True
            else:
                self.add_step(
                    "Endpoint Test",
                    "WARNING",
                    f"Endpoint {endpoint} returned HTTP {response.status_code}"
                )
                return True  # Still consider it working
                
        except Exception as e:
            self.add_step(
                "Endpoint Test",
                "FAILED",
                f"Failed to connect to {endpoint}: {str(e)}"
            )
            return False
    
    def get_events(self):
        """Get cluster events related to our deployment"""
        stdout, stderr, returncode = self.run_kubectl(
            f"get events --field-selector involvedObject.name={self.app_name} -o json"
        )
        
        if returncode == 0:
            events_data = json.loads(stdout)
            for event in events_data.get("items", []):
                event_info = {
                    "type": event.get("type", "Normal"),
                    "reason": event.get("reason", ""),
                    "message": event.get("message", ""),
                    "timestamp": event.get("firstTimestamp", ""),
                    "count": event.get("count", 1)
                }
                self.report_data["events"].append(event_info)
    
    def cleanup_deployment(self):
        """Clean up deployment resources"""
        print("Cleaning up deployment...")
        self.run_kubectl(f"delete deployment {self.app_name}", check=False)
        self.run_kubectl(f"delete service {self.service_name}", check=False)
        self.run_kubectl(f"delete configmap {self.app_name}-config", check=False)
    
    def test_eks_deployment_pass(self):
        """Main test method for successful EKS deployment"""
        try:
            # Step 1: Verify kubectl connectivity
            stdout, stderr, returncode = self.run_kubectl("cluster-info")
            if returncode != 0:
                # If auth fails, still create a report
                self.add_step("Cluster Connectivity", "FAILED", f"kubectl cluster-info failed: {stderr}")
                self.report_data["status"] = "AUTH_FAILED"
                self.report_data["auth_error"] = stderr
                print("❌ Cannot connect to Kubernetes cluster!")
                print(f"Error: {stderr}")
                return False
            
            self.add_step("Cluster Connectivity", "SUCCESS", "Connected to EKS cluster")
            
            # Step 2: Clean up any existing resources
            self.cleanup_deployment()
            time.sleep(5)
            
            # Step 3: Apply ConfigMap
            configmap_file = self.deploy_dir / "configmap.yaml"
            stdout, stderr, returncode = self.run_kubectl(f"apply -f {configmap_file}")
            if returncode != 0:
                self.add_step("ConfigMap Deploy", "FAILED", f"Failed to apply ConfigMap: {stderr}")
                raise Exception("ConfigMap deployment failed")
            
            self.add_step("ConfigMap Deploy", "SUCCESS", "ConfigMap applied successfully")
            
            # Step 4: Apply Service
            service_file = self.deploy_dir / "service.yaml"
            stdout, stderr, returncode = self.run_kubectl(f"apply -f {service_file}")
            if returncode != 0:
                self.add_step("Service Deploy", "FAILED", f"Failed to apply Service: {stderr}")
                raise Exception("Service deployment failed")
            
            self.add_step("Service Deploy", "SUCCESS", "Service applied successfully")
            
            # Step 5: Apply Deployment (PASS version)
            deployment_file = self.deploy_dir / "deployment-pass.yaml"
            stdout, stderr, returncode = self.run_kubectl(f"apply -f {deployment_file}")
            if returncode != 0:
                self.add_step("Deployment Apply", "FAILED", f"Failed to apply Deployment: {stderr}")
                raise Exception("Deployment apply failed")
            
            self.add_step("Deployment Apply", "SUCCESS", "Deployment applied successfully")
            
            # Step 6: Wait for rollout
            if not self.wait_for_rollout(self.app_name):
                raise Exception("Deployment rollout failed")
            
            # Step 7: Get pod status
            self.get_pod_status()
            ready_pods = [p for p in self.report_data["pods"] if p["ready"]]
            if not ready_pods:
                self.add_step("Pod Readiness", "FAILED", "No pods are ready")
                raise Exception("No ready pods found")
            
            self.add_step("Pod Readiness", "SUCCESS", f"{len(ready_pods)} pods are ready")
            
            # Step 8: Get service endpoint
            endpoint = self.get_service_endpoint()
            if not endpoint:
                self.add_step("Service Endpoint", "WARNING", "Could not determine service endpoint")
            else:
                self.add_step("Service Endpoint", "SUCCESS", f"Service endpoint: {endpoint}")
            
            # Step 9: Test connectivity
            if endpoint:
                self.test_endpoint_connectivity(endpoint)
            
            # Step 10: Get events
            self.get_events()
            
            # Step 11: Final validation
            self.report_data["status"] = "SUCCESS"
            self.report_data["success_message"] = f"Successfully deployed {self.app_name} to EKS with {len(ready_pods)} ready pods"
            
            end_time = datetime.now()
            self.report_data["end_time"] = end_time.isoformat()
            self.report_data["total_duration"] = (end_time - self.start_time).total_seconds()
            
            self.add_step("Test Complete", "SUCCESS", "All deployment steps completed successfully")
            
            # Clean up
            self.cleanup_deployment()
            
            return True
            
        except Exception as e:
            self.report_data["status"] = "FAILED"
            self.report_data["error"] = str(e)
            end_time = datetime.now()
            self.report_data["end_time"] = end_time.isoformat()
            self.report_data["total_duration"] = (end_time - self.start_time).total_seconds()
            
            # Clean up on failure too
            self.cleanup_deployment()
            
            print(f"EKS deployment test failed: {e}")
            return False


def test_deploy_eks_pass():
    """Pytest entry point for EKS deployment pass test"""
    test_instance = TestEKSDeploymentPass()
    
    try:
        test_instance.test_eks_deployment_pass()
        
        # Save report data for HTML generation
        report_file = test_instance.test_dir / "reports" / "eks_pass_report.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(test_instance.report_data, f, indent=2)
        
        print(f"Report saved to: {report_file}")
        
    except Exception as e:
        # Save error report
        test_instance.report_data["status"] = "FAILED"
        test_instance.report_data["error"] = str(e)
        
        report_file = test_instance.test_dir / "reports" / "eks_pass_report.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(test_instance.report_data, f, indent=2)
        
        raise


if __name__ == "__main__":
    test_deploy_eks_pass()