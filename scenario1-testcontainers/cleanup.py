#!/usr/bin/env python3
"""
Cleanup script for Scenario 1: TestContainers Magic
Removes orphaned containers, networks, and cleans up Docker resources
Works in both Codespaces and local environments
"""

import subprocess
import sys
import signal
import time

def run_command(cmd, ignore_errors=False):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0 and not ignore_errors:
            print(f"   Warning: {result.stderr.strip()}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"   Timeout running: {cmd}")
        return ""
    except Exception as e:
        if not ignore_errors:
            print(f"   Error: {e}")
        return ""

def check_docker():
    """Check if Docker is available"""
    result = run_command("docker ps", ignore_errors=True)
    if "Cannot connect" in result or not result:
        print("❌ Docker is not running!")
        print("   In Codespaces: Docker should be available automatically")
        print("   Locally: Start Docker Desktop")
        sys.exit(1)

def stop_flask_apps():
    """Stop any running Flask applications"""
    print("🛑 Stopping Flask applications...")

    # Find Python processes running our apps
    processes = [
        "reality_engine.py",
        "workshop.py",
        "app.py",
        "demo.py"
    ]

    for proc in processes:
        try:
            # Find process IDs
            result = subprocess.run(
                f"pgrep -f {proc}",
                shell=True,
                capture_output=True,
                text=True
            )
            pids = result.stdout.strip().split('\n')

            for pid in pids:
                if pid:
                    try:
                        subprocess.run(f"kill -9 {pid}", shell=True, check=False)
                        print(f"   Stopped {proc} (PID: {pid})")
                    except:
                        pass
        except:
            pass

    print("✅ Flask apps stopped\n")

def remove_containers(filter_label=None, filter_image=None):
    """Remove containers by label or image"""
    if filter_label:
        cmd = f'docker ps -a --filter "label={filter_label}" -q'
        name = filter_label
    elif filter_image:
        cmd = f'docker ps -a --filter "ancestor={filter_image}" -q'
        name = filter_image
    else:
        return 0

    container_ids = run_command(cmd, ignore_errors=True)

    if container_ids:
        ids = container_ids.split('\n')
        count = len([i for i in ids if i])

        if count > 0:
            print(f"   Found {count} container(s)")
            run_command(f"docker rm -f {' '.join(ids)}", ignore_errors=True)
            return count

    return 0

def cleanup_networks():
    """Remove orphaned networks"""
    print("🗑️  Removing orphaned networks...")
    cmd = 'docker network ls --filter "label=org.testcontainers=true" -q'
    network_ids = run_command(cmd, ignore_errors=True)

    if network_ids:
        ids = network_ids.split('\n')
        count = len([i for i in ids if i])

        if count > 0:
            print(f"   Found {count} network(s)")
            for net_id in ids:
                if net_id:
                    run_command(f"docker network rm {net_id}", ignore_errors=True)
            print("✅ Removed TestContainers networks\n")
            return

    print("   No TestContainers networks found\n")

def cleanup_volumes():
    """Remove orphaned volumes"""
    print("🗑️  Removing orphaned volumes...")
    cmd = 'docker volume ls --filter "label=org.testcontainers=true" -q'
    volume_ids = run_command(cmd, ignore_errors=True)

    if volume_ids:
        ids = volume_ids.split('\n')
        count = len([i for i in ids if i])

        if count > 0:
            print(f"   Found {count} volume(s)")
            for vol_id in ids:
                if vol_id:
                    run_command(f"docker volume rm {vol_id}", ignore_errors=True)
            print("✅ Removed TestContainers volumes\n")
            return

    print("   No TestContainers volumes found\n")

def cleanup_cache():
    """Clean pytest and Python cache"""
    print("🗑️  Cleaning cache files...")

    import shutil
    import os

    # Remove pytest cache
    if os.path.exists(".pytest_cache"):
        shutil.rmtree(".pytest_cache")
        print("   Removed pytest cache")

    # Remove Python cache
    for root, dirs, files in os.walk("."):
        # Remove __pycache__ directories
        if "__pycache__" in dirs:
            cache_dir = os.path.join(root, "__pycache__")
            shutil.rmtree(cache_dir)

        # Remove .pyc files
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))

    print("✅ Removed Python cache\n")

def show_docker_status():
    """Show current Docker status"""
    print("📊 Current Docker Status:")
    print("=========================\n")

    print("Containers:")
    result = run_command('docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"')
    if result:
        print(result)
    else:
        print("   (none)")

    print("\nNetworks:")
    result = run_command('docker network ls --format "table {{.Name}}\t{{.Driver}}"')
    if result:
        print(result)

    print("\nVolumes:")
    result = run_command('docker volume ls --format "table {{.Name}}\t{{.Driver}}"')
    if result:
        print(result)
    print()

def main():
    """Main cleanup function"""
    print("🧹 Scenario 1: Cleanup Script")
    print("==============================\n")

    # Check Docker
    print("🐳 Checking Docker...")
    check_docker()
    print("✅ Docker is running\n")

    # Stop Flask apps
    stop_flask_apps()

    # Remove TestContainers
    print("🗑️  Removing TestContainers containers...")
    count = remove_containers(filter_label="org.testcontainers=true")
    if count > 0:
        print("✅ Removed TestContainers containers\n")
    else:
        print("   No TestContainers containers found\n")

    # Remove PostgreSQL containers
    print("🗑️  Removing PostgreSQL containers...")
    count = remove_containers(filter_image="postgres:15-alpine")
    if count > 0:
        print("✅ Removed PostgreSQL containers\n")
    else:
        print("   No PostgreSQL containers found\n")

    # Remove Redis containers
    print("🗑️  Removing Redis containers...")
    count = remove_containers(filter_image="redis:7-alpine")
    if count > 0:
        print("✅ Removed Redis containers\n")
    else:
        print("   No Redis containers found\n")

    # Cleanup networks
    cleanup_networks()

    # Cleanup volumes
    cleanup_volumes()

    # Cleanup cache
    cleanup_cache()

    # Show status
    show_docker_status()

    # Summary
    print("✅ Cleanup Complete!")
    print("====================\n")
    print("All TestContainers resources removed.")
    print("You can now run the scenario fresh.\n")
    print("Next steps:")
    print("  python3 reality_engine.py")
    print("  python3 workshop.py\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cleanup interrupted!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
