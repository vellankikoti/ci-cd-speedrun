#!/usr/bin/env python3
"""
Test Master - Demo Script
A script to demonstrate TestContainers integration and run tests.
"""

import subprocess
import sys
import time
import requests
import webbrowser
from threading import Timer

def run_command(command, description):
    """Run a command and print the result."""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Error!")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_endpoints():
    """Test the application endpoints."""
    print("\n🌐 Testing Application Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    try:
        # Test home page
        print("Testing home page...")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Home page working!")
        else:
            print(f"❌ Home page failed: {response.status_code}")
            
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   Database status: {data['database_status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
        # Test users endpoint
        print("Testing users endpoint...")
        response = requests.get(f"{base_url}/users", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Users endpoint: {data['count']} users found")
        else:
            print(f"❌ Users endpoint failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application. Make sure it's running!")
        return False
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")
        return False
    
    return True

def run_testcontainers_tests():
    """Run TestContainers tests."""
    print("\n🧪 Running TestContainers Tests")
    print("=" * 50)
    
    tests = [
        ("PostgreSQL Tests", "python -m pytest tests/test_containers.py::test_postgres -v -s"),
        ("MySQL Tests", "python -m pytest tests/test_containers.py::test_mysql -v -s"),
        ("Redis Tests", "python -m pytest tests/test_containers.py::test_redis -v -s"),
        ("Parallel Tests", "python -m pytest tests/test_containers.py::test_parallel_containers -v -s")
    ]
    
    for test_name, command in tests:
        print(f"\n🔬 {test_name}")
        print("-" * 30)
        
        if not run_command(command, f"Running {test_name}"):
            print(f"❌ {test_name} failed!")
            return False
        else:
            print(f"✅ {test_name} passed!")
    
    return True

def open_browser():
    """Open the application in the browser."""
    try:
        webbrowser.open("http://localhost:5000")
        print("🌐 Opened application in browser!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")

def main():
    """Main demo function."""
    print("🧪 Test Master - Demo Script")
    print("=" * 50)
    print("This script will demonstrate TestContainers integration!")
    print()
    
    # Check if we're in the right directory
    import os
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found. Please run this script from the scenario directory.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Run basic tests
    if not run_command("python -m pytest tests/test_app.py -v", "Running basic tests"):
        print("❌ Basic tests failed. Please check the test output above.")
        sys.exit(1)
    
    print("\n🎉 Basic tests passed! Now testing with TestContainers...")
    print("=" * 50)
    
    # Run TestContainers tests
    if not run_testcontainers_tests():
        print("❌ TestContainers tests failed. Please check the test output above.")
        sys.exit(1)
    
    print("\n🎉 All TestContainers tests passed! Starting the application...")
    print("=" * 50)
    print("The application will start in the background.")
    print("You can test it by visiting: http://localhost:5000")
    print("Press Ctrl+C to stop the application.")
    print()
    
    # Start the application
    try:
        # Open browser after a short delay
        Timer(2.0, open_browser).start()
        
        # Start the Flask app
        import app
        app.app.run(host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo completed! Thanks for trying Test Master!")
        print("Next steps:")
        print("1. Try the Jenkins pipeline")
        print("2. Move to Scenario 3: Docker Ninja")
        print("3. Keep learning Jenkins!")

if __name__ == "__main__":
    main()
