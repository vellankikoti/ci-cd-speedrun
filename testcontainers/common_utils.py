#!/usr/bin/env python3
"""
Common utilities for TestContainers workshop
Provides universal functions for port management, Docker checks, and error handling
"""

import os
import sys
import socket
import subprocess
from pathlib import Path

def find_free_port(start_port=5000, max_attempts=100):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find a free port starting from {start_port}")

def check_docker_universal():
    """Universal Docker check that works across all platforms and environments"""
    try:
        # Check if docker command exists
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        
        # Check if Docker daemon is running
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        
        # If docker ps fails, try docker info as fallback
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        return result.returncode == 0
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def setup_testcontainers_environment():
    """Setup TestContainers environment variables for universal compatibility"""
    # Configure TestContainers to use local Docker
    os.environ["TESTCONTAINERS_CLOUD_ENABLED"] = "false"
    
    # Platform-specific Docker host configuration
    if sys.platform == "win32":
        os.environ["DOCKER_HOST"] = "tcp://localhost:2375"
    else:
        # Try different Docker socket paths
        docker_sockets = [
            "unix:///var/run/docker.sock",
            "unix:///var/run/docker.sock.raw",
            "npipe:////./pipe/docker_engine"  # Windows named pipe
        ]
        
        for socket_path in docker_sockets:
            os.environ["DOCKER_HOST"] = socket_path
            if check_docker_universal():
                break

def check_dependencies_universal(required_packages):
    """Universal dependency check"""
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def safe_database_operation(conn, operation, *args, **kwargs):
    """Safely execute database operations with proper error handling"""
    try:
        return operation(conn, *args, **kwargs)
    except Exception as e:
        try:
            conn.rollback()
        except:
            pass
        raise e
