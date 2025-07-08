#!/usr/bin/env python3
"""
Enhanced Auto-scaling Monitor
============================
Real-time monitoring tool for the enhanced auto-scaling challenge.
Shows pod scaling, CPU usage, HPA status, and scaling events.
"""

import subprocess
import json
import time
import sys
import argparse
from datetime import datetime
from collections import deque

def run_kubectl(command, namespace=None):
    """Execute kubectl command and return output"""
    cmd = ["kubectl"] + command
    if namespace:
        cmd.extend(["-n", namespace])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def get_pod_status(namespace="scaling-challenge"):
    """Get detailed pod status"""
    result = run_kubectl([
        "get", "pods", "-l", "app=cpu-stress-app",
        "-o", "json"
    ], namespace)
    
    if not result:
        return {"total": 0, "running": 0, "pending": 0, "terminating": 0, "pods": []}
    
    try:
        data = json.loads(result)
        pods = data.get("items", [])
        
        status = {"total": len(pods), "running": 0, "pending": 0, "terminating": 0, "pods": []}
        
        for pod in pods:
            pod_name = pod["metadata"]["name"]
            pod_phase = pod["status"]["phase"]
            
            # Check if pod is terminating
            deletion_timestamp = pod["metadata"].get("deletionTimestamp")
            if deletion_timestamp:
                pod_status = "Terminating"
                status["terminating"] += 1
            elif pod_phase == "Running":
                pod_status = "Running"
                status["running"] += 1
            elif pod_phase == "Pending":
                pod_status = "Pending"
                status["pending"] += 1
            else:
                pod_status = pod_phase
            
            # Get pod creation time
            creation_time = pod["metadata"]["creationTimestamp"]
            
            status["pods"].append({
                "name": pod_name,
                "status": pod_status,
                "phase": pod_phase,
                "created": creation_time
            })
        
        return status
    except json.JSONDecodeError:
        return {"total": 0, "running": 0, "pending": 0, "terminating": 0, "pods": []}

def get_hpa_status(namespace="scaling-challenge"):
    """Get HPA status and metrics"""
    result = run_kubectl([
        "get", "hpa", "cpu-stress-app-hpa",
        "-o", "json"
    ], namespace)
    
    if not result:
        return None
    
    try:
        hpa = json.loads(result)
        
        spec = hpa.get("spec", {})
        status = hpa.get("status", {})
        
        # Get current metrics
        cpu_utilization = "Unknown"
        current_metrics = status.get("currentMetrics", [])
        
        for metric in current_metrics:
            if (metric.get("type") == "Resource" and 
                metric.get("resource", {}).get("name") == "cpu"):
                cpu_utilization = metric["resource"]["current"].get("averageUtilization", "Unknown")
                break
        
        # Get conditions
        conditions = status.get("conditions", [])
        scaling_active = False
        able_to_scale = False
        scaling_limited = False
        
        for condition in conditions:
            if condition["type"] == "ScalingActive":
                scaling_active = condition["status"] == "True"
            elif condition["type"] == "AbleToScale":
                able_to_scale = condition["status"] == "True"
            elif condition["type"] == "ScalingLimited":
                scaling_limited = condition["status"] == "True"
        
        return {
            "minReplicas": spec.get("minReplicas", 1),
            "maxReplicas": spec.get("maxReplicas", 10),
            "currentReplicas": status.get("currentReplicas", 1),
            "desiredReplicas": status.get("desiredReplicas", 1),
            "targetCPUUtilization": spec.get("metrics", [{}])[0].get("resource", {}).get("target", {}).get("averageUtilization", 50),
            "currentCPUUtilization": cpu_utilization,
            "scalingActive": scaling_active,
            "ableToScale": able_to_scale,
            "scalingLimited": scaling_limited,
            "lastScaleTime": status.get("lastScaleTime"),
            "conditions": conditions
        }
    except json.JSONDecodeError:
        return None

