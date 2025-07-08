#!/usr/bin/env python3
"""
Load Testing Script
===========================
Advanced load testing tool that can trigger real auto-scaling behavior
by creating actual CPU load on the target pods.
"""

import subprocess
import requests
import json
import time
import argparse
import threading
from datetime import datetime

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

def port_forward_service(service_name, local_port, remote_port, namespace="scaling-challenge"):
    """Start port forwarding in background"""
    def run_port_forward():
        subprocess.run([
            "kubectl", "port-forward", f"svc/{service_name}",
            f"{local_port}:{remote_port}", "-n", namespace
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    thread = threading.Thread(target=run_port_forward, daemon=True)
    thread.start()
    
    # Wait a moment for port forward to establish
    time.sleep(2)
    return thread

def check_pod_count(namespace="scaling-challenge"):
    """Get current pod count for cpu-stress-app"""
    result = run_kubectl([
        "get", "pods", "-l", "app=cpu-stress-app",
        "--no-headers"
    ], namespace)
    
    if result:
        return len([line for line in result.split('\n') if line.strip()])
    return 0

def check_hpa_status(namespace="scaling-challenge"):
    """Get current HPA status"""
    result = run_kubectl([
        "get", "hpa", "cpu-stress-app-hpa",
        "-o", "jsonpath={.status.currentReplicas},{.status.desiredReplicas},{.status.currentMetrics[0].resource.current.averageUtilization}"
    ], namespace)
    
    if result:
        parts = result.split(',')
        if len(parts) >= 2:
            current = int(parts[0]) if parts[0] else 1
            desired = int(parts[1]) if parts[1] else 1
            cpu_usage = int(parts[2]) if len(parts) > 2 and parts[2] else 0
            return {"current": current, "desired": desired, "cpu": cpu_usage}
    
    return {"current": 1, "desired": 1, "cpu": 0}

def start_cpu_stress(intensity=70, duration=120, stress_port=8081):
    """Start CPU stress test via API"""
    stress_url = f"http://localhost:{stress_port}/api/stress"
    
    try:
        response = requests.post(stress_url, json={
            "intensity": intensity,
            "duration": duration
        }, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to start stress test: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to stress service: {e}")
        return None

def stop_cpu_stress(stress_port=8081):
    """Stop CPU stress test via API"""
    stress_url = f"http://localhost:{stress_port}/api/stress"
    
    try:
        response = requests.delete(stress_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to stop stress test: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to stress service: {e}")
        return None

def monitor_scaling_progress(duration=300, check_interval=5):
    """Monitor scaling progress during test"""
    print(f"📊 Monitoring scaling progress for {duration} seconds...")
    print("=" * 60)
    
    start_time = time.time()
    initial_pods = check_pod_count()
    max_pods_seen = initial_pods
    
    print(f"{'Time':<8} {'Pods':<6} {'HPA Current':<12} {'HPA Desired':<12} {'CPU %':<8} {'Status'}")
    print("-" * 60)
    
    while time.time() - start_time < duration:
        elapsed = int(time.time() - start_time)
        current_pods = check_pod_count()
        hpa_status = check_hpa_status()
        
        max_pods_seen = max(max_pods_seen, current_pods)
        
        # Determine status
        if hpa_status["current"] < hpa_status["desired"]:
            status = "Scaling Up"
        elif hpa_status["current"] > hpa_status["desired"]:
            status = "Scaling Down"
        else:
            status = "Stable"
        
        time_str = f"{elapsed//60}:{elapsed%60:02d}"
        
        print(f"{time_str:<8} {current_pods:<6} {hpa_status['current']:<12} {hpa_status['desired']:<12} {hpa_status['cpu']:<8} {status}")
        
        time.sleep(check_interval)
    
    final_pods = check_pod_count()
    
    print("=" * 60)
    print(f"📈 Scaling Summary:")
    print(f"   Initial Pods: {initial_pods}")
    print(f"   Final Pods:   {final_pods}")
    print(f"   Max Pods:     {max_pods_seen}")
    print(f"   Scale Factor: {max_pods_seen / initial_pods:.1f}x")

def run_light_load_test():
    """Run a light load test (30% intensity)"""
    print("🟢 LIGHT LOAD TEST")
    print("=" * 50)
    print("📊 Configuration:")
    print("   Intensity: 30%")
    print("   Duration:  60 seconds")
    print("   Expected:  Minimal scaling (1-2 pods)")
    print()
    
    # Setup port forwarding
    print("🔧 Setting up port forwarding...")
    pf_thread = port_forward_service("cpu-stress-service", 8081, 8080)
    
    # Start stress test
    print("🚀 Starting light CPU stress...")
    result = start_cpu_stress(intensity=30, duration=60)
    
    if result:
        print(f"✅ Stress test started: {result}")
        monitor_scaling_progress(duration=90, check_interval=3)
    else:
        print("❌ Failed to start stress test")

def run_heavy_load_test():
    """Run a heavy load test (70% intensity)"""
    print("🟡 HEAVY LOAD TEST")
    print("=" * 50)
    print("📊 Configuration:")
    print("   Intensity: 70%")
    print("   Duration:  120 seconds")
    print("   Expected:  Significant scaling (3-5 pods)")
    print()
    
    # Setup port forwarding
    print("🔧 Setting up port forwarding...")
    pf_thread = port_forward_service("cpu-stress-service", 8081, 8080)
    
    # Start stress test
    print("🚀 Starting heavy CPU stress...")
    result = start_cpu_stress(intensity=70, duration=120)
    
    if result:
        print(f"✅ Stress test started: {result}")
        monitor_scaling_progress(duration=150, check_interval=5)
    else:
        print("❌ Failed to start stress test")

def run_chaos_attack():
    """Run a chaos attack (90% intensity)"""
    print("🔴 CHAOS ATTACK SIMULATION")
    print("=" * 50)
    print("📊 Configuration:")
    print("   Intensity: 90%")
    print("   Duration:  180 seconds")
    print("   Expected:  Maximum scaling (8-10 pods)")
    print()
    print("⚠️  This test will push the system to its limits!")
    
    # Setup port forwarding
    print("🔧 Setting up port forwarding...")
    pf_thread = port_forward_service("cpu-stress-service", 8081, 8080)
    
    # Start stress test
    print("💥 Launching chaos attack...")
    result = start_cpu_stress(intensity=90, duration=180)
    
    if result:
        print(f"✅ Chaos attack launched: {result}")
        monitor_scaling_progress(duration=210, check_interval=5)
    else:
        print("❌ Failed to launch chaos attack")

def run_custom_load_test(intensity, duration, ramp_up=False):
    """Run a custom load test with specified parameters"""
    print(f"🎯 CUSTOM LOAD TEST")
    print("=" * 50)
    print("📊 Configuration:")
    print(f"   Intensity: {intensity}%")
    print(f"   Duration:  {duration} seconds")
    print(f"   Ramp Up:   {'Yes' if ramp_up else 'No'}")
    
    expected_pods = 1
    if intensity >= 80:
        expected_pods = "8-10"
    elif intensity >= 60:
        expected_pods = "4-6"
    elif intensity >= 40:
        expected_pods = "2-3"
    
    print(f"   Expected:  {expected_pods} pods")
    print()
    
    # Setup port forwarding
    print("🔧 Setting up port forwarding...")
    pf_thread = port_forward_service("cpu-stress-service", 8081, 8080)
    
    if ramp_up:
        print("📈 Starting with ramp-up pattern...")
        # Gradual ramp up
        for ramp_intensity in range(20, intensity + 1, 20):
            print(f"   Ramping to {ramp_intensity}%...")
            start_cpu_stress(intensity=ramp_intensity, duration=30)
            time.sleep(35)
    
    # Start main stress test
    print(f"🚀 Starting main stress test at {intensity}%...")
    result = start_cpu_stress(intensity=intensity, duration=duration)
    
    if result:
        print(f"✅ Custom stress test started: {result}")
        monitor_scaling_progress(duration=duration + 30, check_interval=5)
    else:
        print("❌ Failed to start custom stress test")

def run_scale_down_test():
    """Test scale-down behavior after load removal"""
    print("🔽 SCALE-DOWN TEST")
    print("=" * 50)
    print("📊 This test will:")
    print("   1. Create high load to scale up")
    print("   2. Stop load suddenly")
    print("   3. Monitor scale-down behavior")
    print()
    
    # Setup port forwarding
    print("🔧 Setting up port forwarding...")
    pf_thread = port_forward_service("cpu-stress-service", 8081, 8080)
    
    # Phase 1: Scale up
    print("📈 Phase 1: Scaling up with high load...")
    result = start_cpu_stress(intensity=80, duration=90)
    
    if result:
        print("✅ High load started")
        time.sleep(45)  # Wait for some scaling
        
        current_pods = check_pod_count()
        print(f"📊 Current pods after scale-up: {current_pods}")
        
        # Phase 2: Stop load and monitor scale down
        print("\n🛑 Phase 2: Stopping load and monitoring scale-down...")
        stop_result = stop_cpu_stress()
        
        if stop_result:
            print("✅ Load stopped")
            print("⏳ Monitoring scale-down (this may take 2-3 minutes)...")
            monitor_scaling_progress(duration=300, check_interval=10)
        else:
            print("❌ Failed to stop load")
    else:
        print("❌ Failed to start initial load")

def interactive_load_testing():
    """Interactive load testing mode"""
    print("🎮 INTERACTIVE LOAD TESTING MODE")
    print("=" * 50)
    
    # Setup port forwarding
    print("🔧 Setting up port forwarding...")
    pf_thread = port_forward_service("cpu-stress-service", 8081, 8080)
    
    while True:
        print("\n📋 Available Commands:")
        print("   1. Light Load (30%)")
        print("   2. Medium Load (50%)")
        print("   3. Heavy Load (70%)")
        print("   4. Chaos Attack (90%)")
        print("   5. Custom Load")
        print("   6. Stop Current Load")
        print("   7. Check Status")
        print("   8. Monitor Real-time")
        print("   9. Exit")
        
        choice = input("\n🎯 Enter your choice (1-9): ").strip()
        
        if choice == "1":
            start_cpu_stress(intensity=30, duration=60)
            print("✅ Light load started for 60 seconds")
        elif choice == "2":
            start_cpu_stress(intensity=50, duration=90)
            print("✅ Medium load started for 90 seconds")
        elif choice == "3":
            start_cpu_stress(intensity=70, duration=120)
            print("✅ Heavy load started for 120 seconds")
        elif choice == "4":
            start_cpu_stress(intensity=90, duration=180)
            print("✅ Chaos attack started for 180 seconds")
        elif choice == "5":
            try:
                intensity = int(input("Enter intensity (10-100): "))
                duration = int(input("Enter duration (seconds): "))
                start_cpu_stress(intensity=intensity, duration=duration)
                print(f"✅ Custom load started: {intensity}% for {duration}s")
            except ValueError:
                print("❌ Invalid input")
        elif choice == "6":
            stop_cpu_stress()
            print("✅ Load stopped")
        elif choice == "7":
            pods = check_pod_count()
            hpa = check_hpa_status()
            print(f"📊 Current Status:")
            print(f"   Pods: {pods}")
            print(f"   HPA: {hpa['current']}/{hpa['desired']} replicas")
            print(f"   CPU: {hpa['cpu']}%")
        elif choice == "8":
            print("📊 Starting 60-second real-time monitoring...")
            monitor_scaling_progress(duration=60, check_interval=3)
        elif choice == "9":
            print("👋 Exiting interactive mode")
            break
        else:
            print("❌ Invalid choice")

def main():
    parser = argparse.ArgumentParser(description="Enhanced Load Testing for Auto-scaling")
    parser.add_argument("test_type", nargs="?", default="interactive",
                       choices=["light", "heavy", "chaos", "custom", "scale-down", "interactive"],
                       help="Type of load test to run")
    parser.add_argument("--duration", "-d", type=int, default=120,
                       help="Test duration in seconds")
    parser.add_argument("--ramp-up", "-r", action="store_true",
                       help="Use gradual ramp-up pattern")
    parser.add_argument("--monitor-only", "-m", action="store_true",
                       help="Only monitor scaling without starting load")
    
    args = parser.parse_args()
    
    print("🚀 ENHANCED AUTO-SCALING LOAD TESTER")
    print("=" * 60)
    print(f"🎯 Test Type: {args.test_type.upper()}")
    print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if args.monitor_only:
        print("📊 Monitor-only mode - watching scaling behavior...")
        monitor_scaling_progress(duration=args.duration, check_interval=5)
        return
    
    # Check initial state
    initial_pods = check_pod_count()
    initial_hpa = check_hpa_status()
    
    print("📊 Initial State:")
    print(f"   Pods: {initial_pods}")
    print(f"   HPA Current/Desired: {initial_hpa['current']}/{initial_hpa['desired']}")
    print(f"   CPU Usage: {initial_hpa['cpu']}%")
    print()
    
    # Run the selected test
    if args.test_type == "light":
        run_light_load_test()
    elif args.test_type == "heavy":
        run_heavy_load_test()
    elif args.test_type == "chaos":
        run_chaos_attack()
    elif args.test_type == "custom":
        run_custom_load_test(args.intensity, args.duration, args.ramp_up)
    elif args.test_type == "scale-down":
        run_scale_down_test()
    elif args.test_type == "interactive":
        interactive_load_testing()
    
    # Final state check
    if args.test_type != "interactive":
        print("\n" + "=" * 60)
        print("📈 FINAL RESULTS")
        print("=" * 60)
        
        final_pods = check_pod_count()
        final_hpa = check_hpa_status()
        
        print("📊 Final State:")
        print(f"   Pods: {final_pods}")
        print(f"   HPA Current/Desired: {final_hpa['current']}/{final_hpa['desired']}")
        print(f"   CPU Usage: {final_hpa['cpu']}%")
        print()
        
        print("📈 Test Summary:")
        print(f"   Initial Pods: {initial_pods}")
        print(f"   Final Pods:   {final_pods}")
        
        if final_pods > initial_pods:
            scale_factor = final_pods / initial_pods
            print(f"   ✅ Scaling UP successful! Scale factor: {scale_factor:.1f}x")
        elif final_pods < initial_pods:
            print(f"   ✅ Scaling DOWN successful!")
        else:
            print(f"   ℹ️  No scaling occurred")
        
        print()
        print("🎯 Next Steps:")
        print("   • Monitor scale-down with: python3 enhanced-monitor-scaling.py monitor")
        print("   • View dashboard at: http://localhost:31003")
        print("   • Check HPA status: kubectl get hpa -n scaling-challenge")
        print("   • Watch pods: kubectl get pods -n scaling-challenge -w")

if __name__ == "__main__":
    main()intensity", "-i", type=int, default=50,
                       help="Load intensity percentage (10-100)")
    parser.add_argument("--