#!/usr/bin/env python3
"""
🎓 Jenkins Workshop Demo Script
Complete demonstration script for workshop presenters
"""

import time
import subprocess
import requests
from pathlib import Path

def print_step(step, description):
    print(f"\n🎯 {step}: {description}")
    print("-" * 60)

def print_success(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️ {message}")

def run_command(cmd, description):
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print_success(f"{description} - Success")
            return True
        else:
            print_warning(f"{description} - Failed: {result.stderr}")
            return False
    except Exception as e:
        print_warning(f"{description} - Error: {e}")
        return False

def demo_workshop():
    print("🎓 Jenkins CI/CD Workshop Demo")
    print("=" * 60)
    
    # Demo 1: Show setup
    print_step("Demo 1", "Show Jenkins Setup (One Command!)")
    print("This demonstrates how easy it is to set up Jenkins:")
    print("python3 setup-jenkins-complete.py setup")
    
    input("Press Enter to continue...")
    
    # Demo 2: Show Jenkins is running
    print_step("Demo 2", "Verify Jenkins is Running")
    try:
        response = requests.get("http://localhost:8080/api/json", timeout=5)
        if response.status_code == 200:
            print_success("Jenkins is running and accessible")
        else:
            print_warning("Jenkins is not accessible")
    except:
        print_warning("Jenkins is not running")
    
    # Demo 3: Show test results
    print_step("Demo 3", "Run Complete Test Suite")
    run_command("python3 test-jenkins-pipeline.py", "Test Jenkins setup")
    
    # Demo 4: Show application
    print_step("Demo 4", "Show Application Structure")
    print("Application files:")
    run_command("ls -la scenarios/01-docker-build/", "List application files")
    
    print("\nJenkinsfile content:")
    run_command("head -20 scenarios/01-docker-build/Jenkinsfile", "Show Jenkinsfile")
    
    # Demo 5: Show Docker build
    print_step("Demo 5", "Show Docker Build")
    run_command("cd scenarios/01-docker-build && docker build -t demo-app .", "Build Docker image")
    
    # Demo 6: Show running application
    print_step("Demo 6", "Show Running Application")
    run_command("docker run -d --name demo-app -p 5001:5000 demo-app", "Start application")
    
    print("Waiting for application to start...")
    time.sleep(3)
    
    run_command("curl -s http://localhost:5001/health", "Test application health")
    
    # Cleanup
    print_step("Cleanup", "Clean up demo resources")
    run_command("docker stop demo-app && docker rm demo-app && docker rmi demo-app", "Clean up containers")
    
    print("\n🎉 Demo Complete!")
    print("\nNext steps for attendees:")
    print("1. Open http://localhost:8080")
    print("2. Click on '🎓 Workshop - Docker Build Pipeline'")
    print("3. Click 'Build Now'")
    print("4. Watch the magic happen!")

if __name__ == "__main__":
    demo_workshop()
