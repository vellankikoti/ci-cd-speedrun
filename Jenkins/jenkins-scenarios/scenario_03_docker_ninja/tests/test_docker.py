#!/usr/bin/env python3
"""
Docker Ninja - Docker Tests
Tests for Docker-specific functionality and security.
"""

import pytest
import subprocess
import os
import sys
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_docker_command(command):
    """Run a Docker command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_docker_image_build():
    """Test that Docker image builds successfully."""
    print("\n🐳 Testing Docker image build...")
    
    # Build the image
    success, stdout, stderr = run_docker_command("docker build --no-cache -t docker-ninja:test .")
    
    if not success:
        print(f"❌ Docker build failed: {stderr}")
        return False
    
    print("✅ Docker image built successfully!")
    return True

def test_docker_image_security():
    """Test Docker image security features."""
    print("\n🔒 Testing Docker image security...")
    
    # Check if image exists
    success, stdout, stderr = run_docker_command("docker images docker-ninja:test")
    if not success:
        print("❌ Image not found. Building first...")
        test_docker_image_build()
    
    # Test 1: Check if running as non-root user
    print("Testing non-root user...")
    success, stdout, stderr = run_docker_command("docker run --rm docker-ninja:test whoami")
    if success and "appuser" in stdout:
        print("✅ Running as non-root user (appuser)")
    else:
        print(f"❌ Not running as non-root user: {stdout}")
        return False
    
    # Test 2: Check exposed ports
    print("Testing exposed ports...")
    success, stdout, stderr = run_docker_command("docker inspect docker-ninja:test --format '{{.Config.ExposedPorts}}'")
    if success and "5000/tcp" in stdout:
        print("✅ Port 5000 exposed correctly")
    else:
        print(f"❌ Port 5000 not exposed: {stdout}")
        return False
    
    # Test 3: Check health check
    print("Testing health check...")
    success, stdout, stderr = run_docker_command("docker inspect docker-ninja:test --format '{{.Config.Healthcheck}}'")
    if success and "healthcheck" in stdout.lower():
        print("✅ Health check configured")
    else:
        print(f"❌ Health check not configured: {stdout}")
        return False
    
    return True

def test_docker_container_run():
    """Test that Docker container runs successfully."""
    print("\n🚀 Testing Docker container run...")
    
    # Start container in background
    success, stdout, stderr = run_docker_command("docker run -d --name docker-ninja-test -p 5000:5000 docker-ninja:test")
    if not success:
        print(f"❌ Failed to start container: {stderr}")
        return False
    
    print("✅ Container started successfully!")
    
    # Wait for container to be ready
    time.sleep(5)
    
    # Test health endpoint
    success, stdout, stderr = run_docker_command("curl -f http://localhost:5000/health")
    if success:
        print("✅ Health endpoint responding")
    else:
        print(f"❌ Health endpoint not responding: {stderr}")
        return False
    
    # Test metrics endpoint
    success, stdout, stderr = run_docker_command("curl -f http://localhost:5000/metrics")
    if success:
        print("✅ Metrics endpoint responding")
    else:
        print(f"❌ Metrics endpoint not responding: {stderr}")
        return False
    
    # Clean up
    run_docker_command("docker stop docker-ninja-test")
    run_docker_command("docker rm docker-ninja-test")
    
    return True

def test_docker_compose():
    """Test Docker Compose orchestration."""
    print("\n🐳 Testing Docker Compose...")
    
    # Start services
    success, stdout, stderr = run_docker_command("docker-compose up -d")
    if not success:
        print(f"❌ Docker Compose failed: {stderr}")
        return False
    
    print("✅ Docker Compose started successfully!")
    
    # Wait for services to be ready
    time.sleep(10)
    
    # Test load balancer
    success, stdout, stderr = run_docker_command("curl -f http://localhost:80/health")
    if success:
        print("✅ Load balancer responding")
    else:
        print(f"❌ Load balancer not responding: {stderr}")
        return False
    
    # Test blue-green deployment
    success, stdout, stderr = run_docker_command("curl -f http://localhost:5001/health")
    if success:
        print("✅ Blue deployment responding")
    else:
        print(f"❌ Blue deployment not responding: {stderr}")
        return False
    
    success, stdout, stderr = run_docker_command("curl -f http://localhost:5002/health")
    if success:
        print("✅ Green deployment responding")
    else:
        print(f"❌ Green deployment not responding: {stderr}")
        return False
    
    # Clean up
    run_docker_command("docker-compose down")
    
    return True

def test_docker_image_size():
    """Test Docker image size optimization."""
    print("\n📊 Testing Docker image size...")
    
    # Get image size
    success, stdout, stderr = run_docker_command("docker images docker-ninja:test --format '{{.Size}}'")
    if not success:
        print(f"❌ Could not get image size: {stderr}")
        return False
    
    size_str = stdout.strip()
    print(f"Image size: {size_str}")
    
    # Check if size is reasonable (less than 500MB)
    if "MB" in size_str:
        size_mb = int(size_str.replace("MB", ""))
        if size_mb < 500:
            print("✅ Image size is optimized (< 500MB)")
            return True
        else:
            print(f"⚠️  Image size is large: {size_mb}MB")
            return False
    elif "GB" in size_str:
        print(f"❌ Image size is too large: {size_str}")
        return False
    else:
        print(f"⚠️  Could not parse image size: {size_str}")
        return False

def test_docker_security_scan():
    """Test Docker security scanning."""
    print("\n🔒 Testing Docker security scan...")
    
    # Run security scan
    success, stdout, stderr = run_docker_command("python security-scan.py")
    if success:
        print("✅ Security scan completed successfully")
        return True
    else:
        print(f"❌ Security scan failed: {stderr}")
        return False

def main():
    """Run all Docker tests."""
    print("🐳 Docker Ninja - Docker Tests")
    print("=" * 50)
    
    tests = [
        ("Docker Image Build", test_docker_image_build),
        ("Docker Image Security", test_docker_image_security),
        ("Docker Container Run", test_docker_container_run),
        ("Docker Compose", test_docker_compose),
        ("Docker Image Size", test_docker_image_size),
        ("Docker Security Scan", test_docker_security_scan),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✅ {test_name} passed!")
                passed += 1
            else:
                print(f"❌ {test_name} failed!")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Docker tests passed!")
        return True
    else:
        print("❌ Some Docker tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
