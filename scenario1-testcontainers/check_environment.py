#!/usr/bin/env python3
"""
Environment checker for Codespaces
Checks if Docker is properly installed and guides user to fix if not
"""
import subprocess
import os
import sys

def main():
    print("=" * 70)
    print("🔍 CI/CD Chaos Workshop - Environment Check")
    print("=" * 70)
    print()

    # Check if in Codespaces
    in_codespaces = os.getenv('CODESPACES') == 'true'
    print(f"📍 Environment: {'GitHub Codespaces' if in_codespaces else 'Local'}")
    print()

    # Check Docker
    print("🐳 Checking Docker...")
    docker_installed = False

    # Try to find docker
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            print(f"   ✅ Docker found: {result.stdout.strip()}")
            docker_installed = True
        else:
            print(f"   ❌ Docker command failed")
    except FileNotFoundError:
        print(f"   ❌ Docker not found")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print()

    if docker_installed:
        # Test docker ps
        print("🔍 Testing Docker daemon...")
        try:
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ Docker daemon is running")
                container_count = len(result.stdout.strip().split('\n')) - 1
                print(f"   📊 Running containers: {container_count}")
            else:
                print(f"   ❌ Docker daemon not running")
                print(f"   Error: {result.stderr}")
                docker_installed = False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            docker_installed = False

    print()
    print("=" * 70)

    if docker_installed:
        print("✅ Environment is ready!")
        print()
        print("🚀 Next steps:")
        print("   python3 reality_engine.py")
        print("=" * 70)
        return 0
    else:
        print("❌ Docker is NOT installed!")
        print()

        if in_codespaces:
            print("🔧 FIX: Rebuild your Codespace container")
            print()
            print("   This Codespace was created without Docker.")
            print("   You need to rebuild it to install Docker-in-Docker.")
            print()
            print("   📋 Steps:")
            print("   1. Press F1 or Ctrl+Shift+P")
            print("   2. Type: 'Codespaces: Rebuild Container'")
            print("   3. Select it and wait ~2 minutes")
            print("   4. After rebuild, run: python3 reality_engine.py")
            print()
            print("   🌐 Or via GitHub:")
            print("   1. Go to: https://github.com/codespaces")
            print("   2. Find this Codespace")
            print("   3. Click '...' menu → 'Rebuild container'")
            print()
            print("   ℹ️  Why? The .devcontainer/devcontainer.json has Docker")
            print("           but it only installs when Codespace is created/rebuilt.")
        else:
            print("🔧 FIX: Install Docker Desktop")
            print()
            print("   You're running locally without Docker.")
            print()
            print("   📥 Install Docker:")
            print("   • macOS: https://docs.docker.com/desktop/install/mac-install/")
            print("   • Windows: https://docs.docker.com/desktop/install/windows-install/")
            print("   • Linux: https://docs.docker.com/engine/install/")
            print()
            print("   After installing, start Docker Desktop and run:")
            print("   python3 reality_engine.py")

        print("=" * 70)
        return 1

if __name__ == '__main__':
    sys.exit(main())
