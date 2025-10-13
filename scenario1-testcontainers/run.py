#!/usr/bin/env python3
"""
Scenario 1: TestContainers Magic - Run Script
=============================================

Simple Python script to run the scenario.
Handles setup and execution in one command.

Usage:
    python run.py
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_header():
    """Print run header"""
    print("🧪 Scenario 1: TestContainers Magic")
    print("=" * 50)
    print("⚡ CI/CD Speed Run - PyCon ES 2025")
    print("🐍 Pure Python - Cross Platform")
    print("")

def check_setup():
    """Check if setup is complete"""
    print("🔍 Checking setup...")
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found")
        print("💡 Run 'python setup.py' first")
        return False
    
    # Check if dependencies are installed
    python_cmd = get_python_command()
    try:
        subprocess.run([python_cmd, "-c", "import flask, testcontainers, psycopg"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Dependencies not installed")
        print("💡 Run 'python setup.py' first")
        return False
    
    # Check if Docker is running
    try:
        subprocess.run(["docker", "ps"], check=True, capture_output=True)
        print("✅ Docker is running")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker not running")
        print("💡 Please start Docker and try again")
        return False
    
    print("✅ Setup complete")
    return True

def get_python_command():
    """Get the correct python command for the platform"""
    if sys.platform == "win32":
        return str(Path("venv") / "Scripts" / "python.exe")
    else:
        return str(Path("venv") / "bin" / "python")

def run_app():
    """Run the Flask application"""
    print("🚀 Starting TestContainers Magic...")
    print("")
    
    python_cmd = get_python_command()
    
    try:
        # Start the application
        subprocess.run([python_cmd, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False
    
    return True

def main():
    """Main run function"""
    print_header()
    
    # Check setup
    if not check_setup():
        print("\n💡 To fix setup issues, run:")
        print("   python setup.py")
        sys.exit(1)
    
    print("")
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main()
