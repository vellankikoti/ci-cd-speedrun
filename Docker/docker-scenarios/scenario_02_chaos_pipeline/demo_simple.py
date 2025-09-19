#!/usr/bin/env python3
"""
Docker Chaos Pipeline Demo - Python Version
===========================================

Progressive chaos engineering with 5 failure scenarios
"""

import subprocess
import time
import os
import sys

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

def print_step(message):
    print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def print_header(message):
    print(f"{Colors.PURPLE}🎯 {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def run_command(cmd, description=""):
    """Run a command and return success status"""
    if description:
        print_step(description)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print_error(f"Command failed: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Command error: {e}")
        return False

def cleanup_containers():
    """Clean up all chaos containers and images"""
    print_header("🧹 CLEANUP")
    print("=" * 50)
    
    print_step("Stopping all chaos containers...")
    for i in range(1, 6):
        run_command(f"docker stop chaos-step{i}", f"Stopping chaos-step{i}")
        run_command(f"docker rm chaos-step{i}", f"Removing chaos-step{i}")
    
    print_step("Removing chaos images...")
    for i in range(1, 6):
        run_command(f"docker rmi chaos-step{i}", f"Removing chaos-step{i} image")
    
    print_success("Cleanup completed!")

def run_step(step, port, step_name, step_dir):
    """Run a specific chaos step with educational delays"""
    print_header(f"STEP {step}: {step_name}")
    print("=" * 50)
    
    # Educational pause - explain what we're about to demonstrate
    print_step("🎓 Educational Context:")
    if step == 1:
        print("   • This simulates network connectivity issues")
        print("   • Shows how containers handle external service failures")
        print("   • Demonstrates DNS resolution and HTTP connectivity tests")
    elif step == 2:
        print("   • This simulates resource exhaustion (memory/CPU)")
        print("   • Shows Docker's OOM (Out of Memory) killer in action")
        print("   • Demonstrates resource monitoring and limits")
    elif step == 3:
        print("   • This simulates service dependency failures")
        print("   • Shows how microservices handle Redis unavailability")
        print("   • Demonstrates fallback mechanisms and graceful degradation")
    elif step == 4:
        print("   • This simulates database connectivity failures")
        print("   • Shows how applications handle MySQL unavailability")
        print("   • Demonstrates data persistence and fallback strategies")
    elif step == 5:
        print("   • This shows a production-ready, resilient system")
        print("   • Demonstrates all services working together")
        print("   • Shows comprehensive monitoring and health checks")
    
    print_step("⏳ Pausing for audience to understand the scenario...")
    time.sleep(3)  # Educational pause
    
    # Clean up existing container
    container_name = f"chaos-step{step}"
    print_step("Cleaning up existing container...")
    run_command(f"docker stop {container_name}")
    run_command(f"docker rm {container_name}")
    
    # Build and run container
    print_step(f"Building Docker image for step {step}...")
    if not run_command(f"docker build -t {container_name} .", f"Building {container_name}"):
        return False
    
    print_step(f"Starting container on port {port}...")
    # Step 5 uses port 5000, others use 8080
    internal_port = 5000 if step == 5 else 8080
    if not run_command(f"docker run -d --name {container_name} -p {port}:{internal_port} {container_name}"):
        return False
    
    # Wait for container to be ready with educational context
    if step == 5:
        print_step("⏳ Waiting for container to start (step 5 takes longer due to service initialization)...")
        print("   • This simulates a production environment with multiple services")
        print("   • Shows how real applications need time to initialize")
        time.sleep(15)  # Longer delay for step 5
    else:
        print_step("⏳ Waiting for container to start...")
        print("   • Container needs time to initialize and start services")
        time.sleep(5)  # Increased from 3 to 5 seconds for better demonstration
    
    # Test the endpoint with educational context
    print_step("🧪 Testing endpoint and demonstrating functionality...")
    if run_command(f"curl -s http://localhost:{port} > /dev/null", f"Testing port {port}"):
        print_success(f"✅ Container is responding on port {port}")
        print_step(f"🌐 Visit: http://localhost:{port}")
        
        # Educational pause to let audience see the working service
        print_step("⏳ Pausing to let you explore the service...")
        print("   • Try visiting the URL in your browser")
        print("   • Check out the /health, /debug, and /run-experiment endpoints")
        time.sleep(5)  # Educational pause for exploration
        
        return True
    else:
        print_error(f"❌ Container failed to respond on port {port}")
        print_step("📋 Container logs:")
        run_command(f"docker logs {container_name}")
        return False

def main():
    """Main demo function with educational flow"""
    print_header("🚀 DOCKER CHAOS PIPELINE DEMO")
    print("=" * 50)
    print("Progressive chaos engineering with 5 failure scenarios")
    print("")
    
    # Educational introduction
    print_step("🎓 DEMO OVERVIEW:")
    print("   • Step 1: Network Failure - External connectivity issues")
    print("   • Step 2: Resource Failure - Memory/CPU exhaustion")
    print("   • Step 3: Service Failure - Redis dependency failure")
    print("   • Step 4: Database Failure - MySQL connectivity failure")
    print("   • Step 5: Success Scenario - Production-ready system")
    print("")
    print_step("⏳ Starting demo in 5 seconds...")
    time.sleep(5)
    
    # Trap to ensure cleanup on exit
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Run all steps
        steps = [
            (1, 8001, "Network Failure", "scenarios/step1_fail_network"),
            (2, 8002, "Resource Failure", "scenarios/step2_fail_resource"),
            (3, 8003, "Service Failure", "scenarios/step3_fail_service"),
            (4, 8004, "Database Failure", "scenarios/step4_fail_db"),
            (5, 8005, "Success Scenario", "scenarios/step5_success")
        ]
        
        for i, (step, port, step_name, step_dir) in enumerate(steps):
            # Change to step directory
            original_dir = os.getcwd()
            os.chdir(step_dir)
            
            try:
                success = run_step(step, port, step_name, step_dir)
                if not success:
                    print_error(f"Step {step} failed, stopping...")
                    break
            finally:
                os.chdir(original_dir)
            
            # Add delay between steps (except after the last step)
            if i < len(steps) - 1:
                print("")
                print_step("⏳ Transitioning to next scenario...")
                print("   • This pause allows you to observe the current scenario")
                print("   • You can visit the URL to explore the service")
                print("   • Next scenario will start in 3 seconds...")
                time.sleep(3)
                print("")
        
        print_header("🎉 DEMO COMPLETED")
        print("=" * 50)
        print_success("All chaos scenarios demonstrated!")
        print("")
        print_step("📊 SUMMARY OF WHAT WE LEARNED:")
        print("   • Step 1: How containers handle network failures")
        print("   • Step 2: Docker resource limits and OOM killer")
        print("   • Step 3: Microservice dependency management")
        print("   • Step 4: Database connectivity and fallback strategies")
        print("   • Step 5: Production-ready resilient architecture")
        print("")
        print_step("🔍 Active containers:")
        run_command("docker ps --format 'table {{.Names}}\\t{{.Ports}}\\t{{.Status}}'")
        print("")
        print_step("🌐 Test endpoints (all still running):")
        for step, port, step_name, _ in steps:
            print(f"   Step {step} ({step_name}): http://localhost:{port}")
        print("")
        print_step("🧹 Run 'python3 cleanup.py' to clean up all containers")
        print("")
        print_step("⏳ Demo will auto-cleanup in 30 seconds...")
        print("   • All services are still running and available")
        print("   • You can explore them at your own pace")
        print("   • Press Ctrl+C to stop early and keep containers running")
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        print("🔍 Containers are still running! You can explore them:")
        for step, port, step_name, _ in steps:
            print(f"   Step {step} ({step_name}): http://localhost:{port}")
        print("")
        print("🧹 To clean up later, run: python3 cleanup.py")
        print("⏳ Or wait 30 seconds for auto-cleanup...")
        time.sleep(30)
        cleanup_containers()
    except Exception as e:
        print_error(f"Demo failed: {e}")
        cleanup_containers()
    else:
        # Only cleanup if demo completed successfully
        cleanup_containers()

if __name__ == "__main__":
    main()
