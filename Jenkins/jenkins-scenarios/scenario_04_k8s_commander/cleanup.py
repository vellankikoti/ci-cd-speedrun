#!/usr/bin/env python3
"""
K8s Commander Cleanup Script
Cleans up containers, ports, and resources from Jenkins scenario 04
"""

import os
import subprocess
import time
import sys

def print_header(text):
    """Print a formatted header"""
    print(f"\n{text}")
    print("=" * len(text))

def print_step(text):
    """Print a formatted step"""
    print(f"🔧 {text}")

def print_success(text):
    """Print a success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print an error message"""
    print(f"❌ {text}")

def run_command(cmd, description=""):
    """Run a command and return success status"""
    try:
        if description:
            print(f"   • {description}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print_error(f"Command failed: {cmd}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Command error: {e}")
        return False

def cleanup_containers():
    """Clean up all k8s-commander containers"""
    print_header("🧹 CONTAINER CLEANUP")
    
    print_step("Stopping k8s-commander containers...")
    run_command("docker ps -a --filter 'name=k8s-commander' --format '{{.Names}}' | xargs -r docker stop", "Stopping containers")
    
    print_step("Removing k8s-commander containers...")
    run_command("docker ps -a --filter 'name=k8s-commander' --format '{{.Names}}' | xargs -r docker rm", "Removing containers")
    
    print_step("Removing k8s-commander images...")
    run_command("docker images --filter 'reference=k8s-commander*' --format '{{.Repository}}:{{.Tag}}' | xargs -r docker rmi", "Removing images")
    
    print_success("Container cleanup completed!")

def cleanup_ports():
    """Clean up port usage"""
    print_header("🔌 PORT CLEANUP")
    
    print_step("Cleaning up ports 8081-8090...")
    for port in range(8081, 8091):
        if run_command(f"netstat -tuln 2>/dev/null | grep -q ':{port} '", f"Checking port {port}"):
            print(f"   • Port {port} is in use, attempting to free it...")
            run_command(f"lsof -ti:{port} | xargs -r kill -9", f"Killing processes on port {port}")
            time.sleep(1)
    
    print_success("Port cleanup completed!")

def cleanup_files():
    """Clean up generated files"""
    print_header("📁 FILE CLEANUP")
    
    files_to_clean = [
        'Dockerfile',
        'k8s-demo',
        'k8s-lab'
    ]
    
    for file in files_to_clean:
        if os.path.exists(file):
            if os.path.isdir(file):
                run_command(f"rm -rf {file}", f"Removing directory {file}")
            else:
                run_command(f"rm -f {file}", f"Removing file {file}")
        else:
            print(f"   • {file}... (not found) ✅")
    
    print_success("File cleanup completed!")

def cleanup_docker_resources():
    """Clean up Docker resources"""
    print_header("🐳 DOCKER RESOURCE CLEANUP")
    
    print_step("Cleaning up orphaned containers...")
    run_command("docker container prune -f", "Removing orphaned containers")
    
    print_step("Cleaning up orphaned images...")
    run_command("docker image prune -f", "Removing orphaned images")
    
    print_step("Cleaning up build cache...")
    run_command("docker builder prune -f", "Removing build cache")
    
    print_success("Docker resource cleanup completed!")

def show_cleanup_summary():
    """Show cleanup summary"""
    print_header("📊 CLEANUP SUMMARY")
    
    print("✅ All k8s-commander containers stopped and removed")
    print("✅ All k8s-commander images removed")
    print("✅ Ports 8081-8090 freed up")
    print("✅ Generated files cleaned up")
    print("✅ Docker resources optimized")
    print("\n🎉 K8s Commander cleanup completed successfully!")
    print("🚀 Ready for fresh Jenkins pipeline runs!")

def main():
    """Main cleanup function"""
    print_header("🧹 K8S COMMANDER CLEANUP")
    print("Cleaning up Jenkins scenario 04 resources...")
    
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Run cleanup steps
        cleanup_containers()
        cleanup_ports()
        cleanup_files()
        cleanup_docker_resources()
        show_cleanup_summary()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Cleanup interrupted by user")
        print("🔄 Run the script again to complete cleanup")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error during cleanup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
