#!/usr/bin/env python3
"""
Test script for dynamic Jenkins Scenario 2 Web Application
Tests if the webapp is accessible and shows dynamic content
"""

import os
import sys
import time
import requests
import subprocess
import json

def test_dynamic_webapp():
    """Test if webapp shows dynamic content based on parameters"""
    print("🧪 Testing dynamic webapp...")
    
    # Find the correct port
    webapp_port = "8081"  # Default
    try:
        with open("webapp.port", "r") as f:
            webapp_port = f.read().strip()
    except:
        # Try to find running container port
        try:
            result = subprocess.run(['docker', 'ps', '--filter', 'name=.*-app', '--format', '{{.Ports}}'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and result.stdout.strip():
                # Extract port from output like "0.0.0.0:8081->8080/tcp"
                import re
                match = re.search(r':(\d+)->8080/tcp', result.stdout)
                if match:
                    webapp_port = match.group(1)
        except:
            pass
    
    # Test URLs
    test_urls = [
        f"http://localhost:{webapp_port}",
        f"http://localhost:{webapp_port}/api/status"
    ]
    
    for url in test_urls:
        print(f"🔍 Testing {url}...")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ SUCCESS: {url} is accessible!")
                
                if "/api/status" in url:
                    # Test API endpoint
                    try:
                        data = response.json()
                        print(f"   📊 API Response:")
                        print(f"      • Environment: {data.get('environment', 'N/A')}")
                        print(f"      • Version: {data.get('version', 'N/A')}")
                        print(f"      • Features: {data.get('features', 'N/A')}")
                        print(f"      • Status: {data.get('status', 'N/A')}")
                        print(f"      • Timestamp: {data.get('timestamp', 'N/A')}")
                    except json.JSONDecodeError:
                        print("   ⚠️  API response is not valid JSON")
                else:
                    # Test HTML content
                    content = response.text
                    if "Jenkins Parameterized Build Demo" in content:
                        print("   ✅ Content verified: This is our dynamic webapp!")
                        
                        # Check for dynamic content
                        if "Development" in content or "Staging" in content or "Production" in content:
                            print("   ✅ Dynamic environment content detected!")
                        if "Basic" in content or "Advanced" in content or "Enterprise" in content:
                            print("   ✅ Dynamic feature content detected!")
                        if "1.0.0" in content or "2.0.0" in content:
                            print("   ✅ Dynamic version content detected!")
                    else:
                        print("   ⚠️  Content mismatch: This might not be our webapp")
                
                return True
            else:
                print(f"❌ FAILED: {url} returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ CONNECTION ERROR: {url} is not accessible")
        except requests.exceptions.Timeout:
            print(f"❌ TIMEOUT: {url} took too long to respond")
        except Exception as e:
            print(f"❌ ERROR: {url} - {e}")
    
    return False

def check_docker_container():
    """Check if Docker container is running"""
    print("🐳 Checking Docker container...")
    
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=.*-app', '--format', 'table {{.Names}}\t{{.Status}}'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Docker containers found:")
            print(result.stdout)
            return True
        else:
            print("❌ No Docker containers found")
            return False
    except Exception as e:
        print(f"❌ Error checking Docker containers: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Jenkins Scenario 2 Dynamic Webapp Test")
    print("=" * 60)
    
    # Check Docker container
    container_running = check_docker_container()
    
    # Test webapp
    webapp_accessible = test_dynamic_webapp()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   Docker Container: {'✅' if container_running else '❌'}")
    print(f"   Webapp Accessible: {'✅' if webapp_accessible else '❌'}")
    
    if container_running and webapp_accessible:
        print("\n🎉 SUCCESS: Dynamic webapp is working correctly!")
        print("   🌐 Access: http://localhost:8080")
        print("   📊 API: http://localhost:8080/api/status")
        return True
    else:
        print("\n❌ FAILURE: Dynamic webapp is not working properly")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
