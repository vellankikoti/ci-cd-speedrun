#!/usr/bin/env python3
"""
Quick test to verify Docker detection works
Run this in Codespaces to verify the fix
"""
import subprocess
import os
import sys

print("=" * 60)
print("🔍 Docker Detection Test")
print("=" * 60)
print()

# Check environment
print("📍 Environment:")
print(f"   Platform: {sys.platform}")
if os.getenv('CODESPACES'):
    print(f"   Codespaces: YES")
    print(f"   Codespace Name: {os.getenv('CODESPACE_NAME', 'N/A')}")
else:
    print(f"   Codespaces: NO (running locally)")
print()

# Check PATH
print("📂 PATH:")
path_dirs = os.environ.get('PATH', '').split(':')
for p in path_dirs[:5]:  # Show first 5
    print(f"   • {p}")
if len(path_dirs) > 5:
    print(f"   ... and {len(path_dirs) - 5} more")
print()

# Test which command
print("🔎 Testing 'which docker':")
try:
    result = subprocess.run(['which', 'docker'], capture_output=True, text=True, timeout=2)
    if result.returncode == 0:
        docker_path = result.stdout.strip()
        print(f"   ✅ Found: {docker_path}")
    else:
        print(f"   ❌ Not found")
        docker_path = None
except Exception as e:
    print(f"   ❌ Error: {e}")
    docker_path = None
print()

# Check common locations
print("📁 Checking common Docker locations:")
locations = [
    '/usr/local/bin/docker',
    '/usr/bin/docker',
    '/opt/homebrew/bin/docker'
]

for loc in locations:
    exists = os.path.exists(loc)
    status = "✅ EXISTS" if exists else "❌ NOT FOUND"
    print(f"   {status}: {loc}")
    if exists and not docker_path:
        docker_path = loc
print()

# Test Docker if found
if docker_path:
    print(f"🐳 Testing Docker at: {docker_path}")
    try:
        # Test version
        result = subprocess.run([docker_path, '--version'], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print(f"   ✅ Version: {result.stdout.strip()}")
        else:
            print(f"   ❌ Version check failed")

        # Test ps
        result = subprocess.run([docker_path, 'ps'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   ✅ Docker is running!")
            lines = result.stdout.strip().split('\n')
            print(f"   📊 Containers: {len(lines) - 1} running")
        else:
            print(f"   ❌ Docker not running")
            print(f"   Error: {result.stderr}")
    except Exception as e:
        print(f"   ❌ Error testing Docker: {e}")
else:
    print("❌ Docker not found anywhere!")
    print()
    print("💡 Solutions:")
    print("   • Codespaces: Docker should be at /usr/local/bin/docker")
    print("   • Check if devcontainer.json has Docker-in-Docker feature")
    print("   • Local: Start Docker Desktop")

print()
print("=" * 60)
print("✅ Test complete!")
print("=" * 60)