def get_scaling_events(namespace="scaling-challenge", limit=10):
    """Get recent scaling events"""
    result = run_kubectl([
        "get", "events", "--sort-by=.lastTimestamp",
        "--field-selector=involvedObject.kind=HorizontalPodAutoscaler",
        "-o", "json"
    ], namespace)
    
    if not result:
        return []
    
    try:
        data = json.loads(result)
        events = data.get("items", [])
        
        # Get the most recent events
        recent_events = []
        for event in events[-limit:]:
            recent_events.append({
                "time": event.get("lastTimestamp", event.get("firstTimestamp", "")),
                "reason": event.get("reason", ""),
                "message": event.get("message", ""),
                "type": event.get("type", "Normal")
            })
        
        return list(reversed(recent_events))  # Most recent first
    except json.JSONDecodeError:
        return []

def get_cpu_metrics(namespace="scaling-challenge"):
    """Get CPU metrics for pods"""
    result = run_kubectl([
        "top", "pods", "-l", "app=cpu-stress-app",
        "--no-headers"
    ], namespace)
    
    if not result:
        return {"total_cpu": "0m", "average_cpu": "0m", "pods": []}
    
    lines = result.strip().split('\n')
    pod_metrics = []
    total_cpu_millicores = 0
    
    for line in lines:
        if line.strip():
            parts = line.split()
            if len(parts) >= 3:
                pod_name = parts[0]
                cpu_usage = parts[1]  # e.g., "150m"
                memory_usage = parts[2]  # e.g., "128Mi"
                
                # Extract CPU millicores
                if cpu_usage.endswith('m'):
                    cpu_millicores = int(cpu_usage[:-1])
                else:
                    cpu_millicores = int(float(cpu_usage) * 1000)
                
                total_cpu_millicores += cpu_millicores
                
                pod_metrics.append({
                    "name": pod_name,
                    "cpu": cpu_usage,
                    "memory": memory_usage,
                    "cpu_millicores": cpu_millicores
                })
    
    average_cpu = total_cpu_millicores // max(1, len(pod_metrics))
    
    return {
        "total_cpu": f"{total_cpu_millicores}m",
        "average_cpu": f"{average_cpu}m",
        "pods": pod_metrics
    }

