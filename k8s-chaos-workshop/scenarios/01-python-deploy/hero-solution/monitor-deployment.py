#!/usr/bin/env python3
"""
📊 PYTHON HERO MONITORING SYSTEM
Real-time deployment monitoring - Never miss what's happening!
"""

import time
import json
from datetime import datetime
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from colorama import init, Fore, Style

init(autoreset=True)

class VoteAppMonitor:
    """Real-time monitoring for the vote app deployment"""
    
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.namespace = "vote-app"
        self.app_name = "vote-app"
    
    def get_deployment_status(self):
        """Get current deployment status"""
        try:
            deployment = self.apps_v1.read_namespaced_deployment(
                name=self.app_name,
                namespace=self.namespace
            )
            
            return {
                "name": deployment.metadata.name,
                "replicas": deployment.spec.replicas,
                "ready_replicas": deployment.status.ready_replicas or 0,
                "available_replicas": deployment.status.available_replicas or 0,
                "updated_replicas": deployment.status.updated_replicas or 0,
                "conditions": deployment.status.conditions or []
            }
        except ApiException:
            return None
    
    def get_pod_status(self):
        """Get status of all pods"""
        try:
            pods = self.v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"app={self.app_name}"
            )
            
            pod_info = []
            for pod in pods.items:
                # Get container status
                container_status = "Unknown"
                restart_count = 0
                
                if pod.status.container_statuses:
                    container = pod.status.container_statuses[0]
                    restart_count = container.restart_count or 0
                    
                    if container.ready:
                        container_status = "Ready"
                    elif container.state.waiting:
                        container_status = f"Waiting: {container.state.waiting.reason}"
                    elif container.state.running:
                        container_status = "Running"
                    elif container.state.terminated:
                        container_status = f"Terminated: {container.state.terminated.reason}"
                
                pod_info.append({
                    "name": pod.metadata.name,
                    "phase": pod.status.phase,
                    "node": pod.spec.node_name,
                    "pod_ip": pod.status.pod_ip,
                    "container_status": container_status,
                    "restart_count": restart_count,
                    "created": pod.metadata.creation_timestamp
                })
            
            return pod_info
        except ApiException:
            return []
    
    def get_service_status(self):
        """Get service status and endpoints"""
        try:
            service = self.v1.read_namespaced_service(
                name=f"{self.app_name}-service",
                namespace=self.namespace
            )
            
            return {
                "name": service.metadata.name,
                "type": service.spec.type,
                "cluster_ip": service.spec.cluster_ip,
                "ports": [
                    {
                        "port": port.port,
                        "target_port": port.target_port,
                        "node_port": port.node_port if port.node_port else None
                    }
                    for port in service.spec.ports
                ]
            }
        except ApiException:
            return None
    
    def display_status(self):
        """Display current status in a nice format"""
        print(f"\n{Fore.CYAN}📊 VOTE APP MONITORING DASHBOARD{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
        
        # Deployment Status
        deployment = self.get_deployment_status()
        if deployment:
            print(f"\n{Fore.YELLOW}🚀 DEPLOYMENT STATUS:{Style.RESET_ALL}")
            print(f"   Name: {deployment['name']}")
            print(f"   Desired Replicas: {deployment['replicas']}")
            print(f"   Ready Replicas: {deployment['ready_replicas']}")
            print(f"   Available: {deployment['available_replicas']}")
            print(f"   Updated: {deployment['updated_replicas']}")
            
            # Health indicator
            if deployment['ready_replicas'] == deployment['replicas']:
                print(f"   Status: {Fore.GREEN}✅ HEALTHY{Style.RESET_ALL}")
            else:
                print(f"   Status: {Fore.YELLOW}⏳ SCALING{Style.RESET_ALL}")
        
        # Pod Status
        pods = self.get_pod_status()
        if pods:
            print(f"\n{Fore.YELLOW}📦 POD STATUS:{Style.RESET_ALL}")
            for pod in pods:
                status_color = Fore.GREEN if pod['phase'] == 'Running' else Fore.YELLOW
                print(f"   {status_color}• {pod['name'][:25]:<25}{Style.RESET_ALL} | "
                      f"Phase: {pod['phase']:<10} | "
                      f"Restarts: {pod['restart_count']}")
        
        # Service Status
        service = self.get_service_status()
        if service:
            print(f"\n{Fore.YELLOW}🌐 SERVICE STATUS:{Style.RESET_ALL}")
            print(f"   Name: {service['name']}")
            print(f"   Type: {service['type']}")
            print(f"   Cluster IP: {service['cluster_ip']}")
            for port_info in service['ports']:
                if port_info['node_port']:
                    print(f"   Access: http://localhost:{port_info['node_port']}")
    
    def monitor_continuously(self, interval=10):
        """Monitor continuously with specified interval"""
        print(f"{Fore.MAGENTA}🔍 Starting continuous monitoring (Press Ctrl+C to stop){Style.RESET_ALL}")
        
        try:
            while True:
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                self.display_status()
                
                print(f"\n{Fore.CYAN}⏰ Next update in {interval} seconds...{Style.RESET_ALL}")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}👋 Monitoring stopped. Vote app is still running!{Style.RESET_ALL}")

def main():
    """Main monitoring function"""
    monitor = VoteAppMonitor()
    
    print(f"{Fore.CYAN}📊 Vote App Monitoring System{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Choose monitoring mode:{Style.RESET_ALL}")
    print(f"   1. One-time status check")
    print(f"   2. Continuous monitoring")
    
    choice = input(f"\n{Fore.YELLOW}Enter choice (1 or 2): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        monitor.display_status()
    elif choice == "2":
        monitor.monitor_continuously()
    else:
        print(f"{Fore.RED}Invalid choice. Running one-time check.{Style.RESET_ALL}")
        monitor.display_status()

if __name__ == "__main__":
    main()