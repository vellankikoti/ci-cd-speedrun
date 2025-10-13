#!/usr/bin/env python3
"""
Scenario 1: TestContainers Magic - Python Setup Script
======================================================

Cross-platform Python setup script for Scenario 1.
No shell scripts needed - pure Python for maximum compatibility.

Usage:
    python setup.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🧪 Scenario 1: TestContainers Magic - Setup")
    print("=" * 50)
    print("⚡ CI/CD Speed Run - PyCon ES 2025")
    print("🐍 Pure Python Setup - Cross Platform")
    print("")

def check_python():
    """Check Python version"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python 3.11+ required, found {version.major}.{version.minor}")
        print("💡 Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_docker():
    """Check Docker availability"""
    print("🐳 Checking Docker...")
    
    try:
        result = subprocess.run(
            ["docker", "--version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ Docker found: {result.stdout.strip()}")
        
        # Check if Docker is running
        result = subprocess.run(
            ["docker", "ps"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print("✅ Docker is running")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker not found or not running")
        print("💡 Please install Docker Desktop and start it")
        return False

def create_virtual_environment():
    """Create Python virtual environment"""
    print("📦 Creating virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_pip_command():
    """Get the correct pip command for the platform"""
    if platform.system() == "Windows":
        return str(Path("venv") / "Scripts" / "pip.exe")
    else:
        return str(Path("venv") / "bin" / "pip")

def get_python_command():
    """Get the correct python command for the platform"""
    if platform.system() == "Windows":
        return str(Path("venv") / "Scripts" / "python.exe")
    else:
        return str(Path("venv") / "bin" / "python")

def install_dependencies():
    """Install Python dependencies"""
    print("📚 Installing dependencies...")
    
    pip_cmd = get_pip_command()
    python_cmd = get_python_command()
    
    try:
        # Upgrade pip first
        subprocess.run([python_cmd, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_testcontainers():
    """Test TestContainers functionality"""
    print("🧪 Testing TestContainers...")
    
    python_cmd = get_python_command()
    
    test_script = """
import os
os.environ['TESTCONTAINERS_CLOUD_ENABLED'] = 'false'

try:
    from testcontainers.postgres import PostgresContainer
    import psycopg
    print('✅ TestContainers imports successful')
    
    # Quick test
    with PostgresContainer('postgres:15-alpine') as postgres:
        conn = psycopg.connect(
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
            user=postgres.username,
            password=postgres.password,
            dbname=postgres.dbname
        )
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        print(f'✅ PostgreSQL test successful: {version.split()[0]} {version.split()[1]}')
        cur.close()
        conn.close()
    
    print('✅ TestContainers test passed!')
    
except Exception as e:
    print(f'❌ TestContainers test failed: {e}')
    exit(1)
"""
    
    try:
        result = subprocess.run(
            [python_cmd, "-c", test_script],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ TestContainers test failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def print_success():
    """Print success message"""
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("✅ All checks passed")
    print("✅ Dependencies installed")
    print("✅ TestContainers working")
    print("")
    print("🚀 Ready to run Scenario 1!")
    print("")
    print("📖 Next steps:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5001")
    print("   3. Try voting twice to see the magic!")
    print("")
    print("🧪 Or run the demo:")
    print("   python demo.py")
    print("")
    print("✨ Let's experience TestContainers magic!")

def main():
    """Main setup function"""
    print_header()
    
    # Check prerequisites
    if not check_python():
        sys.exit(1)
    
    if not check_docker():
        sys.exit(1)
    
    print("✅ All prerequisites met")
    print("")
    
    # Setup environment
    if not create_virtual_environment():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    print("")
    
    # Test functionality
    if not test_testcontainers():
        print("❌ Setup incomplete - TestContainers test failed")
        sys.exit(1)
    
    print_success()

if __name__ == "__main__":
    main()
