#!/usr/bin/env python3
"""
Real-time Docker container monitor
Watch TestContainers spin up and down during workshop/demos
Works in Codespaces and local environments
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def get_containers():
    """Get current container status"""
    try:
        result = subprocess.run(
            ['docker', 'ps', '--format', 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def check_docker():
    """Check if Docker is available"""
    try:
        subprocess.run(
            ['docker', 'ps'],
            capture_output=True,
            timeout=5,
            check=True
        )
        return True
    except:
        return False

def main():
    """Main watch loop"""
    print("🔍 Docker Container Monitor")
    print("============================\n")

    # Check environment
    if os.getenv('CODESPACES'):
        print("📍 Running in GitHub Codespaces")
    else:
        print("📍 Running locally")

    # Check Docker
    if not check_docker():
        print("\n❌ Docker is not running!")
        print("   In Codespaces: Docker should be available")
        print("   Locally: Start Docker Desktop")
        sys.exit(1)

    print("✅ Docker is running")
    print("\nWatching for TestContainers...")
    print("Press Ctrl+C to stop\n")

    time.sleep(2)

    try:
        while True:
            clear_screen()

            # Header
            print("🔍 Docker Container Monitor (Live)")
            print("=" * 70)
            print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
            print(f"Press Ctrl+C to stop")
            print("=" * 70)
            print()

            # Get containers
            containers = get_containers()
            print(containers)

            # Footer
            print()
            print("=" * 70)
            print("👀 Watch for postgres:15-alpine and redis:7-alpine containers")
            print("   They will appear when workshop/demo starts")

            # Refresh every second
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n✅ Container monitoring stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
