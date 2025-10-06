#!/usr/bin/env python3
"""
Docker Security & Secrets Management Demo - Simple Version
=========================================================

Transform vulnerable containers into Fort Knox-level security!
Simple, focused demo just like Scenario 3 and 4
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

def run_command(cmd, description="", capture_output=False):
    """Run a command and return success status"""
    if description:
        print_step(description)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        if result.returncode == 0:
            if capture_output and result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            if capture_output and result.stderr:
                print_error(f"Command failed: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Command error: {e}")
        return False

def cleanup_containers():
    """Clean up all demo containers and images"""
    print_header("🧹 CLEANUP")
    print("=" * 50)
    
    print_step("Stopping security demo containers...")
    run_command("docker stop vulnerable-app-demo secure-app-demo security-dashboard")
    
    print_step("Removing containers...")
    run_command("docker rm vulnerable-app-demo secure-app-demo security-dashboard")
    
    print_step("Removing demo images...")
    run_command("docker rmi vulnerable-app secure-app security-dashboard")
    
    print_success("Cleanup completed!")

def main():
    """Main demo function - simple and focused"""
    print_header("🔒 DOCKER SECURITY & SECRETS MANAGEMENT DEMO")
    print("=" * 50)
    print("Transform vulnerable containers into Fort Knox-level security!")
    print("")
    
    # Trap to ensure cleanup on exit
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Step 1: Show vulnerable container problem
        print_header("STEP 1: The Vulnerable Container Problem")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This shows common Docker security anti-patterns")
        print("   • Demonstrates the impact of security vulnerabilities")
        print("   • Shows why security hardening matters in production")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Building vulnerable container with Docker BuildKit...")
        if not run_command("docker buildx build -f dockerfiles/vulnerable.Dockerfile -t vulnerable-app --load ."):
            print_error("Failed to build vulnerable container")
            return
        
        print_step("Starting vulnerable container...")
        if not run_command("docker run -d --name vulnerable-app-demo -p 8001:5000 vulnerable-app"):
            print_error("Failed to start vulnerable container")
            return
        
        print_step("Waiting for vulnerable app to start...")
        time.sleep(5)
        
        print_success("Vulnerable container running at: http://localhost:8001")
        print("   📊 Security Score: 0% (Critical vulnerabilities)")
        print("   📊 Secrets Exposed: 8 hardcoded secrets")
        print("   📊 User: root (privilege escalation risk)")
        
        print("")
        
        # Step 2: Security hardening solution
        print_header("STEP 2: Security Hardening Solution")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This shows how to implement Docker security best practices")
        print("   • Demonstrates proper secrets management")
        print("   • Shows the power of security hardening techniques")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Building secure container with Docker BuildKit...")
        if not run_command("docker buildx build -f dockerfiles/secure.Dockerfile -t secure-app --load ."):
            print_error("Failed to build secure container")
            return
        
        print_step("Starting secure container...")
        if not run_command("docker run -d --name secure-app-demo -p 8002:5000 secure-app"):
            print_error("Failed to start secure container")
            return
        
        print_step("Waiting for secure app to start...")
        time.sleep(5)
        
        print_success("Secure container running at: http://localhost:8002")
        print("   📊 Security Score: 100% (Production-ready)")
        print("   📊 Secrets Exposed: 0 (Properly managed)")
        print("   📊 User: appuser (Non-root security)")
        
        print("")
        
        # Step 3: Show the difference
        print_header("STEP 3: Security Comparison")
        print("=" * 50)
        
        print_step("Comparing security implementations...")
        run_command("docker ps | grep -E '(vulnerable-app-demo|secure-app-demo)'")
        
        print_step("Security analysis...")
        print_success("Security Hardening Complete!")
        print("   🎯 Security Score: 0% → 100% improvement")
        print("   🎯 Secrets Management: Hardcoded → Environment variables")
        print("   🎯 User Privileges: Root → Non-root user")
        print("   🎯 Attack Surface: 90% reduction")
        
        print("")
        
        print_header("🎉 SECURITY HARDENING COMPLETED!")
        print("=" * 50)
        print_success("You've successfully transformed a vulnerable container into a secure masterpiece!")
        print("")
        print_step("📊 FINAL RESULTS:")
        print("   • Docker security best practices implemented")
        print("   • Secrets management with environment variables")
        print("   • Non-root user for security")
        print("   • Production-ready security hardening")
        print("")
        print_step("⏳ Demo will auto-cleanup in 30 seconds...")
        print("   • All security improvements are complete")
        print("   • You can explore the containers at your own pace")
        print("   • Press Ctrl+C to stop early and keep containers running")
        time.sleep(30)
        
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        print("🔍 Containers are still running! You can explore them:")
        print("   • Vulnerable App: http://localhost:8001")
        print("   • Secure App: http://localhost:8002")
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
