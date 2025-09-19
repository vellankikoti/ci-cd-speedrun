#!/usr/bin/env python3
"""
Docker Chaos Pipeline Cleanup Script - Python Version
=====================================================

Clean up all chaos containers, images, and resources
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
    print("🧹 Docker Chaos Pipeline Cleanup")
    print("=" * 40)
    
    print_step("Stopping all demo containers...")
    for i in range(1, 6):
        container_name = f"chaos-step{i}"
        run_command(f"docker stop {container_name}", f"Stopping {container_name}")
        run_command(f"docker rm {container_name}", f"Removing {container_name}")
    
    print_step("Removing demo images...")
    for i in range(1, 6):
        image_name = f"chaos-step{i}"
        run_command(f"docker rmi {image_name}", f"Removing {image_name} image")
    
    print_step("Cleaning up orphaned containers...")
    run_command("docker container prune -f", "Removing orphaned containers")
    
    print_step("Cleaning up orphaned images...")
    run_command("docker image prune -f", "Removing orphaned images")
    
    print_success("Cleanup completed!")
    print_step("All chaos containers and images removed")

if __name__ == "__main__":
    main()