def display_dashboard():
    """Display the main monitoring dashboard"""
    # Clear screen
    print("\033[2J\033[H")
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print("📈 ENHANCED AUTO-SCALING MONITOR")
    print("=" * 80)
    print(f"🕒 Last Update: {timestamp}")
    print()
    
    # Get all metrics
    pod_status = get_pod_status()
    hpa_status = get_hpa_status()
    cpu_metrics = get_cpu_metrics()
    events = get_scaling_events(limit=5)
    
    # Pod Status Section
    print("🏗️  POD STATUS:")
    print("-" * 40)
    print(f"   Total Pods:     {pod_status['total']}")
    print(f"   Running:        {pod_status['running']}")
    print(f"   Pending:        {pod_status['pending']}")
    print(f"   Terminating:    {pod_status['terminating']}")
    
    if pod_status['pods']:
        print("\n   Pod Details:")
        for pod in pod_status['pods'][:8]:  # Show max 8 pods
            status_icon = "🟢" if pod['status'] == "Running" else "🟡" if pod['status'] == "Pending" else "🔴"
            print(f"   {status_icon} {pod['name']:<40} {pod['status']}")
    
    print()
    
    # CPU Metrics Section
    print("⚡ CPU METRICS:")
    print("-" * 40)
    print(f"   Total CPU:      {cpu_metrics['total_cpu']}")
    print(f"   Average CPU:    {cpu_metrics['average_cpu']}")
    
    if cpu_metrics['pods']:
        print("\n   Per-Pod CPU Usage:")
        for pod_metric in cpu_metrics['pods']:
            cpu_bar = create_cpu_bar(pod_metric['cpu_millicores'])
            print(f"   📊 {pod_metric['name']:<30} {pod_metric['cpu']:<8} {cpu_bar}")
    
    print()
    
    # HPA Status Section
    if hpa_status:
        print("🎯 HPA STATUS:")
        print("-" * 40)
        print(f"   Min Replicas:       {hpa_status['minReplicas']}")
        print(f"   Max Replicas:       {hpa_status['maxReplicas']}")
        print(f"   Current Replicas:   {hpa_status['currentReplicas']}")
        print(f"   Desired Replicas:   {hpa_status['desiredReplicas']}")
        print(f"   Target CPU:         {hpa_status['targetCPUUtilization']}%")
        print(f"   Current CPU:        {hpa_status['currentCPUUtilization']}%")
        
        print("\n   Scaling Conditions:")
        scaling_icon = "🟢" if hpa_status['scalingActive'] else "🔴"
        able_icon = "🟢" if hpa_status['ableToScale'] else "🔴"
        limited_icon = "🔴" if hpa_status['scalingLimited'] else "🟢"
        
        print(f"   {scaling_icon} Scaling Active:   {hpa_status['scalingActive']}")
        print(f"   {able_icon} Able to Scale:    {hpa_status['ableToScale']}")
        print(f"   {limited_icon} Scaling Limited:  {hpa_status['scalingLimited']}")
        
        if hpa_status['lastScaleTime']:
            print(f"   🕒 Last Scale Time:  {hpa_status['lastScaleTime']}")
    else:
        print("🎯 HPA STATUS:")
        print("-" * 40)
        print("   ❌ HPA not found or not accessible")
    
    print()
    
    # Scaling Events Section
    print("📊 RECENT SCALING EVENTS:")
    print("-" * 40)
    if events:
        for event in events:
            event_time = event['time'][:19] if event['time'] else "Unknown"
            event_icon = "🟢" if event['type'] == "Normal" else "🟡"
            print(f"   {event_icon} [{event_time}] {event['reason']}")
            print(f"      {event['message']}")
            print()
    else:
        print("   No recent scaling events found")
    
    print()
    
    # Scaling Insights
    print("💡 SCALING INSIGHTS:")
    print("-" * 40)
    
    if hpa_status:
        current_cpu = hpa_status['currentCPUUtilization']
        target_cpu = hpa_status['targetCPUUtilization']
        current_pods = hpa_status['currentReplicas']
        desired_pods = hpa_status['desiredReplicas']
        
        if isinstance(current_cpu, (int, float)) and current_cpu > target_cpu:
            print("   🔼 CPU usage above target - scaling up expected")
        elif isinstance(current_cpu, (int, float)) and current_cpu < target_cpu * 0.7:
            print("   🔽 CPU usage well below target - scaling down expected")
        else:
            print("   ✅ CPU usage within acceptable range")
        
        if current_pods != desired_pods:
            if desired_pods > current_pods:
                print(f"   ⬆️  Scaling UP in progress: {current_pods} → {desired_pods}")
            else:
                print(f"   ⬇️  Scaling DOWN in progress: {current_pods} → {desired_pods}")
        else:
            print("   🎯 Scaling system stable")
        
        if hpa_status['scalingLimited']:
            print("   ⚠️  Scaling is limited (check min/max replicas)")
        
        if not hpa_status['ableToScale']:
            print("   ❌ Unable to scale (check metrics server)")
    else:
        print("   ❌ Cannot provide insights - HPA status unavailable")

def create_cpu_bar(cpu_millicores, max_width=20):
    """Create a visual CPU usage bar"""
    # Assume 200m (0.2 cores) is 100% for display purposes
    max_cpu = 200
    percentage = min(100, (cpu_millicores / max_cpu) * 100)
    filled_width = int((percentage / 100) * max_width)
    
    bar = "█" * filled_width + "░" * (max_width - filled_width)
    return f"[{bar}] {percentage:5.1f}%"

