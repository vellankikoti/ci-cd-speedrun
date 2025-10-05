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
        # Check if pip is available in the existing venv
        if check_pip_in_venv():
            return True
        else:
            print("⚠️  Virtual environment exists but pip is missing, recreating...")
            import shutil
            shutil.rmtree(venv_path)
    
    print("📦 Creating virtual environment...")
    try:
        # Create venv with ensurepip to guarantee pip is included
        subprocess.check_call([
            sys.executable, "-m", "venv", 
            "--upgrade-deps",  # Upgrade pip and setuptools
            "venv-testcontainers"
        ])
        print("✅ Virtual environment created successfully")
        
        # Verify pip is available
        if check_pip_in_venv():
            return True
        else:
            print("⚠️  Installing pip manually...")
            return install_pip_in_venv()
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        print("💡 Trying alternative method...")
        return create_virtual_environment_alternative()

def check_pip_in_venv():
    """Check if pip is available in the virtual environment"""
    venv_python = get_venv_python()
    if not venv_python.exists():
        return False
    
    try:
        result = subprocess.run([
            str(venv_python), "-m", "pip", "--version"
        ], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def install_pip_in_venv():
    """Install pip in the virtual environment if missing"""
    venv_python = get_venv_python()
    if not venv_python.exists():
        return False
    
    print("📦 Installing pip in virtual environment...")
    try:
        # Try to install pip using ensurepip
        subprocess.check_call([
            str(venv_python), "-m", "ensurepip", "--upgrade"
        ])
        print("✅ Pip installed successfully")
        return True
    except subprocess.CalledProcessError:
        try:
            # Fallback: download and install pip manually
            import urllib.request
            import tempfile
            
            print("📦 Downloading pip manually...")
            with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
                urllib.request.urlretrieve(
                    "https://bootstrap.pypa.io/get-pip.py", 
                    f.name
                )
                
                subprocess.check_call([
                    str(venv_python), f.name
                ])
                
                os.unlink(f.name)
            print("✅ Pip installed manually")
            return True
        except Exception as e:
            print(f"❌ Failed to install pip: {e}")
            return False

def create_virtual_environment_alternative():
    """Alternative method to create virtual environment"""
    print("📦 Trying alternative venv creation method...")
    try:
        # Try using virtualenv if available
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "virtualenv"
        ])
        subprocess.check_call([
            sys.executable, "-m", "virtualenv", "venv-testcontainers"
        ])
        print("✅ Virtual environment created with virtualenv")
        return check_pip_in_venv()
    except subprocess.CalledProcessError:
        print("❌ Alternative venv creation also failed")
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
    
    # Ensure pip is available before installing requirements
    if not check_pip_in_venv():
        print("⚠️  Pip not available, installing it first...")
        if not install_pip_in_venv():
            print("❌ Cannot install requirements without pip")
            return False
    
    print("📦 Installing dependencies in virtual environment...")
    try:
        # First upgrade pip itself
        subprocess.check_call([
            str(venv_python), "-m", "pip", "install", "--upgrade", "pip"
        ])
        
        # Then install requirements
        subprocess.check_call([
            str(venv_python), "-m", "pip", "install", "-r", str(requirements_file), "--upgrade"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Trying to install packages individually...")
        return install_requirements_individually()

def install_requirements_individually():
    """Install requirements individually as fallback"""
    venv_python = get_venv_python()
    requirements_file = Path("requirements.txt")
    
    try:
        with open(requirements_file, 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"📦 Installing {len(packages)} packages individually...")
        failed_packages = []
        
        for package in packages:
            try:
                print(f"   Installing {package}...")
                subprocess.check_call([
                    str(venv_python), "-m", "pip", "install", package
                ])
            except subprocess.CalledProcessError:
                print(f"   ⚠️  Failed to install {package}")
                failed_packages.append(package)
        
        if failed_packages:
            print(f"⚠️  {len(failed_packages)} packages failed to install: {', '.join(failed_packages)}")
            print("💡 You can try installing them manually later")
            return len(failed_packages) < len(packages)  # Success if at least some installed
        else:
            print("✅ All packages installed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Failed to install packages individually: {e}")
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
        print("   # For bash/zsh:")
        print("   source venv-testcontainers/bin/activate")
        print("   # Or use the venv python directly:")
        print("   ./venv-testcontainers/bin/python labs/basics/lab1_postgresql_basics.py")
    
    print("\n2. Run a lab:")
    print("   python labs/basics/lab1_postgresql_basics.py")
    print("   python3 labs/basics/lab1_postgresql_basics.py")
    print("   # Or without activation:")
    print("   ./venv-testcontainers/bin/python labs/basics/lab1_postgresql_basics.py")
    
    print("\n3. When done, deactivate:")
    print("   deactivate")
    
    print("\n💡 You should see (venv-testcontainers) in your prompt when activated!")
    print("💡 If activation doesn't work, use the full path to the venv python!")

def install_globally():
    """Install packages globally as fallback option"""
    print("🌍 Installing packages globally (fallback option)...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--user"
        ])
        print("✅ Packages installed globally (user install)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Global installation failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 TestContainers Workshop Setup with Virtual Environment")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    venv_success = create_virtual_environment()
    
    if venv_success:
        # Install requirements in venv
        if not install_requirements():
            print("\n⚠️  Venv setup incomplete, trying global installation...")
            if install_globally():
                print("✅ Global installation successful!")
                print("\n💡 You can now run labs with: python3 labs/basics/lab1_postgresql_basics.py")
                return True
            else:
                print("\n❌ Both venv and global installation failed")
                print("💡 Try manual installation: pip install -r requirements.txt")
                return False
    else:
        print("\n⚠️  Virtual environment creation failed, trying global installation...")
        if install_globally():
            print("✅ Global installation successful!")
            print("\n💡 You can now run labs with: python3 labs/basics/lab1_postgresql_basics.py")
            return True
        else:
            print("\n❌ Both venv and global installation failed")
            print("💡 Try manual installation: pip install -r requirements.txt")
            return False
    
    # Check Docker
    if not check_docker():
        print("\n⚠️  Docker not available, but setup is complete")
        print("💡 Start Docker and then run the labs")
        return False
    
    print("\n✅ Setup completed successfully!")
    if venv_success:
        print_activation_instructions()
    else:
        print("\n💡 Run labs with: python3 labs/basics/lab1_postgresql_basics.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
