#!/usr/bin/env python3
"""
Test script for Jenkins Scenario 2 Web Application
Tests if the webapp is accessible and working correctly
"""

import os
import sys
import time
import requests
import subprocess
from urllib.parse import urljoin

def test_webapp():
    """Test if webapp is accessible"""
    print("🧪 Testing webapp accessibility...")
    
    # Check if webapp directory exists
    if not os.path.exists("webapp"):
        print("❌ Webapp directory not found")
        return False
    
    # Get port from file
    port_file = "webapp/webapp.port"
    if not os.path.exists(port_file):
        print("❌ Port file not found")
        return False
    
    try:
        with open(port_file, 'r') as f:
            port = int(f.read().strip())
    except (ValueError, FileNotFoundError):
        print("❌ Invalid port file")
        return False
    
    # Test URLs
    test_urls = [
        f"http://localhost:{port}",
        f"http://127.0.0.1:{port}",
        f"http://0.0.0.0:{port}"
    ]
    
    # Get Docker host IP
    try:
        result = subprocess.run(['ip', 'route', 'show', 'default'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            docker_host_ip = result.stdout.split()[2]
            test_urls.append(f"http://{docker_host_ip}:{port}")
    except:
        pass
    
    # Test each URL
    for url in test_urls:
        print(f"🔍 Testing {url}...")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ SUCCESS: {url} is accessible!")
                print(f"   Status: {response.status_code}")
                print(f"   Content length: {len(response.text)} characters")
                
                # Check if it's our webapp
                if "Jenkins Parameterized Build Demo" in response.text:
                    print("✅ Content verified: This is our webapp!")
                    return True
                else:
                    print("⚠️  Content mismatch: This might not be our webapp")
            else:
                print(f"❌ FAILED: {url} returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ CONNECTION ERROR: {url} is not accessible")
        except requests.exceptions.Timeout:
            print(f"❌ TIMEOUT: {url} took too long to respond")
        except Exception as e:
            print(f"❌ ERROR: {url} - {e}")
    
    print("❌ No accessible URLs found")
    return False

def check_process():
    """Check if webapp process is running"""
    print("🔍 Checking webapp process...")
    
    pid_file = "webapp/webapp.pid"
    if not os.path.exists(pid_file):
        print("❌ PID file not found")
        return False
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process is running
        try:
            os.kill(pid, 0)
            print(f"✅ Process {pid} is running")
            return True
        except ProcessLookupError:
            print(f"❌ Process {pid} is not running")
            return False
    except (ValueError, FileNotFoundError):
        print("❌ Invalid PID file")
        return False

def main():
    """Main test function"""
    print("🚀 Jenkins Scenario 2 Webapp Test")
    print("=" * 50)
    
    # Check process
    process_running = check_process()
    
    # Test accessibility
    webapp_accessible = test_webapp()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Process Running: {'✅' if process_running else '❌'}")
    print(f"   Webapp Accessible: {'✅' if webapp_accessible else '❌'}")
    
    if process_running and webapp_accessible:
        print("\n🎉 SUCCESS: Webapp is working correctly!")
        return True
    else:
        print("\n❌ FAILURE: Webapp is not working properly")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
