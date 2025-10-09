#!/usr/bin/env python3
"""
Jenkins Powerhouse - Cleanup Script
Comprehensive cleanup for all resources and containers
"""

import os
import sys
import subprocess
import time
import signal
from datetime import datetime

class JenkinsPowerhouseCleanup:
    """Cleanup utility for Jenkins Powerhouse scenario"""
    
    def __init__(self):
        self.containers_to_clean = [
            'development-powerhouse',
            'staging-powerhouse', 
            'production-powerhouse',
            'jenkins-powerhouse-dev',
            'jenkins-powerhouse-staging',
            'jenkins-powerhouse-prod'
        ]
        
        self.images_to_clean = [
            'jenkins-powerhouse-development',
            'jenkins-powerhouse-staging',
            'jenkins-powerhouse-production'
        ]
        
        self.files_to_clean = [
            'webapp.port',
            'docker.image',
            'docker.container',
            'webapp.log',
            'webapp.pid'
        ]
    
    def print_header(self):
        """Print cleanup header"""
        print("=" * 60)
        print("🧹 Jenkins Powerhouse - Cleanup Script")
        print("=" * 60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
    
    def run_command(self, command, description):
        """Run a command and handle errors"""
        print(f"🔧 {description}...", end="")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(" ✅")
                return True
            else:
                print(f" ❌ (Error: {result.stderr.strip()})")
                return False
        except Exception as e:
            print(f" ❌ (Exception: {str(e)})")
            return False
    
    def cleanup_containers(self):
        """Clean up Docker containers"""
        print("🐳 Cleaning up Docker containers...")
        print("-" * 35)
        
        # Stop all containers
        for container in self.containers_to_clean:
            self.run_command(f"docker stop {container}", f"Stopping {container}")
        
        # Remove all containers
        for container in self.containers_to_clean:
            self.run_command(f"docker rm {container}", f"Removing {container}")
        
        # Clean up any remaining containers with similar names
        self.run_command(
            "docker ps -a --filter 'name=.*-powerhouse' --format '{{.Names}}' | xargs -r docker stop",
            "Stopping remaining powerhouse containers"
        )
        
        self.run_command(
            "docker ps -a --filter 'name=.*-powerhouse' --format '{{.Names}}' | xargs -r docker rm",
            "Removing remaining powerhouse containers"
        )
        
        print()
    
    def cleanup_images(self):
        """Clean up Docker images"""
        print("🖼️  Cleaning up Docker images...")
        print("-" * 32)
        
        # Remove specific images
        for image in self.images_to_clean:
            self.run_command(f"docker rmi {image}", f"Removing {image}")
        
        # Clean up dangling images
        self.run_command("docker image prune -f", "Removing dangling images")
        
        # Clean up unused images
        self.run_command("docker image prune -a -f", "Removing unused images")
        
        print()
    
    def cleanup_files(self):
        """Clean up generated files"""
        print("📁 Cleaning up generated files...")
        print("-" * 32)
        
        for file in self.files_to_clean:
            if os.path.exists(file):
                self.run_command(f"rm -f {file}", f"Removing {file}")
            else:
                print(f"🔧 {file}... (not found) ✅")
        
        # Clean up webapp directory
        if os.path.exists('webapp'):
            self.run_command("rm -rf webapp", "Removing webapp directory")
        
        # Clean up any Dockerfiles
        if os.path.exists('Dockerfile'):
            self.run_command("rm -f Dockerfile", "Removing Dockerfile")
        
        print()
    
    def cleanup_ports(self):
        """Clean up port usage"""
        print("🔌 Cleaning up port usage...")
        print("-" * 30)
        
        # Find processes using ports 8081-8090
        for port in range(8081, 8091):
            self.run_command(
                f"lsof -ti:{port} | xargs -r kill -9",
                f"Killing processes on port {port}"
            )
        
        print()
    
    def cleanup_volumes(self):
        """Clean up Docker volumes"""
        print("💾 Cleaning up Docker volumes...")
        print("-" * 32)
        
        # Remove unused volumes
        self.run_command("docker volume prune -f", "Removing unused volumes")
        
        print()
    
    def cleanup_networks(self):
        """Clean up Docker networks"""
        print("🌐 Cleaning up Docker networks...")
        print("-" * 32)
        
        # Remove unused networks
        self.run_command("docker network prune -f", "Removing unused networks")
        
        print()
    
    def show_cleanup_summary(self):
        """Show cleanup summary"""
        print("📊 Cleanup Summary")
        print("-" * 18)
        
        # Check remaining containers
        result = subprocess.run("docker ps -a --filter 'name=.*-powerhouse' --format '{{.Names}}'", 
                              shell=True, capture_output=True, text=True)
        remaining_containers = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        if remaining_containers and remaining_containers[0]:
            print(f"⚠️  Remaining containers: {len(remaining_containers)}")
            for container in remaining_containers:
                print(f"   • {container}")
        else:
            print("✅ No remaining containers")
        
        # Check remaining images
        result = subprocess.run("docker images --filter 'reference=jenkins-powerhouse*' --format '{{.Repository}}'", 
                              shell=True, capture_output=True, text=True)
        remaining_images = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        if remaining_images and remaining_images[0]:
            print(f"⚠️  Remaining images: {len(remaining_images)}")
            for image in remaining_images:
                print(f"   • {image}")
        else:
            print("✅ No remaining images")
        
        # Check remaining files
        remaining_files = []
        for file in self.files_to_clean:
            if os.path.exists(file):
                remaining_files.append(file)
        
        if remaining_files:
            print(f"⚠️  Remaining files: {len(remaining_files)}")
            for file in remaining_files:
                print(f"   • {file}")
        else:
            print("✅ No remaining files")
        
        print()
    
    def run_full_cleanup(self):
        """Run full cleanup"""
        self.print_header()
        
        print("🧹 Starting comprehensive cleanup...")
        print()
        
        self.cleanup_containers()
        self.cleanup_images()
        self.cleanup_files()
        self.cleanup_ports()
        self.cleanup_volumes()
        self.cleanup_networks()
        
        print("✅ Cleanup completed!")
        print()
        
        self.show_cleanup_summary()
    
    def run_quick_cleanup(self):
        """Run quick cleanup (containers and files only)"""
        self.print_header()
        
        print("🧹 Starting quick cleanup...")
        print()
        
        self.cleanup_containers()
        self.cleanup_files()
        
        print("✅ Quick cleanup completed!")
        print()
        
        self.show_cleanup_summary()
    
    def run_interactive_cleanup(self):
        """Run interactive cleanup"""
        self.print_header()
        
        print("🧹 Interactive Cleanup")
        print("-" * 20)
        print("1. 🐳 Clean containers only")
        print("2. 🖼️  Clean images only")
        print("3. 📁 Clean files only")
        print("4. 🔌 Clean ports only")
        print("5. 🧹 Full cleanup")
        print("6. ❌ Exit")
        print()
        
        while True:
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.cleanup_containers()
                self.show_cleanup_summary()
            elif choice == '2':
                self.cleanup_images()
                self.show_cleanup_summary()
            elif choice == '3':
                self.cleanup_files()
                self.show_cleanup_summary()
            elif choice == '4':
                self.cleanup_ports()
                self.show_cleanup_summary()
            elif choice == '5':
                self.run_full_cleanup()
                break
            elif choice == '6':
                print("👋 Cleanup cancelled!")
                break
            else:
                print("❌ Invalid option. Please select 1-6.")
                print()
            
            input("\nPress Enter to continue...")
            print()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Jenkins Powerhouse Cleanup')
    parser.add_argument('--quick', action='store_true', help='Run quick cleanup only')
    parser.add_argument('--full', action='store_true', help='Run full cleanup only')
    parser.add_argument('--interactive', action='store_true', help='Run interactive cleanup')
    
    args = parser.parse_args()
    
    cleanup = JenkinsPowerhouseCleanup()
    
    if args.quick:
        cleanup.run_quick_cleanup()
    elif args.full:
        cleanup.run_full_cleanup()
    elif args.interactive:
        cleanup.run_interactive_cleanup()
    else:
        cleanup.run_interactive_cleanup()

if __name__ == '__main__':
    main()
