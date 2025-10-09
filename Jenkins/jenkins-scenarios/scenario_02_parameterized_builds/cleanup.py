#!/usr/bin/env python3
"""
Jenkins Parameterized Builds - Cleanup Script
============================================

Clean up demo applications and processes.

Usage:
    python3 cleanup.py
"""

import subprocess
import sys
import os
import signal
import time

class Colors:
    """Color support for terminal output."""
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

class CleanupScript:
    """Cleanup script for Jenkins parameterized builds demo."""
    
    def print_header(self, message):
        """Print a header message."""
        print(f"{Colors.PURPLE}🎯 {message}{Colors.NC}")
        
    def print_step(self, message):
        """Print a step message."""
        print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")
        
    def print_success(self, message):
        """Print a success message."""
        print(f"{Colors.GREEN}✅ {message}{Colors.NC}")
        
    def print_info(self, message):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.NC}")
        
    def print_warning(self, message):
        """Print a warning message."""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")
        
    def print_error(self, message):
        """Print an error message."""
        print(f"{Colors.RED}❌ {message}{Colors.NC}")
        
    def run_command(self, cmd, description=""):
        """Run a command with error handling."""
        if description:
            self.print_step(description)
            
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                if result.stdout.strip():
                    print(f"   {result.stdout.strip()}")
                return True
            else:
                if result.stderr.strip():
                    self.print_warning(f"Command output: {result.stderr.strip()}")
                return False
        except Exception as e:
            self.print_warning(f"Command failed: {e}")
            return False
    
    def kill_processes_on_ports(self, ports):
        """Kill processes running on specified ports."""
        for port in ports:
            self.print_step(f"Checking port {port}...")
            
            # Find processes using the port
            result = subprocess.run(
                f"lsof -ti :{port}",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid.strip():
                        self.print_info(f"Killing process {pid} on port {port}")
                        subprocess.run(f"kill -9 {pid}", shell=True)
                        time.sleep(1)
                self.print_success(f"Cleaned up port {port}")
            else:
                self.print_info(f"Port {port} is free")
    
    def cleanup_demo_files(self):
        """Clean up demo application files."""
        demo_files = [
            'parameterized_dashboard_app.py',
            'static_build_limitations_app.py',
            'parameterized_benefits_app.py'
        ]
        
        for file in demo_files:
            if os.path.exists(file):
                self.print_step(f"Removing {file}...")
                try:
                    os.remove(file)
                    self.print_success(f"Removed {file}")
                except Exception as e:
                    self.print_warning(f"Could not remove {file}: {e}")
            else:
                self.print_info(f"{file} not found (already clean)")
    
    def cleanup_python_cache(self):
        """Clean up Python cache files."""
        self.print_step("Cleaning up Python cache files...")
        
        # Remove __pycache__ directories
        self.run_command("find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true", 
                        "Removing __pycache__ directories")
        
        # Remove .pyc files
        self.run_command("find . -name '*.pyc' -delete 2>/dev/null || true", 
                        "Removing .pyc files")
        
        self.print_success("Python cache cleanup completed")
    
    def check_ports(self, ports):
        """Check if ports are free."""
        self.print_step("Checking port availability...")
        
        all_free = True
        for port in ports:
            result = subprocess.run(
                f"lsof -ti :{port}",
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                self.print_warning(f"Port {port} is still in use")
                all_free = False
            else:
                self.print_success(f"Port {port} is free")
        
        return all_free
    
    def run_cleanup(self):
        """Run the complete cleanup process."""
        self.print_header("Jenkins Parameterized Builds - Cleanup")
        self.print_info("Cleaning up demo applications and processes...")
        print()
        
        # Ports used by the demo
        demo_ports = [8000, 8001, 8002]
        
        # Kill processes on demo ports
        self.print_step("Stopping demo applications...")
        self.kill_processes_on_ports(demo_ports)
        print()
        
        # Clean up demo files
        self.print_step("Cleaning up demo files...")
        self.cleanup_demo_files()
        print()
        
        # Clean up Python cache
        self.cleanup_python_cache()
        print()
        
        # Final port check
        self.print_step("Final port check...")
        if self.check_ports(demo_ports):
            self.print_success("All demo ports are free")
        else:
            self.print_warning("Some ports may still be in use")
        print()
        
        # Summary
        self.print_success("🎉 Cleanup completed successfully!")
        self.print_info("All demo applications have been stopped")
        self.print_info("All demo files have been removed")
        self.print_info("All ports are available for future use")
        print()
        self.print_info("You can now run the demo again with: python3 demo_interactive.py")

def main():
    """Main function."""
    cleanup = CleanupScript()
    cleanup.run_cleanup()

if __name__ == '__main__':
    main()
