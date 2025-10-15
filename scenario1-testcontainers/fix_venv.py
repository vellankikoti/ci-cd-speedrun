#!/usr/bin/env python3
"""
Fix Virtual Environment - Python Script
=======================================

Automatically fixes virtual environment issues by recreating it.
Handles the common "required file not found" error in Codespaces.

Usage:
    python3 fix_venv.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_status(message, status="INFO"):
    """Print status message with emoji"""
    emojis = {
        "INFO": "ℹ️",
        "SUCCESS": "✅", 
        "ERROR": "❌",
        "WARNING": "⚠️"
    }
    print(f"{emojis.get(status, 'ℹ️')} {message}")

def run_command(cmd, check=True):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Compatible", "SUCCESS")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Requires 3.11+", "ERROR")
        return False

def recreate_venv():
    """Recreate virtual environment"""
    venv_path = Path("venv")
    
    # Remove existing venv if it exists
    if venv_path.exists():
        print_status("Removing existing virtual environment...", "INFO")
        shutil.rmtree(venv_path)
    
    # Create new venv
    print_status("Creating new virtual environment...", "INFO")
    success, stdout, stderr = run_command("python3 -m venv venv")
    
    if not success:
        print_status(f"Failed to create virtual environment: {stderr}", "ERROR")
        return False
    
    print_status("Virtual environment created successfully", "SUCCESS")
    return True

def install_dependencies():
    """Install dependencies in virtual environment"""
    print_status("Installing dependencies...", "INFO")
    
    # Use venv's pip
    pip_cmd = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip"
    
    success, stdout, stderr = run_command(f"{pip_cmd} install -r requirements.txt")
    
    if not success:
        print_status(f"Failed to install dependencies: {stderr}", "ERROR")
        return False
    
    print_status("Dependencies installed successfully", "SUCCESS")
    return True

def test_installation():
    """Test that everything works"""
    print_status("Testing installation...", "INFO")
    
    # Test Python import
    python_cmd = "venv/bin/python" if os.name != 'nt' else "venv\\Scripts\\python"
    
    # Create a temporary test file
    test_file = "test_imports.py"
    with open(test_file, "w") as f:
        f.write("""import sys
try:
    import flask
    import testcontainers
    import psycopg
    import redis
    import pytest
    print("All imports successful")
    sys.exit(0)
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)
""")
    
    try:
        success, stdout, stderr = run_command(f"{python_cmd} {test_file}")
        
        if success:
            print_status("All dependencies working correctly", "SUCCESS")
            return True
        else:
            print_status(f"Test failed: {stderr}", "ERROR")
            return False
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    """Main function"""
    print("🔧 Virtual Environment Fixer")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Recreate virtual environment
    if not recreate_venv():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    print("\n🎉 Virtual environment fixed successfully!")
    print("\nNext steps:")
    print("1. Activate virtual environment:")
    print("   source venv/bin/activate  # macOS/Linux")
    print("   venv\\Scripts\\activate     # Windows")
    print("\n2. Run the workshop:")
    print("   python reality_engine.py  # The Show")
    print("   python workshop.py        # The Workshop")
    print("   pytest tests/ -v          # The Tests")

if __name__ == "__main__":
    main()
