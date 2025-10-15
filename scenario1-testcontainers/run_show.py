#!/usr/bin/env python3
"""
🎭 TestContainers Magic Show - Launcher
Handles environment setup and starts the theatrical demo
"""

import os
import sys
import subprocess
import shutil

def check_docker():
    """Check if Docker is accessible"""
    # Try common Docker paths
    docker_paths = [
        '/usr/local/bin/docker',
        '/usr/bin/docker',
        shutil.which('docker')
    ]

    for docker_path in docker_paths:
        if docker_path and os.path.exists(docker_path):
            try:
                result = subprocess.run(
                    [docker_path, 'ps'],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    # Docker works! Add to PATH
                    docker_dir = os.path.dirname(docker_path)
                    os.environ['PATH'] = f"{docker_dir}:{os.environ.get('PATH', '')}"
                    print(f"✅ Found Docker at: {docker_path}")
                    return True
            except:
                continue

    # Docker not found
    print("❌ Docker not found or not running")
    print("\n💡 Solutions:")
    print("   1. Start Docker Desktop (macOS/Windows)")
    print("   2. Install Docker: brew install --cask docker")
    print("   3. Linux: sudo systemctl start docker")
    print("\n   Then run this script again!")
    return False

def check_port(port=5001):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        sock.close()
        print(f"✅ Port {port} is available")
        return True
    except OSError:
        print(f"⚠️  Port {port} is in use")
        print(f"\n💡 Solutions:")
        print(f"   • Find what's using it: lsof -i :{port}")
        print(f"   • Kill it: kill -9 <PID>")
        print(f"   • Or the app will use another port automatically")
        return False

def activate_venv():
    """Activate virtual environment"""
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')

    if not os.path.exists(venv_dir):
        print("⚠️  Virtual environment not found")
        print("💡 Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', venv_dir])

    # Activate by modifying PATH and using venv's Python
    if sys.platform == 'win32':
        python_path = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:
        python_path = os.path.join(venv_dir, 'bin', 'python')

    if os.path.exists(python_path):
        print(f"✅ Using venv: {python_path}")
        return python_path
    else:
        print("⚠️  Using system Python")
        return sys.executable

def install_dependencies(python_path):
    """Install required packages"""
    print("\n📦 Checking dependencies...")

    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')

    if os.path.exists(requirements_file):
        print("   Installing from requirements.txt...")
        subprocess.run(
            [python_path, '-m', 'pip', 'install', '-q', '-r', requirements_file],
            check=False
        )
        print("✅ Dependencies installed")
    else:
        print("⚠️  requirements.txt not found, installing basics...")
        packages = ['flask', 'flask-cors', 'testcontainers', 'psycopg', 'redis']
        for pkg in packages:
            subprocess.run(
                [python_path, '-m', 'pip', 'install', '-q', pkg],
                check=False
            )
        print("✅ Basic dependencies installed")

def main():
    print("=" * 60)
    print("🎭 TestContainers Magic Show - Starting Up")
    print("=" * 60)
    print()

    # Step 1: Check Docker
    if not check_docker():
        sys.exit(1)

    # Step 2: Check port
    check_port(5001)

    # Step 3: Activate venv
    python_path = activate_venv()

    # Step 4: Install dependencies
    install_dependencies(python_path)

    print()
    print("=" * 60)
    print("🚀 Launching Reality Engine...")
    print("=" * 60)
    print()

    # Step 5: Run reality_engine.py
    reality_engine = os.path.join(os.path.dirname(__file__), 'reality_engine.py')

    os.execv(python_path, [python_path, reality_engine])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Try running manually:")
        print("   source venv/bin/activate")
        print("   python3 reality_engine.py")
        sys.exit(1)
