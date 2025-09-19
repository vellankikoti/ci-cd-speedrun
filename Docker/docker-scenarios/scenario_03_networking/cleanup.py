#!/usr/bin/env python3
"""
Docker Networking Cleanup Script - Python Version
================================================

Clean up all demo containers, networks, and images
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
    print("🧹 Docker Networking Cleanup")
    print("=" * 40)
    
    print_step("Stopping demo containers...")
    run_command("docker stop app-container db-container", "Stopping containers")
    
    print_step("Removing demo containers...")
    run_command("docker rm app-container db-container", "Removing containers")
    
    print_step("Removing demo network...")
    run_command("docker network rm demo-network", "Removing network")
    
    print_step("Removing demo images...")
    run_command("docker rmi demo-app", "Removing app image")
    
    print_step("Cleaning up orphaned resources...")
    run_command("docker container prune -f", "Removing orphaned containers")
    run_command("docker network prune -f", "Removing orphaned networks")
    
    print_success("Cleanup completed!")
    print_step("All demo containers, networks, and images removed")

if __name__ == "__main__":
    main()
