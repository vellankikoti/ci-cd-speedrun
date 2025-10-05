#!/usr/bin/env python3
"""
Docker Security & Secrets Management Cleanup Script
=================================================

Clean up all demo containers, images, and security resources
"""

import subprocess
import sys

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

def print_step(message):
    print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

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
            # Don't print error for expected failures (e.g., container not found)
            return False
    except Exception as e:
        print_error(f"Command error: {e}")
        return False

def main():
    """Main cleanup function"""
    print("🧹 Docker Security & Secrets Management Cleanup")
    print("=" * 50)
    
    print_step("Stopping security demo containers...")
    run_command("docker stop vulnerable-app-demo secure-app-demo security-dashboard", "Stopping containers")
    
    print_step("Removing demo containers...")
    run_command("docker rm vulnerable-app-demo secure-app-demo security-dashboard", "Removing containers")
    
    print_step("Removing demo images...")
    run_command("docker rmi vulnerable-app secure-app security-dashboard", "Removing images")
    
    print_step("Cleaning up build cache...")
    run_command("docker builder prune -f", "Removing build cache")
    
    print_step("Cleaning up orphaned resources...")
    run_command("docker container prune -f", "Removing orphaned containers")
    run_command("docker image prune -f", "Removing orphaned images")
    run_command("docker volume prune -f", "Removing orphaned volumes")
    
    print_success("Cleanup completed!")
    print_step("All security demo containers, images, and cache removed")

if __name__ == "__main__":
    main()
