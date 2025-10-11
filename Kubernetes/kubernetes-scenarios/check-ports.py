#!/usr/bin/env python3
"""
Port Status Checker
Shows which ports are in use by Kubernetes services and local processes
"""

import subprocess
import socket
from kubernetes import client, config

def check_k8s_ports():
    """Check Kubernetes NodePorts"""
    print("\n" + "="*70)
    print("🔍 Kubernetes NodePort Status")
    print("="*70 + "\n")

    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()

        services = v1.list_service_for_all_namespaces()
        nodeport_services = []

        for svc in services.items:
            if svc.spec.type == 'NodePort' and svc.spec.ports:
                for port in svc.spec.ports:
                    if port.node_port:
                        nodeport_services.append({
                            'namespace': svc.metadata.namespace,
                            'service': svc.metadata.name,
                            'port': port.node_port,
                            'target': port.target_port
                        })

        if nodeport_services:
            print("📊 NodePort Services:")
            for svc in sorted(nodeport_services, key=lambda x: x['port']):
                print(f"   Port {svc['port']:5d} → {svc['namespace']:20s} / {svc['service']:30s} (target: {svc['target']})")
        else:
            print("✅ No NodePort services found")

    except Exception as e:
        print(f"⚠️  Could not check Kubernetes services: {e}")

def check_local_ports():
    """Check local port usage"""
    print("\n" + "="*70)
    print("🔍 Local Port Status")
    print("="*70 + "\n")

    common_ports = {
        5000: "Flask dashboard (comparison-dashboard.py)",
        6000: "Security breach dashboard",
        8000: "MkDocs / other services",
        8080: "Jenkins / other services",
        31000: "Vote app (preferred)",
        31001: "Result app (preferred)",
        31002: "Todo app / other",
    }

    print("📊 Common Ports Status:")
    for port, description in sorted(common_ports.items()):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
            status = "✅ Available"
        except OSError:
            status = "🔴 In use"

        print(f"   Port {port:5d}: {status:15s} - {description}")

def get_port_process(port):
    """Get process using a port"""
    try:
        result = subprocess.run(
            f"lsof -i :{port} | tail -1",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            parts = result.stdout.split()
            if len(parts) >= 2:
                return f"{parts[0]} (PID: {parts[1]})"
    except:
        pass
    return None

def check_port_details():
    """Show detailed port usage"""
    print("\n" + "="*70)
    print("🔍 Detailed Port Usage (ports 5000-6000, 31000-31005)")
    print("="*70 + "\n")

    port_ranges = [(5000, 6001), (31000, 31006)]

    for start, end in port_ranges:
        print(f"\nRange {start}-{end-1}:")
        for port in range(start, end):
            process = get_port_process(port)
            if process:
                print(f"   Port {port}: 🔴 {process}")

def suggest_cleanup():
    """Suggest cleanup commands"""
    print("\n" + "="*70)
    print("🧹 Cleanup Suggestions")
    print("="*70 + "\n")

    print("To free up ports:")
    print("\n1. Stop port-forward processes:")
    print("   pkill -f 'kubectl port-forward'")
    print("\n2. Stop Flask dashboards:")
    print("   pkill -f 'comparison-dashboard.py'")
    print("   pkill -f 'security-breach-dashboard.py'")
    print("\n3. Delete Kubernetes namespaces:")
    print("   kubectl delete namespace vote-app")
    print("   kubectl delete namespace secure-todo")
    print("   kubectl delete namespace insecure-todo")
    print("\n4. Or use the cleanup script:")
    print("   ./cleanup-all.sh")

def main():
    """Main function"""
    print("\n🔍 Port Status Checker for Kubernetes Workshop\n")

    check_k8s_ports()
    check_local_ports()
    check_port_details()
    suggest_cleanup()

    print("\n" + "="*70)
    print("✅ Port check complete!")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