def display_pod_details():
    """Display detailed pod information"""
    print("\033[2J\033[H")
    
    print("🏗️  DETAILED POD STATUS")
    print("=" * 80)
    
    pod_status = get_pod_status()
    cpu_metrics = get_cpu_metrics()
    
    # Create a mapping of pod metrics
    cpu_map = {pod['name']: pod for pod in cpu_metrics['pods']}
    
    if not pod_status['pods']:
        print("No pods found for app=cpu-stress-app")
        return
    
    print(f"{'Pod Name':<50} {'Status':<12} {'CPU':<10} {'Memory':<10} {'Age'}")
    print("-" * 90)
    
    for pod in pod_status['pods']:
        pod_name = pod['name']
        status = pod['status']
        
        # Get CPU and memory from metrics
        cpu_usage = "N/A"
        memory_usage = "N/A"
        
        if pod_name in cpu_map:
            cpu_usage = cpu_map[pod_name]['cpu']
            memory_usage = cpu_map[pod_name]['memory']
        
        # Calculate age
        try:
            from datetime import datetime
            created_time = datetime.fromisoformat(pod['created'].replace('Z', '+00:00'))
            age = datetime.now(created_time.tzinfo) - created_time
            age_str = f"{age.seconds // 60}m{age.seconds % 60}s"
        except:
            age_str = "Unknown"
        
        print(f"{pod_name:<50} {status:<12} {cpu_usage:<10} {memory_usage:<10} {age_str}")

def display_events():
    """Display detailed scaling events"""
    print("\033[2J\033[H")
    
    print("📊 SCALING EVENTS HISTORY")
    print("=" * 80)
    
    events = get_scaling_events(limit=20)
    
    if not events:
        print("No scaling events found")
        return
    
    print(f"{'Time':<20} {'Type':<8} {'Reason':<20} {'Message'}")
    print("-" * 100)
    
    for event in events:
        event_time = event['time'][:19] if event['time'] else "Unknown"
        event_type = event['type']
        reason = event['reason'][:20]
        message = event['message'][:60]
        
        print(f"{event_time:<20} {event_type:<8} {reason:<20} {message}")

def display_stats():
    """Display quick statistics"""
    pod_status = get_pod_status()
    hpa_status = get_hpa_status()
    cpu_metrics = get_cpu_metrics()
    
    print(f"Pods: {pod_status['running']}/{pod_status['total']} running")
    
    if hpa_status:
        print(f"HPA: {hpa_status['currentReplicas']}/{hpa_status['desiredReplicas']} replicas")
        print(f"CPU: {hpa_status['currentCPUUtilization']}% (target: {hpa_status['targetCPUUtilization']}%)")
    
    print(f"Total CPU: {cpu_metrics['total_cpu']}")

def continuous_monitor(refresh_interval=3):
    """Run continuous monitoring"""
    print("🚀 Starting continuous auto-scaling monitor...")
    print(f"📊 Refreshing every {refresh_interval} seconds")
    print("❌ Press Ctrl+C to stop")
    print()
    
    try:
        while True:
            display_dashboard()
            print()
            print(f"🔄 Refreshing in {refresh_interval} seconds... (Ctrl+C to stop)")
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped")

def main():
    parser = argparse.ArgumentParser(description="Enhanced Auto-scaling Monitor")
    parser.add_argument("command", nargs="?", default="dashboard", 
                       choices=["dashboard", "pods", "events", "stats", "monitor"],
                       help="Command to run")
    parser.add_argument("--interval", "-i", type=int, default=3,
                       help="Refresh interval for continuous monitoring (seconds)")
    
    args = parser.parse_args()
    
    if args.command == "dashboard":
        display_dashboard()
    elif args.command == "pods":
        display_pod_details()
    elif args.command == "events":
        display_events()
    elif args.command == "stats":
        display_stats()
    elif args.command == "monitor":
        continuous_monitor(args.interval)

if __name__ == "__main__":
    main()