#!/usr/bin/env python3
"""
TestContainers Workshop Setup with Virtual Environment
Creates venv, installs dependencies, and validates environment
Requires Python 3.10 or later
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10 or later"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv-testcontainers")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv-testcontainers"])
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_venv_python():
    """Get the Python executable in the virtual environment"""
    if sys.platform == "win32":
        return Path("venv-testcontainers/Scripts/python.exe")
    else:
        return Path("venv-testcontainers/bin/python")

def install_requirements():
    """Install requirements in virtual environment"""
    requirements_file = Path("requirements.txt")
    venv_python = get_venv_python()
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    if not venv_python.exists():
        print("❌ Virtual environment Python not found")
        return False
    
    print("📦 Installing dependencies in virtual environment...")
    try:
        subprocess.check_call([
            str(venv_python), "-m", "pip", "install", "-r", str(requirements_file), "--upgrade"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_docker():
    """Check if Docker is available and running"""
    try:
        # Check if docker command exists
        subprocess.run(["docker", "--version"], 
                      capture_output=True, check=True)
        
        # Check if Docker daemon is running
        result = subprocess.run(["docker", "ps"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is running")
            return True
        else:
            print("❌ Docker is installed but not running")
            print("💡 Please start Docker Desktop or Docker Engine")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not in PATH")
        print("💡 Installation guides:")
        print("   Windows: https://docs.docker.com/desktop/windows/")
        print("   macOS: https://docs.docker.com/desktop/mac/")
        print("   Linux: https://docs.docker.com/engine/install/")
        return False

def print_activation_instructions():
    """Print instructions for activating virtual environment"""
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS")
    print("=" * 60)
    print("1. Activate the virtual environment:")
    
    if sys.platform == "win32":
        print("   Command Prompt:")
        print("     venv-testcontainers\\Scripts\\activate")
        print("   PowerShell:")
        print("     venv-testcontainers\\Scripts\\Activate.ps1")
    else:
        print("   source venv-testcontainers/bin/activate")
    
    print("\n2. Run a lab:")
    print("   python labs/basics/lab1_first_container.py")
    print("   python3 labs/basics/lab1_first_container.py")
    
    print("\n3. When done, deactivate:")
    print("   deactivate")
    
    print("\n💡 You should see (venv-testcontainers) in your prompt when activated!")

def main():
    """Main setup function"""
    print("🚀 TestContainers Workshop Setup with Virtual Environment")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n⚠️  Setup incomplete, but you can still try manual installation")
        print("💡 Activate venv and run: pip install -r requirements.txt")
        return False
    
    # Check Docker
    if not check_docker():
        print("\n⚠️  Docker not available, but venv setup is complete")
        print("💡 Start Docker and then run the labs")
        return False
    
    print("\n✅ Setup completed successfully!")
    print_activation_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
