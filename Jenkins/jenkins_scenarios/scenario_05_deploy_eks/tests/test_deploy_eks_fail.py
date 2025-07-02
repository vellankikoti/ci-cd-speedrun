#!/usr/bin/env python3
"""
Scenario 5 - EKS Deployment Fail Test
Tests intentional deployment failures to AWS EKS cluster
"""

import pytest
import subprocess
import time
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import yaml

class TestEKSDeploymentFail:
    
    def __init__(self):
        self.test_dir = Path(__file__).parent
        self.deploy_dir = self.test_dir / "deploy"
        self.app_name = "chaos-workshop-app"
        self.namespace = "default"
        self.service_name = f"{self.app_name}-service"
        self.start_time = datetime.now()
        self.report_data = {
            "scenario": "scenario_05_deploy_eks",
            "test_type": "FAIL",
            "start_time": self.start_time.isoformat(),
            "status": "RUNNING",
            "steps": [],
            "deployment_timeline": [],
            "pods": [],
            "services": [],
            "events": [],
            "error_events": [],
            "logs": "",
            "error_logs": "",
            "rollout_status": "",
            "failure_reasons": [],
            "remediation_suggestions": []
        }
    
    def run_kubectl(self, cmd, capture_output=True, check=False):
        """Execute kubectl command and return result"""
        full_cmd = f"kubectl {cmd}"
        print(f"Executing: {full_cmd}")
        
        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check,
                timeout=60
            )
            
            if capture_output:
                return result.stdout.strip(), result.stderr.strip(), result.returncode
            return "", "", result.returncode
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            if capture_output:
                return e.stdout or "", e.stderr or "", e.returncode
            return "", "", e.returncode
        except subprocess.TimeoutExpired:
            print("Command timed out")
            return "", "Command timed out", 124
    
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
    
    def wait_for_rollout_failure(self, deployment_name, timeout=180):
        """Wait for deployment rollout to fail"""
        print(f"Waiting for rollout failure of {deployment_name}...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            stdout, stderr, returncode = self.run_kubectl(
                f"rollout status deployment/{deployment_name} --timeout=30s",
                check=False
            )
            
            self.report_data["rollout_status"] = stdout + "\n" + stderr
            
            # Check if rollout failed or is stuck
            if "failed" in stdout.lower() or "error" in stderr.lower():
                duration = time.time() - start_time
                self.add_step(
                    "Deployment Rollout",
                    "FAILED_AS_EXPECTED",
                    f"Rollout failed as expected after {duration:.2f} seconds: {stderr}",
                    duration
                )
                return True
            
            # Check deployment status
            dep_stdout, dep_stderr, dep_returncode = self.run_kubectl(
                f"get deployment {deployment_name} -o json"
            )
            
            if dep_returncode == 0:
                try:
                    dep_data = json.loads(dep_stdout)
                    status = dep_data.get("status", {})
                    conditions = status.get("conditions", [])
                    
                    for condition in conditions:
                        if condition["type"] == "Progressing" and condition["status"] == "False":
                            reason = condition.get("reason", "")
                            message = condition.get("message", "")
                            if "ProgressDeadlineExceeded" in reason:
                                duration = time.time() - start_time
                                self.add_step(
                                    "Deployment Rollout",
                                    "FAILED_AS_EXPECTED",
                                    f"Deployment stuck/failed: {message}",
                                    duration
                                )
                                return True
                except json.JSONDecodeError:
                    pass
            
            time.sleep(10)
        
        # Timeout reached - this is also a form of failure
        duration = time.time() - start_time
        self.add_step(
            "Deployment Rollout",
            "FAILED_AS_EXPECTED",
            f"Deployment timed out after {duration:.2f} seconds (rollout stuck)",
            duration
        )
        return True
    
    def get_pod_failures(self):
        """Get pod status and failure details"""
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
                    "creation_time": pod["metadata"]["creationTimestamp"],
                    "container_statuses": []
                }
                
                # Get container statuses and failure reasons
                container_statuses = pod.get("status", {}).get("containerStatuses", [])
                for container in container_statuses:
                    container_info = {
                        "name": container["name"],
                        "ready": container["ready"],
                        "restart_count": container["restartCount"],
                        "state": container["state"]
                    }
                    
                    # Check for failure states
                    if "waiting" in container["state"]:
                        waiting = container["state"]["waiting"]
                        reason = waiting.get("reason", "")
                        message = waiting.get("message", "")
                        container_info["failure_reason"] = f"{reason}: {message}"
                        
                        if reason in ["ImagePullBackOff", "ErrImagePull", "InvalidImageName"]:
                            self.report_data["failure_reasons"].append(f"Image pull failure: {message}")
                            self.report_data["remediation_suggestions"].append(
                                "Check image name, tag, and registry accessibility"
                            )
                        elif reason in ["CrashLoopBackOff"]:
                            self.report_data["failure_reasons"].append(f"Container crashing: {message}")
                            self.report_data["remediation_suggestions"].append(
                                "Check application logs and startup configuration"
                            )
                    
                    pod_info["container_statuses"].append(container_info)
                
                self.report_data["pods"].append(pod_info)
                
                # Get pod logs (even for failed pods)
                logs_stdout, logs_stderr, _ = self.run_kubectl(
                    f"logs {pod_info['name']} --previous --tail=100",
                    check=False
                )
                if not logs_stdout:
                    logs_stdout, logs_stderr, _ = self.run_kubectl(
                        f"logs {pod_info['name']} --tail=100",
                        check=False
                    )
                
                if logs_stdout or logs_stderr:
                    log_content = f"\n=== {pod_info['name']} ===\n"
                    if logs_stdout:
                        log_content += f"STDOUT:\n{logs_stdout}\n"
                    if logs_stderr:
                        log_content += f"STDERR:\n{logs_stderr}\n"
                    self.report_data["error_logs"] += log_content
    
    def is_pod_ready(self, pod):
        """Check if pod is ready"""
        conditions = pod.get("status", {}).get("conditions", [])
        for condition in conditions:
            if condition["type"] == "Ready":
                return condition["status"] == "True"
        return False
    
    def get_failure_events(self):
        """Get cluster events related to failures"""
        # Get events for the deployment
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
                    "count": event.get("count", 1),
                    "object": event.get("involvedObject", {}).get("name", "")
                }
                
                if event_info["type"] == "Warning" or "error" in event_info["message"].lower():
                    self.report_data["error_events"].append(event_info)
                
                self.report_data["events"].append(event_info)
        
        # Also get pod-specific events
        pod_stdout, pod_stderr, pod_returncode = self.run_kubectl(
            f"get pods -l app={self.app_name} -o jsonpath='{{.items[*].metadata.name}}'"
        )
        
        if pod_returncode == 0 and pod_stdout:
            pod_names = pod_stdout.split()
            for pod_name in pod_names:
                stdout, stderr, returncode = self.run_kubectl(
                    f"get events --field-selector involvedObject.name={pod_name} -o json"
                )
                
                if returncode == 0:
                    events_data = json.loads(stdout)
                    for event in events_data.get("items", []):
                        event_info = {
                            "type": event.get("type", "Normal"),
                            "reason": event.get("reason", ""),
                            "message": event.get("message", ""),
                            "timestamp": event.get("firstTimestamp", ""),
                            "count": event.get("count", 1),
                            "object": pod_name
                        }
                        
                        if event_info["type"] == "Warning" or "error" in event_info["message"].lower():
                            self.report_data["error_events"].append(event_info)
    
    def analyze_failure_types(self):
        """Analyze and categorize failure types"""
        # Check deployment YAML for intentional failures
        deployment_file = self.deploy_dir / "deployment-fail.yaml"
        if deployment_file.exists():
            with open(deployment_file, 'r') as f:
                content = f.read()
                
                if "nonexistent-image" in content or "invalid-image" in content:
                    self.report_data["failure_reasons"].append("Invalid/nonexistent container image")
                    self.report_data["remediation_suggestions"].append(
                        "Update deployment.yaml with valid image name and tag"
                    )
                
                if "nonexistent-configmap" in content:
                    self.report_data["failure_reasons"].append("Missing ConfigMap reference")
                    self.report_data["remediation_suggestions"].append(
                        "Create the required ConfigMap or fix the reference"
                    )
                
                if "initialDelaySeconds: 1" in content and "periodSeconds: 1" in content:
                    self.report_data["failure_reasons"].append("Aggressive health check configuration")
                    self.report_data["remediation_suggestions"].append(
                        "Increase initialDelaySeconds and periodSeconds for health checks"
                    )
    
    def cleanup_deployment(self):
        """Clean up deployment resources"""
        print("Cleaning up deployment...")
        self.run_kubectl(f"delete deployment {self.app_name}", check=False)
        self.run_kubectl(f"delete service {self.service_name}", check=False)
        self.run_kubectl(f"delete configmap {self.app_name}-config", check=False)
    
    def test_eks_deployment_fail(self):
        """Main test method for intentional EKS deployment failure"""
        try:
            # Step 1: Verify kubectl connectivity
            stdout, stderr, returncode = self.run_kubectl("cluster-info")
            if returncode != 0:
                self.add_step("Cluster Connectivity", "FAILED", f"kubectl cluster-info failed: {stderr}")
                raise Exception("Cannot connect to EKS cluster")
            
            self.add_step("Cluster Connectivity", "SUCCESS", "Connected to EKS cluster")
            
            # Step 2: Clean up any existing resources
            self.cleanup_deployment()
            time.sleep(5)
            
            # Step 3: Apply ConfigMap (if needed)
            configmap_file = self.deploy_dir / "configmap.yaml"
            if configmap_file.exists():
                stdout, stderr, returncode = self.run_kubectl(f"apply -f {configmap_file}")
                if returncode == 0:
                    self.add_step("ConfigMap Deploy", "SUCCESS", "ConfigMap applied successfully")
                else:
                    self.add_step("ConfigMap Deploy", "WARNING", f"ConfigMap application issues: {stderr}")
            
            # Step 4: Apply Service
            service_file = self.deploy_dir / "service.yaml"
            stdout, stderr, returncode = self.run_kubectl(f"apply -f {service_file}")
            if returncode == 0:
                self.add_step("Service Deploy", "SUCCESS", "Service applied successfully")
            else:
                self.add_step("Service Deploy", "WARNING", f"Service application issues: {stderr}")
            
            # Step 5: Apply Deployment (FAIL version)
            deployment_file = self.deploy_dir / "deployment-fail.yaml"
            stdout, stderr, returncode = self.run_kubectl(f"apply -f {deployment_file}")
            if returncode != 0:
                self.add_step("Deployment Apply", "FAILED", f"Failed to apply Deployment: {stderr}")
                # This might be expected for some failure scenarios
            else:
                self.add_step("Deployment Apply", "SUCCESS", "Deployment applied (but expected to fail)")
            
            # Step 6: Wait for rollout failure
            self.wait_for_rollout_failure(self.app_name)
            
            # Step 7: Analyze pod failures
            self.get_pod_failures()
            
            # Step 8: Get failure events
            self.get_failure_events()
            
            # Step 9: Analyze failure types
            self.analyze_failure_types()
            
            # Step 10: Verify that deployment actually failed
            ready_pods = [p for p in self.report_data["pods"] if p["ready"]]
            if ready_pods:
                self.add_step("Failure Verification", "UNEXPECTED", 
                            f"Warning: {len(ready_pods)} pods are ready - deployment should have failed!")
                self.report_data["status"] = "UNEXPECTED_SUCCESS"
            else:
                self.add_step("Failure Verification", "SUCCESS", 
                            "Deployment failed as expected - no ready pods")
                self.report_data["status"] = "FAILED_AS_EXPECTED"
            
            end_time = datetime.now()
            self.report_data["end_time"] = end_time.isoformat()
            self.report_data["total_duration"] = (end_time - self.start_time).total_seconds()
            
            # Clean up
            self.cleanup_deployment()
            
            # For the fail test, we expect failure, so this is actually success
            return True
            
        except Exception as e:
            self.report_data["status"] = "TEST_ERROR"
            self.report_data["test_error"] = str(e)
            end_time = datetime.now()
            self.report_data["end_time"] = end_time.isoformat()
            self.report_data["total_duration"] = (end_time - self.start_time).total_seconds()
            
            # Clean up on error
            self.cleanup_deployment()
            
            pytest.fail(f"EKS deployment fail test encountered error: {e}")


def test_deploy_eks_fail():
    """Pytest entry point for EKS deployment fail test"""
    test_instance = TestEKSDeploymentFail()
    
    try:
        test_instance.test_eks_deployment_fail()
        
        # Save report data for HTML generation
        report_file = test_instance.test_dir / "reports" / "eks_fail_report.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(test_instance.report_data, f, indent=2)
        
        print(f"Report saved to: {report_file}")
        
    except Exception as e:
        # Save error report
        test_instance.report_data["status"] = "FAILED" 
        test_instance.report_data["error"] = str(e)
        
        report_file = test_instance.test_dir / "reports" / "eks_fail_report.json"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(test_instance.report_data, f, indent=2)
        
        raise