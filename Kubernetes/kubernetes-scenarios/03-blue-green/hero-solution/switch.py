#!/usr/bin/env python3
"""
🔄 Blue-Green Version Switcher
Easily switch between blue and green deployments
"""
import sys
import subprocess
import time

def run_command(cmd, capture=True):
    """Run a command"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=capture,
        text=True
    )
    return result

def get_current_version():
    """Get currently active version"""
    result = run_command(
        "kubectl get service demo-app -n blue-green-demo -o jsonpath='{.spec.selector.version}' 2>/dev/null"
    )
    return result.stdout.strip() or "none"

def get_pod_count(version):
    """Get number of running pods for a version"""
    result = run_command(
        f"kubectl get pods -n blue-green-demo -l version={version} -o jsonpath='{{.items[*].status.phase}}' 2>/dev/null"
    )
    phases = result.stdout.strip().split()
    return len([p for p in phases if p == 'Running'])

def switch_version(target_version):
    """Switch service to target version"""
    current = get_current_version()

    if current == target_version:
        print(f"\n⚠️  Already running {target_version.upper()} version!")
        return True

    print(f"\n🔄 Switching from {current.upper()} to {target_version.upper()}...")

    # Check if target deployment exists and has pods
    pod_count = get_pod_count(target_version)
    if pod_count == 0:
        print(f"❌ No running {target_version} pods found!")
        print(f"   Deploy {target_version} pods first with: kubectl scale deployment {target_version}-deployment -n blue-green-demo --replicas=3")
        return False

    print(f"   Found {pod_count} running {target_version.upper()} pods ✓")

    # Switch the service selector
    cmd = f"kubectl patch service demo-app -n blue-green-demo -p '{{\"spec\":{{\"selector\":{{\"version\":\"{target_version}\"}}}}}}'"
    result = run_command(cmd, capture=False)

    if result.returncode == 0:
        print(f"\n✅ Traffic switched to {target_version.upper()} version!")
        print(f"\n🎯 RESULT:")
        print(f"   Old version ({current.upper()}): Still running, but no traffic")
        print(f"   New version ({target_version.upper()}): Receiving all traffic")
        print(f"\n💡 TIP: Refresh http://localhost:31006 to see the change!")
        print(f"💡 TIP: You can instantly rollback with: python3 switch.py {current}")
        return True
    else:
        print(f"❌ Failed to switch traffic")
        return False

def show_status():
    """Show current deployment status"""
    print("\n" + "="*60)
    print("🎯 BLUE-GREEN DEPLOYMENT STATUS")
    print("="*60 + "\n")

    current = get_current_version()
    blue_pods = get_pod_count('blue')
    green_pods = get_pod_count('green')

    print(f"🔵 BLUE Deployment:")
    print(f"   Pods: {blue_pods}")
    print(f"   Status: {'🟢 ACTIVE (receiving traffic)' if current == 'blue' else '⚪ Standby (no traffic)'}")

    print(f"\n🟢 GREEN Deployment:")
    print(f"   Pods: {green_pods}")
    print(f"   Status: {'🟢 ACTIVE (receiving traffic)' if current == 'green' else '⚪ Standby (no traffic)'}")

    print(f"\n📊 Service Configuration:")
    print(f"   Current active version: {current.upper()}")
    print(f"   Endpoint: http://localhost:31006")

    print("\n" + "="*60)

def main():
    if len(sys.argv) < 2:
        print("""
╔════════════════════════════════════════════════════════════╗
║  🔄 BLUE-GREEN VERSION SWITCHER                           ║
╚════════════════════════════════════════════════════════════╝

Usage:
    python3 switch.py <command>

Commands:
    blue     - Switch to BLUE version (v1.0)
    green    - Switch to GREEN version (v2.0)
    status   - Show current deployment status

Examples:
    python3 switch.py green    # Switch to green
    python3 switch.py blue     # Switch to blue
    python3 switch.py status   # Show status
        """)
        return 1

    command = sys.argv[1].lower()

    if command == 'status':
        show_status()
    elif command == 'blue':
        if not switch_version('blue'):
            return 1
    elif command == 'green':
        if not switch_version('green'):
            return 1
    else:
        print(f"❌ Unknown command: {command}")
        print("   Valid commands: blue, green, status")
        return 1

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
